#!/bin/bash

# Hackforge - Termux Web Server Suite
# XAMPP-like solution for Termux with advanced features

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
ORANGE='\033[0;33m'
PURPLE='\033[0;95m'
NC='\033[0m' # No Color

# Konfigurasi
HACKFORGE_DIR="$HOME/hackforge"
WEB_ROOT="/data/data/com.termux/files/usr/share/apache2/htdocs"
APACHE_CONF_DIR="/data/data/com.termux/files/usr/etc/apache2"
MARIADB_DATA_DIR="$HACKFORGE_DIR/mysql_data"
BACKUP_DIR="$HACKFORGE_DIR/backups"
LOG_DIR="$HACKFORGE_DIR/logs"
PROJECTS_DIR="$HACKFORGE_DIR/projects"
CODE_EDITOR_DIR="$HACKFORGE_DIR/editor"

# Fungsi animasi loading
show_loading() {
    local pid=$1
    local text=$2
    local delay=0.1
    local spinstr='|/-\'
    
    echo -n -e "${YELLOW}[ ] ${text}... ${NC}"
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "\b\b\b\b\b\b"
    echo -e "${GREEN}[✓] ${text} selesai!${NC}"
}

# Fungsi cek koneksi internet
check_internet() {
    echo -e "${YELLOW}[+] Mengecek koneksi internet...${NC}"
    if ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        echo -e "${GREEN}[✓] Koneksi internet tersedia${NC}"
        return 0
    else
        echo -e "${RED}[✗] Tidak ada koneksi internet!${NC}"
        return 1
    fi
}

# Fungsi cek dan install dependencies
check_dependencies() {
    echo -e "${CYAN}[+] Mengecek dependencies...${NC}"
    
    local deps=("wget" "curl" "git" "python" "nodejs" "php" "apache2")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null && ! pkg list-installed | grep -q $dep; then
            missing+=($dep)
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${YELLOW}[+] Menginstall dependencies yang diperlukan...${NC}"
        pkg update -y && pkg upgrade -y
        for dep in "${missing[@]}"; do
            echo -e "${BLUE}[+] Menginstall $dep...${NC}"
            pkg install -y $dep
        done
    else
        echo -e "${GREEN}[✓] Semua dependencies sudah terinstall${NC}"
    fi
}

# Fungsi setup direktori
setup_directories() {
    echo -e "${CYAN}[+] Setup direktori Hackforge...${NC}"
    
    local dirs=("$HACKFORGE_DIR" "$BACKUP_DIR" "$LOG_DIR" "$MARIADB_DATA_DIR" "$WEB_ROOT/projects" "$PROJECTS_DIR" "$CODE_EDITOR_DIR")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo -e "${GREEN}[✓] Direktori $dir dibuat${NC}"
        fi
    done
}

# Fungsi install dan setup MariaDB dengan perbaikan
install_mariadb() {
    echo -e "${CYAN}[+] Setup MariaDB Database...${NC}"
    
    if ! command -v mysql &> /dev/null; then
        echo -e "${YELLOW}[+] Menginstall MariaDB...${NC}"
        pkg install -y mariadb
        
        # Setup data directory
        if [ ! -d "$MARIADB_DATA_DIR/mysql" ]; then
            echo -e "${YELLOW}[+] Initialize MariaDB data directory...${NC}"
            mysql_install_db --datadir="$MARIADB_DATA_DIR"
        fi
    fi

    # Buat config MariaDB untuk Termux
    cat > "$HACKFORGE_DIR/my.cnf" << EOF
[mysqld]
datadir=$MARIADB_DATA_DIR
socket=$HACKFORGE_DIR/mysql.sock
user=$(whoami)
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
log-error=$LOG_DIR/mariadb.log
pid-file=$HACKFORGE_DIR/mysqld.pid

[mysql]
socket=$HACKFORGE_DIR/mysql.sock

[client]
socket=$HACKFORGE_DIR/mysql.sock
EOF

    echo -e "${GREEN}[✓] MariaDB configured${NC}"
}

