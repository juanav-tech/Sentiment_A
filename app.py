import random
from googletrans import Translator
import pandas as pd
from PIL import Image
import streamlit as st
from textblob import TextBlob

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)

# Estilos CSS personalizados para mejorar la interfaz y colores
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        border-radius: 12px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎭 Análisis de Sentimiento")

# Manejo de la imagen principal con manejo de excepción por si no existe localmente
try:
    image = Image.open("emoticones.jpg")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

st.subheader("¿Cómo te sientes hoy? Escribe una frase para analizarla:")

translator = Translator()

# Banco de frases de respuesta
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
    "La neutralidad trae paz mental. Disfruta la tranquilidad. 🍃",
]

with st.sidebar:
    st.header("📊 Métricas")
    st.markdown("""
    **Polaridad:**
    Indica si el sentimiento es positivo, negativo o neutral.
    * Range: **-1.0** (muy negativo) a **1.0** (muy positivo).
    
    **Subjetividad:**
    Mide cuánto del texto es una opinión frente a un hecho real.
    * Range: **0.0** (objetivo) a **1.0** (subjetivo).
    """)

# Interfaz principal de entrada
text = st.text_area(
    "Escribe tu frase o pensamiento aquí:",
    placeholder="Ej: Hoy ha sido un día increíble...",
)

if text:
    try:
        # Traducción y procesamiento de sentimiento
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.divider()

        # Mostrar métricas en columnas visuales
        col1, col2 = st.columns(2)
        col1.metric("Polaridad", f"{polarity}")
        col2.metric("Subjetividad", f"{subjectivity}")

        st.write("---")

        # Lógica condicional de respuestas, colores e íconos dinámicos
        if polarity < -0.05:
            # Estado Triste / Negativo
            st.error("### Estado detectado: Triste / Negativo 😔")
            st.markdown(f"### 💡 **Mensaje para ti:**")
            st.info(random.choice(FRASES_TRISTES))

        elif polarity > 0.05:
            # Estado Feliz / Positivo
            st.success("### Estado detectado: ¡Feliz / Positivo! 😄")
            st.markdown(f"### 🌟 **Mensaje para ti:**")
            st.balloon()  # Animación de globos para reforzar la alegría
            st.success(random.choice(FRASES_FELICES))

        else:
            # Estado Neutral
            st.warning("### Estado detectado: Neutral 😐")
            st.markdown(f"### 🍃 **Mensaje para ti:**")
            st.info(random.choice(FRASES_NEUTRALES))

    except Exception as e:
        st.error(
            "Ocurrió un problema al traducir el texto. Por favor, intenta de nuevo."
        )
