from . import BaseTestClass
from bs4 import BeautifulSoup
class TestEliminarUsuario(BaseTestClass):

    def test_admin_eliminar_usuario(self):
        self.login('james@gmail.com', '123456')
        res2 = self.client.get('/eliminarusuario')
        page = BeautifulSoup(res2.data, features="html.parser")

        # Comprobamos que aparecen los usuarios
        consulta = self.db.select("SELECT nomusuario FROM User")
        usernames = [
            u[0]
            for u in consulta
        ]
        for card in page.find('div', class_='row').find_all('div', class_='card'):
            self.assertTrue(card.find(class_='card-title').get_text() in usernames)

        # Añadimos un usuario y posteriormente lo eliminamos
        valorprueba = "__test"
        params = (valorprueba, valorprueba, valorprueba, valorprueba, valorprueba, 0, 0)
        self.db.insert("INSERT INTO User VALUES(?, ?, ?, ?, ?, ?, ?)", params)

        count = self.db.select("""
                SELECT count() 
                FROM User u
                WHERE u.nomusuario LIKE ? AND deshabilitado = 0
        """, (f"%{valorprueba}%",))[0][0]
        self.assertEqual(1, count)

        res2 = self.client.post('/eliminarusuario', data={'nomusuario': valorprueba},
                                headers={'content-type': 'application/x-www-form-urlencoded'})
        page = BeautifulSoup(res2.data, features="html.parser")

        # Al eliminarlo comprobamos que no aparece en la página pero vemos que esta deshabilitado en la BD

        for card in page.find('div', class_='row').find_all('div', class_='card'):
            self.assertTrue(card.find(class_='card-title').get_text() != valorprueba)

        count = self.db.select("""
                SELECT count() 
                FROM User u
                WHERE u.nomusuario LIKE ? AND deshabilitado = 1
        """, (f"%{valorprueba}%",))[0][0]
        self.assertEqual(1, count)

        # Comprobamos que el usuario deshabilitado no puede iniciar sesión
        self.client.delete_cookie('token')
        self.login(valorprueba, valorprueba)
        desh = self.client.get("/")
        self.assertNotIn('token', ''.join(desh.headers.values()))

        # Limpiamos la BD del usuario de prueba
        self.db.delete("DELETE FROM User WHERE nomusuario = ?", (valorprueba, ))
        count = self.db.select("""
                        SELECT count() 
                        FROM User u
                        WHERE u.nomusuario LIKE ? AND deshabilitado = 1
                """, (f"%{valorprueba}%",))[0][0]
        self.assertEqual(0, count)

    def test_not_admin_eliminar_usuario(self):
        self.login('jhon@gmail.com', '123')
        res2 = self.client.get('/eliminarusuario')
        self.assertEqual(302, res2.status_code)
        self.assertEqual('/', res2.location)

        valorprueba = "__test"
        self.client.post('/eliminarusuario', data={'nomusuario': valorprueba},
                                headers={'content-type': 'application/x-www-form-urlencoded'})
        count = self.db.select("""
                                SELECT count() 
                                FROM User u
                                WHERE u.nomusuario LIKE ? AND deshabilitado = 1
                        """, (f"%{valorprueba}%",))[0][0]
        self.assertEqual(0, count)