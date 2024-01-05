from . import BaseTestClass
from bs4 import BeautifulSoup


class TestCrearTema(BaseTestClass):

    def test_crear_tema_authenticated(self):
        self.login('james@gmail.com', '123456')


        res = self.client.post('/crear_tema', data={'texto': 'Nuevo tema'},
                               headers={'content-type': 'application/x-www-form-urlencoded'})

        self.assertEqual(302, res.status_code)
        self.assertEqual('/foro', res.location)



    def test_crear_tema_unauthenticated(self):

        res = self.client.post('/crear_tema', data={'texto': 'Nuevo tema'},
                               headers={'content-type': 'application/x-www-form-urlencoded'})


        self.assertEqual(302, res.status_code)
        path = res.location
        self.assertEqual('/?path=' + path, res.location)

