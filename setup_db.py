import sqlite3

# Conectamos (se creará el archivo nuevo)
conexion = sqlite3.connect('cultivos.db')
cursor = conexion.cursor()

# 1. Tabla de Ventas (Igual que antes)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cultivo TEXT NOT NULL,
        fecha DATE NOT NULL,
        volumen_kg REAL NOT NULL,
        precio_unitario REAL
    )
''')

# 2. Tabla de Clima (AHORA CON LA COLUMNA 'EVENTO')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clima (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        temperatura REAL,
        precipitacion REAL,
        evento TEXT  -- <--- Nueva columna necesaria
    )
''')

print("¡Base de datos 'cultivos.db' actualizada y creada con éxito!")

conexion.commit()
conexion.close()
