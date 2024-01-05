from . import BaseTestClass
from bs4 import BeautifulSoup
class TestForo(BaseTestClass):

    def test_foro_with_user(self):
        # Comrpobamos que salga el campo para añadir un tema
        self.login('james@gmail.com', '123456')
        res = self.client.get('/foro')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertEqual('Tema', page.find_all('label')[0].get_text())


    def test_foro_without_user(self):
        # Comprobamos que no salga el campo de rellenar
        self.login('james@gmail.com', '0')
        res = self.client.get('/foro')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertNotEqual('Tema', page.find_all('label')[0].get_text())

    def test_foro_se_imprimen_los_temas(self):
        self.login('james@gmail.com', '123456')
        res = self.client.get('/foro')
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual('Accion', page.find_all('h5')[0].get_text())
        self.assertEqual('España', page.find_all('h5')[2].get_text())