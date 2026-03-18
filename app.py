import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Football Analytics", layout="wide", page_icon="⚽")

# Diccionario maestro de métricas por posición
METRICAS_MAP = {
    "Portero": ["Paradas", "Pase", "Salida", "Reflejos"],
    "Defensa Central": ["Intercepciones", "Duelos", "Pase", "Velocidad"],
    "Lateral": ["Velocidad", "Centros", "Duelos", "Pase"],
    "Mediocentro": ["Pases Clave", "Vision", "Resistencia", "Regate"],
    "Extremo": ["Regate", "Velocidad", "Goles", "Centros"],
    "Delantero": ["Remate", "Asistencias", "xG", "Velocidad"]
}

# --- 2. CARGA DE DATOS ---
@st.cache_data
def load_data():
    jugadores = [
        # PORTEROS (M1: Paradas, M2: Pase, M3: Salida, M4: Reflejos)
        {"Nombre": "Courtois", "Pos": "Portero", "M1": 85, "M2": 70, "M3": 80, "M4": 90, "x": 50, "y": 7},
        {"Nombre": "Alisson", "Pos": "Portero", "M1": 86, "M2": 85, "M3": 88, "M4": 87, "x": 50, "y": 7},
        {"Nombre": "Ter Stegen", "Pos": "Portero", "M1": 84, "M2": 89, "M3": 85, "M4": 86, "x": 50, "y": 7},
        {"Nombre": "Ederson", "Pos": "Portero", "M1": 82, "M2": 93, "M3": 86, "M4": 80, "x": 50, "y": 7},

        # DEFENSAS CENTRALES (M1: Intercepciones, M2: Duelos, M3: Pase, M4: Velocidad)
        {"Nombre": "Militao", "Pos": "Defensa Central", "M1": 88, "M2": 85, "M3": 75, "M4": 82, "x": 55, "y": 25},
        {"Nombre": "Van Dijk", "Pos": "Defensa Central", "M1": 90, "M2": 92, "M3": 78, "M4": 75, "x": 45, "y": 25},
        {"Nombre": "Rüdiger", "Pos": "Defensa Central", "M1": 86, "M2": 89, "M3": 72, "M4": 84, "x": 65, "y": 25},
        {"Nombre": "Araujo", "Pos": "Defensa Central", "M1": 85, "M2": 91, "M3": 68, "M4": 88, "x": 35, "y": 25},
        {"Nombre": "Ruben Dias", "Pos": "Defensa Central", "M1": 89, "M2": 90, "M3": 82, "M4": 65, "x": 50, "y": 20},

        # LATERALES (M1: Velocidad, M2: Centros, M3: Duelos, M4: Pase)
        {"Nombre": "Walker", "Pos": "Lateral", "M1": 95, "M2": 75, "M3": 82, "M4": 78, "x": 90, "y": 35},
        {"Nombre": "Davies", "Pos": "Lateral", "M1": 96, "M2": 78, "M3": 75, "M4": 77, "x": 10, "y": 35},
        {"Nombre": "Alexander-Arnold", "Pos": "Lateral", "M1": 78, "M2": 92, "M3": 72, "M4": 90, "x": 90, "y": 45},
        {"Nombre": "Theo Hernandez", "Pos": "Lateral", "M1": 93, "M2": 82, "M3": 79, "M4": 81, "x": 10, "y": 45},

        # MEDIOCENTROS (M1: Pases Clave, M2: Vision, M3: Resistencia, M4: Regate)
        {"Nombre": "Modric", "Pos": "Mediocentro", "M1": 92, "M2": 95, "M3": 80, "M4": 88, "x": 35, "y": 60},
        {"Nombre": "Rodri", "Pos": "Mediocentro", "M1": 88, "M2": 90, "M3": 92, "M4": 78, "x": 50, "y": 45},
        {"Nombre": "De Bruyne", "Pos": "Mediocentro", "M1": 95, "M2": 98, "M3": 85, "M4": 82, "x": 65, "y": 60},
        {"Nombre": "Pedri", "Pos": "Mediocentro", "M1": 90, "M2": 94, "M3": 88, "M4": 91, "x": 30, "y": 55},
        {"Nombre": "Bellingham", "Pos": "Mediocentro", "M1": 85, "M2": 87, "M3": 93, "M4": 88, "x": 50, "y": 65},
        {"Nombre": "Bernardo Silva", "Pos": "Mediocentro", "M1": 91, "M2": 92, "M3": 95, "M4": 92, "x": 70, "y": 55},

        # EXTREMOS (M1: Regate, M2: Velocidad, M3: Goles, M4: Centros)
        {"Nombre": "Vinicius", "Pos": "Extremo", "M1": 95, "M2": 97, "M3": 85, "M4": 82, "x": 20, "y": 80},
        {"Nombre": "Salah", "Pos": "Extremo", "M1": 88, "M2": 89, "M3": 92, "M4": 84, "x": 80, "y": 80},
        {"Nombre": "Mbappé", "Pos": "Extremo", "M1": 92, "M2": 97, "M3": 94, "M4": 80, "x": 15, "y": 85},
        {"Nombre": "Saka", "Pos": "Extremo", "M1": 89, "M2": 86, "M3": 84, "M4": 88, "x": 85, "y": 75},
        {"Nombre": "Leao", "Pos": "Extremo", "M1": 91, "M2": 93, "M3": 80, "M4": 78, "x": 15, "y": 75},

        # DELANTEROS (M1: Remate, M2: Asistencias, M3: xG, M4: Velocidad)
        {"Nombre": "Benzema", "Pos": "Delantero", "M1": 94, "M2": 88, "M3": 85, "M4": 78, "x": 45, "y": 85},
        {"Nombre": "Haaland", "Pos": "Delantero", "M1": 96, "M2": 65, "M3": 98, "M4": 90, "x": 50, "y": 92},
        {"Nombre": "Kane", "Pos": "Delantero", "M1": 93, "M2": 85, "M3": 88, "M4": 75, "x": 55, "y": 88},
        {"Nombre": "Lewandowski", "Pos": "Delantero", "M1": 91, "M2": 75, "M3": 85, "M4": 72, "x": 50, "y": 85},
        {"Nombre": "Lautaro Martinez", "Pos": "Delantero", "M1": 89, "M2": 78, "M3": 82, "M4": 83, "x": 40, "y": 88},
    ]
    df_raw = pd.DataFrame(jugadores)
    # Cálculo de Rating ponderado (40% principal, 20% el resto)
    df_raw['Rating'] = (df_raw['M1'] * 0.4 + df_raw['M2'] * 0.2 + df_raw['M3'] * 0.2 + df_raw['M4'] * 0.2).round(1)
    return df_raw

