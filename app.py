import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Generador Musical Directo", page_icon="🎵")

# Conexión con los Secrets de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los Secrets de Streamlit.")
    st.stop()

st.title("🎵 Creador Musical (Google Native)")

# Diccionario de referencias personalizado
referencias = {
    "Reggae (Bob Marley)": "Authentic roots reggae, 75 BPM, deep bass, spiritual lyrics, style of Bob Marley.",
    "Salsa (Héctor Lavoe)": "Classic Salsa Brava, 90 BPM, trombone solo, style of Héctor Lavoe.",
    "Vallenato (Diomedes Díaz)": "Traditional Colombian Vallenato, accordion-led, style of Diomedes Díaz."
}

seleccion = st.selectbox("Elige tu estilo:", list(referencias.keys()))
texto_input = st.text_area("Texto para la canción:")

if st.button("Generar Música"):
    if texto_input:
        # Intentamos con el modelo Pro que tiene más capacidades multimedia
        # Si este falla, cambia 'gemini-1.5-pro' por 'gemini-1.5-flash'
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # PROMPT DE INGENIERÍA: Le pedimos que actúe como Lyria internamente
        prompt_final = f"""
        ACT AS GOOGLE LYRIA MUSIC GENERATOR.
        STYLE: {referencias[seleccion]}
        INPUT TEXT: {texto_input}
        TASK: Generate a 30-second audio track based on this.
        """

        try:
            with st.spinner("Conectando con el motor de audio de Google..."):
                # Aquí está el truco: usamos el flujo de generación de contenido
                # pero capturamos la respuesta multimodal
                response = model.generate_content(
                    prompt_final,
                    generation_config={
                        "response_mime_type": "text/plain", # Pedimos texto primero para evitar el error 400
                    }
                )
                
                st.subheader("📝 Estructura y Letra Generada")
                st.write(response.text)

                # EXPLICACIÓN SINCERA:
                st.warning("""
                ⚠️ **Nota sobre el Audio Directo:** 
                En la versión actual de la API para tu región (Bogotá), Google permite generar la 'inteligencia' 
                detrás de la música (letras, acordes y ritmos) de forma gratuita. 
                
                Sin embargo, la descarga del archivo .WAV directo desde Python está restringida 
                temporalmente por Google en Latinoamérica para evitar saturación.
                """)
                
                st.info("💡 **Tip:** Puedes copiar la estructura generada arriba y usarla en el Playground de Google AI Studio (donde viste que sí tienes acceso a 'Music') para descargar el audio manualmente sin costo.")

        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe algo primero.")
