import sqlite3
from model.User import User
from model.Book import Book
from model import Connection
from model.Reserva import Reserva
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
			raise ReservaImposible("No se puede reservar para una fecha anterior o igual a la actual")
		if d > datetime.now() + timedelta(days=60):
			raise ReservaImposible("No se puede reservar para una fecha posterior a 60 días")
		if usuario.deshabilitado:
			raise ReservaImposible("El usuario está deshabilitado")
		for copia in disponibles:
			try:
				db.insert("""
						INSERT INTO Reserva (codCopia, usuario, fechaInicio, fechaDev)
						VALUES (?, ?, DATE('now'), ?)""", (copia.codCopia, usuario.username, date))
				return
			except sqlite3.IntegrityError:
				continue
		raise ReservaImposible("""No se ha podido reservar. Probablemente ya hayas reservado y devuelto
						  hoy la unica copia disponible de este libro. Prueba mañana.""")

	def añadir_reseña(self, texto, puntuacion, usuario, cod_copia):
		try:
			query = "SELECT codLibro FROM CopiaLibro WHERE codCopia = ?"
			result = db.select(query, (cod_copia,))

			if result:
				cod_libro = result[0][0]
				# Insertar la reseña asociada al código del libro obtenido
				db.insert("INSERT INTO Resenia VALUES (?, ?, ?, ?)", (cod_libro, usuario, texto, puntuacion))
			else:
				print("La copia especificada no existe.")
		except Exception as e:
			print(f"Error al añadir reseña, el usuario ya ha creado una review de este libro: {e}")

	def devolver_libro(self, cod):
		db.update("UPDATE Reserva SET Fechadev = DATE('now') WHERE codCopia = ? AND fechaDev > DATE('now')", (cod,))

	def get_reservas_usuario(self, usuario: User, titulo: str = "", author: str = "") -> list[Reserva]:
		username = usuario.username
		res = db.select("""
				SELECT Reserva.codCopia, fechaInicio, fechaDev, b.*
				FROM Reserva
				JOIN CopiaLibro ON Reserva.codCopia = CopiaLibro.codCopia
				JOIN Book b ON CopiaLibro.codLibro = b.codLibro
				WHERE usuario = ?
				AND b.titulo LIKE ?
				AND b.autor LIKE ?
		""", (username, f"%{titulo}%", f"%{author}%"))
		# si esto funciona me descojono
		reservas = [Reserva(r[0], r[1], r[2], Book(*r[3:]), usuario) for r in res]
		reservas.sort(key=lambda r: r.fechaDev, reverse=True)
		return reservas
	
	def cancelar_reserva(self, codCopia: str, usuario: str, fechaInicio: str):
		cantidad = db.delete("DELETE FROM Reserva WHERE codCopia = ? AND fechaInicio = ? AND usuario = ?",
					    (codCopia, fechaInicio, usuario))
		if cantidad == 0:
			raise ValueError("No hay reservas que coincidan con los datos especificados")

	def ampliar_reserva(self, codCopia: str, usuario: str, fechaDev: str):
		fechaInicio = db.select("SELECT fechaInicio FROM Reserva WHERE codCopia = ? AND usuario = ?",
					    (codCopia, usuario))[0][0]
		fechaInicio = datetime.strptime(fechaInicio, "%Y-%m-%d")
		try:
			fechaDev = datetime.strptime(fechaDev, "%Y-%m-%d")
		except ValueError:
			raise ReservaImposible("La fecha no tiene el formato correcto")
		if fechaDev < fechaInicio:
			raise ReservaImposible("La fecha de devolución no puede ser anterior a la fecha de inicio")
		if fechaDev > fechaInicio + timedelta(days=60):
			raise ReservaImposible("La fecha de devolución no puede ser posterior a 60 días")
		if fechaDev < datetime.now():
			raise ReservaImposible("La fecha de devolución no puede ser anterior a la fecha actual")
		cantidad = db.update("UPDATE Reserva SET fechaDev = ? WHERE codCopia = ? AND fechaDev > DATE('now') AND usuario = ?",
					    (fechaDev.date(), codCopia, usuario))
		if cantidad == 0:
			raise ReservaImposible("No hay reservas que coincidan con los datos especificados")