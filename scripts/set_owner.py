import sys
from pathlib import Path

# Add parent directory to path to allow importing utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.meshtastic_helpers import MeshtasticHandler

def set_owner(longname: str, shortname: str):
    """Set owner info using persistent connection (does not disconnect)."""
    handler = MeshtasticHandler.get_instance()
    interface = handler.get_interface()

    interface.localNode.setOwner(long_name=longname, short_name=shortname)

    return f"Owner info updated to Long Name: {longname}, Short Name: {shortname}"

if __name__ == "__main__":
    print("Set Owner:")
    longname = input("  Long Name (max 36 bytes): ")
    shortname = input("  Short Name (max 4 bytes): ")
    print(set_owner(longname, shortname))

