from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.database import Base

Base = declarative_base()

# Recipe 모델
class Recipe(Base):
    __tablename__ = "recipe"
    recipe_id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price_id = Column(Integer, ForeignKey("priceRange.price_id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), nullable=False)
    cstore_id = Column(Integer, ForeignKey("storeType.cstore_id"), nullable=False)

    # 관계
    price = relationship("PriceRange", back_populates="recipes")
    keyword = relationship("Keyword", back_populates="recipes")
    cstore = relationship("StoreType", back_populates="recipes")

# Keyword 모델
class Keyword(Base):
    __tablename__ = "keyword"
    keyword_id = Column(Integer, primary_key=True, index=True)
    keyword_name = Column(String(255), nullable=False)

    # 관계
    recipes = relationship("Recipe", back_populates="keyword")

# PriceRange 모델
class PriceRange(Base):
    __tablename__ = "priceRange"
    price_id = Column(Integer, primary_key=True, index=True)
    price_name = Column(String(255), nullable=False)

    # 관계
    recipes = relationship("Recipe", back_populates="price")

# StoreType 모델
class StoreType(Base):
    __tablename__ = "storeType"
    cstore_id = Column(Integer, primary_key=True, index=True)
    cstore_name = Column(String(255), nullable=False)

    # 관계
    recipes = relationship("Recipe", back_populates="cstore")

# Store 모델
class Store(Base):
    __tablename__ = "store"
    store_id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)