import streamlit as st #Fin
import asyncio

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
    
    import base64
    import os
    video_path = "Video.mp4" # O "Final.mp4" si lo regresaste al nombre original
    
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            data = f.read()
            # Convertimos el video a base64 para inyectarlo directo al HTML
            bin_str = base64.b64encode(data).decode()
            
        # Creamos un reproductor HTML5 manual
        html_code = f'''
            <video width="100%" controls autoplay loop muted>
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
                Tu navegador no soporta el video.
            </video>
        '''
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.error("¡Archivo no encontrado!")
        
    st.caption("Video con análisis de ángulos (MediaPipe) activo.")

with col_der:
    st.subheader("Panel de Control")
    
    # Mensaje informativo dinámico
    import os
    audio_path = "analisis.wav"
    
    if not os.path.exists(audio_path):
        st.info("Sube un video y procesa el análisis para escuchar al Coach.")
    else:
        st.success("✅ ¡Análisis de audio listo!")

    # --- SECCIÓN DE ACCIONES ---
    # st.write("### 🛠️ Acciones del Sistema")
    
    # Botón para iniciar el procesamiento de MediaPipe (Lógica de Code.py)
    # if st.button("🔍 Iniciar Análisis de Ángulos", use_container_width=True):
    #     st.write("Procesando frames con MediaPipe...")
    #     # Aquí iría la llamada a tu lógica de detección de pose
    
    st.divider()
    
    # --- SECCIÓN DEL COACH ---
    st.write("### 🇦🇷 Opciones del Coach")
    
    # Botón para ver texto (opcional, si guardas los consejos en un .txt)
    # if st.button("📈 Ver Consejos de Mejora", use_container_width=True):
    #     st.write("Generando reporte de técnica...")

    # Botón de Audio configurado para .wav
    if st.button("🎙️ Activar Audio del Entrenador", type="primary", use_container_width=True):
        if os.path.exists(audio_path):
            try:
                with open(audio_path, 'rb') as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/wav')
                st.balloons() # Efecto visual de éxito para la presentación
            except Exception as e:
                st.error(f"Error al reproducir el archivo: {e}")
        else:
            st.warning(f"No se encontró el archivo '{audio_path}'. Asegúrate de correr primero el script de Gemini.")

    # --- FEEDBACK DE ESTADO (DISEÑO FIME) ---
    estado_texto = "Esperando entrada..."
    estado_color = "#170B47" # Color base oscuro
    
    if os.path.exists(audio_path):
        estado_texto = "Análisis completado. Audio disponible."
        estado_color = "#004010" # Verde oscuro de éxito
    
    st.markdown(f"""
        <div style='background-color: {estado_color}; padding: 15px; border-radius: 10px; margin-top: 25px; border-left: 5px solid #CACFE3;'>
            <p style='margin: 0; font-size: 0.9em; color: #CACFE3; font-family: sans-serif;'>
                <span style='font-weight: bold; color: #FFFFFF;'>ESTADO ACTUAL:</span><br>
                {estado_texto}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("Hackathon Roboborregos 2026")

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/ping-pong.png", width=80)
    st.header("Menú Principal")
    # st.file_uploader("Cargar Video (.mp4)", type=["mp4"])
    
    st.divider()
    st.write("**Integrantes:** Oscar Aldana")
    st.write("Dominik Galván")
    st.write("Ronaldo Velez")