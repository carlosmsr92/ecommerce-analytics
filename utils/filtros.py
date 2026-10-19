"""
Sistema de Filtros Optimizado para Dashboard
Autor: cmsr92
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def obtener_rango_fecha_preset(preset, fecha_fin):
    """Convierte preset de periodo a rango de fechas que termina en fecha_fin (la última fecha con datos).

    Se ancla al final del histórico y no a hoy: si no, «Últimos 90 días» queda vacío en cuanto los datos se quedan atrás.
    """
    
    mapeo = {
        'Últimos 7 Días': 7,
        'Últimos 30 Días': 30,
        'Últimos 90 Días': 90,
        'Último Año': 365,
        'Todo el Histórico': 3650
    }
    
    dias = mapeo.get(preset, 90)
    fecha_inicio = fecha_fin - timedelta(days=dias)
    
    return fecha_inicio, fecha_fin

def crear_filtros_sidebar(transacciones_df):
    """
    Crea sistema de filtros colapsables en sidebar sin solapamiento
    
    Returns:
        dict: Diccionario con todos los filtros aplicados
    """
    st.sidebar.markdown("### ⚙️ Panel de Control")
    st.sidebar.markdown("---")
    
    filtros = {}
    
    with st.sidebar.expander("📅 PERIODO DE ANÁLISIS", expanded=True):
        tipo_periodo = st.selectbox(
            "Seleccionar periodo",
            ['Personalizado', 'Últimos 7 Días', 'Últimos 30 Días', 'Últimos 90 Días', 'Último Año', 'Todo el Histórico'],
            index=3,
            help="Selecciona el rango temporal para el análisis"
        )
        
        # Fechas límite del histórico
        fecha_min_historico = pd.Timestamp(transacciones_df['date'].min()).to_pydatetime().replace(hour=0, minute=0, second=0)
        fecha_max_historico = datetime.combine(pd.Timestamp(transacciones_df['date'].max()).date(), datetime.max.time())
        
        if tipo_periodo == 'Personalizado':
            # Calendarios desplegables para selección personalizada
            col1, col2 = st.columns(2)
            
            with col1:
                fecha_inicio = st.date_input(
                    "Desde",
                    value=datetime(2024, 7, 28),
                    min_value=fecha_min_historico,
                    max_value=fecha_max_historico,
                    format="DD/MM/YYYY",
                    help="Fecha inicio del análisis"
                )
            
            with col2:
                fecha_fin = st.date_input(
                    "Hasta",
                    value=fecha_max_historico,
                    min_value=fecha_min_historico,
                    max_value=fecha_max_historico,
                    format="DD/MM/YYYY",
                    help="Fecha fin del análisis"
                )
            
            # Validar que las fechas no sean None (puede ocurrir durante interacción con calendarios)
            if fecha_inicio is None or fecha_fin is None:
                # Usar valores por defecto si alguna fecha es None
                fecha_inicio = datetime(2024, 7, 28)
                fecha_fin = fecha_max_historico
                st.warning("⚠️ Selecciona ambas fechas para aplicar el filtro personalizado")
            else:
                # Convertir date a datetime para consistencia
                fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
                fecha_fin = datetime.combine(fecha_fin, datetime.max.time())
                
                # Validación: fecha inicio debe ser menor que fecha fin
                if fecha_inicio >= fecha_fin:
                    st.error("⚠️ La fecha de inicio debe ser anterior a la fecha fin")
                    # Usar valores por defecto si hay error
                    fecha_inicio = datetime(2024, 7, 28)
                    fecha_fin = fecha_max_historico
        else:
            # Usar presets
            fecha_inicio, fecha_fin = obtener_rango_fecha_preset(tipo_periodo, fecha_max_historico)
        
        filtros['fecha_inicio'] = fecha_inicio
        filtros['fecha_fin'] = fecha_fin
        
        # Mostrar resumen del rango seleccionado
        duracion_dias = (fecha_fin - fecha_inicio).days
        st.caption(f"📊 Analizando {duracion_dias} días de datos")
    
    with st.sidebar.expander("🌍 GEOGRAFÍA"):
        paises_disponibles = sorted(transacciones_df['country'].unique().tolist())
        paises_seleccionados = st.multiselect(
            "Países",
            paises_disponibles,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por uno o más países (deja vacío para todos)"
        )
        filtros['paises'] = paises_seleccionados
        
        if paises_seleccionados:
            regiones_disponibles = sorted(transacciones_df[
                transacciones_df['country'].isin(paises_seleccionados)
            ]['region'].unique().tolist())
        else:
            regiones_disponibles = sorted(transacciones_df['region'].unique().tolist())
        
        regiones_seleccionadas = st.multiselect(
            "Regiones",
            regiones_disponibles,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por una o más regiones"
        )
        filtros['regiones'] = regiones_seleccionadas
    
    with st.sidebar.expander("📦 PRODUCTOS"):
        categorias_disponibles = sorted(transacciones_df['category'].unique().tolist())
        categorias_seleccionadas = st.multiselect(
            "Categorías",
            categorias_disponibles,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por categorías de productos"
        )
        filtros['categorias'] = categorias_seleccionadas
        
        if categorias_seleccionadas:
            subcategorias_disponibles = sorted(transacciones_df[
                transacciones_df['category'].isin(categorias_seleccionadas)
            ]['subcategory'].unique().tolist())
        else:
            subcategorias_disponibles = sorted(transacciones_df['subcategory'].unique().tolist())
        
        subcategorias_seleccionadas = st.multiselect(
            "Subcategorías",
            subcategorias_disponibles,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por subcategorías específicas"
        )
        filtros['subcategorias'] = subcategorias_seleccionadas
    
    with st.sidebar.expander("👥 CLIENTES"):
        segmentos_disponibles = sorted(transacciones_df['customer_segment'].unique().tolist())
        segmentos_seleccionados = st.multiselect(
            "Segmentos de Cliente",
            segmentos_disponibles,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por segmento de cliente (VIP, Regular, etc.)"
        )
        filtros['segmentos'] = segmentos_seleccionados
    
    with st.sidebar.expander("💳 CANAL Y PAGO"):
        metodos_pago = sorted(transacciones_df['payment_method'].unique().tolist())
        metodos_seleccionados = st.multiselect(
            "Método de Pago",
            metodos_pago,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por método de pago utilizado"
        )
        filtros['metodos_pago'] = metodos_seleccionados
        
        dispositivos = sorted(transacciones_df['device_type'].unique().tolist())
        dispositivos_seleccionados = st.multiselect(
            "Tipo de Dispositivo",
            dispositivos,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por dispositivo usado para la compra"
        )
        filtros['dispositivos'] = dispositivos_seleccionados
        
        fuentes_trafico = sorted(transacciones_df['traffic_source'].unique().tolist())
        fuentes_seleccionadas = st.multiselect(
            "Fuente de Tráfico",
            fuentes_trafico,
            default=[],
            placeholder="Elige opciones",
            help="Filtra por canal de adquisición"
        )
        filtros['fuentes_trafico'] = fuentes_seleccionadas
    
    with st.sidebar.expander("💰 RANGO DE PRECIOS"):
        precio_min = float(transacciones_df['unit_price'].min())
        precio_max = float(transacciones_df['unit_price'].max())
        
        rango_precios = st.slider(
            "Precio Unitario (USD)",
            min_value=precio_min,
            max_value=precio_max,
            value=(precio_min, precio_max),
            help="Ajusta el rango de precios unitarios"
        )
        filtros['precio_min'] = rango_precios[0]
        filtros['precio_max'] = rango_precios[1]
    
    with st.sidebar.expander("🤖 OPCIONES ML/IA"):
        mostrar_ml = st.checkbox(
            "Activar Análisis ML",
            value=True,
            help="Mostrar predicciones y análisis de Machine Learning"
        )
        filtros['mostrar_ml'] = mostrar_ml
        
        mostrar_anomalias = st.checkbox(
            "Detección de Anomalías",
            value=False,
            help="Identificar patrones anómalos en los datos"
        )
        filtros['mostrar_anomalias'] = mostrar_anomalias
    
    st.sidebar.markdown("---")
    
    num_filtros_activos = sum([
        bool(filtros.get('paises')),
        bool(filtros.get('regiones')),
        bool(filtros.get('categorias')),
        bool(filtros.get('subcategorias')),
        bool(filtros.get('segmentos')),
        bool(filtros.get('metodos_pago')),
        bool(filtros.get('dispositivos')),
        bool(filtros.get('fuentes_trafico')),
    ])
    
    if num_filtros_activos > 0:
        st.sidebar.info(f"🔍 **Filtros Activos:** {num_filtros_activos}")
        st.sidebar.caption("💡 Puedes limpiar cada filtro individualmente usando el ícono ✕ en cada campo")
    
    return filtros

def aplicar_filtros(df, filtros):
    """
    Aplica filtros al DataFrame
    
    Args:
        df: DataFrame de transacciones
        filtros: Diccionario de filtros
        
    Returns:
        DataFrame filtrado
    """
    df_filtrado = df.copy()
    
    df_filtrado = df_filtrado[
        (df_filtrado['date'] >= pd.Timestamp(filtros['fecha_inicio'])) & 
        (df_filtrado['date'] <= pd.Timestamp(filtros['fecha_fin']))
    ]
    
    if filtros.get('paises'):
        df_filtrado = df_filtrado[df_filtrado['country'].isin(filtros['paises'])]
    
    if filtros.get('regiones'):
        df_filtrado = df_filtrado[df_filtrado['region'].isin(filtros['regiones'])]
    
    if filtros.get('categorias'):
        df_filtrado = df_filtrado[df_filtrado['category'].isin(filtros['categorias'])]
    
    if filtros.get('subcategorias'):
        df_filtrado = df_filtrado[df_filtrado['subcategory'].isin(filtros['subcategorias'])]
    
    if filtros.get('segmentos'):
        df_filtrado = df_filtrado[df_filtrado['customer_segment'].isin(filtros['segmentos'])]
    
    if filtros.get('metodos_pago'):
        df_filtrado = df_filtrado[df_filtrado['payment_method'].isin(filtros['metodos_pago'])]
    
    if filtros.get('dispositivos'):
        df_filtrado = df_filtrado[df_filtrado['device_type'].isin(filtros['dispositivos'])]
    
    if filtros.get('fuentes_trafico'):
        df_filtrado = df_filtrado[df_filtrado['traffic_source'].isin(filtros['fuentes_trafico'])]
    
    if filtros.get('precio_min') is not None and filtros.get('precio_max') is not None:
        df_filtrado = df_filtrado[
            (df_filtrado['unit_price'] >= filtros['precio_min']) & 
            (df_filtrado['unit_price'] <= filtros['precio_max'])
        ]
    
    return df_filtrado
