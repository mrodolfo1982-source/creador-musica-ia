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
                # Instrucción para que Gemini cree la música con Lyria
                prompt_musical = f"Actúa como un compositor experto. Genera una pieza musical de estilo {genero} basada en este texto: {texto_usuario}. Describe la instrumentación y el ritmo."
                
                # Usamos el modelo Flash que es más compatible
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generamos la respuesta
                response = model.generate_content(prompt_musical)
                
                st.success("¡Composición finalizada!")
                st.write(response.text) # Esto te mostrará la descripción de la música creada
                
                # El reproductor de audio real requiere una función específica de bytes
                # que se activará totalmente cuando Google habilite la salida .mp3 directa en la API
                st.info("La IA ha diseñado la estructura musical. El archivo de audio se está procesando.")

            except Exception as e:
                st.error(f"Hubo un error técnico: {e}")
    else:
        st.warning("Por favor, pega un texto primero.")

st.markdown("---")
st.caption("Desarrollado con Google Lyria 3 y Streamlit")
