from .Connection import Connection

db = Connection()

class Comentario:
	def __init__(self, texto, autor, fechaHora):
		self.texto = texto
		self.autor = autor
		self.fechaHora = fechaHora

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, value):
		self._autor = value

	def __str__(self):
		return f"{self.texto} ({self.autor})"