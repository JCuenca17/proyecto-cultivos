from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
from predictor import calcular_prediccion

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('cultivos.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- RUTAS ---


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ingreso')
def ingreso():
    return render_template('ingreso.html')


@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    if request.method == 'POST':
        cultivo = request.form['cultivo']
        fecha = request.form['fecha']
        volumen = request.form['volumen']
        precio = request.form['precio']
        conn = get_db_connection()
        conn.execute('INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES (?, ?, ?, ?)',
                     (cultivo, fecha, volumen, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('ver_datos'))


@app.route('/cargar_csv', methods=['POST'])
def cargar_csv():
    if 'archivo_csv' not in request.files:
        return "No file", 400
    archivo = request.files['archivo_csv']
    if archivo.filename == '':
        return "No name", 400
    if archivo:
        try:
            df = pd.read_csv(archivo)
            conn = get_db_connection()
            for index, row in df.iterrows():
                conn.execute('INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES (?, ?, ?, ?)',
                             (row['cultivo'], row['fecha'], row['volumen_kg'], row['precio_unitario']))
            conn.commit()
            conn.close()
            return redirect(url_for('ver_datos'))
        except Exception as e:
            return f"Error: {str(e)}"


@app.route('/ver_datos')
def ver_datos():
    conn = get_db_connection()
    ventas = conn.execute(
        'SELECT * FROM ventas ORDER BY fecha DESC').fetchall()
    conn.close()
    return render_template('ver_datos.html', ventas=ventas)


@app.route('/clima')
def clima():
    return render_template('clima.html')

# --- AQUÍ ESTABA EL ERROR, YA CORREGIDO ---


@app.route('/guardar_clima', methods=['POST'])
def guardar_clima():
    if request.method == 'POST':
        fecha = request.form['fecha']
        temp = request.form['temperatura']
        precip = request.form['precipitacion']
        evento = request.form.get('evento', 'Ninguno')

        conn = get_db_connection()
        try:
            # Ahora sí guardamos el 'evento'
            conn.execute('INSERT INTO clima (fecha, temperatura, precipitacion, evento) VALUES (?, ?, ?, ?)',
                         (fecha, temp, precip, evento))
            conn.commit()
            # Mensaje en consola para confirmar
            print(f"Clima guardado: {evento} - {temp}°C")
        except Exception as e:
            print(f"Error guardando clima: {e}")
        finally:
            conn.close()

        return redirect(url_for('index'))


@app.route('/prediccion', methods=['GET', 'POST'])
def prediccion():
    resultado = None
    if request.method == 'POST':
        cultivo = request.form['cultivo']
        resultado = calcular_prediccion(cultivo)
    return render_template('prediccion.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
