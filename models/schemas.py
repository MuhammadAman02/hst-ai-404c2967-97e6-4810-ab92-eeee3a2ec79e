"""Pydantic Models and Database Schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Database Models
class ProductDB(Base):
    """Product database model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    stock = Column(Integer, default=0)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CartItemDB(Base):
    """Cart item database model"""
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    session_id = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    product = relationship("ProductDB")

# Pydantic Models
class ProductBase(BaseModel):
    """Base product model"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    """Product creation model"""
    pass

class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

class Product(ProductBase):
    """Product response model"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    """Base cart item model"""
    product_id: int
    quantity: int = Field(default=1, gt=0)

class CartItemCreate(CartItemBase):
    """Cart item creation model"""
    session_id: str

class CartItem(CartItemBase):
    """Cart item response model"""
    id: int
    session_id: str
    product_name: str
    price: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class CartSummary(BaseModel):
    """Cart summary model"""
    items: List[CartItem]
    total_items: int
    subtotal: float
    tax: float
    total: float