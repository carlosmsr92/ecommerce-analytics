"""
Traducciones completas al español para el dashboard
Incluye: categorías, países, días, segmentos RFM, dispositivos, métodos de pago
"""

import pandas as pd

# Diccionario de traducción de segmentos RFM
SEGMENTOS_RFM_TRADUCCION = {
    'Champions': 'Campeones',
    'Loyal Customers': 'Clientes Leales',
    'Potential Loyalists': 'Potencialmente Leales',
    'Recent Customers': 'Clientes Recientes',
    'Promising': 'Prometedores',
    'Customers Needing Attention': 'Necesitan Atención',
    'About To Sleep': 'Por Dormir',
    'At Risk': 'En Riesgo',
    'Cant Lose Them': 'No Perderlos',
    'Hibernating': 'Hibernando',
    'Lost': 'Perdidos',
    # Versiones alternativas
    'Cant Lose': 'No Perderlos',
    'Lost Customers': 'Perdidos',
    # Minúsculas también
    'champions': 'Campeones',
    'loyal customers': 'Clientes Leales',
    'potential loyalists': 'Potencialmente Leales',
    'recent customers': 'Clientes Recientes',
    'promising': 'Prometedores',
    'customers needing attention': 'Necesitan Atención',
    'about to sleep': 'Por Dormir',
    'at risk': 'En Riesgo',
    'cant lose them': 'No Perderlos',
    'hibernating': 'Hibernando',
    'lost': 'Perdidos'
}

# Diccionario de traducción de dispositivos
DISPOSITIVOS_TRADUCCION = {
    'Mobile': 'Móvil',
    'Tablet': 'Tableta',
    'Desktop': 'Escritorio',
    'mobile': 'Móvil',
    'tablet': 'Tableta',
    'desktop': 'Escritorio'
}

# Diccionario de traducción de métodos de pago
METODOS_PAGO_TRADUCCION = {
    'Credit Card': 'Tarjeta de Crédito',
    'Debit Card': 'Tarjeta de Débito',
    'PayPal': 'PayPal',
    'Bank Transfer': 'Transferencia Bancaria',
    'Cash': 'Efectivo',
    'Wire Transfer': 'Transferencia',
    # Minúsculas
    'credit card': 'Tarjeta de Crédito',
    'debit card': 'Tarjeta de Débito',
    'paypal': 'PayPal',
    'bank transfer': 'Transferencia Bancaria',
    'cash': 'Efectivo',
    'wire transfer': 'Transferencia'
}