# Fungsi start MariaDB dengan perbaikan
start_mariadb() {
    echo -e "${YELLOW}[+] Starting MariaDB...${NC}"
    
    # Hentikan proses mysqld yang mungkin masih berjalan
    pkill mysqld 2>/dev/null
    sleep 2
    
    # Start MariaDB dengan config custom
    mysqld_safe --defaults-file="$HACKFORGE_DIR/my.cnf" --datadir="$MARIADB_DATA_DIR" &
    
    # Tunggu sampai MySQL ready
    local counter=0
    while true; do
        if mysqladmin --defaults-file="$HACKFORGE_DIR/my.cnf" ping >/dev/null 2>&1; then
            echo -e "${GREEN}[✓] MariaDB started successfully${NC}"
            
            # Setup root password jika pertama kali
            if [ ! -f "$HACKFORGE_DIR/mysql_configured" ]; then
                echo -e "${YELLOW}[+] Configuring MariaDB first time setup...${NC}"
                mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';" 2>/dev/null
                mysql -u root -e "DELETE FROM mysql.user WHERE User='';" 2>/dev/null
                mysql -u root -e "FLUSH PRIVILEGES;" 2>/dev/null
                touch "$HACKFORGE_DIR/mysql_configured"
            fi
            return 0
        fi
        
        counter=$((counter + 1))
        if [ $counter -gt 30 ]; then
            echo -e "${RED}[✗] Failed to start MariaDB${NC}"
            return 1
        fi
        sleep 1
    done
}

# Fungsi install Apache dengan perbaikan
install_apache() {
    echo -e "${CYAN}[+] Setup Apache Web Server...${NC}"
    
    if ! command -v apachectl &> /dev/null; then
        pkg install -y apache2
    fi
    
    # Backup config original
    if [ ! -f "$APACHE_CONF_DIR/httpd.conf.bak" ]; then
        cp "$APACHE_CONF_DIR/httpd.conf" "$APACHE_CONF_DIR/httpd.conf.bak"
    fi
    
    # Buat config custom untuk Hackforge
    cat > "$APACHE_CONF_DIR/httpd.conf" << 'EOF'
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
LoadModule headers_module libexec/apache2/mod_headers.so
LoadModule setenvif_module libexec/apache2/mod_setenvif.so
LoadModule version_module libexec/apache2/mod_version.so
LoadModule unixd_module libexec/apache2/mod_unixd.so
LoadModule status_module libexec/apache2/mod_status.so
LoadModule autoindex_module libexec/apache2/mod_autoindex.so
LoadModule dir_module libexec/apache2/mod_dir.so
LoadModule alias_module libexec/apache2/mod_alias.so
LoadModule php_module libexec/apache2/libphp.so

Listen 8080

User $(whoami)
Group $(whoami)

ServerAdmin admin@hackforge.local
ServerName localhost:8080

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "/data/data/com.termux/files/usr/share/apache2/htdocs"

<Directory "/data/data/com.termux/files/usr/share/apache2/htdocs">
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
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
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
EOF

    echo -e "${GREEN}[✓] Apache configured${NC}"
}

# Fungsi install PHP dengan extensions
install_php() {
    echo -e "${CYAN}[+] Setup PHP dengan extensions...${NC}"
    
    local php_extensions=("php-apache" "php-mysqli" "php-pdo_mysql" "php-curl" "php-gd" "php-mbstring" "php-xml" "php-zip" "php-json")
    
    for ext in "${php_extensions[@]}"; do
        if ! pkg list-installed | grep -q $ext; then
            echo -e "${BLUE}[+] Menginstall $ext...${NC}"
            pkg install -y $ext
        fi
    done
    
    # Configure PHP
    local php_ini="/data/data/com.termux/files/usr/etc/php.ini"
    if [ -f "$php_ini" ]; then
        sed -i 's/;extension=mysqli/extension=mysqli/g' "$php_ini"
        sed -i 's/;extension=pdo_mysql/extension=pdo_mysql/g' "$php_ini"
        sed -i 's/;extension=curl/extension=curl/g' "$php_ini"
        sed -i 's/;extension=gd/extension=gd/g' "$php_ini"
        sed -i 's/display_errors = Off/display_errors = On/g' "$php_ini"
        sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 64M/g' "$php_ini"
        sed -i 's/post_max_size = 8M/post_max_size = 64M/g' "$php_ini"
    fi
    
    echo -e "${GREEN}[✓] PHP configured${NC}"
}

