
import subprocess
import sys
import time
import os
import requests
from bs4 import BeautifulSoup
import pyautogui
import win32gui
import win32con

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Error installing package {package}: {e}")
        sys.exit(1)

def setup():
    """Ensure all required packages are installed"""
    required_packages = [
        "pyautogui",
        "requests",
        "beautifulsoup4",
        "pywin32"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Required package '{package}' is not installed. Installing now...")
            install_package(package)

def get_window_handle(title):
    """Find the window by its title"""
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"Window with title '{title}' not found.")
    return hwnd

def hide_window(hwnd):
    """Hide the specified window"""
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        print(f"Hid window with title '{win32gui.GetWindowText(hwnd)}'.")
    else:
        print("No window handle provided.")

def show_window(hwnd):
    """Show the specified window"""
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        print(f"Showed window with title '{win32gui.GetWindowText(hwnd)}'.")
    else:
        print("No window handle provided.")

def minimize_window(hwnd):
    """Minimize the specified window"""
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        print(f"Minimized window with title '{win32gui.GetWindowText(hwnd)}'.")
    else:
        print("No window handle provided.")

def send_commands_to_window(hwnd, commands):
    """Send multiple commands to the specified window"""
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)  # Short delay to ensure the window is in focus
        for command in commands:
            pyautogui.typewrite(command, interval=0.05)
            pyautogui.press('enter')
            time.sleep(0.5)  # Delay between commands
        print(f"Sent commands: {commands}")
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
    """Display the trickshot servers without showing IPs"""
    clear_screen()
    print("Trickshot Servers:")
    servers = [
        ("Celebrity's Trickshot Server", "45.61.162.8:27020"),    # Celebrity's Trickshot Server
        ("Celebrity's Trickshot Server 2", "45.61.162.8:27021"),    # Celebrity's Trickshot Server
        ("Celebrity's Trickshot Server 3", "45.61.162.8:27022"),    # Celebrity's Trickshot Server
        ("@Brudders FFA [TRICKSHOT LAST OR BAN]", "45.62.160.81:27016"),   # @Brudders FFA [TRICKSHOT LAST OR BAN]
        ("[AU] Gunji x 71st - Vanilla FFA Trickshotting!", "51.161.192.200:27018"), # [AU] Gunji x 71st - Vanilla FFA Trickshotting!
        ("[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!", "51.161.192.200:27017")  # [AU] Gunji x 71st - Vanilla FFA Trickshotting 2!
    ]
    for i, (name, _) in enumerate(servers, start=1):
        print(f"{i}. {name}")
    print("0. Back to Main Menu")

def handle_trickshot_choice(choice, servers):
    """Handle the trickshot server selection"""
    if choice == '0':
        return False
    elif choice.isdigit() and 1 <= int(choice) <= len(servers):
        server_name, server_ip = servers[int(choice) - 1]
        hwnd = get_window_handle("H2M-Mod: 03361cd0-dirty")
        if hwnd:
            show_window(hwnd)  # Ensure the window is visible
            send_commands_to_window(hwnd, ['disconnect', f'connect {server_ip}'])
            minimize_window(hwnd)  # Minimize the window after sending commands
        else:
            print("Window with title 'H2M-Mod: 03361cd0-dirty' not found.")
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def scrape_h2m_trickshot_servers(url):
    """Scrape H2M trickshot servers from the specified URL"""
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
        
        # Find the player count
        player_count_td = row.find('td', class_='server-clientnum')
        if player_count_td:
            player_count = player_count_td.get_text(strip=True)
        else:
            player_count = "Unknown"

        if data_ip and data_port:
            ip_port_list.append((server_name, data_ip, data_port, mode, player_count))

    return ip_port_list

def filter_servers_by_mode(servers, mode_filter):
    """Filter the servers based on the game mode"""
    return [server for server in servers if mode_filter.lower() in server[3].lower()]

