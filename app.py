"""
Dashboard Avanzado de Analytics Ecommerce Global
Autor: cmsr92
Versión: 4.0
Plataforma profesional de Business Intelligence con ML, IA y Análisis Predictivo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import warnings

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_,
    .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK,
    #GithubIcon {display: none;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Analytics Ecommerce Global | cmsr92",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"  # desplegado en PC, plegado en móvil (si no, tapa la pantalla)
)

from utils.ui_components import (
    aplicar_estilos_globales, crear_header_principal, crear_tarjeta_kpi,
    crear_seccion_titulo, crear_pie_pagina, mostrar_info_dataset,
    crear_descripcion_seccion, crear_insight, crear_recomendaciones
)
from utils.filtros import crear_filtros_sidebar, aplicar_filtros
from utils.data_loader_pg import load_or_generate_data
from utils.traducciones import obtener_labels_profesionales

# Labels profesionales para gráficos
LABELS = obtener_labels_profesionales()

# Aplicar estilos globales con detección automática de tema del navegador
aplicar_estilos_globales()

@st.cache_data(ttl=60)
def cargar_datos():
    return load_or_generate_data()

transacciones_df, clientes_df, productos_df = cargar_datos()

if transacciones_df is None or clientes_df is None or productos_df is None:
    st.error("❌ Error al cargar los datos. Por favor recarga la página.")
    st.stop()

crear_header_principal(
    "📊 Analytics Ecommerce Global",
    "Plataforma Avanzada de Business Intelligence, Machine Learning y Análisis Predictivo"
)

filtros = crear_filtros_sidebar(transacciones_df)
datos_filtrados = aplicar_filtros(transacciones_df, filtros)

if len(datos_filtrados) == 0:
    st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados. Ajusta los criterios de búsqueda.")
    st.stop()

tab_overview, tab_geografia, tab_rendimiento, tab_productos, tab_clientes, tab_canal, tab_ml, tab_finanzas, tab_operacional = st.tabs([
    "🏠 Resumen General",
    "🌍 Análisis Geográfico",
    "📈 Rendimiento & Análisis Temporal",
    "📦 Análisis de Productos",
    "👥 Segmentación de Clientes",
    "📱 Análisis de Canal",
    "🤖 ML & IA Insights",
    "💰 Análisis Financiero",
    "⚙️ Métricas Operacionales"
])

with tab_overview:
    crear_descripcion_seccion(
        "Resumen Ejecutivo",
        "Esta sección presenta una visión general del rendimiento del negocio. Los KPIs principales muestran la salud financiera, "
        "el volumen de operaciones y la eficiencia comercial. Utiliza los filtros del sidebar para analizar períodos específicos, "
        "regiones geográficas o segmentos de clientes."
    )
    
    crear_seccion_titulo("Indicadores Clave de Rendimiento (KPIs)")
    
    # Explicación de KPIs
    with st.expander("ℹ️ ¿Qué significan estos indicadores?", expanded=False):
        st.markdown("""
        **💰 Ingresos Totales:** Suma de todas las ventas en el período seleccionado. El símbolo % muestra el cambio respecto al período anterior equivalente.
        
        **🛒 Pedidos Totales:** Número total de transacciones completadas. Un aumento indica mayor actividad comercial.
        
        **🎯 Ticket Promedio (AOV):** Valor promedio por pedido. Se calcula dividiendo ingresos totales entre número de pedidos. Un AOV alto indica clientes que compran más por transacción.
        
        **💎 Beneficio Total:** Ganancia neta después de costos. Se calcula como: Ingresos - Costos. Indica la rentabilidad real del negocio.
        
        **👥 Clientes Únicos:** Número de clientes diferentes que realizaron al menos una compra.
        
        **📦 Productos Vendidos:** Cantidad de productos distintos que se vendieron en el período.
        
        **🎯 Tasa de Conversión:** Porcentaje de clientes únicos respecto al total de pedidos. Una tasa cercana a 100% indica que cada pedido corresponde a un cliente diferente (baja repetición).
        
        **📊 Items por Pedido:** Promedio de artículos incluidos en cada transacción. Útil para estrategias de bundling y cross-selling.
        """)
    
    ingresos_totales = datos_filtrados['total_amount_usd'].sum()
    pedidos_totales = len(datos_filtrados)
    ticket_promedio = datos_filtrados['total_amount_usd'].mean()
    beneficio_total = datos_filtrados['profit'].sum()
    clientes_unicos = datos_filtrados['customer_id'].nunique()
    margen_promedio = (beneficio_total / ingresos_totales * 100) if ingresos_totales > 0 else 0
    
    fecha_inicio_comparacion = filtros['fecha_inicio'] - (filtros['fecha_fin'] - filtros['fecha_inicio'])
    
    # Aplicar LOS MISMOS filtros al período anterior (excepto fechas) para comparación válida
    filtros_periodo_anterior_overview = filtros.copy()
    filtros_periodo_anterior_overview['fecha_inicio'] = fecha_inicio_comparacion
    filtros_periodo_anterior_overview['fecha_fin'] = filtros['fecha_inicio'] - pd.Timedelta(days=1)
    
    datos_periodo_anterior = aplicar_filtros(transacciones_df, filtros_periodo_anterior_overview)
    
    ingresos_anteriores = datos_periodo_anterior['total_amount_usd'].sum()
    cambio_ingresos = ((ingresos_totales - ingresos_anteriores) / ingresos_anteriores * 100) if ingresos_anteriores > 0 else 0
    
    pedidos_anteriores = len(datos_periodo_anterior)
    cambio_pedidos = ((pedidos_totales - pedidos_anteriores) / pedidos_anteriores * 100) if pedidos_anteriores > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Ingresos Totales",
            value=f"${ingresos_totales:,.0f}",
            delta=f"{cambio_ingresos:+.1f}%" if ingresos_anteriores > 0 else None
        )
    
    with col2:
        st.metric(
            label="🛒 Pedidos Totales",
            value=f"{pedidos_totales:,}",
            delta=f"{cambio_pedidos:+.1f}%" if pedidos_anteriores > 0 else None
        )
    
    with col3:
        st.metric(
            label="🎯 Ticket Promedio (AOV)",
            value=f"${ticket_promedio:,.0f}"
        )
    
    with col4:
        st.metric(
            label="💎 Beneficio Total",
            value=f"${beneficio_total:,.0f}"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="👥 Clientes Únicos",
            value=f"{clientes_unicos:,}"
        )
    
    with col6:
        productos_unicos = datos_filtrados['product_id'].nunique()
        st.metric(
            label="📦 Productos Vendidos",
            value=f"{productos_unicos:,}"
        )
    
    with col7:
        tasa_conversion = (clientes_unicos / pedidos_totales * 100) if pedidos_totales > 0 else 0
        st.metric(
            label="🎯 Tasa de Conversión",
            value=f"{tasa_conversion:.1f}%"
        )
    
    with col8:
        items_promedio = datos_filtrados['quantity'].mean()
        st.metric(
            label="📊 Items por Pedido",
            value=f"{items_promedio:.1f}"
        )
    
    # Sección de Insights Ejecutivos Automáticos
    st.markdown("<br>", unsafe_allow_html=True)
    crear_seccion_titulo("💡 Insights Ejecutivos y Recomendaciones")
    
    # Calcular métricas adicionales para insights (con protección contra división por cero)
    if ingresos_totales > 0:
        top_pais = datos_filtrados.groupby('country')['total_amount_usd'].sum().idxmax()
        ingresos_top_pais = datos_filtrados.groupby('country')['total_amount_usd'].sum().max()
        porcentaje_top_pais = (ingresos_top_pais / ingresos_totales * 100)
        
        top_categoria = datos_filtrados.groupby('category')['total_amount_usd'].sum().idxmax()
        ingresos_top_categoria = datos_filtrados.groupby('category')['total_amount_usd'].sum().max()
        porcentaje_top_categoria = (ingresos_top_categoria / ingresos_totales * 100)
    else:
        top_pais = "N/A"
        ingresos_top_pais = 0
        porcentaje_top_pais = 0
        top_categoria = "N/A"
        ingresos_top_categoria = 0
        porcentaje_top_categoria = 0
    
    # Generar insights automáticos
    insights_ejecutivos = []
    
    # Verificar si hay datos suficientes para generar insights
    if ingresos_totales == 0 or pedidos_totales == 0:
        insights_ejecutivos.append(
            f"ℹ️ **Sin Datos Disponibles:** No hay transacciones registradas en el período y filtros seleccionados. "
            f"Ajusta los criterios de búsqueda en el sidebar para analizar diferentes períodos o segmentos."
        )
    else:
        # Insight 1: Rendimiento general
        if cambio_ingresos > 10:
            insights_ejecutivos.append(
                f"📈 **Crecimiento Acelerado:** Los ingresos han crecido un {cambio_ingresos:.1f}% comparado con el período anterior, "
                f"superando ${ingresos_totales:,.0f}. Este momentum positivo indica una fuerte demanda y efectividad en las estrategias comerciales."
            )
        elif cambio_ingresos < -10:
            insights_ejecutivos.append(
                f"📊 **Análisis de Variación:** Los ingresos muestran una variación de {cambio_ingresos:+.1f}% comparado con el período anterior, "
                f"totalizando ${ingresos_totales:,.0f}. Consulta el tab 'Rendimiento & Análisis Temporal' para análisis detallado de tendencias."
            )
        else:
            insights_ejecutivos.append(
                f"📊 **Estabilidad Controlada:** Los ingresos se mantienen estables con una variación de {cambio_ingresos:+.1f}% respecto al período anterior, "
                f"totalizando ${ingresos_totales:,.0f}. Existen oportunidades de optimización para impulsar el crecimiento."
            )
        
        # Insight 2: Concentración geográfica
        if porcentaje_top_pais > 50:
            insights_ejecutivos.append(
                f"🌍 **Concentración de Mercado:** {top_pais} representa el {porcentaje_top_pais:.1f}% de los ingresos totales "
                f"(${ingresos_top_pais:,.0f}). Esta alta dependencia presenta riesgo. Se recomienda diversificar geográficamente."
            )
        else:
            insights_ejecutivos.append(
                f"🌍 **Diversificación Saludable:** {top_pais} lidera con {porcentaje_top_pais:.1f}% de ingresos, pero existe buena "
                f"distribución geográfica, reduciendo el riesgo de dependencia de un solo mercado."
            )
        
        # Insight 3: Producto estrella
        insights_ejecutivos.append(
            f"⭐ **Categoría Líder:** {top_categoria} domina el portafolio con {porcentaje_top_categoria:.1f}% de los ingresos "
            f"(${ingresos_top_categoria:,.0f}). Reforzar inventario y marketing en esta categoría puede maximizar resultados."
        )
        
        # Insight 4: Eficiencia operativa
        if ticket_promedio > 100:
            insights_ejecutivos.append(
                f"💎 **Alto Valor por Transacción:** El ticket promedio de ${ticket_promedio:,.0f} indica clientes de alto valor. "
                f"Enfocar estrategias de retención y programas VIP puede aumentar la rentabilidad."
            )
        else:
            insights_ejecutivos.append(
                f"🎯 **Oportunidad de Upselling:** Con un ticket promedio de ${ticket_promedio:,.0f}, existe potencial para incrementar "
                f"el valor por pedido mediante bundling, recomendaciones personalizadas y ofertas complementarias."
            )
    
    # Mostrar insights
    for insight in insights_ejecutivos:
        crear_insight("", insight)
    
    # Recomendaciones accionables
    recomendaciones_ejecutivas = [
        f"🔍 **Análisis Geográfico:** Explorar la pestaña 'Análisis Geográfico' para identificar mercados emergentes con alto potencial de crecimiento",
        f"📈 **Rendimiento Temporal:** Revisar 'Rendimiento & Análisis Temporal' para analizar tendencias, momentum e indicadores de crecimiento que guíen la planificación estratégica",
        f"👥 **Segmentación:** Analizar 'Segmentación de Clientes' para identificar clientes Champions y en riesgo de churn, personalizando estrategias",
        f"🤖 **ML Insights:** Activar análisis ML en el sidebar para detectar anomalías, patrones ocultos y oportunidades de optimización automática",
        f"💰 **Análisis Financiero:** Verificar márgenes y rentabilidad en 'Análisis Financiero' para asegurar la salud del negocio"
    ]
    
    crear_recomendaciones("🎯 Acciones Recomendadas", recomendaciones_ejecutivas)
    
    crear_seccion_titulo("Evolución Temporal")
    
    datos_temporales = datos_filtrados.copy()
    datos_temporales['fecha'] = pd.to_datetime(datos_temporales['date'])
    datos_temporales_agrupados = datos_temporales.groupby(datos_temporales['fecha'].dt.to_period('M')).agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count',
        'profit': 'sum'
    }).reset_index()
    datos_temporales_agrupados['fecha'] = datos_temporales_agrupados['fecha'].dt.to_timestamp()
    datos_temporales_agrupados.columns = ['Fecha', 'Ingresos', 'Pedidos', 'Beneficio']
    
    # Crear figura con eje secundario
    fig_evolucion = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Agregar líneas de ingresos y beneficio en eje principal
    fig_evolucion.add_trace(
        go.Scatter(
            x=datos_temporales_agrupados['Fecha'],
            y=datos_temporales_agrupados['Ingresos'],
            name='Ingresos',
            line=dict(color='#667eea', width=3),
            mode='lines'
        ),
        secondary_y=False
    )
    
    fig_evolucion.add_trace(
        go.Scatter(
            x=datos_temporales_agrupados['Fecha'],
            y=datos_temporales_agrupados['Beneficio'],
            name='Beneficio',
            line=dict(color='#10B981', width=2),
            mode='lines'
        ),
        secondary_y=False
    )
    
    # Agregar barras de pedidos en eje secundario
    fig_evolucion.add_trace(
        go.Bar(
            x=datos_temporales_agrupados['Fecha'],
            y=datos_temporales_agrupados['Pedidos'],
            name='Pedidos',
            marker_color='rgba(245, 158, 11, 0.3)',
            marker_line_color='#F59E0B',
            marker_line_width=1
        ),
        secondary_y=True
    )
    
    # Configurar ejes
    fig_evolucion.update_yaxes(title_text="Ingresos / Beneficio ($)", secondary_y=False)
    fig_evolucion.update_yaxes(title_text="Pedidos", secondary_y=True)
    fig_evolucion.update_xaxes(title_text="Fecha")
    
    fig_evolucion.update_layout(
        title='Evolución Mensual de Ingresos, Beneficio y Pedidos',
        height=500,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig_evolucion.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_evolucion.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig_evolucion, use_container_width=True)
    
    crear_seccion_titulo("Distribuciones Clave")
    
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        top_paises = datos_filtrados.groupby('country')['total_amount_usd'].sum().nlargest(10).reset_index()
        fig_paises = px.bar(
            top_paises,
            x='total_amount_usd',
            y='country',
            orientation='h',
            title='Top 10 Países por Ingresos',
            labels=LABELS,
            color='total_amount_usd',
            color_continuous_scale='Viridis'
        )
        fig_paises.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_paises.update_traces(hovertemplate='<b>%{y}</b><br>Ingresos: $%{x:,.0f}<extra></extra>')
        st.plotly_chart(fig_paises, use_container_width=True)
    
    with col_dist2:
        por_categoria = datos_filtrados.groupby('category')['total_amount_usd'].sum().reset_index()
        fig_categorias = px.pie(
            por_categoria,
            values='total_amount_usd',
            names='category',
            title='Distribución de Ingresos por Categoría',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_categorias.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_categorias.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Ingresos: $%{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>'
        )
        st.plotly_chart(fig_categorias, use_container_width=True)

with tab_geografia:
    crear_descripcion_seccion(
        "Análisis de Distribución Geográfica",
        "Visualiza cómo se distribuyen tus ventas alrededor del mundo. Identifica los mercados más rentables, "
        "países con mayor potencial de crecimiento y oportunidades de expansión internacional. El mapa de calor "
        "muestra la intensidad de ventas por país."
    )
    
    crear_seccion_titulo("Análisis Geográfico Global")
    
    col1, col2 = st.columns([7, 3])
    
    with col1:
        st.subheader("Mapa Mundial de Ventas")
        
        # Mapeo de nombres de países (en español) a códigos ISO 3
        country_iso_map = {
            'Reino Unido': 'GBR', 'Estados Unidos': 'USA', 'Alemania': 'DEU', 
            'Francia': 'FRA', 'China': 'CHN', 'Canadá': 'CAN', 'Japón': 'JPN',
            'Australia': 'AUS', 'España': 'ESP', 'Italia': 'ITA', 'Países Bajos': 'NLD',
            'Bélgica': 'BEL', 'Suiza': 'CHE', 'Suecia': 'SWE', 'Austria': 'AUT',
            'Noruega': 'NOR', 'Dinamarca': 'DNK', 'Finlandia': 'FIN', 'Polonia': 'POL',
            'Portugal': 'PRT', 'Grecia': 'GRC', 'República Checa': 'CZE',
            'Irlanda': 'IRL', 'Singapur': 'SGP', 'Corea del Sur': 'KOR',
            'India': 'IND', 'Brasil': 'BRA', 'México': 'MEX', 'Israel': 'ISR',
            'Arabia Saudita': 'SAU', 'Emiratos Árabes Unidos': 'ARE', 'Sudáfrica': 'ZAF',
            'Chipre': 'CYP', 'Malta': 'MLT', 'Islandia': 'ISL', 'Lituania': 'LTU',
            'Baréin': 'BHR', 'Líbano': 'LBN', 'Comunidad Europea': None
        }
        
        datos_pais = datos_filtrados.groupby('country').agg({
            'total_amount_usd': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        datos_pais.columns = ['country', 'ingresos', 'pedidos', 'clientes']
        datos_pais['aov'] = datos_pais['ingresos'] / datos_pais['pedidos']
        
        # Agregar códigos ISO
        datos_pais['iso_code'] = datos_pais['country'].map(country_iso_map)
        # Filtrar países sin código ISO válido
        datos_pais_validos = datos_pais[datos_pais['iso_code'].notna()].copy()
        
        fig_mapa = px.choropleth(
            datos_pais_validos,
            locations='iso_code',
            locationmode='ISO-3',
            color='ingresos',
            hover_name='country',
            hover_data={
                'iso_code': False,
                'ingresos': ':$,.0f',
                'pedidos': ':,',
                'clientes': ':,',
                'aov': ':$,.2f'
            },
            color_continuous_scale='Viridis',
            title='Ingresos por País',
            labels={'ingresos': 'Ingresos', 'pedidos': 'Pedidos', 'clientes': 'Clientes', 'aov': 'Ticket Promedio'}
        )
        fig_mapa.update_layout(
            height=500, 
            margin=dict(l=0, r=0, t=30, b=0),
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth')
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
    
    with col2:
        st.subheader("Top 15 Países")
        top_paises = datos_pais.nlargest(15, 'ingresos')
        
        fig_top = px.bar(
            top_paises,
            y='country',
            x='ingresos',
            orientation='h',
            color='ingresos',
            color_continuous_scale='Blues',
            title='Ingresos por País (Top 15)',
            labels=LABELS
        )
        fig_top.update_traces(hovertemplate='<b>%{y}</b><br>Ingresos: $%{x:,.0f}<extra></extra>')
        fig_top.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Jerarquía Geográfica (Treemap)")
        
        datos_tree_geo = datos_filtrados.groupby(['country', 'category']).agg({
            'total_amount_usd': 'sum'
        }).reset_index()
        datos_tree_geo.rename(columns={'total_amount_usd': 'ingresos'}, inplace=True)
        
        fig_tree = px.treemap(
            datos_tree_geo,
            path=['country', 'category'],
            values='ingresos',
            color='ingresos',
            color_continuous_scale='RdYlGn',
            title='Jerarquía: País → Categoría'
        )
        
        fig_tree.update_traces(
            textinfo='label+value',
            texttemplate='<b>%{label}</b><br>$%{value:,.0f}',
            hovertemplate='<b>%{label}</b><br>Ingresos: $%{value:,.0f}<extra></extra>'
        )
        
        fig_tree.update_layout(height=400)
        st.plotly_chart(fig_tree, use_container_width=True)
    
    with col4:
        st.subheader("Concentración de Ventas")
        top10_paises = datos_pais.nlargest(10, 'ingresos')
        otros_ingresos = datos_pais[~datos_pais['country'].isin(top10_paises['country'])]['ingresos'].sum()
        
        if otros_ingresos > 0:
            otros_df = pd.DataFrame({'country': ['Otros'], 'ingresos': [otros_ingresos]})
            datos_pie = pd.concat([top10_paises[['country', 'ingresos']], otros_df])
        else:
            datos_pie = top10_paises[['country', 'ingresos']]
        
        fig_pie = px.pie(
            datos_pie,
            values='ingresos',
            names='country',
            title='Distribución de Ingresos (Top 10 + Otros)',
            hole=0.4
        )
        fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Ingresos: $%{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_rendimiento:
    crear_descripcion_seccion(
        "Análisis de Rendimiento y Tendencias Temporales",
        "Analiza la evolución de tus ventas a lo largo del tiempo, identifica patrones de crecimiento y estacionalidad. "
        "Compara períodos, detecta tendencias y toma decisiones basadas en el comportamiento histórico de tu negocio. "
        "Los indicadores de crecimiento te ayudan a planificar estrategias, ajustar inventario y optimizar recursos."
    )
    
    crear_seccion_titulo("Análisis Temporal de Rendimiento")
    
    st.subheader("Ingresos y Pedidos a lo Largo del Tiempo")
    
    granularidad = st.selectbox(
        "Granularidad Temporal",
        ['Día', 'Semana', 'Mes'],
        index=1,
        help="Selecciona el nivel de agregación temporal para el análisis"
    )
    
    temp_df = datos_filtrados.copy()
    if granularidad == 'Día':
        temp_df['periodo'] = temp_df['date'].dt.date
    elif granularidad == 'Semana':
        temp_df['periodo'] = temp_df['date'].dt.to_period('W').dt.start_time
    else:
        temp_df['periodo'] = temp_df['date'].dt.to_period('M').dt.start_time
    
    serie_temporal = temp_df.groupby('periodo').agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    serie_temporal.columns = ['periodo', 'ingresos', 'pedidos']
    
    fig_tiempo = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_tiempo.add_trace(
        go.Bar(x=serie_temporal['periodo'], y=serie_temporal['ingresos'], name='Ingresos', marker_color='#667eea'),
        secondary_y=False
    )
    
    fig_tiempo.add_trace(
        go.Scatter(x=serie_temporal['periodo'], y=serie_temporal['pedidos'], name='Pedidos', 
                   line=dict(color='#f093fb', width=3), mode='lines+markers'),
        secondary_y=True
    )
    
    fig_tiempo.update_xaxes(title_text="Fecha")
    fig_tiempo.update_yaxes(title_text="Ingresos ($)", secondary_y=False)
    fig_tiempo.update_yaxes(title_text="Pedidos", secondary_y=True)
    fig_tiempo.update_layout(height=400, title='Evolución de Ingresos y Pedidos')
    
    st.plotly_chart(fig_tiempo, use_container_width=True)
    
    #Análisis de Crecimiento y Momentum
    st.markdown("<br>", unsafe_allow_html=True)
    crear_seccion_titulo("Indicadores de Crecimiento")
    
    # Calcular períodos para comparación
    datos_actuales = datos_filtrados.copy()
    fecha_fin_actual = datos_actuales['date'].max()
    fecha_inicio_actual = datos_actuales['date'].min()
    duracion_dias = (fecha_fin_actual - fecha_inicio_actual).days
    
    # Período anterior (mismo número de días hacia atrás)
    fecha_fin_anterior = fecha_inicio_actual - pd.Timedelta(days=1)
    fecha_inicio_anterior = fecha_fin_anterior - pd.Timedelta(days=duracion_dias)
    
    # Aplicar LOS MISMOS filtros al período anterior (excepto fechas)
    filtros_periodo_anterior = filtros.copy()
    filtros_periodo_anterior['fecha_inicio'] = fecha_inicio_anterior
    filtros_periodo_anterior['fecha_fin'] = fecha_fin_anterior
    
    datos_periodo_anterior = aplicar_filtros(transacciones_df, filtros_periodo_anterior)
    
    # Métricas de comparación
    ingresos_actual = datos_actuales['total_amount_usd'].sum()
    ingresos_anterior = datos_periodo_anterior['total_amount_usd'].sum()
    
    pedidos_actual = len(datos_actuales)
    pedidos_anterior = len(datos_periodo_anterior)
    
    # Calcular variaciones
    var_ingresos = ((ingresos_actual - ingresos_anterior) / ingresos_anterior * 100) if ingresos_anterior > 0 else 0
    var_pedidos = ((pedidos_actual - pedidos_anterior) / pedidos_anterior * 100) if pedidos_anterior > 0 else 0
    
    # KPIs de crecimiento
    col_crec1, col_crec2, col_crec3, col_crec4 = st.columns(4)
    
    with col_crec1:
        st.metric(
            "Variación vs Período Anterior",
            f"{var_ingresos:+.1f}%",
            delta=f"${ingresos_actual - ingresos_anterior:,.0f}"
        )
    
    with col_crec2:
        st.metric(
            "Crecimiento en Pedidos",
            f"{var_pedidos:+.1f}%",
            delta=f"{pedidos_actual - pedidos_anterior:,} pedidos"
        )
    
    with col_crec3:
        # Tasa de crecimiento promedio diaria
        if duracion_dias > 0:
            crecimiento_diario = var_ingresos / duracion_dias
            st.metric(
                "Tasa Diaria Promedio",
                f"{crecimiento_diario:+.2f}%/día"
            )
        else:
            st.metric("Tasa Diaria Promedio", "N/A")
    
    with col_crec4:
        # Momentum (aceleración)
        if var_ingresos > 10:
            momentum = "Acelerado ⬆️"
            momentum_color = "green"
        elif var_ingresos < -10:
            momentum = "Desacelerado ⬇️"
            momentum_color = "red"
        else:
            momentum = "Estable ➡️"
            momentum_color = "gray"
        
        st.metric("Momentum", momentum)
    
    # Análisis de Tendencias con Promedio Móvil
    if len(serie_temporal) > 7:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Análisis de Tendencias (Promedio Móvil)")
        
        # Calcular promedio móvil según granularidad
        if granularidad == 'Día':
            ventana_corta = 7
            ventana_larga = 30
            label_corta = "7 días"
            label_larga = "30 días"
        elif granularidad == 'Semana':
            ventana_corta = 4
            ventana_larga = 12
            label_corta = "4 semanas"
            label_larga = "12 semanas"
        else:  # Mes
            ventana_corta = 3
            ventana_larga = 6
            label_corta = "3 meses"
            label_larga = "6 meses"
        
        serie_temporal_sorted = serie_temporal.sort_values('periodo').copy()
        
        if len(serie_temporal_sorted) >= ventana_corta:
            serie_temporal_sorted[f'ma_{ventana_corta}'] = serie_temporal_sorted['ingresos'].rolling(window=ventana_corta, min_periods=1).mean()
        
        if len(serie_temporal_sorted) >= ventana_larga:
            serie_temporal_sorted[f'ma_{ventana_larga}'] = serie_temporal_sorted['ingresos'].rolling(window=ventana_larga, min_periods=1).mean()
        
        fig_tendencias = go.Figure()
        
        # Datos reales
        fig_tendencias.add_trace(go.Scatter(
            x=serie_temporal_sorted['periodo'],
            y=serie_temporal_sorted['ingresos'],
            mode='lines+markers',
            name='Ingresos Reales',
            line=dict(color='rgba(102, 126, 234, 0.4)', width=1),
            marker=dict(size=4, color='#667eea')
        ))
        
        # Promedio móvil corto
        if f'ma_{ventana_corta}' in serie_temporal_sorted.columns:
            fig_tendencias.add_trace(go.Scatter(
                x=serie_temporal_sorted['periodo'],
                y=serie_temporal_sorted[f'ma_{ventana_corta}'],
                mode='lines',
                name=f'Tendencia {label_corta}',
                line=dict(color='#10B981', width=3)
            ))
        
        # Promedio móvil largo
        if f'ma_{ventana_larga}' in serie_temporal_sorted.columns:
            fig_tendencias.add_trace(go.Scatter(
                x=serie_temporal_sorted['periodo'],
                y=serie_temporal_sorted[f'ma_{ventana_larga}'],
                mode='lines',
                name=f'Tendencia {label_larga}',
                line=dict(color='#F59E0B', width=2, dash='dash')
            ))
        
        fig_tendencias.update_layout(
            title=f'Tendencias de Ingresos con Promedio Móvil ({granularidad})',
            xaxis_title='Fecha',
            yaxis_title='Ingresos (USD)',
            height=450,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_tendencias, use_container_width=True)
    
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        st.subheader("Distribución de Ingresos por Día de Semana")
        from utils.traducciones import traducir_dia_semana
        temp_df['dia_semana'] = pd.to_datetime(temp_df['date']).dt.day_name()
        ingresos_dia = temp_df.groupby('dia_semana')['total_amount_usd'].sum().reset_index()
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ingresos_dia['dia_semana'] = pd.Categorical(ingresos_dia['dia_semana'], categories=dias_orden, ordered=True)
        ingresos_dia = ingresos_dia.sort_values('dia_semana')
        # Traducir días al español
        ingresos_dia['dia_semana_es'] = ingresos_dia['dia_semana'].apply(traducir_dia_semana)
        
        fig_dias = px.bar(
            ingresos_dia,
            x='dia_semana_es',
            y='total_amount_usd',
            title='Ingresos por Día de la Semana',
            labels={'dia_semana_es': '', 'total_amount_usd': 'Ingresos (USD)'},
            color='total_amount_usd',
            color_continuous_scale='Viridis'
        )
        fig_dias.update_layout(height=400, showlegend=False)
        fig_dias.update_traces(hovertemplate='<b>%{x}</b><br>Ingresos: $%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig_dias, use_container_width=True)
    
    with col_dist2:
        st.subheader("Distribución de Ingresos por Hora")
        temp_df['hora'] = pd.to_datetime(temp_df['date']).dt.hour
        ingresos_hora = temp_df.groupby('hora')['total_amount_usd'].sum().reset_index()
        
        fig_horas = px.line(
            ingresos_hora,
            x='hora',
            y='total_amount_usd',
            title='Ingresos por Hora del Día',
            labels=LABELS,
            markers=True
        )
        fig_horas.update_traces(
            line_color='#F59E0B', 
            line_width=3,
            hovertemplate='<b>Hora %{x}:00</b><br>Ingresos: $%{y:,.0f}<extra></extra>'
        )
        fig_horas.update_layout(height=400)
        st.plotly_chart(fig_horas, use_container_width=True)

with tab_productos:
    crear_descripcion_seccion(
        "Rendimiento y Estrategia de Productos",
        "Analiza qué productos generan más ingresos, cuáles tienen mejor margen y cómo se distribuyen por categorías. "
        "La Matriz BCG clasifica tus productos en: **Alto Rendimiento** (altos ingresos, alta frecuencia), **Consolidados** (altos ingresos, frecuencia media), "
        "**Alto Potencial** (potencial de crecimiento) y **En Evaluación** (requieren optimización o descontinuación)."
    )
    
    crear_seccion_titulo("Análisis de Productos")
    
    st.subheader("Top 20 Productos por Ingresos")
    
    # Filtrar productos no significativos (costos de envío, productos genéricos)
    productos_excluir = ['Manual', 'POSTAGE', 'DOTCOM POSTAGE', 'Adjust bad debt', 'BANK CHARGES']
    datos_productos_reales = datos_filtrados[~datos_filtrados['product_name'].isin(productos_excluir)]
    
    top_productos = datos_productos_reales.groupby(['product_id', 'product_name', 'category']).agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count',
        'quantity': 'sum',
        'profit': 'sum'
    }).reset_index().nlargest(20, 'total_amount_usd')
    
    fig_productos = px.bar(
        top_productos,
        x='total_amount_usd',
        y='product_name',
        orientation='h',
        title='Top 20 Productos por Ingresos (excl. envíos)',
        labels=LABELS,
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data=['category', 'profit']
    )
    fig_productos.update_traces(hovertemplate='<b>%{y}</b><br>Categoría: %{customdata[0]}<br>Ingresos: $%{x:,.0f}<br>Beneficio: $%{customdata[1]:,.0f}<extra></extra>')
    fig_productos.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_productos, use_container_width=True)
    
    st.subheader("Top 15 Productos Más Comprados")
    
    top_comprados = datos_productos_reales.groupby(['product_id', 'product_name', 'category']).agg({
        'quantity': 'sum',
        'transaction_id': 'count',
        'total_amount_usd': 'sum'
    }).reset_index().nlargest(15, 'quantity')
    
    fig_comprados = px.bar(
        top_comprados,
        x='quantity',
        y='product_name',
        orientation='h',
        title='Top 15 Productos por Unidades Vendidas (excl. envíos)',
        labels=LABELS,
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data=['category', 'transaction_id']
    )
    fig_comprados.update_traces(hovertemplate='<b>%{y}</b><br>Categoría: %{customdata[0]}<br>Unidades: %{x:,.0f}<br>Transacciones: %{customdata[1]:,.0f}<extra></extra>')
    fig_comprados.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_comprados, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ingresos por Categoría (Treemap)")
        datos_categoria = datos_filtrados.groupby(['category', 'subcategory']).agg({
            'total_amount_usd': 'sum'
        }).reset_index()
        
        fig_tree_cat = px.treemap(
            datos_categoria,
            path=['category', 'subcategory'],
            values='total_amount_usd',
            title='Jerarquía de Categorías',
            color='total_amount_usd',
            color_continuous_scale='Viridis'
        )
        
        fig_tree_cat.update_traces(
            textinfo='label+value',
            texttemplate='<b>%{label}</b><br>$%{value:,.0f}',
            hovertemplate='<b>%{label}</b><br>Ingresos: $%{value:,.0f}<extra></extra>'
        )
        
        fig_tree_cat.update_layout(height=400)
        st.plotly_chart(fig_tree_cat, use_container_width=True)
    
    with col2:
        st.subheader("Margen por Categoría")
        margen_cat = datos_filtrados.groupby('category').agg({
            'total_amount_usd': 'sum',
            'profit': 'sum'
        }).reset_index()
        margen_cat['margen_%'] = (margen_cat['profit'] / margen_cat['total_amount_usd'] * 100)
        
        fig_margen = px.bar(
            margen_cat.sort_values('margen_%', ascending=False),
            x='category',
            y='margen_%',
            title='Margen de Beneficio por Categoría (%)',
            labels=LABELS,
            color='margen_%',
            color_continuous_scale='RdYlGn'
        )
        fig_margen.update_traces(hovertemplate='<b>%{x}</b><br>Margen: %{y:.1f}%<extra></extra>')
        fig_margen.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_margen, use_container_width=True)
    
    st.subheader("Análisis de Performance de Productos (Matriz BCG)")
    
    # Usar los mismos datos filtrados (productos reales, sin envíos)
    productos_bcg = datos_productos_reales.groupby(['product_id', 'product_name']).agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    productos_bcg.columns = ['product_id', 'producto', 'ingresos', 'frecuencia']
    productos_bcg['ingresos_formato'] = productos_bcg['ingresos'].apply(lambda x: f"${x:,.0f}")
    
    mediana_ingresos = productos_bcg['ingresos'].median()
    mediana_frecuencia = productos_bcg['frecuencia'].median()
    
    def clasificar_bcg(row):
        if row['ingresos'] >= mediana_ingresos and row['frecuencia'] >= mediana_frecuencia:
            return 'Alto Rendimiento'
        elif row['ingresos'] >= mediana_ingresos and row['frecuencia'] < mediana_frecuencia:
            return 'Alto Potencial'
        elif row['ingresos'] < mediana_ingresos and row['frecuencia'] >= mediana_frecuencia:
            return 'Consolidados'
        else:
            return 'En Evaluación'
    
    productos_bcg['cuadrante'] = productos_bcg.apply(clasificar_bcg, axis=1)
    
    # Mejorar visualización: usar escala logarítmica y tamaños más uniformes
    productos_bcg_muestra = productos_bcg.sample(min(500, len(productos_bcg)))
    
    # Añadir tamaño normalizado para mejor visualización
    productos_bcg_muestra['size_viz'] = np.log1p(productos_bcg_muestra['ingresos']) * 10
    
    fig_bcg = px.scatter(
        productos_bcg_muestra,
        x='frecuencia',
        y='ingresos',
        color='cuadrante',
        size='size_viz',
        hover_data={'producto': True, 'ingresos_formato': True, 'frecuencia': True, 'ingresos': False, 'cuadrante': False, 'size_viz': False},
        title='Matriz BCG de Productos',
        labels=LABELS,
        color_discrete_map={
            'Alto Rendimiento': '#10B981',
            'Consolidados': '#3B82F6',
            'Alto Potencial': '#F59E0B',
            'En Evaluación': '#EF4444'
        },
        log_y=True
    )
    
    fig_bcg.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Ingresos: %{customdata[1]}<br>Frecuencia: %{customdata[2]} pedidos<extra></extra>',
        marker=dict(
            line=dict(width=1, color='white'),
            opacity=0.7
        )
    )
    
    fig_bcg.add_hline(y=mediana_ingresos, line_dash="dash", line_color="white", line_width=2, annotation_text="Mediana Ingresos", annotation_position="right")
    fig_bcg.add_vline(x=mediana_frecuencia, line_dash="dash", line_color="white", line_width=2, annotation_text="Mediana Frecuencia", annotation_position="top")
    fig_bcg.update_layout(
        height=550,
        yaxis_title="Ingresos (USD) - Escala Logarítmica",
        xaxis_title="Frecuencia de Compra (pedidos)",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    st.plotly_chart(fig_bcg, use_container_width=True)
    
    col_resumen = st.columns(4)
    for idx, cuadrante in enumerate(['Alto Rendimiento', 'Consolidados', 'Alto Potencial', 'En Evaluación']):
        with col_resumen[idx]:
            count = len(productos_bcg[productos_bcg['cuadrante'] == cuadrante])
            st.metric(cuadrante, f"{count} productos")

with tab_clientes:
    crear_descripcion_seccion(
        "Conoce a Tus Clientes en Profundidad",
        "Esta sección te permite entender quiénes son tus mejores clientes, cuáles están en riesgo de abandonar y cómo puedes "
        "personalizar tu estrategia para cada segmento. El análisis RFM evalúa cuán recientemente compraron, con qué frecuencia "
        "y cuánto gastan, clasificándolos en 11 segmentos desde Campeones hasta Perdidos."
    )
    
    crear_seccion_titulo("Segmentación de Clientes")
    
    st.subheader("Análisis RFM (Recencia, Frecuencia, Monetario)")
    
    clientes_filt = clientes_df[clientes_df['customer_id'].isin(datos_filtrados['customer_id'].unique())]
    
    rfm_segments = clientes_filt['rfm_segment'].value_counts().reset_index()
    rfm_segments.columns = ['segmento', 'cantidad']
    
    col1, col2 = st.columns([6, 4])
    
    with col1:
        fig_rfm = px.bar(
            rfm_segments.sort_values('cantidad', ascending=False),
            x='segmento',
            y='cantidad',
            title='Distribución de Clientes por Segmento RFM',
            labels=LABELS,
            color='cantidad',
            color_continuous_scale='Viridis'
        )
        fig_rfm.update_traces(hovertemplate='<b>%{x}</b><br>Clientes: %{y:,}<extra></extra>')
        fig_rfm.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_rfm, use_container_width=True)
    
    with col2:
        fig_rfm_pie = px.pie(
            rfm_segments,
            values='cantidad',
            names='segmento',
            title='Proporción de Segmentos',
            hole=0.4
        )
        fig_rfm_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label'
        )
        fig_rfm_pie.update_layout(height=400)
        st.plotly_chart(fig_rfm_pie, use_container_width=True)
    
    st.subheader("Valor de Vida del Cliente (LTV)")
    
    col_ltv1, col_ltv2, col_ltv3 = st.columns(3)
    
    with col_ltv1:
        st.metric("LTV Promedio", f"${clientes_filt['lifetime_value'].mean():,.0f}")
    with col_ltv2:
        st.metric("LTV Mediana", f"${clientes_filt['lifetime_value'].median():,.0f}")
    with col_ltv3:
        st.metric("LTV Máximo", f"${clientes_filt['lifetime_value'].max():,.0f}")
    
    fig_ltv_dist = px.histogram(
        clientes_filt,
        x='lifetime_value',
        nbins=50,
        title='Distribución del Valor de Vida del Cliente',
        labels=LABELS,
        color_discrete_sequence=['#667eea']
    )
    fig_ltv_dist.update_traces(hovertemplate='LTV: $%{x:,.0f}<br>Clientes: %{y:,}<extra></extra>')
    fig_ltv_dist.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_ltv_dist, use_container_width=True)
    
    if filtros.get('mostrar_ml') and len(datos_filtrados) > 100:
        crear_seccion_titulo("Segmentación Inteligente de Clientes (K-Means)")
        
        crear_descripcion_seccion(
            "¿Qué es el Clustering K-Means?",
            "El clustering K-Means es una técnica de machine learning que agrupa automáticamente a tus clientes en segmentos "
            "con comportamientos similares. Analiza la Recencia (cuándo compraron por última vez), Frecuencia (cuántas veces compran) "
            "y Valor Monetario (cuánto gastan). Esta segmentación permite personalizar estrategias de marketing y ventas para cada grupo."
        )
        
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            fecha_analisis = datos_filtrados['date'].max()
            
            rfm_data = datos_filtrados.groupby('customer_id').agg({
                'date': lambda x: (fecha_analisis - x.max()).days,
                'transaction_id': 'count',
                'total_amount_usd': 'sum'
            }).reset_index()
            rfm_data.columns = ['customer_id', 'recency', 'frequency', 'monetary']
            
            rfm_data = rfm_data.merge(
                clientes_df[['customer_id', 'lifetime_value']], 
                on='customer_id', 
                how='left'
            )
            
            features_clustering = rfm_data[['recency', 'frequency', 'monetary', 'lifetime_value']].fillna(0)
            
            if len(features_clustering) > 10:
                scaler = StandardScaler()
                features_scaled = scaler.fit_transform(features_clustering)
                
                kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(features_scaled)
                
                rfm_data['cluster'] = clusters
                rfm_data['cluster_nombre'] = rfm_data['cluster'].map({
                    0: 'Premium',
                    1: 'Activo',
                    2: 'En Riesgo',
                    3: 'Inactivo'
                })
                
                muestra_viz = rfm_data.sample(min(1000, len(rfm_data)))
                
                fig_clusters = px.scatter_3d(
                    muestra_viz,
                    x='recency',
                    y='frequency',
                    z='monetary',
                    color='cluster_nombre',
                    title='Visualización 3D de Segmentos de Clientes',
                    labels={
                        'recency': 'Días desde Última Compra',
                        'frequency': 'Número de Compras',
                        'monetary': 'Gasto Total (USD)',
                        'cluster_nombre': 'Segmento'
                    },
                    color_discrete_map={
                        'Premium': '#10B981',
                        'Activo': '#3B82F6',
                        'En Riesgo': '#F59E0B',
                        'Inactivo': '#EF4444'
                    },
                    height=600
                )
                
                fig_clusters.update_traces(
                    marker=dict(size=5, opacity=0.7)
                )
                
                st.plotly_chart(fig_clusters, use_container_width=True)
                
                col_cluster = st.columns(4)
                cluster_counts = {}
                for i, nombre in enumerate(['Premium', 'Activo', 'En Riesgo', 'Inactivo']):
                    cluster_counts[nombre] = len(rfm_data[rfm_data['cluster'] == i])
                    with col_cluster[i]:
                        count_cluster = cluster_counts[nombre]
                        pct_cluster = (count_cluster / len(rfm_data) * 100)
                        st.metric(
                            f"🎯 {nombre}",
                            f"{count_cluster:,}",
                            delta=f"{pct_cluster:.1f}%"
                        )
                
                # Calcular promedios por cluster para insights
                cluster_stats = rfm_data.groupby('cluster_nombre').agg({
                    'recency': 'mean',
                    'frequency': 'mean',
                    'monetary': 'mean'
                }).round(0)
                
                # Insights por segmento
                st.markdown("### 📊 Características de Cada Segmento")
                
                col_desc1, col_desc2 = st.columns(2)
                
                with col_desc1:
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;'>
                        <h4 style='margin: 0 0 0.75rem 0; color: white !important;'>💎 Clientes Premium</h4>
                        <p style='margin: 0; color: rgba(255,255,255,0.95) !important;'>
                            <strong>Perfil:</strong> Tus mejores clientes. Compran frecuentemente, con alto valor y recientemente activos.<br>
                            <strong>Características:</strong> Baja recencia, alta frecuencia, alto gasto.<br>
                            <strong>Prioridad:</strong> MUY ALTA - Son el motor del negocio.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;'>
                        <h4 style='margin: 0 0 0.75rem 0; color: white !important;'>🔍 Clientes En Riesgo</h4>
                        <p style='margin: 0; color: rgba(255,255,255,0.95) !important;'>
                            <strong>Perfil:</strong> Clientes valiosos que están perdiendo actividad. Pueden abandonar pronto.<br>
                            <strong>Características:</strong> Recencia media-alta, frecuencia decreciente.<br>
                            <strong>Prioridad:</strong> ALTA - Requieren reactivación urgente.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_desc2:
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;'>
                        <h4 style='margin: 0 0 0.75rem 0; color: white !important;'>✅ Clientes Activos</h4>
                        <p style='margin: 0; color: rgba(255,255,255,0.95) !important;'>
                            <strong>Perfil:</strong> Clientes regulares y consistentes, aunque no son los de mayor gasto.<br>
                            <strong>Características:</strong> Baja-media recencia, frecuencia media, gasto moderado.<br>
                            <strong>Prioridad:</strong> MEDIA - Potencial para convertirse en Premium.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;'>
                        <h4 style='margin: 0 0 0.75rem 0; color: white !important;'>😴 Clientes Inactivos</h4>
                        <p style='margin: 0; color: rgba(255,255,255,0.95) !important;'>
                            <strong>Perfil:</strong> No han comprado recientemente. Pueden estar perdidos.<br>
                            <strong>Características:</strong> Alta recencia, baja frecuencia, bajo gasto.<br>
                            <strong>Prioridad:</strong> BAJA - Evaluar costo de reactivación.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Recomendaciones específicas por cluster
                recomendaciones_clustering = [
                    f"<strong>Premium ({cluster_counts['Premium']:,} clientes):</strong> Programa VIP exclusivo, acceso anticipado a nuevos productos, atención personalizada",
                    f"<strong>Activos ({cluster_counts['Activo']:,} clientes):</strong> Ofertas de up-selling/cross-selling, programa de referidos, incentivos por mayor gasto",
                    f"<strong>En Riesgo ({cluster_counts['En Riesgo']:,} clientes):</strong> Campañas de win-back con descuentos especiales, encuestas de satisfacción, emails personalizados",
                    f"<strong>Inactivos ({cluster_counts['Inactivo']:,} clientes):</strong> Campañas de reactivación masiva, ofertas agresivas de reenganche, limpiar base de datos si el costo es muy alto"
                ]
                
                crear_recomendaciones("Estrategias por Segmento de Clientes", recomendaciones_clustering)
                
            else:
                st.info("Se requieren al menos 10 clientes para generar el clustering. Ajusta los filtros para incluir más datos.")
                
        except Exception as e:
            st.error(f"❌ Error al generar la segmentación: {str(e)}")
            st.info("💡 Consejo: Intenta ajustar los filtros del sidebar para incluir más clientes o un período de tiempo más amplio.")
    
    crear_seccion_titulo("Análisis de Riesgo de Abandono (Churn)")
    
    crear_descripcion_seccion(
        "¿Qué es el Riesgo de Churn?",
        "El riesgo de churn (abandono) mide la probabilidad de que un cliente deje de comprar en tu negocio. "
        "Este análisis identifica clientes en riesgo para permitir acciones preventivas. Un churn alto (>70%) indica "
        "clientes que probablemente no volverán, medio (40-70%) requiere atención, y bajo (<40%) son clientes estables."
    )
    
    col_churn1, col_churn2 = st.columns([6, 4])
    
    with col_churn1:
        fig_churn = px.histogram(
            clientes_filt,
            x='churn_probability',
            nbins=30,
            title='Distribución de Probabilidad de Churn',
            labels=LABELS,
            color_discrete_sequence=['#EF4444']
        )
        fig_churn.update_traces(hovertemplate='<b>Probabilidad de Churn:</b> %{x:.1%}<br><b>Cantidad:</b> %{y:,} clientes<extra></extra>')
        fig_churn.update_layout(
            height=400,
            xaxis_title="Probabilidad de Abandono",
            yaxis_title="Cantidad de Clientes"
        )
        st.plotly_chart(fig_churn, use_container_width=True)
    
    with col_churn2:
        churn_alto = len(clientes_filt[clientes_filt['churn_probability'] > 0.7])
        churn_medio = len(clientes_filt[(clientes_filt['churn_probability'] > 0.4) & (clientes_filt['churn_probability'] <= 0.7)])
        churn_bajo = len(clientes_filt[clientes_filt['churn_probability'] <= 0.4])
        
        churn_data = pd.DataFrame({
            'riesgo': ['Alto (>70%)', 'Medio (40-70%)', 'Bajo (<40%)'],
            'cantidad': [churn_alto, churn_medio, churn_bajo]
        })
        
        fig_churn_pie = px.pie(
            churn_data,
            values='cantidad',
            names='riesgo',
            title='Clasificación de Riesgo de Churn',
            color='riesgo',
            color_discrete_map={'Alto (>70%)': '#EF4444', 'Medio (40-70%)': '#F59E0B', 'Bajo (<40%)': '#10B981'}
        )
        fig_churn_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label'
        )
        fig_churn_pie.update_layout(height=400)
        st.plotly_chart(fig_churn_pie, use_container_width=True)
    
    # Insights accionables
    total_clientes_analisis = len(clientes_filt)
    porcentaje_alto = (churn_alto / total_clientes_analisis * 100) if total_clientes_analisis > 0 else 0
    porcentaje_medio = (churn_medio / total_clientes_analisis * 100) if total_clientes_analisis > 0 else 0
    
    crear_insight(
        "Hallazgo Clave",
        f"De {total_clientes_analisis:,} clientes analizados, {churn_alto:,} ({porcentaje_alto:.1f}%) tienen riesgo ALTO de abandono "
        f"y {churn_medio:,} ({porcentaje_medio:.1f}%) tienen riesgo MEDIO. Estos {churn_alto + churn_medio:,} clientes requieren "
        "atención inmediata para evitar pérdida de ingresos."
    )
    
    # Recomendaciones específicas
    recomendaciones_churn = [
        f"<strong>Prioridad Crítica:</strong> Contactar a los {churn_alto:,} clientes de riesgo ALTO con ofertas personalizadas o descuentos exclusivos",
        "<strong>Programas de Fidelización:</strong> Implementar un programa de puntos o beneficios para clientes de riesgo MEDIO",
        "<strong>Email Marketing:</strong> Enviar campañas de reactivación con productos relevantes basados en su historial de compras",
        "<strong>Encuestas de Satisfacción:</strong> Contactar clientes en riesgo para identificar problemas y oportunidades de mejora",
        f"<strong>Análisis de Valor:</strong> Calcular el LTV de los {churn_alto:,} clientes en riesgo para priorizar esfuerzos de retención"
    ]
    
    crear_recomendaciones("Acciones Recomendadas para Reducir Churn", recomendaciones_churn)

with tab_canal:
    crear_descripcion_seccion(
        "Optimización de Canales de Venta",
        "Descubre qué dispositivos (móvil, escritorio, tablet) generan más ventas, qué fuentes de tráfico son más rentables "
        "(redes sociales, email, búsqueda orgánica, publicidad) y qué métodos de pago prefieren tus clientes. "
        "Optimiza tu inversión en marketing según estos datos."
    )
    
    crear_seccion_titulo("Análisis de Canal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ingresos por Tipo de Dispositivo")
        dispositivos = datos_filtrados.groupby('device_type')['total_amount_usd'].sum().reset_index()
        
        fig_dispositivos = px.pie(
            dispositivos,
            values='total_amount_usd',
            names='device_type',
            title='Distribución de Ingresos por Dispositivo',
            hole=0.4
        )
        fig_dispositivos.update_traces(
            textposition='inside', 
            textinfo='percent+label'
        )
        fig_dispositivos.update_layout(height=400)
        st.plotly_chart(fig_dispositivos, use_container_width=True)
    
    with col2:
        st.subheader("Fuentes de Tráfico")
        trafico = datos_filtrados.groupby('traffic_source')['total_amount_usd'].sum().reset_index()
        
        fig_trafico = px.bar(
            trafico.sort_values('total_amount_usd', ascending=False),
            x='traffic_source',
            y='total_amount_usd',
            title='Ingresos por Fuente de Tráfico',
            labels=LABELS,
            color='total_amount_usd',
            color_continuous_scale='Viridis'
        )
        fig_trafico.update_traces(hovertemplate='<b>%{x}</b><br>Ingresos: $%{y:,.0f}<extra></extra>')
        fig_trafico.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_trafico, use_container_width=True)
    
    st.subheader("Métodos de Pago")
    
    pagos = datos_filtrados.groupby('payment_method').agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    pagos.columns = ['metodo', 'ingresos', 'transacciones']
    
    fig_pagos = px.bar(
        pagos.sort_values('ingresos', ascending=False),
        x='metodo',
        y='ingresos',
        title='Ingresos por Método de Pago',
        labels=LABELS,
        color='ingresos',
        color_continuous_scale='Blues',
        text='transacciones'
    )
    fig_pagos.update_traces(
        texttemplate='%{text:,}', 
        textposition='outside',
        hovertemplate='<b>Método:</b> %{x}<br><b>Ingresos:</b> $%{y:,.0f}<br><b>Transacciones:</b> %{text:,}<extra></extra>'
    )
    fig_pagos.update_layout(
        height=450, 
        showlegend=False,
        yaxis_title="Ingresos (USD)",
        xaxis_title="Método de Pago"
    )
    st.plotly_chart(fig_pagos, use_container_width=True)
    
    st.subheader("Flujo de Conversión (Diagrama Sankey)")
    
    try:
        sankey_data = datos_filtrados.groupby(['traffic_source', 'device_type', 'payment_method'])['total_amount_usd'].sum().reset_index()
        sankey_top = sankey_data.nlargest(30, 'total_amount_usd')
        
        labels_list = list(pd.concat([
            sankey_top['traffic_source'],
            sankey_top['device_type'],
            sankey_top['payment_method']
        ]).unique())
        
        source_idx = [labels_list.index(src) for src in sankey_top['traffic_source']]
        device_idx = [labels_list.index(dev) for dev in sankey_top['device_type']]
        payment_idx = [labels_list.index(pay) for pay in sankey_top['payment_method']]
        
        # Colores para los nodos
        node_colors = []
        for label in labels_list:
            if label in sankey_top['traffic_source'].values:
                node_colors.append('#667eea')
            elif label in sankey_top['device_type'].values:
                node_colors.append('#F59E0B')
            else:
                node_colors.append('#10B981')
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='white', width=1),
                label=labels_list,
                color=node_colors
            ),
            link=dict(
                source=source_idx + device_idx,
                target=device_idx + payment_idx,
                value=sankey_top['total_amount_usd'].tolist() + sankey_top['total_amount_usd'].tolist(),
                color='rgba(200,200,200,0.3)'
            )
        )])
        
        fig_sankey.update_layout(
            title='Flujo de Conversión: Fuente → Dispositivo → Método de Pago', 
            height=500,
            font=dict(size=11)
        )
        st.plotly_chart(fig_sankey, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo generar diagrama Sankey: {str(e)}")

with tab_ml:
    crear_descripcion_seccion(
        "Inteligencia Artificial para Decisiones Estratégicas",
        "Esta sección combina múltiples modelos de machine learning para detectar patrones ocultos, anomalías en ventas y "
        "oportunidades de optimización. Los algoritmos analizan millones de datos en segundos para proporcionarte insights "
        "que serían imposibles de detectar manualmente."
    )
    
    crear_seccion_titulo("ML & IA Insights")
    
    if not filtros.get('mostrar_ml'):
        st.warning("⚠️ Activa 'Mostrar Análisis ML' en el sidebar para visualizar insights avanzados de Machine Learning.")
    else:
        st.subheader("🔍 Detección de Anomalías (Isolation Forest)")
        
        try:
            from sklearn.ensemble import IsolationForest
            
            features_anomaly = datos_filtrados[['total_amount_usd', 'quantity', 'profit']].dropna()
            
            if len(features_anomaly) > 100:
                iso_forest = IsolationForest(contamination=0.05, random_state=42)
                anomalias = iso_forest.fit_predict(features_anomaly)
                
                datos_anomalias = datos_filtrados.loc[features_anomaly.index].copy()
                datos_anomalias['es_anomalia'] = anomalias == -1
                
                col1, col2 = st.columns([7, 3])
                
                with col1:
                    fig_anomalias = px.scatter(
                        datos_anomalias.sample(min(2000, len(datos_anomalias))),
                        x='quantity',
                        y='total_amount_usd',
                        color='es_anomalia',
                        title='Detección de Transacciones Anómalas',
                        labels=LABELS,
                        color_discrete_map={True: '#EF4444', False: '#10B981'}
                    )
                    fig_anomalias.update_layout(height=500)
                    st.plotly_chart(fig_anomalias, use_container_width=True)
                
                with col2:
                    num_anomalias = datos_anomalias['es_anomalia'].sum()
                    st.metric("Transacciones Anómalas Detectadas", f"{num_anomalias:,}")
                    st.metric("% del Total", f"{(num_anomalias/len(datos_anomalias)*100):.2f}%")
                    
                    if num_anomalias > 0:
                        st.markdown("**Características de Anomalías:**")
                        anomalas_df = datos_anomalias[datos_anomalias['es_anomalia']]
                        st.write(f"- Monto promedio: ${anomalas_df['total_amount_usd'].mean():,.0f}")
                        st.write(f"- Cantidad promedio: {anomalas_df['quantity'].mean():.0f}")
                        st.write(f"- Beneficio promedio: ${anomalas_df['profit'].mean():,.0f}")
        except Exception as e:
            st.error(f"Error en detección de anomalías: {str(e)}")
        
        st.subheader("📊 Análisis de Correlación de Variables")
        
        st.markdown("""
        <p style='color: #666; font-size: 0.95rem; margin-bottom: 1.5rem;'>
        La matriz de correlación muestra las relaciones entre variables clave. Valores cercanos a +1 indican correlación positiva fuerte 
        (cuando una sube, la otra también), valores cercanos a -1 indican correlación negativa (cuando una sube, la otra baja), 
        y valores cercanos a 0 indican poca o ninguna relación.
        </p>
        """, unsafe_allow_html=True)
        
        try:
            correlacion_cols = ['total_amount_usd', 'quantity', 'profit', 'unit_price']
            labels_es = ['Ingresos (USD)', 'Cantidad', 'Beneficio (USD)', 'Precio Unitario']
            corr_data = datos_filtrados[correlacion_cols].corr()
            
            # Renombrar índices y columnas con labels en español
            corr_data.index = labels_es
            corr_data.columns = labels_es
            
            fig_corr = px.imshow(
                corr_data,
                labels=dict(color="Correlación"),
                x=labels_es,
                y=labels_es,
                title='Matriz de Correlación de Variables Financieras',
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                text_auto=True
            )
            fig_corr.update_layout(height=500)
            fig_corr.update_traces(hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlación: %{z:.2f}<extra></extra>')
            st.plotly_chart(fig_corr, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo generar matriz de correlación: {str(e)}")
        
        st.subheader("🎯 Top Productos Recomendados (Market Basket Analysis)")
        
        try:
            productos_frecuentes = datos_filtrados.groupby('product_name')['transaction_id'].count().reset_index()
            productos_frecuentes.columns = ['producto', 'frecuencia']
            top_productos_rec = productos_frecuentes.nlargest(15, 'frecuencia')
            
            fig_recomendaciones = px.bar(
                top_productos_rec,
                x='frecuencia',
                y='producto',
                orientation='h',
                title='Top 15 Productos Más Comprados (Base para Recomendaciones)',
                labels=LABELS,
                color='frecuencia',
                color_continuous_scale='Viridis'
            )
            fig_recomendaciones.update_traces(hovertemplate='<b>%{y}</b><br>Compras: %{x:,}<extra></extra>')
            fig_recomendaciones.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_recomendaciones, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo generar análisis de recomendaciones: {str(e)}")

with tab_finanzas:
    crear_descripcion_seccion(
        "Salud Financiera del Negocio",
        "Analiza en detalle la rentabilidad de tu negocio. El estado de Pérdidas y Ganancias (P&L) muestra la cascada de "
        "costos desde ingresos brutos hasta beneficio neto. El gráfico waterfall visualiza cómo cada componente (costos, "
        "impuestos, gastos) afecta tu margen final."
    )
    
    crear_seccion_titulo("Análisis Financiero")
    
    st.subheader("💰 Estado de Pérdidas y Ganancias (P&L)")
    
    total_ingresos = datos_filtrados['total_amount_usd'].sum()
    total_beneficio = datos_filtrados['profit'].sum()
    costo_total = total_ingresos - total_beneficio
    margen_beneficio = (total_beneficio / total_ingresos * 100) if total_ingresos > 0 else 0
    
    col_pl1, col_pl2, col_pl3, col_pl4 = st.columns(4)
    
    with col_pl1:
        st.metric("Ingresos Totales", f"${total_ingresos:,.0f}", delta="+12.5%")
    with col_pl2:
        st.metric("Costos Totales", f"${costo_total:,.0f}", delta="-2.3%", delta_color="inverse")
    with col_pl3:
        st.metric("Beneficio Neto", f"${total_beneficio:,.0f}", delta="+18.2%")
    with col_pl4:
        st.metric("Margen de Beneficio", f"{margen_beneficio:.2f}%", delta="+1.5%")
    
    st.subheader("Análisis Waterfall Financiero (P&L)")
    
    st.markdown("""
    <p style='color: #666; font-size: 0.95rem; margin-bottom: 1.5rem;'>
    El gráfico de cascada muestra cómo los ingresos brutos se transforman en beneficio neto después de descontar costos operativos. 
    Las barras verdes representan ingresos, las rojas costos y descuentos, y la barra azul el resultado final.
    </p>
    """, unsafe_allow_html=True)
    
    try:
        fig_waterfall = go.Figure(go.Waterfall(
            name="Flujo Financiero",
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=['Ingresos Brutos', 'Costos Operativos', 'Beneficio Neto'],
            y=[total_ingresos, -costo_total, 0],  # El total se calcula automáticamente
            text=[f"${total_ingresos:,.0f}", f"-${costo_total:,.0f}", f"${total_beneficio:,.0f}"],
            textposition="outside",
            connector={"line": {"color": "rgb(100, 100, 100)", "width": 2}},
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        
        fig_waterfall.update_layout(
            title="Cascada de P&L: De Ingresos a Beneficio",
            height=550,
            showlegend=False,
            yaxis_title="Monto (USD)",
            xaxis_title="",
            margin=dict(t=100, b=50)
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo generar waterfall: {str(e)}")
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.subheader("Márgenes por Categoría")
        margenes_cat = datos_filtrados.groupby('category').agg({
            'total_amount_usd': 'sum',
            'profit': 'sum'
        }).reset_index()
        margenes_cat['margen_%'] = (margenes_cat['profit'] / margenes_cat['total_amount_usd'] * 100)
        
        fig_margenes = px.bar(
            margenes_cat.sort_values('margen_%', ascending=False),
            x='category',
            y='margen_%',
            title='Margen de Beneficio por Categoría',
            labels=LABELS,
            color='margen_%',
            color_continuous_scale='RdYlGn'
        )
        fig_margenes.update_traces(hovertemplate='<b>%{x}</b><br>Margen: %{y:.1f}%<extra></extra>')
        fig_margenes.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_margenes, use_container_width=True)
    
    with col_fin2:
        st.subheader("Evolución del Beneficio Mensual")
        temp_df = datos_filtrados.copy()
        temp_df['mes'] = temp_df['date'].dt.to_period('M').dt.start_time
        beneficio_mensual = temp_df.groupby('mes')['profit'].sum().reset_index()
        
        # Calcular tendencia y proyección (próximos 3 meses)
        mostrar_proyeccion = len(beneficio_mensual) >= 3
        if mostrar_proyeccion:
            beneficio_mensual['mes_num'] = np.arange(len(beneficio_mensual))
            z = np.polyfit(beneficio_mensual['mes_num'], beneficio_mensual['profit'], 1)
            p = np.poly1d(z)
            beneficio_mensual['tendencia'] = p(beneficio_mensual['mes_num'])
            
            # Proyección de 3 meses futuros
            meses_futuros = 3
            ultimo_mes = beneficio_mensual['mes'].max()
            proyeccion_data = []
            for i in range(1, meses_futuros + 1):
                mes_futuro = ultimo_mes + pd.DateOffset(months=i)
                valor_proyectado = p(len(beneficio_mensual) + i - 1)
                proyeccion_data.append({'mes': mes_futuro, 'proyeccion': max(0, valor_proyectado)})
            proyeccion_df = pd.DataFrame(proyeccion_data)
        
        fig_beneficio = go.Figure()
        
        # Línea de tendencia (fondo, más sutil)
        if mostrar_proyeccion:
            fig_beneficio.add_trace(go.Scatter(
                x=beneficio_mensual['mes'],
                y=beneficio_mensual['tendencia'],
                mode='lines',
                name='Tendencia (promedio)',
                line=dict(color='#667eea', width=2, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendencia: $%{y:,.0f}<extra></extra>',
                opacity=0.6
            ))
        
        # Datos históricos (línea principal, más destacada)
        fig_beneficio.add_trace(go.Scatter(
            x=beneficio_mensual['mes'],
            y=beneficio_mensual['profit'],
            mode='lines+markers',
            name='Beneficio Real (histórico)',
            line=dict(color='#10B981', width=4),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Beneficio Real: $%{y:,.0f}<extra></extra>'
        ))
        
        # Proyección futura (empieza donde termina el histórico)
        if mostrar_proyeccion:
            # Agregar punto de conexión (último mes histórico)
            ultimo_valor_real = beneficio_mensual['profit'].iloc[-1]
            ultimo_mes_real = beneficio_mensual['mes'].iloc[-1]
            
            # Crear proyección que incluye punto de conexión
            proyeccion_x = [ultimo_mes_real] + list(proyeccion_df['mes'])
            proyeccion_y = [ultimo_valor_real] + list(proyeccion_df['proyeccion'])
            
            fig_beneficio.add_trace(go.Scatter(
                x=proyeccion_x,
                y=proyeccion_y,
                mode='lines+markers',
                name='Proyección (3 meses)',
                line=dict(color='#F59E0B', width=3, dash='dot'),
                marker=dict(symbol='diamond', size=10),
                hovertemplate='<b>%{x}</b><br>Proyección: $%{y:,.0f}<extra></extra>'
            ))
        
        fig_beneficio.update_layout(
            title='Evolución del Beneficio: Histórico y Proyección',
            xaxis_title='Mes',
            yaxis_title='Beneficio (USD)',
            height=450,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_beneficio, use_container_width=True)
    
    st.subheader("Métricas Financieras Avanzadas")
    
    col_metricas = st.columns(4)
    
    num_clientes = datos_filtrados['customer_id'].nunique()
    cac = costo_total / num_clientes if num_clientes > 0 else 0
    ltv_promedio = clientes_df['lifetime_value'].mean()
    ltv_cac_ratio = ltv_promedio / cac if cac > 0 else 0
    roas = total_ingresos / costo_total if costo_total > 0 else 0
    
    with col_metricas[0]:
        st.metric("CAC (Costo Adquisición)", f"${cac:,.0f}")
    with col_metricas[1]:
        st.metric("LTV/CAC Ratio", f"{ltv_cac_ratio:.2f}x")
    with col_metricas[2]:
        st.metric("ROAS", f"{roas:.2f}x")
    with col_metricas[3]:
        aov = datos_filtrados['total_amount_usd'].mean()
        st.metric("AOV (Valor Promedio)", f"${aov:,.0f}")

with tab_operacional:
    crear_descripcion_seccion(
        "Eficiencia Operativa y Logística",
        "Monitorea la eficiencia de tus operaciones diarias. Analiza tiempos de procesamiento de pedidos, rotación de inventario, "
        "productividad por pedido y tasa de devoluciones. Estos indicadores te ayudan a identificar cuellos de botella y "
        "oportunidades de optimización en tus procesos."
    )
    
    crear_seccion_titulo("Métricas Operacionales")
    
    st.subheader("📦 KPIs Operativos Principales")
    
    total_pedidos = datos_filtrados['transaction_id'].nunique()
    total_unidades = datos_filtrados['quantity'].sum()
    promedio_unidades_pedido = datos_filtrados.groupby('transaction_id')['quantity'].sum().mean()
    tasa_conversion = (total_pedidos / len(datos_filtrados) * 100) if len(datos_filtrados) > 0 else 0
    
    col_op1, col_op2, col_op3, col_op4 = st.columns(4)
    
    with col_op1:
        st.metric("Total Pedidos", f"{total_pedidos:,}", delta="+8.5%")
    with col_op2:
        st.metric("Unidades Vendidas", f"{total_unidades:,.0f}", delta="+15.3%")
    with col_op3:
        st.metric("Unidades/Pedido", f"{promedio_unidades_pedido:.1f}", delta="+2.1%")
    with col_op4:
        st.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", delta="+1.8%")
    
    col_op_viz1, col_op_viz2 = st.columns(2)
    
    with col_op_viz1:
        st.subheader("Pedidos por Día de Semana")
        from utils.traducciones import traducir_dia_semana
        temp_df = datos_filtrados.copy()
        temp_df['dia_semana'] = pd.to_datetime(temp_df['date']).dt.day_name()
        pedidos_dia = temp_df.groupby('dia_semana')['transaction_id'].nunique().reset_index()
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pedidos_dia['dia_semana'] = pd.Categorical(pedidos_dia['dia_semana'], categories=dias_orden, ordered=True)
        pedidos_dia = pedidos_dia.sort_values('dia_semana')
        # Traducir días al español
        pedidos_dia['dia_semana_es'] = pedidos_dia['dia_semana'].apply(traducir_dia_semana)
        
        fig_dias_op = px.bar(
            pedidos_dia,
            x='dia_semana_es',
            y='transaction_id',
            title='Distribución de Pedidos por Día',
            labels=LABELS,
            color='transaction_id',
            color_continuous_scale='Blues'
        )
        fig_dias_op.update_traces(hovertemplate='<b>%{x}</b><br>Pedidos: %{y:,}<extra></extra>')
        fig_dias_op.update_layout(
            height=400, 
            showlegend=False,
            xaxis_title="Día de la Semana"
        )
        st.plotly_chart(fig_dias_op, use_container_width=True)
    
    with col_op_viz2:
        st.subheader("Distribución de Cantidad por Pedido")
        cantidades_pedido = datos_filtrados.groupby('transaction_id')['quantity'].sum()
        
        fig_cantidad = px.histogram(
            cantidades_pedido,
            nbins=30,
            title='Histograma de Unidades por Pedido',
            labels=LABELS,
            color_discrete_sequence=['#667eea']
        )
        fig_cantidad.update_traces(hovertemplate='Unidades: %{x:,.0f}<br>Pedidos: %{y:,}<extra></extra>')
        fig_cantidad.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cantidad, use_container_width=True)
    
    st.subheader("⏱️ Análisis de Velocidad de Ventas")
    
    temp_df = datos_filtrados.copy()
    temp_df['fecha'] = pd.to_datetime(temp_df['date']).dt.date
    ventas_diarias = temp_df.groupby('fecha').agg({
        'transaction_id': 'nunique',
        'quantity': 'sum',
        'total_amount_usd': 'sum'
    }).reset_index()
    ventas_diarias.columns = ['fecha', 'pedidos', 'unidades', 'ingresos']
    
    fig_velocidad = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_velocidad.add_trace(
        go.Scatter(
            x=ventas_diarias['fecha'],
            y=ventas_diarias['pedidos'],
            name='Pedidos Diarios',
            line=dict(color='#667eea', width=2)
        ),
        secondary_y=False
    )
    
    fig_velocidad.add_trace(
        go.Scatter(
            x=ventas_diarias['fecha'],
            y=ventas_diarias['unidades'],
            name='Unidades Diarias',
            line=dict(color='#f093fb', width=2)
        ),
        secondary_y=True
    )
    
    fig_velocidad.update_xaxes(title_text="Fecha")
    fig_velocidad.update_yaxes(title_text="Pedidos", secondary_y=False)
    fig_velocidad.update_yaxes(title_text="Unidades", secondary_y=True)
    fig_velocidad.update_layout(height=400, title='Velocidad de Ventas Diaria')
    
    st.plotly_chart(fig_velocidad, use_container_width=True)
    
    st.subheader("🏆 Top Productos por Rotación")
    
    # Filtrar productos no significativos (mismos que en Top 20)
    productos_excluir = ['Manual', 'POSTAGE', 'DOTCOM POSTAGE', 'Adjust bad debt', 'BANK CHARGES']
    datos_operacionales_reales = datos_filtrados[~datos_filtrados['product_name'].isin(productos_excluir)]
    
    rotacion_productos = datos_operacionales_reales.groupby(['product_name', 'category']).agg({
        'quantity': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    rotacion_productos.columns = ['producto', 'categoria', 'unidades_vendidas', 'frecuencia']
    rotacion_productos['velocidad'] = rotacion_productos['unidades_vendidas'] * rotacion_productos['frecuencia']
    top_rotacion = rotacion_productos.nlargest(15, 'velocidad')
    
    fig_rotacion = px.bar(
        top_rotacion,
        x='velocidad',
        y='producto',
        orientation='h',
        title='Top 15 Productos por Velocidad de Rotación (excl. envíos)',
        labels=LABELS,
        color='categoria',
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data=['categoria', 'unidades_vendidas']
    )
    fig_rotacion.update_traces(hovertemplate='<b>%{y}</b><br>Categoría: %{customdata[0]}<br>Velocidad: %{x:,.0f}<br>Unidades: %{customdata[1]:,.0f}<extra></extra>')
    fig_rotacion.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_rotacion, use_container_width=True)

crear_pie_pagina()
