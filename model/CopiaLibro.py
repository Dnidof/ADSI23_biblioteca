from .Connection import Connection

db = Connection()

class CopiaLibro:
    def __init__(self, codCopia):
        self.codCopia = codCopia
    
    def disponible(self) -> bool:
        return len(db.select("SELECT * FROM Reserva WHERE fechaDev>DATE('now') AND codCopia == ?;", (self.codCopia,))) == 0
