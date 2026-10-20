from fastapi import APIRouter, HTTPException, Query
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from database.schema import get_engine
from pydantic import BaseModel

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

# Response Models
class ForecastResponse(BaseModel):
    dates: List[str]
    predictions: List[float]
    lower_bound: List[float]
    upper_bound: List[float]
    model_metrics: dict

class ClusterResponse(BaseModel):
    customer_id: str
    cluster: int
    cluster_name: str
    characteristics: dict

class ChurnResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str
    recommended_action: str

class RecommendationResponse(BaseModel):
    product_id: str
    product_name: str
    category: str
    score: float
    reason: str

class DemandForecastResponse(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    forecasted_demand_30d: int
    forecasted_demand_60d: int
    forecasted_demand_90d: int
    stock_out_risk: str
    recommended_reorder: int

@router.post("/forecast")
def create_forecast(
    days_ahead: int = Query(90, ge=7, le=180),
    metric: str = Query("revenue", description="revenue or orders")
):
    """
    Genera forecast usando Prophet para revenue o orders
    """
    try:
        from prophet import Prophet
        
        engine = get_engine()
        
        # Obtener datos históricos
        query = f"""
        SELECT 
            DATE(date) as ds,
            {'SUM(total_amount_usd)' if metric == 'revenue' else 'COUNT(*)'} as y
        FROM transactions
        GROUP BY DATE(date)
        ORDER BY ds
        """
        
        df = pd.read_sql_query(query, engine)
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Entrenar Prophet
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            interval_width=0.95
        )
        model.fit(df)
        
        # Generar forecast
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)
        
        # Calcular métricas
        from sklearn.metrics import mean_squared_error, r2_score
        
        y_true = df['y'].values
        y_pred = forecast.iloc[:len(df)]['yhat'].values
        
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        # Extraer predicciones futuras
        future_forecast = forecast.tail(days_ahead)
        
        return ForecastResponse(
            dates=[d.strftime('%Y-%m-%d') for d in future_forecast['ds']],
            predictions=future_forecast['yhat'].tolist(),
            lower_bound=future_forecast['yhat_lower'].tolist(),
            upper_bound=future_forecast['yhat_upper'].tolist(),
            model_metrics={
                'mape': round(mape, 2),
                'rmse': round(rmse, 2),
                'r2': round(r2, 3),
                'training_samples': len(df)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando forecast: {str(e)}")

@router.get("/clustering/customers")
def get_customer_clusters(
    n_clusters: int = Query(5, ge=3, le=10)
):
    """
    Clustering de clientes usando K-Means
    """
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        engine = get_engine()
        
        # Cargar datos de clientes
        query = """
        SELECT customer_id, recency_score, frequency_score, monetary_score,
               age, total_orders, avg_order_value
        FROM customers
        """
        df = pd.read_sql_query(query, engine)
        
        # Preparar features
        features = df[['recency_score', 'frequency_score', 'monetary_score', 
                       'age', 'total_orders', 'avg_order_value']]
        
        # Normalizar
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(features_scaled)
        
        # Características por cluster
        clusters_info = []
        cluster_names = ['High Value', 'Loyal', 'At Risk', 'New', 'Lost']
        
        for i in range(n_clusters):
            cluster_data = df[df['cluster'] == i]
            
            clusters_info.append({
                'cluster_id': i,
                'cluster_name': cluster_names[i] if i < len(cluster_names) else f'Cluster {i}',
                'size': len(cluster_data),
                'avg_monetary': round(cluster_data['monetary_score'].mean(), 2),
                'avg_frequency': round(cluster_data['frequency_score'].mean(), 2),
                'avg_recency': round(cluster_data['recency_score'].mean(), 2)
            })
        
        return {
            'n_clusters': n_clusters,
            'total_customers': len(df),
            'clusters': clusters_info
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en clustering: {str(e)}")

@router.get("/churn/at-risk")
def get_at_risk_customers(
    threshold: float = Query(0.7, ge=0.5, le=0.9),
    limit: int = Query(100, le=500)
):
    """
    Obtiene clientes con alto riesgo de churn - SECURED
    """
    try:
        from sqlalchemy import text
        engine = get_engine()
        
        query = text("""
        SELECT customer_id, country, lifetime_value, total_orders,
               last_purchase_date, churn_probability, rfm_segment
        FROM customers
        WHERE churn_probability >= :threshold
        ORDER BY churn_probability DESC, lifetime_value DESC
        LIMIT :limit
        """)
        
        df = pd.read_sql_query(query, engine, params={"threshold": threshold, "limit": limit})
        
        # Determinar nivel de riesgo y acción recomendada
        results = []
        for _, row in df.iterrows():
            risk_level = 'Critical' if row['churn_probability'] > 0.85 else 'High'
            
            if row['lifetime_value'] > 1000:
                action = 'Priority win-back campaign with personalized offer'
            elif row['total_orders'] > 10:
                action = 'Re-engagement email with discount'
            else:
                action = 'Survey to understand pain points'
            
            results.append(ChurnResponse(
                customer_id=row['customer_id'],
                churn_probability=round(row['churn_probability'], 3),
                risk_level=risk_level,
                recommended_action=action
            ))
        
        return {
            'threshold': threshold,
            'total_at_risk': len(results),
            'customers': [r.dict() for r in results]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo clientes en riesgo: {str(e)}")

@router.get("/recommendations/{product_id}")
def get_product_recommendations(
    product_id: str,
    top_n: int = Query(10, ge=5, le=20)
):
    """
    Recomendaciones de productos basadas en co-ocurrencia (Market Basket Analysis) - SECURED
    """
    try:
        from sqlalchemy import text
        engine = get_engine()
        
        # Obtener transacciones del producto
        query1 = text("""
        SELECT DISTINCT customer_id
        FROM transactions
        WHERE product_id = :product_id
        """)
        customers_df = pd.read_sql_query(query1, engine, params={"product_id": product_id})
        
        if len(customers_df) == 0:
            return {'message': 'Producto no encontrado', 'recommendations': []}
        
        customer_ids = customers_df['customer_id'].tolist()
        
        # Encontrar productos que estos clientes también compraron
        # Usar array binding para lista de customer_ids
        query2 = text("""
        SELECT 
            product_id,
            product_name,
            category,
            COUNT(DISTINCT customer_id) as customer_count,
            SUM(total_amount_usd) as total_revenue
        FROM transactions
        WHERE customer_id = ANY(:customer_ids)
            AND product_id != :product_id
        GROUP BY product_id, product_name, category
        ORDER BY customer_count DESC, total_revenue DESC
        LIMIT :top_n
        """)
        
        recommendations_df = pd.read_sql_query(query2, engine, params={
            "customer_ids": customer_ids,
            "product_id": product_id,
            "top_n": top_n
        })
        
        # Calcular score de recomendación
        total_customers = len(customers_df)
        recommendations = []
        
        for _, row in recommendations_df.iterrows():
            score = (row['customer_count'] / total_customers) * 100
            
            recommendations.append(RecommendationResponse(
                product_id=row['product_id'],
                product_name=row['product_name'],
                category=row['category'],
                score=round(score, 2),
                reason=f"{row['customer_count']} clientes que compraron este producto también compraron esto"
            ))
        
        return {
            'source_product_id': product_id,
            'total_customers_analyzed': total_customers,
            'recommendations': [r.dict() for r in recommendations]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando recomendaciones: {str(e)}")

@router.get("/demand-forecast")
def get_demand_forecast(
    top_n: int = Query(50, le=100)
):
    """
    Forecast de demanda por producto con alertas de stock-out - SECURED
    """
    try:
        from sqlalchemy import text
        engine = get_engine()
        
        # Obtener ventas históricas por producto
        query = text("""
        SELECT 
            t.product_id,
            t.product_name,
            t.category,
            p.stock_quantity,
            COUNT(*) as historical_orders,
            SUM(t.quantity) as total_units_sold,
            AVG(t.quantity) as avg_units_per_order
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        WHERE t.date >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY t.product_id, t.product_name, t.category, p.stock_quantity
        ORDER BY total_units_sold DESC
        LIMIT :top_n
        """)
        
        df = pd.read_sql_query(query, engine, params={"top_n": top_n})
        
        results = []
        
        for _, row in df.iterrows():
            # Calcular demanda promedio diaria
            daily_demand = row['total_units_sold'] / 90
            
            # Forecast simple (demanda promedio * días)
            forecast_30d = int(daily_demand * 30 * 1.1)  # +10% buffer
            forecast_60d = int(daily_demand * 60 * 1.1)
            forecast_90d = int(daily_demand * 90 * 1.1)
            
            # Determinar riesgo de stock-out
            current_stock = row['stock_quantity']
            
            if current_stock < forecast_30d:
                risk = 'Critical'
                reorder = forecast_60d - current_stock
            elif current_stock < forecast_60d:
                risk = 'High'
                reorder = forecast_60d - current_stock
            elif current_stock < forecast_90d:
                risk = 'Medium'
                reorder = max(0, forecast_90d - current_stock)
            else:
                risk = 'Low'
                reorder = 0
            
            results.append(DemandForecastResponse(
                product_id=row['product_id'],
                product_name=row['product_name'],
                current_stock=int(current_stock),
                forecasted_demand_30d=forecast_30d,
                forecasted_demand_60d=forecast_60d,
                forecasted_demand_90d=forecast_90d,
                stock_out_risk=risk,
                recommended_reorder=max(0, reorder)
            ))
        
        return {
            'total_products_analyzed': len(results),
            'critical_products': len([r for r in results if r.stock_out_risk == 'Critical']),
            'products': [r.dict() for r in results]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en demand forecast: {str(e)}")

@router.get("/anomalies")
def detect_anomalies(
    contamination: float = Query(0.05, ge=0.01, le=0.1),
    days_back: int = Query(90, ge=30, le=365)
):
    """
    Detección de anomalías en revenue diario usando Isolation Forest - SECURED
    """
    try:
        from sklearn.ensemble import IsolationForest
        from sqlalchemy import text
        
        engine = get_engine()
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        query = text("""
        SELECT 
            DATE(date) as day,
            COUNT(*) as orders,
            SUM(total_amount_usd) as revenue
        FROM transactions
        WHERE date >= :start_date
        GROUP BY DATE(date)
        ORDER BY day
        """)
        
        df = pd.read_sql_query(query, engine, params={"start_date": start_date})
        
        # Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        df['anomaly'] = iso_forest.fit_predict(df[['revenue', 'orders']])
        df['is_anomaly'] = df['anomaly'] == -1
        
        # Anomalías detectadas
        anomalies = df[df['is_anomaly']].copy()
        
        # Calcular desviación
        mean_revenue = df['revenue'].mean()
        anomalies['deviation_pct'] = ((anomalies['revenue'] - mean_revenue) / mean_revenue * 100).round(2)
        anomalies['severity'] = anomalies['deviation_pct'].abs().apply(
            lambda x: 'Critical' if x > 50 else 'High' if x > 25 else 'Medium'
        )
        
        return {
            'total_days_analyzed': len(df),
            'anomalies_detected': len(anomalies),
            'contamination_rate': contamination,
            'anomalies': anomalies[['day', 'revenue', 'orders', 'deviation_pct', 'severity']].to_dict(orient='records')
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detectando anomalías: {str(e)}")
