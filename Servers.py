import subprocess
import sys
import time
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Error installing package {package}: {e}")
        sys.exit(1)

def ensure_packages():
    """Ensure all required packages are installed"""
    required_packages = [
        "pyautogui",
        "requests",
        "beautifulsoup4",
        "pywin32"  # This package includes win32api, win32con, win32gui
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Required package '{package}' is not installed. Installing now...")
            install_package(package)
    
    print("All required packages are installed.")

def get_console_window(title):
    """Find the window by its title"""
    import win32gui
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"Window with title '{title}' not found.")
    return hwnd

def send_command_to_window(hwnd, command):
    """Send a command to the specified window"""
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
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    clear_screen()
    print("Menu:")
    print("1. Trickshot Servers")
    print("2. Server Browser")
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

def handle_trickshot_choice(choice, servers):
    """Handle the trickshot server selection"""
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

def scrape_h2m_trickshot_servers(url):
    """Scrape H2M trickshot servers from the specified URL"""
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the H2M servers section
    h2m_panel = soup.find('div', id='H2M_servers')
    if not h2m_panel:
        print("H2M servers section not found. Check the HTML structure.")
        return []

    # Find the server table within the H2M servers section
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
        if data_ip and data_port:
            ip_port_list.append((data_ip, data_port, server_name, mode))

    return ip_port_list

def handle_scraped_servers_choice():
    """Handle the scraped trickshot server selection"""
    url = 'https://master.iw4.zip/servers'
    servers = scrape_h2m_trickshot_servers(url)

    if not servers:
        print("No H2M trickshot servers found.")
        return True

    clear_screen()
    print("Scraped H2M Trickshot Servers:")
    for i, (ip, port, server_name, mode) in enumerate(servers, start=1):
        print(f"{i}. {server_name} - {mode}")

    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '0':
        return True
    elif choice.isdigit() and 1 <= int(choice) <= len(servers):
        ip, port, server_name, mode = servers[int(choice) - 1]
        connect_command = f"connect {ip}:{port}\n"
        hwnd = get_console_window("H2M-Mod: 03361cd0-dirty")
        if hwnd:
            send_command_to_window(hwnd, connect_command)
        else:
            print("Command prompt window not found.")
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def main():
    """Main function to run the script"""
    ensure_packages()  # Ensure required packages are installed
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            servers = [
                "45.61.162.8:27020",    # Celebrity's Trickshot Server
                "45.61.162.8:27021",    # Celebrity's Trickshot Server
                "45.61.162.8:27022",    # Celebrity's Trickshot Server
                "45.62.160.81:27016",   # @Brudders FFA [TRICKSHOT LAST OR BAN]
                "51.161.192.200:27018", # [AU] Gunji x 71st - Vanilla FFA Trickshotting!
                "51.161.192.200:27017" # [AU] Gunji x 71st - Vanilla FFA Trickshotting 2!
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
