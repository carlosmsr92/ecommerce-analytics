"""
Componentes UI Reutilizables para Dashboard
Autor: cmsr92

La banda de cabecera, el pie y el icono de la pestaña vienen de utils/marca.py (marco común CMSR92 del portfolio);
los colores de fondo, texto y acento, de .streamlit/config.toml.
"""

import re

import streamlit as st

# Colores de acento del portfolio, con contraste >= 3:1 como borde o marca sobre el fondo claro y el oscuro
TURQUESA = '#0A8CA2'
VERDE = '#1F9D55'
AMBAR = '#D97706'
AZUL = '#2F80C8'
ROJO = '#D64545'


def crear_seccion_titulo(titulo, icono="📊"):
    """Crea un título de sección profesional"""
    st.markdown(f'<div class="seccion-titulo">{icono} {titulo}</div>', unsafe_allow_html=True)


def aplicar_estilos_globales():
    """
    Estilos de los componentes propios del dashboard. Las cajas usan un fondo tintado y un borde de color, y el texto
    hereda el del tema: se leen igual en claro y en oscuro (Streamlit sigue el tema del sistema, igual que la media query).
    """
    st.markdown(f"""
    <style>
        :root {{
            --bg-tarjeta: #FFFFFF;
            --color-texto-secundario: #475569;
            --color-borde: #E2E8F0;
            --sombra: 0 4px 6px rgba(0, 0, 0, 0.08);
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-tarjeta: #1E293B;
                --color-texto-secundario: #CBD5E1;
                --color-borde: #334155;
                --sombra: 0 4px 6px rgba(0, 0, 0, 0.3);
            }}
        }}

        .descripcion-seccion {{
            background: var(--bg-tarjeta);
            border-left: 4px solid {TURQUESA};
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: var(--sombra);
        }}
        .descripcion-seccion h4 {{
            margin: 0 0 0.75rem 0;
            padding: 0;
            font-weight: 600;
        }}
        .descripcion-seccion p {{
            color: var(--color-texto-secundario);
            line-height: 1.6;
            margin: 0;
        }}

        .caja {{
            padding: 1.1rem 1.25rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            border-left: 4px solid var(--acento);
            background: color-mix(in srgb, var(--acento) 12%, transparent);
        }}
        .caja h5 {{
            margin: 0 0 0.5rem 0;
            padding: 0;
            font-weight: 700;
        }}
        .caja p, .caja ul {{
            margin: 0;
            line-height: 1.5;
        }}
        .caja ul {{
            padding-left: 1.5rem;
        }}
        .caja li {{
            margin: 0.4rem 0;
        }}
        .caja.insight {{ --acento: {VERDE}; }}
        .caja.recomendacion {{ --acento: {TURQUESA}; }}
        .caja.verde {{ --acento: {VERDE}; }}
        .caja.ambar {{ --acento: {AMBAR}; }}
        .caja.azul {{ --acento: {AZUL}; }}
        .caja.roja {{ --acento: {ROJO}; }}

        .seccion-titulo {{
            font-size: 1.9rem;
            font-weight: 700;
            margin: 2.5rem 0 1.5rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid {TURQUESA};
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        div[data-testid="stExpander"] {{
            background: var(--bg-tarjeta);
            border-radius: 12px;
            border: 2px solid var(--color-borde);
            margin-bottom: 1rem;
        }}
        div[data-testid="stExpander"] summary {{
            font-weight: 600;
            font-size: 1.05rem;
        }}

        .stSelectbox label, .stMultiSelect label, .stDateInput label, .stSlider label, .stCheckbox label {{
            font-weight: 600;
            font-size: 0.95rem;
        }}
    </style>
    """, unsafe_allow_html=True)


def crear_descripcion_seccion(titulo, descripcion):
    """Crea una descripción profesional al inicio de cada sección"""
    st.markdown(f"""
    <div class="descripcion-seccion">
        <h4>📋 {titulo}</h4>
        <p>{_negritas(descripcion)}</p>
    </div>
    """, unsafe_allow_html=True)


def _negritas(texto):
    """Dentro de un bloque HTML Streamlit no interpreta markdown: **texto** se convierte a <strong> a mano."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", str(texto))


def crear_insight(titulo, contenido):
    """Crea un cuadro de insight accionable"""
    # En una sola línea: con líneas en blanco o indentadas, markdown cierra el bloque HTML y muestra el resto como código
    cabecera = f"<h5>💡 {titulo}</h5>" if titulo else ""
    st.markdown(f'<div class="caja insight">{cabecera}<p>{_negritas(contenido)}</p></div>', unsafe_allow_html=True)


def crear_recomendaciones(titulo, recomendaciones):
    """
    Crea un cuadro de recomendaciones profesionales

    Args:
        titulo: Título del cuadro de recomendaciones
        recomendaciones: Lista de strings con las recomendaciones
    """
    items_html = "".join([f"<li>{_negritas(rec)}</li>" for rec in recomendaciones])
    st.markdown(f'<div class="caja recomendacion"><h5>🎯 {titulo}</h5><ul>{items_html}</ul></div>',
                unsafe_allow_html=True)
