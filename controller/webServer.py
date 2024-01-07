from .GestorLibros import GestorLibros
from .GestorTemas import GestorTemas
from .GestorUsuarios import GestorUsuarios
from .GestorReservas import GestorReservas, ReservaImposible
from flask import Flask, render_template, request, make_response, redirect
from model.Tema import Tema

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')

library = GestorLibros()
gestorUsuarios = GestorUsuarios()
gestor_temas = GestorTemas()
gestor_reservas = GestorReservas()

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
        nb_users -= 1  # remove current user
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


@app.route('/profile')
def profile():
    user = request.user
    resp = render_template("profile.html", user=user)
    return resp

@app.route('/resenas/<cod>')
def resenas(cod):
    try:
        resenas = library.get_resenas(cod)
    except IndexError:
        return "No existe el libro"
    page = int(request.values.get("page", 1))
    first = (page - 1) * 6
    total_pages = (len(resenas) // 6) + 1
    book = library.get_book(cod)
    resp = render_template("resenas.html", resenas=resenas[first:first + 6], current_page=page,
                           total_pages=total_pages, max=max, min=min, book=book)
    return resp

@app.route('/libro/<cod>')
def libro(cod):
    try:
        libro = library.get_book(cod)
    except IndexError:
        return "No existe el libro"
    logged = 'user' in dir(request) and request.user and request.user.token
    copias = libro.get_copies()
    disponibles = len([copia for copia in copias if copia.disponible()])
    resp = render_template("book.html", book=libro, copias=len(copias), disponibles=disponibles, logged=logged)
    return resp

@app.route('/resena/<cod>')
def resena(cod):
    try:
        libro = library.get_book(cod)
    except IndexError:
        return render_template("error.html", error="No existe el libro")
    logged = 'user' in dir(request) and request.user and request.user.token
    if not logged:
        return redirect("/login")
    resp = render_template("resena_form.html", book=libro)
    return resp

@app.route('/crear_resena', methods=['POST'])
def crear_resena():
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    cod = request.form.get("book_id")
    book = library.get_book(cod)
    user = request.user
    texto = request.form.get("resena")
    try:
        rating = int(request.form.get("rating"))
        book.add_resena(user, texto, rating)
    except ValueError as e:
        return render_template("error.html", error=str(e))

    resp = redirect(f"/libro/{cod}")
    return resp

@app.route('/crear_reserva', methods=['POST'])
def crear_reserva():
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    cod = request.form.get("book_id")
    book = library.get_book(cod)
    date = request.form.get("date")
    try:
        gestor_reservas.crear_reserva(book, request.user, date)
        resp = redirect("/misLibros")
    except ReservaImposible as e:
        return render_template("error.html", error=str(e)), 400
    return resp

@app.route('/eliminar', methods=['GET'])
def eliminar_reserva():
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    copia = request.values.get("l", "")
    date = request.values.get("date", "")
    try:
        gestor_reservas.cancelar_reserva(copia, request.user.username, date)
    except ValueError as e:
        return render_template("error.html", error=str(e)), 400    
    resp = redirect("/misLibros")
    return resp

@app.route('/reservar/<cod>')
def reservar(cod):
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    libro = library.get_book(cod)
    copias = libro.get_copies()
    resp = render_template("reservar_form.html", book=libro, copias=copias)
    return resp

@app.route('/ampliar/<cod>')
def ampliar(cod):
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    libro = library.obtener_libro_desde_copia(cod)
    resp = render_template("ampliar_reserva_form.html", book=libro, cod_copia=cod)
    return resp

@app.route('/ampliar_reserva', methods=['POST'])
def ampliar_reserva():
    if 'user' not in dir(request) or not request.user or not request.user.token:
        resp = redirect("/login")
        return resp
    cod = request.form.get("codCopia")
    date = request.form.get("date")
    try:
        gestor_reservas.ampliar_reserva(cod, request.user.username, date)
        resp = redirect("/misLibros")
    except ReservaImposible as e:
        return render_template("error.html", error=str(e)), 400
    return resp


@app.route('/misLibros')
def misLibros():
    # books, nb_books = library.search_my_books(request.user)
    titulo = request.values.get("title", "")
    autor = request.values.get("author", "")
    reservas = gestor_reservas.get_reservas_usuario(request.user, titulo, autor)
    page = int(request.values.get("page", 1))
    first = (page - 1) * 6
    total_pages = (len(reservas) // 6) + 1
    return render_template('misLibros.html', books=reservas[first:first+6], titulo=titulo, autor=autor, current_page=page,
                           total_pages=total_pages, max=max, min=min)


@app.route('/amigos')
def gestionaramigos():
    if 'user' in dir(request) and request.user and request.user.token:
        amigos_usernames = [amigo.username for amigo in gestorUsuarios.get_user_friends(request.user)]

        amigos_info = []
        for amigo_username in amigos_usernames:
            amigo = gestorUsuarios.get_user_by_username(amigo_username)
            if amigo:
                amigos_info.append({
                    'username': amigo.username,
                    'name': amigo.name,
                })
        return render_template("amigos.html", amigos=amigos_info)
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp


@app.route('/solicitudes')
def mostrar_solicitudes():
    if 'user' in dir(request) and request.user and request.user.token:
        solicitantes = gestorUsuarios.getSolicitudes(request.user)
        print(solicitantes)
        return render_template("solicitudes.html", solicitantes=solicitantes)
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp


@app.route('/rechazar_solicitud', methods=['POST'])
def rechazar_solicitud():
    if 'user' in dir(request) and request.user and request.user.token:
        solicitante = request.form.get("solicitante")
        gestorUsuarios.rechazar_solicitud(request.user.username, solicitante)
        return redirect('/solicitudes')
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp


@app.route('/aceptar_solicitud', methods=['GET', 'POST'])
def aceptar_solicitud():
    if 'user' in dir(request) and request.user and request.user.token:
        solicitante = request.form.get("solicitante")
        gestorUsuarios.aceptar_solicitud(request.user.username, solicitante)
        return redirect('/solicitudes')
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp


@app.route('/perfil_amigo/<username>')
def perfil_amigo(username):
    if 'user' in dir(request) and request.user and request.user.token:
        return render_template('perfil_amigo.html', amigo=username)


@app.route('/eliminar_amigo', methods=['POST'])
def eliminar_amigo():
    if 'user' in dir(request) and request.user and request.user.token:
        amigo_username = request.values.get("amigo_username")  # Usar "amigo" directamente desde la URL
        gestorUsuarios.eliminar_amigo(request.user.username, amigo_username)
        return redirect('/amigos.html')
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp


@app.route('/perfil_solicitud/<username>')
def perfil_solicitud(username):
    if 'user' in dir(request) and request.user and request.user.token:
        # Obtener información de la solicitud
        return render_template('perfil_solicitud.html', solicitud=username)


@app.route('/devolverLibro/<cod>')
def devolver_libro(cod):
    gestor_reservas.devolver_libro(cod)
    return redirect('/misLibros')


@app.route('/editarPerfil', methods=['GET', 'POST'])
def editar_perfil():
    if request.method == 'POST':
        ##guardar info
        nombre = request.values.get("nombre", "")
        dni = request.values.get("dni", "")

        success = request.user.editar_perfil(nombre, dni)
        if success:
            return redirect('/profile')
        else:
            return redirect('/editarPerfil')
    else:
        user = request.user
        return render_template('editarperfil.html', user=user, error=False)
@app.route('/foro')
def foro():
    texto = request.values.get("texto", "")
    page = int(request.values.get("page", 1))
    temas, nb_temas = gestor_temas.search_temas(texto=texto, page=page - 1)
    total_pages = (nb_temas // 6) + 1
    if 'user' in dir(request) and request.user and request.user.token:
        usuario=request.user

    else:
        usuario=None
    return render_template('foro.html', temas=temas, current_page=page,total_pages=total_pages, max=max, min=min, user=usuario)

@app.route('/crear_tema', methods=['GET', 'POST'])
def crear_tema():
    if 'user' in dir(request) and request.user and request.user.token:
        texto = request.form.get("texto")
        gestor_temas.addTema(texto=texto, autor=request.user.username)
        return redirect('/foro')
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp

@app.route('/post/<int:cod>')
def post(cod):
    texto = request.values.get("texto", "")
    page = int(request.values.get("page", 1))
    tema = Tema(cod, "", "")
    comentarios = tema.comentarios()
    nb_comentarios = len(comentarios)
    total_pages = (nb_comentarios // 6) + 1
    if 'user' in dir(request) and request.user and request.user.token:
        usuario = request.user

    else:
        usuario = None
    return render_template('post.html',tema=tema, comentarios=comentarios, current_page=page, total_pages=total_pages, max=max, min=min,
                           user=usuario)


@app.route('/post/<int:cod>/crearComentario', methods=['GET', 'POST'])
def postCrear(cod):
    if 'user' in dir(request) and request.user and request.user.token:
        texto = request.form.get("contenido")
        tema = Tema(cod, "", "")

        tema.agregar_comentario(autor=request.user.username, contenido=texto)
        return redirect(f'/post/{cod}')
    else:
        path = request.values.get("path", "/")
        resp = redirect(path)
        return resp
    return resp
