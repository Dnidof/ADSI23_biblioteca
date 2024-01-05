from . import BaseTestClass
class TestGestorUsuarios(BaseTestClass):


    def test_aceptar_solicitud_exitosa(self):
        receptor_username = "usuario1"
        solicitante_username = "usuario2"

        self.login("usuario1@gmail.com","usuario1")


        self.db.insert("INSERT INTO Solicitud (usuarioReceptor, usuarioEnvia) VALUES (?, ?)",
                  (receptor_username, solicitante_username))

        # Realizar la acción que se está probando
        res = self.client.post('/aceptar_solicitud', data={'solicitante': solicitante_username})

        # Verificar que la solicitud se haya eliminado
        existing_request = self.db.select("SELECT * FROM Solicitud WHERE usuarioReceptor = ? AND usuarioEnvia = ?",
                                     (receptor_username, solicitante_username))
        self.assertEqual(0, len(existing_request))

        # Verificar que la relación de amistad se haya establecido correctamente
        friends = self.db.select("SELECT * FROM Amigo WHERE usuarioA = ? AND usuarioB = ?",
                                 (receptor_username, solicitante_username))
        self.assertTrue(any(solicitante_username in friend for friend in friends),
                        "El usuario solicitante no es un amigo")

        # Verificar redirección
        self.assertEqual(res.status_code, 302)  # Código de estado de redirección
        self.assertEqual(res.location, '/solicitudes')  # Dirección de redirección esperada
