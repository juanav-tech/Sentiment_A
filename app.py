import random
from googletrans import Translator
from PIL import Image
import streamlit as st
from textblob import TextBlob

# 1. Configuración básica de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)

# Inicializar Traductor
translator = Translator()

# Encabezado principal
st.title("🎭 Análisis de Sentimiento")

# Manejo de la imagen sin pixelado (tamaño controlado mediante ancho directo)
try:
    image = Image.open("emoticones.jpg")
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(image, width=300)
except FileNotFoundError:
    pass

st.subheader("Escribe una frase para analizar tu estado de ánimo:")

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
    "La tranquilidad de hoy es la base para un gran día mañana. 🍃",
]

# Barra lateral informativa
with st.sidebar:
    st.subheader("Información General")
    st.write("""
    **Polaridad:**
    Indica si el sentimiento es positivo, negativo o neutral (-1 a 1).
    
    **Subjetividad:**
    Mide cuánto del texto representa una opinión sobre un hecho real (0 a 1).
    """)

# Entrada de texto del usuario
text = st.text_input(
    "Escribe por favor tu frase aquí:", placeholder="Ej: Hoy es un día triste..."
)

# Botón para ejecutar el análisis
analizar_btn = st.button("🔍 Analizar Sentimiento", use_container_width=True)

if analizar_btn and text:
    # Detección directa de palabras clave en español para corregir traducciones cortas
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

    # Ajuste manual para asegurar que palabras directas como "triste" cambien la polaridad
    texto_lower = text.lower()
    if any(p in texto_lower for p in palabras_tristes) and polarity >= 0:
        polarity = -0.50
    elif any(p in texto_lower for p in palabras_felices) and polarity <= 0:
        polarity = 0.50

    st.write("---")

    # Muestreo de métricas numéricas mediante componentes estándar
    col1, col2 = st.columns(2)
    col1.metric("Polaridad", f"{polarity}")
    col2.metric("Subjetividad", f"{subjectivity}")

    st.write("### Resultado del Análisis:")

    # Generación de respuestas utilizando componentes 100% nativos de Streamlit
    if polarity < 0:
        # Estado Negativo / Triste (Cuadro rojo nativo)
        st.error("## 😔 Sentimiento Detectado: Negativo / Triste")
        st.error(f"**Mensaje:** {random.choice(FRASES_TRISTES)}")

    elif polarity > 0:
        # Estado Positivo / Feliz (Cuadro verde nativo)
        st.success("## 😄 Sentimiento Detectado: Positivo / Feliz")
        st.success(f"**Mensaje:** {random.choice(FRASES_FELICES)}")
        st.balloons()

    else:
        # Estado Neutral (Cuadro azul nativo)
        st.info("## 😐 Sentimiento Detectado: Neutral")
        st.info(f"**Mensaje:** {random.choice(FRASES_NEUTRALES)}")

elif analizar_btn and not text:
    st.warning("Por favor escribe una frase antes de presionar el botón.")