# Fungsi install phpMyAdmin
install_phpmyadmin() {
    echo -e "${CYAN}[+] Setup phpMyAdmin...${NC}"
    
    local pma_dir="$WEB_ROOT/phpmyadmin"
    local pma_version="5.2.1"
    local pma_url="https://files.phpmyadmin.net/phpMyAdmin/$pma_version/phpMyAdmin-$pma_version-all-languages.tar.gz"
    
    if [ ! -d "$pma_dir" ]; then
        mkdir -p "$pma_dir"
        echo -e "${BLUE}[+] Downloading phpMyAdmin...${NC}"
        wget -q -O "/tmp/phpmyadmin.tar.gz" "$pma_url"
        tar -xzf "/tmp/phpmyadmin.tar.gz" -C "$pma_dir" --strip-components=1
        rm "/tmp/phpmyadmin.tar.gz"
        
        # Buat config phpMyAdmin
        cat > "$pma_dir/config.inc.php" << 'EOF'
<?php
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
EOF
    fi
    
    echo -e "${GREEN}[✓] phpMyAdmin installed${NC}"
}

# Fungsi install code editor (Ace Editor)
install_code_editor() {
    echo -e "${CYAN}[+] Installing Web Code Editor...${NC}"
    
    local editor_dir="$CODE_EDITOR_DIR"
    
    # Download Ace Editor
    if [ ! -f "$editor_dir/ace.js" ]; then
        echo -e "${BLUE}[+] Downloading Ace Editor...${NC}"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js" -O "$editor_dir/ace.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-language_tools.js" -O "$editor_dir/ext-language_tools.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-php.js" -O "$editor_dir/mode-php.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-html.js" -O "$editor_dir/mode-html.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-javascript.js" -O "$editor_dir/mode-javascript.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-css.js" -O "$editor_dir/mode-css.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-mysql.js" -O "$editor_dir/mode-mysql.js"
        wget -q "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/theme-monokai.js" -O "$editor_dir/theme-monokai.js"
    fi
    
    # Buat file editor HTML
    cat > "$WEB_ROOT/editor.php" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackforge Code Editor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace;
            background: #1a1a1a;
            color: #f0f0f0;
            height: 100vh;
            overflow: hidden;
        }
        .header {
            background: #2d2d2d;
            padding: 10px;
            border-bottom: 1px solid #444;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            font-size: 1.2em;
            font-weight: bold;
            color: #00ff00;
        }
        .controls {
            display: flex;
            gap: 10px;
        }
        button {
            background: #444;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
        }
        button:hover {
            background: #555;
        }
        .container {
            display: flex;
            height: calc(100vh - 50px);
        }
        .sidebar {
            width: 200px;
            background: #252525;
            border-right: 1px solid #444;
            padding: 10px;
            overflow-y: auto;
        }
        .editor-container {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        #editor {
            flex: 1;
            font-size: 14px;
        }
        .file-list {
            list-style: none;
        }
        .file-item {
            padding: 5px;
            cursor: pointer;
            border-radius: 3px;
            margin-bottom: 2px;
        }
        .file-item:hover {
            background: #444;
        }
        .file-item.active {
            background: #0066cc;
        }
        .status-bar {
            background: #2d2d2d;
            padding: 5px 10px;
            border-top: 1px solid #444;
            font-size: 12px;
            color: #888;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
        }
        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #2d2d2d;
            padding: 20px;
            border-radius: 5px;
            min-width: 300px;
        }
        .modal input {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            background: #1a1a1a;
            border: 1px solid #444;
            color: white;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">Hackforge Code Editor</div>
        <div class="controls">
            <button onclick="newFile()">New File</button>
            <button onclick="saveFile()">Save</button>
            <button onclick="runCode()">Run</button>
            <button onclick="toggleTheme()">Theme</button>
        </div>
    </div>

    <div class="container">
        <div class="sidebar">
            <h4>Projects</h4>
            <ul class="file-list" id="fileList">
                <!-- Files will be loaded here -->
            </ul>
        </div>
        <div class="editor-container">
            <div id="editor"></div>
            <div class="status-bar">
                <span id="status">Ready</span>
            </div>
        </div>
    </div>

    <div id="newFileModal" class="modal">
        <div class="modal-content">
            <h3>Create New File</h3>
            <input type="text" id="fileName" placeholder="filename.php" />
            <div style="text-align: right; margin-top: 10px;">
                <button onclick="createNewFile()">Create</button>
                <button onclick="closeModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script src="../hackforge/editor/ace.js"></script>
    <script src="../hackforge/editor/mode-php.js"></script>
    <script src="../hackforge/editor/mode-html.js"></script>
    <script src="../hackforge/editor/mode-javascript.js"></script>
    <script src="../hackforge/editor/mode-css.js"></script>
    <script src="../hackforge/editor/mode-mysql.js"></script>
    <script src="../hackforge/editor/theme-monokai.js"></script>
    <script src="../hackforge/editor/ext-language_tools.js"></script>

    <script>
        let editor;
        let currentFile = '';
        let isDarkTheme = true;

        function initEditor() {
            editor = ace.edit("editor");
            editor.setTheme("ace/theme/monokai");
            editor.session.setMode("ace/mode/php");
            editor.setOptions({
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                fontSize: "12pt"
            });
        }

        function loadFileList() {
            fetch('?action=list_files')
                .then(response => response.json())
                .then(files => {
                    const fileList = document.getElementById('fileList');
                    fileList.innerHTML = '';
                    files.forEach(file => {
                        const li = document.createElement('li');
                        li.className = 'file-item';
                        li.textContent = file.name;
                        li.onclick = () => openFile(file.path);
                        fileList.appendChild(li);
                    });
                });
        }

        function openFile(filePath) {
            fetch(`?action=open_file&file=${encodeURIComponent(filePath)}`)
                .then(response => response.text())
                .then(content => {
                    editor.setValue(content);
                    currentFile = filePath;
                    updateStatus(`Editing: ${filePath}`);
                    
                    // Set mode based on file extension
                    const ext = filePath.split('.').pop().toLowerCase();
                    const modes = {
                        'php': 'php',
                        'html': 'html',
                        'js': 'javascript',
                        'css': 'css',
                        'sql': 'mysql'
                    };
                    editor.session.setMode(`ace/mode/${modes[ext] || 'text'}`);
                });
        }

        function saveFile() {
            if (!currentFile) {
                newFile();
                return;
            }
            
            const content = editor.getValue();
            const formData = new FormData();
            formData.append('action', 'save_file');
            formData.append('file', currentFile);
            formData.append('content', content);
            
            fetch('?action=save_file', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(result => {
                updateStatus(`Saved: ${currentFile}`);
            });
        }

        function newFile() {
            document.getElementById('newFileModal').style.display = 'block';
            document.getElementById('fileName').focus();
        }

        function createNewFile() {
            const fileName = document.getElementById('fileName').value;
            if (fileName) {
                currentFile = `projects/${fileName}`;
                editor.setValue('<?php\n// New PHP file\necho "Hello Hackforge!";\n?>');
                closeModal();
                saveFile();
            }
        }

        function closeModal() {
            document.getElementById('newFileModal').style.display = 'none';
        }

        function runCode() {
            if (currentFile && currentFile.endsWith('.php')) {
                window.open(`/${currentFile}`, '_blank');
            } else {
                updateStatus('Can only run PHP files');
            }
        }

        function toggleTheme() {
            isDarkTheme = !isDarkTheme;
            editor.setTheme(isDarkTheme ? "ace/theme/monokai" : "ace/theme/chrome");
        }

        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }

        // Initialize
        initEditor();
        loadFileList();
        
        // Auto-save every 30 seconds
        setInterval(saveFile, 30000);
    </script>

    <?php
    // PHP backend for file operations
    if (isset($_GET['action'])) {
        switch ($_GET['action']) {
            case 'list_files':
                $files = [];
                $projectFiles = glob($_SERVER['DOCUMENT_ROOT'] . '/projects/*.{php,html,js,css,sql,txt}', GLOB_BRACE);
                foreach ($projectFiles as $file) {
                    $files[] = [
                        'name' => basename($file),
                        'path' => 'projects/' . basename($file)
                    ];
                }
                header('Content-Type: application/json');
                echo json_encode($files);
                exit;
                
            case 'open_file':
                if (isset($_GET['file'])) {
                    $filePath = $_SERVER['DOCUMENT_ROOT'] . '/' . $_GET['file'];
                    if (file_exists($filePath)) {
                        echo file_get_contents($filePath);
                    }
                }
                exit;
        }
    }

    if ($_POST['action'] ?? '' === 'save_file') {
        $filePath = $_SERVER['DOCUMENT_ROOT'] . '/' . $_POST['file'];
        file_put_contents($filePath, $_POST['content']);
        echo 'OK';
        exit;
    }
    ?>
</body>
</html>
EOF

    echo -e "${GREEN}[✓] Web Code Editor installed${NC}"
}

