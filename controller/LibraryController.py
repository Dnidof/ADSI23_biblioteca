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
		user = db.select("SELECT * from User WHERE correo = ? AND password = ? AND deshabilitado = 0", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.nomusuario = s.nomusuario AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6])
		else:
			return None

	def bookExists(self, titulo, autor):
		libro = db.select("SELECT * FROM Book WHERE titulo = ? AND autor = ?", (titulo, autor))
		return len(libro) > 0

	def addBook(self, titulo, autor, foto, desc):
		db.insert("INSERT INTO Book VALUES(NULL, ?, ?, ?, ?)", (titulo, autor, foto, desc))

	def checkUsernameExists(self, username):
		user = db.select("SELECT * FROM User WHERE nomusuario = ?", (username,))
		return len(user) > 0

	def checkEmailExists(self, email):
		user = db.select("SELECT * FROM User WHERE correo = ?", (email,))
		return len(user) > 0

	def addUser(self, usuario, nombre, correo, password, dni, rol, deshabilitado):
		db_password = hash_password(password)
		params = (usuario, nombre, correo, db_password, dni, rol, deshabilitado)
		db.insert("INSERT INTO User VALUES(?, ?, ?, ?, ?, ?, ?)", params)

	def getUsers(self, limit=6, page=0):
		count = db.select("""
						SELECT count() 
						FROM User 
				""")[0][0]

		res = db.select("SELECT * from User WHERE deshabilitado = 0 LIMIT ? OFFSET ?", (limit, limit*page))
		users = [
			User(u[0], u[1], u[2], u[4], u[5], u[6])
			for u in res
		]
		return users, count

	def deleteUser(self, username, email):
		db.update("UPDATE User SET deshabilitado = 1 WHERE nomusuario = ? AND correo = ?", (username, email))
