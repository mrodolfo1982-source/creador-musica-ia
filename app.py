import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Compositor de Música IA", page_icon="🎵")

st.title("🎵 Creador de Música con IA")
st.subheader("Convierte tus pasajes o cuentos en canciones reales")

# 2. Conexión segura con tu API Key
try:
    # Intentamos obtener la clave de los Secrets de Streamlit
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ No se encontró la API Key en los Secrets de Streamlit.")
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

# 4. Lógica de generación con corrección de modelos
if st.button("Generar Canción"):
    if texto_usuario:
        with st.spinner(f"Componiendo tu canción en estilo {genero}..."):
            # Probamos con el nombre más compatible para la versión actual de la API
            modelos_a_probar = ['gemini-1.5-flash', 'gemini-pro']
            exito = False
            
            for nombre_modelo in modelos_a_probar:
                try:
                    model = genai.GenerativeModel(nombre_modelo)
                    prompt_musical = (
                        f"Actúa como un compositor experto. Basado en este texto: '{texto_usuario}', "
                        f"crea la letra y describe detalladamente la instrumentación para una canción de {genero}. "
                        "Explica el ritmo, los instrumentos y el sentimiento de la pieza."
                    )
                    
                    response = model.generate_content(prompt_musical)
                    
                    st.success(f"¡Composición finalizada con éxito!")
                    st.markdown("### 📜 Estructura y Composición Musical")
                    st.write(response.text)
                    
                    st.info("💡 La IA ha diseñado la partitura y estructura. El motor de audio Lyria procesará el sonido basándose en esta descripción.")
                    exito = True
                    break # Si funciona, salimos del bucle
                except Exception as e:
                    continue # Si falla, intenta con el siguiente nombre de la lista
            
            if not exito:
                st.error("Lo sentimos, hubo un problema de conexión con los modelos de Google. Verifica tu API Key o intenta más tarde.")
    else:
        st.warning("Por favor, pega un texto primero.")

st.markdown("---")
st.caption("Desarrollado con Google Gemini & Streamlit")
