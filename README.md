# 📊 Análisis global de e-commerce

**Dashboard profesional de Business Intelligence con Machine Learning y Análisis Estadístico para E-commerce Global**

> Autor: **Carlos Manuel Suárez Rivero (CMSR92)**  
> Plataforma: Streamlit (dashboard) · FastAPI y PostgreSQL opcionales

---

## 🎯 Descripción

Plataforma avanzada de Business Intelligence que analiza **472.211 transacciones** (diciembre de 2010 a octubre de 2025) con capacidades de:

- **9 Tabs de Análisis** interactivos y profesionales
- **4 Modelos de Machine Learning** (Isolation Forest, K-Means, Correlación, Recomendaciones)
- **Análisis Estadístico Robusto** con promedios móviles e indicadores de crecimiento
- **100% Internacionalizado** en español profesional
- **Filtros Avanzados** multi-dimensionales con selector personalizado de fechas

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
| 🏠 **Resumen General** | KPIs principales, insights ejecutivos, evolución temporal |
| 🌍 **Análisis Geográfico** | Mapas interactivos, distribución por país/región |
| 📈 **Rendimiento & Análisis Temporal** | Indicadores de crecimiento, promedios móviles, momentum |
| 📦 **Análisis de Productos** | BCG Matrix, categorías top, subcategorías |
| 👥 **Segmentación de Clientes** | RFM, K-Means clustering, análisis de cohortes |
| 📱 **Análisis de Canal** | Diagramas Sankey, conversión por dispositivo |
| 🤖 **Machine Learning e IA** | Isolation Forest, anomalías, correlaciones |
| 💰 **Análisis Financiero** | P&L waterfall, márgenes, rentabilidad |
| ⚙️ **Métricas Operacionales** | Logística, cumplimiento, satisfacción |

### 2. **Machine Learning**

- **Isolation Forest:** Detección de anomalías en transacciones
- **K-Means:** Segmentación automática de clientes (RFM)
- **Análisis de Correlación:** Identificación de patrones ocultos
- **Sistema de Recomendaciones:** Productos relacionados

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

- **Primario:** Parquet (optimizado para performance)
- **Backup:** PostgreSQL (opcional)

---

## 🛠️ Tecnologías

- **Dashboard:** Streamlit, pandas, NumPy
- **Visualización:** Plotly, Folium, Matplotlib, Seaborn
- **Machine learning:** scikit-learn (Isolation Forest, K-Means), XGBoost
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
