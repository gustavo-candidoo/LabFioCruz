from sqlalchemy import text
from sqlalchemy.orm import Session
from models.conexao import engine

# Tabela utilizada nos exemplos:
# 
# CREATE TABLE pessoa (
#   id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
#   nome varchar(50) NOT NULL,
#   email varchar(50) NOT NULL,
#   UNIQUE KEY nome_UN (nome)
# );

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

def listarProjetos():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		projetos = sessao.execute(text("SELECT p.id, p.idusuario, u.nome usuario, p.banco, p.resumoods, p.nome FROM projeto p INNER JOIN usuario u ON u.id = p.idusuario"))

		lista = []

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, idusuario, usuario, banco, resumoods, nome) in projetos:
			lista.append({
				'id': id,
				'idusuario': idusuario,
				'usuario': usuario,
				'banco': banco,
				'resumoods': resumoods,
				'nome': nome
			})

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')
		return lista

def obterProjeto(id):
	with Session(engine) as sessao:
		parametros = {
			'id': id
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

		if pessoa == None:
			print('Pessoa não encontrada!')
		else:
			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def criarPessoa(nome, email):
	# É importante utilizar o método begin() para que a sessão seja comitada
	# automaticamente ao final, caso não ocorra uma exceção!
	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
	# e nenhuma alteração será persistida. Para mais informações de como explicitar
	# esse processo de commit() e rollback():
	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
	with Session(engine) as sessao, sessao.begin():
		pessoa = {
			'nomeXXX': nome,
			'emailXXX': email
		}

		sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nomeXXX, :emailXXX)"), pessoa)

		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
		# é passar uma lista como segundo parâmetro:
		# lista = [ ... ]
		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)

# O uso desse tipo de instrução é muito comum em Python!
# Quando executamos um arquivo direto pela linha de comando, como
# python exemplo_sql.py
# o Python fará com que a variável global __name__ valha '__main__', indicando
# que a execução do programa se deu a partir daquele arquivo, e não de outro.
# Quando o arquivo é importado, __name__ valerá o nome do arquivo sem a extensão
# .py, como 'exemplo_sql'
#if __name__ == '__main__':
#	criarPessoa('Nome3', 'Email3') # listarPessoas()

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html
