from model import Connection, User
from model.tools import hash_password

db = Connection()

class GestorUsuarios:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GestorUsuarios, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE correo = ? AND password = ? AND deshabilitado = 0",
                         (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT u.* from User u, Session s WHERE u.nomusuario = s.nomusuario AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6])
        else:
            return None

    def checkUsernameExists(self, username):
        user = db.select("SELECT * FROM User WHERE nomusuario = ?", (username,))
        return len(user) > 0

    def checkEmailExists(self, email):
        user = db.select("SELECT * FROM User WHERE correo = ?", (email,))
        return len(user) > 0

    def addUser(self, usuario, nombre, correo, password, dni, rol, deshabilitado):
        db_password = hash_password(password)
        params = (usuario, nombre, correo, db_password, dni, rol, deshabilitado)
        db.insert("INSERT INTO User VALUES(?, ?, ?, ?, ?, ?, ?)", params)

    def getUsers(self, limit=6, page=0):
        count = db.select("""
    					SELECT count() 
    					FROM User 
    			""")[0][0]

        res = db.select("SELECT * from User WHERE deshabilitado = 0 LIMIT ? OFFSET ?", (limit, limit * page))
        users = [
            User(u[0], u[1], u[2], u[4], u[5], u[6])
            for u in res
        ]
        return users, count

    def deleteUser(self, username):
        db.update("UPDATE User SET deshabilitado = 1 WHERE nomusuario = ?", (username, ))

    def get_user_by_username(self, username):
        user_data = db.select("SELECT * from User WHERE nomusuario = ?", (username,))
        if len(user_data) > 0:
            return User(user_data[0][0], user_data[0][1], user_data[0][2], user_data[0][4], user_data[0][5],
                        user_data[0][6])
        else:
            return None

    def get_user_friends(self, user):
        friends_data = db.select("SELECT usuarioB FROM Amigo WHERE usuarioA = ?", (user.username,))
        friends = [self.get_user_by_username(username) for (username,) in friends_data]
        user.amigos = friends
        return friends
    def getSolicitudes(self, user):
        solicitantes_data = db.select("SELECT usuarioEnvia FROM Solicitud WHERE usuarioReceptor = ?", (user.username,))
        user.solicitudesRecibidas = [username for (username,) in solicitantes_data]
        return user.solicitudesRecibidas