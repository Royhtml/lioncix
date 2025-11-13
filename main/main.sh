#!/bin/bash

# Termux Multi-Tool - Shell Script Version
# Compatible with Termux and Linux

# Colors definition
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
MAGENTA='\033[95m'
BLUE='\033[94m'
WHITE='\033[97m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
END='\033[0m'

# Function to clear screen
clear_screen() {
    clear
}

# Function to check internet connection
check_internet() {
    if ping -c 1 8.8.8.8 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to display loading animation
show_loading() {
    local message="$1"
    local delay=0.1
    local spinstr='|/-\'
    
    printf "${CYAN}${message}...${END}"
    
    while :; do
        local temp=${spinstr#?}
        printf " [%c]" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
}

start_loading() {
    show_loading "$1" &
    LOADING_PID=$!
}

stop_loading() {
    kill $LOADING_PID 2>/dev/null
    printf "\b\b\b\b    \b\b\b\b\n"
}

# Function to get terminal size
get_terminal_size() {
    local cols=$(tput cols)
    local rows=$(tput lines)
    echo "$cols $rows"
}

# Function to display ASCII art
display_ascii_art() {
    clear_screen
    local size=($(get_terminal_size))
    local cols=${size[0]}
    
    if [ $cols -ge 80 ]; then
        cat << "EOF"

${CYAN}
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║  ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗                ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝                ║
║     ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝                 ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗                 ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗                ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝                ║
║                                                                        ║
║                 MULTI-TOOL TERMUX & LINUX                             ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
EOF
    elif [ $cols -ge 60 ]; then
        cat << "EOF"

${CYAN}
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
EOF
    else
        cat << "EOF"

${CYAN}
╔══════════════════╗
║                  ║
║   TERMUX TOOL    ║
║   MULTI-FUNCTION ║
║                  ║
╚══════════════════╝
EOF
    fi
}

# Function to install packages
install_packages() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                   INSTALL PACKAGES                         ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    local packages=("python" "python3" "git" "curl" "wget" "nano" "vim")
    
    echo "${CYAN}Package yang akan diinstall:${END}"
    for i in "${!packages[@]}"; do
        echo "  ${YELLOW}[$((i+1))]${END} ${packages[i]}"
    done
    
    echo "  ${YELLOW}[A]${END} Install semua package"
    echo "  ${YELLOW}[0]${END} Kembali"
    echo ""
    
    read -p "${GREEN}Pilih package (nomor/A/0): ${END}" choice
    choice=$(echo "$choice" | tr '[:lower:]' '[:upper:]')
    
    if [ "$choice" = "0" ]; then
        return
    elif [ "$choice" = "A" ]; then
        packages_to_install=("${packages[@]}")
    else
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#packages[@]}" ]; then
            packages_to_install=("${packages[choice-1]}")
        else
            echo "${RED}Pilihan tidak valid!${END}"
            sleep 1
            return
        fi
    fi
    
    for package in "${packages_to_install[@]}"; do
        start_loading "Installing $package"
        sleep 2
        
        if command -v pkg &> /dev/null; then
            # Termux
            pkg install -y "$package" &> /dev/null
        elif command -v apt-get &> /dev/null; then
            # Debian/Ubuntu
            sudo apt-get update &> /dev/null
            sudo apt-get install -y "$package" &> /dev/null
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            sudo yum install -y "$package" &> /dev/null
        elif command -v pacman &> /dev/null; then
            # Arch Linux
            sudo pacman -S --noconfirm "$package" &> /dev/null
        fi
        
        stop_loading
        
        if [ $? -eq 0 ]; then
            echo "${GREEN}✓ $package berhasil diinstall${END}"
        else
            echo "${RED}✗ Gagal install $package${END}"
        fi
    done
    
    echo ""
    read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
}

# Function to update system packages
update_system() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                     UPDATE SYSTEM                           ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    echo "${YELLOW}Memperbarui sistem...${END}"
    
    start_loading "Updating system packages"
    sleep 3
    
    if command -v pkg &> /dev/null; then
        # Termux
        pkg update -y && pkg upgrade -y
    elif command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update && sudo apt-get upgrade -y
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum update -y
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -Syu --noconfirm
    fi
    
    stop_loading
    
    if [ $? -eq 0 ]; then
        echo "${GREEN}✓ Sistem berhasil diupdate${END}"
    else
        echo "${RED}✗ Gagal update sistem${END}"
    fi
    
    echo ""
    read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
}

