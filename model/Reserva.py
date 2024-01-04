from .Connection import Connection
from datetime import datetime
from .Book import Book

db = Connection()

class Reserva:
    def __init__(self, codCopia: int, fechaInicio: str, fechaDev: str, book: Book):
        fechaIn = datetime.strptime(fechaInicio, "%Y-%m-%d")
        fechaDv = datetime.strptime(fechaDev, "%Y-%m-%d")
        self.codCopia = codCopia
        self.fechaInicio = fechaIn
        self.fechaDev = fechaDv
        self.book = book
    
    def devolver(self):
        db.update("UPDATE CopiaLibro SET fechaDev = DATE('now') WHERE codCopia = ?", (self.codCopia,))

    def is_active(self):
        return self.fechaDev > datetime.now()
