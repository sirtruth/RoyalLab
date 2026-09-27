import platform
import socket
import ipaddress
import subprocess


def system_info():
    print("\n=== SYSTEM INFO ===")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")


def check_up():
    print("\n=== Scan IP ===")
    target = input("Enter IP address: ")

    ports = [22, 80, 443, 8080]

    print(f"\nScanning {target}...")

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            print(f"[OPEN]   {port}")
        else:
            print(f"[CLOSED] {port}")


def identify_device(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]

        hostname_lower = hostname.lower()

        if "iphone" in hostname_lower:
            return "iPhone"
        elif "ipad" in hostname_lower:
            return "iPad"
        elif "android" in hostname_lower:
            return "Android"
        elif "mac" in hostname_lower:
            return "Mac"
        elif "windows" in hostname_lower:
            return "Windows PC"
        else:
            return hostname

    except (socket.herror, socket.gaierror):
        return "Unknown"


def discover_hosts():
    print("\n=== HOST DISCOVERY ===")

    network_input = input(
        "Enter network (example 192.168.1.0/24): "
    )

    try:
        network = ipaddress.ip_network(network_input, strict=False)
    except ValueError:
        print("Invalid network.")
        return

    print(f"\nNetwork: {network}")
    print("Discovering reachable hosts...\n")

    found = []

    for ip in network.hosts():
        ip_string = str(ip)

        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", ip_string],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if result.returncode == 0:
                device = identify_device(ip_string)
                found.append(ip_string)

                print(f"[+] {ip_string:<16} {device}")

        except Exception:
            pass

    print("\n────────────────────────────────")
    print(f"Found: {len(found)} hosts")
    print("────────────────────────────────")

    print("\nLESSON")
    print("IP addresses identify network interfaces.")
    print("Device identification is best-effort and")
    print("may not always be accurate.")
    print("\nNo port scanning performed.")
    print("No login attempts performed.")


def main():
    while True:
        print("""
╔══════════════════════════════════╗
║          ROYALLAB v0.1           ║
╚══════════════════════════════════╝

[1] System Information
[2] Scan an IP
[3] Discover Hosts
[0] Exit
""")

        choice = input("Select: ")

        if choice == "1":
            system_info()

        elif choice == "2":
            check_up()

        elif choice == "3":
            discover_hosts()

        elif choice == "0":
            print("Exiting RoyalLab...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