# Diccionario de traducción de países
PAISES_TRADUCCION = {
    'United Kingdom': 'Reino Unido',
    'United States': 'Estados Unidos',
    'France': 'Francia',
    'Germany': 'Alemania',
    'Spain': 'España',
    'Italy': 'Italia',
    'Netherlands': 'Países Bajos',
    'Belgium': 'Bélgica',
    'Switzerland': 'Suiza',
    'Portugal': 'Portugal',
    'Sweden': 'Suecia',
    'Norway': 'Noruega',
    'Denmark': 'Dinamarca',
    'Finland': 'Finlandia',
    'Poland': 'Polonia',
    'Austria': 'Austria',
    'Greece': 'Grecia',
    'Ireland': 'Irlanda',
    'EIRE': 'Irlanda',
    'Czech Republic': 'República Checa',
    'Hungary': 'Hungría',
    'Romania': 'Rumania',
    'Bulgaria': 'Bulgaria',
    'Croatia': 'Croacia',
    'Slovakia': 'Eslovaquia',
    'Slovenia': 'Eslovenia',
    'Lithuania': 'Lituania',
    'Latvia': 'Letonia',
    'Estonia': 'Estonia',
    'Luxembourg': 'Luxemburgo',
    'Malta': 'Malta',
    'Cyprus': 'Chipre',
    'Australia': 'Australia',
    'Canada': 'Canadá',
    'Japan': 'Japón',
    'China': 'China',
    'India': 'India',
    'Brazil': 'Brasil',
    'Mexico': 'México',
    'Argentina': 'Argentina',
    'Chile': 'Chile',
    'Colombia': 'Colombia',
    'Peru': 'Perú',
    'Venezuela': 'Venezuela',
    'Ecuador': 'Ecuador',
    'Uruguay': 'Uruguay',
    'Paraguay': 'Paraguay',
    'Bolivia': 'Bolivia',
    'Costa Rica': 'Costa Rica',
    'Panama': 'Panamá',
    'Guatemala': 'Guatemala',
    'Honduras': 'Honduras',
    'Nicaragua': 'Nicaragua',
    'El Salvador': 'El Salvador',
    'Dominican Republic': 'República Dominicana',
    'Cuba': 'Cuba',
    'Puerto Rico': 'Puerto Rico',
    'Jamaica': 'Jamaica',
    'Trinidad and Tobago': 'Trinidad y Tobago',
    'Bahamas': 'Bahamas',
    'Barbados': 'Barbados',
    'South Africa': 'Sudáfrica',
    'Egypt': 'Egipto',
    'Morocco': 'Marruecos',
    'Tunisia': 'Túnez',
    'Algeria': 'Argelia',
    'Kenya': 'Kenia',
    'Nigeria': 'Nigeria',
    'Ghana': 'Ghana',
    'Ethiopia': 'Etiopía',
    'Tanzania': 'Tanzania',
    'Uganda': 'Uganda',
    'Zimbabwe': 'Zimbabue',
    'South Korea': 'Corea del Sur',
    'North Korea': 'Corea del Norte',
    'Singapore': 'Singapur',
    'Malaysia': 'Malasia',
    'Indonesia': 'Indonesia',
    'Philippines': 'Filipinas',
    'Thailand': 'Tailandia',
    'Vietnam': 'Vietnam',
    'Cambodia': 'Camboya',
    'Laos': 'Laos',
    'Myanmar': 'Myanmar',
    'Bangladesh': 'Bangladés',
    'Pakistan': 'Pakistán',
    'Sri Lanka': 'Sri Lanka',
    'Nepal': 'Nepal',
    'Afghanistan': 'Afganistán',
    'Iran': 'Irán',
    'Iraq': 'Irak',
    'Saudi Arabia': 'Arabia Saudita',
    'United Arab Emirates': 'Emiratos Árabes Unidos',
    'Kuwait': 'Kuwait',
    'Qatar': 'Catar',
    'Bahrain': 'Baréin',
    'Oman': 'Omán',
    'Jordan': 'Jordania',
    'Lebanon': 'Líbano',
    'Syria': 'Siria',
    'Israel': 'Israel',
    'Palestine': 'Palestina',
    'Turkey': 'Turquía',
    'Russia': 'Rusia',
    'Ukraine': 'Ucrania',
    'Belarus': 'Bielorrusia',
    'Moldova': 'Moldavia',
    'Georgia': 'Georgia',
    'Armenia': 'Armenia',
    'Azerbaijan': 'Azerbaiyán',
    'Kazakhstan': 'Kazajistán',
    'Uzbekistan': 'Uzbekistán',
    'Turkmenistan': 'Turkmenistán',
    'Kyrgyzstan': 'Kirguistán',
    'Tajikistan': 'Tayikistán',
    'New Zealand': 'Nueva Zelanda',
    'Fiji': 'Fiyi',
    'Papua New Guinea': 'Papúa Nueva Guinea',
    'Iceland': 'Islandia'
}

# Diccionario de traducción de días de semana
DIAS_SEMANA_TRADUCCION = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo',
    # Abreviaciones
    'Mon': 'Lun',
    'Tue': 'Mar',
    'Wed': 'Mié',
    'Thu': 'Jue',
    'Fri': 'Vie',
    'Sat': 'Sáb',
    'Sun': 'Dom'
}

# Diccionario de traducción de meses
MESES_TRADUCCION = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre',
    # Abreviaciones
    'Jan': 'Ene',
    'Feb': 'Feb',
    'Mar': 'Mar',
    'Apr': 'Abr',
    # 'May' es a la vez nombre y abreviatura: ya está arriba
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Aug': 'Ago',
    'Sep': 'Sep',
    'Oct': 'Oct',
    'Nov': 'Nov',
    'Dec': 'Dic'
}

