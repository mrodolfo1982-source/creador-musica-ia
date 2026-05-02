import streamlit as st
import google.generativeai as genai
import numpy as np
from scipy.io.wavfile import write
import io

st.set_page_config(page_title="Music Gen Pro", page_icon="🎵")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configura la API Key en Secrets.")
    st.stop()

st.title("🎵 Generador de Conceptos y Audio")

# Diccionario de referencias (como querías)
opciones = {
    "Reggae (Bob Marley)": "Roots reggae, 75 BPM, deep bass, off-beat guitar.",
    "Salsa (Héctor Lavoe)": "Salsa brava, 90 BPM, bright brass, piano montuno.",
    "Vallenato (Diomedes)": "Traditional vallenato, accordion melody, fast percussion."
}

seleccion = st.selectbox("Elige tu referencia:", list(opciones.keys()))
mensaje = st.text_area("Texto para la canción:")

def generar_audio_base(duracion=5, frecuencia=440):
    # Genera un tono de prueba para asegurar que el reproductor funciona
    sample_rate = 44100
    t = np.linspace(0, duracion, sample_rate * duracion)
    data = np.sin(2 * np.pi * frecuencia * t)
    scaled = np.int16(data * 32767)
    byte_io = io.BytesIO()
    write(byte_io, sample_rate, scaled)
    return byte_io.getvalue()

if st.button("Generar"):
    if mensaje:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Pedimos la letra y estructura
            prompt = f"Escribe la letra de una canción corta de {seleccion} basada en: {mensaje}. Incluye acordes."
            
            with st.spinner("Componiendo..."):
                res = model.generate_content(prompt)
                st.subheader("📝 Composición")
                st.write(res.text)
                
                # Generamos el archivo de audio
                audio_bytes = generar_audio_base()
                st.subheader("🔊 Previsualización de Ritmo")
                st.audio(audio_bytes, format="audio/wav")
                st.info("Nota: Debido a restricciones de región de Google Lyria en Colombia, se genera un tono base. La composición completa está arriba.")
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Escribe algo primero.")
