"""
Componentes UI Reutilizables para Dashboard
Autor: cmsr92
"""

import base64
import re
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

PALETA_CORPORATIVA = {
    'primario': '#0F172A',
    'secundario': '#1E40AF',
    'acento': '#10B981',
    'acento2': '#F59E0B',
    'error': '#EF4444',
    'exito': '#10B981',
    'neutro': '#64748B',
    'fondo': '#F8FAFC',
}

def crear_tarjeta_kpi(icono, etiqueta, valor, cambio=None, formato='numero', col=None):
    """
    Crea una tarjeta KPI profesional
    
    Args:
        icono: Emoji del icono
        etiqueta: Texto descriptivo del KPI
        valor: Valor numérico del KPI
        cambio: Cambio porcentual vs periodo anterior (opcional)
        formato: 'numero', 'moneda', 'porcentaje'
        col: Columna de streamlit donde renderizar (opcional)
    """
    if formato == 'moneda':
        valor_formateado = f"${valor:,.0f}"
    elif formato == 'porcentaje':
        valor_formateado = f"{valor:.1f}%"
    else:
        valor_formateado = f"{valor:,}" if isinstance(valor, (int, float)) else str(valor)
    
    html_cambio = ""
    if cambio is not None:
        icono_tendencia = "📈" if cambio >= 0 else "📉"
        clase_cambio = "positivo" if cambio >= 0 else "negativo"
        html_cambio = f'''
        <div class="kpi-cambio {clase_cambio}">
            {icono_tendencia} {abs(cambio):.1f}% vs periodo anterior
        </div>
        '''
    
    html_kpi = f'''
    <div class="tarjeta-kpi">
        <div class="kpi-icono">{icono}</div>
        <div class="kpi-etiqueta">{etiqueta}</div>
        <div class="kpi-valor">{valor_formateado}</div>
        {html_cambio}
    </div>
    '''
    
    if col:
        col.markdown(html_kpi, unsafe_allow_html=True)
    else:
        st.markdown(html_kpi, unsafe_allow_html=True)

def crear_seccion_titulo(titulo, icono="📊"):
    """Crea un título de sección profesional"""
    st.markdown(f'<div class="seccion-titulo">{icono} {titulo}</div>', unsafe_allow_html=True)

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo_cmsr92.png"

def crear_header_principal(titulo, subtitulo):
    """Crea el header principal del dashboard, con el logo CMSR92 en blanco (PNG transparente + filtro CSS)"""
    logo = (f'<img class="logo-cmsr92" alt="CMSR92" src="data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}">'
            if LOGO.exists() else "")
    st.markdown(f'<div class="header-principal">{logo}<h1>{titulo}</h1><p>{subtitulo}</p></div>', unsafe_allow_html=True)

def crear_pie_pagina():
    """Crea el pie de página con firma CMSR92"""
    st.markdown("""
    <div class="pie-pagina">
        <p>Analítica global de e-commerce</p>
        <p class="firma-autor">Carlos Manuel Suárez Rivero · CMSR92</p>
    </div>
    """, unsafe_allow_html=True)

def crear_metrica_comparativa(titulo, valor_actual, valor_anterior, formato='numero'):
    """Crea una métrica con comparación visual"""
    if formato == 'moneda':
        actual_str = f"${valor_actual:,.0f}"
        anterior_str = f"${valor_anterior:,.0f}"
    elif formato == 'porcentaje':
        actual_str = f"{valor_actual:.1f}%"
        anterior_str = f"{valor_anterior:.1f}%"
    else:
        actual_str = f"{valor_actual:,}"
        anterior_str = f"{valor_anterior:,}"
    
    if valor_anterior > 0:
        cambio = ((valor_actual - valor_anterior) / valor_anterior) * 100
        delta_str = f"{cambio:+.1f}%"
    else:
        delta_str = "N/A"
    
    st.metric(
        label=titulo,
        value=actual_str,
        delta=delta_str,
        delta_color="normal"
    )