df = load_data()

# --- 3. FUNCIONES VISUALES ---
def draw_half_pitch(df_selection):
    # Proporciones reales de medio campo: 100 de ancho (x) por 50 de alto (y)
    fig = px.scatter(df_selection, x="x_tactic", y="y_tactic", text="Nombre", 
                     range_x=[-5, 105], range_y=[45, 105]) 

    # Dibujamos el medio campo con formas (Shapes)
    fig.update_layout(
        plot_bgcolor="#2e7d32",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
        height=500, # Altura ajustada para que no se vea estirado
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )

    # --- LÍNEAS DEL MEDIO CAMPO ---
    # Línea de banda izquierda, derecha y fondo (superior)
    lines = [
        dict(type="line", x0=0, y0=50, x1=0, y1=100, line_color="white"),
        dict(type="line", x0=100, y0=50, x1=100, y1=100, line_color="white"),
        dict(type="line", x0=0, y0=100, x1=100, y1=100, line_color="white"),
        # Línea de medio campo (inferior)
        dict(type="line", x0=0, y0=50, x1=100, y1=50, line_color="white", line_width=4),
    ]
    
    # Área Grande
    lines.append(dict(type="rect", x0=22, y0=84, x1=78, y1=100, line_color="white"))
    # Área Pequeña
    lines.append(dict(type="rect", x0=38, y0=94, x1=62, y1=100, line_color="white"))
    # Semicírculo del área (arco)
    fig.add_shape(type="path", path="M 35,84 Q 50,70 65,84", line_color="white")
    # Círculo central (medio círculo)
    fig.add_shape(type="path", path="M 35,50 A 15,15 0 0 1 65,50", line_color="white")

    fig.update_shapes(dict(xref='x', yref='y'))
    for line in lines:
        fig.add_shape(line)

    fig.update_traces(
        marker=dict(size=20, color='#fb8c00', line=dict(width=2, color='white')), 
        textposition='bottom center',
        textfont=dict(family="Arial Black", size=11, color="white")
    )
    return fig

