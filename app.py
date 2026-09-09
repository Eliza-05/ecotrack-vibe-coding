"""Interfaz web de EcoTrack: estimación de huella de carbono diaria."""

import streamlit as st

from carbon_estimator import estimar_huella

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")

# CSS mínimo y controlado: solo tipografía de acento (Fraunces, usada
# únicamente en el título y el resultado) y el estilo de las tarjetas/filas
# del desglose. El resto de la interfaz usa componentes nativos de Streamlit.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&display=swap');

    .eco-kicker {
        font-size: 0.75rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #2F6E4E;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .eco-title {
        font-family: 'Fraunces', serif;
        font-size: 2.6rem;
        font-weight: 600;
        color: #1F2A22;
        margin: 0;
        line-height: 1.15;
    }
    .eco-subtitle {
        color: #7C8577;
        font-size: 1rem;
        margin-top: 0.35rem;
        margin-bottom: 1.75rem;
    }
    .eco-result-label {
        color: #3f4a3f;
        font-size: 0.95rem;
        margin-bottom: 0.15rem;
    }
    .eco-result-value {
        font-family: 'Fraunces', serif;
        font-size: 3rem;
        font-weight: 600;
        color: #A85A3B;
        line-height: 1;
    }
    .eco-result-unit {
        font-size: 1.05rem;
        color: #1F2A22;
        font-weight: 500;
        margin-left: 0.4rem;
    }
    .eco-section-label {
        color: #3f4a3f;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 1.1rem 0 0.4rem 0;
    }
    .eco-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.45rem 0;
        border-bottom: 1px solid rgba(31, 42, 34, 0.08);
        font-size: 0.98rem;
    }
    .eco-row:last-child {
        border-bottom: none;
    }
    .stTextArea textarea {
        border-radius: 12px;
        font-size: 1.02rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _icono_actividad(descripcion: str) -> str:
    """Ícono cosmético según el texto de la actividad (solo presentación)."""
    texto = descripcion.lower()
    if texto.startswith("comida"):
        return "🍽️"

    iconos_transporte = [
        ("autobus", "🚌"),
        ("bus", "🚌"),
        ("avion", "✈️"),
        ("avión", "✈️"),
        ("tren", "🚆"),
        ("moto", "🏍️"),
        ("bici", "🚲"),
        ("caminando", "🚶"),
        ("a pie", "🚶"),
        ("carro", "🚗"),
        ("coche", "🚗"),
        ("auto", "🚗"),
    ]
    for palabra, icono in iconos_transporte:
        if palabra in texto:
            return icono
    return "🌍"


def _etiqueta_actividad(descripcion: str) -> str:
    """Texto legible de la actividad (solo presentación)."""
    if descripcion.lower().startswith("comida:"):
        return descripcion.split(":", 1)[1].strip().capitalize()
    return descripcion.capitalize()


st.markdown('<div class="eco-kicker">Diario de huella de carbono</div>', unsafe_allow_html=True)
st.markdown('<p class="eco-title">🌱 EcoTrack</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="eco-subtitle">Cuéntame qué hiciste hoy y te muestro tu huella estimada de CO2e.</p>',
    unsafe_allow_html=True,
)

texto = st.text_area(
    "¿Qué hiciste hoy?",
    placeholder='Ej: "Hoy comí carne y viajé 20 km en bus"',
    height=140,
)

calcular = st.button("Calcular huella de carbono", type="primary", use_container_width=True)

if calcular:
    if not texto or not texto.strip():
        st.warning("Por favor escribe una descripción de tus actividades antes de calcular.")
    else:
        total_co2e, actividades = estimar_huella(texto)

        if not actividades:
            st.info(
                "No se detectaron actividades reconocibles en el texto. "
                "Intenta mencionar transporte (ej. \"10 km en bus\") o alimentación (ej. \"comí pollo\")."
            )
        else:
            with st.container(border=True):
                st.markdown(
                    '<div class="eco-result-label">Tu huella estimada de hoy</div>'
                    f'<div><span class="eco-result-value">{total_co2e:g}</span>'
                    '<span class="eco-result-unit">kg CO2e</span></div>',
                    unsafe_allow_html=True,
                )

                st.markdown('<div class="eco-section-label">Desglose de actividades</div>', unsafe_allow_html=True)

                filas = "".join(
                    '<div class="eco-row">'
                    f'<span>{_icono_actividad(a.descripcion)} {_etiqueta_actividad(a.descripcion)}</span>'
                    f'<span><strong>{a.co2e_kg:g} kg CO2e</strong></span>'
                    "</div>"
                    for a in actividades
                )
                st.markdown(filas, unsafe_allow_html=True)

st.divider()
st.caption(
    "Estimación aproximada con fines educativos, basada en factores de emisión generales."
)
