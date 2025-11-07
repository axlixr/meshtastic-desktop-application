# utils/meshtastic_helpers.py

import threading
import serial.tools.list_ports
import meshtastic.serial_interface

# Try importing TCP interface
try:
    from meshtastic import tcp_interface
    TCP_AVAILABLE = True
except ImportError:
    TCP_AVAILABLE = False
    print("Warning: TCP interface not available. Network connections will not work.")


class MeshtasticHandler:
    """Singleton handler for Meshtastic serial and network connections with connection callbacks."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.interface = None
                    cls._instance._connection_lock = threading.Lock()
                    cls._instance._connected_port = None
                    cls._instance._connection_type = None
                    cls._instance._connection_info = None
                    cls._instance._callbacks = []  # <-- list of connection state change callbacks
        return cls._instance

    # --- Callback registration ---
    def register_callback(self, callback):
        """Register a function to be called on connect/disconnect events."""
        if callable(callback) and callback not in self._callbacks:
            self._callbacks.append(callback)

    def _run_callbacks(self):
        """Call all registered callbacks in a thread-safe way."""
        for cb in self._callbacks:
            try:
                cb()
            except Exception as e:
                print(f"Callback error: {e}")

    # --- Serial scanning ---
    def scan_serial_ports(self):
        """Scan available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [{"device": p.device, "description": p.description, "hwid": p.hwid} for p in ports]

    # --- Connect ---
    def connect(self, port=None, hostname=None, portnum=None):
        with self._connection_lock:
            if self.interface:
                raise Exception("Already connected. Disconnect first.")

            # --- Network connection ---
            if hostname:
                if not TCP_AVAILABLE:
                    raise Exception("TCP interface not available.")
                portnum = portnum or 4403
                try:
                    self.interface = tcp_interface.TCPInterface(hostname=hostname, portNumber=portnum)
                    self._connection_type = 'network'
                    self._connected_port = f"{hostname}:{portnum}"
                    self._connection_info = self._connected_port
                except Exception as e:
                    raise Exception(f"Failed to connect via TCP: {e}")
                finally:
                    self._run_callbacks()
                return self.interface

            # --- Serial connection ---
            try:
                if port:
                    self.interface = meshtastic.serial_interface.SerialInterface(devPath=port)
                else:
                    available_ports = self.scan_serial_ports()
                    if not available_ports:
                        raise Exception("No serial ports found.")
                    self.interface = meshtastic.serial_interface.SerialInterface(devPath=available_ports[0]["device"])

                # Set connected info
                if hasattr(self.interface, "port") and self.interface.port:
                    self._connected_port = self.interface.port
                    self._connection_info = self.interface.port
                elif hasattr(self.interface, "stream") and hasattr(self.interface.stream, "port"):
                    self._connected_port = self.interface.stream.port
                    self._connection_info = self.interface.stream.port

                self._connection_type = 'serial'
            except Exception as e:
                raise Exception(f"Serial connection failed: {e}")
            finally:
                self._run_callbacks()  # <-- refresh tabs/UI on connect
            return self.interface

    # --- Disconnect ---
    def disconnect(self):
        with self._connection_lock:
            if self.interface:
                try:
                    self.interface.close()
                except:
                    pass
            self.interface = None
            self._connected_port = None
            self._connection_type = None
            self._connection_info = None
            self._run_callbacks()  # <-- refresh tabs/UI on disconnect

    # --- Status helpers ---
    def is_connected(self):
        if not self.interface:
            return False
        try:
            return hasattr(self.interface, 'port') or hasattr(self.interface, 'stream') or hasattr(self.interface, 'hostname')
        except:
            return False

    def get_interface(self):
        if not self.interface:
            raise Exception("Not connected.")
        return self.interface

    def get_connected_port(self):
        return self._connected_port

    def get_connection_type(self):
        return self._connection_type

    def get_connection_info(self):
        return self._connection_info

    @classmethod
    def get_instance(cls):
        return cls()
