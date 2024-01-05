from unittest import SkipTest
from . import BaseTestClass
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class TestReservas(BaseTestClass):

	def setUp(self):
		super().setUp()
		self.db.delete("DELETE FROM Reserva WHERE usuario = 'NgbZCib'")

	def tearDown(self):
		# self.db.delete("DELETE FROM Reserva WHERE usuario = 'NgbZCib'")
		pass


	def crear_reserva(self, libro_a_reservar: int, date: datetime):
		self.db.insert("""
				INSERT INTO Reserva (codCopia, usuario, fechaInicio, fechaDev)
				VALUES (?, ?, DATE('now'), ?)""", (libro_a_reservar*2, 'NgbZCib', date.strftime('%Y-%m-%d')))

	def test_reserva_legal(self):
		self.login('ejemplo@gmail.com', '123456')
		libro_a_reservar = 1
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
		data = f"date={date}&book_id={libro_a_reservar}"
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(302, res.status_code)
		self.assertEqual("/misLibros", res.location)
		db_result = self.db.select("SELECT * FROM Reserva WHERE usuario = 'NgbZCib'")
		self.assertEqual(1, len(db_result))

	def test_reserva_ilegal(self):
		self.login('ejemplo@gmail.com', '123456')
		libro_a_reservar = 1
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		date = (datetime.now() + timedelta(days=61)).strftime('%Y-%m-%d')
		data = f"date={date}&book_id={libro_a_reservar}"
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(400, res.status_code)
		db_result = self.db.select("SELECT * FROM Reserva WHERE usuario = 'NgbZCib'")
		self.assertEqual(0, len(db_result))
		
	def test_historial_reservas(self):
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/misLibros')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		reservas = page.find_all("div", {"class": "card"})
		self.assertEqual(0, len(reservas))
		
		#este libro está devuelto y se comprueba que también aparece en el historial
		self.crear_reserva(1, datetime.now() + timedelta(days=-1))

		self.crear_reserva(2, datetime.now() + timedelta(days=2))
		self.crear_reserva(3, datetime.now() + timedelta(days=3))
		res = self.client.get('/misLibros')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		reservas = page.find_all("div", {"class": "card"})
		self.assertEqual(3, len(reservas))
		self.crear_reserva(4, datetime.now() + timedelta(days=4))
		self.crear_reserva(5, datetime.now() + timedelta(days=5))
		self.crear_reserva(6, datetime.now() + timedelta(days=6))
		self.crear_reserva(7, datetime.now() + timedelta(days=7))
		res = self.client.get('/misLibros', query_string={'page': 2})
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		reservas = page.find_all("div", {"class": "card"})
		self.assertEqual(1, len(reservas))
		ultima = reservas[0].find_all("p", {"class": "card-text"})[1:]
		fecha_prestado = list(ultima[0].children)[2]
		fecha_devolucion = list(ultima[1].children)[2]
		self.assertEqual((datetime.now()).strftime('%Y-%m-%d'), fecha_prestado)
		self.assertEqual((datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d'), fecha_devolucion)

	def test_no_identificado_no_puede_reservar(self):
		page = self.client.get("/libro/1")
		self.assertEqual(200, page.status_code)
		page = BeautifulSoup(page.data, features="html.parser")
		reserva = page.find_all("a", {"class": "btn btn-danger"})
		self.assertEqual([], reserva)
		res = self.client.post("/crear_reserva")
		self.assertEqual(302, res.status_code)
		self.assertEqual("/login", res.location)
		self.login('ejemplo@gmail.com', '123456')
		page = self.client.get("/libro/1")
		self.assertEqual(200, page.status_code)
		page = BeautifulSoup(page.data, features="html.parser")
		reserva = page.find_all("a", {"class": "btn btn-danger"})
		self.assertEqual(1, len(reserva))

	def test_ampliar(self):
		raise SkipTest("Not implemented")
	
	def test_cancelar(self):
		raise SkipTest("Not implemented")
	
	def test_reservas_exclusivas(self):
		self.login('ejemplo@gmail.com', '123456')
		libro_a_reservar = 1
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
		data = f"date={date}&book_id={libro_a_reservar}"
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(302, res.status_code)
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(302, res.status_code)
		self.login('ejemploo@gmail.com', '123456')
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(400, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		error = page.find_all("div", {"class": "error-details"})
		error = list(error[0].children)[0]
		self.assertEqual("No hay copias disponibles para este libro", error.strip())
		res = self.client.get('/libro/1')
		page = BeautifulSoup(res.data, features="html.parser")
		boton_reserva = page.find_all("a", {"class": "btn btn-danger disabled"})
		self.assertEqual(1, len(boton_reserva))
