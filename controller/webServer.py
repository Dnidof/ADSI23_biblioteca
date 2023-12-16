from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


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
	user = library.get_user(email, password)
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

@app.route('/gestionusuarios')
def gestionUsuarios():
	if 'user' in dir(request) and request.user and request.user.token and request.user.isAdmin():
		return render_template("gestionusuarios.html")
	else:
		return render_template("index.html")


@app.route('/addusuario')
def gestionUsuarios():
	if 'user' in dir(request) and request.user and request.user.token and request.user.isAdmin():
		return render_template("addusuario.html")
	else:
		return render_template("index.html")

@app.route('/eliminarusuario')
def gestionUsuarios():
	if 'user' in dir(request) and request.user and request.user.token and request.user.isAdmin():
		return render_template("eliminarusuario.html")
	else:
		return render_template("index.html")

@app.route('/addlibro')
def gestionUsuarios():
	if 'user' in dir(request) and request.user and request.user.token and request.user.isAdmin():
		return render_template("addlibro.html")
	else:
		return render_template("index.html")