def display_scraped_servers(servers):
    """Display the scraped trickshot servers with player counts"""
    clear_screen()
    print("Scraped H2M Trickshot Servers:")
    for i, (server_name, ip, port, mode, player_count) in enumerate(servers, start=1):
        # Extract current and max player counts
        try:
            current_players, max_players = map(int, player_count.split('/'))
        except ValueError:
            current_players = 0
            max_players = 0

        # Color coding based on player count
        if max_players <= 18:
            color = '\033[91m' if current_players == max_players else '\033[92m'  # Red for full, green otherwise
        else:
            color = '\033[0m'  # Default color

        print(f"{i}. {server_name} - {mode} - {color}{player_count}\033[0m")  # Reset color after player count

    print("0. Back to Main Menu")

def display_game_modes():
    """Display the game modes using a dictionary"""
    clear_screen()
    game_modes = {
        "hp": "Hard Point",
        "dom": "Domination",
        "dm": "Free For All",
        "gun": "Gun Game",
        "war": "Team Death Match",
        "sd": "Search And Destroy",
        "conf": "Kill Confirmed"
    }

    print("Game Modes Options:")
    for code, name in game_modes.items():
        print(f"{code} - {name}")
    print()

def handle_scraped_servers_choice(is_filtered):
    """Handle the scraped trickshot server selection"""
    url = 'https://master.iw4.zip/servers'
    servers = scrape_h2m_trickshot_servers(url)

    if not servers:
        print("No H2M trickshot servers found.")
        return True

    while True:
        clear_screen()
        print("1. Show all servers")
        print("2. Filter by game mode")
        print("0. Back to Main Menu" if not is_filtered else "0. Back to Game Mode Filter")
        filter_choice = input("Enter your choice: ")

        if filter_choice == '1':
            display_scraped_servers(servers)
            choice = input("Enter your choice: ")
            if choice == '0':
                return True if not is_filtered else False
            elif choice.isdigit() and 1 <= int(choice) <= len(servers):
                server_name, ip, port, mode, player_count = servers[int(choice) - 1]
                hwnd = get_window_handle("H2M-Mod: 03361cd0-dirty")
                if hwnd:
                    show_window(hwnd)  # Ensure the window is visible
                    send_commands_to_window(hwnd, ['disconnect', f'connect {ip}:{port}'])
                    minimize_window(hwnd)  # Minimize the window after sending commands
                else:
                    print("Window with title 'H2M-Mod: 03361cd0-dirty' not found.")
            else:
                print("Invalid choice. Please select a valid option.")
        elif filter_choice == '2':
            display_game_modes()
            mode_filter = input("Enter game mode to filter by: ")
            filtered_servers = filter_servers_by_mode(servers, mode_filter)
            display_scraped_servers(filtered_servers)
            choice = input("Enter your choice: ")
            if choice == '0':
                return True if not is_filtered else False
            elif choice.isdigit() and 1 <= int(choice) <= len(filtered_servers):
                server_name, ip, port, mode, player_count = filtered_servers[int(choice) - 1]
                hwnd = get_window_handle("H2M-Mod: 03361cd0-dirty")
                if hwnd:
                    show_window(hwnd)  # Ensure the window is visible
                    send_commands_to_window(hwnd, ['disconnect', f'connect {ip}:{port}'])
                    minimize_window(hwnd)  # Minimize the window after sending commands
                else:
                    print("Window with title 'H2M-Mod: 03361cd0-dirty' not found.")
            else:
                print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid choice. Please select a valid option.")

# Main execution
if __name__ == "__main__":
    setup()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            display_trickshot_servers()
            server_choice = input("Enter your choice: ")
            if handle_trickshot_choice(server_choice, [
                ("Celebrity's Trickshot Server", "45.61.162.8:27020"),
                ("Celebrity's Trickshot Server 2", "45.61.162.8:27021"),
                ("Celebrity's Trickshot Server 3", "45.61.162.8:27022"),
                ("@Brudders FFA [TRICKSHOT LAST OR BAN]", "45.62.160.81:27016"),
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting!", "51.161.192.200:27018"),
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!", "51.161.192.200:27017")
            ]) == False:
                break
        elif choice == '2':
            if not handle_scraped_servers_choice(is_filtered=False):
                break
        elif choice == '0':
            sys.exit()
        else:
            print("Invalid choice. Please select a valid option.")
