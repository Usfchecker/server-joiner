import subprocess
import sys
import time
import os
import pyautogui
import win32api
import win32con
import win32gui

def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup():
    """Ensure all required packages are installed"""
    try:
        import pyautogui
    except ImportError:
        print("Required package 'pyautogui' is not installed. Installing now...")
        install_package("pyautogui")

def get_console_window(title):
    """Find the window by its title"""
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"Window with title '{title}' not found.")
    return hwnd

def send_command_to_window(hwnd, command):
    """Send a command to the specified window"""
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)  # Short delay to ensure the window is in focus
        pyautogui.typewrite(command, interval=0.05)
        pyautogui.press('enter')
        print(f"Sent command: {command}")
    else:
        print("No window handle provided.")

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    clear_screen()
    print("Menu:")
    print("1. Trickshot Servers")
    print("0. Exit")

def display_trickshot_servers():
    """Display the trickshot servers"""
    clear_screen()
    print("Trickshot Servers:")
    servers = [
        "Celebrity's Trickshot Server",
        "Celebrity's Trickshot Server 2",
        "Celebrity's Trickshot Server 3",
        "@Brudders FFA [TRICKSHOT LAST OR BAN]",
        "[AU] Gunji x 71st - Vanilla FFA Trickshotting!",
        "[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!",
    ]
    for i, server in enumerate(servers, start=1):
        print(f"{i}. {server}")
    print("0. Back to Main Menu")

def handle_trickshot_choice(choice):
    """Handle the trickshot server selection"""
    servers = [
        "45.61.162.8:27020",    # Celebrity's Trickshot Server
        "45.61.162.8:27021",    # Celebrity's Trickshot Server
        "45.61.162.8:27022",    # Celebrity's Trickshot Server
        "45.62.160.81:27016",   # @Brudders FFA [TRICKSHOT LAST OR BAN]
        "51.161.192.200:27018", # [AU] Gunji x 71st - Vanilla FFA Trickshotting!
        "51.161.192.200:27017" # [AU] Gunji x 71st - Vanilla FFA Trickshotting 2!
    ]
    
    if choice == '0':
        return False
    elif choice.isdigit() and 1 <= int(choice) <= len(servers):
        server_ip = servers[int(choice) - 1]
        hwnd = get_console_window("H2M-Mod: 03361cd0-dirty")
        if hwnd:
            connect_command = f"connect {server_ip}\n"
            send_command_to_window(hwnd, connect_command)
        else:
            print("Command prompt window not found.")
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def main():
    """Main function to run the script"""
    setup()  # Ensure required packages are installed
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                display_trickshot_servers()
                trickshot_choice = input("Enter your choice: ")
                if not handle_trickshot_choice(trickshot_choice):
                    break
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
