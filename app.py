import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configuración de la página
st.set_page_config(page_title="Music Gen AI", page_icon="🎵")

# Cargar API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## --- INTERFAZ DE USUARIO ---
st.title("🎵 Generador de Conceptos Musicales")
st.markdown("Crea estructuras y sugerencias de composición usando IA.")

with st.sidebar:
    st.header("Configuración")
    model_choice = st.selectbox("Modelo", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temperature = st.slider("Creatividad", 0.0, 1.0, 0.7)

prompt_usuario = st.text_area(
    "Describe la música que tienes en mente:",
    placeholder="Ej: Un beat de Lo-fi melancólico con trompetas de jazz y un ritmo de 90 BPM..."
)

if st.button("Generar Estructura Musical"):
    if prompt_usuario:
        try:
            model = genai.GenerativeModel(model_choice)
            
            # Prompt optimizado para composición
            full_prompt = f"""
            Actúa como un productor musical experto. Basado en la siguiente descripción: '{prompt_usuario}', 
            proporciona:
            1. Progresión de acordes sugerida.
            2. Instrumentación recomendada.
            3. Estructura de la canción (Intro, Verso, Coro).
            4. Sugerencia de BPM y escala musical.
            """
            
            with st.spinner("Componiendo..."):
                response = model.generate_content(full_prompt)
                
            st.subheader("🎼 Propuesta Musical")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Hubo un error: {e}")
    else:
        st.warning("Por favor, escribe una descripción.")
