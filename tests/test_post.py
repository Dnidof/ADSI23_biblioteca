from . import BaseTestClass
from bs4 import BeautifulSoup


class TestPost(BaseTestClass):

    def test_post_authenticated(self):
        self.login('james@gmail.com', '123456')


        cod_tema = 1
        res = self.client.get(f'/post/{cod_tema}', query_string={'texto': 'Nuevo comentario', 'page': 1})

        self.assertEqual(200, res.status_code)

        page_content = res.get_data(as_text=True)
        self.assertIn('Detalles del Tema', page_content)
        self.assertIn('Nuevo comentario', page_content)



    def test_post_unauthenticated(self):

        cod_tema = 1  # Reemplaza esto con un código de tema existente en tu aplicación
        res = self.client.get(f'/post/{cod_tema}', query_string={'texto': 'Nuevo comentario', 'page': 1})


        self.assertEqual(200, res.status_code)


        page_content = res.get_data(as_text=True)
        self.assertIn('Detalles del Tema', page_content)
        self.assertIn('Nuevo comentario', page_content)


