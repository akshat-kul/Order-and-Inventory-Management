from sqlalchemy import Float, create_engine, Boolean, TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:root@localhost/postgres"

Base = declarative_base()

engine = create_engine(DB_URL, pool_recycle=3600, connect_args={'connect_timeout': 60})
session = sessionmaker(bind=engine)

class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(60))
    admin = Column(Boolean)
    signup_date = Column(TIMESTAMP)

class Products(Base):
    __tablename__ = 'products'
    item_id = Column(Integer, primary_key = True, autoincrement=True)
    id = Column(Integer)
    product = Column(String(100))
    price = Column(Float)

class Orders(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key =True)
    product_name = Column(String(100))
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(TIMESTAMP)

Base.metadata.create_all(engine)