# Diccionario de traducción de categorías
CATEGORIAS_TRADUCCION = {
    # Categorías principales
    'Books': 'Libros',
    'Electronics': 'Electrónica',
    'Clothing': 'Ropa',
    'Home & Garden': 'Hogar y Jardín',
    'Home': 'Hogar',
    'Sports': 'Deportes',
    'Toys': 'Juguetes',
    'Beauty': 'Belleza',
    'Food': 'Alimentos',
    'Groceries': 'Comestibles',
    'Fashion': 'Moda',
    'Health': 'Salud',
    'Automotive': 'Automotriz',
    'Office': 'Oficina',
    'Pet Supplies': 'Mascotas',
    'Music': 'Música',
    'Movies': 'Películas',
    'Games': 'Videojuegos',
    'Baby': 'Bebé',
    'Tools': 'Herramientas',
    'Jewelry': 'Joyería',
    'Shoes': 'Calzado',
    'Outdoor': 'Exterior',
    
    # Subcategorías comunes
    'book': 'libros',
    'electronics': 'electrónica',
    'clothing': 'ropa',
    'home': 'hogar',
    'garden': 'jardín',
    'sports': 'deportes',
    'toys': 'juguetes',
    'beauty': 'belleza',
    'food': 'alimentos',
    'groceries': 'comestibles',
    'fashion': 'moda',
    'health': 'salud',
    'automotive': 'automotriz',
    'office': 'oficina',
    'pet': 'mascotas',
    'music': 'música',
    'movies': 'películas',
    'games': 'videojuegos',
    'baby': 'bebé',
    'tools': 'herramientas',
    'jewelry': 'joyería',
    'shoes': 'calzado',
    'outdoor': 'exterior'
}

# Diccionario de traducción de fuentes de tráfico
FUENTES_TRAFICO_TRADUCCION = {
    'Direct': 'Directo',
    'Organic': 'Orgánico',
    'Paid Ads': 'Anuncios Pagados',
    'Social Media': 'Redes Sociales',
    'Email': 'Correo Electrónico',
    'Referral': 'Referencia',
    'Affiliate': 'Afiliado',
    # Minúsculas
    'direct': 'Directo',
    'organic': 'Orgánico',
    'paid ads': 'Anuncios Pagados',
    'social media': 'Redes Sociales',
    'email': 'Correo Electrónico',
    'referral': 'Referencia',
    'affiliate': 'Afiliado'
}

# Diccionario de traducción de segmentos de clientes
SEGMENTOS_CLIENTES_TRADUCCION = {
    'New': 'Nuevo',
    'Regular': 'Regular',
    'VIP': 'VIP',
    'Premium': 'Premium',
    'Bronze': 'Bronce',
    'Silver': 'Plata',
    'Gold': 'Oro',
    # Minúsculas
    'new': 'Nuevo',
    'regular': 'Regular',
    'vip': 'VIP',
    'premium': 'Premium',
    'bronze': 'Bronce',
    'silver': 'Plata',
    'gold': 'Oro'
}

# Diccionario inverso (español -> inglés) para filtros
CATEGORIAS_INVERSO = {v: k for k, v in CATEGORIAS_TRADUCCION.items()}

def traducir_categoria(categoria):
    """Traduce una categoría del inglés al español"""
    if not categoria:
        return categoria
    
    # Buscar traducción exacta
    if categoria in CATEGORIAS_TRADUCCION:
        return CATEGORIAS_TRADUCCION[categoria]
    
    # Buscar traducción case-insensitive
    categoria_lower = categoria.lower()
    if categoria_lower in CATEGORIAS_TRADUCCION:
        return CATEGORIAS_TRADUCCION[categoria_lower]
    
    # Si no hay traducción, capitalizar la primera letra
    return categoria.capitalize()

