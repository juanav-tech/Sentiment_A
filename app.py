import random
import pandas as pd
from PIL import Image
import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# 1. Configuración de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)

# Initialize Translator
translator = Translator()

# 2. Personalización visual y de colores con CSS
st.markdown(
    """
    <style>
    /* Fondo principal de la aplicación */
    .stApp {
        background-color: #f4f6f9;
    }
    
    /* Estilo para el contenedor de resultado con ícono */
    .mood-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    }
    
    .mood-icon {
        font-size: 80px;
        margin-bottom: 10px;
    }

    .mood-title {
        font-size: 26px;
        font-weight: bold;
    }

    /* Personalización del botón */
    div.stButton > button:first-child {
        background-color: #4f46e5;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 24px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #4338ca;
        color: #ffffff;
        transform: scale(1.01);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Título e Imagen
st.title("🎭 Análisis de Sentimiento")

try:
    image = Image.open("emoticones.jpg")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# Frases motivacionales y de refuerzo
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

# Barra lateral
with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.write("""
    **Polaridad:** Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
    Su valor oscila entre -1 (muy negativo) y 1 (muy positivo).
    
    **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones) frente a objetivo (hechos). 
    Va de 0 a 1.
    """)

# Campo de texto de entrada
text = st.text_input("Escribe por favor tu frase aquí:", key="input_texto")

# Botón para ejecutar el análisis
analizar_btn = st.button("🔍 Analizar Sentimiento")

if analizar_btn and text:
    # Palabras clave explícitas en español para evitar fallas en la traducción de frases muy cortas
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

    # Intentar traducción
    try:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
    except Exception:
        trans_text = text

    blob = TextBlob(trans_text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)

    # Ajuste manual si el diccionario encuentra palabras directas en español (corrige el caso de "día triste")
    texto_lower = text.lower()
    if any(p in texto_lower for p in palabras_tristes) and polarity >= 0:
        polarity = -0.50
    elif any(p in texto_lower for p in palabras_felices) and polarity <= 0:
        polarity = 0.50

    st.write("---")

    # Mostrar métricas visuales
    col1, col2 = st.columns(2)
    col1.metric("Polaridad", f"{polarity}")
    col2.metric("Subjetividad", f"{subjectivity}")

    # Lógica de detección, íconos y cambio de colores de fondo según sentimiento
    if polarity < 0:
        # TRISTE: Fondo rojo claro/rosado
        icono = "😔"
        color_fondo = "#ffebee"
        color_borde = "#ef5350"
        color_texto = "#c62828"
        titulo = "Sentimiento Detectado: Negativo / Triste"
        mensaje = random.choice(FRASES_TRISTES)

    elif polarity > 0:
        # FELIZ: Fondo verde claro
        icono = "😊"
        color_fondo = "#e8f5e9"
        color_borde = "#66bb6a"
        color_texto = "#2e7d32"
        titulo = "Sentimiento Detectado: Positivo / Feliz"
        mensaje = random.choice(FRASES_FELICES)
        st.balloons()

    else:
        # NEUTRAL: Fondo gris/azul claro
        icono = "😐"
        color_fondo = "#e3f2fd"
        color_borde = "#42a5f5"
        color_texto = "#1565c0"
        titulo = "Sentimiento Detectado: Neutral"
        mensaje = random.choice(FRASES_NEUTRALES)

    # Tarjeta de resultado visual personalizada en HTML/CSS
    st.markdown(
        f"""
        <div class="mood-box" style="background-color: {color_fondo}; border: 2px solid {color_borde}; color: {color_texto};">
            <div class="mood-icon">{icono}</div>
            <div class="mood-title">{titulo}</div>
            <p style="font-size: 18px; margin-top: 15px;">{mensaje}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif analizar_btn and not text:
    st.warning("Por favor, escribe una frase antes de hacer clic en el botón.")
