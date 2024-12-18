from flask import Flask, render_template, request, redirect, url_for, session
import json, os, threading, queue
import numpy as np
import matplotlib.pyplot as plt
import Auxiliares.Constantes

app = Flask(__name__)
app.secret_key = Auxiliares.Constantes.MASTERKEY

# Cola para la comunicación entre hilos
graph_queue = queue.Queue()

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

#Formatear numeros con punto a la centesima
def format_number(num):
    return '{:,.0f}'.format(num).replace(',', '.')

app.jinja_env.filters['format_number'] = format_number

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
# DASHBOARD DE USUARIO LOGGEADO
@app.route('/dashboard')
def dashboard():
    username = session.get('username')  # Obtener el nombre de usuario de la sesión
    ingresos = 0
    gastos_esenciales = 0
    gastos_no_esenciales = 0

    # Cargar datos de transacciones
    file_path = os.path.join(os.path.dirname(__file__), 'datos.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                for transaction in data:
                    if transaction['username'] == username:  # Filtrar por usuario
                        if transaction['tipo_transaccion'] == 'ingreso':
                            ingresos += float(transaction['monto'])
                        elif transaction['tipo_transaccion'] == 'gasto':
                            if transaction['tipo_gasto'] == 'Gasto Esencial':
                                gastos_esenciales += float(transaction['monto'])
                            elif transaction['tipo_gasto'] == 'No Esencial':
                                gastos_no_esenciales += float(transaction['monto'])
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")

    # Cargar metas
    goals = load_goals()  # Cargar metas desde el archivo JSON

    # Filtrar metas por el usuario logueado
    user_goals = [goal for goal in goals if goal['username'] == username]

    # Calcular dinero restante
    total_gastos = gastos_esenciales + gastos_no_esenciales
    dinero_restante = ingresos - total_gastos

    # Convertir a enteros
    ingresos = int(ingresos)
    gastos_esenciales = int(gastos_esenciales)
    gastos_no_esenciales = int(gastos_no_esenciales)
    dinero_restante = int(dinero_restante)

    return render_template('dashboard.html', ingreso=ingresos, gastos_esenciales=gastos_esenciales, gastos_no_esenciales=gastos_no_esenciales, metas=user_goals, dinero_restante=dinero_restante)

# INGRESO DE DATOS
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        tipo_transaccion = request.form.get('tipo-transaccion')
        monto = request.form.get('Monto')
        fecha = request.form.get('Fecha')
        descripcion = request.form.get('Descripción')
        tipo_gasto = request.form.get('tipo_gasto') if tipo_transaccion == 'gasto' else None
        
        # Obtener el nombre de usuario de la sesión
        username = session.get('username')

        # Guardarlos en un archivo JSON:
        data = {
            'tipo_transaccion': tipo_transaccion,
            'monto': monto,
            'fecha': fecha,
            'descripcion': descripcion,
            'tipo_gasto': tipo_gasto,
            'username': username  # Agregar el nombre de usuario
        }
        
        # Guardar en el archivo JSON
        data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos.json')
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r+') as f:
                existing_data = json.load(f)
                existing_data.append(data)
                f.seek(0)
                json.dump(existing_data, f)
        else:
            with open(data_file_path, 'w') as f:
                json.dump([data], f)

        return redirect(url_for('dashboard'))

    return render_template('add_data.html')

# Función para cargar metas desde el archivo JSON
def load_goals():
    file_path = os.path.join(os.path.dirname(__file__), 'metas.json')  # Ruta del archivo metas.json
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error al leer el archivo metas.json. El archivo puede estar corrupto.")
                return []
    return []

# Función para guardar metas en el archivo JSON
def save_goals(goals):
    file_path = os.path.join(os.path.dirname(__file__), 'metas.json')  # Ruta del archivo metas.json
    try:
        with open(file_path, 'w') as f:
            json.dump(goals, f)
    except Exception as e:
        print("Error al guardar metas:", e)

# Ruta para agregar metas
@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        name_goal = request.form.get('name_goal')
        valor_meta = request.form.get('valor_meta')
        descr_goal = request.form.get('descr_goal')

        # Obtener el nombre de usuario de la sesión
        username = session.get('username')

        # Crear un diccionario para la nueva meta
        new_goal = {
            'name_goal': name_goal,
            'valor_meta': valor_meta,
            'descr_goal': descr_goal,
            'username': username  # Asociar la meta al usuario
        }

        # Cargar metas existentes
        goals = load_goals()
        goals.append(new_goal)  # Añadir la nueva meta a la lista

        # Guardar las metas actualizadas en el archivo
        save_goals(goals)

        return redirect(url_for('dashboard'))  # Redirigir al dashboard después de agregar la meta

    return render_template('add_goal.html')  # Renderizar el formulario para agregar metas

# GENERACIÓN DE GRAFICOS Y VISTA DE GRAFICOS
# Función para generar el gráfico
def generate_graph(username):
    ingresos_graph2 = []
    fechas = []

    # Cargar datos de transacciones
    file_path = os.path.join(os.path.dirname(__file__), 'datos.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                for transaction in data:
                    if transaction['username'] == username and transaction['tipo_transaccion'] == 'ingreso':
                        ingresos_graph2.append(float(transaction['monto']))
                        fechas.append(transaction['fecha'])  # Suponiendo que tienes fechas

            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")

    # Imprimir los valores para depuración
    print(f'Ingresos: {ingresos_graph2}')

    # Calcular el ajuste exponencial
    if ingresos_graph2:
        x = np.arange(len(ingresos_graph2))  # Índices de los ingresos
        y = np.array(ingresos_graph2)

        # Ajuste exponencial
        def exp_func(x, a, b):
            return a * np.exp(b * x)

        # Realizar el ajuste
        from scipy.optimize import curve_fit
        popt, _ = curve_fit(exp_func, x, y, p0=(1, 0.1))

        # Generar valores ajustados
        y_fit = exp_func(x, *popt)

        # Graficar
        plt.figure()
        plt.scatter(x, y, label='Datos de Ingresos', color='blue')
        plt.plot(x, y_fit, label='Ajuste Exponencial', color='red')
        plt.title('Ajuste Exponencial de Ingresos')
        plt.xlabel('Tiempo (días)')
        plt.ylabel('Ingresos')
        plt.legend()

        # Guardar la figura en un archivo
        graph_file_path = os.path.join(os.path.dirname(__file__), 'static', 'graph.png')
        plt.savefig(graph_file_path)
        plt.close()  # Cerrar la figura para liberar memoria

        # Poner la ruta del gráfico en la cola
        graph_queue.put(graph_file_path)


@app.route('/graph')
def graph():
    username = session.get('username')  # Obtener el nombre de usuario de la sesión
    ingresos = 0
    gastos_esenciales = 0
    gastos_no_esenciales = 0

    # Cargar datos de transacciones
    file_path = os.path.join(os.path.dirname(__file__), 'datos.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                for transaction in data:
                    if transaction['username'] == username:  # Filtrar por usuario
                        if transaction['tipo_transaccion'] == 'ingreso':
                            ingresos += float(transaction['monto'])
                        elif transaction['tipo_transaccion'] == 'gasto':
                            if transaction['tipo_gasto'] == 'Gasto Esencial':
                                gastos_esenciales += float(transaction['monto'])
                            elif transaction['tipo_gasto'] == 'No Esencial':
                                gastos_no_esenciales += float(transaction['monto'])
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")

    # Iniciar el hilo para generar el gráfico
    threading.Thread(target=generate_graph, args=(username,), daemon=True).start()

    # Comenzar a verificar la cola para ver si el gráfico ha sido generado
    check_graph_queue()

    return render_template('graph.html', ingresos=ingresos, gastos_esenciales=gastos_esenciales, gastos_no_esenciales=gastos_no_esenciales)

def check_graph_queue():
    try:
        graph_file_path = graph_queue.get_nowait()  # Intenta obtener la ruta del gráfico de la cola
        # Aquí puedes hacer algo con la ruta del gráfico, como actualizar la interfaz
        print(f'Gráfico generado: {graph_file_path}')
    except queue.Empty:
        pass  # No hay gráficos generados aún




if __name__ == '__main__':
    app.run(debug=True)