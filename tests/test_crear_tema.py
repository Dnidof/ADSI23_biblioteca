from . import BaseTestClass
from bs4 import BeautifulSoup
from . import webServer
from controller import GestorTemas


class TestCrearTema(BaseTestClass):

    def test_crear_tema_authenticated(self):
        #vamos a comprobar que el numero de temas aumente al crear uno nuevo demostrando que se crea correctamente y que hay que estar loggeado para ello
        self.login('james@gmail.com', '123456')
        res = self.client.get('/foro')
        page = BeautifulSoup(res.data, features="html.parser")

        self.assertEqual('Tema', page.find_all('label')[0].get_text())

        res_before = self.client.get('/foro')
        page_before = BeautifulSoup(res_before.data, features="html.parser")
        total_pages_before = int(page_before.find_all('li', class_='page-item')[-1].text)
        total_elements_before = 0
        for page_num in range(1, total_pages_before + 1):
            res_before = self.client.get(f'/foro?page={page_num}')
            page_before = BeautifulSoup(res_before.data, features="html.parser")
            total_elements_before += len(page_before.find_all('h5'))

        num = total_elements_before

        self.client.post('/crear_tema', data={'texto': 'prueba'})
        res_after = self.client.get('/foro')
        page_after = BeautifulSoup(res_after.data, features="html.parser")
        total_pages_after = int(page_after.find_all('li', class_='page-item')[-1].text)
        total_elements_after = 0

        for page_num in range(1, total_pages_after + 1):
            res_after = self.client.get(f'/foro?page={page_num}')
            page_after = BeautifulSoup(res_after.data, features="html.parser")
            total_elements_after += len(page_after.find_all('h5'))

        self.assertEqual(num + 1, total_elements_after)


