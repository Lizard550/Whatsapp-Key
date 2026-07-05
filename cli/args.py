import sys
from utils import logger


def parse() -> dict:
    argv = sys.argv[1:]

    if not argv:
        logger.warn("No Arguments Provided, Please Read The Following")
        logger.info("Make Sure Your Phone Is Plugged In Via USB Cable Or Connected Wirelessly")
        logger.info("Make Sure WhatsApp Is Open On The Username Key Page")
        logger.info("Run python bot.py --help To See All Available Commands")
        raise SystemExit(0)

    if "--help" in argv:
        from cli.help import show_help
        show_help()
        raise SystemExit(0)

    targets = []
    save_ss = False
    wireless = False
    wireless_ip = None
    wireless_port = 5555

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--ss":
            save_ss = True
        elif arg == "--wireless" or arg == "-w":
            wireless = True
            # Check if next argument is IP address
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                wireless_ip = argv[i + 1]
                i += 1
        elif arg.startswith("--port="):
            try:
                wireless_port = int(arg.split("=")[1])
            except (IndexError, ValueError):
                logger.warn("Invalid Port Number, Using Default 5555")
        elif arg == "--twin":
            targets += [str(i) * 4 for i in range(10)]
        elif arg.startswith("--") and arg[2:].isdigit() and len(arg[2:]) == 4:
            targets.append(arg[2:])
        i += 1

    targets = list(dict.fromkeys(targets))

    if not targets:
        logger.error("No Valid Target Keys Provided, Use --help For Usage")
        raise SystemExit(1)

    return {
        "targets": targets,
        "save_ss": save_ss,
        "wireless": wireless,
        "wireless_ip": wireless_ip,
        "wireless_port": wireless_port,
    }
