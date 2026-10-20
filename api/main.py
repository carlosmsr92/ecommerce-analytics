from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime, timedelta
import pandas as pd
from database.schema import get_engine
from pydantic import BaseModel
from sqlalchemy import text
from api.ml_endpoints import router as ml_router

app = FastAPI(
    title="Global Ecommerce Analytics API",
    description="API REST para análisis de ecommerce con Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ML router
app.include_router(ml_router)

# Models
class KPIResponse(BaseModel):
    total_revenue: float
    total_orders: int
    avg_order_value: float
    gross_profit: float
    total_customers: int
    conversion_rate: float
    period_start: str
    period_end: str

class TransactionResponse(BaseModel):
    transaction_id: str
    date: datetime
    customer_id: str
    country: str
    product_name: str
    category: str
    total_amount_usd: float
    payment_method: str

class CustomerResponse(BaseModel):
    customer_id: str
    country: str
    lifetime_value: float
    total_orders: int
    rfm_segment: str
    churn_probability: float

class ProductResponse(BaseModel):
    product_id: str
    product_name: str
    category: str
    base_price: float
    margin_percentage: float
    rating: float

# Helper function
def get_db_engine():
    return get_engine()

@app.get("/")
def read_root():
    return {
        "message": "Global Ecommerce Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "kpis": "/api/kpis",
            "transactions": "/api/transactions",
            "customers": "/api/customers",
            "products": "/api/products",
            "countries": "/api/analytics/countries",
            "categories": "/api/analytics/categories"
        }
    }