def traducir_categoria_inverso(categoria_es):
    """Traduce una categoría del español al inglés (para filtros)"""
    if not categoria_es:
        return categoria_es
    
    if categoria_es in CATEGORIAS_INVERSO:
        return CATEGORIAS_INVERSO[categoria_es]
    
    # Si no hay traducción inversa, devolver como está
    return categoria_es

def traducir_pais(pais):
    """Traduce un país del inglés al español"""
    if not pais:
        return pais
    
    # Buscar traducción exacta
    if pais in PAISES_TRADUCCION:
        return PAISES_TRADUCCION[pais]
    
    # Si no hay traducción, devolver como está
    return pais

def traducir_dia_semana(dia):
    """Traduce un día de la semana del inglés al español"""
    if not dia:
        return dia
    
    # Buscar traducción exacta
    if dia in DIAS_SEMANA_TRADUCCION:
        return DIAS_SEMANA_TRADUCCION[dia]
    
    # Si no hay traducción, devolver como está
    return dia

def traducir_mes(mes):
    """Traduce un mes del inglés al español"""
    if not mes:
        return mes
    
    # Buscar traducción exacta
    if mes in MESES_TRADUCCION:
        return MESES_TRADUCCION[mes]
    
    # Si no hay traducción, devolver como está
    return mes

def aplicar_traducciones_df(df, columna='category'):
    """Aplica traducciones a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_categoria)
    return df

def aplicar_traducciones_paises_df(df, columna='country'):
    """Aplica traducciones de países a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_pais)
    return df

def traducir_segmento_rfm(segmento):
    """Traduce un segmento RFM del inglés al español"""
    if not segmento or pd.isna(segmento):
        return segmento
    
    # Convertir a string y buscar traducción (case-insensitive)
    segmento_str = str(segmento).strip()
    
    # Buscar traducción exacta
    if segmento_str in SEGMENTOS_RFM_TRADUCCION:
        return SEGMENTOS_RFM_TRADUCCION[segmento_str]
    
    # Buscar case-insensitive
    for key, value in SEGMENTOS_RFM_TRADUCCION.items():
        if key.lower() == segmento_str.lower():
            return value
    
    # Si no hay traducción, devolver como está
    return segmento_str

def traducir_dispositivo(dispositivo):
    """Traduce un tipo de dispositivo del inglés al español"""
    if not dispositivo or pd.isna(dispositivo):
        return dispositivo
    
    dispositivo_str = str(dispositivo).strip()
    
    # Buscar traducción exacta o case-insensitive
    if dispositivo_str in DISPOSITIVOS_TRADUCCION:
        return DISPOSITIVOS_TRADUCCION[dispositivo_str]
    
    for key, value in DISPOSITIVOS_TRADUCCION.items():
        if key.lower() == dispositivo_str.lower():
            return value
    
    return dispositivo_str

def traducir_metodo_pago(metodo):
    """Traduce un método de pago del inglés al español"""
    if not metodo or pd.isna(metodo):
        return metodo
    
    metodo_str = str(metodo).strip()
    
    # Buscar traducción exacta o case-insensitive
    if metodo_str in METODOS_PAGO_TRADUCCION:
        return METODOS_PAGO_TRADUCCION[metodo_str]
    
    for key, value in METODOS_PAGO_TRADUCCION.items():
        if key.lower() == metodo_str.lower():
            return value
    
    return metodo_str

def aplicar_traducciones_rfm_df(df, columna='rfm_segment'):
    """Aplica traducciones de segmentos RFM a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_segmento_rfm)
    return df

def aplicar_traducciones_dispositivos_df(df, columna='device_type'):
    """Aplica traducciones de dispositivos a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_dispositivo)
    return df

