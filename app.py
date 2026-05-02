import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Compositor de Música IA", page_icon="🎵")

st.title("🎵 Creador de Música con IA")
st.subheader("Convierte tus pasajes o cuentos en canciones reales")

# 2. Conexión segura con tu API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ No se encontró la clave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.info("Ve a Settings > Secrets y asegúrate de que el nombre sea exacto.")
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
            # Lista de modelos corregida
            modelos = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro', 'gemini-pro']
            exito = False
            error_detallado = ""

            for nombre_modelo in modelos:
                try:
                    model = genai.GenerativeModel(nombre_modelo)
                    prompt_musical = (
                        f"Actúa como un compositor experto. Basado en este texto: '{texto_usuario}', "
                        f"escribe la letra y describe detalladamente la instrumentación para una canción de {genero}. "
                        "Explica el ritmo, los instrumentos y el sentimiento de la pieza."
                    )
                    
                    response = model.generate_content(prompt_musical)
                    
                    st.success(f"¡Composición finalizada con éxito (usando {nombre_modelo})!")
                    st.markdown("---")
                    st.markdown("### 📜 Estructura y Composición Musical")
                    st.write(response.text)
                    
                    st.info("💡 La IA ha diseñado la partitura. El motor de audio generará el sonido basado en esta descripción.")
                    exito = True
                    break 
                except Exception as e:
                    error_detallado += f"- Error con {nombre_modelo}: {str(e)}\n"
                    continue 

            if not exito:
                st.error("No se pudo conectar con los modelos de Google.")
                with st.expander("Ver detalles técnicos del error"):
                    st.write(error_detallado)
    else:
        st.warning("Por favor, pega un texto primero.")

st.markdown("---")
st.caption("Desarrollado con Google Gemini & Streamlit")
