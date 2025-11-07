# main.py
import flet as ft
import atexit
from ui.node_info_tab import create_node_info_tab
from ui.messaging_tab import create_messaging_tab
from ui.nodes_tab import create_nodes_tab
from ui.settings_tab import create_settings_tab
from ui.connection_tab import create_connection_tab
from utils.meshtastic_helpers import MeshtasticHandler

def main(page: ft.Page):
    page.title = "Meshtastic Dashboard"
    page.theme_mode = "dark"
    page.scroll = "hidden"
    page.padding = 20

    # Initialize tabs and collect refresh functions
    refresh_functions = []
    
    # Connection tab (doesn't return a refresh function, but we'll handle it separately)
    connection_content = create_connection_tab(page)
    
    # Other tabs return (content, refresh_function)
    node_info_content, node_info_refresh = create_node_info_tab(page)
    messaging_content, messaging_refresh = create_messaging_tab(page)
    nodes_content, nodes_refresh = create_nodes_tab(page)
    settings_content, settings_refresh = create_settings_tab(page)
    
    # Store refresh functions in page.data for access by connection tab
    refresh_functions = [node_info_refresh, messaging_refresh, nodes_refresh, settings_refresh]
    page.data = {"refresh_functions": refresh_functions}
    
    # Initialize tabs
    tabs = ft.Tabs(
        selected_index=0,
        expand=1,
        tabs=[
            ft.Tab(text="Connection", content=connection_content),
            ft.Tab(text="Node Info", content=node_info_content),
            ft.Tab(text="Messaging", content=messaging_content),
            ft.Tab(text="Nodes", content=nodes_content),
            ft.Tab(text="Settings", content=settings_content),
        ]
    )

    page.add(tabs)

def cleanup_connection():
    """Clean up persistent connection when app closes."""
    try:
        handler = MeshtasticHandler.get_instance()
        handler.disconnect()
        print("Meshtastic connection closed.")
    except:
        pass

atexit.register(cleanup_connection)

if __name__ == "__main__":
    try:
        ft.app(target=main)
    finally:
        cleanup_connection()