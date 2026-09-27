import os
import platform
import socket


def system_info():
    print("\n=== SYSTEM INFO ===")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")


def check_up():
    import socket

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


def main():
    while True:
        print("""
╔══════════════════════════════════╗
║          ROYALLAB v0.1           ║
╚══════════════════════════════════╝

[1] System Information
[2] Scan an IP
[0] Exit
""")

        choice = input("Select: ")

        if choice == "1":
            system_info()

        elif choice == "2":
            check_up()

        elif choice == "0":
            print("Exiting RoyalLab...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

