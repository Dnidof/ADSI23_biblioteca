from . import BaseTestClass
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class TestReservas(BaseTestClass):

	def test_reserva_legal(self):
		self.db.delete("DELETE FROM Reserva WHERE usuario = 'NgbZCib'")
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
		self.db.delete("DELETE FROM Reserva WHERE usuario = 'NgbZCib'")
		self.login('ejemplo@gmail.com', '123456')
		libro_a_reservar = 1
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		date = (datetime.now() + timedelta(days=61)).strftime('%Y-%m-%d')
		data = f"date={date}&book_id={libro_a_reservar}"
		res = self.client.post('/crear_reserva', data = data, headers = headers)
		self.assertEqual(400, res.status_code)
		db_result = self.db.select("SELECT * FROM Reserva WHERE usuario = 'NgbZCib'")
		self.assertEqual(0, len(db_result))
		
		