"""
    pyMaestro is a tool for organizing professional appointments

    Copyright (C) 2007 Frederico Gonzalez Colombo Arnoldi<fredgca@hotmail.com>

    This file is part of pyMaestro.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Please send bugreports with examples or suggestions to fredgca@hotmail.com

"""



import pygtk, gtk.glade
from bd import banco_de_dados
from aviso import aviso
from financeiro import financeiro

class Interface:
    """Sistema de cadastro e agendamento de clientes"""
    ##################Metodos Login####################
    def get_login_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._l_nome_do_widget"""
        widget_names = ["botao_logar", "login_dialog", "usuario_entry", "senha_entry"]
        for widget_name in widget_names:
            setattr(self, "_l_" + widget_name, self.login_glade_xml.get_widget(widget_name))

    def efetuar_login(self,*args):            
        nome = self._l_usuario_entry.get_text()
        senha = self._l_senha_entry.get_text()
        self.aviso = aviso()
        try:
            self.bd = banco_de_dados(nome, senha)
            self._l_login_dialog.hide()        
            # -- Carrega os dados de todos os clientes cadastrados no banco de dados
            self.todos_clientes = self.bd.carregar_todos_clientes()
            # -- Inicializa o sistema de cadastro e agendamento de clientes
            self.inicializar_agenda()
            self.inicializar_cadastro_de_clientes()
            self._A_janela_agenda.show()
            self.financeiro = financeiro()
        except:
            self.aviso.mostrar_aviso("Os dados que você inseriu não conferem")
            self._l_usuario_entry.set_text("")
            self._l_senha_entry.set_text("")

    ##################Metodos do sistema de cadastro de clientes####################
    def carregar_dados_na_gui(self, campos, dados):
        """Recebe duas listas: uma com os campos, e outra com os dados dos campos.
            Imprime na GUI o campo e seu respectivo dado"""
        for linha in range(len(campos)):
            self.clientes_liststore.append([campos[linha], dados[linha]])

    def abrir_janela_clientes(self,*args):     
        self._c_botao_usar_cadastro.set_sensitive(False)
        self._c_janela_de_clientes.show()

    def ir_cliente_anterior(self,*args):
        """ Retrocede na lista de todos os clientes cadastrados e apresenta na tela """

        self._c_botao_usar_cadastro.set_sensitive(True)

        if len(self.todos_clientes) > 0:
            if self.indice_visualizacao_cadastro > -len(self.todos_clientes)+1:
                self.indice_visualizacao_cadastro += -1
            else:
                self.indice_visualizacao_cadastro += -1 + len(self.todos_clientes)
        
            self.clientes_liststore.clear()
            self.carregar_dados_na_gui(self.campos_de_dados, self.todos_clientes[self.indice_visualizacao_cadastro])

    def ir_proximo_cliente(self,*args):
        """ Avanca na lista de todos os clientes cadastrados e apresenta na tela """
        self._c_botao_usar_cadastro.set_sensitive(True)

        if len(self.todos_clientes) > 0:
            if self.indice_visualizacao_cadastro < len(self.todos_clientes)-1:
                self.indice_visualizacao_cadastro += 1
            else:
                self.indice_visualizacao_cadastro += 1
                self.indice_visualizacao_cadastro -= len(self.todos_clientes)
           
            self.clientes_liststore.clear()
            self.carregar_dados_na_gui(self.campos_de_dados, self.todos_clientes[self.indice_visualizacao_cadastro])


    def procurar_cliente(self,*args):
        """Esse metodo executa a busca de um cliente no banco de dados"""
        campo_de_busca = self._c_campo_de_busca_combobox.get_active_text() #indentifica por qual campo a busca sera realizado
        dado_para_busca = self._c_busca_cliente_entry.get_text()# pega o dado chave para a busca
        if dado_para_busca == "":
            self.aviso.mostrar_aviso("Você não preencheu os dados para busca.")
            return

        clientes_encontrados = self.bd.buscar_cliente(campo_de_busca,dado_para_busca)
        self.clientes_liststore.clear()
        # -- Se nenhum resultado foi encontrado
        if len(clientes_encontrados) == 0: 
           self.carregar_dados_na_gui([""], ["Desculpe, nenhum cliente foi encontrado com esses dados"]) 
           self._c_botao_usar_cadastro.set_sensitive(True)
        # --  Se apenas um resultado foi encontrado
        elif len(clientes_encontrados) == 1: 
           self._c_botao_usar_cadastro.set_sensitive(True)
           self.carregar_dados_na_gui(self.campos_de_dados, clientes_encontrados[0]) 
        # -- Se mais de um resultado foi encontrado
        else: 
            self._c_botao_usar_cadastro.set_sensitive(False)
            texto_n_clientes = "Sua consulta encontrou %i clientes" %len(clientes_encontrados) 
            self.clientes_liststore.append(["",texto_n_clientes])
            for resultado_n in range(len(clientes_encontrados)): # Para cada cliente encontrado
                self.clientes_liststore.append(["",""]) #adiciona uma linha em branco
                self.carregar_dados_na_gui(self.campos_de_dados, clientes_encontrados[resultado_n]) # carrega os dados do cliente na gui


    def criar_novo_cliente(self,*args):
        """Esse metodo limpa os dados de todos os campos, induzindo o usuario a inserir
           os dados de um novo cliente. Se, ao final, o usuario nao salvar as alteracoes, 
           esse metodo nao altera o banco de dados"""
        self.clientes_liststore.clear()
        for campo in range(len(self.campos_de_dados)):
            if self.campos_de_dados[campo] == "ID":
                self.clientes_liststore.append([self.campos_de_dados[campo], "Nao alterar"])
            else:                
                self.clientes_liststore.append([self.campos_de_dados[campo], "Campo Vazio"])

    def carregar_todos_clientes(self, *args):
        """Esse metodo carrega todos os clientes cadastrados no banco de dados"""
        self.todos_clientes = self.bd.carregar_todos_clientes()

    def gravar(self,*args):
        """Metodo que recupera os dados da Interface e salva no banco de dados"""
        dados_novo_cliente = self.carregar_dados_da_gui() 
        self.bd.cadastrar_cliente(dados_novo_cliente)
        self.ir_proximo_cliente()
        self.carregar_todos_clientes()

    def carregar_dados_da_gui(self, *args):
        """Funcao que extrai os dados da Interface"""
        novos_dados = []
        self.selecao_dados_clientes.select_all() #seleciona todas as linhas da treeview
        (model, paths) = self.selecao_dados_clientes.get_selected_rows()
        for path in paths: #pega o conteudo de cada linha
            kiter = model.get_iter(path)
            campo = model.get_value(kiter,0)	
            dado_do_campo = model.get_value(kiter,1)
            if campo == "ID": # caso o campo seja ID
                if dado_do_campo == "Nao alterar": # se o dado dessa linha for de um novo cliente
                    novos_dados.append("NULL") #deixa o mysql incrementar automaticamente
                else:
                    novos_dados.append(int(dado_do_campo)) # caso contrario passa o ID do cliente

            else: # para todos os demais campos, salva-se os dados
                novos_dados.append(dado_do_campo)

        return novos_dados

    def apagar_cliente(self,*args):
        """Funcao executada quando o botao apagar_cliente eh clicado"""
        dados_cliente_completo = self.carregar_dados_da_gui() # carrega os dados da gui
        dados_cliente = (dados_cliente_completo[1],dados_cliente_completo[4]) # seleciona nome e rg
        self.bd.apagar_cliente(dados_cliente) # apagar o registro com aquele nome e rg
        self.carregar_todos_clientes() #recarrega os dados de todos os clientes, agora sem o excluido
        self.ir_proximo_cliente()

    def fechar_janela_clientes(self,*args):
        self._c_janela_de_clientes.hide()
        return True

    def usar_cadastro(self, *args):
        """Esse metodo pega o cadastro de um cliente no sistema de Cadastro e o passa para o sistema de agendamento"""
        dados_do_cliente = self.carregar_dados_da_gui() 
        cadastro_selecionado = dados_do_cliente[1]
        self._A_cliente_para_agendamento_entry.set_text(cadastro_selecionado)
        self._c_janela_de_clientes.hide()

    def get_clientes_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._c_nome_do_widget"""
        widget_names = ["janela_de_clientes","dados_clientes_treeview", "botao_cliente_anterior", "botao_proximo_cliente", "botao_gravar", "botao_apagar_cliente", "botao_sair_janela_cliente", "botao_procurar_cliente", "botao_novo_cliente", "busca_cliente_entry", "campo_de_busca_combobox", "botao_usar_cadastro"]
        for widget_name in widget_names:
            setattr(self, "_c_" + widget_name, self.cliente_glade_xml.get_widget(widget_name))

    def edicao_dos_dados(self, cell, path, new_text, model):
        """Quando uma linha do treeview eh editada, as alteracoes sao salvas por esse metodo"""
        model[path][1] = new_text
        return

    def financa_cliente(self, *args):
        dados = self.carregar_dados_da_gui()
        resultado = self.bd.procurar_agendamento_nome(dados[1])
        self.financeiro.financa_pessoal(resultado)

    ##################Metodos da Agenda####################
    def criar_backup(self,*args):
        self.bd.criar_backup()

    def financa_mensal(self, *args):
        data = self.pegar_data_gui()
        resultado = self.bd.procurar_agendamentos_mes(data)
        self.financeiro.financa_mensal(resultado, data)

    
    def carregar_dados_na_gui(self, campos, dados):
        """Recebe duas listas: uma com os campos, e outra com os dados dos campos.
            Imprime na GUI o campo e seu respectivo dado"""
        for linha in range(len(campos)):
            self.clientes_liststore.append([campos[linha], dados[linha]])

    def get_agenda_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._A_nome_do_widget"""
        widget_names = ["janela_agenda","calendario", "botao_adicionar_agendamento", "botao_sair_agenda", "botao_remover_agendamento", "treeview_de_agendamento", "cliente_para_agendamento_entry", "observacao_entry", "horarios_combo", "botao_agendar", "valor_consulta_entry", "valor_pago_entry", "botao_salvar_modificacoes_agendamento", "botao_selecionar_cadastro", "dados_hbox", "botao_abrir_cadastro", "botao_backup"]
        for widget_name in widget_names:
            setattr(self, "_A_" + widget_name, self.agenda_glade_xml.get_widget(widget_name))

    def resetar_quadro_agendamento(self,*args):
        self._A_cliente_para_agendamento_entry.set_text("Use o botao ->")
        self._A_observacao_entry.set_text("--- --- --- ---")
        self._A_valor_consulta_entry.set_text("0.0")
        self._A_valor_pago_entry.set_text("0.0")
        self._A_horarios_combo.set_active(0)

    def ativar_quadro_agendamento(self, *args):
        self._A_horarios_combo.set_sensitive(True)
        self._A_botao_salvar_modificacoes_agendamento.set_sensitive(False)
        self._A_botao_agendar.set_sensitive(True)
        self._A_botao_selecionar_cadastro.set_sensitive(True)
        self.resetar_quadro_agendamento()
        self._A_dados_hbox.set_sensitive(True)

    def desativar_quadro_agendamento(self, *args):
        self.resetar_quadro_agendamento()
        self._A_dados_hbox.set_sensitive(False)

    def abrir_janela_agenda(self, *args):
        self._A_janela_agenda.show()

    def encerrar_programa(self,*args):
        gtk.main_quit()

    def get_active_text(combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def selecionar_cadastro(self,*args):
        self._c_janela_de_clientes.show()

    def atualizar_agenda(self, compromissos):        
        self.agenda_liststore.clear()
        for compromisso in compromissos:
            self.agenda_liststore.append((compromisso[1], compromisso[2], compromisso[3]))
         
    def apagar_compromisso(self, *args):
        dados_compromisso = self.carrega_selecionado_treeview()
        self.bd.apagar_compromisso((dados_compromisso[0],dados_compromisso[1]))
        self.mostrar_compromissos_diario()

    def carrega_selecionado_treeview(self): 
        linhas_selecionadas = self._A_treeview_de_agendamento.get_selection()
        data = self.pegar_data_gui()    
        (model, paths) = linhas_selecionadas.get_selected_rows()
        for path in paths:
            kiter = model.get_iter(path)
            horario = model.get_value(kiter,0)	
            nome = model.get_value(kiter,1)
            
        return (data,horario,nome)
    
    def agendar(self, *args):
        data = self.pegar_data_gui()
        cliente = self._A_cliente_para_agendamento_entry.get_text()
        obs = self._A_observacao_entry.get_text()
        horario = self._A_horarios_combo.get_active_text()
        valor_consulta = float(self._A_valor_consulta_entry.get_text())
        valor_pago = float(self._A_valor_pago_entry.get_text())
        self.bd.criar_novo_compromisso((data,horario,cliente, obs, valor_consulta, valor_pago))
        self.mostrar_compromissos_diario()
        self._A_dados_hbox.set_sensitive(False)
        self.resetar_quadro_agendamento()

    def pegar_data_gui(self, *args):
        ano, mes, dia = self._A_calendario.get_date()
        data = str(ano)+"-"+str(mes+1)+"-"+str(dia)
        return data        

    def mostrar_compromissos_diario(self, *args):
        data = self.pegar_data_gui()
        compromissos = self.bd.carregar_todos_compromissos_diario(data)
        self.atualizar_agenda(compromissos)

    def salvar_modificacoes_agendamento(self, *args):
        data = self.pegar_data_gui()
        cliente = self._A_cliente_para_agendamento_entry.get_text()
        obs = self._A_observacao_entry.get_text()
        horario = self._A_horarios_combo.get_active_text()
        valor_consulta = float(self._A_valor_consulta_entry.get_text())
        valor_pago = float(self._A_valor_pago_entry.get_text())
        self.bd.atualizar_compromisso((data,horario,cliente, obs, valor_consulta, valor_pago))
        self.mostrar_compromissos_diario()
        self._A_dados_hbox.set_sensitive(False)
        self.resetar_quadro_agendamento()

    def ativar_quadro_agendamento_com_dados(self, *args):
        indices = ["07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00","12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30"]
        data, horario, nome = self.carrega_selecionado_treeview()
        dados = self.bd.procurar_por_agendamento((data, horario))
        indice_ativo = indices.index(horario) 
        self._A_cliente_para_agendamento_entry.set_text(dados[0][2])
        self._A_observacao_entry.set_text(str(dados[0][3]))
        self._A_valor_consulta_entry.set_text(str(dados[0][4]))
        self._A_valor_pago_entry.set_text(str(dados[0][5]))
        self._A_horarios_combo.set_active(indice_ativo)
        self._A_horarios_combo.set_sensitive(False)
        self._A_botao_salvar_modificacoes_agendamento.set_sensitive(True)
        self._A_botao_selecionar_cadastro.set_sensitive(False)
        self._A_botao_agendar.set_sensitive(False)
        self._A_dados_hbox.set_sensitive(True)


############################ Inicializacao e __init__########################################
    def inicializar_cadastro_de_clientes(self):
        """Inicializa sistema de cadastro de clientes"""
        self.cliente_glade_xml = gtk.glade.XML("gui/janela_cliente.glade")
        # -- Dicionario com as funcoes callback dos sistema de cadastro 
        cliente_funcoes_callback= {
             "fechar_janela": self.fechar_janela_clientes,
             "ir_cliente_anterior": self.ir_cliente_anterior,
             "ir_proximo_cliente": self.ir_proximo_cliente,
             "procurar_cliente": self.procurar_cliente,
             "apagar_cliente": self.apagar_cliente,             
             "gravar": self.gravar,             
             "sair_janela_clientes": self.fechar_janela_clientes,
             "criar_novo_cliente": self.criar_novo_cliente,
             "botao_usar_cadastro_clicado":self.usar_cadastro,
             "botao_financa_cliente_clicado": self.financa_cliente
             }

        self.indice_visualizacao_cadastro = 0
        self.campos_de_dados = ['ID', "Nome","Endereco", "Telefone", "R.G.", "C.P.F.", "Celular", "Nascimento", "Sexo", "Observacao"]
        self.cliente_glade_xml.signal_autoconnect(cliente_funcoes_callback)
        self.get_clientes_widgets()
        self._c_janela_de_clientes.connect("delete-event", self.fechar_janela_clientes)
        # -- Liststore que apresentara os dados dos clientes
        self.clientes_liststore = gtk.ListStore(str, str)
        # -- Passando a liststore para a treeview
        self._c_dados_clientes_treeview.set_model(self.clientes_liststore)
        # -- Configurando a Treeview
        self._c_dados_clientes_treeview.set_rules_hint(True)
        self.selecao_dados_clientes = self._c_dados_clientes_treeview.get_selection()
        self.selecao_dados_clientes.set_mode(gtk.SELECTION_MULTIPLE)
        # -- Criando as colunas da treeview
        self.tv_coluna_campos = gtk.TreeViewColumn('Campos')
        self.tv_coluna_dados = gtk.TreeViewColumn('Dados dos clientes')
        # -- Adicionando as colunas na treeview
        self._c_dados_clientes_treeview.append_column(self.tv_coluna_campos)
        self._c_dados_clientes_treeview.append_column(self.tv_coluna_dados)
        # -- Criando os CellRenderers
        self.celula_campos = gtk.CellRendererText()
        self.celula_dados = gtk.CellRendererText()
        # -- Configurando as propriedades das celulas
        self.celula_campos.set_property('foreground', 'white')
        self.celula_campos.set_property('cell-background', 'dark blue')
        self.celula_campos.set_property('editable', True)
        self.celula_campos.set_property('font', 'Arial')
        self.celula_dados.set_property('editable', True)
        self.celula_dados.set_property('font', 'Arial')
        self.celula_dados.connect('edited', self.edicao_dos_dados, self.clientes_liststore)
        # -- Associando as celulas as colunas 
        self.tv_coluna_campos.pack_start(self.celula_campos)
        self.tv_coluna_dados.pack_start(self.celula_dados)
        # -- Determinando os dados das colunas
        self.tv_coluna_campos.set_attributes(self.celula_campos, markup=0)
        self.tv_coluna_dados.set_attributes(self.celula_dados, text=1)

    def iniciar_login(self):
        self.login_glade_xml= gtk.glade.XML("gui/login.glade")
        funcoes_callback_login= {
            "botao_logar_clicado": self.efetuar_login,
            "encerrar_programa": self.encerrar_programa
}
        self.get_login_widgets()
        self.login_glade_xml.signal_autoconnect(funcoes_callback_login)
        self._l_login_dialog.show()

    def inicializar_agenda(self):
        """Inicializa Sistema de agendamento de clientes"""
        self.agenda_glade_xml= gtk.glade.XML("gui/agenda.glade")
        # -- Dicionario com as funcoes callback da agenda
        funcoes_callback_agenda= {
            "fechar_janela": self.encerrar_programa,
            "botao_adicionar_agendamento_clicado": self.ativar_quadro_agendamento,
            "botao_desativar_quadro_agendamento_clicado": self.desativar_quadro_agendamento,
            "botao_agendar_clicado": self.agendar,
            "botao_sair_agenda_clicado":self.encerrar_programa,
            "botao_selecionar_cadastro_clicado": self.selecionar_cadastro,
            "data_selecionada": self.mostrar_compromissos_diario,
            "botao_remover_agendamento_clicado": self.apagar_compromisso,
            "botao_salvar_modificacoes_agendamento_clicado": self.salvar_modificacoes_agendamento,
            "abre_janela_agendamento_com_dados": self.ativar_quadro_agendamento_com_dados,
            "botao_abrir_cadastro_clicado": self.abrir_janela_clientes,
            "botao_financa_mensal_clicado": self.financa_mensal,
            "botao_backup_clicado": self.criar_backup,
             }
        self.get_agenda_widgets()
        self.agenda_glade_xml.signal_autoconnect(funcoes_callback_agenda)
        # --Configurando Treeview de Agendamento
        self.agenda_liststore = gtk.ListStore(str, str, str)
        self._A_treeview_de_agendamento.set_model(self.agenda_liststore)
        self._A_treeview_de_agendamento.set_rules_hint(True)
        # -- Criando colunas
        self.tv_coluna_cliente = gtk.TreeViewColumn('Cliente')
        self.tv_coluna_horario= gtk.TreeViewColumn('Horário')
        self.tv_coluna_obs = gtk.TreeViewColumn('Observacões')
        # -- Colocando as colunas na treeview_de_agendamento
        self._A_treeview_de_agendamento.append_column(self.tv_coluna_horario)
        self._A_treeview_de_agendamento.append_column(self.tv_coluna_cliente)
        self._A_treeview_de_agendamento.append_column(self.tv_coluna_obs)
        # -- Criando as celulas
        self.celula_cliente = gtk.CellRendererText()
        self.celula_horario = gtk.CellRendererText()
        self.celula_obs = gtk.CellRendererText()
        # -- Ligando as colunas as celulas
        self.tv_coluna_cliente.pack_start(self.celula_cliente)
        self.tv_coluna_horario.pack_start(self.celula_horario)
        self.tv_coluna_obs.pack_start(self.celula_obs)
        # -- Determinando os dados das colunas
        self.tv_coluna_cliente.set_attributes(self.celula_cliente, text=1)
        self.tv_coluna_horario.set_attributes(self.celula_horario, text=0)
        self.tv_coluna_obs.set_attributes(self.celula_obs, text=2)
        self._A_janela_agenda.connect("delete-event", self.encerrar_programa)
        self.mostrar_compromissos_diario()
        self._A_dados_hbox.set_sensitive(False)
        self._A_cliente_para_agendamento_entry.set_editable(False)


            
    def __init__ (self):
        """Sistema de cadastro e agendamento de clientes"""
        self.iniciar_login()

if __name__ == "__main__":		
    Interface()
    gtk.main()		

		
