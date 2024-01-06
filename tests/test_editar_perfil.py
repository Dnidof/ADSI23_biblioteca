from . import BaseTestClass
from bs4 import BeautifulSoup


class testEditar(BaseTestClass):

    def test_editar_peril(self):
        #comprobamos que al editar el perfil se han guardado los cambios
        self.login("jhon@gmail.com", "123")
        self.editar_perfil("prueba", "46368336D")
        db = self.db.select(f"SELECT nombre,dni FROM User WHERE correo = 'jhon@gmail.com'")
        self.assertEqual(db[0][0], "prueba")
        self.assertEqual(db[0][1], "46368336D")
