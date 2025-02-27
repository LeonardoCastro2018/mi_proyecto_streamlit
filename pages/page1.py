import streamlit as st
from api_futbol import obtener_partidos_premier

def app():
    st.title("⚽ Partidos de la Premier League")
    st.write("📅 Aquí puedes ver los próximos partidos de la Premier League.")

    df = obtener_partidos_premier()

    if df.empty:
        st.warning("⚠️ No se pudieron cargar los datos de la API.")
    else:
        st.dataframe(df, use_container_width=True)
