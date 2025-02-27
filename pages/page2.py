import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import sqlite3
import plotly.express as px

# Función para obtener datos de la base de datos
def obtener_datos():
    conn = sqlite3.connect('database/premier_league.db')
    df = pd.read_sql_query("SELECT * FROM partidos", conn)
    conn.close()
    return df

# Función para exportar datos a PDF
def exportar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Datos de Partidos - Premier League", ln=True, align='C')

    for index, row in df.iterrows():
        texto = f"{row['fecha']} - {row['equipo_local']} vs {row['equipo_visitante']} - {row['resultado']}"
        pdf.multi_cell(0, 10, txt=texto)

    pdf_file = "datos_partidos.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Descarga del PDF
def obtener_enlace_descarga(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:file/pdf;base64,{b64}" download="datos_partidos.pdf">📄 Descargar PDF</a>'
    return href

# Visualización de la página de Streamlit
def app():
    st.title("📊 Partidos de la Premier League")
    df = obtener_datos()

    if df.empty:
        st.warning("No se encontraron datos en la base de datos.")
    else:
        st.dataframe(df)

        # 📊 Distribución de Resultados (Victorias, Empates, Derrotas)
        st.subheader("📈 Distribución de Resultados (Victorias, Empates, Derrotas)")
        df_filtrado = df[df['resultado'].str.contains(' - ', na=False)]
        df_filtrado[['goles_local', 'goles_visitante']] = (
            df_filtrado['resultado']
            .str.split(' - ', expand=True)
            .apply(pd.to_numeric, errors='coerce')
        )
        df_filtrado = df_filtrado.dropna(subset=['goles_local', 'goles_visitante'])
        
        df_filtrado['resultado_match'] = df_filtrado.apply(
            lambda x: 'Victoria Local' if x['goles_local'] > x['goles_visitante']
            else ('Victoria Visitante' if x['goles_local'] < x['goles_visitante'] else 'Empate'),
            axis=1
        )
        
        resultado_count = df_filtrado['resultado_match'].value_counts().reset_index()
        resultado_count.columns = ['Resultado', 'Cantidad']
        fig_pie = px.pie(resultado_count, names='Resultado', values='Cantidad', title='Distribución de Resultados')
        st.plotly_chart(fig_pie)

        # 🏃‍♂️ Goles Totales (Locales y Visitantes)
        st.subheader("⚽ Goles Totales (Locales y Visitantes)")
        goles_totales = df_filtrado.groupby('equipo_local').agg({'goles_local': 'sum', 'goles_visitante': 'sum'}).reset_index()
        fig_goles = px.bar(goles_totales, x='equipo_local', y=['goles_local', 'goles_visitante'],
                           title='Goles Totales por Equipo (Locales y Visitantes)', barmode='stack')
        st.plotly_chart(fig_goles)

        # 📊 Evolución de Goles por Fecha
        st.subheader("📅 Evolución de Goles por Fecha")
        goles_por_fecha = df_filtrado.groupby('fecha').agg({'goles_local': 'sum', 'goles_visitante': 'sum'}).reset_index()
        goles_por_fecha['goles_totales'] = goles_por_fecha['goles_local'] + goles_por_fecha['goles_visitante']
        fig_line = px.line(goles_por_fecha, x='fecha', y='goles_totales', title='Evolución de Goles Totales por Fecha')
        st.plotly_chart(fig_line)

        # 🔥 Partidos con Más Goles
        st.subheader("🔥 Partidos con Más Goles")
        df_filtrado['goles_totales'] = df_filtrado['goles_local'] + df_filtrado['goles_visitante']
        top_partidos = df_filtrado.sort_values(by='goles_totales', ascending=False).head(10)
        st.dataframe(top_partidos[['fecha', 'equipo_local', 'equipo_visitante', 'resultado', 'goles_totales']])

        # ⚖️ Diferencia de Goles por Equipo
        st.subheader("⚖️ Diferencia de Goles por Equipo")
        diferencia_goles = goles_totales.copy()
        diferencia_goles['diferencia'] = diferencia_goles['goles_local'] - diferencia_goles['goles_visitante']
        fig_diff = px.bar(diferencia_goles, x='equipo_local', y='diferencia',
                          title='Diferencia de Goles por Equipo', color='diferencia', color_continuous_scale='RdBu')
        st.plotly_chart(fig_diff)

        # 🖨️ Botón para imprimir
        st.markdown("""
            <button onclick="window.print()">🖨️ Imprimir Página</button>
        """, unsafe_allow_html=True)

        # 📩 Botón para exportar a PDF
        if st.button("📩 Exportar Resultados a PDF"):
            pdf_file = exportar_pdf(df)
            st.markdown(obtener_enlace_descarga(pdf_file), unsafe_allow_html=True)

if __name__ == "__main__":
    app()
