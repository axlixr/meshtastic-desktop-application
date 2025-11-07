# utils/format_utils.py
import flet as ft
import re

def format_key(key):
    """Convert snake_case or camelCase to Title Case"""
    if '_' in key:
        return ' '.join(word.capitalize() for word in key.split('_'))
    return re.sub(r'([A-Z])', r' \1', key).strip().title()

def format_value(value):
    """Format value for display"""
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if value else "N/A"

def create_info_section(title, icon, data):
    """Create a formatted section card for node information"""
    if not data or (isinstance(data, dict) and not any(data.values())):
        return ft.Container(
            content=ft.Text(f"{icon} {title}\nNo data available", color=ft.Colors.GREY_400),
            padding=10,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=5,
            margin=ft.margin.only(bottom=10)
        )
    
    items = []
    for k, v in data.items():
        if v is not None and v != "":
            formatted_key = format_key(k)
            formatted_val = format_value(v)
            items.append(
                ft.Row([
                    ft.Text(f"{formatted_key}:", weight="bold", width=180, color=ft.Colors.BLUE_300),
                    ft.Text(formatted_val, color=ft.Colors.WHITE, expand=True, selectable=True)
                ], spacing=10)
            )
    
    if not items:
        return ft.Container(
            content=ft.Text(f"{icon} {title}\nNo data available", color=ft.Colors.GREY_400),
            padding=10,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=5,
            margin=ft.margin.only(bottom=10)
        )
    
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(f"{icon} {title}", size=18, weight="bold", color=ft.Colors.BLUE_200),
                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
                *items
            ], spacing=8),
            padding=15
        ),
        elevation=2,
        margin=ft.margin.only(bottom=15)
    )

def create_contact_card(node_num, display_name, short_name, on_click):
    """Create a contact card for the direct messages sub-tab"""
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(display_name, weight="bold", size=16),
                    ft.Text(f"Short: {short_name} | Node #{node_num}", 
                           size=12, color=ft.Colors.GREY_400)
                ], expand=True, spacing=2)
            ], alignment="spaceBetween"),
            padding=15,
            on_click=on_click
        ),
        elevation=1
    )