import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utils.traducciones import (
    aplicar_traducciones_df, 
    aplicar_traducciones_paises_df,
    aplicar_traducciones_rfm_df,
    aplicar_traducciones_dispositivos_df,
    aplicar_traducciones_metodos_pago_df,
    aplicar_traducciones_fuentes_trafico_df,
    aplicar_traducciones_segmentos_clientes_df
)

def load_data_from_postgres():
    """Carga datos desde archivos unificados (Parquet) o PostgreSQL - con consolidación de variantes de países"""
    import os
    
    # Verificar si existen archivos unificados
    use_unified = os.path.exists('data/transactions_unified.parquet')
    
    if use_unified:
        try:
            # Cargar desde archivos unificados
            transactions_df = pd.read_parquet('data/transactions_unified.parquet')
            customers_df = pd.read_parquet('data/customers_unified.parquet')
            products_df = pd.read_parquet('data/products_unified.parquet')
            
            # Convertir fechas
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
            customers_df['last_purchase_date'] = pd.to_datetime(customers_df['last_purchase_date'])
            if 'launch_date' in products_df.columns:
                products_df['launch_date'] = pd.to_datetime(products_df['launch_date'])
            
            # Traducir categorías al español
            transactions_df = aplicar_traducciones_df(transactions_df, 'category')
            products_df = aplicar_traducciones_df(products_df, 'category')
            if 'subcategory' in transactions_df.columns:
                transactions_df = aplicar_traducciones_df(transactions_df, 'subcategory')
            if 'subcategory' in products_df.columns:
                products_df = aplicar_traducciones_df(products_df, 'subcategory')
            
            # Traducir países al español
            transactions_df = aplicar_traducciones_paises_df(transactions_df, 'country')
            customers_df = aplicar_traducciones_paises_df(customers_df, 'country')
            
            # Consolidar variantes de nombres de países
            transactions_df['country'] = transactions_df['country'].replace({
                'USA': 'Estados Unidos',
                'EIRE': 'Irlanda',
                'Ireland': 'Irlanda',
                'RSA': 'Sudáfrica',
                'Channel Islands': 'Reino Unido',
                'European Community': 'Unión Europea',
                'Unspecified': 'No Especificado'
            })
            customers_df['country'] = customers_df['country'].replace({
                'USA': 'Estados Unidos',
                'EIRE': 'Irlanda',
                'Ireland': 'Irlanda',
                'RSA': 'Sudáfrica',
                'Channel Islands': 'Reino Unido',
                'European Community': 'Unión Europea',
                'Unspecified': 'No Especificado'
            })
            
            # Traducir segmentos RFM al español
            if 'rfm_segment' in customers_df.columns:
                customers_df = aplicar_traducciones_rfm_df(customers_df, 'rfm_segment')
            
            # Traducir dispositivos al español
            if 'device_type' in transactions_df.columns:
                transactions_df = aplicar_traducciones_dispositivos_df(transactions_df, 'device_type')
            
            # Traducir métodos de pago al español
            if 'payment_method' in transactions_df.columns:
                transactions_df = aplicar_traducciones_metodos_pago_df(transactions_df, 'payment_method')
            
            # Traducir fuentes de tráfico al español
            if 'traffic_source' in transactions_df.columns:
                transactions_df = aplicar_traducciones_fuentes_trafico_df(transactions_df, 'traffic_source')
            
            # Traducir segmentos de clientes al español
            if 'customer_segment' in transactions_df.columns:
                transactions_df = aplicar_traducciones_segmentos_clientes_df(transactions_df, 'customer_segment')
            if 'customer_segment' in customers_df.columns:
                customers_df = aplicar_traducciones_segmentos_clientes_df(customers_df, 'customer_segment')
            
            # Convertir churn_probability de escala 0-100 a escala 0-1 estándar
            if 'churn_probability' in customers_df.columns:
                # Si los valores están en rango 0-100, convertir a 0-1
                if customers_df['churn_probability'].max() > 1.0:
                    customers_df['churn_probability'] = customers_df['churn_probability'] / 100.0
            
            return transactions_df, customers_df, products_df
            
        except Exception as e:
            # Sin esto, un fallo al leer los Parquet pasaba desapercibido y la app esperaba a una base de datos inexistente
            st.error(f"No se pudieron leer los datos Parquet: {e}")
            return None, None, None

    # Fallback a PostgreSQL (solo si no hay Parquet): se importa aquí para no exigir SQLAlchemy al dashboard
    from database.schema import get_engine
    engine = get_engine()
    
    try:
        # Cargar transacciones
        transactions_df = pd.read_sql_table('transactions', engine)
        
        # Cargar clientes
        customers_df = pd.read_sql_table('customers', engine)
        
        # Cargar productos
        products_df = pd.read_sql_table('products', engine)
        
        # Convertir fechas
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
        customers_df['last_purchase_date'] = pd.to_datetime(customers_df['last_purchase_date'])
        products_df['launch_date'] = pd.to_datetime(products_df['launch_date'])
        
        # Traducir categorías al español
        transactions_df = aplicar_traducciones_df(transactions_df, 'category')
        products_df = aplicar_traducciones_df(products_df, 'category')
        if 'subcategory' in transactions_df.columns:
            transactions_df = aplicar_traducciones_df(transactions_df, 'subcategory')
        if 'subcategory' in products_df.columns:
            products_df = aplicar_traducciones_df(products_df, 'subcategory')
        
        # Traducir países al español
        transactions_df = aplicar_traducciones_paises_df(transactions_df, 'country')
        customers_df = aplicar_traducciones_paises_df(customers_df, 'country')
        
        # Consolidar variantes de nombres de países
        transactions_df['country'] = transactions_df['country'].replace({
            'USA': 'Estados Unidos',
            'EIRE': 'Irlanda',
            'Ireland': 'Irlanda',
            'RSA': 'Sudáfrica',
            'Channel Islands': 'Reino Unido',
            'European Community': 'Unión Europea',
            'Unspecified': 'No Especificado'
        })
        customers_df['country'] = customers_df['country'].replace({
            'USA': 'Estados Unidos',
            'EIRE': 'Irlanda',
            'Ireland': 'Irlanda',
            'RSA': 'Sudáfrica',
            'Channel Islands': 'Reino Unido',
            'European Community': 'Unión Europea',
            'Unspecified': 'No Especificado'
        })
        
        # Traducir segmentos RFM al español
        if 'rfm_segment' in customers_df.columns:
            customers_df = aplicar_traducciones_rfm_df(customers_df, 'rfm_segment')
        
        # Traducir dispositivos al español
        if 'device_type' in transactions_df.columns:
            transactions_df = aplicar_traducciones_dispositivos_df(transactions_df, 'device_type')
        
        # Traducir métodos de pago al español
        if 'payment_method' in transactions_df.columns:
            transactions_df = aplicar_traducciones_metodos_pago_df(transactions_df, 'payment_method')
        
        # Traducir fuentes de tráfico al español
        if 'traffic_source' in transactions_df.columns:
            transactions_df = aplicar_traducciones_fuentes_trafico_df(transactions_df, 'traffic_source')
        
        # Traducir segmentos de clientes al español
        if 'customer_segment' in transactions_df.columns:
            transactions_df = aplicar_traducciones_segmentos_clientes_df(transactions_df, 'customer_segment')
        if 'customer_segment' in customers_df.columns:
            customers_df = aplicar_traducciones_segmentos_clientes_df(customers_df, 'customer_segment')
        
        # Convertir churn_probability de escala 0-100 a escala 0-1 estándar
        if 'churn_probability' in customers_df.columns:
            # Si los valores están en rango 0-100, convertir a 0-1
            if customers_df['churn_probability'].max() > 1.0:
                customers_df['churn_probability'] = customers_df['churn_probability'] / 100.0
        
        return transactions_df, customers_df, products_df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

