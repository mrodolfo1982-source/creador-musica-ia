import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Compositor IA", page_icon="🎵")
st.title("🎵 Creador de Música con IA")

# Conexión con la llave
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Interfaz
texto_usuario = st.text_area("Texto para musicalizar:", height=150)
genero = st.selectbox("Estilo:", ["Roots Reggae", "Gospel", "Balada", "Jazz"])

if st.button("Generar Canción"):
    if texto_usuario:
        with st.spinner("Componiendo..."):
            try:
                # Usamos el nombre más estándar y moderno
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Actúa como compositor. Crea la letra y describe la música para un {genero} basado en: {texto_usuario}"
                
                response = model.generate_content(prompt)
                
                st.success("¡Composición lista!")
                st.markdown("### 📜 Resultado")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("Si el error persiste, verifica que tu API Key sea de un proyecto de Google Cloud con Gemini habilitado.")
    else:
        st.warning("Escribe algo primero.")
