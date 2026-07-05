from utils import logger


def show_help():
    help_text = """
╔════════════════════════════════════════════════════════════════════════════╗
║                     WhatsApp Key Bot - Help & Usage                         ║
╚════════════════════════════════════════════════════════════════════════════╝

USAGE:
    python bot.py [OPTIONS] [KEYS]

OPTIONS:
    --XXXX                  Search for a specific 4-digit key
                            Example: --7777 searches for 7777
    
    --XXXX --YYYY           Search for multiple keys at once
                            Example: --7777 --1234 stops on first match
    
    --twin                  Search for all twin keys (0000-9999)
                            Twin keys: 0000, 1111, 2222, ..., 9999
    
    --ss                    Save screenshot when target key is found
                            Screenshot saved to screenshots/ folder
    
    --wireless, -w [IP]     Enable wireless ADB mode
                            Example: --wireless 192.168.1.100
                            (Optional: --port=5555 to specify custom port)
    
    --help                  Display this help message

EXAMPLES:
    USB Mode (Default):
        python bot.py --7777
        python bot.py --1111 --2222 --3333
        python bot.py --twin --ss
    
    Wireless Mode:
        python bot.py --wireless 192.168.1.100 --7777
        python bot.py --wireless 192.168.1.100 --port=5555 --1111 --ss
        python bot.py -w 192.168.1.100 --twin

PREREQUISITES:
    USB Mode:
        1. Phone connected via USB cable
        2. USB Debugging enabled
        3. USB Debugging permission granted on phone
        4. WhatsApp open on username key page
    
    Wireless Mode:
        1. Phone and PC on same network (WiFi)
        2. USB Debugging enabled
        3. Run "adb tcpip 5555" on phone via USB first (optional)
        4. Know your phone's IP address
        5. WhatsApp open on username key page

FIND YOUR PHONE'S IP ADDRESS:
    1. Go to Settings > About Phone
    2. Look for IP address under Network information
    3. Or use: adb shell "getprop dhcp.wlan0.ipaddress"

ENABLE WIRELESS DEBUGGING:
    1. Connect phone via USB
    2. Run: adb tcpip 5555
    3. Phone will restart in wireless mode
    4. Then disconnect USB and use with --wireless flag

TROUBLESHOOTING:
    - If wireless fails: Ensure phone and PC are on same network
    - If connection drops: Re-run the command to reconnect
    - If buttons not found: Ensure WhatsApp is open on correct page
    - For detailed logs: Check console output for error messages

╔════════════════════════════════════════════════════════════════════════════╗
║                   Built with ❤️ by Yuurisandesu                             ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(help_text)
