# 📊 Análisis global de e-commerce

**Un dashboard para entender cómo va una tienda online que vende en 43 países: qué se vende, dónde, a quién y con qué margen.**

> Autor: **Carlos Manuel Suárez Rivero (CMSR92)**  
> Plataforma: Streamlit (dashboard) · FastAPI y PostgreSQL opcionales

---

## 🎯 Descripción

Analiza **472.211 transacciones** (de diciembre de 2010 a octubre de 2025) y las presenta en:

- **9 pestañas** de análisis: resumen, países, evolución en el tiempo, productos, clientes, canales, machine learning, finanzas y operaciones
- **Machine learning** para agrupar clientes (K-Means) y marcar transacciones fuera de lo normal (Isolation Forest)
- **Tendencias** con medias móviles e indicadores de crecimiento
- **Todo en español**, con los números en formato español
- **Filtros combinables** por fechas, país, producto, cliente, canal y precio

---
🔗 **Dashboard:** [ecommers.streamlit.app](https://ecommers.streamlit.app/)

## 📦 Estructura del Proyecto

```
ecommerce-analytics/
├── app.py                          # Dashboard principal (Streamlit)
├── requirements.txt                # Dependencias del dashboard
├── requirements-api.txt            # Dependencias de la API y PostgreSQL (opcionales)
│
├── api/
│   ├── main.py                     # API RESTful (FastAPI, opcional)
│   └── ml_endpoints.py             # Endpoints de los modelos
│
├── data/                           # Datos (Parquet optimizado)
│   ├── transactions_unified.parquet
│   ├── customers_unified.parquet
│   └── products_unified.parquet
│
├── database/
│   └── schema.py                   # Esquema PostgreSQL (opcional)
│
├── utils/                          # Módulos auxiliares
│   ├── data_loader_pg.py          # Carga de datos
│   ├── filtros.py                 # Sistema de filtros
│   ├── traducciones.py            # Internacionalización
│   ├── ui_components.py           # Componentes UI
│   ├── export_utils.py            # Exportación de informes (API)
│   ├── formato.py                 # Números en formato español
│   ├── marca.py                   # Cabecera, pie e icono comunes CMSR92
│   └── assets/                    # Logo y símbolo de marca
│
└── .streamlit/
    └── config.toml                # Configuración Streamlit
```

---

## 🎨 Features Principales

### 1. **Tabs de Análisis**

| Tab | Descripción |
|-----|-------------|
| 🏠 **Resumen General** | Indicadores principales, conclusiones automáticas y evolución en el tiempo |
| 🌍 **Análisis Geográfico** | Mapa de ventas por país y ranking de países |
| 📈 **Rendimiento & Análisis Temporal** | Crecimiento, medias móviles y ventas por día y hora |
| 📦 **Análisis de Productos** | Productos que más venden, márgenes por categoría y matriz BCG |
| 👥 **Segmentación de Clientes** | Segmentos RFM, grupos con K-Means, valor de vida y riesgo de abandono |
| 📱 **Análisis de Canal** | Dispositivos, origen de las visitas, métodos de pago y diagrama de flujo |
| 🤖 **Machine Learning e IA** | Transacciones fuera de lo normal, correlaciones y productos más comprados |
| 💰 **Análisis Financiero** | Cuenta de resultados en cascada, márgenes y beneficio |
| ⚙️ **Métricas Operacionales** | Pedidos, unidades por pedido y rotación de productos |

### 2. **Machine Learning**

- **Isolation Forest:** marca las transacciones que se salen de lo normal
- **K-Means:** agrupa a los clientes según cuándo, cuánto y cada cuánto compran
- **Correlaciones:** qué variables se mueven juntas
- **Productos más comprados:** el punto de partida para un futuro sistema de recomendaciones

### 3. **Filtros Avanzados**

- **Selector personalizado de fechas** dentro del rango con datos (01/12/2010 - 24/10/2025)
- Presets: 7 días, 30 días, 90 días, 1 año, histórico completo (contados hacia atrás desde la última fecha con datos)
- Filtros multidimensionales:
  - Geografía (países, regiones)
  - Productos (categorías, subcategorías)
  - Clientes (segmentos)
  - Canal (método pago, dispositivo, tráfico)
  - Rango de precios

---

## 📊 Datos

### Fuentes de Datos

- **Transacciones:** 472.211 registros. Las de 2010-2011 proceden del dataset público *Online Retail* (UCI); las de
  2012-2025 son sintéticas, generadas para extender la serie temporal.
- **Clientes:** 4.338 clientes únicos de 43 países
- **Productos:** 29.120 productos en 8 categorías

### Formato

- **Principal:** Parquet (ocupa poco y se lee rápido)
- **Backup:** PostgreSQL (opcional)

---

## 🛠️ Tecnologías

- **Dashboard:** Streamlit, pandas, NumPy
- **Visualización:** Plotly
- **Machine learning:** scikit-learn (Isolation Forest, K-Means)
- **API y base de datos (opcionales):** FastAPI, SQLAlchemy, PostgreSQL

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para la API opcional: `pip install -r requirements-api.txt` y `uvicorn api.main:app`.

## Desplegar en Streamlit Community Cloud

Repositorio `carlosmsr92/ecommerce-analytics`, rama `main`, archivo principal **`app.py`**. Los datos se leen de los
Parquet de `data/`; no hace falta base de datos.

---

## 🤝 Contribuciones

Este es un proyecto personal de **CMSR92**. Si encuentras bugs o tienes sugerencias, abre un issue.

---

## 📄 Licencia

[MIT](LICENSE) © 2025 Carlos Manuel Suárez Rivero (CMSR92)

---

## 👤 Autor

**Carlos Manuel Suárez Rivero (CMSR92)** · [LinkedIn](https://www.linkedin.com/in/cmsr92) · [Portfolio](https://carlosmsr92.github.io/cmsr92/)
