import sqlite3
import pandas as pd


def get_db_connection():
    conn = sqlite3.connect('cultivos.db')
    conn.row_factory = sqlite3.Row
    return conn


def obtener_factor_climatico():
    """
    Analiza el último registro climático para determinar riesgos.
    Retorna: Factor (float), Mensaje (str), Es_Alerta (bool)
    """
    conn = get_db_connection()
    try:
        clima = conn.execute(
            'SELECT * FROM clima ORDER BY fecha DESC, id DESC LIMIT 1').fetchone()
    except sqlite3.OperationalError:
        clima = None
    finally:
        conn.close()

    if not clima:
        # Retorna 3 valores por defecto si no hay datos
        return 1.0, "No hay datos climáticos recientes.", False

    # Verificamos si existe la columna evento
    keys = clima.keys()
    evento = clima['evento'] if 'evento' in keys else "Ninguno"
    temp = clima['temperatura']

    # Lógica de Riesgo Climático
    factor = 1.0
    mensaje = "Condiciones climáticas normales."
    alerta = False

    if evento == "El Niño":
        factor = 0.80  # -20%
        mensaje = "ALERTA: 'El Niño' detectado. Riesgo alto."
        alerta = True
    elif evento == "La Niña":
        factor = 0.90  # -10%
        mensaje = "PRECAUCIÓN: 'La Niña' detectada. Riesgo moderado."
        alerta = True
    elif evento == "Ola de Calor" or (temp is not None and temp > 30):
        factor = 0.85  # -15%
        mensaje = "ALERTA: Altas temperaturas detectadas."
        alerta = True

    return factor, mensaje, alerta


def calcular_prediccion(cultivo_seleccionado):
    conn = get_db_connection()

    # 1. Obtener Historial
    query = "SELECT fecha, volumen_kg FROM ventas WHERE cultivo = ? ORDER BY fecha ASC"
    df = pd.read_sql_query(query, conn, params=(cultivo_seleccionado,))
    conn.close()

    if df.empty:
        return {
            'error': True,
            'mensaje': f"No hay datos históricos para {cultivo_seleccionado}."
        }

    # 2. Promedio Ponderado (Base)
    total_registros = len(df)
    pesos = list(range(1, total_registros + 1))
    numerador = sum(df['volumen_kg'] * pesos)
    denominador = sum(pesos)
    prediccion_base = numerador / denominador

    # 3. Factor de Tendencia (Mercado)
    # Si el último valor es mayor al promedio simple, asumimos tendencia al alza (+5%)
    promedio_simple = df['volumen_kg'].mean()
    ultimo_valor = df['volumen_kg'].iloc[-1]
    ajuste_tendencia = 1.0

    if ultimo_valor > promedio_simple:
        ajuste_tendencia = 1.05  # +5%
    elif ultimo_valor < promedio_simple:
        ajuste_tendencia = 0.95  # -5%

    # 4. Factor Climático (Sostenibilidad)
    factor_clima, mensaje_clima, es_alerta = obtener_factor_climatico()

    # --- CÁLCULO FINAL ---
    # Base * Tendencia * Clima
    resultado_final = prediccion_base * ajuste_tendencia * factor_clima

    return {
        'error': False,
        'cultivo': cultivo_seleccionado,
        'prediccion_base': round(prediccion_base, 2),
        'factor_ajuste': round((1 - factor_clima) * 100),
        'prediccion_final': round(resultado_final, 2),
        'mensaje_clima': mensaje_clima,
        'es_alerta': es_alerta,
        'datos_usados': total_registros
    }
