import mysql.connector, auxiliares.constantes

def conexion_db():
    """Función para conectar la DB"""
    try:
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

def signup_db(name, last_name, mail, username, password):
    """Función para crear un nuevo usuario en la DB"""
    cnx = conexion_db()
    if cnx is not None:
        cursor = cnx.cursor()
        query = """INSERT INTO usuario (name, last_name, mail, username, password) VALUES
        (%s, %s, %s, %s, %s);"""
        cursor.execute(query, (name, last_name, mail, username, password))
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    else:
        return False
    
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
