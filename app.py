import random
from googletrans import Translator
from PIL import Image
import streamlit as st
from textblob import TextBlob

# 1. Configuración de página con layout ancho
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="wide"
)

# Inicializar Traductor
translator = Translator()

# Encabezado principal
st.title("🎭 <u>Análisis de Sentimiento y Emociones</u>")

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
    st.markdown("### <u>Información General</u>")
    st.write("""
    **Polaridad:**
    Indica si el sentimiento es positivo, negativo o neutral (-1 a 1).
    
    **Subjetividad:**
    Mide cuánto del texto representa una opinión sobre un hecho real (0 a 1).
    """)

# NUEVO LAYOUT: Organización en 2 columnas paralelas
col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.markdown("### <u>Ingresa tu mensaje:</u>")
    text = st.text_area(
        "Escribe la frase que deseas evaluar:",
        placeholder="Ej: Hoy ha sido un día triste...",
        height=130,
    )
    analizar_btn = st.button("🔍 Analizar Sentimiento", use_container_width=True)

with col_der:
    st.markdown("### <u>Resultado del Análisis:</u>")

    if analizar_btn and text:
        # Detección explicita de palabras clave en español
        palabras_tristes = [
            "triste",
            "mal",
            "deprimido",
            "llorar",
            "horrible",
            "fatal",
            "solo",
            "dolor",
            "desanimado",
        ]
        palabras_felices = [
            "feliz",
            "bien",
            "contento",
            "alegre",
            "excelente",
            "genial",
            "fantastico",
            "maravilloso",
        ]

        try:
            translation = translator.translate(text, src="es", dest="en")
            trans_text = translation.text
        except Exception:
            trans_text = text

        blob = TextBlob(trans_text)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # Ajuste directo para palabras clave en español
        texto_lower = text.lower()
        if any(p in texto_lower for p in palabras_tristes) and polarity >= 0:
            polarity = -0.50
        elif any(p in texto_lower for p in palabras_felices) and polarity <= 0:
            polarity = 0.50

        # Muestreo de métricas numéricas
        m1, m2 = st.columns(2)
        m1.metric("Polaridad", f"{polarity}")
        m2.metric("Subjetividad", f"{subjectivity}")

        st.write("")

        # Lógica con EMOJIS A AMBOS LADOS y TEXTO SUBRAYADO
        if polarity < 0:
            emoji_izq, emoji_der = "😔💧", "🌧️😔"
            st.error(
                f"## {emoji_izq} <u>Sentimiento: Negativo / Triste</u> {emoji_der}"
            )
            st.error(
                f"{emoji_izq} **<u>Mensaje motivacional:</u>** {random.choice(FRASES_TRISTES)} {emoji_der}"
            )

        elif polarity > 0:
            emoji_izq, emoji_der = "😄✨", "🎉😄"
            st.success(
                f"## {emoji_izq} <u>Sentimiento: Positivo / Feliz</u> {emoji_der}"
            )
            st.success(
                f"{emoji_izq} **<u>Mensaje de refuerzo:</u>** {random.choice(FRASES_FELICES)} {emoji_der}"
            )
            st.balloons()

        else:
            emoji_izq, emoji_der = "😐🍃", "☕😐"
            st.info(f"## {emoji_izq} <u>Sentimiento: Neutral</u> {emoji_der}")
            st.info(
                f"{emoji_izq} **<u>Mensaje de reflexión:</u>** {random.choice(FRASES_NEUTRALES)} {emoji_der}"
            )

    elif analizar_btn and not text:
        st.warning(
            "⚠️ <u>Por favor escribe una frase en el panel izquierdo antes de analizar.</u>"
        )
    else:
        st.write(
            "⬅️ *Ingresa un texto a la izquierda y presiona el botón para ver los resultados aquí.*"
        )
