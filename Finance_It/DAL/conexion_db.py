import mysql.connector

def conexion_db():
    try:
        # Establecer la conexión
        cnx = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='financeit'
            )
        return cnx
    except mysql.connector.Error as err:
        print("Error de conexión: {}".format(err))
        return None

def signup_db(username, name, last_name, mail, password):
    cnx = conexion_db()
    if cnx is not None:
        cursor = cnx.cursor()
        query = """
        INSERT INTO usuarios (username, name, last_name, mail, password)
        SELECT %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM usuarios WHERE username = %s
        )
        """
        cursor.execute(query, (username, name, last_name, mail, password))
        cnx.commit()
        cursor.close()
        cnx.close()

def login_db(username, password):
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