# --- FUNCIÓN PARA GENERAR EL PDF ---
def generar_pdf(avg, atk, dfn, notas):
    pdf = FPDF()
    pdf.add_page()
    
    # Título del Informe
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "RESUMEN DE RENDIMIENTO TACTICO", ln=True, align='C')
    pdf.ln(10)

    # 1. BLOQUE DE MÉTRICAS
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "1. Metricas Colectivas del Once:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 8, f"-> Rating Global del Equipo: {avg:.1f}", ln=True)
    pdf.cell(200, 8, f"-> Potencial Ofensivo: {atk:.1f}", ln=True)
    pdf.cell(200, 8, f"-> Solidez Defensiva: {dfn:.1f}", ln=True)
    pdf.ln(10)

    # 2. BLOQUE DE NOTAS
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "2. Justificacion y Estrategia:", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Limpiamos el texto
    notas_limpias = notas.encode('latin-1', 'replace').decode('latin-1') if notas else "Sin anotaciones."
    pdf.multi_cell(0, 8, notas_limpias)

    # IMPORTANTE: Retornamos los bytes directamente
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFAZ STREAMLIT ---
tab1, tab2, tab3 = st.tabs(["Individual", "Comparador 1vs1", "Tu Alineación"])

# --- TAB 1 y 2 (Se mantienen igual) ---
with tab1:
    st.header("Análisis por Posición")
    pos_selected = st.selectbox("Selecciona una posición", list(METRICAS_MAP.keys()))
    filtered_df = df[df["Pos"] == pos_selected].sort_values("Rating", ascending=False).copy()
    nombres_reales = METRICAS_MAP[pos_selected]
    mapeo_columnas = {"M1": nombres_reales[0], "M2": nombres_reales[1], "M3": nombres_reales[2], "M4": nombres_reales[3]}
    col1, col2 = st.columns([1.5, 2])
    with col1:
        st.dataframe(filtered_df[["Nombre", "Rating", "M1", "M2", "M3", "M4"]].rename(columns=mapeo_columnas), hide_index=True)
    with col2:
        st.plotly_chart(px.bar(filtered_df, x="Nombre", y="Rating", color="Rating", color_continuous_scale="Greens"), use_container_width=True)

with tab2:
    st.header("Cara a Cara (Análisis Comparativo)")
    
    # 1. Filtro de posición para que la comparación sea justa
    pos_comp = st.selectbox("Selecciona posición para comparar", list(METRICAS_MAP.keys()), key="comp_pos_tab2")
    
    # 2. Filtrar jugadores por esa posición
    opciones_comparar = df[df["Pos"] == pos_comp]["Nombre"].unique()
    
    if len(opciones_comparar) >= 2:
        c1, c2 = st.columns(2)
        p1 = c1.selectbox("Jugador A", opciones_comparar, index=0)
        p2 = c2.selectbox("Jugador B", opciones_comparar, index=1)

        # Extraer datos de los jugadores seleccionados
        p1_data = df[df["Nombre"] == p1].iloc[0]
        p2_data = df[df["Nombre"] == p2].iloc[0]
        labels = METRICAS_MAP[pos_comp]

        # --- GRÁFICO DE RADAR ---
        fig_radar = go.Figure()

        # Jugador A
        fig_radar.add_trace(go.Scatterpolar(
            r=[p1_data['M1'], p1_data['M2'], p1_data['M3'], p1_data['M4']],
            theta=labels,
            fill='toself',
            name=p1,
            line_color="#00FF00"
        ))

        # Jugador B
        fig_radar.add_trace(go.Scatterpolar(
            r=[p2_data['M1'], p2_data['M2'], p2_data['M3'], p2_data['M4']],
            theta=labels,
            fill='toself',
            name=p2,
            line_color="#FF4B4B"
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12, color="white"))
            ),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=450
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        # --- TABLA COMPARATIVA RÁPIDA ---
        st.subheader("Diferencia de Atributos")
        comparativa = pd.DataFrame({
            "Métrica": labels,
            p1: [p1_data['M1'], p1_data['M2'], p1_data['M3'], p1_data['M4']],
            p2: [p2_data['M1'], p2_data['M2'], p2_data['M3'], p2_data['M4']]
        })
        st.table(comparativa)

    else:
        st.warning(f"No hay suficientes jugadores en la posición '{pos_comp}' para realizar una comparación.")

