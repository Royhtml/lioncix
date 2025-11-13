#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import threading
import socket
import platform
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class AnimasiLoading:
    def __init__(self):
        self.animasi = [
            "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"
        ]
        self.running = False
        self.thread = None
    
    def _animate(self, pesan="Loading"):
        i = 0
        while self.running:
            print(f"\r{Colors.CYAN}{self.animasi[i % len(self.animasi)]} {pesan}...{Colors.END}", end="", flush=True)
            time.sleep(0.1)
            i += 1
    
    def start(self, pesan="Loading"):
        self.running = True
        self.thread = threading.Thread(target=self._animate, args=(pesan,))
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * 50 + "\r", end="", flush=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Mendapatkan ukuran terminal"""
    try:
        if os.name == 'nt':  # Windows
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            cols = csbi.raw[10] - csbi.raw[8] + 1
            rows = csbi.raw[12] - csbi.raw[6] + 1
            return cols, rows
        else:  # Unix/Linux
            cols, rows = os.get_terminal_size()
            return cols, rows
    except:
        return 80, 24  # Default size

def tampilkan_ascii_art():
    """Menampilkan ASCII art yang menyesuaikan ukuran terminal"""
    cols, rows = get_terminal_size()
    
    # ASCII art yang responsif
    if cols >= 80:
        ascii_art = f"""
{Colors.CYAN}
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║  ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗                ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝                ║
║     ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝                 ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗                 ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗                ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝                ║
║                                                                        ║
║                 MULTI-TOOL TERMUX & WINDOWS                           ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    elif cols >= 60:
        ascii_art = f"""
{Colors.CYAN}
╔══════════════════════════════════════════╗
║                                          ║
║  ████████╗███████╗██████╗ ███╗   ███╗   ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║   ║
║     ██║   █████╗  ██████╔╝██╔████╔██║   ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║   ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║   ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝   ║
║                                          ║
║           MULTI-TOOL TERMUX              ║
║                                          ║
╚══════════════════════════════════════════╝
{Colors.END}
"""
    else:
        ascii_art = f"""
{Colors.CYAN}
╔══════════════════╗
║                  ║
║   TERMUX TOOL    ║
║   MULTI-FUNCTION ║
║                  ║
╚══════════════════╝
{Colors.END}
"""
    print(ascii_art)

