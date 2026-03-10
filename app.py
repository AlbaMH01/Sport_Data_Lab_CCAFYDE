import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Generar datos ficticios para 20 jugadores
n_jugadores = 20
nombres = [
    "Lamine Yamal", "Nico Williams", "Rodri", "Pedri", "Gavi", 
    "Carvajal", "Le Normand", "Cucurella", "Dani Olmo", "Morata",
    "Zubimendi", "Baena", "Ferran", "Oyarzabal", "Grimaldo", 
    "Vivian", "Laporte", "Navas", "Merino", "Fabian"
]

posiciones = ["Extremo", "Extremo", "Medio", "Medio", "Medio", 
              "Defensa", "Defensa", "Defensa", "Medio", "Delantero",
              "Medio", "Medio", "Extremo", "Delantero", "Defensa",
              "Defensa", "Defensa", "Defensa", "Medio", "Medio"]

data = {
    "Nombre": nombres,
    "Posicion": posiciones,
    # Distancia entre 8 y 13 km
    "Distancia_km": np.round(np.random.uniform(8.5, 12.8, n_jugadores), 2),
    # Sprints entre 10 y 45
    "Sprints": np.random.randint(10, 48, n_jugadores),
    # % Pases éxito entre 70 y 95
    "Pases_Exito": np.random.randint(70, 96, n_jugadores),
    # RPE (Fatiga percibida) del 1 al 10
    "RPE_Fatiga": np.random.randint(3, 10, n_jugadores),
    # Goles esperados (xG)
    "Goles_xG": np.round(np.random.uniform(0.0, 1.2, n_jugadores), 2)
}

df = pd.DataFrame(data)

# Añadimos un "Outlier" (el caso trampa para la clase)
# Un jugador que ha corrido poco pero está muertísimo (RPE 10)
df.loc[df['Nombre'] == 'Morata', 'Distancia_km'] = 6.2
df.loc[df['Nombre'] == 'Morata', 'RPE_Fatiga'] = 10

st.set_page_config(layout="wide")
st.title("🚀 Sport Data Lab: 1º CCAFYDE")

tab1, tab2, tab3 = st.tabs(["👤 Perfil Individual", "📊 Comparativa Equipo", "🧠 Correlaciones Tácticas"])

# --- TAB 1: RADAR CHART (ANÁLISIS 1 vs 1) ---
with tab1:
    st.header("Análisis de Perfil de Jugador")
    jugador = st.selectbox("Selecciona un jugador para ver su 'ADN':", df['Nombre'].unique())
    
    # Filtrar datos del jugador
    datos_jugador = df[df['Nombre'] == jugador].iloc[0]
    metrics = ['Sprints', 'Pases_Exito', 'Distancia_km', 'Goles_xG'] # Ejemplo
    
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=[datos_jugador[m] for m in metrics],
      theta=metrics,
      fill='toself'
    ))
    st.plotly_chart(fig_radar)

# --- TAB 2: RANKING (ESTADO DEL EQUIPO) ---
with tab2:
    st.header("¿Quién destaca en el equipo?")
    metrica_rank = st.selectbox("Elige qué quieres medir:", ["Sprints", "RPE_Fatiga", "Pases_Exito"])
    
    fig_bar = px.bar(df.sort_values(metrica_rank, ascending=False), 
                     x='Nombre', y=metrica_rank, color='Posicion',
                     title=f"Ranking de {metrica_rank}")
    st.plotly_chart(fig_bar)

# --- TAB 3: SCATTER (EL LABORATORIO) ---
with tab3:
    st.header("Laboratorio de Correlaciones")
    col1, col2 = st.columns(2)
    with col1:
        eje_x = st.selectbox("Métrica Física (Eje X)", ["Distancia_km", "Sprints"])
    with col2:
        eje_y = st.selectbox("Métrica Técnica (Eje Y)", ["Pases_Exito", "RPE_Fatiga", "Goles_xG"])
    
    fig_scatter = px.scatter(df, x=eje_x, y=eje_y, color="Posicion", 
                             hover_name="Nombre", size="Sprints", 
                             trendline="ols") # Línea de tendencia para que vean si hay relación
    st.plotly_chart(fig_scatter)