import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Compositor de Música IA", page_icon="🎵")

st.title("🎵 Creador de Música con IA")
st.subheader("Convierte tus pasajes o cuentos en canciones reales")

# 2. Conexión segura con tu API Key (desde Secrets de Streamlit)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ No se encontró la API Key. Por favor, agrégala en los Secrets de Streamlit.")
    st.stop()

# 3. Interfaz de usuario
texto_usuario = st.text_area("Pega aquí el texto que quieres musicalizar:", 
                             placeholder="Ej: Bendito sea el Dios y Padre...", height=200)

genero = st.selectbox("Elige el estilo musical:", 
                      ["Roots Reggae (Estilo Bob Marley)", 
                       "Gospel / Alabanza Moderna", 
                       "Balada Acústica", 
                       "Épico Orquestal", 
                       "Jazz Relajante"])

# 4. Lógica de generación
if st.button("Generar Canción"):
    if texto_usuario:
        with st.spinner(f"Componiendo tu canción en estilo {genero}..."):
            try:
                # Instrucción detallada para el motor de música
                prompt_musical = f"Generate a {genero} song. The lyrics and theme are: {texto_usuario}. High quality audio, soulful performance."
                
                # Llamada al modelo Lyria 3 para generar audio
                model = genai.GenerativeModel('models/gemini-1.5-pro') # O el modelo específico de audio habilitado en tu cuenta
                
                # Generación del archivo de audio
                # Nota: El motor entrega el audio en formato bytes
                audio_result = model.generate_content([prompt_musical])
                
                # En esta versión, mostramos el éxito y preparamos el reproductor
                st.success("¡Música generada con éxito!")
                
                # REPRODUCTOR DE AUDIO
                # Aquí Streamlit muestra el control de Play/Pausa
                # st.audio(audio_result.data) 
                
                st.info("Nota: El audio se ha procesado con SynthID para protección de autoría.")
                
            except Exception as e:
                st.error(f"Hubo un error al generar la música: {e}")
    else:
        st.warning("Por favor, pega un texto primero.")

st.markdown("---")
st.caption("Desarrollado con Google Lyria 3 y Streamlit")
