import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Music Generator Free", page_icon="🎵")

# Solo necesitas tu Google API Key en los Secrets de Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    st.title("🎵 Generador de Música 100% Google (Free)")
    
    genero = st.selectbox("Estilo musical:", 
                          ["Reggae", "Salsa", "Rock", "Lo-fi", "Pop"])
    
    texto_input = st.text_area("Texto para convertir en música:")

    if st.button("Generar Audio Real"):
        if texto_input:
            # Usamos el modelo Lyria 3 que permite salida de AUDIO directamente
            model = genai.GenerativeModel('lyria-3-pro-preview')
            
            prompt_completo = f"Create a 30-second {genero} track. Vocal style should be expressive. Lyrics: {texto_input}"
            
            with st.spinner("Google Lyria está componiendo tu música..."):
                try:
                    # Configuramos la respuesta para que devuelva AUDIO y TEXTO
                    response = model.generate_content(
                        prompt_completo,
                        config=genai.types.GenerateContentConfig(
                            response_modalities=["AUDIO", "TEXT"],
                            response_mime_type="audio/wav"
                        )
                    )
                    
                    # El audio viene dentro de los 'parts' de la respuesta
                    audio_part = next(p for p in response.candidates[0].content.parts if p.inline_data)
                    
                    st.subheader("🎼 Tu música está lista")
                    st.audio(audio_part.inline_data.data, format="audio/wav")
                    st.success("Generado con éxito usando Lyria 3")
                    
                except Exception as e:
                    st.error(f"Error: {e}. Asegúrate de que tu API Key tenga habilitado Lyria 3.")
        else:
            st.warning("Escribe algo para empezar.")
else:
    st.warning("Por favor, configura GOOGLE_API_KEY en los Secrets de Streamlit.")
