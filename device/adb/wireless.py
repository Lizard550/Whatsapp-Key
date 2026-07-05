import subprocess
from utils import logger


def connect_wireless(host: str, port: int = 5555) -> bool:
    """
    Connect to Android device via wireless ADB.
    
    Args:
        host: IP address or hostname of the device
        port: Port number (default 5555)
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    from device.adb import client
    
    try:
        logger.info(f"Attempting Wireless Connection To {host}:{port}")
        result = client.run("connect", f"{host}:{port}")
        output = result.stdout.decode().strip()
        
        if "connected to" in output.lower():
            logger.info(f"Successfully Connected To Device At {host}:{port}")
            return True
        elif "already connected" in output.lower():
            logger.info(f"Device Already Connected At {host}:{port}")
            return True
        else:
            logger.error(f"Failed To Connect: {output}")
            return False
    
    except Exception as e:
        logger.error(f"Wireless Connection Error: {str(e)}")
        return False


def disconnect_wireless(host: str, port: int = 5555) -> bool:
    """
    Disconnect from wireless ADB connection.
    
    Args:
        host: IP address or hostname of the device
        port: Port number (default 5555)
    
    Returns:
        bool: True if disconnection successful, False otherwise
    """
    from device.adb import client
    
    try:
        logger.info(f"Disconnecting From {host}:{port}")
        result = client.run("disconnect", f"{host}:{port}")
        output = result.stdout.decode().strip()
        
        if not output or "disconnected" in output.lower():
            logger.info(f"Successfully Disconnected From {host}:{port}")
            return True
        else:
            logger.warn(f"Disconnect Result: {output}")
            return True
    
    except Exception as e:
        logger.error(f"Wireless Disconnection Error: {str(e)}")
        return False


def list_wireless_devices() -> list:
    """
    List all connected wireless ADB devices.
    
    Returns:
        list: List of connected device addresses
    """
    from device.adb import client
    
    try:
        result = client.run("devices")
        output = result.stdout.decode().strip()
        
        devices = []
        for line in output.splitlines():
            if "device" in line and not line.startswith("List"):
                parts = line.split()
                if len(parts) >= 2:
                    device_id = parts[0]
                    # Check if it's a wireless connection (contains ':' for IP:PORT)
                    if ":" in device_id:
                        devices.append(device_id)
        
        return devices
    
    except Exception as e:
        logger.error(f"Error Listing Wireless Devices: {str(e)}")
        return []


def get_device_ip(device_id: str = None) -> str:
    """
    Get the IP address of the connected device.
    
    Args:
        device_id: Specific device ID (optional)
    
    Returns:
        str: IP address of the device, or None if not found
    """
    from device.adb import client
    
    try:
        # Try to get IP via getprop
        result = client.run("shell", "getprop", "dhcp.wlan0.ipaddress")
        ip = result.stdout.decode().strip()
        
        if ip:
            logger.info(f"Device IP Address: {ip}")
            return ip
        
        # Fallback method
        result = client.run("shell", "ip", "addr", "show", "wlan0")
        output = result.stdout.decode().strip()
        
        for line in output.splitlines():
            if "inet " in line:
                parts = line.split()
                if len(parts) >= 2:
                    ip_with_mask = parts[1]
                    ip = ip_with_mask.split("/")[0]
                    logger.info(f"Device IP Address: {ip}")
                    return ip
        
        logger.warn("Could Not Determine Device IP Address")
        return None
    
    except Exception as e:
        logger.warn(f"Error Getting Device IP: {str(e)}")
        return None


def enable_wireless_debugging() -> bool:
    """
    Enable wireless debugging on the connected device.
    
    Returns:
        bool: True if successful, False otherwise
    """
    from device.adb import client
    
    try:
        logger.info("Enabling Wireless Debugging On Device")
        
        # Enable TCP/IP mode on device (port 5555)
        result = client.run("tcpip", "5555")
        output = result.stdout.decode().strip()
        
        if "restarting" in output.lower() or not output:
            logger.info("Wireless Debugging Enabled Successfully")
            return True
        else:
            logger.error(f"Failed To Enable Wireless Debugging: {output}")
            return False
    
    except Exception as e:
        logger.error(f"Error Enabling Wireless Debugging: {str(e)}")
        return False
