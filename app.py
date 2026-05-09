import streamlit as st

# Configuración inicial
st.set_page_config(page_title="AI Coach Ping Pong", layout="wide")

# Aplicación de los colores solicitados mediante CSS
st.markdown(f"""
    <style>
    /* Fondo principal */
    .stApp {{
        background-color: #4A4857;
        color: #CACFE3;
    }}
    
    /* Barra lateral */
    [data-testid="stSidebar"] {{
        background-color: #170B47;
    }}
    
    /* Títulos y textos */
    h1, h2, h3, p {{
        color: #CACFE3 !important;
    }}

    /* Botones personalizados */
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #170B47;
        color: #CACFE3;
        border: 2px solid #CACFE3;
        font-weight: bold;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #CACFE3;
        color: #170B47;
        border: 2px solid #170B47;
    }}

    /* Contenedores de video y resultados */
    .video-container {{
        border: 2px solid #CACFE3;
        border-radius: 15px;
        padding: 10px;
        background-color: #170B47;
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.title("🏓 AI Coach: Análisis de Saque")
st.write("Prototipo de interfaz para el Hackaton Roboborregos 2026")

# --- LAYOUT PRINCIPAL ---
col_izq, col_der = st.columns([1.2, 0.8], gap="large")

with col_izq:
    st.subheader("Visualización del Análisis")
    # Contenedor simulado para el video vertical
    st.markdown("""
        <div class="video-container">
            <p style='text-align: center; color: #CACFE3;'>
                Área del Video Analizado<br>
                (Aquí se mostrará el output de MediaPipe)
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Tracking de muñeca, brazo y tronco activo.")

with col_der:
    st.subheader("Panel de Control")
    
    st.info("Sube un video para habilitar las funciones del Coach.")
    
    # Botones de acción
    btn_analizar = st.button("🔍 Iniciar Análisis de Ángulos")
    
    st.divider()
    
    st.write("### Opciones del Coach")
    btn_mejoras = st.button("📈 Ver Consejos de Mejora")
    
    btn_audio = st.button("🎙️ Activar Audio del Entrenador")

    # Espacio para feedback simulado
    st.markdown("""
        <div style='background-color: #170B47; padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <p style='margin: 0; font-size: 0.9em; color: #CACFE3;'>
                <b>Estado:</b> Esperando entrada...
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/ping-pong.png", width=80)
    st.header("Menú Principal")
    st.file_uploader("Cargar Video (.mp4)", type=["mp4"])
    
    st.divider()
    st.write("**Integrantes:** Oscar Aldana")
    st.write("Dominik Galván")
    st.write("Ronaldo Velez")