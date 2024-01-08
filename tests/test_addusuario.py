from . import BaseTestClass
from bs4 import BeautifulSoup
class TestAddUsuario(BaseTestClass):

	def test_admin_add_usuario(self):
		# Comprobamos a añadir unos usuarios admin y no admin y comprobamos que pasa si no rellenamos un campo
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

		nomusrPrueba = 'test12345'
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

		# Eliminamos el usuario y hacemos lo mismo para crear un usuario no admin

		self.db.delete("DELETE FROM User WHERE nomusuario = ?", (nomusrPrueba,))
		count = self.db.select("""
												SELECT count() 
												FROM User u
													WHERE u.nomusuario LIKE ? 
										""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(0, count)

		self.client.post('/addusuario', data={'usuario': nomusrPrueba, 'nombre': nomusrPrueba,
											  'correo': nomusrPrueba, 'password': nomusrPrueba,
											  'dni': nomusrPrueba, 'rol': '0'},
						 headers={'content-type': 'application/x-www-form-urlencoded'})
		count = self.db.select("""
										SELECT count() 
										FROM User u
											WHERE u.nomusuario LIKE ? 
								""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(1, count)

		# Comprobamos que no está disponible si lo intentamos volver a añadir y posteriormente lo eliminamos

		res3 = self.client.post('/addusuario', data={'usuario': nomusrPrueba, 'nombre': nomusrPrueba,
													 'correo': nomusrPrueba, 'password': nomusrPrueba,
													 'dni': nomusrPrueba, 'rol': '1'},
								headers={'content-type': 'application/x-www-form-urlencoded'})
		page = BeautifulSoup(res3.data, features="html.parser")
		mydivs = page.find_all("div", {"class": "error"})
		self.assertEqual(2, len(mydivs))
		self.assertEqual('Nombre de usuario no disponible', mydivs[0].get_text())
		self.assertEqual('Correo no disponible', mydivs[1].get_text())

		self.db.delete("DELETE FROM User WHERE nomusuario = ?", (nomusrPrueba,))
		count = self.db.select("""
														SELECT count() 
														FROM User u
															WHERE u.nomusuario LIKE ? 
												""", (f"%{nomusrPrueba}%",))[0][0]
		self.assertEqual(0, count)

		# Comprobamos que sucede si no rellenamos todos los campos


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

	def test_add_usuario_limites(self):
		self.login('james@gmail.com', '123456')

		# El primer valor -> [0] será el bueno, el resto provocarán un error por cada tipo (user, nombre...)
		users = ["test", "1"*16]
		nombres = ["test", "1"*21]
		correos = ["test", "1"*31]
		passwords = ["test", "1"*33]
		dnis = ["12345678Z", "1", "1"*10]
		rol = "0"
		mensajes = ["El nombre de usuario debe tener entre 1-15 caracteres",
					"El nombre debe tener entre 1-20 caracteres",
					"El correo debe tener como máximo 30 caracteres",
					"La contraseña debe tener como máximo 32 caracteres",
					"El DNI debe tener 9 caracteres"]

		for ind_user, user in enumerate(users):
			for ind_nombre, nombre in enumerate(nombres):
				for ind_correo, correo in enumerate(correos):
					for ind_passwd, passwd in enumerate(passwords):
						for ind_dni, dni in enumerate(dnis):

							# Saltamos la primera iteración con todos los valores correctos
							# utilizamos el min(ind_dni, 1) porque dnis[2] solo provoca 1 error
							ind_sum = ind_user + ind_nombre + ind_correo + ind_passwd + min(ind_dni, 1)
							if ind_sum == 0:
								continue

							res3 = self.client.post('/addusuario', data={'usuario': user, 'nombre': nombre,
													 'correo': correo, 'password': passwd,
													 'dni': dni, 'rol': rol},
								headers={'content-type': 'application/x-www-form-urlencoded'})
							page = BeautifulSoup(res3.data, features="html.parser")
							mydivs = page.find_all("div", {"class": "error"})

							errormsg = f"user:{user},nombre:{nombre},correo:{correo},password:{passwd},dni:{dni}\nErrores:{[e.get_text() for e in mydivs]}"
							self.assertEqual(ind_sum, len(set(d.get_text() for d in mydivs)), errormsg)
							for e in mydivs:
								self.assertTrue(e.get_text() in mensajes)

							count = self.db.select("""
																	SELECT count() 
																	FROM User u
																		WHERE u.nomusuario LIKE ? 
															""", (f"%{user}%",))[0][0]
							self.assertEqual(0, count)


