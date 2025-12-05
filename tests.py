import unittest
import sqlite3
import os
from app import app
from predictor import calcular_prediccion

# Nombre de la base de datos de prueba
TEST_DB = 'test_cultivos.db'


class TestSistemaCompleto(unittest.TestCase):

    # --- CONFIGURACIÓN (Se ejecuta antes de cada test) ---
    def setUp(self):
        # Modo prueba activado
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()

        # Crear BD temporal limpia
        self.conn = sqlite3.connect(TEST_DB)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cultivo TEXT, fecha DATE, volumen_kg REAL, precio_unitario REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS clima (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fecha DATE, temperatura REAL, precipitacion REAL, evento TEXT)''')
        self.conn.commit()

        # Redirigir la app a la BD de prueba
        self.original_connect = sqlite3.connect
        sqlite3.connect = lambda *args, **kwargs: self.original_connect(
            TEST_DB)

    # --- LIMPIEZA (Se ejecuta al terminar cada test) ---
    def tearDown(self):
        self.conn.close()
        sqlite3.connect = self.original_connect
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # ======================================================
    # 1. PRUEBAS DE INFRAESTRUCTURA (¿La App funciona?)
    # ======================================================

    def test_01_web_disponible(self):
        """Verifica que la página de inicio carga (Código 200 OK)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200,
                         "Error: El servidor web no responde.")

    def test_02_guardar_datos(self):
        """Verifica que la base de datos acepta nueva información."""
        self.client.post('/guardar_venta', data={
            'cultivo': 'Palta', 'fecha': '2023-10-01', 'volumen': '500', 'precio': '5.00'
        }, follow_redirects=True)

        conn = sqlite3.connect(TEST_DB)
        fila = conn.execute(
            "SELECT * FROM ventas WHERE cultivo='Palta'").fetchone()
        conn.close()
        self.assertIsNotNone(
            fila, "Error: La base de datos no guardó el registro.")

    # ======================================================
    # 2. PRUEBAS DE INTELIGENCIA (¿El algoritmo piensa bien?)
    # ======================================================

    def test_03_tendencia_mercado(self):
        """Si las ventas suben, la predicción debe subir (+5% extra)."""
        conn = sqlite3.connect(TEST_DB)
        # Mes 1: 1000, Mes 2: 2000 (Tendencia al alza)
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Mango', '2023-01', 1000, 2)")
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Mango', '2023-02', 2000, 2)")
        conn.commit()
        conn.close()

        # Ponderado: (1000*1 + 2000*2)/3 = 1666.66
        # Ajuste Tendencia (+5%): 1666.66 * 1.05 = 1750.0
        resultado = calcular_prediccion('Mango')
        self.assertAlmostEqual(
            resultado['prediccion_final'], 1750.0, delta=1.0)

    # ======================================================
    # 3. PRUEBAS DE SOSTENIBILIDAD (¿Los climas funcionan?)
    # ======================================================

    def test_04_escenario_el_nino(self):
        """Caso: El Niño detectado -> Debe reducir 20%."""
        conn = sqlite3.connect(TEST_DB)
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Arándanos', '2023-01', 1000, 5)")
        conn.execute(
            "INSERT INTO clima (fecha, temperatura, precipitacion, evento) VALUES ('2023-12', 28, 50, 'El Niño')")
        conn.commit()
        conn.close()

        resultado = calcular_prediccion('Arándanos')
        # 1000 - 20% = 800
        self.assertTrue(resultado['es_alerta'])
        self.assertEqual(resultado['prediccion_final'], 800.0)

    def test_05_escenario_la_nina(self):
        """Caso: La Niña detectada -> Debe reducir 10%."""
        conn = sqlite3.connect(TEST_DB)
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Palta', '2023-01', 1000, 5)")
        conn.execute(
            "INSERT INTO clima (fecha, temperatura, precipitacion, evento) VALUES ('2023-12', 15, 0, 'La Niña')")
        conn.commit()
        conn.close()

        resultado = calcular_prediccion('Palta')
        # 1000 - 10% = 900
        self.assertTrue(resultado['es_alerta'])
        self.assertEqual(resultado['prediccion_final'], 900.0)

    def test_06_escenario_ola_calor_automatico(self):
        """Caso: Temp > 30°C (sin evento manual) -> Debe reducir 15% automáticamente."""
        conn = sqlite3.connect(TEST_DB)
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Mango', '2023-01', 1000, 5)")
        # No ponemos 'Ola de Calor' en texto, pero ponemos 35 grados
        conn.execute(
            "INSERT INTO clima (fecha, temperatura, precipitacion, evento) VALUES ('2023-12', 35, 0, 'Ninguno')")
        conn.commit()
        conn.close()

        resultado = calcular_prediccion('Mango')
        # 1000 - 15% = 850
        self.assertTrue(resultado['es_alerta'])
        self.assertEqual(resultado['prediccion_final'], 850.0)

    def test_07_escenario_normal(self):
        """Caso: Clima Normal -> No debe alterar la predicción."""
        conn = sqlite3.connect(TEST_DB)
        conn.execute(
            "INSERT INTO ventas (cultivo, fecha, volumen_kg, precio_unitario) VALUES ('Palta', '2023-01', 1000, 5)")
        conn.execute(
            "INSERT INTO clima (fecha, temperatura, precipitacion, evento) VALUES ('2023-12', 22, 0, 'Ninguno')")
        conn.commit()
        conn.close()

        resultado = calcular_prediccion('Palta')
        self.assertFalse(resultado['es_alerta'])
        self.assertEqual(resultado['prediccion_final'], 1000.0)


if __name__ == '__main__':
    print("\n--- EJECUTANDO CERTIFICACIÓN DE CALIDAD COMPLETA ---")
    unittest.main()
