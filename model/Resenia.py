from .Connection import Connection

db = Connection()

class Resenia:
    codLibro: int
    autor: str
    texto: str
    estrellas: int

    def __init__(self, codLibro: int, autor: str, texto: str, estrellas: int):
        self.codLibro = codLibro
        self.autor = autor
        self.texto = texto
        self.estrellas = estrellas

    