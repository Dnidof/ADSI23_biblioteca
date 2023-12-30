from .GestorLibros import GestorLibros
from .GestorUsuarios import GestorUsuarios
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = GestorLibros()
gestorUsuarios = GestorUsuarios()

@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = gestorUsuarios.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token
				request.admin = request.user.isAdmin()


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	titulo = request.values.get("title", "")
	autor = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(titulo=titulo, autor=autor, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, titulo=titulo, autor=autor, current_page=page,
	                       total_pages=total_pages, max=max, min=min)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = gestorUsuarios.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

@app.route('/addusuario', methods=['GET', 'POST'])
def addUsuario():
	if 'user' in dir(request) and request.user and request.user.token and request.admin:
		errores = []
		if request.method == "POST":
			usuario = request.values.get("usuario")
			nombre = request.values.get("nombre")
			correo = request.values.get("correo")
			password = request.values.get("password")
			dni = request.values.get("dni")
			rol = 1 if request.values.get("rol") == "1" else 0
			deshabilitado = 0

			if usuario and nombre and correo and password and dni and rol is not None:

				if len(usuario) > 15:
					errores.append("El nombre de usuario debe tener entre 1-15 caracteres")
				if len(nombre) > 20:
					errores.append("El nombre debe tener entre 1-20 caracteres")
				if len(correo) > 30:
					errores.append("El correo debe tener como máximo 30 caracteres")
				if len(password) > 32:
					errores.append("La contraseña debe tener como máximo 32 caracteres")
				if len(dni) != 9:
					errores.append("El DNI debe tener 9 caracteres")

				if len(errores) == 0:
					usuarioDisponible = not gestorUsuarios.checkUsernameExists(usuario)
					correoDisponible = not gestorUsuarios.checkEmailExists(correo)

					if not usuarioDisponible:
						errores.append("Nombre de usuario no disponible")
					if not correoDisponible:
						errores.append("Correo no disponible")
			else:
				errores.append("Todos los campos son obligatorios")

			if len(errores) == 0:
				gestorUsuarios.addUser(usuario, nombre, correo, password, dni, rol, deshabilitado)

		resp = render_template("addusuario.html", errores=errores)
	else:
		path = request.values.get("path", "/")
		resp = redirect(path)
	return resp

@app.route('/eliminarusuario', methods=['GET', 'POST'])
def eliminarUsuario():
	if 'user' in dir(request) and request.user and request.user.token and request.admin:
		if request.method == "POST":
			username = request.values.get("nomusuario")
			if username:
				gestorUsuarios.deleteUser(username)

		page = int(request.values.get("page", 1))
		users, nb_users = gestorUsuarios.getUsers(page=page - 1)
		nb_users -= 1 # remove current user
		total_pages = (nb_users // 6) + 1

		# remove current user from search
		results = []
		for usr in users:
			if usr.username != request.user.username:
				results.append(usr)

		resp = render_template("eliminarusuario.html", users=results, current_page=page,
							   total_pages=total_pages, max=max, min=min)
	else:
		path = request.values.get("path", "/")
		resp = redirect(path)
	return resp

@app.route('/addlibro', methods=['GET', 'POST'])
def addLibro():
	if 'user' in dir(request) and request.user and request.user.token and request.admin:
		errores = []
		if request.method == "POST":
			titulo = request.values.get("titulo")
			autor = request.values.get("autor")
			foto = request.values.get("foto", "")
			desc = request.values.get("desc")
			if titulo and autor and desc:
				if len(titulo) > 50:
					errores.append("El título debe tener entre 1-50 caracteres")
				if len(autor) > 40:
					errores.append("El autor debe tener entre 1-40 caracteres")
				if foto and len(foto) > 50:
					errores.append("El link de la foto debe tener como máximo 50 caracteres")
				if len(desc) > 65535:
					errores.append("La descripción debe tener como máximo 65535 caracteres")

				if len(errores) == 0:
					books, count = library.search_books(titulo, autor)
					if count != 0:
						errores.append("Ya existe un libro con el mismo título y el mismo autor")
			else:
				errores.append("Rellena los campos de Título, Autor y Descripción, son obligatorios.")

			if len(errores) == 0:
				library.addBook(titulo, autor, foto, desc)

		resp = render_template("addlibro.html", errores=errores)
	else:
		path = request.values.get("path", "/")
		resp = redirect(path)
	return resp

@app.route('/gestionarusuarios')
def gestionarUsuarios():
	if 'user' in dir(request) and request.user and request.user.token and request.admin:
		resp = render_template("gestionarusuarios.html")
	else:
		path = request.values.get("path", "/")
		resp = redirect(path)
	return resp


@app.route('/profile.html')
def    profile():
    user = request.user
    resp = render_template("profile.html", user= user)
    return resp

@app.route('/amigos.html')
def gestionaramigos():
    if 'user' in dir(request) and request.user and request.user.token:
        amigos_info = request.user.getInfoAmigos()
        return render_template("amigos.html", friends=amigos_info['amigos'])
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp

