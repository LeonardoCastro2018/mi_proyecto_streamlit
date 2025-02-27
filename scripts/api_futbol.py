import streamlit as st
import requests
import pandas as pd
import sqlite3

API_URL = "https://api.football-data.org/v4/competitions/PL/matches"
API_KEY = "1e784d0236db4564b2c243469dac77c6"  # 👉 Reemplaza con tu API KEY

@st.cache_data(ttl=300)  # 🕒 Cachea los datos por 5 minutos
def obtener_partidos_premier():
    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        partidos = []
        for partido in data.get('matches', []):
            partidos.append({
                'fecha': partido['utcDate'][:10],
                'equipo_local': partido['homeTeam']['name'],
                'equipo_visitante': partido['awayTeam']['name'],
                'estado': partido['status'],
                'resultado': f"{partido['score']['fullTime']['home']} - {partido['score']['fullTime']['away']}"
            })

        df = pd.DataFrame(partidos)
        guardar_en_db(df)
        return df
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al obtener datos: {e}")
        return pd.DataFrame()

def guardar_en_db(df):
    conexion = sqlite3.connect('database/premier_league.db')
    df.to_sql('partidos', conexion, if_exists='replace', index=False)
    conexion.close()
    print("✅ Datos guardados en la base de datos.")