# Fungsi buat sample project
create_sample_project() {
    echo -e "${CYAN}[+] Membuat sample project...${NC}"
    
    local project_dir="$WEB_ROOT/projects"
    
    # Buat index.php demo
    cat > "$project_dir/demo.php" << 'EOF'
<!DOCTYPE html>
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
        .code-editor {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Hackforge Code Environment</h1>
            <p>Your Complete Web Development Suite for Termux</p>
        </div>

        <div class="code-editor">
            <h3>🚀 Quick Start</h3>
            <p>Access the code editor: <a href="/editor.php" style="color: #48dbfb;">/editor.php</a></p>
            <p>Create new PHP files and run them instantly!</p>
        </div>

        <div style="text-align: center; margin: 20px 0;">
            <button class="btn" onclick="window.open('/editor.php', '_blank')">Open Code Editor</button>
            <button class="btn" onclick="window.open('/phpmyadmin', '_blank')">Open phpMyAdmin</button>
            <button class="btn" onclick="window.open('/info.php', '_blank')">PHP Info</button>
        </div>

        <?php
        // Database connection test
        echo '<div class="code-editor">';
        echo '<h3>🧪 Database Test</h3>';
        
        try {
            $conn = new mysqli('127.0.0.1', 'root', '', 'mysql', 3306, '/data/data/com.termux/files/home/hackforge/mysql.sock');
            
            if ($conn->connect_error) {
                echo '<p style="color: #ff6b6b;">❌ Database Connection Failed: ' . $conn->connect_error . '</p>';
            } else {
                echo '<p style="color: #00ff00;">✅ Database Connected Successfully!</p>';
                
                // Show MySQL version
                $result = $conn->query("SELECT VERSION() as version");
                $row = $result->fetch_assoc();
                echo '<p>MySQL Version: ' . $row['version'] . '</p>';
                
                $conn->close();
            }
        } catch (Exception $e) {
            echo '<p style="color: #ff6b6b;">❌ Database Error: ' . $e->getMessage() . '</p>';
        }
        echo '</div>';
        ?>

        <div class="code-editor">
            <h3>🛠️ Available Tools</h3>
            <ul>
                <li>✅ Apache Web Server</li>
                <li>✅ PHP with Extensions</li>
                <li>✅ MariaDB Database</li>
                <li>✅ phpMyAdmin</li>
                <li>✅ Web Code Editor</li>
                <li>✅ File Manager</li>
                <li>✅ Project Management</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

    # Buat info.php
    cat > "$WEB_ROOT/info.php" << 'EOF'
<?php
phpinfo();
?>
EOF

    echo -e "${GREEN}[✓] Sample projects created${NC}"
}

# Fungsi start services dengan perbaikan
start_services() {
    echo -e "${CYAN}[+] Starting Hackforge Services...${NC}"
    
    # Start Apache
    if ! pgrep -x "httpd" > /dev/null; then
        apachectl -k start
        echo -e "${GREEN}[✓] Apache started${NC}"
    else
        echo -e "${YELLOW}[!] Apache already running${NC}"
    fi
    
    # Start MariaDB
    start_mariadb
}

# Fungsi stop services
stop_services() {
    echo -e "${CYAN}[+] Stopping Hackforge Services...${NC}"
    
    # Stop Apache
    if pgrep -x "httpd" > /dev/null; then
        apachectl -k stop
        echo -e "${GREEN}[✓] Apache stopped${NC}"
    fi
    
    # Stop MariaDB
    if pgrep -x "mysqld" > /dev/null; then
        mysqladmin --defaults-file="$HACKFORGE_DIR/my.cnf" shutdown
        echo -e "${GREEN}[✓] MariaDB stopped${NC}"
    fi
}

# Fungsi status services
status_services() {
    echo -e "${CYAN}[+] Hackforge Services Status${NC}"
    echo -e "─────────────────────────────"
    
    # Check Apache
    if pgrep -x "httpd" > /dev/null; then
        echo -e "Apache:    ${GREEN}● RUNNING${NC}"
    else
        echo -e "Apache:    ${RED}● STOPPED${NC}"
    fi
    
    # Check MariaDB
    if pgrep -x "mysqld" > /dev/null; then
        echo -e "MariaDB:   ${GREEN}● RUNNING${NC}"
    else
        echo -e "MariaDB:   ${RED}● STOPPED${NC}"
    fi
    
    # Check PHP
    if command -v php &> /dev/null; then
        echo -e "PHP:       ${GREEN}● INSTALLED${NC}"
    else
        echo -e "PHP:       ${RED}● NOT INSTALLED${NC}"
    fi
    
    echo -e "─────────────────────────────"
    echo -e "Web Server: ${BLUE}http://localhost:8080${NC}"
    echo -e "Code Editor: ${BLUE}http://localhost:8080/editor.php${NC}"
    echo -e "phpMyAdmin: ${BLUE}http://localhost:8080/phpmyadmin${NC}"
    echo -e "Demo Page:  ${BLUE}http://localhost:8080/projects/demo.php${NC}"
}

# Fungsi install Hackforge
install_hackforge() {
    clear
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║             HACKFORGE INSTALLER              ║"
    echo "║            Complete Code Environment         ║"
    echo "║                                              ║"
    echo "║            Installing Components...          ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    if ! check_internet; then
        echo -e "${RED}[!] Installation requires internet connection${NC}"
        return 1
    fi
    
    # Eksekusi installasi
    check_dependencies
    setup_directories
    install_apache
    install_php
    install_mariadb
    install_phpmyadmin
    install_code_editor
    create_sample_project
    
    # Tandai sudah terinstall
    touch "$HACKFORGE_DIR/installed"
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║           INSTALLATION COMPLETE!             ║"
    echo "║                                              ║"
    echo "║        Hackforge is ready to use!            ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    start_services
    status_services
    
    echo -e "\n${YELLOW}Quick Start:${NC}"
    echo -e "1. Open browser: ${BLUE}http://localhost:8080${NC}"
    echo -e "2. Code Editor: ${BLUE}http://localhost:8080/editor.php${NC}"
    echo -e "3. Create PHP files in ${BLUE}http://localhost:8080/projects/${NC}"
    echo -e "4. Database Admin: ${BLUE}http://localhost:8080/phpmyadmin${NC}"
    
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Fungsi quick coding
quick_coding() {
    echo -e "${CYAN}[+] Quick Coding Mode${NC}"
    echo -e "${YELLOW}Enter PHP code (type 'END' on new line to finish):${NC}"
    
    local code=""
    local line
    
    while true; do
        read -r line
        if [ "$line" = "END" ]; then
            break
        fi
        code="$code$line\n"
    done
    
    local filename="quick_demo_$(date +%s).php"
    local filepath="$WEB_ROOT/projects/$filename"
    
    echo -e "<?php\n$code" > "$filepath"
    
    echo -e "${GREEN}[✓] File created: $filename${NC}"
    echo -e "${BLUE}[+] Access at: http://localhost:8080/projects/$filename${NC}"
    
    # Auto open in browser
    am start -a android.intent.action.VIEW -d "http://localhost:8080/projects/$filename" 2>/dev/null &
}

# Fungsi create new project
create_new_project() {
    echo -e -n "${YELLOW}Enter project name: ${NC}"
    read project_name
    
    if [ -z "$project_name" ]; then
        echo -e "${RED}[!] Project name cannot be empty${NC}"
        return
    fi
    
    local project_dir="$WEB_ROOT/projects/$project_name"
    
    if [ -d "$project_dir" ]; then
        echo -e "${RED}[!] Project already exists${NC}"
        return
    fi
    
    mkdir -p "$project_dir"
    
    # Buat file index.php untuk project
    cat > "$project_dir/index.php" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>$project_name - Hackforge</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px;
            background: #1a1a1a;
            color: white;
        }
        .container {
            background: #2d2d2d;
            padding: 30px;
            border-radius: 10px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #00ff00;
        }
        .info {
            background: #3d3d3d;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 $project_name</h1>
        <p>Welcome to your new Hackforge project!</p>
        
        <div class="info">
            <h3>Project Information:</h3>
            <p><strong>Created:</strong> <?php echo date('Y-m-d H:i:s'); ?></p>
            <p><strong>PHP Version:</strong> <?php echo phpversion(); ?></p>
            <p><strong>Server:</strong> <?php echo \$_SERVER['SERVER_SOFTWARE']; ?></p>
        </div>

        <div class="info">
            <h3>Database Connection Test:</h3>
            <?php
            \$conn = new mysqli('127.0.0.1', 'root', '', 'mysql', 3306, '/data/data/com.termux/files/home/hackforge/mysql.sock');
            if (\$conn->connect_error) {
                echo '<p style="color: #ff6b6b;">❌ Database connection failed: ' . \$conn->connect_error . '</p>';
            } else {
                echo '<p style="color: #00ff00;">✅ Database connection successful!</p>';
                
                // Create project database
                \$db_name = "$project_name";
                if (\$conn->query("CREATE DATABASE IF NOT EXISTS \$db_name")) {
                    echo '<p style="color: #00ff00;">✅ Project database created!</p>';
                }
                
                \$conn->close();
            }
            ?>
        </div>

        <div class="info">
            <h3>Quick Links:</h3>
            <ul>
                <li><a href="/editor.php" style="color: #48dbfb;">Online Code Editor</a></li>
                <li><a href="/phpmyadmin" style="color: #48dbfb;">phpMyAdmin</a></li>
                <li><a href="/info.php" style="color: #48dbfb;">PHP Info</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

    echo -e "${GREEN}[✓] Project '$project_name' created${NC}"
    echo -e "${BLUE}[+] Access URL: http://localhost:8080/projects/$project_name${NC}"
    echo -e "${BLUE}[+] Project directory: $project_dir${NC}"
}

# Fungsi database management
database_management() {
    echo -e "${CYAN}[+] Database Management${NC}"
    
    if ! pgrep -x "mysqld" > /dev/null; then
        echo -e "${RED}[!] MariaDB is not running${NC}"
        return
    fi
    
    echo -e "1. Create Database"
    echo -e "2. List Databases"
    echo -e "3. Execute SQL Query"
    echo -e "4. Backup Database"
    echo -e "5. Back to Main Menu"
    
    echo -e -n "${YELLOW}Choose option: ${NC}"
    read choice
    
    case $choice in
        1)
            echo -e -n "${YELLOW}Enter database name: ${NC}"
            read db_name
            mysql -u root -e "CREATE DATABASE IF NOT EXISTS \`$db_name\`;"
            echo -e "${GREEN}[✓] Database '$db_name' created${NC}"
            ;;
        2)
            echo -e "${YELLOW}Available databases:${NC}"
            mysql -u root -e "SHOW DATABASES;" | grep -v "Database\|information_schema\|mysql\|performance_schema"
            ;;
        3)
            echo -e "${YELLOW}Enter SQL query (type 'END' to execute):${NC}"
            local query=""
            local line
            while true; do
                read -r line
                if [ "$line" = "END" ]; then
                    break
                fi
                query="$query $line"
            done
            mysql -u root -e "$query"
            ;;
        4)
            local backup_file="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
            mysqldump -u root --all-databases > "$backup_file"
            echo -e "${GREEN}[✓] Backup created: $backup_file${NC}"
            ;;
        5)
            return
            ;;
        *)
            echo -e "${RED}Invalid choice!${NC}"
            ;;
    esac
}

