from flask import Flask, render_template, request, redirect, url_for, session
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambia esto en producción

# Datos temporales
user_credentials = {'Admin': '12345'}
gastos = {'esenciales': 0, 'no_esenciales': 0}
ingreso_mensual = 0
metas = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    if username in user_credentials and user_credentials[username] == password:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return "Usuario o contraseña incorrectos"

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', gastos=gastos, metas=metas)
    return redirect(url_for('login'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    global gastos, ingreso_mensual
    ingreso_mensual = float(request.form['ingreso'])
    esenciales = float(request.form['esenciales'])
    no_esenciales = float(request.form['no_esenciales'])
    gastos = {'esenciales': esenciales, 'no_esenciales': no_esenciales}
    generar_grafico(ingreso_mensual, esenciales, no_esenciales)
    return redirect(url_for('dashboard'))

def generar_grafico(ingreso, esenciales, no_esenciales):
    categorias = ['Esenciales', 'No Esenciales', 'Ahorro']
    valores = [esenciales, no_esenciales, ingreso - esenciales - no_esenciales]
    
    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Gastos')
    plt.savefig('static/grafico.png')  # Guardar el gráfico
    plt.close()

@app.route('/add_goal', methods=['POST'])
def add_goal():
    global metas, gastos, ingreso_mensual
    nombre_meta = request.form['nombre_meta']
    valor_meta = float(request.form['valor_meta'])
    
    ahorro_mensual = ingreso_mensual - (gastos['esenciales'] + gastos['no_esenciales'])
    if ahorro_mensual > 0:
        dias_necesarios = int((valor_meta / ahorro_mensual) * 30)  # Aproximar a días
    else:
        dias_necesarios = "Inalcanzable con el ingreso actual"
    
    metas.append({
        'nombre': nombre_meta,
        'valor': valor_meta,
        'dias': dias_necesarios
    })
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
