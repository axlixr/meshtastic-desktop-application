import sys
from pathlib import Path

# Add parent directory to path to allow importing utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.meshtastic_helpers import MeshtasticHandler

def list_nodes():
    """Get list of nodes using persistent connection (does not disconnect)."""
    handler = MeshtasticHandler.get_instance()
    try:
        interface = handler.get_interface()
        
        if not interface:
            raise Exception("Failed to connect to Meshtastic device")

        nodes = getattr(interface, 'nodes', None)
        if nodes is None:
            raise Exception("Nodes data not available. Make sure your device is connected and powered on.")

        node_list = []

        # Handle both dict and other iterable types
        if isinstance(nodes, dict):
            for node_num, node in nodes.items():
                try:
                    user = node.get("user", {}) if isinstance(node, dict) else {}
                    node_list.append({
                        "num": node_num,
                        "long_name": user.get("longName", "Unknown") if isinstance(user, dict) else "Unknown",
                        "short_name": user.get("shortName", "Unknown") if isinstance(user, dict) else "Unknown",
                        "mac": user.get("macaddr", "Unknown") if isinstance(user, dict) else "Unknown"
                    })
                except Exception as e:
                    # Skip problematic nodes
                    print(f"Error processing node {node_num}: {e}")
                    continue
        else:
            raise Exception(f"Unexpected nodes format: {type(nodes)}")

        return node_list
    except Exception as e:
        raise Exception(f"Error loading nodes: {str(e)}")
    # Note: We don't disconnect to maintain persistent connection

if __name__ == "__main__":
    nodes = list_nodes()
    print(f"Total nodes connected: {len(nodes)}")
    for n in nodes:
        print(f"Node {n['num']} | Long: {n['long_name']} | Short: {n['short_name']} | MAC: {n['mac']}")
