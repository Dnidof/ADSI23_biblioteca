from .Connection import Connection

db = Connection()

class Book:
	def __init__(self, cod, texto, autor, comentarios):
		self.cod = cod
		self.texto = texto
		self.autor = autor
		self.comentarios = comentarios

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, value):
		self._autor = value

	def __str__(self):
		return f"{self.texto} ({self.autor})"