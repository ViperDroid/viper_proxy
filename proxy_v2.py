import requests
from bs4 import BeautifulSoup
import os
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# ASCII Art with color
ascii_art = """
     ██╗   ██╗██╗██████╗ ███████╗███████╗██████╗ 
     ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔══██╗
     ██║   ██║██║██████╔╝█████╗  █████╗  ██████╔╝
     ██║   ██║██║██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗
     ╚██████╔╝██║██║     ███████╗███████╗██║  ██║
      ╚═════╝ ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
    Powered by Viper Droid
"""

# Function to print the text with animation
def animated_print(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)  # Print one character at a time
        time.sleep(delay)  # Delay between characters

# Color the ASCII Art (optional, you can modify the colors as you like)
colored_ascii = f"{Fore.RED}{ascii_art}"

# Print the ASCII Art with animation
animated_print(colored_ascii)


# Fetch proxies from a public proxy list
def fetch_proxies():
    url = "https://free-proxy-list.net/"  # Example of a free proxy list site
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.select("table tbody tr"):
        tds = row.find_all("td")
        if len(tds) >= 2:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(f"{ip}:{port}")
    return proxies

# Save proxies to proxy_viper.txt (appending)
def save_proxies(proxy, proxy_file_path):
    try:
        # Open the file in append mode to add valid proxies if it exists
        with open(proxy_file_path, "a") as proxy_file:
            proxy_file.write(proxy + "\n")
        print(f"Proxies successfully saved to {proxy_file_path}.")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Validate proxies and write valid proxies in real-time
def validate_proxies(proxies, test_url="http://httpbin.org/ip", proxy_file_path=None):
    valid_proxies = []  # Make sure valid_proxies is defined here
    for proxy in proxies:
        try:
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            response = requests.get(test_url, proxies=proxy_dict, timeout=5)
            if response.status_code == 200:
                print(f"Valid proxy: {proxy}")
                if proxy_file_path:
                    save_proxies(proxy, proxy_file_path)  # Save valid proxy to the file immediately
                valid_proxies.append(proxy)
        except Exception as e:
            print(f"Invalid proxy: {proxy} ({e})")
    return valid_proxies

# Main Function
def main():
    # Path for the proxy_viper.txt
    proxy_dir = "/home/kali/Desktop/tools/proxy_viper/"
    
    # Ensure the directory exists
    if not os.path.exists(proxy_dir):
        print(f"Creating directory: {proxy_dir}")
        os.makedirs(proxy_dir)  # Create the directory if it doesn't exist
    
    # Define the path for the proxy file
    proxy_file_path = os.path.join(proxy_dir, "proxy_viper.txt")

    # Create the file immediately if it doesn't exist
    if not os.path.exists(proxy_file_path):
        try:
            with open(proxy_file_path, "w") as proxy_file:
                pass  # Create the file and close it if it's empty
            print(f"Created {proxy_file_path}")
        except Exception as e:
            print(f"Error creating file: {e}")

    print("Fetching proxies...")
    proxies = fetch_proxies()
    print(f"Fetched {len(proxies)} proxies.")
    
    print("\nValidating proxies and saving valid ones to proxy_viper.txt...")
    valid_proxies = validate_proxies(proxies, proxy_file_path=proxy_file_path)
    
    print("\nSummary:")
    print(f"Fetched proxies: {len(proxies)}")
    print(f"Valid proxies: {len(valid_proxies)}")

if __name__ == "__main__":
    main()
