# ui/settings_tab.py
import flet as ft
from scripts.set_owner import set_owner
from ui.components import show_snackbar

def create_settings_tab(page: ft.Page):
    
    longname_input = ft.TextField(label="Long Name", width=300)
    shortname_input = ft.TextField(label="Short Name", width=150)

    def update_owner(e):
        ln = longname_input.value.strip()
        sn = shortname_input.value.strip()
        try:
            result = set_owner(ln, sn)
            show_snackbar(page, result, success=True)
        except Exception as ex:
            show_snackbar(page, f"Error: {ex}", success=False)
        page.update()

    
    tab_content = ft.Container(
        content=ft.Column([
            ft.Row([longname_input, shortname_input]),
            ft.ElevatedButton("Update Owner Info", on_click=update_owner)
        ], spacing=15),
        expand=True
    )
    
    def refresh_settings():
        """Settings tab doesn't need refresh, but we provide a no-op function"""
        pass
    
    # Return both the content and the refresh function
    return tab_content, refresh_settings