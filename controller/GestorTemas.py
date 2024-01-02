from model import Connection, Book, User
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
				FROM Book b
					WHERE b.titulo LIKE ? 
					AND b.autor LIKE ? 
		""", (f"%{titulo}%", f"%{autor}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b
					WHERE b.titulo LIKE ? 
					AND b.autor LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{titulo}%", f"%{autor}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def addBook(self, titulo, autor, foto, desc):
		db.insert("INSERT INTO Book VALUES(NULL, ?, ?, ?, ?)", (titulo, autor, foto, desc))
	def search_my_books(self, user, titulo="", autor="", limit=6, page=0):
		res = db.select("""
				SELECT CopiaLibro.codCopia, b.*
				FROM Reserva
				JOIN CopiaLibro ON Reserva.codCopia = CopiaLibro.codCopia
				JOIN User ON Reserva.usuario = User.nomusuario
				JOIN Book b ON CopiaLibro.codLibro = b.codLibro
				WHERE b.titulo LIKE ? 
					AND b.autor LIKE ? 
					And nomUsuario LIKE ?
					AND fechaDev is null 
		""", (f"%{titulo}%", f"%{autor}%",f"{user.username}"))
		count = db.select("""
				SELECT count()
				FROM Reserva
				JOIN CopiaLibro ON Reserva.codCopia = CopiaLibro.codCopia
				JOIN User ON Reserva.usuario = User.nomusuario
				JOIN Book b ON CopiaLibro.codLibro = b.codLibro
				WHERE b.titulo LIKE ? 
					AND b.autor LIKE ? 
					And nomUsuario LIKE ?
					AND fechaDev is null 
		""", (f"%{titulo}%", f"%{autor}%",f"{user.username}"))[0][0]
		books = [
			(b[0],Book(b[1],b[2],b[3],b[4],b[5]))
			for b in res
		]
		return books, count

	def devolver_libro(self, cod):
		db.delete("DELETE FROM Reserva WHERE codCopia = ?", (cod,))
