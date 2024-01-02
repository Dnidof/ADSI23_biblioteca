from .Comentario import Comentario
from .Connection import Connection

db = Connection()

class Tema:
	def __init__(self, cod, texto, autor):
		self.cod = cod
		self.texto = texto
		self.autor = autor

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, value):
		self._autor = value

	def comentarios(self):
		# Realiza una consulta para obtener todos los comentarios asociados a este tema
		comentarios_data = db.select("SELECT * FROM Comentario WHERE codpost = ?", (self.cod,))


		comentarios = [Comentario(*comentario_data) for comentario_data in comentarios_data]

		return comentarios
	def __str__(self):
		return f"{self.texto} ({self.autor})"