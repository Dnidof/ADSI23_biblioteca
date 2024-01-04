from .Connection import Connection
from .Resenia import Resenia
from .CopiaLibro import CopiaLibro
from .User import User

db = Connection()

class Book:
	def __init__(self, id, title, author, cover, description):
		self.id = id
		self.title = title
		self.author = author
		self.cover = cover
		self.description = description

	@property
	def author(self):
		return self._author

	@author.setter
	def author(self, value):
		self._author = value

	def __str__(self):
		return f"{self.title} ({self.author})"
	
	def get_resenas(self) -> list[Resenia]:
		res = db.select("""
				SELECT *
				FROM Resenia
				WHERE codLibro = ?
		""", (self.id,))
		return [Resenia(*r) for r in res]
	
	def get_copies(self) -> list[CopiaLibro]:
		res = db.select("""
				SELECT codCopia
				FROM CopiaLibro
				WHERE codLibro = ?
		""", (self.id,))
		res = [CopiaLibro(*r) for r in res]
		return res
	
	def ha_sido_resenado_por(self, usuario: User) -> bool:
		res = db.select("""
				SELECT *
				FROM Resenia
				WHERE codLibro = ? AND usuario = ?
		""", (self.id, usuario.username))
		return len(res) > 0
	
	def add_resena(self, usuario: User, texto: str, rating: int):
		if rating < 1 or rating > 5:
			raise ValueError("Rating must be between 1 and 5")
		if self.ha_sido_resenado_por(usuario):
			raise ValueError("User has already reviewed this book")
		db.insert("""
				INSERT INTO Resenia VALUES(?, ?, ?, ?)
		""", (self.id, usuario.username, texto, rating))