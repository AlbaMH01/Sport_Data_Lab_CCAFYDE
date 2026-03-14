import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Scouting Delanteros - CCAFYDE", layout="wide")

@st.cache_data
def cargar_datos_delanteros():
    # Lista de delanteros (mezcla de perfiles: ratones de área, tanques, móviles)
    nombres = [
        "A. Morata", "R. Lewandowski", "K. Mbappé", "E. Haaland", "H. Kane", 
        "Lamine Yamal", "Vini Jr.", "Griezmann", "Julián Álvarez", "Iago Aspas",
        "Artem Dovbyk", "Ante Budimir", "Alexander Sorloth", "Guruzeta", "Hugo Duro",
        "En-Nesyri", "Gerard Moreno", "Samu Omorodion", "Isaac Romero", "Borja Mayoral"
    ]
    
    # Perfiles simulados:
    # xG: Peligro de gol | Toques_Area: Presencia | Sprints: Velocidad
    data = {
        "Nombre": nombres,
        "Goles_xG": np.round(np.random.uniform(0.3, 0.95, len(nombres)), 2),
        "Toques_Area": np.random.randint(4, 12, len(nombres)),
        "Sprints": np.random.randint(15, 45, len(nombres)),
        "Eficacia_%": np.random.randint(10, 30, len(nombres)), # % de tiros que son gol
        "Km_Recorridos": np.round(np.random.uniform(8.0, 11.5, len(nombres)), 1)
    }
    return pd.DataFrame(data)

df = cargar_datos_delanteros()

st.title("🎯 Especialista en Scouting: El '9' Ideal")
st.write("Contexto: Eres el director deportivo y buscas un delantero. ¿Prefieres un rematador de área o uno que corra al espacio?")

tab1, tab2, tab3 = st.tabs(["👤 Perfil Individual", "⚡ Test de Velocidad", "⚽ Laboratorio de Goleadores"])

# --- TAB 1: RADAR (ADN DEL DELANTERO) ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        jugador = st.selectbox("Analiza a un delantero:", df['Nombre'].sort_values())
        st.write("---")
        st.markdown("""
        **Guía de lectura:**
        * **xG:** ¿Sabe desmarcarse bien?
        * **Toques Área:** ¿Es un 'pivote' de área?
        * **Sprints:** ¿Es una amenaza al contraataque?
        """)
    
    with col2:
        vals = df[df['Nombre'] == jugador].iloc[0]
        metrics = ['Goles_xG', 'Toques_Area', 'Sprints']
        # Normalizamos un poco para que el radar se vea bien (rango 0-1)
        r_values = [vals['Goles_xG']*50, vals['Toques_Area']*4, vals['Sprints']] 
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=r_values,
            theta=['Peligro (xG)', 'Presencia (Área)', 'Velocidad (Sprints)'],
            fill='toself',
            line_color='red'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 50])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 2: RANKING ---
with tab2:
    st.header("Ranking: Capacidad de Repetición de Esfuerzos")
    fig_bar = px.bar(df.sort_values("Sprints"), x='Sprints', y='Nombre', orientation='h', 
                     color='Sprints', color_continuous_scale='OrRd')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 3: SCATTER (DECISIÓN FINAL) ---
with tab3:
    st.header("¿Quién es el más eficiente?")
    c1, c2 = st.columns(2)
    with c1:
        eje_x = st.selectbox("Eje X:", ["Toques_Area", "Km_Recorridos"])
    with c2:
        eje_y = st.selectbox("Eje Y:", ["Goles_xG", "Eficacia_%"])

    fig_scatter = px.scatter(df, x=eje_x, y=eje_y, size="Sprints", color="Sprints",
                             hover_name="Nombre", text="Nombre",
                             color_continuous_scale='Viridis')
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.info("💡 CONSEJO: Busca a los que están arriba a la derecha. Tienen mucho volumen de juego y mucha calidad.")