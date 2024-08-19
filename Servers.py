import subprocess
import sys
import os
import time
import importlib

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Error installing package {package}: {e}")
        sys.exit(1)

def check_and_install_package(package):
    """Check if a package is installed and install it if not."""
    try:
        importlib.import_module(package)
        print(f"Package '{package}' is already installed.")
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        install_package(package)

def install_required_packages():
    """Ensure all required packages are installed."""
    packages = [
        "pyautogui",
        "pywin32",
        "beautifulsoup4",
        "requests"
    ]
    for package in packages:
        check_and_install_package(package)

def get_console_window(title):
    """Find the window by its title."""
    import win32gui
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"Window with title '{title}' not found.")
    return hwnd

def send_command_to_window(hwnd, command):
    """Send a command to the specified window."""
    import pyautogui
    import win32gui
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)  # Short delay to ensure the window is in focus
        pyautogui.typewrite(command, interval=0.05)
        pyautogui.press('enter')
        print(f"Sent command: {command}")
    else:
        print("No window handle provided.")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu."""
    clear_screen()
    print("Menu:")
    print("1. Trickshot Servers")
    print("2. Server Browser")
    print("0. Exit")

def display_trickshot_servers():
    """Display the trickshot servers without showing IPs."""
    clear_screen()
    print("Trickshot Servers:")
    servers = [
        ("Celebrity's Trickshot Server", "45.61.162.8:27020"),
        ("Celebrity's Trickshot Server 2", "45.61.162.8:27021"),
        ("Celebrity's Trickshot Server 3", "45.61.162.8:27022"),
        ("@Brudders FFA [TRICKSHOT LAST OR BAN]", "45.62.160.81:27016"),
        ("[AU] Gunji x 71st - Vanilla FFA Trickshotting!", "51.161.192.200:27018"),
        ("[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!", "51.161.192.200:27017")
    ]
    for i, (name, _) in enumerate(servers, start=1):
        print(f"{i}. {name}")
    print("0. Back to Main Menu")

def handle_trickshot_choice(choice, servers):
    """Handle the trickshot server selection."""
    if choice == '0':
        return False
    elif choice.isdigit() and 1 <= int(choice) <= len(servers):
        server_name, server_ip = servers[int(choice) - 1]
        hwnd = get_console_window("H2M-Mod: 03361cd0-dirty")
        if hwnd:
            disconnect_command = "disconnect\n"
            connect_command = f"connect {server_ip}\n"
            send_command_to_window(hwnd, disconnect_command)
            time.sleep(1)  # Short delay to ensure disconnect completes
            send_command_to_window(hwnd, connect_command)
        else:
            print("Command prompt window not found.")
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def scrape_h2m_trickshot_servers(url):
    """Scrape H2M trickshot servers from the specified URL."""
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    h2m_panel = soup.find('div', id='H2M_servers')
    if not h2m_panel:
        print("H2M servers section not found. Check the HTML structure.")
        return []

    server_table = h2m_panel.find('table', class_='table table-striped table-hover table-responsive table-outer-bordered')
    if not server_table:
        print("Server table not found within H2M servers section.")
        return []

    ip_port_list = []
    table_rows = server_table.find_all('tr', class_='server-row')

    for row in table_rows:
        data_ip = row.get('data-ip')
        data_port = row.get('data-port')
        server_name = row.find('td').get_text(strip=True)
        mode = row.find_all('td')[3].get_text(strip=True)
        
        player_count_td = row.find('td', class_='server-clientnum')
        if player_count_td:
            player_count = player_count_td.get_text(strip=True)
        else:
            player_count = "Unknown"

        if data_ip and data_port:
            ip_port_list.append((server_name, data_ip, data_port, mode, player_count))

    return ip_port_list

def display_scraped_servers(servers):
    """Display the scraped trickshot servers with player counts."""
    clear_screen()
    print("Scraped H2M Trickshot Servers:")
    for i, (server_name, ip, port, mode, player_count) in enumerate(servers, start=1):
        try:
            current_players, max_players = map(int, player_count.split('/'))
        except ValueError:
            current_players = 0
            max_players = 0

        if max_players <= 18:
            color = '\033[91m' if current_players == max_players else '\033[92m'
        else:
            color = '\033[0m'

        print(f"{i}. {server_name} - {mode} - {color}{player_count}\033[0m")

    print("0. Back to Main Menu")

def handle_scraped_servers_choice():
    """Handle the scraped trickshot server selection."""
    url = 'https://master.iw4.zip/servers'
    servers = scrape_h2m_trickshot_servers(url)

    if not servers:
        print("No H2M trickshot servers found.")
        return True

    display_scraped_servers(servers)

    choice = input("Enter your choice: ")

    if choice == '0':
        return False
    elif choice.isdigit() and 1 <= int(choice) <= len(servers):
        server_name, ip, port, mode, player_count = servers[int(choice) - 1]
        connect_command = f"connect {ip}:{port}\n"
        hwnd = get_console_window("H2M-Mod: 03361cd0-dirty")
        if hwnd:
            disconnect_command = "disconnect\n"
            send_command_to_window(hwnd, disconnect_command)
            time.sleep(1)  # Short delay to ensure disconnect completes
            send_command_to_window(hwnd, connect_command)
        else:
            print("Command prompt window not found.")
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def main():
    """Main function to run the script."""
    install_required_packages()  # Ensure required packages are installed
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            servers = [
                ("Celebrity's Trickshot Server", "45.61.162.8:27020"),
                ("Celebrity's Trickshot Server 2", "45.61.162.8:27021"),
                ("Celebrity's Trickshot Server 3", "45.61.162.8:27022"),
                ("@Brudders FFA [TRICKSHOT LAST OR BAN]", "45.62.160.81:27016"),
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting!", "51.161.192.200:27018"),
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!", "51.161.192.200:27017")
            ]
            while True:
                display_trickshot_servers()
                trickshot_choice = input("Enter your choice: ")
                if not handle_trickshot_choice(trickshot_choice, servers):
                    break
        elif choice == '2':
            while True:
                if not handle_scraped_servers_choice():
                    break
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
