from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(50), unique=True, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    customer_id = Column(String(50), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    region = Column(String(100))
    city = Column(String(100))
    product_id = Column(String(50), nullable=False, index=True)
    product_name = Column(String(500))
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    discount_applied = Column(Float)
    payment_method = Column(String(50), index=True)
    shipping_cost = Column(Float)
    delivery_time = Column(Integer)
    customer_segment = Column(String(50), index=True)
    device_type = Column(String(50), index=True)
    traffic_source = Column(String(50), index=True)
    currency = Column(String(10))
    exchange_rate = Column(Float)
    total_amount_usd = Column(Float, index=True)
    cost_price = Column(Float)
    profit = Column(Float)

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), unique=True, nullable=False, index=True)
    registration_date = Column(Date, nullable=False)
    country = Column(String(100), index=True)
    age = Column(Integer)
    gender = Column(String(20))
    lifetime_value = Column(Float, index=True)
    total_orders = Column(Integer)
    avg_order_value = Column(Float)
    last_purchase_date = Column(DateTime)
    recency_score = Column(Integer)
    frequency_score = Column(Integer)
    monetary_score = Column(Float)
    rfm_segment = Column(String(50), index=True)
    churn_probability = Column(Float)
    preferred_category = Column(String(100))

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100))
    brand = Column(String(100))
    base_price = Column(Float)
    cost_price = Column(Float)
    margin_percentage = Column(Float)
    stock_quantity = Column(Integer)
    supplier_country = Column(String(100))
    weight = Column(Float)
    rating = Column(Float)
    reviews_count = Column(Integer)
    launch_date = Column(Date)

# Database connection
def get_database_url():
    return os.getenv('DATABASE_URL', 'postgresql://localhost/ecommerce_db')

def get_engine():
    return create_engine(get_database_url())

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✅ Tablas creadas exitosamente")

def drop_tables():
    engine = get_engine()
    Base.metadata.drop_all(engine)
    print("🗑️ Tablas eliminadas")
