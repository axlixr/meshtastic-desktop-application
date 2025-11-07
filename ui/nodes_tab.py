# ui/nodes_tab.py
import flet as ft
from scripts.nodes import list_nodes
from ui.components import show_snackbar

def create_nodes_tab(page: ft.Page):
    nodes_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Node #")),
            ft.DataColumn(ft.Text("Long Name")),
            ft.DataColumn(ft.Text("Short Name")),
            ft.DataColumn(ft.Text("MAC"))
        ],
        rows=[],
        border_radius=5,
        column_spacing=30,
        heading_row_color=ft.Colors.BLUE_GREY_900,
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.WHITE),
        data_row_color=ft.Colors.BLUE_GREY_800
    )

    def refresh_nodes(e=None):
        try:
            nodes = list_nodes()
            nodes_table.rows.clear()
            for n in nodes:
                nodes_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(n["num"]))),
                            ft.DataCell(ft.Text(n["long_name"])),
                            ft.DataCell(ft.Text(n["short_name"])),
                            ft.DataCell(ft.Text(n["mac"]))
                        ]
                    )
                )
            show_snackbar(page, f"Loaded {len(nodes)} nodes", success=True)
        except Exception as ex:
            show_snackbar(page, f"Error: {ex}", success=False)
        page.update()

    refresh_nodes()

    tab_content = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Connected Nodes", size=24, weight="bold"),
                ft.ElevatedButton("Refresh Nodes", on_click=refresh_nodes)
            ]),
            ft.Container(
                content=ft.Column([nodes_table], scroll="auto"),
                expand=True,
                padding=10
            )
        ], spacing=10),
        expand=True
    )
    
    # Return both the content and the refresh function
    return tab_content, refresh_nodes