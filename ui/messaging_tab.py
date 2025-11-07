# ui/messaging_tab.py
import flet as ft
from scripts.channels import send_to_channel
from scripts.direct_msg import send_message
from scripts.nodes import list_nodes
from ui.components import show_snackbar
from utils.format_utils import create_contact_card

def create_messaging_tab(page: ft.Page):
    # Channels Sub-tab
    channel_message_input = ft.TextField(label="Message", expand=True, multiline=True, min_lines=3)

    def send_channel_message(_e):
        msg = channel_message_input.value.strip()
        if not msg:
            show_snackbar(page, "Please enter a message", success=False)
            return
        try:
            channel_idx = 0  # Primary channel
            result = send_to_channel(msg, channel_idx)
            show_snackbar(page, result, success=True)
            channel_message_input.value = ""
        except Exception as ex:
            show_snackbar(page, f"Error: {ex}", success=False)
        page.update()

    channels_subtab = ft.Container(
        content=ft.Column([
            ft.Text("Primary Channel", size=20, weight="bold"),
            ft.Divider(),
            ft.Text("Send a message to the primary channel (broadcast)", color=ft.Colors.GREY_400, size=12),
            channel_message_input,
            ft.ElevatedButton("Send to Primary Channel", on_click=send_channel_message, width=250)
        ], spacing=15, scroll="auto"),
        expand=True
    )

    # Direct Messages Sub-tab
    chat_message_input = ft.TextField(
        label="Type a message...", 
        expand=True, 
        multiline=True,
        min_lines=1,
        max_lines=5,
        on_submit=lambda _e: send_chat_message()
    )

    selected_contact = {"num": None, "name": None}
    contacts_list = ft.ListView(expand=True, spacing=5)
    direct_messages_view = ft.Container()

    def show_contacts_view():
        direct_messages_view.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Direct Messages", size=24, weight="bold"),
                    ft.ElevatedButton("Refresh", on_click=load_contacts, width=150)
                ], alignment="spaceBetween"),
                ft.Divider(),
                ft.Container(
                    content=contacts_list,
                    expand=True,
                    padding=10
                )
            ], spacing=10),
            expand=True
        )
        page.update()

    def show_chat_view(node_num, name):
        chat_header = ft.Container(
            content=ft.Row([
                ft.TextButton(
                    text="← Back",
                    tooltip="Back to contacts",
                    on_click=lambda _e: show_contacts_view()
                ),
                ft.Column([
                    ft.Text(name, size=18, weight="bold"),
                    ft.Text(f"Node #{node_num}", size=12, color=ft.Colors.GREY_400)
                ], expand=True, spacing=0)
            ], alignment="start"),
            padding=15,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=5
        )

        chat_input_area = ft.Container(
            content=ft.Row([
                chat_message_input,
                ft.ElevatedButton(
                    text="Send",
                    tooltip="Send message",
                    on_click=lambda _e: send_chat_message(),
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                )
            ], spacing=5),
            padding=10,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=5
        )

        direct_messages_view.content = ft.Container(
            content=ft.Column([
                chat_header,
                chat_input_area
            ], spacing=0),
            expand=True
        )
        page.update()

    def load_contacts(_e=None):
        contacts_list.controls.clear()
        try:
            nodes = list_nodes()
            if not nodes:
                contacts_list.controls.append(
                    ft.Container(
                        content=ft.Text("No nodes found. Make sure your device is connected.", color=ft.Colors.GREY_400),
                        padding=15
                    )
                )
            else:
                contact_count = 0
                for node in nodes:
                    try:
                        node_num = node.get("num")
                        if not node_num:
                            continue
                        long_name = node.get("long_name", "Unknown")
                        short_name = node.get("short_name", "Unknown")
                        display_name = long_name if long_name != "Unknown" else f"Node {node_num}"

                        contacts_list.controls.append(
                            create_contact_card(
                                node_num, display_name, short_name,
                                lambda _e, n=node_num, name=display_name: (
                                    selected_contact.update({'num': n, 'name': name}) or
                                    show_chat_view(n, name)
                                )
                            )
                        )
                        contact_count += 1
                    except Exception as node_ex:
                        print(f"Error processing node: {node_ex}")
                        continue

                if contact_count == 0:
                    contacts_list.controls.append(
                        ft.Container(
                            content=ft.Text("No contacts available. All nodes may be broadcast nodes.", color=ft.Colors.GREY_400),
                            padding=15
                        )
                    )
                else:
                    show_snackbar(page, f"Loaded {contact_count} contacts", success=True)
        except Exception as ex:
            contacts_list.controls.append(
                ft.Container(
                    content=ft.Text(f"Error: {str(ex)}", color=ft.Colors.RED_400),
                    padding=15,
                    bgcolor=ft.Colors.RED_900,
                    border_radius=5
                )
            )
            show_snackbar(page, f"Error loading contacts: {ex}", success=False)
        page.update()

    def send_chat_message():
        if selected_contact["num"] is None:
            show_snackbar(page, "No contact selected", success=False)
            return
        
        msg = chat_message_input.value.strip()
        if not msg:
            return
        
        node_num = selected_contact["num"]
        name = selected_contact["name"]

        try:
            send_message(msg, node_num)
            chat_message_input.value = ""
            show_snackbar(page, "Message sent", success=True)
        except Exception as ex:
            show_snackbar(page, f"Error sending message: {ex}", success=False)
        page.update()

    show_contacts_view()
    load_contacts()

    direct_messages_subtab = direct_messages_view

    messaging_subtabs = ft.Tabs(
        selected_index=0,
        expand=True,
        tabs=[
            ft.Tab(text="Channels", content=channels_subtab),
            ft.Tab(text="Direct Messages", content=direct_messages_subtab)
        ]
    )

    def refresh_messaging():
        """Refresh messaging tab - reload contacts"""
        load_contacts()

    return messaging_subtabs, refresh_messaging
