import sys
from pathlib import Path

# Add parent directory to path to allow importing utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.meshtastic_helpers import MeshtasticHandler

def send_message(message: str, destination: int = 0):
    """Send message using persistent connection (does not disconnect)."""
    handler = MeshtasticHandler.get_instance()
    interface = handler.get_interface()

    interface.sendText(message, destination)

    # Note: We don't disconnect to maintain persistent connection
    return f"Message '{message}' sent to node {destination}."

if __name__ == "__main__":
    message = input("Enter message: ")
    destination = int(input("Enter destination node number (0 for broadcast): "))
    print(send_message(message, destination))
