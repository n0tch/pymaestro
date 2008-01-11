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
import os
import sys
from aviso import aviso

class adm:
    ###funcoes da gui####
    def get_glade_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._nome_do_widget"""
        widget_names = ["nome_entry", "senha_entry1", "senha_entry2", 
                        "botao_cadastrar_usuario", "botao_criar_bd", 
                        "botao_sair", "adm_window", "aviso_dialog",
                        "botao_cancelar", "botao_ok", "senha_root_entry"]

        for widget_name in widget_names:
            setattr(self, "_" + widget_name, self.xml_glade.get_widget(widget_name))

    def botao_sair_clicado(self,*args):
        gtk.main_quit()

    def cadastrar_usuario(self, *args):
        nome = self._nome_entry.get_text()
        senha1 = self._senha_entry1.get_text()
        senha2 = self._senha_entry2.get_text()
        senha_root = self._senha_root_entry.get_text()  
        if nome and senha1 and senha2:
            if senha1 == senha2:
                cmd = """ grant create, create temporary tables, delete, execute, index,
                          insert, lock tables, select, show databases, 
                          update on *.* to %s identified by "%s";""" %(nome, senha1)
                arquivo_tmp = open("tmp.sql", "wr")
                arquivo_tmp.write(cmd)
                arquivo_tmp.close()
                os.system("mysql --i-am-a-dummy -u root -p%s< tmp.sql" %senha_root)
                if sys.platform == "win32" :
                    os.system("del tmp.sql")
                else:
                    os.system("rm tmp.sql")

                self.aviso.mostrar_aviso(("Usuário %s cadastrado" %nome))

            else:
                self.aviso.mostrar_aviso("As senhas que você digitou não conferem")
        else:
            self.aviso.mostrar_aviso("Você precisa preencher todos os campos")


    def mostrar_aviso_criar_bd(self, *args):
        self._aviso_dialog.show()

    def esconder_aviso(self, *args):
        self._aviso_dialog.hide()

    def criar_bd(self, args):
        senha_root = self._senha_root_entry.get_text()  
        os.system("mysql --i-am-a-dummy -u root -p%s < create_db.sql" %senha_root)
        self._aviso_dialog.hide()
               
    ### __INIT__####
    def __init__ (self):
        """Adiminstração do Maestro"""
        self.xml_glade= gtk.glade.XML("gui/adm.glade")
        # --- Dicionario com as funcoes callback ---
        funcoes_callback= {
                    "botao_sair_clicado": self.botao_sair_clicado,
                    "botao_cadastrar_usuario_clicado": self.cadastrar_usuario,
                    "botao_criar_bd_clicado": self.mostrar_aviso_criar_bd,
                    "botao_cancelar_clicado": self.esconder_aviso,
                    "botao_ok_clicado": self.criar_bd,
                    "evento_delete": self.botao_sair_clicado,
             }
        self.get_glade_widgets()
        self.xml_glade.signal_autoconnect(funcoes_callback)
        self.aviso = aviso()
        self._adm_window.show()	
        rc_style = '''
	style "editfont" 
	{
	   font_name="courier 13"
	}
	
	widget "edit_window.*" style "editfont"
	
'''
        gtk.rc_parse_string(rc_style)

if __name__ == "__main__":
    adm = adm()
    gtk.main()
