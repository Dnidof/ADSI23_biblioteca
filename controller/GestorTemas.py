from model import Connection, Tema, User
from model.Tema import Tema
from model.tools import hash_password

db = Connection()

class GestorTemas:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(GestorTemas, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_temas(self, texto="", autor="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Post p
					WHERE p.texto_post LIKE ? 
					AND p.nomusuario LIKE ? 
		""", (f"%{texto}%", f"%{autor}%"))[0][0]
		res = db.select("""
				SELECT p.* 
				FROM Post p
					WHERE p.texto_post LIKE ? 
					AND p.nomusuario LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{texto}%", f"%{autor}%", limit, limit*page))
		temas = [
			Tema(p[0], p[2], p[1])
			for p in res
		]

		return temas, count

	def addTema(self, texto, autor):
		db.insert("INSERT INTO Post VALUES(NULL, ?, ?)", (texto, autor))