# ui/node_info_tab.py
import flet as ft
from scripts.my_node_info import get_node_info
from ui.components import show_snackbar
from utils.format_utils import format_key, format_value, create_info_section

def create_node_info_tab(page: ft.Page):
    node_info_container = ft.Container(
        content=ft.Column([], scroll="auto"),
        padding=15,
        expand=True
    )

    def load_node_info(e=None):
        node_info_container.content.controls.clear()
        node_info_container.content.controls.append(
            ft.Text("Loading...", size=16, color=ft.Colors.GREY_400)
        )
        page.update()
        try:
            info = get_node_info()
            node_info_container.content.controls.clear()

            # Add node number and favorite status
            status_icon = "★" if info.get("is_favorite") else "◆"
            node_info_container.content.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{status_icon} Node #{info.get('num', 'N/A')}", 
                                       size=20, weight="bold", color=ft.Colors.WHITE),
                                ft.Container(
                                    content=ft.Text("★ Favorite" if info.get("is_favorite") else "", 
                                                   size=14, color=ft.Colors.AMBER),
                                    padding=ft.padding.only(left=10)
                                )
                            ])
                        ]),
                        padding=15
                    ),
                    elevation=3,
                    color=ft.Colors.BLUE_400,
                    margin=ft.margin.only(bottom=15)
                )
            )

            # Add sections for user, position, and metrics
            if info.get("user"):
                node_info_container.content.controls.append(
                    create_info_section("User Information", "", info["user"])
                )
            if info.get("position"):
                node_info_container.content.controls.append(
                    create_info_section("Position Information", "", info["position"])
                )
            if info.get("metrics"):
                node_info_container.content.controls.append(
                    create_info_section("Device Metrics", "", info["metrics"])
                )

            show_snackbar(page, "Node information loaded successfully", success=True)
        except Exception as ex:
            node_info_container.content.controls.clear()
            node_info_container.content.controls.append(
                ft.Container(
                    content=ft.Text(f"Error: {ex}", color=ft.Colors.RED_400, size=14),
                    padding=15,
                    bgcolor=ft.Colors.RED_900,
                    border_radius=5
                )
            )
            show_snackbar(page, f"Error loading node info: {ex}", success=False)
        page.update()

    # Load node info on startup
    load_node_info()

    tab_content = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("My Node", size=24, weight="bold"),
                ft.ElevatedButton("Refresh Info", on_click=load_node_info)
            ], alignment="spaceBetween"),
            node_info_container
        ], spacing=10),
        expand=True
    )
    
    # Return both the content and the refresh function
    return tab_content, load_node_info