# --- TAB 3: PLANTILLA (NUEVA LÓGICA DE SELECCIÓN POR ZONA) ---
with tab3:
    st.header("📍 Configuración del Once")
    c_sel, c_map = st.columns([1, 2])
    
    with c_sel:
        # Reparto de selectores para 11 jugadores
        col_a, col_b = st.columns(2)
        li = col_a.selectbox("LAT Izquierdo", df[df["Pos"] == "Lateral"]["Nombre"])
        ld = col_b.selectbox("LAT Derecho", df[df["Pos"] == "Lateral"]["Nombre"])
        
        col_c, col_d = st.columns(2)
        dfc1 = col_c.selectbox("Central 1", df[df["Pos"] == "Defensa Central"]["Nombre"])
        dfc2 = col_d.selectbox("Central 2", df[df["Pos"] == "Defensa Central"]["Nombre"])
        
        mcd = st.selectbox("Mediocentro Def.", df[df["Pos"] == "Mediocentro"]["Nombre"])
        col_e, col_f = st.columns(2)
        mc1 = col_e.selectbox("Interior 1", df[df["Pos"] == "Mediocentro"]["Nombre"])
        mc2 = col_f.selectbox("Interior 2", df[df["Pos"] == "Mediocentro"]["Nombre"])
        
        col_g, col_h = st.columns(2)
        ei = col_g.selectbox("Extremo Izq.", df[df["Pos"] == "Extremo"]["Nombre"])
        ed = col_h.selectbox("Extremo Der.", df[df["Pos"] == "Extremo"]["Nombre"])
        dc = st.selectbox("Delantero Centro", df[df["Pos"] == "Delantero"]["Nombre"])
        
        s_por = st.selectbox("Portero", df[df["Pos"] == "Portero"]["Nombre"])
        
        seleccionados = [li, ld, dfc1, dfc2, mcd, mc1, mc2, ei, ed, dc, s_por]
        df_equipo = df[df["Nombre"].isin(seleccionados)]

    with c_map:
        # Coordenadas ajustadas para que quepan todos sin pisar las líneas
        coords = {
            s_por: [50, 8],    # Subimos un poco al portero para que entre en el margen
            li: [10, 60], ld: [90, 60], 
            dfc1: [35, 58], dfc2: [65, 58],
            mcd: [50, 68], mc1: [30, 78], mc2: [70, 78],
            ei: [15, 88], ed: [85, 88], 
            dc: [50, 90]       # Bajamos al DC para que no esté dentro de la red
        }
        
        df_mapa = df_equipo.copy()
        df_mapa['x_tactic'] = df_mapa['Nombre'].map(lambda n: coords.get(n, [50,50])[0])
        df_mapa['y_tactic'] = df_mapa['Nombre'].map(lambda n: coords.get(n, [50,50])[1])
        
        st.plotly_chart(draw_half_pitch(df_mapa), use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Análisis de Rendimiento Colectivo")
    
    m1, m2, m3 = st.columns(3)
    avg_total = df_equipo["Rating"].mean()
    ataque = df_equipo[df_equipo["Pos"].isin(["Delantero", "Extremo"])]["Rating"].mean()
    defensa = df_equipo[df_equipo["Pos"].isin(["Defensa Central", "Lateral", "Portero"])]["Rating"].mean()

    m1.metric("Rating Global", f"{avg_total:.1f}")
    m2.metric("Potencial Ofensivo", f"{ataque:.1f}" if not np.isnan(ataque) else "N/A")
    m3.metric("Solidez Defensiva", f"{defensa:.1f}" if not np.isnan(defensa) else "N/A")

    st.markdown("---")
    st.subheader("🧠 Justificación")

    # Inicializamos el estado del texto si no existe
    if 'notas_tacticas' not in st.session_state:
        st.session_state.notas_tacticas = ""

    # Área de texto vinculada al estado de sesión
    texto_usuario = st.text_area(
        "Explica el porqué de tu alineación (roles, estrategia, etc.):",
        value=st.session_state.notas_tacticas,
        placeholder="Ej: He elegido a Haaland por su capacidad de remate frente a defensas cerradas...",
        height=150
    )

    col_btn1, col_btn2 = st.columns([1, 5])
    
    if col_btn1.button("💾 Guardar Notas"):
        st.session_state.notas_tacticas = texto_usuario
        st.success("¡Justificación guardada correctamente!")
    
    if col_btn2.button("🗑️ Borrar"):
        st.session_state.notas_tacticas = ""
        st.rerun() # Recarga para limpiar el área de texto

    # Mostrar lo guardado debajo (opcional)
    if st.session_state.notas_tacticas:
        with st.expander("Ver justificación actual"):
            st.write(st.session_state.notas_tacticas)
    
    # Preparamos el archivo
    st.markdown("---")
    st.subheader("📤 Exportar Informe")

    # Usamos un contenedor para que el botón de descarga aparezca solo al preparar
    if st.button("📝 Generar PDF ahora"):
        try:
            pdf_output = generar_pdf(
                avg_total, 
                ataque, 
                defensa, 
                st.session_state.notas_tacticas
            )

            st.success("✅ PDF generado con éxito. Haz clic abajo para guardarlo.")
            
            st.download_button(
                label="💾 Guardar archivo PDF",
                data=pdf_output,
                file_name="resumen_tactico.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")