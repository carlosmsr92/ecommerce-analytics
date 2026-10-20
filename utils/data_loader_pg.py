import pandas as pd
import streamlit as st
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
        st.error(f"Error al cargar los datos: {e}")
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
