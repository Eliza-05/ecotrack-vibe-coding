"""Lógica de estimación de huella de carbono a partir de texto libre.

No depende de Streamlit ni de ninguna librería de interfaz: recibe texto
y devuelve datos estructurados para que la capa de UI los presente.
"""

import re
from dataclasses import dataclass

# Factores de emisión aproximados en kg CO2e.
# Transporte: por kilómetro recorrido.
FACTORES_TRANSPORTE = {
    "bus": 0.10,
    "autobus": 0.10,
    "carro": 0.19,
    "coche": 0.19,
    "auto": 0.19,
    "moto": 0.11,
    "motocicleta": 0.11,
    "avion": 0.25,
    "avión": 0.25,
    "tren": 0.04,
    "bicicleta": 0.0,
    "bici": 0.0,
    "caminando": 0.0,
    "a pie": 0.0,
}

# Alimentación: por mención de la comida (estimación de una porción/comida).
FACTORES_ALIMENTACION = {
    "carne": 6.0,
    "res": 6.0,
    "pollo": 1.1,
    "pescado": 1.5,
    "cerdo": 3.5,
    "vegetariano": 0.5,
    "vegetariana": 0.5,
    "verduras": 0.5,
    "ensalada": 0.5,
}

# Patrón: un número (con o sin decimales) seguido de "km" y opcionalmente
# "en <medio>", donde <medio> debe ser una de las claves conocidas de
# FACTORES_TRANSPORTE. Restringir el medio a la lista conocida (en vez de
# aceptar cualquier palabra) evita que el grupo capture de más palabras
# siguientes (p. ej. la conjunción "y" en "10 km en carro y 5 km en bus").
# Se ordenan las claves de más larga a más corta para que, ante medios que
# comparten prefijo (p. ej. "auto" y "autobus"), se intente primero el más
# específico.
_MODOS_ORDENADOS = sorted(FACTORES_TRANSPORTE, key=len, reverse=True)
_ALTERNANCIA_MODOS = "|".join(re.escape(modo) for modo in _MODOS_ORDENADOS)

PATRON_TRANSPORTE = re.compile(
    rf"(\d+(?:[.,]\d+)?)\s*km(?:\s+en\s+({_ALTERNANCIA_MODOS})\b)?",
    re.IGNORECASE,
)

# Verbos que implican conducir un carro cuando el texto no especifica medio
# explícito (p. ej. "manejé 15 km", "conduje 15 km"). Supuesto documentado
# a pedido del usuario: estas raíces verbales se interpretan como "carro".
PATRON_VERBO_CONDUCIR = re.compile(r"\b(?:manej|conduj)\w*\b", re.IGNORECASE)


@dataclass
class Actividad:
    descripcion: str
    co2e_kg: float


def _detectar_transporte(texto_normalizado: str) -> list[Actividad]:
    hay_verbo_conducir = PATRON_VERBO_CONDUCIR.search(texto_normalizado) is not None

    actividades = []
    for match in PATRON_TRANSPORTE.finditer(texto_normalizado):
        distancia = float(match.group(1).replace(",", "."))
        medio = (match.group(2) or "").strip().lower()

        if not medio and hay_verbo_conducir:
            medio = "carro"

        factor = FACTORES_TRANSPORTE.get(medio)
        if factor is None:
            continue
        co2e = round(distancia * factor, 2)
        actividades.append(
            Actividad(f"{distancia:g} km en {medio}", co2e)
        )
    return actividades


def _detectar_alimentacion(texto_normalizado: str) -> list[Actividad]:
    actividades = []
    for palabra, factor in FACTORES_ALIMENTACION.items():
        if re.search(rf"\b{re.escape(palabra)}\b", texto_normalizado):
            actividades.append(Actividad(f"Comida: {palabra}", factor))
    return actividades


def estimar_huella(texto: str) -> tuple[float, list[Actividad]]:
    """Estima el CO2e total y el desglose de actividades detectadas en el texto.

    Devuelve (0.0, []) si el texto está vacío o no se reconoce ninguna actividad.
    """
    if not texto or not texto.strip():
        return 0.0, []

    texto_normalizado = texto.lower()

    actividades = _detectar_transporte(texto_normalizado) + _detectar_alimentacion(
        texto_normalizado
    )

    total = round(sum(a.co2e_kg for a in actividades), 2)
    return total, actividades