def aplicar_traducciones_metodos_pago_df(df, columna='payment_method'):
    """Aplica traducciones de métodos de pago a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_metodo_pago)
    return df

def traducir_fuente_trafico(fuente):
    """Traduce una fuente de tráfico del inglés al español"""
    if not fuente or pd.isna(fuente):
        return fuente
    
    fuente_str = str(fuente).strip()
    
    # Buscar traducción exacta o case-insensitive
    if fuente_str in FUENTES_TRAFICO_TRADUCCION:
        return FUENTES_TRAFICO_TRADUCCION[fuente_str]
    
    for key, value in FUENTES_TRAFICO_TRADUCCION.items():
        if key.lower() == fuente_str.lower():
            return value
    
    return fuente_str

def traducir_segmento_cliente(segmento):
    """Traduce un segmento de cliente del inglés al español"""
    if not segmento or pd.isna(segmento):
        return segmento
    
    segmento_str = str(segmento).strip()
    
    # Buscar traducción exacta o case-insensitive
    if segmento_str in SEGMENTOS_CLIENTES_TRADUCCION:
        return SEGMENTOS_CLIENTES_TRADUCCION[segmento_str]
    
    for key, value in SEGMENTOS_CLIENTES_TRADUCCION.items():
        if key.lower() == segmento_str.lower():
            return value
    
    return segmento_str

def aplicar_traducciones_fuentes_trafico_df(df, columna='traffic_source'):
    """Aplica traducciones de fuentes de tráfico a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_fuente_trafico)
    return df

def aplicar_traducciones_segmentos_clientes_df(df, columna='customer_segment'):
    """Aplica traducciones de segmentos de clientes a una columna de DataFrame"""
    if columna in df.columns:
        df[columna] = df[columna].apply(traducir_segmento_cliente)
    return df

# Diccionario de labels profesionales para gráficos
LABELS_PROFESIONALES = {
    # Columnas comunes
    'total_amount_usd': 'Ingresos (USD)',
    'transaction_id': 'Transacciones',
    'profit': 'Beneficio (USD)',
    'quantity': 'Cantidad',
    'unit_price': 'Precio Unitario (USD)',
    'customer_id': 'ID Cliente',
    'product_id': 'ID Producto',
    'product_name': 'Producto',
    'category': 'Categoría',
    'subcategory': 'Subcategoría',
    'country': 'País',
    'city': 'Ciudad',
    'date': 'Fecha',
    'device_type': 'Dispositivo',
    'traffic_source': 'Fuente de Tráfico',
    'payment_method': 'Método de Pago',
    'customer_segment': 'Segmento',
    
    # RFM y segmentación
    'recency': 'Recencia (días)',
    'frequency': 'Frecuencia (compras)',
    'monetary': 'Valor Monetario (USD)',
    'rfm_segment': 'Segmento RFM',
    'churn_probability': 'Probabilidad de Churn (%)',
    'lifetime_value': 'Valor de Vida (USD)',
    'count': 'Cantidad',
    'value': 'Valor',
    
    # Análisis especiales
    'margen_%': 'Margen (%)',
    'churn_risk': 'Riesgo de Churn (%)',
    'ltv': 'Valor de Vida (USD)',
    'aov': 'Ticket Promedio (USD)',
    'es_anomalia': 'Anomalía',
    
    # Temporal
    'dia_semana': 'Día de la Semana',
    'hora': 'Hora del Día',
    'mes': 'Mes',
    'año': 'Año',
    'periodo': 'Período',
    'Fecha': 'Fecha',
    'Ingresos': 'Ingresos (USD)',
    'Pedidos': 'Pedidos',
    'Beneficio': 'Beneficio (USD)',
    
    # Agregaciones
    'ingresos': 'Ingresos (USD)',
    'pedidos': 'Pedidos',
    'beneficio': 'Beneficio (USD)',
    'cantidad': 'Cantidad',
    'clientes': 'Clientes',
    'productos': 'Productos',
    'producto': 'Producto',
    'transacciones': 'Transacciones',
    'metodo': 'Método de Pago',
    'segmento': 'Segmento',
    'nivel_riesgo': 'Nivel de Riesgo',
    'cluster': 'Cluster',
    'cuadrante': 'Cuadrante BCG',
    'velocidad': 'Velocidad de Rotación',
    'frecuencia': 'Frecuencia'
}

def obtener_labels_profesionales():
    """Retorna diccionario de labels profesionales para gráficos"""
    return LABELS_PROFESIONALES.copy()
