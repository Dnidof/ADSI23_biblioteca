from . import BaseTestClass
from bs4 import BeautifulSoup


class TestPostCrear(BaseTestClass):

    def test_post_crear_authenticated(self):
        self.login('james@gmail.com', '123456')

        cod_tema = 1
        res = self.client.post(f'/post/{cod_tema}/crearComentario', data={'contenido': 'Nuevo comentario'})


        self.assertEqual(302, res.status_code)



    def test_post_crear_unauthenticated(self):

        cod_tema = 1
        res = self.client.post(f'/post/{cod_tema}/crearComentario', data={'contenido': 'Nuevo comentario'})


        self.assertEqual(302, res.status_code)

