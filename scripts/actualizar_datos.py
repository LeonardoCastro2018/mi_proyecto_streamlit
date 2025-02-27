# 🔄 **Archivo: actualizar_datos.py**

import sqlite3
import requests
import time

# ✅ **Función para obtener los datos de la API**
def obtener_partidos_api():
    url = "https://api.football-data.org/v4/competitions/PL/matches"
    headers = {"X-Auth-Token": "1e784d0236db4564b2c243469dac77c6"}  # ⚠️ Reemplaza 'TU_API_KEY' con tu clave real

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        partidos = []

        for partido in data.get("matches", []):
            fecha = partido.get("utcDate", "No disponible").split("T")[0]
            equipo_local = partido.get("homeTeam", {}).get("name", "Desconocido")
            equipo_visitante = partido.get("awayTeam", {}).get("name", "Desconocido")
            estado = partido.get("status", "Desconocido")
            resultado_local = partido.get("score", {}).get("fullTime", {}).get("home", "-")
            resultado_visitante = partido.get("score", {}).get("fullTime", {}).get("away", "-")
            resultado = f"{resultado_local} - {resultado_visitante}"

            partidos.append((fecha, equipo_local, equipo_visitante, estado, resultado))

        return partidos

    except requests.RequestException as e:
        print(f"❌ Error al obtener datos de la API: {e}")
        return []

# 💾 **Función para guardar los datos en la base de datos**
def guardar_en_db(partidos):
    conn = sqlite3.connect('partidos.db')
    cursor = conn.cursor()

    # Limpia los datos antiguos
    cursor.execute("DELETE FROM partidos")
    
    # Inserta los datos nuevos
    cursor.executemany('''
        INSERT INTO partidos (fecha, equipo_local, equipo_visitante, estado, resultado)
        VALUES (?, ?, ?, ?, ?)
    ''', partidos)

    conn.commit()
    conn.close()
    print("✅ Datos actualizados en la base de datos.")

# ⏳ **Bucle de actualización cada 5 minutos**
if __name__ == "__main__":
    while True:
        print("🔄 Actualizando datos...")
        partidos = obtener_partidos_api()
        if partidos:
            guardar_en_db(partidos)
            print("✅ Datos actualizados exitosamente. Esperando 5 minutos...")
        else:
            print("⚠️ No se encontraron datos para actualizar.")
        
        time.sleep(300)  # 5 minutos
