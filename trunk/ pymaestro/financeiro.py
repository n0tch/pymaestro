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



import gtk
from aviso import aviso

class financeiro:
    def financa_mensal(self, dados, data):
        self.liststore_financeira.clear()
        saldo_total = 0
        self.liststore_financeira.append(("Relatório do mês:", data[:-3], "","","","",""))
        self.liststore_financeira.append(("", "Data"," Horario","Cliente","Valor cobrado",
                                          "Valor Pago","Saldo"))
        for servico in dados:
            data = servico[0]
            hora = servico[1]
            cliente = servico[2]
            valor= servico[4]
            pago = servico[5]
            saldo = pago - valor
            saldo_total += saldo
            self.liststore_financeira.append(("",str(data), str(hora), str(cliente), str(valor), 
                                             str(pago), str(saldo)))

        self.liststore_financeira.append(("","Saldo Final", "","","","",str(saldo_total)))
        self.mostrar_relatorio()

    def financa_pessoal(self, dados):        
        self.liststore_financeira.clear()
        if len(dados) == 0:
            self.aviso.mostrar_aviso("O Cliente selecionado não possui agendamentos")
            return

        motivo = str(dados[0][2])
        saldo_total = 0
        self.liststore_financeira.append(("Relatório do Cliente:", motivo, "","","","",""))
        self.liststore_financeira.append(("", "Data","Horario","Valor cobrado",
                                            "Valor Pago","Saldo", ""))
        for servico in dados:
            data = servico[0]
            hora = servico[1]
            valor= servico[4]
            pago = servico[5]
            saldo = pago - valor
            saldo_total += saldo
            self.liststore_financeira.append(("",str(data), str(hora), str(valor), 
                                             str(pago), str(saldo), ""))

        self.liststore_financeira.append(("","Saldo Final", "","","","",str(saldo_total)))
        self.mostrar_relatorio()

    def get_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._A_nome_do_widget"""
        widget_names = ["janela_informacoes_financeiras", "treeview_financeira",
                        "botao_imprimir_relatorio", "fechar_janela_financeira" ]

        for widget_name in widget_names:
            setattr(self, "_" + widget_name, self.glade_xml.get_widget(widget_name))

    def imprimir_relatorio(self, *args):
        print "Ferramenta não disponível"

    def fechar_janela_financeira(self,*args):
        self._janela_informacoes_financeiras.hide()

    def abrir_janela_financeira(self, *args):
        self._janela_informacoes_financeiras.show()

    def mostrar_relatorio(self, *args):
        self.abrir_janela_financeira()            
    
    def __init__ (self):
        self.glade_xml= gtk.glade.XML("gui/financeiro.glade")
        # -- Dicionario com as funcoes callback
        funcoes_callback= {"botao_imprimir_relatorio_clicked": self.imprimir_relatorio,
                           "fechar_janela_financeira_clicked": self.fechar_janela_financeira}
        self.get_widgets()
        self.glade_xml.signal_autoconnect(funcoes_callback)
        # -- Liststore que apresentara os dados dos clientes
        self.liststore_financeira = gtk.ListStore(str, str, str, str, str, str, str)
        # -- Passando a liststore para a treeview
        self._treeview_financeira.set_model(self.liststore_financeira)
        # -- Criando as colunas da treeview
        self.tv_coluna_1 = gtk.TreeViewColumn()
        self.tv_coluna_2 = gtk.TreeViewColumn()

        # -- Adicionando as colunas na treeview
        self._treeview_financeira.append_column(self.tv_coluna_1)
        self._treeview_financeira.append_column(self.tv_coluna_2)

        # -- Confirgurando a Treeview
        self._treeview_financeira.set_rules_hint(True)

        # -- Criando os CellRenderers
        self.celula_motivo = gtk.CellRendererText()
        self.celula_data = gtk.CellRendererText()
        self.celula_horario = gtk.CellRendererText()
        self.celula_cliente = gtk.CellRendererText()
        self.celula_valor = gtk.CellRendererText()
        self.celula_pago = gtk.CellRendererText()
        self.celula_saldo = gtk.CellRendererText()

        # -- Associando as celulas as colunas 
        self.tv_coluna_1.pack_start(self.celula_motivo)
        self.tv_coluna_2.pack_start(self.celula_data)
        self.tv_coluna_2.pack_start(self.celula_horario)
        self.tv_coluna_2.pack_start(self.celula_cliente)
        self.tv_coluna_2.pack_start(self.celula_valor)
        self.tv_coluna_2.pack_start(self.celula_pago)
        self.tv_coluna_2.pack_start(self.celula_saldo)

        # -- Determinando os dados das colunas
        self.tv_coluna_1.set_attributes(self.celula_motivo, text=0)
        self.tv_coluna_2.set_attributes(self.celula_data, text=1)
        self.tv_coluna_2.set_attributes(self.celula_horario, text=2)
        self.tv_coluna_2.set_attributes(self.celula_cliente, text=3)
        self.tv_coluna_2.set_attributes(self.celula_valor, text=4)
        self.tv_coluna_2.set_attributes(self.celula_pago, text=5)
        self.tv_coluna_2.set_attributes(self.celula_saldo, text=6)
        self.aviso = aviso()

