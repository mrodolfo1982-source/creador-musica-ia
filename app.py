import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Compositor Musical IA", page_icon="🎵")
st.title("🎵 Generador de Composiciones Musicales")

# 2. Configuración de la API Key (Desde Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Entrada de datos
texto_usuario = st.text_area("Ingresa el texto o pasaje:", height=150)
genero = st.selectbox("Estilo musical:", ["Reggae", "Gospel", "Balada", "Jazz", "Orquestal"])

# 4. Generación
if st.button("Generar"):
    if texto_usuario:
        with st.spinner("Procesando..."):
            try:
                # Usamos el modelo más estable
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Escribe la letra y describe la instrumentación para una canción de estilo {genero} basada en: {texto_usuario}"
                
                response = model.generate_content(prompt)
                
                st.success("¡Listo!")
                st.markdown("### Resultado:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Escribe algo para continuar.")
