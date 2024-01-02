import hashlib
import sqlite3
import json

salt = "library"


con = sqlite3.connect("datos.db")
cur = con.cursor()


### Create tables
cur.execute("""
	CREATE TABLE Book(
		codLibro integer primary key AUTOINCREMENT,
		titulo varchar(50),
		autor varchar(40),
		foto varchar(50),
		descripcion TEXT
	)
""")

cur.execute("""
	CREATE TABLE User(
		nomusuario varchar(15) primary key,
		nombre varchar(20),
		correo varchar(30) UNIQUE,
		password varchar(32),
		dni varchar(9),
		rol BIT,
		deshabilitado BIT
	)
""")

cur.execute("""
	CREATE TABLE Post(
		codpost integer primary key autoincrement,
		nomusuario varchar(15),
		texto_post TEXT,
		FOREIGN KEY(nomusuario) REFERENCES User(nomusuario) ON UPDATE CASCADE
	)
""")

cur.execute("""
	CREATE TABLE Comentario(
		codpost integer,
		usuario varchar(15),
		fecha DATE,
		texto_comentario TEXT,
		primary key (codpost, usuario, texto_comentario),
		FOREIGN KEY(usuario) REFERENCES User(nomusuario) ON UPDATE CASCADE, 
		FOREIGN KEY(codpost) REFERENCES Post(codpost)
	)
""")

cur.execute("""
	CREATE TABLE CopiaLibro(
		codCopia integer primary key autoincrement,
		codLibro integer,
		FOREIGN KEY(codLibro) REFERENCES Book(codLibro)
	)
""")

cur.execute("""
	CREATE TABLE Solicitud(
		usuarioEnvia varchar(15),
		usuarioReceptor varchar(15),
		primary key (usuarioEnvia, usuarioReceptor),
		FOREIGN KEY (usuarioReceptor) REFERENCES  User(nomusuario) ON UPDATE CASCADE ,
		FOREIGN KEY (usuarioEnvia) REFERENCES  User(nomusuario) ON UPDATE CASCADE
	)
""")

cur.execute("""
	CREATE TABLE Amigo(
		usuarioA varchar(15),
		usuarioB varchar(15),
		primary key (usuarioA, usuarioB),
		FOREIGN KEY (usuarioA) REFERENCES  User(nomusuario) ON UPDATE CASCADE,
		FOREIGN KEY (usuarioB) REFERENCES  User(nomusuario) ON UPDATE CASCADE
	)
""")

cur.execute("""
	CREATE TABLE Resenia(
		codLibro integer,
		usuario varchar(15),
		texto TEXT,
		estrellas integer,
		primary key (usuario, codLibro),
		FOREIGN KEY (usuario) REFERENCES  User(nomusuario) ON UPDATE CASCADE,
		FOREIGN KEY (codLibro) REFERENCES  Book(codLibro)
	)
""")

cur.execute("""
	CREATE TABLE Reserva(
		codCopia integer,
		usuario varchar(15),
		fechaInicio DATE,
		fechaDev DATE,
		primary key (usuario, codCopia, fechaInicio),
		FOREIGN KEY (usuario) REFERENCES  User(nomusuario) ON UPDATE CASCADE,
		FOREIGN KEY (codCopia) REFERENCES  CopiaLibro(codCopia)
	)
""")

cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		nomusuario varchar(15),
		last_login float,
		FOREIGN KEY(nomusuario) REFERENCES User(nomusuario) ON UPDATE CASCADE
	)
""")

### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES ('{user['nomusuario']}', '{user['nombres']}', '{user['email']}', '{dataBase_password}', '{user['dni']}', {user['rol']}, {user['deshabilitado']})""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r', encoding="utf8") as f:
	libros = [x.split("\t") for x in f.readlines()]

cont = 1
for author, title, cover, description in libros:
	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author, cover, description.strip()))
	cur.execute("INSERT INTO CopiaLibro VALUES (NULL,?)",
		            (cont,))
	cur.execute("INSERT INTO CopiaLibro VALUES (NULL,?)",
				(cont,))
	cont +=1
	con.commit()



