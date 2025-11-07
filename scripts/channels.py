import sys
from pathlib import Path

# Add parent directory to path to allow importing utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.meshtastic_helpers import MeshtasticHandler


def send_to_channel(message: str, *_args, **_kwargs):
    """
    Send a message to the primary broadcast channel using a persistent connection.
    Works with the Flet front end. Ignores channel index arguments if passed.
    """
    handler = MeshtasticHandler.get_instance()
    interface = handler.get_interface()

    try:
        # Always send to the primary broadcast channel (channel index 0)
        interface.sendText(message)
        return "Message sent to primary broadcast channel."
    except Exception as e:
        print(f"[Error] Failed to send message: {e}")
        return f"Error sending message: {e}"


if __name__ == "__main__":
    # Simple CLI test
    msg = input("Enter message to broadcast: ")
    print(send_to_channel(msg))
