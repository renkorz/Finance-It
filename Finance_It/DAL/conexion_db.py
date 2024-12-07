import mysql.connector
import auxiliares.constantes
from flask import session

def conexion_db():
    """Función para conectar la DB"""
    try:
        # Establecer la conexión
        cnx = mysql.connector.connect(
            user=auxiliares.constantes.user,
            password=auxiliares.constantes.password,
            host=auxiliares.constantes.host,
            database=auxiliares.constantes.database
            )
        return cnx
    except mysql.connector.Error as err:
        print("Error de conexión: {}".format(err))
        return None

def signup_db(username, name, last_name, mail, password):
    """Función para agregar el usuario nuevo en la DB"""
    cnx = conexion_db()
    if cnx is not None:
        cursor = cnx.cursor()
        try:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT 1 FROM usuario WHERE username = %s", (username))
            if cursor.fetchone() is not None:
                print("El nombre de usuario ya existe.")
                return

            # Insertar el nuevo usuario
            query = """
            INSERT INTO usuario (username, name, last_name, mail, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, name, last_name, mail, password))
            cnx.commit()
            print("Registro exitoso.")
        except mysql.connector.Error as err:
            print(f"Error al registrar el usuario: {err}")
        finally:
            cursor.close()
            cnx.close()

def login_db(username, password):
    """Función para buscar las credenciales en la DB"""
    cnx = conexion_db()
    if cnx is not None:
        cursor = cnx.cursor()
        query = "SELECT * FROM usuario WHERE username = %s AND password = %s;"
        cursor.execute(query, (username, password))
        resultados = cursor.fetchall()
        cursor.close()
        cnx.close()
        
        # Verifica si se encontraron resultados
        if len(resultados) > 0:
            return True  # Credenciales correctas
        else:
            return False  # Credenciales incorrectas

def ingrsar_transccion(tipo_t, monto_t, fecha_t):
    """Función para agregar la transacción a la DB"""
    cnx = conexion_db()
    if cnx is not None:
        cursor = cnx.cursor()
        if 'username' in session:
            username = 'username'
            id_usuario = f"SELECT id_usuario FROM Usuario WHERE username = '{username}'"
            query = f"INSERT INTO transaccion (tipo_transaccion, monto_transaccion, fecha, id_usuario) VALUES (%s, %s, %s, {id_usuario})"
            cursor.execute(query, (tipo_t, monto_t, fecha_t))
        else:
            print("usuario no identificado correctamente.")
        cnx.commit()
        cursor.close
        cnx.close