def _optimizar_memoria(df):
    """Columnas de texto con pocos valores distintos (país, categoría, método de pago...) como 'category'.

    Reduce mucho la memoria, clave en Streamlit Community Cloud, donde pasarse del límite reinicia la app.
    """
    if df is None:
        return df
    for col in df.columns:
        if (df[col].dtype == object or str(df[col].dtype).startswith("str")) and df[col].nunique() < 0.5 * len(df):
            df[col] = df[col].astype("category")
    return df

def load_or_generate_data():
    """Carga datos desde fuente disponible (la caché está en app.py: una sola copia en memoria)"""
    return tuple(_optimizar_memoria(df) for df in load_data_from_postgres())

def filter_data(df, filters):
    """Aplica filtros al DataFrame"""
    filtered_df = df.copy()
    
    if 'date_range' in filters and filters['date_range']:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[(filtered_df['date'] >= pd.Timestamp(start_date)) & 
                                   (filtered_df['date'] <= pd.Timestamp(end_date))]
    
    if 'countries' in filters and filters['countries']:
        filtered_df = filtered_df[filtered_df['country'].isin(filters['countries'])]
    
    if 'categories' in filters and filters['categories']:
        filtered_df = filtered_df[filtered_df['category'].isin(filters['categories'])]
    
    if 'segments' in filters and filters['segments']:
        filtered_df = filtered_df[filtered_df['customer_segment'].isin(filters['segments'])]
    
    if 'payment_methods' in filters and filters['payment_methods']:
        filtered_df = filtered_df[filtered_df['payment_method'].isin(filters['payment_methods'])]
    
    if 'device_types' in filters and filters['device_types']:
        filtered_df = filtered_df[filtered_df['device_type'].isin(filters['device_types'])]
    
    if 'traffic_sources' in filters and filters['traffic_sources']:
        filtered_df = filtered_df[filtered_df['traffic_source'].isin(filters['traffic_sources'])]
    
    if 'price_range' in filters and filters['price_range']:
        min_price, max_price = filters['price_range']
        filtered_df = filtered_df[(filtered_df['unit_price'] >= min_price) & 
                                   (filtered_df['unit_price'] <= max_price)]
    
    return filtered_df

