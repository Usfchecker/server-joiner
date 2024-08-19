import subprocess
import sys
import time
import os
import requests

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
        "requests"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Required package '{package}' is not installed. Installing now...")
            install_package(package)

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
        command = f"connect {server_ip}"
        subprocess.Popen(['cmd', '/c', 'echo', command], shell=True)  # Open a new command prompt and echo the command
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

def handle_scraped_servers_choice():
    """Handle the scraped trickshot server selection"""
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
        connect_command = f"connect {ip}:{port}"
        subprocess.Popen(['cmd', '/c', 'echo', connect_command], shell=True)  # Open a new command prompt and echo the command
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
            servers = [
                ("Celebrity's Trickshot Server", "45.61.162.8:27020"),    # Celebrity's Trickshot Server
                ("Celebrity's Trickshot Server 2", "45.61.162.8:27021"),    # Celebrity's Trickshot Server
                ("Celebrity's Trickshot Server 3", "45.61.162.8:27022"),    # Celebrity's Trickshot Server
                ("@Brudders FFA [TRICKSHOT LAST OR BAN]", "45.62.160.81:27016"),   # @Brudders FFA [TRICKSHOT LAST OR BAN]
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting!", "51.161.192.200:27018"), # [AU] Gunji x 71st - Vanilla FFA Trickshotting!
                ("[AU] Gunji x 71st - Vanilla FFA Trickshotting 2!", "51.161.192.200:27017")  # [AU] Gunji x 71st - Vanilla FFA Trickshotting 2!
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
