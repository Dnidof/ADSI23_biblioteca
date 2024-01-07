from . import BaseTestClass
class TestGestorUsuarios(BaseTestClass):


    def test_eliminar_amigo(self):
        receptor_username = "usuario1"
        solicitante_username = "usuario2"

        self.login("usuario1@gmail.com","usuario1")


        self.db.insert("INSERT INTO Amigo (usuarioA, usuarioB) VALUES (?, ?)",
                  (receptor_username, solicitante_username))

        #Realizar la acción que se está probando
        res = self.client.post('/eliminar_amigo',data={'amigo_username': solicitante_username})

        # Verificar que la relacion de amistad se haya eliminado
        existing_request = self.db.select("SELECT * FROM Amigo WHERE usuarioA = ? AND usuarioB = ?",
                                     (receptor_username, solicitante_username))
        self.assertEqual(0, len(existing_request))

        # Verificar redirección
        self.assertEqual(res.status_code, 302)  # Código de estado de redirección
        self.assertEqual(res.location, '/amigos.html')  # Dirección de redirección esperada
