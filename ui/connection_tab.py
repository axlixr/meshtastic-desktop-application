# ui/connection_tab.py

import flet as ft
import threading
from utils.meshtastic_helpers import MeshtasticHandler
from ui.components import show_snackbar

def create_connection_tab(page: ft.Page):
    handler = MeshtasticHandler.get_instance()

    # --- Status indicator ---
    status_text = ft.Text("Disconnected", size=18, weight="bold")
    status_icon = ft.Text("●", size=20, color=ft.Colors.RED_400)
    status_indicator = ft.Container(
        content=ft.Row([status_icon, status_text], spacing=10),
        padding=15,
        bgcolor=ft.Colors.RED_900,
        border_radius=5,
        margin=ft.margin.only(bottom=20)
    )

    # --- Connection type ---
    connection_type = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="serial", label="Serial"),
            ft.Radio(value="network", label="Network (TCP)")
        ], spacing=20),
        value="serial"
    )

    # --- Serial section ---
    port_dropdown = ft.Dropdown(label="Select Serial Port", options=[], width=400)
    serial_section = ft.Container(
        content=ft.Column([
            ft.Text("Serial Connection", size=16, weight="bold", color=ft.Colors.WHITE),
            ft.Row([port_dropdown, ft.ElevatedButton("Scan Ports")], spacing=10)
        ], spacing=10),
        visible=True
    )

    # --- Network section ---
    ip_input = ft.TextField(label="IP Address or Hostname", hint_text="192.168.1.100", width=300)
    port_input = ft.TextField(label="Port", hint_text="4403", value="4403", width=150)
    network_section = ft.Container(
        content=ft.Column([
            ft.Text("Network Connection (TCP)", size=16, weight="bold", color=ft.Colors.WHITE),
            ft.Row([ip_input, port_input], spacing=10),
            ft.Text("Enter IP of your Meshtastic device.", size=12, color=ft.Colors.GREY_400, italic=True)
        ], spacing=10),
        visible=False
    )

    # --- Connected info ---
    connected_port_text = ft.Text("", size=14, color=ft.Colors.GREY_400)
    connection_type_text = ft.Text("", size=12, color=ft.Colors.GREY_500)

    # --- Update UI ---
    def update_connection_status():
        if handler.is_connected():
            status_text.value = "Connected"
            status_icon.color = ft.Colors.GREEN_400
            status_indicator.bgcolor = ft.Colors.GREEN_900
            connection_type_val = handler.get_connection_type()
            info = handler.get_connected_port()
            connected_port_text.value = f"Connected to: {info}" if info else "Connected (unknown)"
            connection_type_text.value = f"Connection type: {'Network' if connection_type_val=='network' else 'Serial'}"
        else:
            status_text.value = "Disconnected"
            status_icon.color = ft.Colors.RED_400
            status_indicator.bgcolor = ft.Colors.RED_900
            connected_port_text.value = ""
            connection_type_text.value = ""
        page.update()

    # --- Refresh all tabs ---
    def refresh_all_tabs():
        if hasattr(page, "data") and page.data.get("refresh_functions"):
            for func in page.data["refresh_functions"]:
                try:
                    func()
                except Exception as e:
                    print(f"Tab refresh error: {e}")

    # Register the callback for auto-refresh
    handler.register_callback(lambda: (update_connection_status(), refresh_all_tabs()))

    # --- Scan serial ports ---
    def scan_ports(e=None):
        port_dropdown.options.clear()
        port_dropdown.disabled = True
        page.update()

        def _scan():
            try:
                ports = handler.scan_serial_ports()
                port_dropdown.options = [
                    ft.dropdown.Option(key=p["device"], text=f"{p['device']} - {p['description']}") for p in ports
                ]
                if ports:
                    port_dropdown.value = ports[0]["device"]
                    show_snackbar(page, f"Found {len(ports)} port(s)", success=True)
                else:
                    show_snackbar(page, "No serial ports found.", success=False)
            except Exception as ex:
                show_snackbar(page, f"Scan error: {ex}", success=False)
            finally:
                port_dropdown.disabled = False
                page.update()

        threading.Thread(target=_scan, daemon=True).start()

    # --- Connect ---
    def connect_device(e=None):
        if handler.is_connected():
            show_snackbar(page, "Already connected. Disconnect first.", success=False)
            return

        def _connect():
            try:
                if connection_type.value == "serial":
                    selected_port = port_dropdown.value
                    if not selected_port:
                        show_snackbar(page, "Select a serial port", success=False)
                        return
                    handler.connect(port=selected_port)
                    show_snackbar(page, f"Connected to {selected_port}", success=True)
                else:
                    ip = ip_input.value.strip()
                    portnum = int(port_input.value.strip() or 4403)
                    if not ip:
                        show_snackbar(page, "Enter IP/hostname", success=False)
                        return
                    handler.connect(hostname=ip, portnum=portnum)
                    show_snackbar(page, f"Connected to {ip}:{portnum}", success=True)
            except Exception as ex:
                show_snackbar(page, f"Connection failed: {ex}", success=False)

        threading.Thread(target=_connect, daemon=True).start()

    # --- Disconnect ---
    def disconnect_device(e=None):
        if not handler.is_connected():
            show_snackbar(page, "Not connected", success=False)
            return

        def _disconnect():
            try:
                handler.disconnect()
                show_snackbar(page, "Disconnected", success=True)
            except Exception as ex:
                show_snackbar(page, f"Disconnect error: {ex}", success=False)

        threading.Thread(target=_disconnect, daemon=True).start()

    # --- Event handlers ---
    connection_type.on_change = lambda e=None: (
        setattr(serial_section, "visible", connection_type.value == "serial"),
        setattr(network_section, "visible", connection_type.value == "network"),
        page.update()
    )
    serial_section.content.controls[1].controls[1].on_click = scan_ports  # Scan button

    # --- Initial setup ---
    scan_ports()
    update_connection_status()

    # --- Layout ---
    return ft.Column([
        ft.Row([
            ft.Text("Connection", size=24, weight="bold"),
            ft.ElevatedButton("Refresh Ports", on_click=scan_ports)
        ], alignment="spaceBetween"),
        ft.Container(content=ft.Column([status_indicator, connected_port_text, connection_type_text]),
                     padding=20, bgcolor=ft.Colors.GREY_900, border_radius=10, margin=ft.margin.only(bottom=20)),
        ft.Container(content=ft.Column([
            ft.Text("Connection Type", size=18, weight="bold", color=ft.Colors.WHITE),
            connection_type,
            ft.Divider(),
            serial_section,
            network_section,
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton("Connect", on_click=connect_device, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                ft.ElevatedButton("Disconnect", on_click=disconnect_device, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
            ], spacing=10)
        ], spacing=15), padding=20, bgcolor=ft.Colors.GREY_900, border_radius=10)
    ], expand=True, spacing=20)
