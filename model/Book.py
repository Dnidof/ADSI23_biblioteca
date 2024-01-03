from .Connection import Connection
from .Resenia import Resenia
from .CopiaLibro import CopiaLibro

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