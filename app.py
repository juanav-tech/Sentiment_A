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

# 2. CSS forzado para garantizar contraste 100% legible
st.markdown(
    """
    <style>
    /* Forzar fondo general claro */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Contenedor principal del resultado */
    .mood-box {
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    
    .mood-icon {
        font-size: 75px;
        line-height: 1;
        margin-bottom: 15px;
    }

    /* Título del resultado: Forzado a texto oscuro */
    .mood-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #111827 !important;
        margin-bottom: 12px !important;
    }

    /* Mensaje del resultado: Forzado a texto oscuro */
    .mood-message {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
        line-height: 1.5 !important;
    }

    /* Estilo del Botón */
    div.stButton > button:first-child {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        border: none !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado principal
st.title("🎭 Análisis de Sentimiento")

# Manejo de la imagen (escalada para evitar pixelado)
try:
    image = Image.open("emoticones.jpg")
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(image, width=320)
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

# Barra lateral
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

# Botón para activar el análisis
analizar_btn = st.button("🔍 Analizar Sentimiento")

if analizar_btn and text:
    # Corrección rápida para palabras clave explícitas en español
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

    # Ajuste para palabras directas en español si falla la librería de traducción
    texto_lower = text.lower()
    if any(p in texto_lower for p in palabras_tristes) and polarity >= 0:
        polarity = -0.50
    elif any(p in texto_lower for p in palabras_felices) and polarity <= 0:
        polarity = 0.50

    st.write("---")

    # Mostrar métricas
    col1, col2 = st.columns(2)
    col1.metric("Polaridad", f"{polarity}")
    col2.metric("Subjetividad", f"{subjectivity}")

    # Configuración de colores con alto contraste (Fondo claro + Borde visible + Texto muy oscuro)
    if polarity < 0:
        icono = "😔"
        color_fondo = "#fde8e8"  # Fondo Rojo / Rosa pastel
        color_borde = "#f87171"  # Borde rojo
        titulo = "Sentimiento Detectado: Negativo / Triste"
        mensaje = random.choice(FRASES_TRISTES)

    elif polarity > 0:
        icono = "😄"
        color_fondo = "#def7ec"  # Fondo Verde pastel
        color_borde = "#31c48d"  # Borde verde
        titulo = "Sentimiento Detectado: Positivo / Feliz"
        mensaje = random.choice(FRASES_FELICES)
        st.balloons()

    else:
        icono = "😐"
        color_fondo = "#e1effe"  # Fondo Azul pastel
        color_borde = "#76a9fa"  # Borde azul
        titulo = "Sentimiento Detectado: Neutral"
        mensaje = random.choice(FRASES_NEUTRALES)

    # Caja renderizada garantizando lectura limpia
    st.markdown(
        f"""
        <div class="mood-box" style="background-color: {color_fondo}; border: 3px solid {color_borde};">
            <div class="mood-icon">{icono}</div>
            <div class="mood-title">{titulo}</div>
            <div class="mood-message">{mensaje}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif analizar_btn and not text:
    st.warning("Por favor escribe una frase antes de hacer clic en el botón.")
