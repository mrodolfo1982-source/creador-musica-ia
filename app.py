import streamlit as st
import google.generativeai as genai

# Configuración visual
st.set_page_config(page_title="Generador de Música Lyria", page_icon="🎵")

# Recuperar la llave de los Secretos de Streamlit (Para la web)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Falta la configuración de GOOGLE_API_KEY en Secrets.")
    st.stop()

st.title("🎵 Generador de Música Real (Free)")
st.markdown("Utilizando tecnología de **Google Lyria 3**.")

# Opciones de estilo
estilo = st.selectbox("Selecciona un estilo musical:", 
                      ["Reggae (Voz estilo Bob Marley)", "Vallenato", "Salsa", "Rock", "Lo-fi"])

# El "Chat" donde pegas tu texto
mensaje = st.text_area("Pega el texto que quieres convertir en canción:", 
                       height=150, 
                       placeholder="Ej: Para ser adoptados hijos suyos por medio de Jesucristo...")

if st.button("Generar Audio"):
    if mensaje:
        try:
            # Seleccionamos el modelo de música que aparece en tu panel
            model = genai.GenerativeModel('lyria-3')
            
            # Configuramos el prompt para que sea específico al estilo
            prompt_final = f"Generate a high-fidelity 30-second music track in {estilo} style. Use the following lyrics/theme: {mensaje}"
            
            with st.spinner("Compitiendo... esto puede tardar unos segundos"):
                # Llamada a la API de generación de música
                result = model.generate_content(prompt_final)
                
                # El modelo Lyria devuelve un objeto que incluye el audio
                # Streamlit lo reproduce automáticamente
                st.subheader("🎼 Tu resultado:")
                st.audio(result.audio_data, format="audio/wav")
                st.success("¡Música generada exitosamente!")
                
        except Exception as e:
            st.error(f"Error al generar: {e}")
            st.info("Nota: Si recibes un error de 'Model Not Found', es posible que debas usar 'gemini-3-flash' para la lógica y esperar la integración completa del audio.")
    else:
        st.warning("Escribe algo primero para poder generar la música.")
