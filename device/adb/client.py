import subprocess
from utils import logger


_adb_path = "adb"
_connection_type = "usb"  # 'usb' or 'wireless'


def init(path: str):
    global _adb_path
    _adb_path = path


def run(*args) -> subprocess.CompletedProcess:
    return subprocess.run([_adb_path] + list(args), capture_output=True)


def connect_usb():
    global _connection_type
    result = run("devices")
    output = result.stdout.decode().strip()
    lines = [l for l in output.splitlines() if l and "List" not in l and "device" in l]
    if not lines:
        logger.error("No Device Detected Via USB Connection")
        raise SystemExit(1)
    device_id = lines[0].split()[0]
    _connection_type = "usb"
    logger.info(f"Device Successfully Connected Via USB With ID {device_id}")


def connect_wireless(host: str, port: int = 5555) -> bool:
    """Connect to device via wireless ADB."""
    global _connection_type
    try:
        logger.info(f"Attempting Wireless Connection To {host}:{port}")
        result = run("connect", f"{host}:{port}")
        output = result.stdout.decode().strip()
        
        if "connected to" in output.lower() or "already connected" in output.lower():
            _connection_type = "wireless"
            logger.info(f"Successfully Connected To Device At {host}:{port}")
            return True
        else:
            logger.error(f"Failed To Connect: {output}")
            return False
    except Exception as e:
        logger.error(f"Wireless Connection Error: {str(e)}")
        return False


def disconnect_wireless(host: str, port: int = 5555) -> bool:
    """Disconnect from wireless ADB connection."""
    global _connection_type
    try:
        logger.info(f"Disconnecting From {host}:{port}")
        result = run("disconnect", f"{host}:{port}")
        output = result.stdout.decode().strip()
        
        if not output or "disconnected" in output.lower():
            _connection_type = "usb"
            logger.info(f"Successfully Disconnected From {host}:{port}")
            return True
        return True
    except Exception as e:
        logger.error(f"Wireless Disconnection Error: {str(e)}")
        return False


def shell(*args) -> str:
    result = run("shell", *args)
    return result.stdout.decode().strip()


def get_connection_type() -> str:
    """Get current connection type."""
    return _connection_type
