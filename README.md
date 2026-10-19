# 📊 Análisis global de e-commerce

**Dashboard profesional de Business Intelligence con Machine Learning y Análisis Estadístico para E-commerce Global**

> Autor: **Carlos Manuel Suárez Rivero (CMSR92)**  
> Plataforma: Streamlit (dashboard) · FastAPI y PostgreSQL opcionales

---

## 🎯 Descripción

Plataforma avanzada de Business Intelligence que analiza más de **774,000 transacciones** (2015-2025) con capacidades de:

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
├── requirements.txt                # Dependencias Python
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
│   ├── export_utils.py            # Exportación de informes
│   └── visualizaciones_avanzadas.py
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
| 🤖 **ML & IA Insights** | Isolation Forest, anomalías, correlaciones |
| 💰 **Análisis Financiero** | P&L waterfall, márgenes, rentabilidad |
| ⚙️ **Métricas Operacionales** | Logística, cumplimiento, satisfacción |

### 2. **Machine Learning**

- **Isolation Forest:** Detección de anomalías en transacciones
- **K-Means:** Segmentación automática de clientes (RFM)
- **Análisis de Correlación:** Identificación de patrones ocultos
- **Sistema de Recomendaciones:** Productos relacionados

### 3. **Filtros Avanzados**

- **Selector Personalizado de Fechas** (29/10/2015 - 26/10/2025)
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

- **Transactions:** 774,434 registros (541,909 reales + 232,525 sintéticos)
- **Customers:** 100,000 clientes únicos
- **Products:** 1,000 productos en 15 categorías

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

---

## 🤝 Contribuciones

Este es un proyecto personal de **CMSR92**. Si encuentras bugs o tienes sugerencias, abre un issue.

---

## 📄 Licencia

[MIT](LICENSE) © 2025 Carlos Manuel Suárez Rivero (CMSR92)

---

## 👤 Autor

**Carlos Manuel Suárez Rivero (CMSR92)**  
[LinkedIn](https://www.linkedin.com/in/cmsr92) · [Portfolio](https://carlosmsr92.github.io/cmsr92/)

---
**Desarrollado con ❤️ para la comunidad de Data Science y Business Intelligence**