def aplicar_estilos_globales():
    """
    Aplica los estilos CSS globales del dashboard con detección automática de tema del navegador.
    Utiliza CSS media query 'prefers-color-scheme' para adaptar automáticamente los colores.
    """
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Variables CSS para modo claro (por defecto) */
        :root {
            --bg-principal: #F8FAFC;
            --bg-secundario: #FFFFFF;
            --bg-tarjeta: #FFFFFF;
            --color-texto: #0F172A;
            --color-texto-secundario: #475569;
            --color-borde: #E2E8F0;
            --sombra: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Variables CSS para modo oscuro - detección automática */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-principal: #0F172A;
                --bg-secundario: #1E293B;
                --bg-tarjeta: #1E293B;
                --color-texto: #F1F5F9;
                --color-texto-secundario: #CBD5E1;
                --color-borde: #334155;
                --sombra: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
        }
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background-color: var(--bg-principal);
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: var(--bg-principal);
        }
        
        .header-principal {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2.5rem;
            text-align: center;
        }
        
        /* Texto blanco también en los elementos internos que crea Streamlit (span), que la regla global de color pisaba */
        .header-principal h1, .header-principal h1 * {
            color: white !important;
        }

        .header-principal p, .header-principal p * {
            color: rgba(255,255,255,0.95) !important;
        }

        .header-principal .logo-cmsr92 {
            height: 46px;
            width: auto;
            filter: brightness(0) invert(1);
            margin-bottom: 1rem;
        }

        .header-principal h1 {
            color: white !important;  /* el tema claro de Streamlit lo pintaba en azul oscuro sobre el morado */
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-principal p {
            color: rgba(255,255,255,0.95);
            font-size: 1.15rem;
            margin-top: 0.75rem;
            font-weight: 300;
        }
        
        .descripcion-seccion {
            background: var(--bg-tarjeta);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: var(--sombra);
        }
        
        .descripcion-seccion h4 {
            color: var(--color-texto);
            margin: 0 0 0.75rem 0;
            font-weight: 600;
        }
        
        .descripcion-seccion p {
            color: var(--color-texto-secundario);
            line-height: 1.6;
            margin: 0;
        }
        
        .insight-box {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            padding: 1.25rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        .insight-box h5 {
            margin: 0 0 0.5rem 0;
            font-weight: 700;
            color: white !important;
        }
        
        .insight-box p {
            margin: 0;
            color: rgba(255,255,255,0.95) !important;
            line-height: 1.5;
        }
        
        .recomendacion-box {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: white;
            padding: 1.25rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .recomendacion-box h5 {
            margin: 0 0 0.5rem 0;
            font-weight: 700;
            color: white !important;
        }
        
        .recomendacion-box ul {
            margin: 0.5rem 0 0 0;
            padding-left: 1.5rem;
            color: rgba(255,255,255,0.95) !important;
        }
        
        .recomendacion-box li {
            margin: 0.4rem 0;
            color: rgba(255,255,255,0.95) !important;
        }
        
        .tarjeta-kpi {
            background: var(--bg-tarjeta);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: var(--sombra);
            border-left: 4px solid #10B981;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
        }
        
        .tarjeta-kpi:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        }
        
        .kpi-icono {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .kpi-valor {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--color-texto);
            margin: 0.5rem 0;
        }
        
        .kpi-etiqueta {
            font-size: 0.9rem;
            color: var(--color-texto-secundario);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .kpi-cambio {
            font-size: 0.85rem;
            margin-top: 0.5rem;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            display: inline-block;
        }
        
        .kpi-cambio.positivo {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10B981;
            font-weight: 600;
        }
        
        .kpi-cambio.negativo {
            background-color: rgba(239, 68, 68, 0.15);
            color: #EF4444;
            font-weight: 600;
        }
        
        .seccion-titulo {
            font-size: 1.9rem;
            font-weight: 700;
            color: var(--color-texto);
            margin: 2.5rem 0 1.5rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid #10B981;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        /* Navegación de pestañas mejorada - más compacta y profesional */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: var(--bg-secundario);
            padding: 0.75rem;
            border-radius: 12px;
            box-shadow: var(--sombra);
            display: flex;
            flex-wrap: wrap !important;
            justify-content: center;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px;
            background-color: var(--bg-principal);
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--color-texto-secundario);
            border: 2px solid var(--color-borde);
            transition: all 0.3s;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(102, 126, 234, 0.1);
            border-color: #667eea;
            color: var(--color-texto);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-color: transparent !important;
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
        }
        
        .pie-pagina {
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            border-top: 2px solid var(--color-borde);
            color: var(--color-texto-secundario);
            font-size: 0.9rem;
        }
        
        .firma-autor {
            font-weight: 700;
            color: #667eea;
            font-size: 1.2rem;
            margin: 0.5rem 0;
        }
        
        div[data-testid="stExpander"] {
            background: var(--bg-tarjeta);
            border-radius: 12px;
            border: 2px solid var(--color-borde);
            margin-bottom: 1rem;
        }
        
        div[data-testid="stExpander"] summary {
            font-weight: 600;
            color: var(--color-texto);
            font-size: 1.05rem;
        }
        
        .stSelectbox label, .stMultiSelect label, .stDateInput label, .stSlider label, .stCheckbox label {
            font-weight: 600;
            color: var(--color-texto) !important;
            font-size: 0.95rem;
        }
        
        .tooltip-info {
            font-size: 0.85rem;
            color: var(--color-texto-secundario);
            font-style: italic;
            margin-top: 0.25rem;
        }
        
        /* Asegurar legibilidad en todos los elementos de Streamlit */
        .stMarkdown, .stText, p, span, div {
            color: var(--color-texto) !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--color-texto) !important;
        }
        
        /* Estilos responsive para navegación */
        @media (max-width: 1200px) {
            .stTabs [data-baseweb="tab"] {
                font-size: 0.85rem;
                padding: 8px 14px;
            }
        }
        
        @media (max-width: 768px) {
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap !important;
                gap: 4px;
            }
            
            .stTabs [data-baseweb="tab"] {
                font-size: 0.8rem;
                padding: 8px 12px;
            }
            
            .tarjeta-kpi {
                margin-bottom: 1rem;
            }
            
            .header-principal h1 {
                font-size: 2rem;
            }
            
            .header-principal p {
                font-size: 1rem;
            }
        }
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
    st.markdown(f'<div class="insight-box">{cabecera}<p>{_negritas(contenido)}</p></div>', unsafe_allow_html=True)

def crear_recomendaciones(titulo, recomendaciones):
    """
    Crea un cuadro de recomendaciones profesionales
    
    Args:
        titulo: Título del cuadro de recomendaciones
        recomendaciones: Lista de strings con las recomendaciones
    """
    items_html = "".join([f"<li>{_negritas(rec)}</li>" for rec in recomendaciones])
    st.markdown(f"""
    <div class="recomendacion-box">
        <h5>🎯 {titulo}</h5>
        <ul>{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)

def mostrar_info_dataset(num_transacciones, num_clientes, num_productos, fecha_min, fecha_max):
    """Muestra información resumida del dataset"""
    años = fecha_max.year - fecha_min.year + 1
    st.info(f"""
    📊 **Dataset Actual:** {num_transacciones:,} transacciones | {num_clientes:,} clientes | {num_productos:,} productos  
    📅 **Periodo:** {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')} ({años} años)
    """)
