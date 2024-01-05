from .Connection import Connection
from datetime import datetime
from .Book import Book
from .User import User

db = Connection()

class Reserva:
    def __init__(self, codCopia: int, fechaInicio: str, fechaDev: str, book: Book, usuario: User):
        fechaIn = datetime.strptime(fechaInicio, "%Y-%m-%d")
        fechaDv = datetime.strptime(fechaDev, "%Y-%m-%d")
        self.codCopia = codCopia
        self.fechaInicio = fechaIn
        self.fechaDev = fechaDv
        self.book = book
        self.usuario = usuario
    
    def devolver(self):
        db.update("UPDATE CopiaLibro SET fechaDev = DATE('now') WHERE codCopia = ?", (self.codCopia,))

    def is_active(self):
        return self.fechaDev > datetime.now()
    
    def resenable(self):
        return not self.book.ha_sido_resenado_por(self.usuario)
