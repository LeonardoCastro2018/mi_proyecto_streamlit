import sqlite3
import pandas as pd

# ✅ Datos de ejemplo (puedes modificarlos si tienes los datos reales)
datos_partidos = {
    'fecha': ['2024-08-16', '2024-08-17', '2024-08-17'],
    'equipo_local': ['Manchester United FC', 'Ipswich Town FC', 'Arsenal FC'],
    'equipo_visitante': ['Fulham FC', 'Liverpool FC', 'Wolverhampton Wanderers FC'],
    'estado': ['FINISHED', 'FINISHED', 'FINISHED'],
    'resultado': ['1 - 0', '0 - 2', '2 - 0']
}

df = pd.DataFrame(datos_partidos)

# ✅ Crear conexión a la base de datos
conn = sqlite3.connect('partidos_premier_league.db')
cursor = conn.cursor()

# ✅ Crear tabla 'partidos'
cursor.execute('''
CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    equipo_local TEXT,
    equipo_visitante TEXT,
    estado TEXT,
    resultado TEXT
)
''')

# ✅ Insertar datos en la tabla
df.to_sql('partidos', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("✅ Base de datos creada y poblada con éxito.")