# Function to run Python scripts
run_python_script() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                   JALANKAN SCRIPT PYTHON                    ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    # Find Python files in current directory
    local python_files=($(find . -maxdepth 1 -name "*.py" -type f))
    
    if [ ${#python_files[@]} -eq 0 ]; then
        echo "${RED}Tidak ada file Python (.py) ditemukan di direktori ini.${END}"
        echo ""
        read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
        return
    fi
    
    echo "${CYAN}Pilih script Python yang ingin dijalankan:${END}"
    for i in "${!python_files[@]}"; do
        echo "  ${YELLOW}[$((i+1))]${END} ${python_files[i]#./}"
    done
    
    echo "  ${YELLOW}[0]${END} Kembali"
    echo ""
    
    read -p "${GREEN}Pilih nomor: ${END}" choice
    
    if [ "$choice" = "0" ]; then
        return
    fi
    
    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#python_files[@]}" ]; then
        local selected_file="${python_files[choice-1]}"
        
        start_loading "Menjalankan $selected_file"
        sleep 2
        stop_loading
        
        echo ""
        echo "${GREEN}Menjalankan: $selected_file${END}"
        echo "${CYAN}==================================================${END}"
        echo ""
        
        # Run Python script
        if command -v python3 &> /dev/null; then
            python3 "$selected_file"
        elif command -v python &> /dev/null; then
            python "$selected_file"
        else
            echo "${RED}Python tidak terinstall!${END}"
        fi
        
        echo ""
        read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
    else
        echo "${RED}Pilihan tidak valid!${END}"
        sleep 1
    fi
}

# Function to run web server
run_web_server() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                   JALANKAN SERVER WEB                       ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    # Create web directory if it doesn't exist
    local web_dir="web"
    if [ ! -d "$web_dir" ]; then
        echo "${YELLOW}Membuat direktori 'web'...${END}"
        mkdir -p "$web_dir"
    fi
    
    # Create index.html if it doesn't exist
    local index_file="$web_dir/index.html"
    if [ ! -f "$index_file" ]; then
        create_index_html
    fi
    
    echo "${CYAN}Pilih port untuk server web:${END}"
    echo "  ${YELLOW}[1]${END} Port 8080 (Default)"
    echo "  ${YELLOW}[2]${END} Port 8000"
    echo "  ${YELLOW}[3]${END} Custom port"
    echo "  ${YELLOW}[0]${END} Kembali"
    echo ""
    
    read -p "${GREEN}Pilih nomor: ${END}" choice
    
    if [ "$choice" = "0" ]; then
        return
    fi
    
    local port=8080
    
    case $choice in
        1) port=8080 ;;
        2) port=8000 ;;
        3)
            read -p "${CYAN}Masukkan port: ${END}" custom_port
            if [[ "$custom_port" =~ ^[0-9]+$ ]] && [ "$custom_port" -ge 1 ] && [ "$custom_port" -le 65535 ]; then
                port=$custom_port
            else
                echo "${RED}Port tidak valid! Menggunakan port 8080${END}"
            fi
            ;;
        *)
            echo "${RED}Pilihan tidak valid! Menggunakan port 8080${END}"
            ;;
    esac
    
    echo ""
    echo "${GREEN}Server web berhasil dijalankan!${END}"
    echo "${CYAN}URL: http://localhost:$port${END}"
    echo "${CYAN}Direktori: $(pwd)/$web_dir${END}"
    echo ""
    echo "${YELLOW}Tekan Ctrl+C untuk menghentikan server${END}"
    echo "${CYAN}==================================================${END}"
    echo ""
    
    # Start web server
    cd "$web_dir" && python3 -m http.server "$port"
    cd ..
    
    echo ""
    read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
}

# Function to create index.html
create_index_html() {
    cat > "web/index.html" << 'EOF'
<!DOCTYPE html>
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
</html>
EOF
    echo "${GREEN}File index.html berhasil dibuat${END}"
}

# Function to show system information
show_system_info() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                     INFORMASI SISTEM                        ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    local size=($(get_terminal_size))
    local cols=${size[0]}
    
    echo "${CYAN}Informasi Sistem:${END}"
    echo "  ${CYAN}Sistem Operasi:${END} ${YELLOW}$(uname -o)${END}"
    echo "  ${CYAN}Kernel:${END} ${YELLOW}$(uname -r)${END}"
    echo "  ${CYAN}Arsitektur:${END} ${YELLOW}$(uname -m)${END}"
    echo "  ${CYAN}Hostname:${END} ${YELLOW}$(hostname)${END}"
    echo "  ${CYAN}Direktori Saat Ini:${END} ${YELLOW}$(pwd)${END}"
    echo "  ${CYAN}User:${END} ${YELLOW}$(whoami)${END}"
    
    if check_internet; then
        echo "  ${CYAN}Koneksi Internet:${END} ${GREEN}✅ Terhubung${END}"
    else
        echo "  ${CYAN}Koneksi Internet:${END} ${RED}❌ Terputus${END}"
    fi
    
    echo "  ${CYAN}Ukuran Terminal:${END} ${YELLOW}${cols}x${size[1]}${END}"
    
    # Package manager info
    if command -v pkg &> /dev/null; then
        echo "  ${CYAN}Package Manager:${END} ${YELLOW}pkg (Termux)${END}"
    elif command -v apt-get &> /dev/null; then
        echo "  ${CYAN}Package Manager:${END} ${YELLOW}apt (Debian/Ubuntu)${END}"
    elif command -v yum &> /dev/null; then
        echo "  ${CYAN}Package Manager:${END} ${YELLOW}yum (CentOS/RHEL)${END}"
    elif command -v pacman &> /dev/null; then
        echo "  ${CYAN}Package Manager:${END} ${YELLOW}pacman (Arch)${END}"
    fi
    
    echo ""
    read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
}

