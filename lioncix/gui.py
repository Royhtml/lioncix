import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import sys
import os
from PIL import Image, ImageTk, ImageDraw
import cv2
import queue
import time

class SpeechManager:
    """Thread-safe speech manager"""
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.is_running = False
        self.speech_thread = None
        self.engine = None
        self.voices = []
        self.speech_available = False
        
        self.init_speech_engine()
        self.start_speech_processor()
    
    def init_speech_engine(self):
        """Initialize speech engine"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
            self.speech_available = True
            
            # Set default voice to female
            self.set_voice_gender("Female")
            
        except Exception as e:
            print(f"Text-to-speech unavailable: {e}")
            self.speech_available = False
    
    def set_voice_gender(self, gender):
        """Set voice gender"""
        if not self.speech_available or not self.engine:
            return
            
        female_keywords = ["zira", "samantha", "hazel", "eva", "anna", "helen", "linda", "susan"]
        selected_voice = None
        
        for voice in self.voices:
            name = voice.name.lower()
            if gender == "Female":
                if any(keyword in name for keyword in female_keywords):
                    selected_voice = voice
                    break
            else:
                if any(keyword in name for keyword in ["david", "mark", "george"]):
                    selected_voice = voice
                    break
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice.id)
        elif self.voices:
            self.engine.setProperty('voice', self.voices[0].id)
    
    def start_speech_processor(self):
        """Start the speech processing thread"""
        if not self.speech_available:
            return
            
        self.is_running = True
        self.speech_thread = threading.Thread(target=self._speech_processor, daemon=True)
        self.speech_thread.start()
    
    def _speech_processor(self):
        """Process speech requests from queue"""
        while self.is_running:
            try:
                text = self.speech_queue.get(timeout=1)
                if text is None:  # Shutdown signal
                    break
                    
                if self.engine:
                    try:
                        self.engine.say(text)
                        self.engine.runAndWait()
                    except Exception as e:
                        print(f"Speech error in processor: {e}")
                        # Reset engine on error
                        try:
                            self.engine.stop()
                            time.sleep(0.1)
                        except:
                            pass
                        
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Speech processor error: {e}")
    
    def speak(self, text):
        """Add text to speech queue"""
        if self.speech_available and text:
            self.speech_queue.put(text)
    
    def stop(self):
        """Stop speech manager"""
        self.is_running = False
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        # Add None to break the queue get
        try:
            self.speech_queue.put(None)
        except:
            pass

class HackForgeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Lioncix HackForge")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        
        # Initialize speech manager
        self.speech_manager = SpeechManager()
        
        # Theme settings - Default to Dark with Green text
        self.current_theme = "Lioncix HackForge"
        self.custom_colors = {
            "bg": "#1a1a1a",
            "fg": "#00ff00",
            "button_bg": "#2a2a2a",
            "button_fg": "#00ff00",
            "text_bg": "#1a1a1a",
            "text_fg": "#00ff00",
            "accent": "#00ff00"
        }
        
        self.themes = {
            "Lioncix HackForge": {
                "bg": "#1a1a1a",
                "fg": "#00ff00",
                "button_bg": "#2a2a2a",
                "button_fg": "#00ff00",
                "text_bg": "#1a1a1a",
                "text_fg": "#00ff00",
                "accent": "#00ff00"
            },
            "Light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "button_bg": "#f0f0f0",
                "button_fg": "#000000",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "accent": "#007acc"
            },
            "Dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "button_bg": "#3c3c3c",
                "button_fg": "#ffffff",
                "text_bg": "#1e1e1e",
                "text_fg": "#ffffff",
                "accent": "#007acc"
            }
        }
        
        try:
            # Create a simple hacker-style icon programmatically
            self.create_hacker_icon()
            icon_path = "hackforge_icon.ico"
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARNING] Gagal load icon: {e}")

        self.process = None
        self.is_running = False
        self.video_capture = None
        self.terminal_process = None

        # Default language
        self.current_language = "English"
        self.languages = {
            "English": self.english_texts(),
            "Chinese": self.chinese_texts(),
            "Japanese": self.japanese_texts(),
            "Russian": self.russian_texts(),
            "Jawa": self.jawa_texts()
        }

        # Find main Python script
        self.script_path = self.find_main_script()

        # Setup UI
        self.setup_ui()
        self.update_ui_text()
        self.apply_theme()

        # Start video playback if available
        self.setup_video()

        # Welcome
        self.play_welcome_speech()
        
        # Auto-run script on startup
        self.root.after(1000, self.auto_start_script)

    def create_hacker_icon(self):
        """Create a hacker-style icon programmatically"""
        try:
            # Create a 64x64 icon with matrix/hacker style
            size = (64, 64)
            img = Image.new('RGB', size, color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Draw some green lines/code-like patterns
            for i in range(0, 64, 8):
                draw.line([(i, 0), (i, 64)], fill='#00ff00', width=1)
                draw.line([(0, i), (64, i)], fill='#00ff00', width=1)
            
            # Draw a central "H" for HackForge
            draw.rectangle([24, 16, 28, 48], fill='#00ff00')  # Left vertical
            draw.rectangle([36, 16, 40, 48], fill='#00ff00')  # Right vertical
            draw.rectangle([24, 30, 40, 34], fill='#00ff00')  # Horizontal
            
            # Save as ICO
            img.save('hackforge_icon.ico', format='ICO')
            
        except Exception as e:
            print(f"Icon creation failed: {e}")

    def speak_text(self, text):
        """Speak text using thread-safe speech manager"""
        if text:
            self.speech_manager.speak(text)

    def setup_video(self):
        """Tampilkan gambar sebagai pengganti video intro"""
        image_path = r"C:\Users\User\Downloads\lioncix\lioncix\hackforge\lion.png"

        if os.path.exists(image_path):
            try:
                image = cv2.imread(image_path)
                if image is not None:
                    # Konversi BGR->RGB
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Convert ke PIL
                    img = Image.fromarray(image)
                    img = img.resize((800, 450))  # Atur ukuran sesuai kebutuhan

                    # Convert ke ImageTk
                    self.photo = ImageTk.PhotoImage(img)

                    # Tampilkan ke label/frame
                    self.video_label.configure(image=self.photo)
                    self.video_label.image = self.photo

                else:
                    print("[WARNING] Tidak bisa membuka gambar, memanggil fallback.")
                    self.load_image_fallback()

            except Exception as e:
                print(f"[WARNING] Gagal load gambar: {e}")
                self.load_image_fallback()

        else:
            print("[WARNING] File gambar tidak ditemukan, memanggil fallback.")
            self.load_image_fallback()


    def load_image_fallback(self):
        """Load fallback image if video is not available"""
        try:
            # Create a hacker-style fallback image
            img = Image.new('RGB', (390, 250), color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Draw hacker-style text and patterns
            draw.rectangle([10, 10, 380, 240], outline='#00ff00', width=2)
            
            # Draw matrix-style falling code
            for i in range(0, 380, 20):
                for j in range(0, 250, 20):
                    if (i + j) % 40 == 0:
                        draw.text((i, j), "1", fill='#00ff00')
                    elif (i + j) % 40 == 20:
                        draw.text((i, j), "0", fill='#00ff00')
            
            # Draw HackForge text
            draw.text((120, 110), "HACKFORGE", fill='#00ff00', font=None)
            draw.text((140, 130), "LAUNCHER", fill='#00ff00', font=None)
            
            self.fallback_photo = ImageTk.PhotoImage(img)
            if hasattr(self, 'video_label'):
                self.video_label.config(image=self.fallback_photo)
        except Exception as e:
            print(f"[WARNING] Gagal load fallback image: {e}")

    def update_video_frame(self):
        """Update video frame continuously"""
        if self.video_capture and hasattr(self, 'video_label'):
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (390, 250))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
                
                self.root.after(30, self.update_video_frame)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.root.after(30, self.update_video_frame)

    # ============ THEME MANAGEMENT ==============
    def apply_theme(self):
        """Apply current theme to all widgets"""
        theme = self.themes[self.current_theme]
        
        style = ttk.Style()
        
        # Always use dark theme as base for HackForge
        style.theme_use('clam')
        style.configure(".", 
                      background=theme["bg"],
                      foreground=theme["fg"],
                      fieldbackground=theme["text_bg"])
        
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("TButton", 
                      background=theme["button_bg"], 
                      foreground=theme["button_fg"])
        style.configure("TCombobox", 
                      fieldbackground=theme["text_bg"],
                      background=theme["button_bg"],
                      foreground=theme["fg"])
        style.configure("TLabelframe", 
                      background=theme["bg"],
                      foreground=theme["fg"])
        style.configure("TLabelframe.Label", 
                      background=theme["bg"],
                      foreground=theme["fg"])

        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            self.apply_theme_to_widget(widget, theme)
        
        self.log_text.config(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["fg"]
        )
        
        if hasattr(self, 'canvas'):
            self.canvas.config(bg=theme["bg"])

    def apply_theme_to_widget(self, widget, theme):
        """Recursively apply theme to widget and its children"""
        try:
            if isinstance(widget, (tk.Frame, ttk.Frame)):
                widget.configure(style="TFrame")
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=theme["text_bg"], fg=theme["fg"], 
                               insertbackground=theme["fg"])
            elif isinstance(widget, tk.Text):
                widget.configure(bg=theme["text_bg"], fg=theme["fg"],
                               insertbackground=theme["fg"])
            elif isinstance(widget, tk.Canvas):
                widget.configure(bg=theme["bg"])
            
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, theme)
        except:
            pass

    # ============ LANGUAGE PACKS ==============
    def english_texts(self):
        return {
            "title": "Lioncix HackForge Launcher",
            "script": "Script:",
            "run": "Run Script",
            "stop": "Stop Script",
            "log": "Terminal Output",
            "status_ready": "Ready",
            "language": "Language:",
            "theme": "Theme:",
            "customize": "Customize",
            "welcome_speech": "Welcome to Lioncix HackForge Launcher",
            "start_speech": "Starting Python Script",
            "stop_speech": "Stopping Python Script",
            "open_terminal": "💻 Open Terminal"
        }

    def chinese_texts(self):
        return {
            "title": "Lioncix HackForge 启动器",
            "script": "脚本:",
            "run": "运行脚本",
            "stop": "停止脚本",
            "log": "终端输出",
            "status_ready": "准备就绪",
            "language": "语言:",
            "theme": "主题:",
            "customize": "自定义",
            "welcome_speech": "欢迎使用 Lioncix HackForge 启动器",
            "start_speech": "正在启动 Python 脚本",
            "stop_speech": "正在停止 Python 脚本",
            "open_terminal": "💻 打开终端"
        }

    def japanese_texts(self):
        return {
            "title": "Lioncix HackForge ランチャー",
            "script": "スクリプト:",
            "run": "スクリプト実行",
            "stop": "スクリプト停止",
            "log": "ターミナル出力",
            "status_ready": "準備完了",
            "language": "言語:",
            "theme": "テーマ:",
            "customize": "カスタマイズ",
            "welcome_speech": "ハックフォージランチャーへようこそ",
            "start_speech": "Pythonスクリプトを起動しています",
            "stop_speech": "Pythonスクリプトを停止しています",
            "open_terminal": "💻 ターミナルを開く"
        }
        
    def russian_texts(self):
        return {
            "title": "Lioncix HackForge Launcher",
            "script": "Скрипт:",
            "run": "Запустить скрипт",
            "stop": "Остановить скрипт",
            "log": "Вывод терминала",
            "status_ready": "Готово",
            "language": "Язык:",
            "theme": "Тема:",
            "customize": "Настроить",
            "welcome_speech": "Добро пожаловать в Lioncix HackForge Launcher",
            "start_speech": "Запуск Python скрипта",
            "stop_speech": "Остановка Python скрипта",
            "open_terminal": "💻 Открыть терминал"
        }
        
    def jawa_texts(self):
        return {
            "title": "Lioncix HackForge Launcher",
            "script": "Script:",
            "run": "Jalankan Script",
            "stop": "Stop Script",
            "log": "Output Terminal",
            "status_ready": "Siap",
            "language": "Basa:",
            "theme": "Tema:",
            "customize": "Sesuaikan",
            "welcome_speech": "Sugeng Rawuh ing Lioncix HackForge Launcher",
            "start_speech": "Miwiti Script Python",
            "stop_speech": "Script Python Mungkasi",
            "open_terminal": "💻 Bukak Terminal"
        }

    def find_main_script(self):
        base_dir = r"C:\Users\User\Downloads\lioncix\lioncix"
        main_path = os.path.join(base_dir, "mainpy.py")
        server_path = os.path.join(base_dir, "server.py")
        app_path = os.path.join(base_dir, "app.py")

        if os.path.exists(main_path):
            return os.path.abspath(main_path)
        elif os.path.exists(server_path):
            return os.path.abspath(server_path)
        elif os.path.exists(app_path):
            return os.path.abspath(app_path)
        else:
            # Create a simple demo script if none exists
            demo_script = os.path.join(base_dir, "demo.py")
            with open(demo_script, 'w') as f:
                f.write('''#!/usr/bin/env python3
print("HackForge Demo Script")
print("=" * 30)
print("Script is running successfully!")
print("This is a terminal-based Python application.")
input("Press Enter to exit...")
''')
            return os.path.abspath(demo_script)

    # ============ UI ==============
    def setup_ui(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        for i in range(8):
            self.main_frame.rowconfigure(i, weight=0)
        self.main_frame.rowconfigure(7, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Title
        self.title_label = ttk.Label(self.main_frame, font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, pady=5, sticky="n")

        # Language
        lang_frame = ttk.Frame(self.main_frame)
        lang_frame.grid(row=1, column=0, sticky="ew", pady=5)
        lang_frame.columnconfigure(1, weight=1)
        ttk.Label(lang_frame, text="Language:").grid(row=0, column=0, sticky="w")
        self.lang_var = tk.StringVar(value=self.current_language)
        lang_combo = ttk.Combobox(
            lang_frame, textvariable=self.lang_var,
            values=list(self.languages.keys()), state="readonly"
        )
        lang_combo.grid(row=0, column=1, sticky="ew")
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        # Theme Selector
        theme_frame = ttk.Frame(self.main_frame)
        theme_frame.grid(row=2, column=0, sticky="ew", pady=5)
        theme_frame.columnconfigure(1, weight=1)
        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky="w")
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(
            theme_frame, textvariable=self.theme_var,
            values=list(self.themes.keys()), state="readonly"
        )
        theme_combo.grid(row=0, column=1, sticky="ew")
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Video/Image Frame
        video_frame = ttk.Frame(self.main_frame, relief="solid", borderwidth=1)
        video_frame.grid(row=3, column=0, pady=10, sticky="n")
        self.video_label = ttk.Label(video_frame)
        self.video_label.grid(row=0, column=0)

        # Script path display
        script_frame = ttk.Frame(self.main_frame)
        script_frame.grid(row=4, column=0, sticky="ew", pady=5)
        script_frame.columnconfigure(0, weight=1)
        
        ttk.Label(script_frame, text="Script:").grid(row=0, column=0, sticky="w")
        
        # Script path with scrollbar
        script_path_frame = ttk.Frame(script_frame)
        script_path_frame.grid(row=1, column=0, sticky="ew", pady=2)
        script_path_frame.columnconfigure(0, weight=1)
        
        self.script_var = tk.StringVar(value=self.script_path)
        script_entry = ttk.Entry(script_path_frame, textvariable=self.script_var, state="readonly")
        script_entry.grid(row=0, column=0, sticky="ew")
        
        # Browse button for script
        browse_btn = ttk.Button(
            script_path_frame, 
            text="📁", 
            width=3,
            command=self.browse_script
        )
        browse_btn.grid(row=0, column=1, padx=(5, 0))

        # Main Control Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2), weight=1)
        
        self.start_btn = ttk.Button(
            button_frame, 
            command=self.start_server
        )
        self.start_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        self.stop_btn = ttk.Button(
            button_frame, 
            command=self.stop_server, 
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        # Open terminal button
        self.terminal_btn = ttk.Button(
            button_frame,
            command=self.open_terminal
        )
        self.terminal_btn.grid(row=0, column=2, padx=2, sticky="ew")

        # Log
        log_frame = ttk.LabelFrame(self.main_frame, text="Terminal Output", padding=5)
        log_frame.grid(row=7, column=0, sticky="nsew", pady=5)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.config(state=tk.DISABLED)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor="w")
        status_bar.grid(row=8, column=0, sticky="ew")

    def browse_script(self):
        """Browse for Python script"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            self.script_path = file_path
            self.script_var.set(file_path)

    def change_theme(self, event=None):
        self.current_theme = self.theme_var.get()
        self.apply_theme()

    def update_ui_text(self):
        texts = self.languages[self.current_language]
        self.root.title(texts["title"])
        self.title_label.config(text=texts["title"])
        self.start_btn.config(text=texts["run"])
        self.stop_btn.config(text=texts["stop"])
        self.terminal_btn.config(text=texts["open_terminal"])
        self.log_text.master.master.config(text=texts["log"])
        self.status_var.set(texts["status_ready"])

    # ============ EVENTS ==============
    def change_language(self, event):
        self.current_language = self.lang_var.get()
        self.update_ui_text()

    def play_welcome_speech(self):
        self.speak_text(self.languages[self.current_language]["welcome_speech"])

    def play_start_speech(self):
        self.speak_text(self.languages[self.current_language]["start_speech"])

    def play_stop_speech(self):
        self.speak_text(self.languages[self.current_language]["stop_speech"])

    def open_terminal_and_run_script(self):
        """Open terminal and automatically run python main.py"""
        script_dir = os.path.dirname(self.script_path)
        script_name = os.path.basename(self.script_path)
        
        try:
            if os.name == 'nt':  # Windows
                # Open command prompt and automatically run the script
                command = f'cmd /K "cd /d "{script_dir}" && python {script_name} && echo. && echo Script execution completed. && echo Press any key to close... && pause >nul"'
                self.terminal_process = subprocess.Popen(command, shell=True)
                
            elif sys.platform == 'darwin':  # macOS
                # For macOS, use AppleScript to open Terminal and run command
                command = f'cd "{script_dir}" && python3 {script_name}'
                applescript = f'''
                tell application "Terminal"
                    do script "{command}"
                    activate
                end tell
                '''
                self.terminal_process = subprocess.Popen(['osascript', '-e', applescript])
                
            else:  # Linux
                # For Linux, use gnome-terminal or similar
                command = f'cd "{script_dir}" && python3 {script_name} && echo "Script execution completed." && read -p "Press Enter to close..."'
                self.terminal_process = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
                
            self.log_message(f"Opened terminal and running: python {script_name}")
            self.status_var.set(f"Running in terminal: {script_name}")
            
        except Exception as e:
            error_msg = f"Failed to open terminal: {e}"
            messagebox.showerror("Error", error_msg)
            self.log_message(error_msg)

    def open_terminal(self):
        """Open terminal to script directory without running script"""
        script_dir = os.path.dirname(self.script_path)
        try:
            if os.name == 'nt':  # Windows
                # Open command prompt in the script directory
                subprocess.Popen(f'cmd /K "cd /d "{script_dir}" && echo HackForge Terminal && echo Script: {os.path.basename(self.script_path)}"', 
                               shell=True)
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', '-a', 'Terminal', script_dir])
            else:  # Linux
                subprocess.Popen(['gnome-terminal', '--working-directory', script_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")

    def auto_start_script(self):
        """Automatically start the script on application launch by opening terminal"""
        if not self.is_running:
            self.log_message("Auto-starting script in terminal...")
            self.open_terminal_and_run_script()
            # Update UI to reflect running state
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set(f"Running in terminal: {os.path.basename(self.script_path)}")

    # ============ SCRIPT CONTROL ==============
    def start_server(self):
        """Start script by opening terminal and running it"""
        filename = self.script_path
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File '{filename}' not found")
            return
            
        self.play_start_speech()
        self.open_terminal_and_run_script()
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Running in terminal: {os.path.basename(filename)}")
        self.log_message(f"Starting Python script in terminal: {filename}")
        self.log_message("=" * 50)

    def run_python_script(self, filename):
        """Legacy method - kept for compatibility"""
        try:
            # Set environment to use UTF-8 encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # Run Python script directly and capture output
            self.process = subprocess.Popen(
                [sys.executable, '-X', 'utf8', filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace",
                env=env
            )
            
            # Read output in real-time
            for line in iter(self.process.stdout.readline, ''):
                if not self.is_running:
                    break
                self.log_message(line.strip())
                
            self.process.stdout.close()
            return_code = self.process.wait()
            
            if return_code == 0:
                self.log_message("Script finished successfully.")
            else:
                self.log_message(f"Script exited with code: {return_code}")
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.log_message(f"Error: {str(e)}")
        finally:
            self.root.after(0, self.script_finished)

    def script_finished(self):
        """Called when script finishes execution"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set(self.languages[self.current_language]["status_ready"])

    def log_message(self, message):
        def update():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self.root.after(0, update)

    def stop_server(self):
        """Stop the script and terminal"""
        self.play_stop_speech()
        
        # Try to stop the terminal process
        if self.terminal_process:
            try:
                if os.name == "nt":
                    # Windows - terminate the process tree
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(self.terminal_process.pid)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                else:
                    # Unix-like systems
                    self.terminal_process.terminate()
                self.terminal_process = None
                self.log_message("Terminal and script stopped by user")
            except Exception as e:
                self.status_var.set(f"Error stopping: {e}")
                self.log_message(f"Error stopping terminal: {e}")
        
        # Also stop any direct process
        if self.process:
            try:
                self.is_running = False
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(self.process.pid)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                else:
                    import signal
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process = None
                self.log_message("Script stopped by user")
            except Exception as e:
                self.status_var.set(f"Error stopping: {e}")
                self.log_message(f"Error stopping: {e}")
        
        self.script_finished()

    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_server()
        if self.speech_manager:
            self.speech_manager.stop()
        if self.video_capture:
            self.video_capture.release()
        self.root.quit()
        self.root.destroy()

def run_gui():
    root = tk.Tk()
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(f"Warning: DPI awareness setting failed: {e}")

    app = HackForgeLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


def run_cli():
    run_gui()


if __name__ == "__main__":
    run_gui()
