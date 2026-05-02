import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Generador de Música Gemini 3", page_icon="🎵")

# Recuperar la llave de los Secretos de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Configura GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.title("🎵 Generador de Música Gemini 3")

estilo = st.selectbox("Selecciona un estilo:", 
                      ["Reggae", "Vallenato", "Salsa", "Rock Alternativo", "Gospel", "Lo-fi"])

mensaje = st.text_area("Texto para la canción:")

if st.button("Generar Audio"):
    if mensaje:
        try:
            # Usamos Gemini 3 Flash, que es el modelo central en tu tier gratuito
            model = genai.GenerativeModel('gemini-3-flash')
            
            # El prompt debe ser explícito para que el modelo active su herramienta de audio
            prompt_final = f"Generate a 30-second music track. Style: {estilo}. Theme: {mensaje}. Return the audio file."
            
            with st.spinner("Generando música con Gemini 3..."):
                # En Gemini 3, la generación de audio se maneja a través de generate_content
                response = model.generate_content(prompt_final)
                
                # Buscamos el componente de audio en la respuesta
                if response.candidates[0].content.parts:
                    # Intentamos extraer los datos binarios del audio
                    st.subheader("🎼 Resultado:")
                    # Nota: Streamlit necesita los bytes directamente
                    st.audio(response.candidates[0].content.parts[0].inline_data.data, format="audio/wav")
                    st.success("¡Generado con éxito!")
                else:
                    st.error("El modelo no devolvió un archivo de audio. Intenta simplificar el texto.")
                
        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe algo primero.")
