from model.User import User
from model.Book import Book
from model import Connection
from datetime import datetime, timedelta

class ReservaImposible(Exception):
	def __init__(self, msg):
		self.msg = msg

db = Connection()

class GestorReservas:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(GestorReservas, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance
	
	def _obtener_reservas_activas_usuario(self, usuario: User) -> int:
		username = usuario.username
		res = db.select("""
				SELECT count(*)
				FROM Reserva
				WHERE usuario = ? AND fechaDev > DATE('now')
		""", (username,))
		return res[0][0]


	def crear_reserva(self, libro: Book, usuario: User, date: str):
		copias = libro.get_copies()
		if date is None or date == "":
			raise ReservaImposible("La fecha no puede estar vacía")
		if len(copias) == 0:
			raise ReservaImposible("No existen copias de este libro")
		disponibles = [c for c in copias if c.disponible()]
		if len(disponibles) == 0:
			raise ReservaImposible("No hay copias disponibles para este libro")
		if self._obtener_reservas_activas_usuario(usuario) >= 3:
			raise ReservaImposible("El usuario ya tiene 3 reservas activas")
		try:
			d = datetime.strptime(date, "%Y-%m-%d")
		except ValueError:
			raise ReservaImposible("La fecha no tiene el formato correcto")
		if d < datetime.now():
			raise ReservaImposible("No se puede reservar para una fecha anterior a la actual")
		if d > datetime.now() + timedelta(days=60):
			raise ReservaImposible("No se puede reservar para una fecha posterior a 15 días")
		if usuario.deshabilitado:
			raise ReservaImposible("El usuario está deshabilitado")
		db.insert("""
				INSERT INTO Reserva (codCopia, usuario, fechaInicio, fechaDev)
				VALUES (?, ?, DATE('now'), ?)""", (disponibles[0].codCopia, usuario.username, date))
		
		
	def devolver_libro(self, cod):
		db.delete("DELETE FROM Reserva WHERE codCopia = ?", (cod,))
