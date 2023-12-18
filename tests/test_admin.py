from . import BaseTestClass
from bs4 import BeautifulSoup
class TestAdmin(BaseTestClass):

    def test_is_admin(self):
        res = self.login('james@gmail.com', '123456')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)
        self.assertIn('token', ''.join(res.headers.values()))
        self.assertIn('time', ''.join(res.headers.values()))
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertEqual(6, len(page.find('header').find('ul').find_all('li')))
        self.assertEqual('Gestionar usuarios', page.find('header').find('ul').find_all('li')[3].get_text())
        self.assertEqual('Añadir libro', page.find('header').find('ul').find_all('li')[4].get_text())

        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        for link in page.find("div", {"class": "p-5"}).find_all("a"):
            print(link.get_text())
            self.assertTrue(link.get_text() in ["Añadir usuario", "Eliminar usuario"])

    def test_is_not_admin(self):
        res = self.login('jhon@gmail.com', '123')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)
        self.assertIn('token', ''.join(res.headers.values()))
        self.assertIn('time', ''.join(res.headers.values()))
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertEqual(4, len(page.find('header').find('ul').find_all('li')))