from .Connection import Connection

db = Connection()

class Comentario:
	def __init__(self, codpost, usuario, fecha, texto_comentario):
		self.codpost = codpost
		self.usuario = usuario
		self.fecha = fecha
		self.texto_comentario = texto_comentario

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, value):
		self._autor = value

	def __str__(self):
		return f"{self.texto} ({self.autor})"