@app.get("/api/kpis", response_model=KPIResponse)
def get_kpis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    country: Optional[str] = Query(None, description="Filter by country"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Obtiene KPIs principales del ecommerce - SECURED with parameterized queries
    """
    engine = get_db_engine()
    
    # Fechas por defecto
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Query base con parámetros
    query = text("""
    SELECT 
        COUNT(*) as total_orders,
        SUM(total_amount_usd) as total_revenue,
        AVG(total_amount_usd) as avg_order_value,
        SUM(profit) as gross_profit,
        COUNT(DISTINCT customer_id) as total_customers
    FROM transactions
    WHERE date >= :start_date AND date <= :end_date
    """ + (" AND country = :country" if country else "") +
          (" AND category = :category" if category else ""))
    
    params = {"start_date": start_date, "end_date": end_date}
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query, params)
            row = result.fetchone()
            
            if row is None:
                raise HTTPException(status_code=404, detail="No data found")
            
            total_customers = float(row[4]) if row[4] else 1
            total_orders = float(row[0]) if row[0] else 0
            
            return KPIResponse(
                total_revenue=float(row[1] or 0),
                total_orders=int(row[0] or 0),
                avg_order_value=float(row[2] or 0),
                gross_profit=float(row[3] or 0),
                total_customers=int(total_customers),
                conversion_rate=round((total_orders / total_customers) * 100, 2) if total_customers > 0 else 0,
                period_start=start_date,
                period_end=end_date
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/transactions")
def get_transactions(
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
    country: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Obtiene transacciones con paginación y filtros - SECURED
    """
    engine = get_db_engine()
    
    # Construir query con condiciones dinámicas pero parámetros seguros
    where_clauses = []
    params = {}
    
    if start_date:
        where_clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("date <= :end_date")
        params["end_date"] = end_date
    if country:
        where_clauses.append("country = :country")
        params["country"] = country
    if category:
        where_clauses.append("category = :category")
        params["category"] = category
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT * FROM transactions
    {where_sql}
    ORDER BY date DESC
    LIMIT :limit OFFSET :offset
    """)
    
    params["limit"] = limit
    params["offset"] = offset
    
    try:
        df = pd.read_sql_query(query, engine, params=params)
        return {
            "total": len(df),
            "limit": limit,
            "offset": offset,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
    country: Optional[str] = None,
    rfm_segment: Optional[str] = None,
    min_ltv: Optional[float] = None
):
    """
    Obtiene clientes con filtros - SECURED
    """
    engine = get_db_engine()
    
    where_clauses = []
    params = {}
    
    if country:
        where_clauses.append("country = :country")
        params["country"] = country
    if rfm_segment:
        where_clauses.append("rfm_segment = :rfm_segment")
        params["rfm_segment"] = rfm_segment
    if min_ltv is not None:
        where_clauses.append("lifetime_value >= :min_ltv")
        params["min_ltv"] = min_ltv
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT * FROM customers
    {where_sql}
    ORDER BY lifetime_value DESC
    LIMIT :limit OFFSET :offset
    """)
    
    params["limit"] = limit
    params["offset"] = offset
    
    try:
        df = pd.read_sql_query(query, engine, params=params)
        return {
            "total": len(df),
            "limit": limit,
            "offset": offset,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
def get_products(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    category: Optional[str] = None,
    min_rating: Optional[float] = None
):
    """
    Obtiene productos con filtros - SECURED
    """
    engine = get_db_engine()
    
    where_clauses = []
    params = {}
    
    if category:
        where_clauses.append("category = :category")
        params["category"] = category
    if min_rating is not None:
        where_clauses.append("rating >= :min_rating")
        params["min_rating"] = min_rating
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT * FROM products
    {where_sql}
    ORDER BY rating DESC
    LIMIT :limit OFFSET :offset
    """)
    
    params["limit"] = limit
    params["offset"] = offset
    
    try:
        df = pd.read_sql_query(query, engine, params=params)
        return {
            "total": len(df),
            "limit": limit,
            "offset": offset,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/countries")
def get_country_analytics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Análisis de revenue por país - SECURED
    """
    engine = get_db_engine()
    
    where_clauses = []
    params = {}
    
    if start_date:
        where_clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("date <= :end_date")
        params["end_date"] = end_date
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT 
        country,
        COUNT(*) as orders,
        SUM(total_amount_usd) as revenue,
        AVG(total_amount_usd) as aov,
        COUNT(DISTINCT customer_id) as customers
    FROM transactions
    {where_sql}
    GROUP BY country
    ORDER BY revenue DESC
    """)
    
    try:
        df = pd.read_sql_query(query, engine, params=params if params else None)
        return {
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/categories")
def get_category_analytics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Análisis de revenue por categoría - SECURED
    """
    engine = get_db_engine()
    
    where_clauses = []
    params = {}
    
    if start_date:
        where_clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("date <= :end_date")
        params["end_date"] = end_date
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT 
        category,
        COUNT(*) as orders,
        SUM(total_amount_usd) as revenue,
        SUM(profit) as profit,
        AVG((profit / NULLIF(total_amount_usd, 0)) * 100) as avg_margin
    FROM transactions
    {where_sql}
    GROUP BY category
    ORDER BY revenue DESC
    """)
    
    try:
        df = pd.read_sql_query(query, engine, params=params if params else None)
        return {
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/time-series")
def get_time_series(
    granularity: str = Query("day", description="day, week, or month"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Serie temporal de revenue y orders - SECURED
    """
    engine = get_db_engine()
    
    # Validar granularity (whitelist approach)
    granularity_map = {
        'day': "DATE(date)",
        'week': "DATE_TRUNC('week', date)",
        'month': "DATE_TRUNC('month', date)"
    }
    
    if granularity not in granularity_map:
        raise HTTPException(status_code=400, detail="Invalid granularity. Use: day, week, or month")
    
    date_format = granularity_map[granularity]
    
    where_clauses = []
    params = {}
    
    if start_date:
        where_clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("date <= :end_date")
        params["end_date"] = end_date
    
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = text(f"""
    SELECT 
        {date_format} as period,
        COUNT(*) as orders,
        SUM(total_amount_usd) as revenue,
        SUM(profit) as profit
    FROM transactions
    {where_sql}
    GROUP BY {date_format}
    ORDER BY period
    """)
    
    try:
        df = pd.read_sql_query(query, engine, params=params if params else None)
        df['period'] = df['period'].astype(str)
        return {
            "granularity": granularity,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/top-products")
def get_top_products(
    limit: int = Query(20, le=100),
    metric: str = Query("revenue", description="revenue, orders, or margin")
):
    """
    Top productos por métrica seleccionada - SECURED
    """
    engine = get_db_engine()
    
    # Whitelist approach para métrica
    metric_map = {
        'revenue': 'SUM(total_amount_usd)',
        'orders': 'COUNT(*)',
        'margin': 'AVG(profit / NULLIF(total_amount_usd, 0) * 100)'
    }
    
    if metric not in metric_map:
        raise HTTPException(status_code=400, detail="Invalid metric. Use: revenue, orders, or margin")
    
    metric_sql = metric_map[metric]
    
    query = text(f"""
    SELECT 
        product_id,
        product_name,
        category,
        COUNT(*) as orders,
        SUM(total_amount_usd) as revenue,
        SUM(profit) as profit,
        SUM(quantity) as units_sold
    FROM transactions
    GROUP BY product_id, product_name, category
    ORDER BY {metric_sql} DESC
    LIMIT :limit
    """)
    
    try:
        df = pd.read_sql_query(query, engine, params={"limit": limit})
        return {
            "metric": metric,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/export/excel")
def export_excel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Exporta datos a Excel con análisis completo - SECURED
    """
    from fastapi.responses import StreamingResponse
    from utils.export_utils import create_excel_report
    
    try:
        engine = get_db_engine()
        
        # Construir query con parámetros seguros
        where_clauses = []
        params = {}
        
        if start_date:
            where_clauses.append("date >= :start_date")
            params["start_date"] = start_date
        if end_date:
            where_clauses.append("date <= :end_date")
            params["end_date"] = end_date
        if country:
            where_clauses.append("country = :country")
            params["country"] = country
        if category:
            where_clauses.append("category = :category")
            params["category"] = category
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        transactions_query = text(f"SELECT * FROM transactions {where_sql}")
        
        transactions_df = pd.read_sql_query(transactions_query, engine, params=params if params else None)
        customers_df = pd.read_sql_table('customers', engine)
        products_df = pd.read_sql_table('products', engine)
        
        # Generar Excel
        excel_buffer = create_excel_report(transactions_df, customers_df, products_df, {})
        
        return StreamingResponse(
            excel_buffer,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': f'attachment; filename=ecommerce_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando Excel: {str(e)}")

@app.get("/api/export/pdf")
def export_pdf(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Exporta reporte en PDF profesional - SECURED
    """
    from fastapi.responses import StreamingResponse
    from utils.export_utils import create_pdf_report
    
    try:
        engine = get_db_engine()
        
        # Construir query con parámetros seguros
        where_clauses = []
        params = {}
        
        if start_date:
            where_clauses.append("date >= :start_date")
            params["start_date"] = start_date
        if end_date:
            where_clauses.append("date <= :end_date")
            params["end_date"] = end_date
        if country:
            where_clauses.append("country = :country")
            params["country"] = country
        if category:
            where_clauses.append("category = :category")
            params["category"] = category
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        transactions_query = text(f"SELECT * FROM transactions {where_sql}")
        
        transactions_df = pd.read_sql_query(transactions_query, engine, params=params if params else None)
        customers_df = pd.read_sql_table('customers', engine)
        products_df = pd.read_sql_table('products', engine)
        
        # Generar PDF
        pdf_buffer = create_pdf_report(transactions_df, customers_df, products_df, {})
        
        return StreamingResponse(
            pdf_buffer,
            media_type='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=ecommerce_report_{datetime.now().strftime("%Y%m%d")}.pdf'
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
