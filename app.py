import random
from PIL import Image
import streamlit as st

# 1. Configuración de página con layout ancho
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="wide"
)

# Encabezado principal
st.title("🎭 Análisis de Sentimiento y Emociones")

# Imagen superior
try:
    image = Image.open("emoticones.jpg")
    st.image(image, width=280)
except FileNotFoundError:
    pass

st.markdown("---")

# Banco de frases
FRASES_TRISTES = [
    "Ánimo, los días difíciles son solo capítulos, no toda la historia. 🌈",
    "Está bien no estar bien todo el tiempo. Tómate un respiro y sigue adelante. 💛",
    "Mañana será un día más brillante. ¡Confía en el proceso! ✨",
    "Cada tormenta se queda sin lluvia eventualmente. ¡Tú puedes con esto! 💪",
]

FRASES_FELICES = [
    "¡Qué gran energía! Sigue contagiando esa alegría al mundo. 🌟",
    "¡Me alegra mucho leer eso! Disfruta al máximo este gran momento. 🎉",
    "¡Espléndido! La felicidad te sienta muy bien. 😊",
    "¡Mantén esa sonrisa y esa buena vibración todo el día! 🚀",
]

FRASES_NEUTRALES = [
    "Un estado de calma y equilibrio siempre es un buen punto de partida. 🧘",
    "Todo en orden. ¡Que tengas un día sereno y productivo! ☕",
    "La tranquilidad de hoy es la base para un gran día mañana. 🍃",
]

# Barra lateral informativa
with st.sidebar:
    st.markdown("### Información General")
    st.write("""
    **Polaridad:**
    Indica si el sentimiento es positivo, negativo o neutral (-1 a 1).
    
    **Subjetividad:**
    Mide cuánto del texto representa una opinión sobre un hecho real (0 a 1).
    """)

# Layout en 2 columnas paralelas
col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.markdown("### Selecciona cómo te sientes hoy:")
    
    # Tres botones independientes
    btn_feliz = st.button("😄 Estoy muy feliz", use_container_width=True)
    btn_triste = st.button("😔 Estoy triste", use_container_width=True)
    btn_neutral = st.button("😐 Estoy neutral", use_container_width=True)

with col_der:
    st.markdown("### Resultado del Análisis:")

    # Evaluación según el botón presionado
    if btn_feliz:
        polarity = 0.85
        subjectivity = 0.90
        
        m1, m2 = st.columns(2)
        m1.metric("Polaridad", f"{polarity}")
        m2.metric("Subjetividad", f"{subjectivity}")
        st.write("")
        
        emoji_izq, emoji_der = "😄✨", "🎉😄"
        st.success(f"## {emoji_izq} Sentimiento: Positivo / Feliz {emoji_der}")
        st.success(f"{emoji_izq} **Mensaje de refuerzo:** {random.choice(FRASES_FELICES)} {emoji_der}")
        st.balloons()

    elif btn_triste:
        polarity = -0.75
        subjectivity = 0.85
        
        m1, m2 = st.columns(2)
        m1.metric("Polaridad", f"{polarity}")
        m2.metric("Subjetividad", f"{subjectivity}")
        st.write("")
        
        emoji_izq, emoji_der = "😔💧", "🌧️😔"
        st.error(f"## {emoji_izq} Sentimiento: Negativo / Triste {emoji_der}")
        st.error(f"{emoji_izq} **Mensaje motivacional:** {random.choice(FRASES_TRISTES)} {emoji_der}")

    elif btn_neutral:
        polarity = 0.00
        subjectivity = 0.10
        
        m1, m2 = st.columns(2)
        m1.metric("Polaridad", f"{polarity}")
        m2.metric("Subjetividad", f"{subjectivity}")
        st.write("")
        
        emoji_izq, emoji_der = "😐🍃", "☕😐"
        st.info(f"## {emoji_izq} Sentimiento: Neutral {emoji_der}")
        st.info(f"{emoji_izq} **Mensaje de reflexión:** {random.choice(FRASES_NEUTRALES)} {emoji_der}")

    else:
        st.write("⬅️ *Haz clic en alguno de los 3 botones de la izquierda para ver el resultado.*")