def get_date_range_preset(preset):
    """Devuelve rango de fechas basado en preset"""
    end_date = datetime.now()
    
    if preset == 'Today':
        start_date = end_date - timedelta(days=1)
    elif preset == 'Last 7 Days':
        start_date = end_date - timedelta(days=7)
    elif preset == 'Last 30 Days':
        start_date = end_date - timedelta(days=30)
    elif preset == 'Last 90 Days':
        start_date = end_date - timedelta(days=90)
    elif preset == 'Last Year':
        start_date = end_date - timedelta(days=365)
    elif preset == 'All Time':
        start_date = end_date - timedelta(days=730)
    else:
        start_date = end_date - timedelta(days=30)
    
    return start_date, end_date

@st.cache_data(ttl=60)
def get_kpis_from_db(start_date, end_date, filters=None):
    """Obtiene KPIs directamente desde PostgreSQL con query optimizada"""
    engine = get_engine()
    
    query = f"""
    SELECT 
        COUNT(*) as total_orders,
        SUM(total_amount_usd) as total_revenue,
        AVG(total_amount_usd) as avg_order_value,
        SUM(profit) as total_profit,
        COUNT(DISTINCT customer_id) as total_customers
    FROM transactions
    WHERE date >= '{start_date}' AND date <= '{end_date}'
    """
    
    if filters:
        if 'countries' in filters and filters['countries']:
            countries_str = "','".join(filters['countries'])
            query += f" AND country IN ('{countries_str}')"
        
        if 'categories' in filters and filters['categories']:
            categories_str = "','".join(filters['categories'])
            query += f" AND category IN ('{categories_str}')"
    
    try:
        result = pd.read_sql_query(query, engine)
        return result.iloc[0].to_dict()
    except:
        return None
