from . import BaseTestClass
from bs4 import BeautifulSoup
class TestAddLibro(BaseTestClass):

	def test_add_libro_admin(self):
		self.login('james@gmail.com', '123456')
		res2 = self.client.get('/addlibro')
		page = BeautifulSoup(res2.data, features="html.parser")

		self.assertEqual('Título', page.find_all('label')[0].get_text())
		self.assertEqual('Autor', page.find_all('label')[1].get_text())
		self.assertEqual('Foto', page.find_all('label')[2].get_text())
		self.assertEqual('Descripción', page.find_all('label')[3].get_text())
		self.assertEqual('Añadir libro', page.find_all('button')[0].get_text())

		self.db.delete("DELETE FROM Book WHERE titulo = 'hola' AND autor = 'hola'")

		count = self.db.select("""
						SELECT count() 
						FROM Book b
							WHERE b.titulo LIKE ? 
							AND b.autor LIKE ? 
				""", (f"%{'hola'}%", f"%{'hola'}%"))[0][0]
		self.assertEqual(0, count)

		res2 = self.client.post('/addlibro', data={'titulo': 'hola', 'autor': 'hola', 'foto': '', 'desc': 'prueba'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		count = self.db.select("""
								SELECT count() 
								FROM Book b
									WHERE b.titulo LIKE ? 
									AND b.autor LIKE ? 
						""", (f"%{'hola'}%", f"%{'hola'}%"))[0][0]
		self.assertEqual(1, count)

		res3 = self.client.post('/addlibro', data={'titulo': 'hola', 'autor': 'hola', 'foto': '', 'desc': 'prueba'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Ya existe un libro con el mismo título y el mismo autor', mydivs[0].get_text())



		res3 = self.client.post('/addlibro', data={'autor': 'hola', 'foto': '', 'desc': 'prueba'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Rellena los campos de Título, Autor y Descripción, son obligatorios.', mydivs[0].get_text())

		res3 = self.client.post('/addlibro', data={'titulo': 'hola', 'foto': '', 'desc': 'prueba'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Rellena los campos de Título, Autor y Descripción, son obligatorios.', mydivs[0].get_text())

		res3 = self.client.post('/addlibro', data={'titulo': 'hola', 'autor': 'hola', 'foto': ''},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Rellena los campos de Título, Autor y Descripción, son obligatorios.', mydivs[0].get_text())

		self.db.delete("DELETE FROM Book WHERE titulo = 'hola' AND autor = 'hola'")

	def test_add_libro_not_admin(self):
		self.login('jhon@gmail.com', '123')
		res2 = self.client.get('/addlibro')
		self.assertEqual(302, res2.status_code)
		self.assertEqual('/', res2.location)

		self.client.post('/addlibro', data={'titulo': 'hola', 'autor': 'hola', 'foto': '', 'desc': 'prueba'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		count = self.db.select("""
										SELECT count() 
										FROM Book b
											WHERE b.titulo LIKE ? 
											AND b.autor LIKE ? 
								""", (f"%{'hola'}%", f"%{'hola'}%"))[0][0]
		self.assertEqual(0, count)