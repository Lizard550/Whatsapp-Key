import os
import sys

from cli.args import parse
from device.adb.setup import ensure_adb
from device.adb import client
from core.engine import run
from utils import logger

MY_PROJECT = "Get a username key"


def main():
    from utils.banner import show_banner
    show_banner(MY_PROJECT)

    args = parse()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = ensure_adb(base_dir)
    client.init(adb_path)
    
    # Route to wireless or USB connection
    if args["wireless"]:
        # For wireless mode, connection is handled in core.engine.run()
        pass
    else:
        # For USB mode, connect here
        client.connect_usb()

    run(
        targets=args["targets"],
        save_ss=args["save_ss"],
        wireless=args["wireless"],
        wireless_ip=args["wireless_ip"],
        wireless_port=args["wireless_port"],
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.stopped()
    finally:
        os._exit(0)
