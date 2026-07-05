import threading
from utils import logger


def run(targets: list, save_ss: bool, wireless: bool = False, wireless_ip: str = None, wireless_port: int = 5555):
    from core.worker import search_loop
    from device.adb import client, wireless as wireless_module

    # Handle wireless connection if specified
    if wireless:
        if not wireless_ip:
            logger.error("Wireless Mode Requires IP Address. Use: python bot.py --wireless <IP_ADDRESS> --XXXX")
            raise SystemExit(1)
        
        if not wireless_module.connect_wireless(wireless_ip, wireless_port):
            logger.error(f"Failed To Connect Wirelessly To {wireless_ip}:{wireless_port}")
            raise SystemExit(1)
    else:
        # Use USB connection by default
        client.connect_usb()

    target_set = set(targets)
    logger.info(f"Initiating Search For Keys {', '.join(targets)}")
    logger.info(f"Connection Type: {'Wireless' if wireless else 'USB'}")

    stop_event = threading.Event()
    result_holder = []

    t = threading.Thread(
        target=search_loop,
        args=(target_set, save_ss, result_holder, stop_event),
        daemon=True
    )
    t.start()

    try:
        while t.is_alive():
            t.join(timeout=0.5)
    except KeyboardInterrupt:
        stop_event.set()
        t.join(timeout=3)
        # Disconnect wireless if it was used
        if wireless and wireless_ip:
            wireless_module.disconnect_wireless(wireless_ip, wireless_port)
        raise

    if result_holder:
        logger.info(f"Search Completed Successfully With Key {result_holder[0]}")
    else:
        logger.warn("Search Ended Without Any Matching Key")
    
    # Disconnect wireless if it was used
    if wireless and wireless_ip:
        wireless_module.disconnect_wireless(wireless_ip, wireless_port)
