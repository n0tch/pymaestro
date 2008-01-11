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
class aviso:
    ###funcoes da gui####
    def get_glade_widgets(self):
        """Carrega todos os widgets do arquivo Glade que estao na lista "widget_names
           e cria um atributo self._nome_do_widget"""
        widget_names = ["aviso_dialog", "aviso_label", "botao_ok_dialog"]
        for widget_name in widget_names:
            setattr(self, "_" + widget_name, self.xml_glade.get_widget(widget_name))

    def ok_clicado(self,*args):
        self._aviso_dialog.hide()
        return True

    def mostrar_aviso(self,msg):
        self._aviso_label.set_text(msg)
        self._aviso_dialog.show()

    ### __INIT__####
    def __init__ (self):
        """Sistema de agendamento de clientes"""
        self.xml_glade= gtk.glade.XML("gui/aviso.glade")
        # --- Dicionario com as funcoes callback ---
        funcoes_callback= {
                    "botao_ok_dialog_clicado": self.ok_clicado,
             }
        self.get_glade_widgets()
        self.xml_glade.signal_autoconnect(funcoes_callback)
        self._aviso_dialog.connect("delete-event", self.ok_clicado)
		