# Fungsi main menu
main_menu() {
    while true; do
        clear
        echo -e "${MAGENTA}"
        echo "╔══════════════════════════════════════════════╗"
        echo "║                   HACKFORGE                  ║"
        echo "║         Complete Coding Environment          ║"
        echo "║                                              ║"
        echo "║     Web Server + Database + Code Editor      ║"
        echo "╚══════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        status_services
        echo -e ""
        echo -e "${CYAN}MAIN MENU:${NC}"
        echo -e "1. 🚀 INSTALL Hackforge (Full Setup)"
        echo -e "2. ⚡ START All Services"
        echo -e "3. 🛑 STOP All Services"
        echo -e "4. 📝 QUICK Coding (PHP)"
        echo -e "5. 📁 NEW Project"
        echo -e "6. 🗃️  DATABASE Management"
        echo -e "7. 🔧 SERVICE Management"
        echo -e "8. 🌐 OPEN in Browser"
        echo -e "9. ℹ️  SYSTEM Info"
        echo -e "0. ❌ EXIT"
        echo -e ""
        echo -e "${YELLOW}Choose option [0-9]: ${NC}"
        read choice
        
        case $choice in
            1)
                install_hackforge
                ;;
            2)
                start_services
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            3)
                stop_services
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            4)
                quick_coding
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            5)
                create_new_project
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            6)
                database_management
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            7)
                manage_services_menu
                ;;
            8)
                am start -a android.intent.action.VIEW -d "http://localhost:8080" 2>/dev/null &
                echo -e "${GREEN}[✓] Opening browser...${NC}"
                sleep 2
                ;;
            9)
                show_system_info
                ;;
            0)
                echo -e "${GREEN}Thank you for using Hackforge! 👋${NC}"
                stop_services
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                sleep 2
                ;;
        esac
    done
}

