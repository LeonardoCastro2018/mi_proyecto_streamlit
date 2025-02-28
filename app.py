import streamlit as st
import pandas as pd
import requests
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts")))

import streamlit as st
from pages import page1, page2  # Importamos las páginas


# Mensaje de depuración para verificar que el script se ejecuta correctamente
st.write("✅ Script de Streamlit ejecutándose correctamente...")

# Inicializar el estado de la sesión si no existe
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Inicio"

# Función para verificar credenciales
def check_login(username, password):
    return username == "admin" and password == "admin"

# Función para manejar el login
def login():
    st.title("Inicio de Sesión")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Iniciar Sesión")

    if login_button:
        if check_login(username, password):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# Función para manejar el logout
def logout():
    st.session_state["authenticated"] = False
    st.session_state["selected_page"] = "Inicio"  # Volver a inicio después de cerrar sesión
    st.rerun()

# Si el usuario no está autenticado, mostrar login
if not st.session_state["authenticated"]:
    login()
else:
    # Sidebar con opciones de navegación
    st.sidebar.title("Menú de Navegación")

    # Usamos `st.radio` con `key="nav_radio"` para que Streamlit no lo resetee
    selected_option = st.sidebar.radio("Selecciona una página", 
                                       ["Inicio", "Página 1", "Página 2"], 
                                       index=["Inicio", "Página 1", "Página 2"].index(st.session_state["selected_page"]),
                                       key="nav_radio")

    # Solo actualizamos el estado si cambia la selección
    if selected_option != st.session_state["selected_page"]:
        st.session_state["selected_page"] = selected_option
        st.rerun()  # Forzar actualización para cambiar la página sin fallos

    st.sidebar.button("Cerrar Sesión", on_click=logout)

    # Cargar las páginas según la opción seleccionada
    if st.session_state["selected_page"] == "Inicio":
        st.write("## Bienvenido a la aplicación interactiva con Streamlit")
        st.write("Selecciona una opción en el menú lateral para comenzar.")
    elif st.session_state["selected_page"] == "Página 1":
        page1.app()
    elif st.session_state["selected_page"] == "Página 2":
        page2.app()

