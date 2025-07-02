"""Cart Sidebar Component"""

from nicegui import ui
from models.schemas import CartItem
from services.cart_service import CartService
from typing import List

class CartSidebar:
    """Shopping cart sidebar component"""
    
    def __init__(self, cart_items: List[CartItem], cart_service: CartService):
        self.cart_items = cart_items
        self.cart_service = cart_service
        self.render()
    
    def render(self):
        """Render the cart sidebar"""
        with ui.element('div').style('''
            position: fixed;
            top: 0;
            right: 0;
            width: 400px;
            height: 100vh;
            background: white;
            box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 20px;
            overflow-y: auto;
        '''):
            # Cart Header
            with ui.row().classes('w-full justify-between items-center mb-6'):
                ui.label('Shopping Cart').classes('text-xl font-bold')
                ui.button(icon='close', on_click=self.close_cart).props('flat round')
            
            if not self.cart_items:
                # Empty Cart
                with ui.column().classes('w-full items-center justify-center').style('height: 200px;'):
                    ui.icon('shopping_cart', size='3rem').style('color: #ccc;')
                    ui.label('Your cart is empty').classes('text-gray-500 mt-4')
                    ui.label('Add some products to get started!').classes('text-sm text-gray-400')
            else:
                # Cart Items
                total = 0
                for item in self.cart_items:
                    with ui.card().classes('w-full mb-4').style('padding: 16px;'):
                        with ui.row().classes('w-full items-center gap-4'):
                            # Product Image Placeholder
                            with ui.element('div').style('width: 60px; height: 60px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center;'):
                                ui.icon('devices', size='1.5rem').style('color: #ccc;')
                            
                            # Product Info
                            with ui.column().classes('flex-1'):
                                ui.label(item.product_name).classes('font-semibold')
                                ui.label(f'${item.price:.2f}').classes('text-blue-600')
                                
                                # Quantity Controls
                                with ui.row().classes('items-center gap-2 mt-2'):
                                    ui.button('-', on_click=lambda i=item: self.update_quantity(i, -1)).props('size=sm round')
                                    ui.label(str(item.quantity)).classes('mx-2')
                                    ui.button('+', on_click=lambda i=item: self.update_quantity(i, 1)).props('size=sm round')
                            
                            # Remove Button
                            ui.button(icon='delete', on_click=lambda i=item: self.remove_item(i)).props('flat round color=red')
                    
                    total += item.price * item.quantity
                
                # Cart Summary
                ui.separator().classes('my-6')
                
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Subtotal:').classes('text-lg')
                    ui.label(f'${total:.2f}').classes('text-lg font-bold')
                
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Tax:').classes('text-sm text-gray-600')
                    ui.label(f'${total * 0.08:.2f}').classes('text-sm text-gray-600')
                
                with ui.row().classes('w-full justify-between items-center mb-6'):
                    ui.label('Total:').classes('text-xl font-bold')
                    ui.label(f'${total * 1.08:.2f}').classes('text-xl font-bold text-blue-600')
                
                # Checkout Button
                ui.button(
                    'Checkout',
                    icon='payment',
                    on_click=self.checkout
                ).classes('apple-button w-full').style('padding: 16px;')
    
    def close_cart(self):
        """Close the cart sidebar"""
        # This would typically update the parent component state
        ui.notify('Cart closed', type='info')
    
    async def update_quantity(self, item: CartItem, change: int):
        """Update item quantity"""
        try:
            new_quantity = max(0, item.quantity + change)
            if new_quantity == 0:
                await self.cart_service.remove_from_cart(item.product_id)
            else:
                await self.cart_service.update_quantity(item.product_id, new_quantity)
            ui.notify('Cart updated', type='positive')
        except Exception as e:
            ui.notify(f'Error updating cart: {str(e)}', type='negative')
    
    async def remove_item(self, item: CartItem):
        """Remove item from cart"""
        try:
            await self.cart_service.remove_from_cart(item.product_id)
            ui.notify('Item removed from cart', type='positive')
        except Exception as e:
            ui.notify(f'Error removing item: {str(e)}', type='negative')
    
    def checkout(self):
        """Process checkout"""
        ui.notify('Checkout functionality coming soon!', type='info')