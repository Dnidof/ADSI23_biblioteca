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
		self.amigos = []
		self.solicitudesEnviadas = []
		self.solicitudesRecibidas = []

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
	
	def esUsuario(self, username):
		return self.username == username
	
	def obtenerInfoPerfil(self):
		return {
			'username': self.username,
			'name': self.name,
			'email': self.email,
			'dni': self.dni,
			'rol': self.rol,
			'deshabilitado': self.deshabilitado,
			'amigos': [amigo.username for amigo in self.amigos],
			'solicitudesEnviadas': [solicitud.username for solicitud in self.solicitudesEnviadas],
			'solicitudesRecibidas': [solicitud.username for solicitud in self.solicitudesRecibidas]
		}
	
	def actualizarPerfil(self, perfil):
		self.name = perfil.get('name', self.name)
		self.email = perfil.get('email', self.email)
		self.dni = perfil.get('dni', self.dni)
        # ... resto de campos si necesario

	def añadirAmigo(self, user):
		self.amigos.append(user)

	def eliminarAmigo(self, user):
		self.amigos.remove(user)

	def añadirSolicitud(self, user):
		self.solicitudesEnviadas.append(user)

	def eliminarSolicitud(self, user):
		self.solicitudesEnviadas.remove(user)

	def getInfoSolicitudes(self):
		return {
            'solicitudesEnviadas': [solicitud.username for solicitud in self.solicitudesEnviadas],
            'solicitudesRecibidas': [solicitud.username for solicitud in self.solicitudesRecibidas]
        }

	def getInfoAmigos(self):
		amigos_info = {
			'amigos': [{'username': amigo.username, 'name': amigo.name}
					   for amigo in self.amigos]
		}
		return amigos_info