#!/usr/bin/env python3
"""
Hackforge - Termux Web Server Suite
XAMPP-like solution for Termux with advanced features
Python Version dengan perbaikan lengkap
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
import urllib.request
import tarfile
import json
from pathlib import Path
import socket
import shutil
from datetime import datetime

# Konfigurasi
HOME_DIR = str(Path.home())
HACKFORGE_DIR = os.path.join(HOME_DIR, "hackforge")
WEB_ROOT = "/data/data/com.termux/files/usr/share/apache2/htdocs"
APACHE_CONF_DIR = "/data/data/com.termux/files/usr/etc/apache2"
MARIADB_DATA_DIR = os.path.join(HACKFORGE_DIR, "mysql_data")
BACKUP_DIR = os.path.join(HACKFORGE_DIR, "backups")
LOG_DIR = os.path.join(HACKFORGE_DIR, "logs")
PROJECTS_DIR = os.path.join(HACKFORGE_DIR, "projects")
CODE_EDITOR_DIR = os.path.join(HACKFORGE_DIR, "editor")

# Warna untuk output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    ORANGE = '\033[0;33m'
    PURPLE = '\033[0;95m'
    NC = '\033[0m'  # No Color

class Hackforge:
    def __init__(self):
        self.setup_directories()
        self.services = {
            'apache': False,
            'mariadb': False
        }
        
    def print_banner(self):
        """Menampilkan banner Hackforge"""
        banner = f"""
{Colors.MAGENTA}
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
║    Complete Coding Environment      ║
║         Python Edition              ║
╚═════════════════════════════════════╝
{Colors.NC}
"""
        print(banner)
    
    def print_status(self, message, status="info"):
        """Print status dengan warna"""
        colors = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED
        }
        prefix = {
            "info": "[+]",
            "success": "[✓]",
            "warning": "[!]",
            "error": "[✗]"
        }
        color = colors.get(status, Colors.BLUE)
        print(f"{color}{prefix[status]} {message}{Colors.NC}")
    
    def run_command(self, command, shell=False):
        """Menjalankan command dan return output"""
        try:
            if shell:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def check_internet(self):
        """Cek koneksi internet"""
        self.print_status("Mengecek koneksi internet...", "info")
        try:
            urllib.request.urlopen('http://google.com', timeout=3)
            self.print_status("Koneksi internet tersedia", "success")
            return True
        except:
            self.print_status("Tidak ada koneksi internet!", "error")
            return False
    
    def setup_directories(self):
        """Setup direktori Hackforge"""
        self.print_status("Setup direktori Hackforge...", "info")
        
        directories = [
            HACKFORGE_DIR,
            BACKUP_DIR,
            LOG_DIR,
            MARIADB_DATA_DIR,
            os.path.join(WEB_ROOT, "projects"),
            PROJECTS_DIR,
            CODE_EDITOR_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.print_status(f"Direktori {directory} siap", "success")
    
    def install_dependencies(self):
        """Install dependencies yang diperlukan"""
        self.print_status("Mengecek dependencies...", "info")
        
        dependencies = ["wget", "curl", "git", "python", "nodejs", "php", "apache2"]
        
        for dep in dependencies:
            code, stdout, stderr = self.run_command(f"pkg list-installed | grep -q {dep}", shell=True)
            if code != 0:
                self.print_status(f"Menginstall {dep}...", "warning")
                self.run_command(f"pkg install -y {dep}", shell=True)
                self.print_status(f"{dep} terinstall", "success")
            else:
                self.print_status(f"{dep} sudah terinstall", "success")
    
    def install_apache(self):
        """Install dan konfigurasi Apache"""
        self.print_status("Setup Apache Web Server...", "info")
        
        # Install Apache jika belum ada
        code, stdout, stderr = self.run_command("which apachectl", shell=True)
        if code != 0:
            self.print_status("Menginstall Apache...", "warning")
            self.run_command("pkg install -y apache2", shell=True)
        
        # Backup config original
        apache_conf = os.path.join(APACHE_CONF_DIR, "httpd.conf")
        backup_conf = apache_conf + ".bak"
        
        if not os.path.exists(backup_conf):
            shutil.copy2(apache_conf, backup_conf)
        
        # Buat config custom
        config_content = f'''
ServerRoot "/data/data/com.termux/files/usr"

LoadModule mpm_worker_module libexec/apache2/mod_mpm_worker.so
LoadModule authn_file_module libexec/apache2/mod_authn_file.so
LoadModule authn_core_module libexec/apache2/mod_authn_core.so
LoadModule authz_host_module libexec/apache2/mod_authz_host.so
LoadModule authz_groupfile_module libexec/apache2/mod_authz_groupfile.so
LoadModule authz_user_module libexec/apache2/mod_authz_user.so
LoadModule authz_core_module libexec/apache2/mod_authz_core.so
LoadModule access_compat_module libexec/apache2/mod_access_compat.so
LoadModule auth_basic_module libexec/apache2/mod_auth_basic.so
LoadModule reqtimeout_module libexec/apache2/mod_reqtimeout.so
LoadModule filter_module libexec/apache2/mod_filter.so
LoadModule mime_module libexec/apache2/mod_mime.so
LoadModule log_config_module libexec/apache2/mod_log_config.so
LoadModule env_module libexec/apache2/mod_env.so
LoadModule headers_module libache2/mod_headers.so
LoadModule setenvif_module libexec/apache2/mod_setenvif.so
LoadModule version_module libexec/apache2/mod_version.so
LoadModule unixd_module libexec/apache2/mod_unixd.so
LoadModule status_module libexec/apache2/mod_status.so
LoadModule autoindex_module libexec/apache2/mod_autoindex.so
LoadModule dir_module libexec/apache2/mod_dir.so
LoadModule alias_module libexec/apache2/mod_alias.so
LoadModule php_module libexec/apache2/libphp.so

Listen 8080

User {os.getlogin()}
Group {os.getlogin()}

ServerAdmin admin@hackforge.local
ServerName localhost:8080

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "{WEB_ROOT}"

<Directory "{WEB_ROOT}">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

<IfModule dir_module>
    DirectoryIndex index.html index.php
</IfModule>

<Files ".ht*">
    Require all denied
</Files>

ErrorLog "/data/data/com.termux/files/usr/var/log/apache2/error.log"
LogLevel warn

<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{{Referer}}i\" \"%{{User-Agent}}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common
    CustomLog "/data/data/com.termux/files/usr/var/log/apache2/access.log" common
</IfModule>

<IfModule mime_module>
    TypesConfig /data/data/com.termux/files/usr/etc/apache2/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps
</IfModule>

# PHP configuration
<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

PHPIniDir "/data/data/com.termux/files/usr/etc/php"
'''
        
        with open(apache_conf, 'w') as f:
            f.write(config_content)
        
        self.print_status("Apache configured", "success")
    
    def install_php(self):
        """Install PHP dengan extensions"""
        self.print_status("Setup PHP dengan extensions...", "info")
        
        php_extensions = [
            "php-apache", "php-mysqli", "php-pdo_mysql", 
            "php-curl", "php-gd", "php-mbstring", 
            "php-xml", "php-zip", "php-json"
        ]
        
        for ext in php_extensions:
            code, stdout, stderr = self.run_command(f"pkg list-installed | grep -q {ext}", shell=True)
            if code != 0:
                self.print_status(f"Menginstall {ext}...", "warning")
                self.run_command(f"pkg install -y {ext}", shell=True)
        
        # Configure PHP
        php_ini = "/data/data/com.termux/files/usr/etc/php.ini"
        if os.path.exists(php_ini):
            with open(php_ini, 'r') as f:
                content = f.read()
            
            replacements = {
                ';extension=mysqli': 'extension=mysqli',
                ';extension=pdo_mysql': 'extension=pdo_mysql',
                ';extension=curl': 'extension=curl',
                ';extension=gd': 'extension=gd',
                'display_errors = Off': 'display_errors = On',
                'upload_max_filesize = 2M': 'upload_max_filesize = 64M',
                'post_max_size = 8M': 'post_max_size = 64M'
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            with open(php_ini, 'w') as f:
                f.write(content)
        
        self.print_status("PHP configured", "success")
    
    def install_mariadb(self):
        """Install dan setup MariaDB"""
        self.print_status("Setup MariaDB Database...", "info")
        
        # Install MariaDB jika belum ada
        code, stdout, stderr = self.run_command("which mysql", shell=True)
        if code != 0:
            self.print_status("Menginstall MariaDB...", "warning")
            self.run_command("pkg install -y mariadb", shell=True)
        
        # Setup data directory
        mysql_dir = os.path.join(MARIADB_DATA_DIR, "mysql")
        if not os.path.exists(mysql_dir):
            self.print_status("Initialize MariaDB data directory...", "warning")
            self.run_command(f"mysql_install_db --datadir={MARIADB_DATA_DIR}", shell=True)
        
        # Buat config MariaDB
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        config_content = f'''
[mysqld]
datadir={MARIADB_DATA_DIR}
socket={HACKFORGE_DIR}/mysql.sock
user={os.getlogin()}
port=3306

# Security
skip-networking
bind-address=127.0.0.1

# Performance
key_buffer_size=16M
max_allowed_packet=16M
thread_stack=192K
thread_cache_size=8

[mysqld_safe]
log-error={LOG_DIR}/mariadb.log
pid-file={HACKFORGE_DIR}/mysqld.pid

[mysql]
socket={HACKFORGE_DIR}/mysql.sock

[client]
socket={HACKFORGE_DIR}/mysql.sock
'''
        
        with open(my_cnf, 'w') as f:
            f.write(config_content)
        
        self.print_status("MariaDB configured", "success")
    
    def install_phpmyadmin(self):
        """Install phpMyAdmin secara otomatis"""
        self.print_status("Setup phpMyAdmin...", "info")
        
        pma_dir = os.path.join(WEB_ROOT, "phpmyadmin")
        pma_version = "5.2.1"
        pma_url = f"https://files.phpmyadmin.net/phpMyAdmin/{pma_version}/phpMyAdmin-{pma_version}-all-languages.tar.gz"
        
        if not os.path.exists(pma_dir):
            os.makedirs(pma_dir, exist_ok=True)
            self.print_status("Downloading phpMyAdmin...", "warning")
            
            # Download phpMyAdmin
            tar_path = "/tmp/phpmyadmin.tar.gz"
            try:
                urllib.request.urlretrieve(pma_url, tar_path)
                
                # Extract
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall("/tmp/")
                
                # Move to web directory
                extracted_dir = f"/tmp/phpMyAdmin-{pma_version}-all-languages"
                if os.path.exists(extracted_dir):
                    for item in os.listdir(extracted_dir):
                        shutil.move(os.path.join(extracted_dir, item), pma_dir)
                    
                    # Cleanup
                    shutil.rmtree(extracted_dir)
                    os.remove(tar_path)
                
                # Buat config phpMyAdmin
                config_content = '''<?php
$cfg['blowfish_secret'] = 'hackforge_termux_secret_key_2024';
$i = 0;
$i++;
$cfg['Servers'][$i]['auth_type'] = 'cookie';
$cfg['Servers'][$i]['host'] = '127.0.0.1';
$cfg['Servers'][$i]['connect_type'] = 'tcp';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = true;
$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';
$cfg['TempDir'] = '/tmp';
?>
'''
                config_file = os.path.join(pma_dir, "config.inc.php")
                with open(config_file, 'w') as f:
                    f.write(config_content)
                
                self.print_status("phpMyAdmin installed", "success")
            except Exception as e:
                self.print_status(f"Error installing phpMyAdmin: {e}", "error")
        else:
            self.print_status("phpMyAdmin already installed", "success")
    
    def start_apache(self):
        """Start Apache web server"""
        self.print_status("Starting Apache...", "info")
        
        # Cek jika Apache sudah running
        code, stdout, stderr = self.run_command("pgrep -x httpd", shell=True)
        if code == 0:
            self.print_status("Apache already running", "warning")
            self.services['apache'] = True
            return True
        
        # Start Apache
        code, stdout, stderr = self.run_command("apachectl -k start", shell=True)
        if code == 0:
            self.print_status("Apache started successfully", "success")
            self.services['apache'] = True
            return True
        else:
            self.print_status(f"Failed to start Apache: {stderr}", "error")
            return False
    
    def start_mariadb(self):
        """Start MariaDB database server"""
        self.print_status("Starting MariaDB...", "info")
        
        # Cek jika MariaDB sudah running
        code, stdout, stderr = self.run_command("pgrep -x mysqld", shell=True)
        if code == 0:
            self.print_status("MariaDB already running", "warning")
            self.services['mariadb'] = True
            return True
        
        # Hentikan proses mysqld yang mungkin masih berjalan
        self.run_command("pkill mysqld", shell=True)
        time.sleep(2)
        
        # Start MariaDB dengan config custom
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        cmd = f"mysqld_safe --defaults-file={my_cnf} --datadir={MARIADB_DATA_DIR} &"
        code, stdout, stderr = self.run_command(cmd, shell=True)
        
        # Tunggu sampai MySQL ready
        for i in range(30):
            code, stdout, stderr = self.run_command(
                f"mysqladmin --defaults-file={my_cnf} ping", shell=True
            )
            if code == 0:
                self.print_status("MariaDB started successfully", "success")
                
                # Setup root password jika pertama kali
                mysql_configured = os.path.join(HACKFORGE_DIR, "mysql_configured")
                if not os.path.exists(mysql_configured):
                    self.print_status("Configuring MariaDB first time setup...", "warning")
                    self.run_command(
                        f"mysql --defaults-file={my_cnf} -u root -e \"ALTER USER 'root'@'localhost' IDENTIFIED BY '';\"",
                        shell=True
                    )
                    self.run_command(
                        f"mysql --defaults-file={my_cnf} -u root -e \"DELETE FROM mysql.user WHERE User='';\"",
                        shell=True
                    )
                    self.run_command(
                        f"mysql --defaults-file={my_cnf} -u root -e \"FLUSH PRIVILEGES;\"",
                        shell=True
                    )
                    Path(mysql_configured).touch()
                
                self.services['mariadb'] = True
                return True
            
            time.sleep(1)
        
        self.print_status("Failed to start MariaDB", "error")
        return False
    
    def stop_apache(self):
        """Stop Apache web server"""
        self.print_status("Stopping Apache...", "info")
        code, stdout, stderr = self.run_command("apachectl -k stop", shell=True)
        if code == 0:
            self.print_status("Apache stopped", "success")
            self.services['apache'] = False
        else:
            self.print_status("Failed to stop Apache", "error")
    
    def stop_mariadb(self):
        """Stop MariaDB database server"""
        self.print_status("Stopping MariaDB...", "info")
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        code, stdout, stderr = self.run_command(
            f"mysqladmin --defaults-file={my_cnf} shutdown", shell=True
        )
        if code == 0:
            self.print_status("MariaDB stopped", "success")
            self.services['mariadb'] = False
        else:
            self.print_status("Failed to stop MariaDB", "error")
    
    def check_services_status(self):
        """Cek status semua services"""
        # Cek Apache
        code, stdout, stderr = self.run_command("pgrep -x httpd", shell=True)
        apache_running = code == 0
        
        # Cek MariaDB
        code, stdout, stderr = self.run_command("pgrep -x mysqld", shell=True)
        mariadb_running = code == 0
        
        return apache_running, mariadb_running
    
    def create_sample_project(self):
        """Buat sample project demo"""
        self.print_status("Membuat sample project...", "info")
        
        project_dir = os.path.join(WEB_ROOT, "projects")
        os.makedirs(project_dir, exist_ok=True)
        
        # Buat demo.php
        demo_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackforge Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0,0,0,0.7);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .status-box {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover {
            background: #0056b3;
        }
        .success { color: #00ff00; }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Hackforge Python Edition</h1>
            <p>Your Complete Web Development Suite for Termux</p>
        </div>

        <div class="status-box">
            <h3>🛠️ System Status</h3>
            <p>Apache: <span class="success">● RUNNING</span></p>
            <p>MariaDB: <span class="success">● RUNNING</span></p>
            <p>PHP: <span class="success">● READY</span></p>
        </div>

        <div style="text-align: center; margin: 20px 0;">
            <a href="/phpmyadmin" class="btn" target="_blank">Open phpMyAdmin</a>
            <a href="/info.php" class="btn" target="_blank">PHP Info</a>
            <a href="/projects/" class="btn" target="_blank">Projects</a>
        </div>

        <?php
        // Database connection test
        echo '<div class="status-box">';
        echo '<h3>🧪 Database Test</h3>';
        
        try {
            $socket = '/data/data/com.termux/files/home/hackforge/mysql.sock';
            $conn = new mysqli('127.0.0.1', 'root', '', 'mysql', 3306, $socket);
            
            if ($conn->connect_error) {
                echo '<p class="error">❌ Database Connection Failed: ' . $conn->connect_error . '</p>';
            } else {
                echo '<p class="success">✅ Database Connected Successfully!</p>';
                
                // Show MySQL version
                $result = $conn->query("SELECT VERSION() as version");
                $row = $result->fetch_assoc();
                echo '<p>MySQL Version: ' . $row['version'] . '</p>';
                
                $conn->close();
            }
        } catch (Exception $e) {
            echo '<p class="error">❌ Database Error: ' . $e->getMessage() . '</p>';
        }
        echo '</div>';
        ?>

        <div class="status-box">
            <h3>📁 Quick Links</h3>
            <ul>
                <li><a href="/phpmyadmin" style="color: #48dbfb;">phpMyAdmin</a> - Database management</li>
                <li><a href="/info.php" style="color: #48dbfb;">PHP Info</a> - PHP configuration</li>
                <li><a href="/projects/" style="color: #48dbfb;">Projects Directory</a> - Your web projects</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''
        
        demo_file = os.path.join(project_dir, "demo.php")
        with open(demo_file, 'w') as f:
            f.write(demo_content)
        
        # Buat info.php
        info_file = os.path.join(WEB_ROOT, "info.php")
        with open(info_file, 'w') as f:
            f.write("<?php phpinfo(); ?>")
        
        self.print_status("Sample projects created", "success")
    
    def install_complete(self):
        """Installasi lengkap Hackforge"""
        self.print_banner()
        
        if not self.check_internet():
            return False
        
        self.print_status("Starting Hackforge installation...", "info")
        
        # Install dependencies
        self.install_dependencies()
        
        # Setup components
        self.install_apache()
        self.install_php()
        self.install_mariadb()
        self.install_phpmyadmin()
        self.create_sample_project()
        
        # Tandai sudah terinstall
        installed_file = os.path.join(HACKFORGE_DIR, "installed")
        with open(installed_file, 'w') as f:
            f.write(f"Hackforge installed at {datetime.now()}")
        
        self.print_status("Hackforge installation complete!", "success")
        
        # Start services
        self.start_services()
        
        return True
    
    def start_services(self):
        """Start semua services"""
        self.print_status("Starting all services...", "info")
        self.start_apache()
        self.start_mariadb()
    
    def stop_services(self):
        """Stop semua services"""
        self.print_status("Stopping all services...", "info")
        self.stop_apache()
        self.stop_mariadb()
    
    def restart_services(self):
        """Restart semua services"""
        self.print_status("Restarting all services...", "info")
        self.stop_services()
        time.sleep(2)
        self.start_services()
    
    def show_status(self):
        """Tampilkan status services"""
        apache_status, mariadb_status = self.check_services_status()
        
        print(f"\n{Colors.CYAN}Hackforge Services Status{Colors.NC}")
        print("─" * 40)
        
        print(f"Apache:    {'● RUNNING' if apache_status else '● STOPPED'}")
        print(f"MariaDB:   {'● RUNNING' if mariadb_status else '● STOPPED'}")
        
        # Check PHP
        code, stdout, stderr = self.run_command("which php", shell=True)
        php_status = code == 0
        print(f"PHP:       {'● INSTALLED' if php_status else '● NOT INSTALLED'}")
        
        print("─" * 40)
        print(f"Web Server: {Colors.BLUE}http://localhost:8080{Colors.NC}")
        print(f"phpMyAdmin: {Colors.BLUE}http://localhost:8080/phpmyadmin{Colors.NC}")
        print(f"Demo Page:  {Colors.BLUE}http://localhost:8080/projects/demo.php{Colors.NC}")
        print(f"PHP Info:   {Colors.BLUE}http://localhost:8080/info.php{Colors.NC}")
    
    def open_in_browser(self, url_path=""):
        """Buka URL di browser"""
        url = f"http://localhost:8080{url_path}"
        self.print_status(f"Opening {url}", "info")
        try:
            webbrowser.open(url)
        except:
            self.print_status("Could not open browser automatically", "warning")
            print(f"Please open manually: {Colors.BLUE}{url}{Colors.NC}")

def main():
    """Main function"""
    hackforge = Hackforge()
    
    while True:
        hackforge.print_banner()
        hackforge.show_status()
        
        print(f"\n{Colors.CYAN}MAIN MENU:{Colors.NC}")
        print("1. 🚀 INSTALL Hackforge (Full Setup)")
        print("2. ⚡ START All Services")
        print("3. 🛑 STOP All Services")
        print("4. 🔄 RESTART All Services")
        print("5. 🌐 OPEN Web Interface")
        print("6. 🗃️  OPEN phpMyAdmin")
        print("7. 📊 OPEN PHP Info")
        print("8. 📁 OPEN Projects")
        print("9. ℹ️  SYSTEM Info")
        print("0. ❌ EXIT")
        
        choice = input(f"\n{Colors.YELLOW}Choose option [0-9]: {Colors.NC}").strip()
        
        if choice == "1":
            hackforge.install_complete()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
        
        elif choice == "2":
            hackforge.start_services()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
        
        elif choice == "3":
            hackforge.stop_services()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
        
        elif choice == "4":
            hackforge.restart_services()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
        
        elif choice == "5":
            hackforge.open_in_browser()
        
        elif choice == "6":
            hackforge.open_in_browser("/phpmyadmin")
        
        elif choice == "7":
            hackforge.open_in_browser("/info.php")
        
        elif choice == "8":
            hackforge.open_in_browser("/projects/")
        
        elif choice == "9":
            print(f"\n{Colors.CYAN}System Information:{Colors.NC}")
            print("─" * 30)
            print(f"OS: {os.uname().sysname} {os.uname().release}")
            print(f"Architecture: {os.uname().machine}")
            print(f"Hackforge Dir: {HACKFORGE_DIR}")
            print(f"Web Root: {WEB_ROOT}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
        
        elif choice == "0":
            hackforge.print_status("Stopping services...", "info")
            hackforge.stop_services()
            hackforge.print_status("Thank you for using Hackforge! 👋", "success")
            break
        
        else:
            hackforge.print_status("Invalid choice!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Program interrupted by user{Colors.NC}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.NC}")