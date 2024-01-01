import datetime
from .Connection import Connection
from .tools import hash_password

db = Connection()

class Session:
	def __init__(self, hash, time):
		self.hash = hash
		self.time = time

	def __str__(self):
		return f"{self.hash} ({self.time})"

class User:
	def __init__(self, username, name, email, dni, rol, deshabilitado):
		self.username = username
		self.name = name
		self.email = email
		self.dni = dni
		self.rol = int(rol)
		self.deshabilitado = int(deshabilitado)

	def __str__(self):
		return f"{self.username} ({self.email})"

	def new_session(self):
		now = float(datetime.datetime.now().time().strftime("%Y%m%d%H%M%S.%f"))
		session_hash = hash_password(str(self.username)+str(now))
		db.insert("INSERT INTO Session VALUES (?, ?, ?)", (session_hash, self.username, now))
		return Session(session_hash, now)

	def validate_session(self, session_hash):
		s = db.select("SELECT * from Session WHERE nomusuario = ? AND session_hash = ?", (self.username, session_hash))
		if len(s) > 0:
			now = float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
			session_hash_new = hash_password(str(self.username) + str(now))
			db.update("UPDATE Session SET session_hash = ?, last_login=? WHERE session_hash = ? and nomusuario = ?", (session_hash_new, now, session_hash, self.username))
			return Session(session_hash_new, now)
		else:
			return None

	def delete_session(self, session_hash):
		db.delete("DELETE FROM Session WHERE session_hash = ? AND nomusuario = ?", (session_hash, self.username))


	def isAdmin(self):
		return self.rol == 1