def cek_koneksi_internet():
    """Cek koneksi internet"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def install_packages():
    """Install package Python yang diperlukan"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                   INSTALL PACKAGES                         ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    packages = [
        "requests", "colorama", "flask", "django", "numpy", "pandas"
    ]
    
    print(f"{Colors.CYAN}Package yang akan diinstall:{Colors.END}")
    for i, package in enumerate(packages, 1):
        print(f"  {Colors.YELLOW}[{i}]{Colors.END} {package}")
    
    print(f"  {Colors.YELLOW}[A]{Colors.END} Install semua package")
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    pilihan = input(f"{Colors.GREEN}Pilih package (nomor/A/0): {Colors.END}").strip().upper()
    
    if pilihan == "0":
        return
    elif pilihan == "A":
        packages_to_install = packages
    else:
        try:
            index = int(pilihan) - 1
            if 0 <= index < len(packages):
                packages_to_install = [packages[index]]
            else:
                print(f"{Colors.RED}Pilihan tidak valid!{Colors.END}")
                time.sleep(1)
                return
        except ValueError:
            print(f"{Colors.RED}Input tidak valid!{Colors.END}")
            time.sleep(1)
            return
    
    loading = AnimasiLoading()
    
    for package in packages_to_install:
        loading.start(f"Installing {package}")
        try:
            # Gunakan pip yang sesuai
            pip_cmd = "pip" if os.name == 'nt' else "pip3"
            
            result = subprocess.run(
                [pip_cmd, "install", package], 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            loading.stop()
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✓ {package} berhasil diinstall{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Gagal install {package}: {result.stderr}{Colors.END}")
                
        except subprocess.TimeoutExpired:
            loading.stop()
            print(f"{Colors.RED}✗ Timeout saat install {package}{Colors.END}")
        except Exception as e:
            loading.stop()
            print(f"{Colors.RED}✗ Error install {package}: {str(e)}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def update_pip():
    """Update pip ke versi terbaru"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                     UPDATE PIP                            ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    print(f"{Colors.YELLOW}Memperbarui pip...{Colors.END}")
    
    loading = AnimasiLoading()
    loading.start("Updating pip")
    
    try:
        pip_cmd = "pip" if os.name == 'nt' else "pip3"
        python_cmd = "python" if os.name == 'nt' else "python3"
        
        # Update pip
        result = subprocess.run(
            [python_cmd, "-m", "pip", "install", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        loading.stop()
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Pip berhasil diupdate{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Gagal update pip: {result.stderr}{Colors.END}")
            
    except subprocess.TimeoutExpired:
        loading.stop()
        print(f"{Colors.RED}✗ Timeout saat update pip{Colors.END}")
    except Exception as e:
        loading.stop()
        print(f"{Colors.RED}✗ Error update pip: {str(e)}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def jalankan_python_script():
    """Menjalankan script Python"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                   JALANKAN SCRIPT PYTHON                    ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    # Cari semua file tes.py di direktori dan subfolder
    files_python = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f == 'tes.py':
                files_python.append(os.path.join(root, f))
    
    if not files_python:
        print(f"{Colors.RED}Tidak ada file 'tes.py' ditemukan di direktori ini.{Colors.END}")
        input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")
        return
    
    print(f"{Colors.CYAN}Pilih script Python yang ingin dijalankan:{Colors.END}")
    for i, file in enumerate(files_python, 1):
        print(f"  {Colors.YELLOW}[{i}]{Colors.END} {file}")
    
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    try:
        pilihan = int(input(f"{Colors.GREEN}Pilih nomor: {Colors.END}"))
        
        if pilihan == 0:
            return
        
        if 1 <= pilihan <= len(files_python):
            file_terpilih = files_python[pilihan-1]
            
            loading = AnimasiLoading()
            loading.start(f"Menjalankan {file_terpilih}")
            
            try:
                time.sleep(2)
                loading.stop()
                
                print(f"\n{Colors.GREEN}Menjalankan: {file_terpilih}{Colors.END}")
                print(f"{Colors.CYAN}" + "="*50 + f"{Colors.END}")
                
                # Jalankan script Python dengan command yang sesuai
                python_cmd = "python" if os.name == 'nt' else "python3"
                os.system(f'{python_cmd} "{file_terpilih}"')
                
            except Exception as e:
                loading.stop()
                print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")
        else:
            print(f"{Colors.RED}Pilihan tidak valid!{Colors.END}")
            time.sleep(1)
    
    except ValueError:
        print(f"{Colors.RED}Input harus berupa angka!{Colors.END}")
        time.sleep(1)


def jalankan_server_web():
    """Menjalankan server web localhost menggunakan Python"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                   JALANKAN SERVER WEB                       ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    # Cek apakah direktori web dan file index.html ada
    web_dir = "web"
    index_file = os.path.join(web_dir, "index.html")
    
    if not os.path.exists(web_dir):
        print(f"{Colors.YELLOW}Membuat direktori 'web'...{Colors.END}")
        os.makedirs(web_dir)
    
    if not os.path.exists(index_file):
        print(f"{Colors.YELLOW}Membuat file index.html...{Colors.END}")
        buat_file_index_html()
    
    print(f"{Colors.CYAN}Pilih port untuk server web:{Colors.END}")
    print(f"  {Colors.YELLOW}[1]{Colors.END} Port 8080 (Default)")
    print(f"  {Colors.YELLOW}[2]{Colors.END} Port 8000")
    print(f"  {Colors.YELLOW}[3]{Colors.END} Custom port")
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    try:
        pilihan_port = int(input(f"{Colors.GREEN}Pilih nomor: {Colors.END}"))
        
        if pilihan_port == 0:
            return
        
        port = 8080  # Default
        
        if pilihan_port == 1:
            port = 8080
        elif pilihan_port == 2:
            port = 8000
        elif pilihan_port == 3:
            try:
                port = int(input(f"{Colors.CYAN}Masukkan port: {Colors.END}"))
                if port < 1 or port > 65535:
                    raise ValueError
            except ValueError:
                print(f"{Colors.RED}Port tidak valid! Menggunakan port 8080{Colors.END}")
                port = 8080
        else:
            print(f"{Colors.RED}Pilihan tidak valid! Menggunakan port 8080{Colors.END}")
        
        loading = AnimasiLoading()
        loading.start(f"Menjalankan server web di port {port}")
        
        try:
            time.sleep(2)
            loading.stop()
            
            print(f"\n{Colors.GREEN}Server web berhasil dijalankan!{Colors.END}")
            print(f"{Colors.CYAN}URL: http://localhost:{port}{Colors.END}")
            print(f"{Colors.CYAN}Direktori: {os.path.abspath(web_dir)}{Colors.END}")
            print(f"\n{Colors.YELLOW}Tekan Ctrl+C untuk menghentikan server{Colors.END}")
            print(f"{Colors.CYAN}" + "="*50 + f"{Colors.END}")
            
            # Simpan direktori saat ini
            current_dir = os.getcwd()
            
            # Pastikan kita di direktori yang benar
            if os.path.exists(web_dir):
                os.chdir(web_dir)
            
            try:
                # Jalankan server web menggunakan Python
                python_cmd = "python" if os.name == 'nt' else "python3"
                
                if os.name == 'nt':  # Windows
                    os.system(f'{python_cmd} -m http.server {port}')
                else:  # Unix/Linux
                    os.system(f'{python_cmd} -m http.server {port}')
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Server dihentikan.{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.RED}Error menjalankan server: {str(e)}{Colors.END}")
            finally:
                # Kembali ke direktori semula
                os.chdir(current_dir)
            
        except Exception as e:
            loading.stop()
            print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
    
    except ValueError:
        print(f"{Colors.RED}Input harus berupa angka!{Colors.END}")
        time.sleep(1)

def buat_file_index_html():
    """Membuat file index.html default"""
    content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HackForge - Infinite Cybersecurity Challenge</title>
    <link rel = "stylesheet" href = "css/index.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">HACKFORGE ∞</div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="level-display">1</div>
                    <div class="stat-label">LEVEL</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="score-display">0</div>
                    <div class="stat-label">SCORE</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="lives-display">3</div>
                    <div class="stat-label">NYAWA</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="streak-display">0</div>
                    <div class="stat-label">STREAK</div>
                </div>
                <div class="timer" id="timer">02:00:00</div>
            </div>
        </header>
        
        <div class="game-area">
            <div class="main-content">
                <div class="level-container">
                    <div class="level-header">
                        <h2 class="level-title" id="level-title">Level 1: Password Cracking Dasar</h2>
                        <div class="difficulty-badge difficulty-easy" id="difficulty-badge">MUDAH</div>
                    </div>
                    <p class="level-description" id="level-description">
                        Sebuah perusahaan kecil menjadi korban serangan siber. Anda harus memecahkan password administrator untuk mengamankan sistem.
                    </p>
                    
                    <div class="difficulty-meter">
                        <div class="difficulty-fill" id="difficulty-fill"></div>
                    </div>
                    
                    <div class="complexity-indicators" id="complexity-indicators">
                        <!-- Complexity dots will be generated here -->
                    </div>
                    
                    <div class="challenge-area" id="challenge-area">
                        <div class="terminal-line">
                            <span class="terminal-prompt">hackforge@root:~$ </span>
                            <span class="terminal-command">scan_target --ip 192.168.1.45</span>
                        </div>
                        <div class="terminal-line terminal-output">
                            [+] Target teridentifikasi: Server Perusahaan XYZ
                        </div>
                        <div class="terminal-line terminal-output">
                            [+] Port terbuka: 22, 80, 443
                        </div>
                        <div class="terminal-line terminal-output">
                            [+] Vulnerability detected: Weak password hashing
                        </div>
                        <div class="terminal-line">
                            <span class="terminal-prompt">hackforge@root:~$ </span>
                            <span class="terminal-command">hash_crack --type md5 --hash 5f4dcc3b5aa765d61d8327deb882cf99</span>
                        </div>
                        <div class="terminal-line terminal-output">
                            [+] Memulai proses cracking...
                        </div>
                        <div class="terminal-line terminal-output">
                            [+] Dictionary attack in progress...
                        </div>
                    </div>
                    
                    <div class="input-area">
                        <input type="text" class="input-field" id="answer-input" placeholder="Masukkan jawaban...">
                        <button class="btn" id="submit-btn">Submit</button>
                        <button class="btn btn-warning" id="hint-btn">Hint</button>
                        <button class="btn btn-danger" id="skip-btn">Skip</button>
                        <button class="btn btn-info" id="solve-btn">Solve</button>
                    </div>
                    
                    <div class="time-bonus" id="time-bonus">
                        Time Bonus: +0 points
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="hint-container">
                    <h3 class="sidebar-title">PETUNJUK</h3>
                    <div class="hint-text" id="hint-text">
                        Hash MD5 ini adalah hash untuk password yang sangat umum digunakan. Coba pikirkan password paling populer yang terdiri dari 8 karakter.
                    </div>
                </div>
                
                <div class="lives-container">
                    <h3 class="sidebar-title">NYAWA</h3>
                    <div class="life" id="life-1"></div>
                    <div class="life" id="life-2"></div>
                    <div class="life" id="life-3"></div>
                </div>
                
                <div class="progress-section">
                    <h3 class="sidebar-title">MILESTONE</h3>
                    <div class="milestone" id="milestone-5">Level 5: Script Kiddie</div>
                    <div class="milestone" id="milestone-10">Level 10: Junior Hacker</div>
                    <div class="milestone" id="milestone-25">Level 25: Security Analyst</div>
                    <div class="milestone" id="milestone-50">Level 50: Pentester</div>
                    <div class="milestone" id="milestone-100">Level 100: Elite Hacker</div>
                    <div class="milestone" id="milestone-150">Level 150: Cyber Warrior</div>
                    <div class="milestone" id="milestone-200">Level 200: Digital Legend</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Achievement Notification -->
    <div class="achievement" id="achievement-notification">
        <div class="achievement-title" id="achievement-title">Pencapaian Terbuka!</div>
        <div id="achievement-description">Anda telah mencapai level 5!</div>
    </div>
    
    <!-- Modal for level completion -->
    <div class="modal" id="success-modal">
        <div class="modal-content">
            <h2 class="modal-title" id="success-title">LEVEL BERHASIL!</h2>
            <p class="modal-message" id="success-message">Selamat! Anda berhasil memecahkan tantangan.</p>
            <div class="modal-message">
                <strong>Skor: +<span id="score-earned">0</span></strong>
                <br>Streak: <span id="streak-count">0</span>
                <br>Time Bonus: +<span id="time-bonus-earned">0</span>
            </div>
            <button class="btn" id="next-level-btn">Level Berikutnya</button>
        </div>
    </div>
    
    <!-- Modal for game over -->
    <div class="modal" id="game-over-modal">
        <div class="modal-content">
            <h2 class="modal-title">GAME OVER</h2>
            <p class="modal-message" id="game-over-message">Nyawa Anda telah habis. Mulai dari awal?</p>
            <p class="modal-message">Level Tertinggi: <span id="highest-level">1</span></p>
            <p class="modal-message">Total Skor: <span id="final-score">0</span></p>
            <button class="btn" id="restart-btn">Mulai Ulang</button>
        </div>
    </div>
    
    <!-- Modal for time up -->
    <div class="modal" id="time-up-modal">
        <div class="modal-content">
            <h2 class="modal-title">WAKTU HABIS!</h2>
            <p class="modal-message">Waktu 2 jam telah habis. Pertahankan progres Anda?</p>
            <p class="modal-message">Level Tertinggi: <span id="time-up-level">1</span></p>
            <p class="modal-message">Total Skor: <span id="time-up-score">0</span></p>
            <button class="btn" id="continue-btn">Lanjutkan Tanpa Timer</button>
            <button class="btn btn-danger" id="new-game-btn">Game Baru</button>
        </div>
    </div>
    
    <script src="js/index.js"></script>

</body>
</html>"""
    
    with open(os.path.join("web", "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

def informasi_sistem():
    """Menampilkan informasi sistem"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                     INFORMASI SISTEM                        ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    # Informasi sistem yang lebih lengkap
    system_info = [
        ("Sistem Operasi", platform.system()),
        ("Versi OS", platform.release()),
        ("Arsitektur", platform.architecture()[0]),
        ("Processor", platform.processor() or "Tidak diketahui"),
        ("Python Version", platform.python_version()),
        ("Direktori Saat Ini", os.getcwd()),
        ("Koneksi Internet", "✅ Terhubung" if cek_koneksi_internet() else "❌ Terputus"),
        ("Platform", sys.platform),
        ("Terminal Size", f"{get_terminal_size()[0]}x{get_terminal_size()[1]}"),
    ]
    
    for label, value in system_info:
        print(f"{Colors.CYAN}{label:<20}:{Colors.END} {Colors.YELLOW}{value}{Colors.END}")
    
    print()
    input(f"{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def main():
    # Cek Python version
    if sys.version_info < (3, 6):
        print(f"{Colors.RED}Python 3.6 atau lebih tinggi diperlukan!{Colors.END}")
        sys.exit(1)
    
    while True:
        clear_screen()
        tampilkan_ascii_art()
        
        # Header dengan informasi
        cols, rows = get_terminal_size()
        header_width = min(cols - 4, 76)
        
        print(f"{Colors.GREEN}╔{'═' * header_width}╗{Colors.END}")
        print(f"{Colors.GREEN}║{'MENU UTAMA - TERMUX & WINDOWS TOOL'.center(header_width)}║{Colors.END}")
        print(f"{Colors.GREEN}╚{'═' * header_width}╝{Colors.END}")
        print()
        
        # Menu options yang diperbarui
        menu_options = [
            ("1", "Jalankan Script Python", "🐍"),
            ("2", "Jalankan Server Web", "🌐"),
            ("3", "Install Packages", "📦"),
            ("4", "Update Pip", "🔄"),
            ("5", "Informasi Sistem", "💻"),
            ("0", "Keluar", "🚪")
        ]
        
        for option, description, icon in menu_options:
            print(f"  {Colors.YELLOW}[{option}]{Colors.END} {icon} {description}")
        
        print()
        print(f"{Colors.CYAN}{'═' * header_width}{Colors.END}")
        
        # Informasi platform
        platform_info = "Windows" if os.name == 'nt' else "Termux/Linux"
        print(f"{Colors.MAGENTA}Platform: {platform_info} | Terminal: {cols}x{rows}{Colors.END}")
        print()
        
        try:
            pilihan = input(f"{Colors.GREEN}Pilih menu [{Colors.YELLOW}0-5{Colors.GREEN}]: {Colors.END}").strip()
            
            if pilihan == "1":
                jalankan_python_script()
            elif pilihan == "2":
                jalankan_server_web()
            elif pilihan == "3":
                install_packages()
            elif pilihan == "4":
                update_pip()
            elif pilihan == "5":
                informasi_sistem()
            elif pilihan == "0":
                print(f"\n{Colors.GREEN}Terima kasih telah menggunakan Termux Multi-Tool! 👋{Colors.END}")
                print(f"{Colors.CYAN}Sampai jumpa! 😊{Colors.END}")
                time.sleep(1)
                break
            else:
                print(f"{Colors.RED}Pilihan tidak valid! Silakan pilih 0-5.{Colors.END}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Program dihentikan oleh pengguna.{Colors.END}")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        sys.exit(1)