@ -0,0 +1,39 @@
import os
import platform
import socket


def system_info():
    print("\n=== SYSTEM INFO ===")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Architecture: {platform.machine()}")


def main():
    while True:
        print("""
╔══════════════════════════════════╗
║          ROYALLAB v0.1           ║
╚══════════════════════════════════╝

[1] System Information
[0] Exit
""")

        choice = input("Select: ")

        if choice == "1":
            system_info()

        elif choice == "0":
            print("Exiting RoyalLab...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
