from . import BaseTestClass
class TestGestorUsuarios(BaseTestClass):


    def test_rechazar_solicitud_exitosa(self):
        receptor_username = "usuario1"
        solicitante_username = "usuario2"

        self.login("usuario1@gmail.com","usuario1")


        self.db.insert("INSERT INTO Solicitud (usuarioReceptor, usuarioEnvia) VALUES (?, ?)",
                  (receptor_username, solicitante_username))

        # Realizar la acción que se está probando
        res = self.client.post('/rechazar_solicitud', data={'solicitante': solicitante_username})

        #Verificar que la solicitud se haya eliminado
        existing_request = self.db.select("SELECT * FROM Solicitud WHERE usuarioReceptor = ? AND usuarioEnvia = ?",
                                     (receptor_username, solicitante_username))
        self.assertEqual(0, len(existing_request))

        # Verificar redirección
        self.assertEqual(res.status_code, 302)  # Código de estado de redirección
        self.assertEqual(res.location, '/solicitudes')  # Dirección de redirección esperada
