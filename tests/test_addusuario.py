from . import BaseTestClass
from bs4 import BeautifulSoup
class TestAddUsuario(BaseTestClass):

	def test_admin_add_usuario(self):
		self.login('james@gmail.com', '123456')
		res2 = self.client.get('/addusuario')
		page = BeautifulSoup(res2.data, features="html.parser")

		self.assertEqual('Usuario', page.find_all('label')[0].get_text())
		self.assertEqual('Nombre', page.find_all('label')[1].get_text())
		self.assertEqual('Correo', page.find_all('label')[2].get_text())
		self.assertEqual('Contraseña', page.find_all('label')[3].get_text())
		self.assertEqual('DNI', page.find_all('label')[4].get_text())
		self.assertEqual('Admin', page.find_all('label')[5].get_text())
		self.assertEqual('Añadir usuario', page.find_all('button')[0].get_text())

		nomusrPrueba = '_test'
		self.db.delete("DELETE FROM User WHERE nomusuario = ?", (nomusrPrueba, ))

		count = self.db.select("""
						SELECT count() 
						FROM User u
							WHERE u.nomusuario LIKE ? 
				""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(0, count)

		self.client.post('/addusuario', data={'usuario': nomusrPrueba, 'nombre': nomusrPrueba,
													 'correo': nomusrPrueba, 'password': nomusrPrueba,
													 'dni': nomusrPrueba, 'rol': '1'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		count = self.db.select("""
								SELECT count() 
								FROM User u
									WHERE u.nomusuario LIKE ? 
						""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(1, count)

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba, 'nombre': nomusrPrueba,
													 'correo': nomusrPrueba, 'password': nomusrPrueba,
													 'dni': nomusrPrueba, 'rol': '1'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(2, len(mydivs))
		self.assertEqual('Nombre de usuario no disponible', mydivs[0].get_text())
		self.assertEqual('Correo no disponible', mydivs[1].get_text())


		res3 = self.client.post('/addusuario', data={'nombre': nomusrPrueba,
													 'correo': nomusrPrueba, 'password': nomusrPrueba,
													 'dni': nomusrPrueba, 'rol': '1'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Todos los campos son obligatorios', mydivs[0].get_text())

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba,
											  'correo': nomusrPrueba, 'password': nomusrPrueba,
											  'dni': nomusrPrueba, 'rol': '1'},
						 headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Todos los campos son obligatorios', mydivs[0].get_text())

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba,
											  'nombre': nomusrPrueba, 'password': nomusrPrueba,
											  'dni': nomusrPrueba, 'rol': '1'},
						 headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Todos los campos son obligatorios', mydivs[0].get_text())

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba,
											  'nombre': nomusrPrueba, 'correo': nomusrPrueba,
											  'dni': nomusrPrueba, 'rol': '1'},
						 headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Todos los campos son obligatorios', mydivs[0].get_text())

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba,
											  'nombre': nomusrPrueba, 'correo': nomusrPrueba,
											  'password': nomusrPrueba, 'rol': '1'},
						 headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(1, len(mydivs))
		self.assertEqual('Todos los campos son obligatorios', mydivs[0].get_text())

		self.db.delete("DELETE FROM User WHERE nomusuario = ?", (nomusrPrueba, ))

	def test_not_admin_add_usuario(self):
		self.login('jhon@gmail.com', '123')
		res2 = self.client.get('/addusuario')
		self.assertEqual(302, res2.status_code)
		self.assertEqual('/', res2.location)

		nomusrPrueba = "__test"
		self.client.post('/addusuario', data={'usuario': nomusrPrueba, 'nombre': nomusrPrueba,
													 'correo': nomusrPrueba, 'password': nomusrPrueba,
													 'dni': nomusrPrueba, 'rol': '1'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		count = self.db.select("""
										SELECT count() 
										FROM User u
											WHERE u.nomusuario LIKE ? 
								""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(0, count)