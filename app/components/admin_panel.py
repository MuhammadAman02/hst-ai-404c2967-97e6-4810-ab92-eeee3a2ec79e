"""Admin Panel Component"""

from nicegui import ui
from services.product_service import ProductService
from models.schemas import ProductCreate
from typing import Optional
import os

class AdminPanel:
    """Admin panel for managing products"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self.products = []
        self.render()
    
    def render(self):
        """Render the admin panel"""
        ui.label('Apple Store Admin').classes('text-3xl font-bold mb-8')
        
        # Add Product Form
        with ui.card().classes('w-full max-w-2xl mb-8'):
            ui.label('Add New Product').classes('text-xl font-semibold mb-4')
            
            with ui.row().classes('w-full gap-4'):
                with ui.column().classes('flex-1'):
                    name_input = ui.input('Product Name').classes('w-full')
                    description_input = ui.textarea('Description').classes('w-full')
                    price_input = ui.number('Price', value=0, format='%.2f').classes('w-full')
                
                with ui.column().classes('flex-1'):
                    category_input = ui.select(
                        ['iPhone', 'iPad', 'Mac', 'Watch', 'AirPods', 'Accessories'],
                        label='Category'
                    ).classes('w-full')
                    stock_input = ui.number('Stock', value=0).classes('w-full')
                    image_input = ui.input('Image URL').classes('w-full')
            
            ui.button(
                'Add Product',
                on_click=lambda: self.add_product(
                    name_input.value,
                    description_input.value,
                    float(price_input.value or 0),
                    category_input.value,
                    int(stock_input.value or 0),
                    image_input.value
                )
            ).classes('apple-button mt-4')
        
        # Products List
        with ui.card().classes('w-full'):
            ui.label('Manage Products').classes('text-xl font-semibold mb-4')
            self.products_container = ui.column().classes('w-full')
            self.load_products()
    
    async def load_products(self):
        """Load and display products"""
        try:
            self.products = await self.product_service.get_all_products()
            self.products_container.clear()
            
            for product in self.products:
                with self.products_container:
                    with ui.row().classes('w-full items-center justify-between p-4 border rounded'):
                        with ui.column():
                            ui.label(product.name).classes('font-semibold')
                            ui.label(f'${product.price:.2f} - {product.category}').classes('text-sm text-gray-600')
                            ui.label(f'Stock: {product.stock}').classes('text-xs')
                        
                        with ui.row().classes('gap-2'):
                            ui.button(
                                'Edit',
                                on_click=lambda p=product: self.edit_product(p)
                            ).props('size=sm outline')
                            ui.button(
                                'Delete',
                                on_click=lambda p=product: self.delete_product(p.id)
                            ).props('size=sm color=red outline')
        
        except Exception as e:
            ui.notify(f'Error loading products: {str(e)}', type='negative')
    
    async def add_product(self, name: str, description: str, price: float, category: str, stock: int, image_url: str):
        """Add a new product"""
        try:
            if not all([name, description, category]):
                ui.notify('Please fill in all required fields', type='warning')
                return
            
            product_data = ProductCreate(
                name=name,
                description=description,
                price=price,
                category=category,
                stock=stock,
                image_url=image_url or None
            )
            
            await self.product_service.create_product(product_data)
            ui.notify('Product added successfully!', type='positive')
            await self.load_products()
            
        except Exception as e:
            ui.notify(f'Error adding product: {str(e)}', type='negative')
    
    def edit_product(self, product):
        """Edit product (placeholder)"""
        ui.notify(f'Edit functionality for {product.name} coming soon!', type='info')
    
    async def delete_product(self, product_id: int):
        """Delete a product"""
        try:
            await self.product_service.delete_product(product_id)
            ui.notify('Product deleted successfully!', type='positive')
            await self.load_products()
        except Exception as e:
            ui.notify(f'Error deleting product: {str(e)}', type='negative')