# Fungsi manage services menu
manage_services_menu() {
    while true; do
        clear
        echo -e "${CYAN}"
        echo "╔══════════════════════════════════════════════╗"
        echo "║              MANAGE SERVICES                 ║"
        echo "╚══════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        status_services
        echo -e ""
        echo -e "${YELLOW}MANAGEMENT OPTIONS:${NC}"
        echo -e "1. 🔄 RESTART Apache"
        echo -e "2. 🔄 RESTART MariaDB"
        echo -e "3. 📝 VIEW Apache Logs"
        echo -e "4. 📝 VIEW MariaDB Logs"
        echo -e "5. 🧹 CLEAR Logs"
        echo -e "6. 🏠 BACK to Main Menu"
        echo -e ""
        echo -e "${YELLOW}Choose option [1-6]: ${NC}"
        read choice
        
        case $choice in
            1)
                echo -e "${YELLOW}[+] Restarting Apache...${NC}"
                apachectl -k restart
                echo -e "${GREEN}[✓] Apache restarted${NC}"
                sleep 2
                ;;
            2)
                echo -e "${YELLOW}[+] Restarting MariaDB...${NC}"
                stop_services
                sleep 2
                start_services
                echo -e "${GREEN}[✓] MariaDB restarted${NC}"
                sleep 2
                ;;
            3)
                echo -e "${CYAN}[+] Apache Error Log:${NC}"
                tail -20 "/data/data/com.termux/files/usr/var/log/apache2/error.log"
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            4)
                echo -e "${CYAN}[+] MariaDB Error Log:${NC}"
                tail -20 "$LOG_DIR/mariadb.log"
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            5)
                echo -e "${YELLOW}[+] Clearing logs...${NC}"
                > "/data/data/com.termux/files/usr/var/log/apache2/error.log"
                > "/data/data/com.termux/files/usr/var/log/apache2/access.log"
                > "$LOG_DIR/mariadb.log"
                echo -e "${GREEN}[✓] Logs cleared${NC}"
                sleep 2
                ;;
            6)
                return
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                sleep 2
                ;;
        esac
    done
}

