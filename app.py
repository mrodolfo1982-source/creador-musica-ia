import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página
st.set_page_config(page_title="Music Generator Pro", page_icon="🎵")

# --- MANEJO DE API KEY SEGURA ---
# En local busca en st.secrets, en la web también.
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Introduce tu Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    st.title("🎵 Generador de Música Online")
    st.markdown("Escribe un texto y transfórmalo en un concepto musical.")

    # Selección de Género
    genero = st.selectbox("Elige el estilo musical:", 
                          ["Reggae (Estilo Bob Marley)", "Vallenato", "Rock en Español", "Lo-fi Beats", "Salsa"])

    # Entrada de texto (Chat-style)
    texto_input = st.text_area("Pega el texto para tu canción:", placeholder="Escribe aquí...")

    if st.button("Generar Propuesta Musical"):
        if texto_input:
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt_config = f"""
            Eres un productor musical de alto nivel. Toma este texto: '{texto_input}' 
            y conviértelo en una estructura de canción de {genero}.
            Incluye: Ritmo (BPM), instrumentos clave y cómo debe sonar la voz.
            """
            
            with st.spinner("Componiendo..."):
                response = model.generate_content(prompt_config)
                st.subheader(f"🎼 Resultado: {genero}")
                st.write(response.text)
        else:
            st.warning("Escribe algo primero.")
else:
    st.info("Por favor, configura la API Key en los secretos de Streamlit o escríbela en la barra lateral.")
