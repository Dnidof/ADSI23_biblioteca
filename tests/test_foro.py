from . import BaseTestClass
from bs4 import BeautifulSoup

class TestForo(BaseTestClass):

    def test_foro_with_text(self):
        self.login('james@gmail.com', '123456')


        res = self.client.get('/foro?texto=test')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertEqual('Título del Tema', page.find_all('h2')[0].get_text())


    def test_foro_without_text(self):

        res = self.client.get('/foro')
        page = BeautifulSoup(res.data, features="html.parser")


        self.assertEqual('Título del Tema', page.find_all('h2')[0].get_text())
