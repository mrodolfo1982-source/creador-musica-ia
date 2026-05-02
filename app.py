import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Generador Musical Personalizado", page_icon="🎵")

# Configuración de la API Key desde los Secrets de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Por favor, configura la GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.title("🎵 Generador de Música con Referencias")

# --- AQUÍ PUEDES COLOCAR TUS PROPIAS REFERENCIAS ---
# Puedes añadir más artistas o géneros siguiendo este formato
opciones_musicales = {
    "Reggae (Bob Marley)": "Classic roots reggae with a voice similar to Bob Marley, rhythmic guitar skanks, and a deep bassline.",
    "Vallenato (Diomedes Díaz)": "Traditional Colombian Vallenato with accordion, caja, and guacharaca, style of Diomedes Díaz.",
    "Salsa (Héctor Lavoe)": "Classic 70s Salsa Brava with heavy trombones and the vocal phrasing of Héctor Lavoe.",
    "Rock (Soda Stereo)": "80s Latin Rock/Post-punk style, melodic bass and atmospheric guitars similar to Gustavo Cerati.",
    "Rock (Caramelos de Cianuro)": "90s Latin Rock/Post-punk style, melodic bass and vocal ad-libs in the style of Asier Cazalis.",
    "Pop (Michael Jackson)": "80s Pop with groovy synth-bass, crisp drums, and vocal ad-libs in the style of Michael Jackson."
}

seleccion = st.selectbox("Elige tu estilo y referencia:", list(opciones_musicales.keys()))
referencia_tecnica = opciones_musicales[seleccion]

mensaje = st.text_area("Texto/Letra para la canción:", placeholder="Escribe aquí el mensaje...")

if st.button("Generar Audio"):
    if mensaje:
        try:
            # Usamos el modelo 1.5 Flash que es el más estable para la API por ahora
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Construimos el prompt usando la referencia que elegiste
            prompt_final = f"""
            Generate a 30-second high-quality audio track.
            STYLE REFERENCE: {referencia_tecnica}
            LYRICS/THEME: {mensaje}
            Output only the audio content.
            """
            
            with st.spinner(f"Generando {seleccion}..."):
                # Llamada con soporte para audio
                response = model.generate_content(
                    prompt_final,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="audio/wav"
                    )
                )
                
                # Verificamos si devolvió datos de audio
                if response.candidates[0].content.parts:
                    audio_data = response.candidates[0].content.parts[0].inline_data.data
                    st.subheader(f"🎼 Resultado: {seleccion}")
                    st.audio(audio_data, format="audio/wav")
                    st.success("¡Música generada!")
                else:
                    st.error("El modelo no generó audio. Intenta con un texto más corto.")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Si el error persiste, es probable que Google esté limitando la generación de audio en tu región hoy.")
    else:
        st.warning("Escribe algo primero.")
