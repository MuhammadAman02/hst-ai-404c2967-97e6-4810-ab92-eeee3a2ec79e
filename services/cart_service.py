"""Cart Service Layer"""

from typing import List
from sqlalchemy.orm import Session
from models.schemas import CartItem, CartItemCreate, CartItemDB, ProductDB, CartSummary
from core.database import get_session
from app.config import settings
import uuid
import logging

logger = logging.getLogger(__name__)

class CartService:
    """Service for managing shopping cart"""
    
    def __init__(self):
        # For demo purposes, using a simple session ID
        # In production, this would be tied to user sessions
        self.session_id = str(uuid.uuid4())
    
    async def get_cart_items(self) -> List[CartItem]:
        """Get all items in cart"""
        session = get_session()
        try:
            cart_items = session.query(CartItemDB, ProductDB).join(
                ProductDB, CartItemDB.product_id == ProductDB.id
            ).filter(CartItemDB.session_id == self.session_id).all()
            
            result = []
            for cart_item, product in cart_items:
                result.append(CartItem(
                    id=cart_item.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    session_id=cart_item.session_id,
                    product_name=product.name,
                    price=product.price,
                    created_at=cart_item.created_at
                ))
            
            return result
        except Exception as e:
            logger.error(f"Error getting cart items: {e}")
            raise
        finally:
            session.close()
    
    async def add_to_cart(self, product_id: int, quantity: int = 1) -> CartItem:
        """Add item to cart"""
        session = get_session()
        try:
            # Check if item already exists in cart
            existing_item = session.query(CartItemDB).filter(
                CartItemDB.product_id == product_id,
                CartItemDB.session_id == self.session_id
            ).first()
            
            if existing_item:
                # Update quantity
                existing_item.quantity += quantity
                session.commit()
                session.refresh(existing_item)
                
                # Get product info
                product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
                return CartItem(
                    id=existing_item.id,
                    product_id=existing_item.product_id,
                    quantity=existing_item.quantity,
                    session_id=existing_item.session_id,
                    product_name=product.name,
                    price=product.price,
                    created_at=existing_item.created_at
                )
            else:
                # Create new cart item
                cart_item = CartItemDB(
                    product_id=product_id,
                    quantity=quantity,
                    session_id=self.session_id
                )
                session.add(cart_item)
                session.commit()
                session.refresh(cart_item)
                
                # Get product info
                product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
                return CartItem(
                    id=cart_item.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    session_id=cart_item.session_id,
                    product_name=product.name,
                    price=product.price,
                    created_at=cart_item.created_at
                )
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding to cart: {e}")
            raise
        finally:
            session.close()
    
    async def update_quantity(self, product_id: int, quantity: int) -> bool:
        """Update item quantity in cart"""
        session = get_session()
        try:
            cart_item = session.query(CartItemDB).filter(
                CartItemDB.product_id == product_id,
                CartItemDB.session_id == self.session_id
            ).first()
            
            if not cart_item:
                return False
            
            if quantity <= 0:
                session.delete(cart_item)
            else:
                cart_item.quantity = quantity
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating cart quantity: {e}")
            raise
        finally:
            session.close()
    
    async def remove_from_cart(self, product_id: int) -> bool:
        """Remove item from cart"""
        session = get_session()
        try:
            cart_item = session.query(CartItemDB).filter(
                CartItemDB.product_id == product_id,
                CartItemDB.session_id == self.session_id
            ).first()
            
            if not cart_item:
                return False
            
            session.delete(cart_item)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error removing from cart: {e}")
            raise
        finally:
            session.close()
    
    async def clear_cart(self) -> bool:
        """Clear all items from cart"""
        session = get_session()
        try:
            session.query(CartItemDB).filter(
                CartItemDB.session_id == self.session_id
            ).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error clearing cart: {e}")
            raise
        finally:
            session.close()
    
    async def get_cart_summary(self) -> CartSummary:
        """Get cart summary with totals"""
        cart_items = await self.get_cart_items()
        
        total_items = sum(item.quantity for item in cart_items)
        subtotal = sum(item.price * item.quantity for item in cart_items)
        tax = subtotal * settings.TAX_RATE
        total = subtotal + tax
        
        return CartSummary(
            items=cart_items,
            total_items=total_items,
            subtotal=subtotal,
            tax=tax,
            total=total
        )