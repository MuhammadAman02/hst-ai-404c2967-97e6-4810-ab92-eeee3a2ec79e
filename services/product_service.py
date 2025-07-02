"""Product Service Layer"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models.schemas import Product, ProductCreate, ProductUpdate, ProductDB
from core.database import get_session
import logging

logger = logging.getLogger(__name__)

class ProductService:
    """Service for managing products"""
    
    async def get_all_products(self) -> List[Product]:
        """Get all products"""
        session = get_session()
        try:
            products = session.query(ProductDB).all()
            return [Product.from_orm(product) for product in products]
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            raise
        finally:
            session.close()
    
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        session = get_session()
        try:
            product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
            return Product.from_orm(product) if product else None
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            raise
        finally:
            session.close()
    
    async def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        session = get_session()
        try:
            products = session.query(ProductDB).filter(ProductDB.category == category).all()
            return [Product.from_orm(product) for product in products]
        except Exception as e:
            logger.error(f"Error getting products by category {category}: {e}")
            raise
        finally:
            session.close()
    
    async def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        session = get_session()
        try:
            db_product = ProductDB(**product_data.dict())
            session.add(db_product)
            session.commit()
            session.refresh(db_product)
            return Product.from_orm(db_product)
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating product: {e}")
            raise
        finally:
            session.close()
    
    async def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        session = get_session()
        try:
            db_product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
            if not db_product:
                return None
            
            update_data = product_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_product, field, value)
            
            session.commit()
            session.refresh(db_product)
            return Product.from_orm(db_product)
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating product {product_id}: {e}")
            raise
        finally:
            session.close()
    
    async def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        session = get_session()
        try:
            db_product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
            if not db_product:
                return False
            
            session.delete(db_product)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting product {product_id}: {e}")
            raise
        finally:
            session.close()
    
    async def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        session = get_session()
        try:
            products = session.query(ProductDB).filter(
                ProductDB.name.contains(query) | 
                ProductDB.description.contains(query)
            ).all()
            return [Product.from_orm(product) for product in products]
        except Exception as e:
            logger.error(f"Error searching products with query '{query}': {e}")
            raise
        finally:
            session.close()