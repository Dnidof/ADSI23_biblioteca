from model import Connection, Book, User
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, titulo="", autor="", limit=6, page=0):
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

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE correo = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.nomusuario = s.nomusuario AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5])
		else:
			return None