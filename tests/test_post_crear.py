from . import BaseTestClass
from bs4 import BeautifulSoup


class TestPostCrear(BaseTestClass):

    def test_crear_post_authenticated(self):
        # Logueamos al usuario
        self.login('james@gmail.com', '123456')

        # Accedemos a la página del post
        res = self.client.get('/post/2')  # Asegúrate de ajustar el ID del post según tu caso
        page = BeautifulSoup(res.data, features="html.parser")

        # Comprobamos que hay un campo para añadir un comentario
        self.assertEqual('Publicar comentario:', page.find_all('label')[0].get_text())

        # Contamos los comentarios actuales
        num_comentarios = len(page.find_all('h5', class_='mt-0 font-weight-bold'))

        # Creamos un comentario
        self.client.post('/post/2/crearComentario', data={'contenido': 'Este es un comentario de prueba'})

        # Volvemos a acceder a la página del post
        res_after = self.client.get('/post/2')  # Asegúrate de ajustar el ID del post según tu caso
        page_after = BeautifulSoup(res_after.data, features="html.parser")

        # Comprobamos que el número de comentarios ha aumentado en 1
        self.assertEqual(num_comentarios + 1, len(page_after.find_all('h5', class_='mt-0 font-weight-bold')))

