# ui/components.py
import flet as ft

def show_snackbar(page, message, success=True):
    page.snack_bar = ft.SnackBar(
        ft.Text(message, color=ft.Colors.WHITE),
        bgcolor="#4caf50" if success else "#f44336",
        open=True,
        duration=3000
    )
    page.update()