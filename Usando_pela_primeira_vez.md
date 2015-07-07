# Usando o pyMaestro pela primeira vez #

Bom, se você está aqui, considero que já tenha instalado todos os pré-requisitos e descompactado o pyMaestro na pasta desejada conforme orientado na página "Como instalar".

Primeiramente, você deve acessar a pasta com o pyMaestro e rodar o programa adm.py.
Esse programa é responsável por criar as tabelas necessárias no MySQL que armazenarão seus dados ao utilizar o pyMaestro e, caso deseje, adicionar novos usuários que tenham acesso ao seu banco de dados.

Para isso, acesse adm.py (no console: python adm.py) , digite a senha do administrador no local apropriado e clique no botão "Criar banco de dados" (tela abaixo). Pronto! Seu banco de dados está criado.

![http://pymaestro.googlecode.com/svn/wiki/adm_screenshot.jpg](http://pymaestro.googlecode.com/svn/wiki/adm_screenshot.jpg)

É interessante também criar um novo usuário para não utilizar o Administrador durante trabalhos cotidianos. Para isso, digite nos campos indicados o nome do novo usuário e a senha; clique então no botão "cadastrar" para salvar esse novo usuário.

Agora é só sair do programa adm.py e acessar iniciar.py (no console: python iniciar.py).