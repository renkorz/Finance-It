from flask import Flask, render_template, request, redirect, url_for, session
import Auxiliares.Constantes
import json, os

app = Flask(__name__)
app.secret_key = Auxiliares.Constantes.MASTERKEY

#Variables globales
ingresos = 0
gastos_esenciales = 0
gastos_no_esenciales = 0

#USUARIOS EN ARCHIVO JSON
def load_users():
    file_path = os.path.join(os.path.dirname(__file__), 'usuarios.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")
                return []
    return []

def save_users(users):
    file_path = os.path.join(os.path.dirname(__file__), 'usuarios.json')
    try:
        with open(file_path, 'w') as f:
            json.dump(users, f)
    except Exception as e:
        print("Error al guardar usuarios:", e)  # Imprime el error en la consola

#INDEX DE LA APP
@app.route('/')
def index():
    return render_template('index.html')

#LOGIN DE USUARIO
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Cargar usuarios desde el archivo JSON
        users = load_users()

        # Verificar si el usuario y la contraseña son correctos
        for user in users:
            if user.get('username') == username and user.get('password') == password:
                session['username'] = username  # Guardar el nombre de usuario en la sesión
                return redirect(url_for('dashboard'))  # Redirigir al dashboard

        # Si no se encontró el usuario o la contraseña es incorrecta
        error = "Nombre de usuario o contraseña incorrectos."
        return render_template('login.html', error=error)

    return render_template('login.html')

#REGISTRO DE USUARIO
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None  # Inicializa la variable de error
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Cargar usuarios desde el archivo JSON
        users = load_users()

        # Verificar si el usuario ya existe
        if any(user['username'] == username for user in users):
            error = f"El nombre de usuario '{username}' ya está en uso."
        # Verificar si el email ya existe
        elif any(user['email'] == email for user in users):
            error = f"El correo electrónico '{email}' ya está en uso."
        else:
            # Agregar el nuevo usuario
            users.append({
                "username": username,
                "email": email,
                "password": password
            })
            save_users(users)  # Guardar los usuarios actualizados en el archivo
            return redirect(url_for('login'))  # Redirigir a la página de inicio de sesión

    return render_template('signup.html', error=error)

#DASHBOARD DE USUARIO LOGGEADO
@app.route('/dashboard')
def dashboard():
    # Cargar datos de transacciones desde el archivo JSON
    file_path = os.path.join(os.path.dirname(__file__), 'datos.json')
    ingresos = 0
    gastos_esenciales = 0
    gastos_no_esenciales = 0

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                for transaction in data:
                    if transaction['tipo_transaccion'] == 'ingreso':
                        ingresos += float(transaction['monto'])
                    elif transaction['tipo_transaccion'] == 'gasto':
                        if transaction['tipo_gasto'] == 'Gasto Esencial':
                            gastos_esenciales += float(transaction['monto'])
                        elif transaction['tipo_gasto'] == 'No Esencial':
                            gastos_no_esenciales += float(transaction['monto'])
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")

    return render_template('dashboard.html', ingreso=ingresos, gastos_esenciales=gastos_esenciales, gastos_no_esenciales=gastos_no_esenciales)

# INGRESO DE DATOS
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        tipo_transaccion = request.form.get('tipo-transaccion')
        monto = request.form.get('Monto')
        fecha = request.form.get('Fecha')
        descripcion = request.form.get('Descripción')
        # Si es un gasto, obtener el tipo de gasto
        tipo_gasto = request.form.get('tipo_gasto') if tipo_transaccion == 'gasto' else None
        
        # Guardarlos en un archivo JSON:
        data = {
            'tipo_transaccion': tipo_transaccion,
            'monto': monto,
            'fecha': fecha,
            'descripcion': descripcion,
            'tipo_gasto': tipo_gasto
        }
        
        # Guardar en un archivo JSON (opcional)
        if os.path.exists('datos.json'):
            with open('datos.json', 'r+') as f:
                existing_data = json.load(f)
                existing_data.append(data)
                f.seek(0)
                json.dump(existing_data, f)
        else:
            with open('datos.json', 'w') as f:
                json.dump([data], f)

        return redirect(url_for('dashboard'))  # Redirigir a otra página después de guardar

    return render_template('add_data.html')  # Renderizar el formulario si es un GET

# INGRESO DE METAS
@app.route('/add_goal')
def add_goal():
    return render_template('add_goal.html')

# GENERACIÓN DE GRAFICOS Y VISTA DE GRAFICOS
@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)