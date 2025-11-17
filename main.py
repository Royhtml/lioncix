#!/usr/bin/env python3
# Installer untuk dependencies Alat Bantu

import subprocess
import sys
import os
import time
import threading
import random
import platform

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
    """Class untuk memutar sound di Termux tanpa API"""
    
    @staticmethod
    def check_audio_dependencies():
        """Cek dependencies audio yang tersedia"""
        available_methods = []
        
        # Cek sox (Sound eXchange) - paling reliable di Termux
        try:
            result = subprocess.run(["which", "play"], capture_output=True, text=True)
            if result.returncode == 0:
                available_methods.append("sox")
        except:
            pass
            
        # Cek termux-tts-speak (Text-to-Speech)
        try:
            result = subprocess.run(["which", "termux-tts-speak"], capture_output=True, text=True)
            if result.returncode == 0:
                available_methods.append("tts")
        except:
            pass
            
        # Cek beep dan vibrate
        try:
            result = subprocess.run(["which", "termux-beep"], capture_output=True, text=True)
            if result.returncode == 0:
                available_methods.append("beep")
        except:
            pass
            
        try:
            result = subprocess.run(["which", "termux-vibrate"], capture_output=True, text=True)
            if result.returncode == 0:
                available_methods.append("vibrate")
        except:
            pass
            
        return available_methods
    
    @staticmethod
    def generate_beep_sound(frequency=1000, duration=0.5):
        """Generate beep sound menggunakan Python"""
        try:
            # Coba menggunakan os.system beep jika tersedia
            if platform.system() != "Windows":
                os.system(f"beep -f {frequency} -l {duration*1000} 2>/dev/null")
                return True
        except:
            pass
        return False
    
    @staticmethod
    def play_sox_sound(sound_type="success"):
        """Memutar sound menggunakan sox/play"""
        sound_configs = {
            "success": {"freq1": 1000, "freq2": 1500, "duration": 0.3},
            "error": {"freq1": 500, "freq2": 400, "duration": 0.5},
            "warning": {"freq1": 800, "freq2": 600, "duration": 0.2},
            "complete": {"freq1": 800, "freq2": 1200, "freq3": 1500, "duration": 0.8},
            "startup": {"freq1": 200, "freq2": 800, "freq3": 1200, "duration": 1.0}
        }
        
        config = sound_configs.get(sound_type, sound_configs["success"])
        
        try:
            if sound_type == "success":
                # Single beep
                subprocess.Popen([
                    "play", "-q", "-n", "synth", str(config["duration"]), 
                    "sine", str(config["freq1"]), "gain", "-5"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            elif sound_type == "error":
                # Low beep
                subprocess.Popen([
                    "play", "-q", "-n", "synth", str(config["duration"]), 
                    "sine", str(config["freq1"]), "gain", "-3"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            elif sound_type == "warning":
                # Short beep
                subprocess.Popen([
                    "play", "-q", "-n", "synth", str(config["duration"]), 
                    "sine", str(config["freq1"]), "gain", "-7"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            elif sound_type == "complete":
                # Rising tone
                subprocess.Popen([
                    "play", "-q", "-n", "synth", str(config["duration"]), 
                    "sine", "mix", f"{config['freq1']}-{config['freq3']}", "gain", "-5"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            elif sound_type == "startup":
                # Startup sequence
                subprocess.Popen([
                    "play", "-q", "-n", "synth", "0.3", "sine", str(config["freq1"]),
                    "synth", "0.3", "sine", str(config["freq2"]), 
                    "synth", "0.4", "sine", str(config["freq3"]), "gain", "-8"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            return True
        except:
            return False
    
    @staticmethod
    def play_tts_sound(sound_type="success"):
        """Memutar sound menggunakan text-to-speech"""
        tts_messages = {
            "success": "Success",
            "error": "Error", 
            "warning": "Warning",
            "complete": "Task complete",
            "startup": "Hack Forge starting"
        }
        
        try:
            message = tts_messages.get(sound_type, "Done")
            subprocess.Popen([
                "termux-tts-speak", "-r", "1.2", message
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False
    
    @staticmethod
    def play_beep_vibrate(sound_type="success"):
        """Memutar beep dan vibration"""
        configs = {
            "success": {"beep_freq": 1000, "beep_duration": 200, "vibrate_duration": 100},
            "error": {"beep_freq": 400, "beep_duration": 500, "vibrate_duration": 300},
            "warning": {"beep_freq": 800, "beep_duration": 300, "vibrate_duration": 200},
            "complete": {"beep_freq": 1200, "beep_duration": 400, "vibrate_duration": 400},
            "startup": {"beep_freq": 1500, "beep_duration": 100, "vibrate_duration": 50}
        }
        
        config = configs.get(sound_type, configs["success"])
        
        try:
            # Vibrate
            subprocess.Popen([
                "termux-vibrate", "-d", str(config["vibrate_duration"])
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
            
        try:
            # Beep
            subprocess.Popen([
                "termux-beep", "-f", str(config["beep_freq"]), "-d", str(config["beep_duration"])
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
            
        return True
    
    @staticmethod
    def play_sound(sound_type="success"):
        """Main method untuk memutar sound dengan fallback"""
        available_methods = SoundPlayer.check_audio_dependencies()
        
        if not available_methods:
            # Fallback ke Python beep
            return SoundPlayer.generate_beep_sound()
        
        # Priority: sox > tts > beep+vibrate
        if "sox" in available_methods:
            if SoundPlayer.play_sox_sound(sound_type):
                return True
                
        if "tts" in available_methods:
            if SoundPlayer.play_tts_sound(sound_type):
                return True
                
        if "beep" in available_methods or "vibrate" in available_methods:
            if SoundPlayer.play_beep_vibrate(sound_type):
                return True
                
        # Ultimate fallback
        return SoundPlayer.generate_beep_sound()

def show_ascii_art():
    """Menampilkan ASCII art"""
    ascii_art = f"""
{Colors.CYAN}
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
║                                                  ║
║              █░░ █ █▀█ █▄░█ █▀▀ █ ▀▄▀            ║
║              █▄▄ █ █▄█ █░▀█ █▄▄ █ █░█            ║
║                                                  ║
║        █░█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█ █▀█ █▀▀ █▀▀       ║
║        █▀█ █▀█ █▄▄ █░█ █▀░ █▄█ █▀▄ █▄█ ██▄       ║
║                                                  ║
║            PROFESSIONAL Hacker V2.8.7            ║
║            Created by Dwi Bakti N Dev            ║
║                                                  ║                        
║[•] Installing required packages...               ║
║[•] Setting up environment...                     ║
║[•] Preparing tools...                            ║
╚══════════════════════════════════════════════════╝
{Colors.RESET}
    """
    print(ascii_art)
    
    # Play startup sound dengan delay
    time.sleep(0.5)
    SoundPlayer.play_sound("startup")

def animate_selection(choice):
    """Animasi ketika memilih menu"""
    choices = {
        1: "Manual Installation",
        2: "Requirements Installation", 
        3: "Running HackForge",
        4: "Run Web Script (PHP Admin)",
        5: "Run Exploitation Hacking (Games)",
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
    SoundPlayer.play_sound("success")
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
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
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
        SoundPlayer.play_sound("success")
        
        if result.stdout:
            print(f"{Colors.GREEN}   Output: {result.stdout.strip()}{Colors.RESET}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        loading_thread.join(timeout=0.1)
        print(f"\r{Colors.RED}✗{Colors.RESET} {description} - Gagal!")
        
        # Play error sound
        SoundPlayer.play_sound("error")
        
        print(f"{Colors.RED}   Error: {e.stderr.strip()}{Colors.RESET}")
        return False, e.stderr
    except subprocess.TimeoutExpired:
        loading_thread.join(timeout=0.1)
        print(f"\r{Colors.RED}✗{Colors.RESET} {description} - Timeout!")
        
        # Play error sound
        SoundPlayer.play_sound("error")
        
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
    available_methods = SoundPlayer.check_audio_dependencies()
    if available_methods:
        sound_status = f"{Colors.GREEN}🔊 Sound: {', '.join(available_methods).upper()}{Colors.RESET}"
    else:
        sound_status = f"{Colors.RED}🔇 Sound: FALLBACK ONLY{Colors.RESET}"
    print(f"          {sound_status}")
    
    # Animasi menu items
    menu_items = [
        f"  {Colors.GREEN}1{Colors.RESET} - Install dependencies manual (package Termux)",
        f"  {Colors.GREEN}2{Colors.RESET} - Install py requirements.txt", 
        f"  {Colors.GREEN}3{Colors.RESET} - Running Now HackForge (skip instalasi)",
        f"  {Colors.GREEN}4{Colors.RESET} - Run Web Script (PHP Admin)",
        f"  {Colors.GREEN}5{Colors.RESET} - Run Exploitation Hacking (Games)",
        f"  {Colors.GREEN}6{Colors.RESET} - Run Token Generator (JWT)",
        f"  {Colors.GREEN}7{Colors.RESET} - Keluar"
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
                SoundPlayer.play_sound("error")
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Operasi dibatalkan.{Colors.RESET}")
            SoundPlayer.play_sound("error")
            sys.exit(1)

def install_audio_dependencies():
    """Install dependencies audio untuk Termux"""
    print(f"\n{Colors.BLUE}[SOUND] Menginstall audio dependencies...{Colors.RESET}")
    
    commands = [
        "pkg update -y",
        "pkg install sox -y",  # Sound eXchange - untuk generate sound
        "pkg install termux-api -y",  # Untuk beep dan vibrate
    ]
    
    success_count = 0
    for cmd in commands:
        success, output = run_command(cmd, f"Executing: {cmd.split()[0]}")
        if success:
            success_count += 1
    
    # Verifikasi instalasi
    available_methods = SoundPlayer.check_audio_dependencies()
    if available_methods:
        print(f"{Colors.GREEN}✓ Audio dependencies berhasil diinstall: {', '.join(available_methods)}{Colors.RESET}")
        SoundPlayer.play_sound("success")
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Audio dependencies terinstall tetapi mungkin memerlukan konfigurasi tambahan{Colors.RESET}")
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
                SoundPlayer.play_sound("success")
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
        SoundPlayer.play_sound("error")
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
        SoundPlayer.play_sound("success")
    
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
        SoundPlayer.play_sound("warning")
        
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
        SoundPlayer.play_sound("success")

def run_python_script(script_path, script_name):
    """Jalankan file Python script"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}MENJALANKAN {script_name.upper()}...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    animate_bar_chart(f"Mempersiapkan {script_name}", duration=2)
    
    if not os.path.exists(script_path):
        print(f"\n{Colors.RED}❌ File {script_path} tidak ditemukan!{Colors.RESET}")
        SoundPlayer.play_sound("error")
        
        # Coba cari file alternatif
        possible_files = [
            script_path.replace('.py', '.sh'),
            script_path.replace('.py', ''),
            os.path.basename(script_path),
            f"src/{script_path}",
            f"main/{script_path}"
        ]
        
        found_alternative = None
        for alt_file in possible_files:
            if os.path.exists(alt_file):
                found_alternative = alt_file
                break
        
        if found_alternative:
            print(f"{Colors.YELLOW}⚠️  Ditemukan file alternatif: {found_alternative}{Colors.RESET}")
            use_alternative = input(f"{Colors.YELLOW}Gunakan file ini? (y/N): {Colors.RESET}").strip().lower()
            if use_alternative in ['y', 'yes']:
                script_path = found_alternative
            else:
                return False
        else:
            print(f"{Colors.YELLOW}Pastikan file {script_path} ada di direktori tersebut.{Colors.RESET}")
            return False
    
    print(f"\n{Colors.GREEN}🚀 Menemukan {script_path}, menjalankan...{Colors.RESET}")
    
    # Animasi sebelum menjalankan
    animate_bar_chart(f"Starting {script_name}", duration=2)
    
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{script_name.upper()} BERJALAN{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
    
    time.sleep(1)
    
    # Play startup sound
    SoundPlayer.play_sound("startup")
    
    # Jalankan script Python
    try:
        print(f"{Colors.BLUE}[→] Menjalankan: python {script_path}{Colors.RESET}")
        
        # Gunakan os.system untuk interaktif execution
        result = os.system(f"python {script_path}")
        
        if result == 0:
            print(f"\n{Colors.GREEN}✅ {script_name} selesai dengan sukses!{Colors.RESET}")
            SoundPlayer.play_sound("success")
        else:
            print(f"\n{Colors.YELLOW}⚠️  {script_name} selesai dengan kode exit: {result}{Colors.RESET}")
            SoundPlayer.play_sound("warning")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error saat menjalankan {script_name}: {e}{Colors.RESET}")
        SoundPlayer.play_sound("error")
        print(f"{Colors.YELLOW}Coba jalankan manual: python {script_path}{Colors.RESET}")
        return False

def run_hackforge():
    """Jalankan HackForge langsung"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}MENJALANKAN HACKFORGE...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    animate_bar_chart("Mempersiapkan HackForge", duration=2)
    
    check_and_fix_dependencies()
    
    # Cek berbagai kemungkinan file main
    possible_files = [
        "hackforge/src/main.py",
        "hackforge/mainpy.py",
        "hackforge.py",
        "HackForge.py",
        "tool.py"
    ]
    
    main_file = None
    for file in possible_files:
        if os.path.exists(file):
            main_file = file
            print(f"{Colors.GREEN}✓ Ditemukan: {file}{Colors.RESET}")
            SoundPlayer.play_sound("success")
            break
    
    if main_file:
        return run_python_script(main_file, "HackForge")
    else:
        print(f"\n{Colors.RED}❌ File main HackForge tidak ditemukan!{Colors.RESET}")
        SoundPlayer.play_sound("error")
        print(f"{Colors.YELLOW}File yang dicari:{Colors.RESET}")
        for file in possible_files:
            print(f"  {Colors.WHITE}- {file}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Pastikan Anda berada di direktori yang benar.{Colors.RESET}")
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
        SoundPlayer.play_sound("complete")
        for _ in range(3):
            for char in ["🎉", "🎊", "✨"]:
                print(f"\r{char} {Colors.GREEN}SUKSES!{Colors.RESET}", end="", flush=True)
                time.sleep(0.3)
        print()
    else:
        print(f"\n{Colors.YELLOW}⚠️  Beberapa packages gagal diinstall.{Colors.RESET}")
        SoundPlayer.play_sound("warning")
        print(f"{Colors.YELLOW}   Anda masih bisa menjalankan tool, tetapi beberapa fitur mungkin tidak bekerja.{Colors.RESET}")

def check_sound_installation():
    """Cek dan install sound dependencies jika diperlukan"""
    print(f"\n{Colors.BLUE}[SOUND] Memeriksa fitur sound...{Colors.RESET}")
    
    available_methods = SoundPlayer.check_audio_dependencies()
    if available_methods:
        print(f"{Colors.GREEN}✓ Fitur sound tersedia: {', '.join(available_methods)}{Colors.RESET}")
        SoundPlayer.play_sound("success")  # Test sound
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Fitur sound tidak tersedia{Colors.RESET}")
        print(f"{Colors.WHITE}   Untuk mengaktifkan sound, install sox dan termux-api:{Colors.RESET}")
        print(f"{Colors.WHITE}   pkg install sox termux-api{Colors.RESET}")
        
        install_sound = input(f"\n{Colors.YELLOW}Install audio dependencies sekarang? (y/N): {Colors.RESET}").strip().lower()
        if install_sound in ['y', 'yes']:
            if install_audio_dependencies():
                return True
        
        print(f"{Colors.YELLOW}⚠️  Menggunakan fallback sound (Python beep){Colors.RESET}")
        # Test fallback sound
        SoundPlayer.play_sound("success")
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
                # Jalankan web/main.py
                run_python_script("lioncix/server.py", "Web Script")
                break
                
            elif choice == 5:
                # Jalankan main/main.py
                run_python_script("lioncix/main/main.py", "Main Script")
                break
            
            elif choice == 6:
                # Jalankan Token/main.py
                run_python_script("lioncix/Token/main.py", "Main Script")
                break
                
            elif choice == 7:
                print(f"\n{Colors.YELLOW}👋 Terima kasih! Keluar dari installer.{Colors.RESET}")
                # Exit animation dengan sound
                SoundPlayer.play_sound("success")
                for char in ["👋", "😊", "👍"]:
                    print(f"\r{char} Sampai jumpa...", end="", flush=True)
                    time.sleep(0.5)
                print()
                sys.exit(0)
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}❌ Instalasi dibatalkan oleh user{Colors.RESET}")
        SoundPlayer.play_sound("error")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
        SoundPlayer.play_sound("error")
        sys.exit(1)

if __name__ == "__main__":
    main()