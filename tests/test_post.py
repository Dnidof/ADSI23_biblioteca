from . import BaseTestClass
from bs4 import BeautifulSoup
class TestPost(BaseTestClass):

    def test_post_with_user(self):
        # Comrpobamos que salga el campo para añadir un tema
        self.login('james@gmail.com', '123456')
        res = self.client.get('/post/2')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertEqual('Publicar comentario:', page.find_all('label')[0].get_text())


    def test_post_without_user(self):
        # Comprobamos que no salga el campo de rellenar
        self.login('james@gmail.com', '0')
        res = self.client.get('/post/2')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertNotEqual('Publicar comentario:', page.find_all('label')[0].get_text())

