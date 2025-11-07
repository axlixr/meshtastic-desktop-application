import sys
from pathlib import Path

# Add parent directory to path to allow importing utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.meshtastic_helpers import MeshtasticHandler

def get_node_info():
    """Get node info using persistent connection (does not disconnect)."""
    handler = MeshtasticHandler.get_instance()
    interface = handler.get_interface()

    info = interface.getMyNodeInfo()

    data = {
        "num": info.get("num"),
        "is_favorite": info.get("isFavorite"),
        "user": info.get("user", {}),
        "position": info.get("position", {}),
        "metrics": info.get("deviceMetrics", {})
    }

    # Note: We don't disconnect to maintain persistent connection
    return data

if __name__ == "__main__":
    node_info = get_node_info()

    print("----------------------------------------------------")
    print("Node Number:", node_info["num"])
    print("Is Favorite:", node_info["is_favorite"])
    print("----------------------------------------------------")

    for key, value in node_info["user"].items():
        print(f"{key}: {value}")

    print("----------------------------------------------------")

    for key, value in node_info["position"].items():
        print(f"{key}: {value}")

    print("----------------------------------------------------")

    for key, value in node_info["metrics"].items():
        print(f"{key}: {value}")

    print("----------------------------------------------------")