# Function to show network tools
network_tools() {
    clear_screen
    display_ascii_art
    
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${END}"
    echo "${GREEN}║                     TOOLS JARINGAN                         ║${END}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${END}"
    echo ""
    
    echo "${CYAN}Pilih tool jaringan:${END}"
    echo "  ${YELLOW}[1]${END} Ping host"
    echo "  ${YELLOW}[2]${END} Cek IP address"
    echo "  ${YELLOW}[3]${END} Scan port lokal"
    echo "  ${YELLOW}[0]${END} Kembali"
    echo ""
    
    read -p "${GREEN}Pilih nomor: ${END}" choice
    
    case $choice in
        1)
            read -p "${CYAN}Masukkan host/IP untuk ping: ${END}" host
            if [ -n "$host" ]; then
                echo ""
                ping -c 4 "$host"
            fi
            ;;
        2)
            echo ""
            echo "${CYAN}IP Address:${END}"
            if command -v ip &> /dev/null; then
                ip addr show | grep -E "inet " | grep -v "127.0.0.1"
            else
                ifconfig | grep -E "inet " | grep -v "127.0.0.1"
            fi
            ;;
        3)
            echo ""
            echo "${CYAN}Port yang terbuka di localhost:${END}"
            if command -v netstat &> /dev/null; then
                netstat -tuln | grep LISTEN
            elif command -v ss &> /dev/null; then
                ss -tuln | grep LISTEN
            else
                echo "${RED}Tool netstat atau ss tidak tersedia${END}"
            fi
            ;;
        0) return ;;
        *) echo "${RED}Pilihan tidak valid!${END}" ;;
    esac
    
    echo ""
    read -p "${YELLOW}Tekan Enter untuk kembali...${END}" dummy
}

# Main menu function
main_menu() {
    while true; do
        clear_screen
        display_ascii_art
        
        local size=($(get_terminal_size))
        local cols=${size[0]}
        local header_width=$((cols < 80 ? cols - 4 : 76))
        
        # Create header line
        local header_line=""
        for ((i=0; i<header_width; i++)); do
            header_line+="═"
        done
        
        echo "${GREEN}╔${header_line}╗${END}"
        printf "${GREEN}║%*s%*s║${END}\n" $(( (header_width + 22) / 2 )) "MENU UTAMA - TERMUX & LINUX TOOL" $(( (header_width - 22) / 2 )) ""
        echo "${GREEN}╚${header_line}╝${END}"
        echo ""
        
        # Menu options
        echo "  ${YELLOW}[1]${END} 🐍 Jalankan Script Python"
        echo "  ${YELLOW}[2]${END} 🌐 Jalankan Server Web"
        echo "  ${YELLOW}[3]${END} 📦 Install Packages"
        echo "  ${YELLOW}[4]${END} 🔄 Update System"
        echo "  ${YELLOW}[5]${END} 💻 Informasi Sistem"
        echo "  ${YELLOW}[6]${END} 🌐 Tools Jaringan"
        echo "  ${YELLOW}[0]${END} 🚪 Keluar"
        echo ""
        echo "${CYAN}${header_line}${END}"
        
        # Platform info
        if [ -d "/data/data/com.termux" ]; then
            local platform_info="Termux"
        else
            local platform_info="Linux"
        fi
        echo "${MAGENTA}Platform: $platform_info | Terminal: ${cols}x${size[1]}${END}"
        echo ""
        
        read -p "${GREEN}Pilih menu [0-6]: ${END}" choice
        
        case $choice in
            1) run_python_script ;;
            2) run_web_server ;;
            3) install_packages ;;
            4) update_system ;;
            5) show_system_info ;;
            6) network_tools ;;
            0)
                echo ""
                echo "${GREEN}Terima kasih telah menggunakan Termux Multi-Tool! 👋${END}"
                echo "${CYAN}Sampai jumpa! 😊${END}"
                sleep 1
                break
                ;;
            *)
                echo "${RED}Pilihan tidak valid! Silakan pilih 0-6.${END}"
                sleep 1
                ;;
        esac
    done
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}Program dihentikan oleh pengguna.${END}"; exit 1' INT

# Main execution
if [ "$0" = "$BASH_SOURCE" ]; then
    main_menu
fi