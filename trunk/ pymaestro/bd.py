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



import os
import MySQLdb
from aviso import aviso
class banco_de_dados:
    """Essa classe encapsula todas as funções relativas ao cadastro de clientes e agendamento de compromissos no banco de dados MySQL"""

    #############Funções sobre compromissos #############
    def criar_novo_compromisso(self,dados_agendamento):
        """data, horario, nome, obs, valor, pago"""
        compromisso_conflitante = self.procurar_por_agendamento((dados_agendamento[0],dados_agendamento[1]))
        if compromisso_conflitante:
            if compromisso_conflitante[0][2] == dados_agendamento[2]:
                self.aviso.mostrar_aviso("Esse compromisso já está agendado")
            else:
                self.aviso.mostrar_aviso("Existe outro compromisso marcado para esse horário.\n Se desejar alterá-lo, remova-o e adicione um novo")
        else:
            self.cursor.execute("insert into agenda values ('%s','%s','%s','%s' ,%f,%f)" %dados_agendamento)
            self.db.commit()

    def atualizar_compromisso(self,dados_agendamento):
        """data, horario, nome, obs, valor, pago"""
        self.cursor.execute("replace into agenda values ('%s','%s','%s','%s' ,%f,%f)" %dados_agendamento)
        self.db.commit()


    def apagar_compromisso(self,dados_agendamento):
        """Apaga o registro do banco de dados pela data e horario"""
        self.cursor.execute("delete from agenda where data = %s and horario= %s", dados_agendamento)
        self.db.commit()

    def procurar_por_agendamento(self, data_e_hora):
        self.cursor.execute("select * from agenda where data = %s and horario = %s", data_e_hora)
        resultado_da_busca = self.cursor.fetchall()
        return resultado_da_busca

    def procurar_agendamento_nome(self, nome):
        self.cursor.execute("select * from agenda where nome = %s ", nome)
        resultado_da_busca = self.cursor.fetchall()
        return resultado_da_busca
    
    def procurar_agendamentos_mes(self, data):
        comando = "select * from agenda where data rlike \'^%s\' " %data[:-2]
        self.cursor.execute(comando)
        resultado_da_busca = self.cursor.fetchall()
        return resultado_da_busca

    def carregar_todos_compromissos_diario(self, data):
        """Carrega todos os compromissos de determinado dia"""
        self.cursor.execute("select * from agenda where data = %s order by horario asc", data)
        self.agendamentos_diario = self.cursor.fetchall()
        return self.agendamentos_diario

    ########### Funções sobre o cadastro de clientes ########################
    def cadastrar_cliente(self,dados_novo_cliente):# nome, endereco, telefone, rg, cpf, celular, nascimento, sexo, observacao):
        """ID,nome, endereco, telefone, rg, cpf, celular, nascimento, sexo, observacao"""
        if dados_novo_cliente[0] == "NULL":
            self.cursor.execute("insert into clientes values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)", dados_novo_cliente[1:])#(nome, endereco, telefone, rg, cpf, celular, nascimento, sexo, observacao))
            self.db.commit()
        else:
            self.cursor.execute("replace into clientes values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", dados_novo_cliente)#(nome, endereco, telefone, rg, cpf, celular, nascimento, sexo, observacao))
            self.db.commit()

    def apagar_cliente(self,dados_cliente):
        """Apaga o registro do banco de dados pelo nome e rg do cadastro"""
        self.cursor.execute("delete from clientes where nome = %s and rg = %s", dados_cliente)
        self.db.commit()

    def carregar_todos_clientes(self):
        """Carrega os dados de todos os clientes presente no BD"""
        self.cursor.execute("select * from clientes")
        todos_clientes = self.cursor.fetchall()
        return todos_clientes

    def apagar_todos_clientes(self):
        """Apaga todos os clientes do banco de dados"""
        self.cursor.execute("delete from clientes")
        self.db.commit()

    def buscar_cliente(self, campo_de_busca, dado_para_busca):
        """Busca um cliente por um determinado dado, por exemplo: rg, telefone, nome"""
        texto_mysql = "select * from clientes where %s rlike \'%s\'" %(campo_de_busca,dado_para_busca)
#        texto_mysql = "select * from clientes where %s = \'%s\'" %(campo_de_busca,dado_para_busca)

        self.cursor.execute(texto_mysql) # executa a busca
        clientes_encontrados = self.cursor.fetchall() # recupera os resultados
        return clientes_encontrados

    def criar_backup(self, destino="backup.sql"):
        os.system("mysqldump --opt -u %s -p%s maestro > %s" %(self.nome, self.senha, destino))
        self.aviso.mostrar_aviso("O backup do seu banco de dados está em 'backup.sql'")
    
    ### __INIT__####
    def __init__ (self, nome, senha):
        """Sistema de cadastro de clientes"""
        self.aviso = aviso()
        self.nome = nome
        self.senha = senha
        try:
            self.db = MySQLdb.connect(host="localhost", user=self.nome, passwd=self.senha, db="maestro")
            
        except:
            raise 

        self.cursor = self.db.cursor()
        self.agendamentos_diario = []


		
