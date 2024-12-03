from flask import Flask, render_template, request, redirect, url_for, session
from jinja2 import Environment, select_autoescape
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.jinja_env.globals['sum'] = sum

# Variables globales
usuarios = {'Admin': '12345'}
ingreso_mensual = 0
gastos_esenciales = []
gastos_no_esenciales = []
metas = []
ahorros = []

# Ruta de inicio (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in usuarios and usuarios[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

# Ruta del dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    total_gastos_esenciales = sum(gastos_esenciales)
    total_gastos_no_esenciales = sum(gastos_no_esenciales)

    return render_template(
        'dashboard.html',
        ingreso=ingreso_mensual,
        gastos_esenciales=gastos_esenciales,
        gastos_no_esenciales=gastos_no_esenciales,
        metas=metas,
        total_gastos_esenciales=total_gastos_esenciales,
        total_gastos_no_esenciales=total_gastos_no_esenciales
    )

# Ruta para agregar ingresos y gastos
@app.route('/add_finances', methods=['GET', 'POST'])
def add_finances():
    global ingreso_mensual
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        ingreso_mensual = float(request.form['ingreso_mensual'])
        gastos_esenciales.append(float(request.form['gasto_esencial']))
        gastos_no_esenciales.append(float(request.form['gasto_no_esencial']))
        ahorros.append(float(request.form['ahorro']))  # Agregar el ahorro
        return redirect(url_for('dashboard'))
    return render_template('add_finances.html')

# Ruta para agregar metas
@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre_meta = request.form['nombre_meta']
        valor_meta = float(request.form['valor_meta'])
        metas.append({'nombre': nombre_meta, 'valor': valor_meta})
        return redirect(url_for('dashboard'))
    return render_template('add_goal.html')

# Ruta para generar el gráfico de metas
@app.route('/graph_goals')
def graph_goals():
    if 'username' not in session:
        return redirect(url_for('login'))

    if not metas:
        return "No hay metas registradas para generar un gráfico."

    # Crear el gráfico
    nombres = [meta['nombre'] for meta in metas]
    valores = [meta['valor'] for meta in metas]

    x = np.arange(len(valores))
    y = np.array(valores)
    coef = np.polyfit(x, y, 1)
    ajuste_lineal = np.poly1d(coef)

    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='skyblue', label='Metas')
    plt.plot(x, ajuste_lineal(x), color='red', linestyle='--', label='Ajuste Lineal')
    plt.xticks(x, nombres, rotation=45)
    plt.ylabel('Valor ($)')
    plt.title('Metas Financieras y Ajuste Lineal')
    plt.legend()
    plt.tight_layout()

    # Guardar gráfico
    graph_path = os.path.join('static', 'graph_goals.png')
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    plt.savefig(graph_path)
    plt.close()

    return render_template('graph.html', graph_path='/static/graph_goals.png')

# Ruta para generar el gráfico de gastos
@app.route('/graph_expenses')
def graph_expenses():
    if 'username' not in session:
        return redirect(url_for('login'))

    if not gastos_esenciales and not gastos_no_esenciales:
        return "No hay datos suficientes para generar un gráfico."

    labels = ['Esenciales', 'No Esenciales']
    valores = [sum(gastos_esenciales), sum(gastos_no_esenciales)]

    # Crear el gráfico
    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightcoral'])
    plt.title('Distribución de Gastos')

    # Guardar el gráfico
    graph_path = os.path.join('static', 'graph_expenses.png')
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    plt.savefig(graph_path)
    plt.close()

    return render_template('graph.html', graph_path='/static/graph_expenses.png')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)