import streamlit as st
import time

st.set_page_config(page_title="Compositor de Música IA", page_icon="🎵")

st.title("🎵 Creador de Música con IA")
st.subheader("Convierte tus versículos o cuentos en canciones")

# Cuadro de texto para pegar el pasaje o cuento
texto_usuario = st.text_area("Pega aquí el texto que quieres musicalizar:", 
                             placeholder="Ej: Bendito sea el Dios y Padre...", height=200)

# Selector de género musical
genero = st.selectbox("Elige el estilo musical:", 
                      ["Reggae (Estilo Bob Marley)", "Gospel / Alabanza", "Balada Cristiana", "Épico / Orquestal", "Jazz Relajante"])

if st.button("Generar Canción"):
    if texto_usuario:
        with st.spinner(f"Componiendo tu canción en estilo {genero}..."):
            # Aquí se conectará con el motor Lyria 3
            time.sleep(3) # Simulación de proceso
            st.success("¡Música generada con éxito!")
            
            # Nota: En la versión final, aquí aparecerá el reproductor de audio real
            st.info("Nota: La integración directa con el motor de audio se activará al conectar tu API Key.")
            
            # Espacio para el reproductor
            # st.audio(archivo_generado) 
    else:
        st.warning("Por favor, pega un texto primero.")