# Fungsi show system info
show_system_info() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║               SYSTEM INFORMATION             ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}System Info:${NC}"
    echo -e "  OS: $(uname -o)"
    echo -e "  Kernel: $(uname -r)"
    echo -e "  Architecture: $(uname -m)"
    
    echo -e "\n${YELLOW}Hackforge Info:${NC}"
    echo -e "  Version: 2.1.0"
    echo -e "  Install Directory: $HACKFORGE_DIR"
    echo -e "  Web Root: $WEB_ROOT"
    echo -e "  Projects: $PROJECTS_DIR"
    
    echo -e "\n${YELLOW}Installed Components:${NC}"
    echo -e "  Apache: $(apachectl -v 2>/dev/null | head -1 | cut -d' ' -f3) ✓"
    echo -e "  PHP: $(php -v 2>/dev/null | head -1 | cut -d' ' -f2) ✓"
    echo -e "  MariaDB: $(mysql --version 2>/dev/null | cut -d' ' -f5 | sed 's/,//') ✓"
    echo -e "  Node.js: $(node --version 2>/dev/null) ✓"
    echo -e "  Python: $(python --version 2>/dev/null) ✓"
    
    echo -e "\n${YELLOW}Access URLs:${NC}"
    echo -e "  Main Site: ${BLUE}http://localhost:8080${NC}"
    echo -e "  Code Editor: ${BLUE}http://localhost:8080/editor.php${NC}"
    echo -e "  phpMyAdmin: ${BLUE}http://localhost:8080/phpmyadmin${NC}"
    echo -e "  PHP Info: ${BLUE}http://localhost:8080/info.php${NC}"
    echo -e "  Projects: ${BLUE}http://localhost:8080/projects${NC}"
    
    echo -e "\n${GREEN}Press Enter to continue...${NC}"
    read
}

# Initialize Hackforge
initialize_hackforge() {
    clear
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║                   HACKFORGE                  ║"
    echo "║         Complete Coding Environment          ║"
    echo "║                                              ║"
    echo "║                 Initializing...              ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Buat direktori utama
    mkdir -p "$HACKFORGE_DIR" "$BACKUP_DIR" "$LOG_DIR" "$PROJECTS_DIR" "$CODE_EDITOR_DIR"
    
    # Check jika sudah terinstall
    if [ -f "$HACKFORGE_DIR/installed" ]; then
        echo -e "${GREEN}[✓] Hackforge detected${NC}"
        start_services
    fi
    
    echo -e "${GREEN}[✓] Hackforge initialized${NC}"
    sleep 2
}

# Main execution
initialize_hackforge
main_menu