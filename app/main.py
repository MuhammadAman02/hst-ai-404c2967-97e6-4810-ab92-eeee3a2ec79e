"""
Apple Store - Main Application
Beautiful e-commerce interface with Apple-inspired design
"""

from nicegui import ui, app
import asyncio
from typing import Dict, List, Optional
import os

from core.database import init_database, get_session
from models.schemas import Product, CartItem
from services.product_service import ProductService
from services.cart_service import CartService
from app.components.product_card import ProductCard
from app.components.cart_sidebar import CartSidebar
from app.components.admin_panel import AdminPanel
from app.config import settings

# Global services
product_service = ProductService()
cart_service = CartService()

# Add custom CSS for Apple-inspired design
ui.add_head_html('''
<style>
    :root {
        --apple-blue: #007AFF;
        --apple-gray: #8E8E93;
        --apple-light-gray: #F2F2F7;
        --apple-dark: #1C1C1E;
        --apple-white: #FFFFFF;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 0;
        padding: 0;
    }
    
    .apple-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .apple-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: none;
    }
    
    .apple-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .apple-button {
        background: var(--apple-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .apple-button:hover {
        background: #0056CC;
        transform: scale(1.02);
    }
    
    .apple-button-secondary {
        background: var(--apple-light-gray);
        color: var(--apple-dark);
        border: 1px solid var(--apple-gray);
    }
    
    .apple-button-secondary:hover {
        background: #E5E5EA;
    }
    
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 24px;
        padding: 24px;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 80px 20px;
        margin-bottom: 40px;
    }
    
    .cart-badge {
        background: #FF3B30;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        top: -8px;
        right: -8px;
    }
    
    .price-tag {
        font-size: 24px;
        font-weight: 700;
        color: var(--apple-blue);
    }
    
    .category-nav {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .loading-spinner {
        border: 3px solid var(--apple-light-gray);
        border-top: 3px solid var(--apple-blue);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .error-message {
        background: #FF3B30;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 10px;
        text-align: center;
    }
    
    .success-message {
        background: #34C759;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 10px;
        text-align: center;
    }
</style>
''')

class AppleStore:
    def __init__(self):
        self.current_category = "All"
        self.cart_visible = False
        self.products: List[Product] = []
        self.cart_items: List[CartItem] = []
        self.loading = False
        
    async def load_products(self):
        """Load products from database"""
        try:
            self.loading = True
            self.products = await product_service.get_all_products()
            self.cart_items = await cart_service.get_cart_items()
        except Exception as e:
            ui.notify(f"Error loading products: {str(e)}", type='negative')
        finally:
            self.loading = False

    async def add_to_cart(self, product: Product):
        """Add product to cart"""
        try:
            await cart_service.add_to_cart(product.id, 1)
            self.cart_items = await cart_service.get_cart_items()
            ui.notify(f"Added {product.name} to cart!", type='positive')
        except Exception as e:
            ui.notify(f"Error adding to cart: {str(e)}", type='negative')

    async def filter_by_category(self, category: str):
        """Filter products by category"""
        self.current_category = category
        if category == "All":
            self.products = await product_service.get_all_products()
        else:
            self.products = await product_service.get_products_by_category(category)

store = AppleStore()

@ui.page('/')
async def index():
    """Main store page"""
    await store.load_products()
    
    # Header
    with ui.row().classes('w-full apple-header').style('position: sticky; top: 0; z-index: 100; padding: 16px 24px;'):
        with ui.row().classes('w-full items-center justify-between'):
            # Logo and title
            with ui.row().classes('items-center gap-4'):
                ui.icon('apple', size='2rem').style('color: #000;')
                ui.label('Apple Store').classes('text-2xl font-bold')
            
            # Navigation
            with ui.row().classes('items-center gap-6'):
                for category in ['All', 'iPhone', 'iPad', 'Mac', 'Watch', 'AirPods']:
                    ui.button(
                        category, 
                        on_click=lambda cat=category: store.filter_by_category(cat)
                    ).props('flat').classes('text-gray-700 hover:text-blue-600')
                
                # Cart button
                with ui.element('div').style('position: relative;'):
                    cart_btn = ui.button(
                        icon='shopping_cart',
                        on_click=lambda: setattr(store, 'cart_visible', not store.cart_visible)
                    ).props('round').classes('apple-button')
                    
                    # Cart badge
                    if len(store.cart_items) > 0:
                        ui.element('div').classes('cart-badge').text(str(len(store.cart_items)))
                
                # Admin button
                ui.button('Admin', on_click=lambda: ui.navigate.to('/admin')).props('outline')

    # Hero Section
    with ui.element('div').classes('hero-section'):
        ui.label('Think Different').classes('text-5xl font-bold mb-4')
        ui.label('Discover the latest Apple products with innovative technology').classes('text-xl opacity-90')

    # Category Navigation
    with ui.element('div').classes('category-nav'):
        with ui.row().classes('w-full justify-center gap-4'):
            for category in ['All', 'iPhone', 'iPad', 'Mac', 'Watch', 'AirPods', 'Accessories']:
                ui.button(
                    category,
                    on_click=lambda cat=category: store.filter_by_category(cat)
                ).classes('apple-button-secondary' if category != store.current_category else 'apple-button')

    # Loading indicator
    if store.loading:
        with ui.element('div').classes('loading-spinner'):
            pass

    # Products Grid
    with ui.element('div').classes('product-grid'):
        for product in store.products:
            ProductCard(product, store.add_to_cart)

    # Cart Sidebar
    if store.cart_visible:
        CartSidebar(store.cart_items, cart_service)

    # Footer
    with ui.element('footer').style('background: #1C1C1E; color: white; padding: 40px 20px; margin-top: 60px;'):
        with ui.row().classes('w-full justify-center'):
            ui.label('© 2024 Apple Store. All rights reserved.').classes('text-center')

@ui.page('/admin')
async def admin():
    """Admin panel for managing products"""
    AdminPanel(product_service)

@ui.page('/health')
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Apple Store"}

def main():
    """Main application entry point"""
    # Initialize database
    init_database()
    
    # Configure NiceGUI
    ui.run(
        host=settings.HOST,
        port=settings.PORT,
        title=settings.STORE_NAME,
        favicon='🍎',
        dark=False,
        show=False,
        reload=settings.DEBUG
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()