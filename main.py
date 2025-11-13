#!/usr/bin/env python3
# Installer untuk dependencies Alat Bantu

import subprocess
import sys
import os
import time
import threading
import random

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class SoundPlayer:
    """Class untuk memutar sound di Termux"""
    
    @staticmethod
    def check_termux_api():
        """Cek apakah termux-api terinstall dan tersedia"""
        try:
            # Cek apakah perintah termux-media-player tersedia
            result = subprocess.run(["which", "termux-media-player"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return False
                
            # Test dengan perintah sederhana
            test_result = subprocess.run(["termux-media-player", "-h"], 
                                       capture_output=True, text=True, timeout=5)
            return test_result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def check_sound_dependencies():
        """Cek semua dependencies sound"""
        sound_available = SoundPlayer.check_termux_api()
        
        # Cek apakah ada aplikasi Termux:API di Android
        try:
            result = subprocess.run(["termux-api-start"], 
                                  capture_output=True, text=True)
            # Jika berhasil mulai service, berarti tersedia
            if result.returncode == 0:
                return True
        except:
            pass
            
        return sound_available
    
    @staticmethod
    def play_sound_advanced(sound_type="success"):
        """Metode advanced untuk memutar sound dengan fallback"""
        if not SoundPlayer.check_sound_dependencies():
            print(f"{Colors.YELLOW}[SOUND] Termux-API tidak tersedia, menggunakan fallback...{Colors.RESET}")
            return SoundPlayer.play_fallback_sound(sound_type)
            
        try:
            # Gunakan termux-media-player dengan file local jika ada
            sound_files = {
                "success": "/blog/positive.mp3",
                "error": "/blog/error.mp3", 
                "warning": "/blog/alert.mp3",
                "complete": "/blog/complete.mp3",
                "startup": "/blog/startup.mp3"
            }
            
            # Fallback ke system sounds
            fallback_urls = {
                "success": "https://www.soundjay.com/buttons/sounds/button-09.mp3",
                "error": "https://www.soundjay.com/buttons/sounds/button-10.mp3",
                "warning": "https://www.soundjay.com/buttons/sounds/beep-01a.mp3",
                "complete": "https://www.soundjay.com/buttons/sounds/button-09.mp3",
                "startup": "https://www.soundjay.com/buttons/sounds/button-3.mp3"
            }
            
            sound_file = sound_files.get(sound_type)
            
            # Coba file local dulu
            if sound_file and os.path.exists(sound_file):
                subprocess.Popen([
                    "termux-media-player", "play", sound_file
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            else:
                # Download dan play dari URL
                temp_file = f"/data/data/com.termux/files/usr/tmp/sound_{sound_type}.mp3"
                url = fallback_urls.get(sound_type)
                
                # Download sound
                download_cmd = f"curl -s -L '{url}' -o '{temp_file}' --connect-timeout 10"
                subprocess.run(download_cmd, shell=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                time.sleep(0.5)
                
                # Play sound
                if os.path.exists(temp_file):
                    subprocess.Popen([
                        "termux-media-player", "play", temp_file
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # Cleanup setelah beberapa detik
                    threading.Timer(5.0, lambda: os.remove(temp_file) if os.path.exists(temp_file) else None).start()
                    return True
                    
            return False
            
        except Exception as e:
            print(f"{Colors.RED}[SOUND ERROR] {e}{Colors.RESET}")
            return SoundPlayer.play_fallback_sound(sound_type)
    
    @staticmethod
    def play_fallback_sound(sound_type="success"):
        """Fallback sound menggunakan termux-beep dan termux-vibrate"""
        try:
            # Konfigurasi untuk berbagai jenis sound
            sound_configs = {
                "success": {"beep": True, "vibrate": 200, "freq": 1000, "duration": 300},
                "error": {"beep": True, "vibrate": 500, "freq": 500, "duration": 500},
                "warning": {"beep": True, "vibrate": 300, "freq": 800, "duration": 200},
                "complete": {"beep": True, "vibrate": 400, "freq": 1200, "duration": 400},
                "startup": {"beep": True, "vibrate": 100, "freq": 1500, "duration": 100}
            }
            
            config = sound_configs.get(sound_type, sound_configs["success"])
            
            # Play vibration jika tersedia
            if config.get("vibrate"):
                try:
                    subprocess.Popen([
                        "termux-vibrate", "-d", str(config["vibrate"])
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    pass
            
            # Play beep jika tersedia
            if config.get("beep"):
                try:
                    subprocess.Popen([
                        "termux-beep", "-f", str(config["freq"]), "-d", str(config["duration"])
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[FALLBACK SOUND ERROR] {e}{Colors.RESET}")
            return False
    
    @staticmethod
    def play_beep(frequency=1000, duration=200):
        """Memutar beep sound menggunakan termux-beep"""
        try:
            subprocess.Popen([
                "termux-beep", "-f", str(frequency), "-d", str(duration)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False
    
    @staticmethod
    def play_vibration(duration=500):
        """Memutar vibration"""
        try:
            subprocess.Popen([
                "termux-vibrate", "-d", str(duration)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False
    
    @staticmethod
    def play_complex_sound(sound_type="success"):
        """Memutar sound dengan kombinasi berbagai metode"""
        # Coba metode advanced dulu
        if SoundPlayer.play_sound_advanced(sound_type):
            return True
        
        # Fallback ke metode sederhana
        return SoundPlayer.play_fallback_sound(sound_type)

def show_ascii_art():
    """Menampilkan ASCII art"""
    ascii_art = f"""
{Colors.CYAN}
╔═════════════════════════════════════╗
║                       ▒░░░          ║
║                      ░▒▒░░          ║
║                     ▒▒▒▒░░          ║
║       ▒▒░░▒   ▒░░░░▒▒▒▒▒░▒          ║
║     ░░░░░░▒▒░░░░░░░░░▒▒▒▒           ║
║ ▒░░░░▒▒▒▒▒░░░░░░░░░░░░░▒▒▒          ║
║   ▒▒▓   ▒░▒░░▓▓▓▓▓▒░░░░░░▒▒         ║
║        ▓░░░▓▓▓▓▒▓▓▓▓▓░░░░░▒         ║
║        ▒░▒▓▓▒▓▓▓▓▓▒▓▓▓▒░░░░▒        ║
║        ░░▓▓▒░▒▓▒▒▒▒▒▒▓▓▒░░░▒        ║
║       ▒░▒▓▒▓░█░░░░▒█▓▓▓▓░░░▒▒       ║
║       ▒░▒▓▓▒░░░░░░░░▒▓▓▓▓░░▒▒       ║
║       ▒░▓▓▓▓░░░░░░░░▒▓▓▓░▒▒▒▓       ║
║        ▒▓▓▓▓▒▒▒▒░░▒▓▓▓▓▒▒░░░▒       ║
║                                     ║
║ █░█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█ █▀█ █▀▀ █▀▀ ║
║ █▀█ █▀█ █▄▄ █░█ █▀░ █▄█ █▀▄ █▄█ ██▄ ║
║                                     ║
║         HACKFORGE INSTALLER         ║
║    Dependency Installation Tool     ║
║                                     ║
║[•] Installing required packages...  ║
║[•] Setting up environment...        ║
║[•] Preparing tools...               ║
╚═════════════════════════════════════╝
{Colors.RESET}
    """
    print(ascii_art)
    
    # Play startup sound dengan delay
    time.sleep(0.5)
    SoundPlayer.play_complex_sound("startup")

def animate_selection(choice):
    """Animasi ketika memilih menu"""
    choices = {
        1: "Manual Installation",
        2: "Requirements Installation", 
        3: "Running HackForge",
        4: "Run Web Script (PHP Admin)",
        5: "Run Ekploitasi Hacking (Games)",
        6: "Exit"
    }
    
    text = f"Memilih: {choices[choice]}"
    chars = ["▹▹▹▹▹", "▸▹▹▹▹", "▹▸▹▹▹", "▹▹▸▹▹", "▹▹▹▸▹", "▹▹▹▹▸"]
    
    print(f"\n{Colors.MAGENTA}{'='*50}{Colors.RESET}")
    for i in range(len(chars)):
        print(f"\r{Colors.CYAN}{chars[i]}{Colors.RESET} {Colors.BOLD}{text}{Colors.RESET}", end="", flush=True)
        time.sleep(0.1)
    print(f"\r{Colors.GREEN}✓✓✓✓✓{Colors.RESET} {Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{'='*50}{Colors.RESET}")
    
    # Play selection sound
    SoundPlayer.play_complex_sound("success")
    time.sleep(0.5)

def animate_bar_chart(title, duration=2, width=40):
    """Animasi bar chart yang mengisi secara progresif"""
    print(f"\n{Colors.BLUE}{title}{Colors.RESET}")
    
    start_time = time.time()
    elapsed = 0
    
    while elapsed < duration:
        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1.0)
        
        # Buat bar chart
        bar_width = int(width * progress)
        bar = "█" * bar_width + "░" * (width - bar_width)
        percentage = int(progress * 100)
        
        # Efek warna berbeda berdasarkan progress
        if progress < 0.5:
            color = Colors.RED
        elif progress < 0.8:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
            
        print(f"\r{color}[{bar}] {percentage}%{Colors.RESET}", end="", flush=True)
        time.sleep(0.05)
    
    print(f"\r{Colors.GREEN}[{'█' * width}] 100%{Colors.RESET}")

def animate_loading(text, duration=2):
    """Animasi loading dengan berbagai style"""
    # Pilih style animasi secara random
    styles = [
        ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],  # Classic
        ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],  # Circle
        ["▹▹▹▹▹", "▸▹▹▹▹", "▹▸▹▹▹", "▹▹▸▹▹", "▹▹▹▸▹", "▹▹▹▹▸"],  # Arrow
        ["◐", "◓", "◑", "◒"],  # Simple circle
        ["⢀", "⡀", "⡄", "⡆", "⡇", "⡏", "⡟", "⡿", "⣿", "⣷", "⣯", "⣟", "⡏", "⡇", "⡆", "⡄"]  # Bar fill
    ]
    
    chars = random.choice(styles)
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        print(f"\r{Colors.YELLOW}{chars[i % len(chars)]}{Colors.RESET} {text}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    
    print(f"\r{Colors.GREEN}✓{Colors.RESET} {text}")

def run_command(command, description):
    """Jalankan command dengan animasi loading"""
    print(f"\n{Colors.BLUE}[→]{Colors.RESET} {description}")
    print(f"{Colors.WHITE}   Command: {command}{Colors.RESET}")
    
    # Animasi loading selama proses
    loading_thread = threading.Thread(target=animate_loading, args=(f"Installing...",))
    loading_thread.start()
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              timeout=120)
        loading_thread.join(timeout=0.1)
        print(f"\r{Colors.GREEN}✓{Colors.RESET} {description} - Berhasil!")
        
        # Play success sound
        SoundPlayer.play_complex_sound("success")
        
        if result.stdout:
            print(f"{Colors.GREEN}   Output: {result.stdout.strip()}{Colors.RESET}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        loading_thread.join(timeout=0.1)
        print(f"\r{Colors.RED}✗{Colors.RESET} {description} - Gagal!")
        
        # Play error sound
        SoundPlayer.play_complex_sound("error")
        
        print(f"{Colors.RED}   Error: {e.stderr.strip()}{Colors.RESET}")
        return False, e.stderr
    except subprocess.TimeoutExpired:
        loading_thread.join(timeout=0.1)
        print(f"\r{Colors.RED}✗{Colors.RESET} {description} - Timeout!")
        
        # Play error sound
        SoundPlayer.play_complex_sound("error")
        
        return False, "Command timeout"

def check_python_package(package):
    """Cek apakah package Python sudah terinstall"""
    try:
        if package == "dnspython":
            import dns.resolver
            return True
        elif package == "beautifulsoup4":
            import bs4
            return True
        else:
            __import__(package.replace('-', '_'))
        return True
    except ImportError:
        return False

def show_menu():
    """Menampilkan menu pilihan dengan animasi"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}𝓟𝓘𝓛𝓘𝓗𝓐𝓝 𝓘𝓝𝓢𝓣𝓐𝓛𝓐𝓢𝓘 𝓗𝓐𝓒𝓚𝓕𝓞𝓡𝓖𝓔{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    # Check sound availability
    sound_available = SoundPlayer.check_sound_dependencies()
    sound_status = f"{Colors.GREEN}🔊 Sound: ON{Colors.RESET}" if sound_available else f"{Colors.RED}🔇 Sound: OFF{Colors.RESET}"
    print(f"          {sound_status}")
    
    # Animasi menu items
    menu_items = [
        f"  {Colors.GREEN}1{Colors.RESET} - Install dependencies manual (package Termux)",
        f"  {Colors.GREEN}2{Colors.RESET} - Install py requirements.txt", 
        f"  {Colors.GREEN}3{Colors.RESET} - Running Now HackForge (skip instalasi)",
        f"  {Colors.GREEN}4{Colors.RESET} - Run Web Script (PHP Admin)",
        f"  {Colors.GREEN}5{Colors.RESET} - Run Ekploitasi Hacking (Games)",
        f"  {Colors.GREEN}6{Colors.RESET} - Keluar"
    ]
    
    for item in menu_items:
        print(item)
        time.sleep(0.1)
    
    while True:
        try:
            choice = input(f"\n{Colors.YELLOW}Pilih opsi (1-6): {Colors.RESET}").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print(f"{Colors.RED}Pilihan tidak valid! Silakan pilih 1-6.{Colors.RESET}")
                SoundPlayer.play_complex_sound("error")
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Operasi dibatalkan.{Colors.RESET}")
            SoundPlayer.play_complex_sound("error")
            sys.exit(1)

def install_termux_api():
    """Install dan setup Termux API"""
    print(f"\n{Colors.BLUE}[SOUND] Menginstall Termux API...{Colors.RESET}")
    
    commands = [
        "pkg update -y",
        "pkg install termux-api -y",
        "termux-api-start"
    ]
    
    for cmd in commands:
        success, output = run_command(cmd, f"Executing: {cmd.split()[0]}")
        if not success and "termux-api-start" in cmd:
            # termux-api-start mungkin gagal tapi tidak masalah
            print(f"{Colors.YELLOW}⚠️  termux-api-start mungkin tidak diperlukan{Colors.RESET}")
    
    # Verifikasi instalasi
    if SoundPlayer.check_sound_dependencies():
        print(f"{Colors.GREEN}✓ Termux API berhasil diinstall!{Colors.RESET}")
        SoundPlayer.play_complex_sound("success")
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Termux API terinstall tetapi mungkin memerlukan aplikasi Android{Colors.RESET}")
        return False

def fix_dnspython_issue():
    """Perbaiki issue dnspython yang umum"""
    print(f"\n{Colors.YELLOW}[🔧] Memperbaiki issue dnspython...{Colors.RESET}")
    
    solutions = [
        "pip uninstall dnspython -y && pip install dnspython",
        "python -m pip install --force-reinstall dnspython", 
        "pip install --upgrade dnspython"
    ]
    
    for i, solution in enumerate(solutions, 1):
        animate_bar_chart(f"Memperbaiki dnspython (coba {i}/3)", duration=1)
        success, output = run_command(solution, f"Memperbaiki dnspython (coba {i})")
        if success:
            if check_python_package("dnspython"):
                print(f"{Colors.GREEN}✓ Issue dnspython berhasil diperbaiki!{Colors.RESET}")
                SoundPlayer.play_complex_sound("success")
                return True
    return False

def install_manual():
    """Install dependencies manual package per package"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}INSTALASI MANUAL - Package per Package{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    python_packages = [
        "requests", "dnspython", "tqdm", "argparse", 
        "tabulate", "urllib3", "beautifulsoup4"
    ]
    
    # Animasi inisialisasi
    animate_bar_chart("Memulai instalasi manual", duration=1.5)
    
    # Step 1: Update package manager
    if os.name != 'nt':
        print(f"\n{Colors.BLUE}[STEP 1] Update Package Manager{Colors.RESET}")
        success, output = run_command("pkg update -y", "Update package repository")
    
    # Step 2: Install system packages
    if os.name != 'nt':
        print(f"\n{Colors.BLUE}[STEP 2] Install System Packages{Colors.RESET}")
        system_packages = ["openssl", "whois", "curl"]
        
        for pkg in system_packages:
            success, output = run_command(f"pkg install {pkg} -y", f"Install system package: {pkg}")
    
    # Step 3: Upgrade pip
    print(f"\n{Colors.BLUE}[STEP 3] Setup Python Environment{Colors.RESET}")
    success, output = run_command("python -m pip install --upgrade pip", "Upgrade pip")
    
    # Step 4: Install Python packages dengan progress bar
    print(f"\n{Colors.BLUE}[STEP 4] Install Python Packages{Colors.RESET}")
    
    installed_count = 0
    total_packages = len(python_packages)
    
    for i, package in enumerate(python_packages, 1):
        animate_bar_chart(f"Progress instalasi ({i}/{total_packages})", duration=0.5)
        
        if check_python_package(package):
            print(f"{Colors.GREEN}✓{Colors.RESET} {package} sudah terinstall")
            installed_count += 1
        else:
            success, output = run_command(f"pip install {package}", f"Install Python package: {package}")
            if success:
                if package == "dnspython" and not check_python_package("dnspython"):
                    print(f"{Colors.YELLOW}⚠️  dnspython terinstall tapi tidak bisa diimport, memperbaiki...{Colors.RESET}")
                    if fix_dnspython_issue():
                        installed_count += 1
                else:
                    installed_count += 1
    
    return installed_count, total_packages

def install_from_requirements():
    """Install dari file requirements.txt"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}INSTALASI DARI REQUIREMENTS.TXT{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    animate_bar_chart("Mempersiapkan requirements.txt", duration=1.5)
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"{Colors.RED}✗ File {requirements_file} tidak ditemukan!{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        print(f"{Colors.YELLOW}Membuat file requirements.txt...{Colors.RESET}")
        
        requirements_content = """requests>=2.28.0
dnspython>=2.2.0
tqdm>=4.64.0
argparse>=1.4.0
tabulate>=0.8.0
urllib3>=1.26.0
beautifulsoup4>=4.11.0
"""
        with open(requirements_file, 'w') as f:
            f.write(requirements_content)
        print(f"{Colors.GREEN}✓ File requirements.txt berhasil dibuat{Colors.RESET}")
        SoundPlayer.play_complex_sound("success")
    
    # Step 1-3: System preparation
    if os.name != 'nt':
        print(f"\n{Colors.BLUE}[STEP 1] Update Package Manager{Colors.RESET}")
        success, output = run_command("pkg update -y", "Update package repository")
    
    if os.name != 'nt':
        print(f"\n{Colors.BLUE}[STEP 2] Install System Packages{Colors.RESET}")
        system_packages = ["openssl", "whois", "curl"]
        
        for pkg in system_packages:
            success, output = run_command(f"pkg install {pkg} -y", f"Install system package: {pkg}")
    
    print(f"\n{Colors.BLUE}[STEP 3] Setup Python Environment{Colors.RESET}")
    success, output = run_command("python -m pip install --upgrade pip", "Upgrade pip")
    
    # Step 4: Install dari requirements.txt
    print(f"\n{Colors.BLUE}[STEP 4] Install dari requirements.txt{Colors.RESET}")
    animate_bar_chart("Instalasi dari requirements.txt", duration=2)
    success, output = run_command(f"pip install -r {requirements_file}", "Install semua dependencies dari requirements.txt")
    
    if not check_python_package("dnspython"):
        print(f"{Colors.YELLOW}⚠️  dnspython ada issue, memperbaiki...{Colors.RESET}")
        fix_dnspython_issue()
    
    if success:
        try:
            with open(requirements_file, 'r') as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            return len(packages), len(packages)
        except:
            return 1, 1
    else:
        return 0, 1

def check_and_fix_dependencies():
    """Cek dan perbaiki dependencies sebelum running"""
    print(f"\n{Colors.BLUE}[CHECK] Memeriksa dependencies dasar...{Colors.RESET}")
    
    animate_bar_chart("Memindai dependencies", duration=1.5)
    
    basic_packages = ["requests", "dnspython", "tqdm", "tabulate", "bs4"]
    missing_packages = []
    
    for package in basic_packages:
        if not check_python_package(package):
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Colors.YELLOW}⚠️  Beberapa dependencies tidak ditemukan: {', '.join(missing_packages)}{Colors.RESET}")
        SoundPlayer.play_complex_sound("warning")
        
        if "dnspython" in missing_packages:
            print(f"{Colors.YELLOW}🔧 Mencoba memperbaiki dnspython secara otomatis...{Colors.RESET}")
            if fix_dnspython_issue():
                missing_packages.remove("dnspython")
        
        if missing_packages:
            print(f"{Colors.YELLOW}   Tool mungkin tidak berjalan dengan baik.{Colors.RESET}")
            
            install_missing = input(f"\n{Colors.YELLOW}Install dependencies yang missing? (y/N): {Colors.RESET}").strip().lower()
            if install_missing in ['y', 'yes']:
                for package in missing_packages:
                    if package == "bs4":
                        package = "beautifulsoup4"
                    success, output = run_command(f"pip install {package}", f"Install {package}")
                    if package == "dnspython" and success and not check_python_package("dnspython"):
                        fix_dnspython_issue()
    else:
        print(f"{Colors.GREEN}✓ Semua dependencies dasar terinstall dengan baik{Colors.RESET}")
        SoundPlayer.play_complex_sound("success")

def run_hackforge():
    """Jalankan HackForge langsung"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}MENJALANKAN HACKFORGE...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    animate_bar_chart("Mempersiapkan HackForge", duration=2)
    
    check_and_fix_dependencies()
    
    # Cek berbagai kemungkinan file main
    possible_files = [
        "src/main.py",
        "main.py"
    ]
    
    main_file = None
    for file in possible_files:
        if os.path.exists(file):
            main_file = file
            print(f"{Colors.GREEN}✓ Ditemukan: {file}{Colors.RESET}")
            SoundPlayer.play_complex_sound("success")
            break
    
    if main_file:
        print(f"\n{Colors.GREEN}🚀 Menemukan {main_file}, menjalankan...{Colors.RESET}")
        
        # Animasi sebelum menjalankan
        animate_bar_chart("Starting HackForge", duration=2)
        
        print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}HACKFORGE BERJALAN{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
        
        time.sleep(1)
        
        # Play startup sound
        SoundPlayer.play_complex_sound("startup")
        
        # Jalankan file
        try:
            os.system(f"python {main_file}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error saat menjalankan: {e}{Colors.RESET}")
            SoundPlayer.play_complex_sound("error")
            print(f"{Colors.YELLOW}Coba jalankan manual: python {main_file}{Colors.RESET}")
        
    else:
        print(f"\n{Colors.RED}❌ File main HackForge tidak ditemukan!{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        print(f"{Colors.YELLOW}File yang dicari:{Colors.RESET}")
        for file in possible_files:
            print(f"  {Colors.WHITE}- {file}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Pastikan Anda berada di direktori yang benar.{Colors.RESET}")

def run_bash_script(script_path, script_name):
    """Jalankan file bash script"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}MENJALANKAN {script_name.upper()}...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    animate_bar_chart(f"Mempersiapkan {script_name}", duration=2)
    
    if not os.path.exists(script_path):
        print(f"\n{Colors.RED}❌ File {script_path} tidak ditemukan!{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        print(f"{Colors.YELLOW}Pastikan file {script_path} ada di direktori tersebut.{Colors.RESET}")
        return False
    
    # Cek apakah file executable
    if not os.access(script_path, os.X_OK):
        print(f"{Colors.YELLOW}⚠️  File tidak executable, menambahkan permission...{Colors.RESET}")
        success, output = run_command(f"chmod +x {script_path}", f"Menambah permission execute untuk {script_path}")
        if not success:
            print(f"{Colors.RED}❌ Gagal menambah permission execute{Colors.RESET}")
            return False
    
    print(f"\n{Colors.GREEN}🚀 Menemukan {script_path}, menjalankan...{Colors.RESET}")
    
    # Animasi sebelum menjalankan
    animate_bar_chart(f"Starting {script_name}", duration=2)
    
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{script_name.upper()} BERJALAN{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
    
    time.sleep(1)
    
    # Play startup sound
    SoundPlayer.play_complex_sound("startup")
    
    # Jalankan script bash
    try:
        print(f"{Colors.BLUE}[→] Menjalankan: bash {script_path}{Colors.RESET}")
        result = subprocess.run(f"bash {script_path}", shell=True, check=False)
        
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✅ {script_name} selesai dengan sukses!{Colors.RESET}")
            SoundPlayer.play_complex_sound("success")
        else:
            print(f"\n{Colors.YELLOW}⚠️  {script_name} selesai dengan kode exit: {result.returncode}{Colors.RESET}")
            SoundPlayer.play_complex_sound("warning")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error saat menjalankan {script_name}: {e}{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        print(f"{Colors.YELLOW}Coba jalankan manual: bash {script_path}{Colors.RESET}")
        return False

def show_summary(installed, total):
    """Tampilkan ringkasan instalasi dengan animasi"""
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}INSTALASI SELESAI!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    
    # Animasi progress summary
    progress = installed / total if total > 0 else 1
    animate_bar_chart("Progress Instalasi Keseluruhan", duration=2)
    
    print(f"\n{Colors.BOLD}Ringkasan:{Colors.RESET}")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Python packages: {installed}/{total} berhasil")
    
    if installed == total:
        print(f"\n{Colors.GREEN}🎉 Semua dependencies berhasil diinstall!{Colors.RESET}")
        # Celebration animation dengan sound
        SoundPlayer.play_complex_sound("complete")
        for _ in range(3):
            for char in ["🎉", "🎊", "✨"]:
                print(f"\r{char} {Colors.GREEN}SUKSES!{Colors.RESET}", end="", flush=True)
                time.sleep(0.3)
        print()
    else:
        print(f"\n{Colors.YELLOW}⚠️  Beberapa packages gagal diinstall.{Colors.RESET}")
        SoundPlayer.play_complex_sound("warning")
        print(f"{Colors.YELLOW}   Anda masih bisa menjalankan tool, tetapi beberapa fitur mungkin tidak bekerja.{Colors.RESET}")

def check_sound_installation():
    """Cek dan install sound dependencies jika diperlukan"""
    print(f"\n{Colors.BLUE}[SOUND] Memeriksa fitur sound...{Colors.RESET}")
    
    if SoundPlayer.check_sound_dependencies():
        print(f"{Colors.GREEN}✓ Fitur sound tersedia{Colors.RESET}")
        SoundPlayer.play_complex_sound("success")  # Test sound
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Fitur sound tidak tersedia{Colors.RESET}")
        print(f"{Colors.WHITE}   Untuk mengaktifkan sound, install termux-api:{Colors.RESET}")
        print(f"{Colors.WHITE}   pkg install termux-api{Colors.RESET}")
        
        install_sound = input(f"\n{Colors.YELLOW}Install termux-api sekarang? (y/N): {Colors.RESET}").strip().lower()
        if install_sound in ['y', 'yes']:
            if install_termux_api():
                return True
        
        print(f"{Colors.YELLOW}⚠️  Menggunakan fallback sound (beep & vibrate){Colors.RESET}")
        # Test fallback sound
        SoundPlayer.play_fallback_sound("success")
        return False

def main():
    try:
        show_ascii_art()
        
        # Cek fitur sound
        sound_available = check_sound_installation()
        
        while True:
            choice = show_menu()
            animate_selection(choice)
            
            if choice == 1:
                installed, total = install_manual()
                show_summary(installed, total)
                
                run_now = input(f"\n{Colors.YELLOW}Jalankan HackForge sekarang? (Y/n): {Colors.RESET}").strip().lower()
                if run_now in ['y', 'yes', '']:
                    run_hackforge()
                break
                
            elif choice == 2:
                installed, total = install_from_requirements()
                show_summary(installed, total)
                
                run_now = input(f"\n{Colors.YELLOW}Jalankan HackForge sekarang? (Y/n): {Colors.RESET}").strip().lower()
                if run_now in ['y', 'yes', '']:
                    run_hackforge()
                break
                
            elif choice == 3:
                run_hackforge()
                break
                
            elif choice == 4:
                # Jalankan web/main.sh
                run_bash_script("main.sh", "Web Script")
                break
                
            elif choice == 5:
                # Jalankan main/main.sh
                run_bash_script("main/main.sh", "Main Script")
                break
                
            elif choice == 6:
                print(f"\n{Colors.YELLOW}👋 Terima kasih! Keluar dari installer.{Colors.RESET}")
                # Exit animation dengan sound
                SoundPlayer.play_complex_sound("success")
                for char in ["👋", "😊", "👍"]:
                    print(f"\r{char} Sampai jumpa...", end="", flush=True)
                    time.sleep(0.5)
                print()
                sys.exit(0)
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}❌ Instalasi dibatalkan oleh user{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
        SoundPlayer.play_complex_sound("error")
        sys.exit(1)

if __name__ == "__main__":
    main()