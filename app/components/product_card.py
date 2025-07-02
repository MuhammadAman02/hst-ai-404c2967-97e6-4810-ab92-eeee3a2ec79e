"""Product Card Component"""

from nicegui import ui
from models.schemas import Product
from typing import Callable, Awaitable

class ProductCard:
    """Apple-inspired product card component"""
    
    def __init__(self, product: Product, add_to_cart_callback: Callable[[Product], Awaitable[None]]):
        self.product = product
        self.add_to_cart = add_to_cart_callback
        self.render()
    
    def render(self):
        """Render the product card"""
        with ui.card().classes('apple-card').style('width: 300px; height: 400px; padding: 0; overflow: hidden;'):
            # Product Image
            with ui.element('div').style('height: 200px; background: #f8f9fa; display: flex; align-items: center; justify-content: center;'):
                if self.product.image_url:
                    ui.image(self.product.image_url).style('max-width: 100%; max-height: 100%; object-fit: contain;')
                else:
                    # Placeholder with Apple product icon
                    ui.icon('devices', size='4rem').style('color: #ccc;')
            
            # Product Info
            with ui.element('div').style('padding: 20px;'):
                # Product Name
                ui.label(self.product.name).classes('text-lg font-semibold mb-2').style('color: #1C1C1E;')
                
                # Product Description
                ui.label(self.product.description).classes('text-sm text-gray-600 mb-4').style('line-height: 1.4; height: 40px; overflow: hidden;')
                
                # Price and Category
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label(f'${self.product.price:.2f}').classes('price-tag')
                    ui.chip(self.product.category, icon='category').props('outline').classes('text-xs')
                
                # Stock Status
                if self.product.stock > 0:
                    ui.label(f'{self.product.stock} in stock').classes('text-xs text-green-600 mb-3')
                else:
                    ui.label('Out of stock').classes('text-xs text-red-600 mb-3')
                
                # Add to Cart Button
                ui.button(
                    'Add to Cart',
                    icon='add_shopping_cart',
                    on_click=lambda: self.add_to_cart(self.product)
                ).classes('apple-button w-full').props('no-caps').style('margin-top: auto;')