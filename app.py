import random
from googletrans import Translator
from PIL import Image
import streamlit as st
from textblob import TextBlob

# 1. Configuración de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)

# Inicializar Traductor
translator = Translator()

# 2. CSS optimizado: Contraste de texto legible y diseño estilizado
st.markdown(
    """
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Tarjeta de resultado con alto contraste */
    .mood-box {
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    }
    
    .mood-icon {
        font-size: 75px;
        margin-bottom: 10px;
    }

    .mood-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .mood-message {
        font-size: 18px;
        font-weight: 500;
        line-height: 1.5;
    }

    /* Botón personalizado */
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: #ffffff !important;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8;
        transform: scale(1.01);
    }

    /* Formato para el código de requirements */
    .req-box {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado
st.title("🎭 Análisis de Sentimiento")

# Manejo de imagen escalada para evitar pixelado
try:
    image = Image.open("emoticones.jpg")
    # Se limita el ancho a 350px e incluye centrado para mantener nitidez
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(image, width=350)
except FileNotFoundError:
    pass

st.subheader("Escribe una frase para analizar tu estado de ánimo:")

# Banco de respuestas
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
    st.subheader("Información General")
    st.write("""
    **Polaridad:**
    Indica si el sentimiento es positivo, negativo o neutral (-1 a 1).
    
    **Subjetividad:**
    Mide cuánto del texto representa una opinión sobre un hecho real (0 a 1).
    """)

# Campo de texto de entrada
text = st.text_input(
    "Escribe por favor tu frase aquí:", placeholder="Ej: Hoy es un día triste..."
)

# Botón para ejecutar el análisis
analizar_btn = st.button("🔍 Analizar Sentimiento")

if analizar_btn and text:
    # Detección explicita de términos clave en español
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

    # Regla de corrección directa para frases cortas en español
    texto_lower = text.lower()
    if any(p in texto_lower for p in palabras_tristes) and polarity >= 0:
        polarity = -0.50
    elif any(p in texto_lower for p in palabras_felices) and polarity <= 0:
        polarity = 0.50

    st.write("---")

    # Métricas
    col1, col2 = st.columns(2)
    col1.metric("Polaridad", f"{polarity}")
    col2.metric("Subjetividad", f"{subjectivity}")

    # Definición estricta de contraste: Fondos pastel claros con texto oscuro muy legible
    if polarity < 0:
        icono = "😔"
        color_fondo = "#fee2e2"  # Rojo claro pastel
        color_borde = "#f87171"
        color_texto = "#7f1d1d"  # Rojo oscuro legibilidad 100%
        titulo = "Sentimiento Detectado: Negativo / Triste"
        mensaje = random.choice(FRASES_TRISTES)

    elif polarity > 0:
        icono = "😄"
        color_fondo = "#dcfce7"  # Verde claro pastel
        color_borde = "#4ade80"
        color_texto = "#14532d"  # Verde oscuro legibilidad 100%
        titulo = "Sentimiento Detectado: Positivo / Feliz"
        mensaje = random.choice(FRASES_FELICES)
        st.balloons()

    else:
        icono = "😐"
        color_fondo = "#e0f2fe"  # Azul claro pastel
        color_borde = "#38bdf8"
        color_texto = "#0c4a6e"  # Azul oscuro legibilidad 100%
        titulo = "Sentimiento Detectado: Neutral"
        mensaje = random.choice(FRASES_NEUTRALES)

    # Tarjeta estilizada con colores corregidos
    st.markdown(
        f"""
        <div class="mood-box" style="background-color: {color_fondo}; border: 2px solid {color_borde};">
            <div class="mood-icon">{icono}</div>
            <div class="mood-title" style="color: {color_texto};">{titulo}</div>
            <div class="mood-message" style="color: {color_texto};">{mensaje}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif analizar_btn and not text:
    st.warning("Por favor escribe una frase antes de analizar.")

# ----------------------------------------------------
# Requisitos del Proyecto (requirements.txt)
# ----------------------------------------------------
st.write("---")
with st.expander("📄 Ver archivo requirements.txt recomendado"):
    st.markdown(
        "Copia y pega estas dependencias en tu archivo `requirements.txt`:"
    )
    st.code(
        """
streamlit>=1.28.0
textblob>=0.17.1
pandas>=2.0.0
Pillow>=10.0.0
googletrans==3.1.0a0
    """,
        language="text",
    )
