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
from interface import Interface
class Principal:
    def __init__ (self):
        """Sistema de agendamento de clientes"""
        self.interface = Interface()

        rc_style = '''
	style "editfont" 
	{
	   font_name="courier 13"
	}
	
	widget "edit_window.*" style "editfont"
	
'''
        gtk.rc_parse_string(rc_style)           

a = Principal()
gtk.main()		

		
