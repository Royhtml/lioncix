import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, colorchooser
import subprocess
import threading
import sys
import os
from PIL import Image, ImageTk, ImageDraw
import cv2
from tkinter import Frame
import pystray
from pystray import MenuItem as item
import webbrowser
import requests
import base64
from io import BytesIO

class HackForgeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("HackForge Launcher")
        self.root.geometry("400x610")
        self.root.resizable(False, False)
        
        # System tray variables
        self.tray_icon = None
        self.tray_running = False
        self.is_hidden = False
        
        # Drawing functionality variables
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.draw_color = "black"
        self.line_width = 3
        self.drawing_enabled = False
        
        # Theme settings - Default to Dark with Green text
        self.current_theme = "HackForge Dark"
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
            "HackForge Dark": {
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
            },
            "Blue": {
                "bg": "#f0f8ff",
                "fg": "#000000",
                "button_bg": "#007acc",
                "button_fg": "#ffffff",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "accent": "#007acc"
            },
            "Green": {
                "bg": "#f0fff0",
                "fg": "#000000",
                "button_bg": "#28a745",
                "button_fg": "#ffffff",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "accent": "#28a745"
            },
            "Custom": self.custom_colors.copy()
        }
        
        # Load icons for tray and buttons
        self.load_icons()
        
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

        # Init speech
        self.setup_speech()

        # Default language
        self.current_language = "English"
        self.languages = {
            "English": self.english_texts(),
            "Chinese": self.chinese_texts(),
            "Japanese": self.japanese_texts(),
            "Russian": self.russian_texts(),
            "Jawa": self.jawa_texts()
        }

        # Selalu pakai Female Voice
        self.voice_gender = "Female"
        self.set_voice_gender("Female")

        # Find main Python script
        self.script_path = self.find_main_script()

        # Setup UI
        self.setup_ui()
        self.update_ui_text()
        self.apply_theme()

        # Start video playback if available
        self.setup_video()

        # Setup system tray
        self.setup_system_tray()

        # Welcome
        self.play_welcome_speech()

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

    def setup_speech(self):
        """Setup text-to-speech functionality"""
        try:
            import pyttsx3
            self.client = pyttsx3.init()
            self.voices = self.client.getProperty("voices")
            self.speech_available = True
            self.set_voice_gender("Female")
        except Exception as e:
            print(f"Text-to-speech unavailable: {e}")
            self.client = None
            self.voices = []
            self.speech_available = False

    def set_voice_gender(self, gender):
        """Set voice gender for text-to-speech"""
        if not self.speech_available:
            return

        self.voice_gender = gender
        female_keywords = ["zira", "samantha", "hazel", "eva", "anna", "helen", "linda", "susan"]

        selected_voice = None
        for voice in self.voices:
            name = voice.name.lower()
            if gender == "Female":
                if any(key in name for key in female_keywords):
                    selected_voice = voice
                    break
            else:
                if "david" in name or "mark" in name or "george" in name:
                    selected_voice = voice
                    break

        if selected_voice:
            self.client.setProperty("voice", selected_voice.id)
        else:
            self.client.setProperty("voice", self.voices[0].id)

    def speak_text(self, text):
        """Speak text using text-to-speech"""
        if self.speech_available and self.client:
            def speak():
                try:
                    self.set_voice_gender("Female")
                    self.client.say(text)
                    self.client.runAndWait()
                except Exception as e:
                    print("Speech error:", e)
            threading.Thread(target=speak, daemon=True).start()

    def load_icons(self):
        """Load icons for tray and buttons"""
        try:
            # Create simple icons programmatically if files don't exist
            self.create_icons()
            
            # Tray icons
            self.tray_icon_running = Image.open("tray_running.ico")
            self.tray_icon_stopped = Image.open("tray_stopped.ico")
            
            # Button icons (resized for buttons)
            self.start_icon = ImageTk.PhotoImage(Image.open("start_icon.png").resize((16, 16), Image.LANCZOS))
            self.stop_icon = ImageTk.PhotoImage(Image.open("stop_icon.png").resize((16, 16), Image.LANCZOS))
            self.hide_icon = ImageTk.PhotoImage(Image.open("hide_icon.png").resize((16, 16), Image.LANCZOS))
            self.drawing_icon = ImageTk.PhotoImage(Image.open("drawing_icon.png").resize((16, 16), Image.LANCZOS))
            self.remove_bg_icon = ImageTk.PhotoImage(Image.open("remove_bg_icon.png").resize((16, 16), Image.LANCZOS))
            self.developer_icon = ImageTk.PhotoImage(Image.open("developer_icon.png").resize((16, 16), Image.LANCZOS))
            self.theme_icon = ImageTk.PhotoImage(Image.open("theme_icon.png").resize((16, 16), Image.LANCZOS))
            
        except Exception as e:
            print(f"[WARNING] Gagal load icons: {e}")
            # Use default icons if custom icons fail to load
            self.start_icon = None
            self.stop_icon = None
            self.hide_icon = None
            self.drawing_icon = None
            self.remove_bg_icon = None
            self.developer_icon = None
            self.theme_icon = None

    def create_icons(self):
        """Create default icons if they don't exist"""
        icons_to_create = {
            "tray_running.ico": (64, 64, "#00ff00"),  # Green for running
            "tray_stopped.ico": (64, 64, "#ff0000"),  # Red for stopped
            "start_icon.png": (32, 32, "#00ff00"),    # Green start
            "stop_icon.png": (32, 32, "#ff0000"),     # Red stop
            "hide_icon.png": (32, 32, "#007acc"),     # Blue hide
            "drawing_icon.png": (32, 32, "#ff9900"),  # Orange for drawing
            "remove_bg_icon.png": (32, 32, "#ff66cc"), # Pink for remove bg
            "developer_icon.png": (32, 32, "#9933ff"), # Purple for developer
            "theme_icon.png": (32, 32, "#ffcc00")     # Yellow for theme
        }
        
        for filename, (width, height, color) in icons_to_create.items():
            if not os.path.exists(filename):
                # Create a simple colored circle icon
                img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Draw circle
                draw.ellipse([5, 5, width-5, height-5], fill=color)
                
                # Save
                if filename.endswith('.ico'):
                    img.save(filename, format='ICO')
                else:
                    img.save(filename, format='PNG')

    def setup_system_tray(self):
        """Setup system tray icon"""
        try:
            # Create tray menu
            menu = (
                item('Show/Hide', self.toggle_window),
                item('Run Script', self.start_server_from_tray),
                item('Stop Script', self.stop_server_from_tray),
                item('Open Terminal', self.open_terminal),
                item('Exit', self.quit_application)
            )
            
            # Create tray icon
            self.tray_icon = pystray.Icon(
                "hackforge_launcher",
                self.tray_icon_stopped,
                "HackForge Launcher",
                menu
            )
            
            # Start tray in separate thread
            self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            self.tray_thread.start()
            self.tray_running = True
            
        except Exception as e:
            print(f"[WARNING] Gagal setup system tray: {e}")

    def update_tray_icon(self, running=False):
        """Update tray icon based on server status"""
        if self.tray_icon:
            if running:
                self.tray_icon.icon = self.tray_icon_running
                self.tray_icon.title = "HackForge Launcher (Running)"
            else:
                self.tray_icon.icon = self.tray_icon_stopped
                self.tray_icon.title = "HackForge Launcher (Stopped)"

    def toggle_window(self, icon=None, item=None):
        """Show/hide main window"""
        if self.is_hidden:
            self.root.deiconify()
            self.root.attributes('-topmost', True)
            self.root.after_idle(lambda: self.root.attributes('-topmost', False))
            self.is_hidden = False
        else:
            self.root.withdraw()
            self.is_hidden = True

    def start_server_from_tray(self, icon=None, item=None):
        """Start server from tray menu"""
        if not self.is_running:
            self.root.after(0, self.start_server)

    def stop_server_from_tray(self, icon=None, item=None):
        """Stop server from tray menu"""
        if self.is_running:
            self.root.after(0, self.stop_server)

    def open_terminal(self, icon=None, item=None):
        """Open terminal to script directory"""
        script_dir = os.path.dirname(self.script_path)
        try:
            if os.name == 'nt':  # Windows
                os.startfile(script_dir)
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', script_dir])
            else:  # Linux
                subprocess.Popen(['xdg-open', script_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")

    def quit_application(self, icon=None, item=None):
        """Quit application from tray"""
        if self.is_running:
            self.stop_server()
        self.tray_icon.stop()
        self.root.quit()

    # ============ DRAWING POPUP WINDOW ==============
    def open_drawing_popup(self):
        """Open drawing in a popup window"""
        drawing_window = tk.Toplevel(self.root)
        drawing_window.title("HackForge Drawing Canvas")
        drawing_window.geometry("800x600")
        drawing_window.minsize(600, 400)
        drawing_window.transient(self.root)
        drawing_window.grab_set()
        
        try:
            icon_path = "hackforge_icon.ico"
            if os.path.exists(icon_path):
                drawing_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARNING] Gagal load icon: {e}")
        
        # Apply theme to popup
        theme = self.themes[self.current_theme]
        drawing_window.configure(bg=theme["bg"])
        
        # Main frame
        main_frame = ttk.Frame(drawing_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=5)
        controls_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Color selection
        color_btn = ttk.Button(
            controls_frame, 
            text="🌈 Color", 
            command=lambda: self.choose_draw_color_popup(drawing_canvas)
        )
        color_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        # Line width
        width_frame = ttk.Frame(controls_frame)
        width_frame.grid(row=0, column=1, padx=2, sticky="ew")
        ttk.Label(width_frame, text="Size:").pack(side=tk.LEFT)
        width_var = tk.IntVar(value=3)
        width_spin = ttk.Spinbox(width_frame, from_=1, to=20, width=5, textvariable=width_var)
        width_spin.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Eraser button
        eraser_btn = ttk.Button(
            controls_frame, 
            text="📝 Eraser", 
            command=lambda: self.activate_eraser_popup(drawing_canvas)
        )
        eraser_btn.grid(row=0, column=2, padx=2, sticky="ew")
        
        # Clear button
        clear_btn = ttk.Button(
            controls_frame, 
            text="🧹 Clear All", 
            command=lambda: self.clear_canvas_popup(drawing_canvas)
        )
        clear_btn.grid(row=0, column=3, padx=2, sticky="ew")
        
        # Save button
        save_btn = ttk.Button(
            controls_frame, 
            text="💾 Save", 
            command=lambda: self.save_drawing(drawing_canvas)
        )
        save_btn.grid(row=0, column=4, padx=2, sticky="ew")
        
        # Close button
        close_btn = ttk.Button(
            controls_frame, 
            text="❌ Close", 
            command=drawing_window.destroy
        )
        close_btn.grid(row=0, column=5, padx=2, sticky="ew")
        
        # Drawing canvas
        canvas_frame = ttk.Frame(main_frame, relief="solid", borderwidth=1)
        canvas_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        
        # Create canvas with black background for hacker theme
        drawing_canvas = tk.Canvas(
            canvas_frame, 
            bg="black",
            width=760, 
            height=500,
            cursor="pencil"
        )
        drawing_canvas.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        # Scrollbars for canvas
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=drawing_canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=drawing_canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        drawing_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Initialize drawing for popup
        self.setup_drawing_for_popup(drawing_canvas, width_var)
        
        # Bind events
        drawing_canvas.bind("<Configure>", lambda e: drawing_canvas.configure(scrollregion=drawing_canvas.bbox("all")))

    def setup_drawing_for_popup(self, canvas, width_var):
        """Setup drawing functionality for popup canvas"""
        canvas.drawing_data = {
            "drawing": False,
            "last_x": None,
            "last_y": None,
            "color": "#00ff00",  # Default green for hacker theme
            "tool": "pen"
        }
        
        def start_draw(event):
            canvas.drawing_data["drawing"] = True
            canvas.drawing_data["last_x"] = canvas.canvasx(event.x)
            canvas.drawing_data["last_y"] = canvas.canvasy(event.y)
        
        def draw(event):
            if canvas.drawing_data["drawing"]:
                x = canvas.canvasx(event.x)
                y = canvas.canvasy(event.y)
                
                if canvas.drawing_data["last_x"] and canvas.drawing_data["last_y"]:
                    if canvas.drawing_data["tool"] == "pen":
                        # Draw with pen
                        canvas.create_line(
                            canvas.drawing_data["last_x"], canvas.drawing_data["last_y"], x, y,
                            width=width_var.get(), fill=canvas.drawing_data["color"],
                            capstyle=tk.ROUND, smooth=True
                        )
                    elif canvas.drawing_data["tool"] == "eraser":
                        # Erase with black color
                        canvas.create_line(
                            canvas.drawing_data["last_x"], canvas.drawing_data["last_y"], x, y,
                            width=width_var.get() * 3, fill="black",
                            capstyle=tk.ROUND, smooth=True
                        )
                
                canvas.drawing_data["last_x"] = x
                canvas.drawing_data["last_y"] = y
        
        def stop_draw(event):
            canvas.drawing_data["drawing"] = False
            canvas.drawing_data["last_x"] = None
            canvas.drawing_data["last_y"] = None
        
        # Bind events
        canvas.bind("<Button-1>", start_draw)
        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<ButtonRelease-1>", stop_draw)

    def choose_draw_color_popup(self, canvas):
        """Choose drawing color for popup"""
        color = colorchooser.askcolor(title="Choose drawing color", initialcolor=canvas.drawing_data["color"])
        if color[1]:
            canvas.drawing_data["color"] = color[1]
            canvas.drawing_data["tool"] = "pen"
            canvas.config(cursor="pencil")

    def activate_eraser_popup(self, canvas):
        """Activate eraser tool for popup"""
        canvas.drawing_data["tool"] = "eraser"
        canvas.config(cursor="circle")

    def clear_canvas_popup(self, canvas):
        """Clear the popup canvas"""
        canvas.delete("all")

    def save_drawing(self, canvas):
        """Save drawing to file"""
        try:
            # Create image from canvas
            x = self.root.winfo_rootx() + canvas.winfo_x()
            y = self.root.winfo_rooty() + canvas.winfo_y()
            x1 = x + canvas.winfo_width()
            y1 = y + canvas.winfo_height()
            
            from PIL import ImageGrab
            image = ImageGrab.grab().crop((x, y, x1, y1))
            
            # Save file
            filename = f"hackforge_drawing_{threading.get_ident()}.png"
            image.save(filename)
            messagebox.showinfo("Success", f"Drawing saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save drawing: {e}")

    # ============ REMOVE.BG POPUP ==============
    def open_remove_bg_popup(self):
        """Open remove.bg tool in a popup window"""
        remove_bg_window = tk.Toplevel(self.root)
        remove_bg_window.title("HackForge - Remove Background Tool")
        remove_bg_window.geometry("400x500")
        remove_bg_window.minsize(400, 500)
        remove_bg_window.transient(self.root)
        remove_bg_window.grab_set()
        try:
            icon_path = "hackforge_icon.ico"
            if os.path.exists(icon_path):
                remove_bg_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARNING] Gagal load icon: {e}")
        
        # Apply theme
        theme = self.themes[self.current_theme]
        remove_bg_window.configure(bg=theme["bg"])
        
        # Main frame
        main_frame = ttk.Frame(remove_bg_window, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title with icon
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title_frame.columnconfigure(1, weight=1)
        
        if self.remove_bg_icon:
            icon_label = ttk.Label(title_frame, image=self.remove_bg_icon)
            icon_label.grid(row=0, column=0, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Remove Background", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=1, sticky="w")
        
        # API Key frame (hidden - using predefined key)
        self.remove_bg_api_key = "xQH5KznYiupRrywK5yPcjeyi"
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, sticky="ew", pady=10)
        controls_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Load image button
        load_btn = ttk.Button(
            controls_frame,
            text="📁 Load Image",
            command=lambda: self.load_image_for_remove_bg(remove_bg_window)
        )
        load_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        # Process button
        process_btn = ttk.Button(
            controls_frame,
            text="✨ Remove BG",
            command=self.process_remove_bg
        )
        process_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        # Save button
        save_btn = ttk.Button(
            controls_frame,
            text="💾 Save",
            command=self.save_remove_bg_result
        )
        save_btn.grid(row=0, column=2, padx=2, sticky="ew")
        
        # Image display frame
        image_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding=10)
        image_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        image_frame.rowconfigure(0, weight=1)
        image_frame.columnconfigure((0, 1), weight=1)
        
        # Original image
        orig_frame = ttk.Frame(image_frame)
        orig_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        ttk.Label(orig_frame, text="Original", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        self.original_image_label = ttk.Label(orig_frame, background="#f0f0f0", relief="solid", borderwidth=1)
        self.original_image_label.pack(fill=tk.BOTH, expand=True)
        
        # Processed image
        proc_frame = ttk.Frame(image_frame)
        proc_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        ttk.Label(proc_frame, text="Processed", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        self.processed_image_label = ttk.Label(proc_frame, background="#f0f0f0", relief="solid", borderwidth=1)
        self.processed_image_label.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky="ew", pady=10)
        self.remove_bg_status = tk.StringVar(value="Load an image to begin")
        status_label = ttk.Label(status_frame, textvariable=self.remove_bg_status, font=("Arial", 9))
        status_label.pack()
        
        # Configure weights for responsive layout
        main_frame.rowconfigure(2, weight=1)
        image_frame.rowconfigure(0, weight=1)
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        
        # Store instance variables
        self.remove_bg_window = remove_bg_window
        self.remove_bg_original_image = None
        self.remove_bg_processed_image = None

    def load_image_for_remove_bg(self, parent):
        """Load image for remove.bg processing"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                # Load and display original image
                image = Image.open(file_path)
                # Resize for display
                display_size = (150, 150)
                image.thumbnail(display_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.original_image_label.configure(image=photo)
                self.original_image_label.image = photo
                self.remove_bg_original_image = file_path
                self.remove_bg_status.set("✓ Image loaded successfully")
                
                # Clear previous result
                self.processed_image_label.configure(image='')
                self.remove_bg_processed_image = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def process_remove_bg(self):
        """Process image with remove.bg API"""
        if not self.remove_bg_original_image:
            messagebox.showerror("Error", "Please load an image first")
            return
            
        try:
            self.remove_bg_status.set("🔄 Processing image...")
            self.remove_bg_window.update()
            
            # Call remove.bg API
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(self.remove_bg_original_image, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': self.remove_bg_api_key},
            )
            
            if response.status_code == requests.codes.ok:
                # Save processed image
                self.remove_bg_processed_image = "hackforge_removed_bg.png"
                with open(self.remove_bg_processed_image, 'wb') as out:
                    out.write(response.content)
                
                # Display processed image
                image = Image.open(self.remove_bg_processed_image)
                display_size = (150, 150)
                image.thumbnail(display_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.processed_image_label.configure(image=photo)
                self.processed_image_label.image = photo
                self.remove_bg_status.set("✓ Background removed successfully!")
                
            else:
                error_msg = f"API Error: {response.status_code}"
                if response.status_code == 402:
                    error_msg += " - Invalid API key or quota exceeded"
                elif response.status_code == 400:
                    error_msg += " - Invalid image format"
                elif response.status_code == 403:
                    error_msg += " - Access denied"
                    
                messagebox.showerror("Error", error_msg)
                self.remove_bg_status.set("❌ Processing failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")
            self.remove_bg_status.set("❌ Processing failed")

    def save_remove_bg_result(self):
        """Save the remove.bg result"""
        if not self.remove_bg_processed_image:
            messagebox.showerror("Error", "No processed image to save")
            return
            
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            title="Save Processed Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.remove_bg_processed_image, file_path)
                messagebox.showinfo("Success", f"Image saved successfully!")
                self.remove_bg_status.set("✓ Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    # ============ DEVELOPER POPUP ==============
    def open_developer_popup(self):
        """Open developer information popup"""
        dev_window = tk.Toplevel(self.root)
        dev_window.title("HackForge - Developer Information")
        dev_window.geometry("400x500")
        dev_window.minsize(400, 500)
        dev_window.transient(self.root)
        dev_window.grab_set()
        try:
            icon_path = "hackforge_icon.ico"
            if os.path.exists(icon_path):
                dev_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARNING] Gagal load icon: {e}")
        
        # Apply theme
        theme = self.themes[self.current_theme]
        dev_window.configure(bg=theme["bg"])
        
        # Main frame
        main_frame = ttk.Frame(dev_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        
        # Title with icon
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        title_frame.columnconfigure(1, weight=1)
        
        if self.developer_icon:
            icon_label = ttk.Label(title_frame, image=self.developer_icon)
            icon_label.grid(row=0, column=0, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="HackForge Developer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, sticky="w")
        
        # Developer image
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, pady=10)
        try:
            # Create a hacker-style placeholder image
            img = Image.new('RGB', (150, 150), color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            draw.rectangle([20, 20, 130, 130], outline='#00ff00', width=2)
            draw.text((40, 65), "HACKFORGE", fill='#00ff00')
            
            dev_photo = ImageTk.PhotoImage(img)
            image_label = ttk.Label(image_frame, image=dev_photo)
            image_label.image = dev_photo
            image_label.pack()
        except Exception as e:
            print(f"Failed to create developer image: {e}")
        
        # Developer information
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        info_text = """HACKFORGE LAUNCHER

Developer: Dwi Bakti N Dev
Version: V 4.0.0
Date: 2025

Features:
• Python Script Launcher
• Multi-language Support
• Hacker Theme
• Drawing Tools
• Background Removal
• System Tray Integration
• Text-to-Speech

Contact: dwibakti76@gmail.com
GitHub: https://github.com/DwiDevelopes
Google Search : Dwi Bakti N Dev"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, font=("Arial", 10))
        info_label.pack()
        
        # Close button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            command=dev_window.destroy,
            width=15
        )
        close_btn.pack()

    # ============ CUSTOM THEME POPUP ==============
    def open_custom_theme_popup(self):
        """Open custom theme customization popup"""
        theme_window = tk.Toplevel(self.root)
        theme_window.title("HackForge - Custom Theme Editor")
        theme_window.geometry("390x720")
        theme_window.transient(self.root)
        theme_window.grab_set()
        try:
            icon_path = "hackforge_icon.ico"
            if os.path.exists(icon_path):
                theme_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARNING] Gagal load icon: {e}")
        
        # Apply theme
        theme = self.themes[self.current_theme]
        theme_window.configure(bg=theme["bg"])
        
        # Main frame with scrollbar
        main_frame = ttk.Frame(theme_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar for responsive layout
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title with icon
        title_frame = ttk.Frame(scrollable_frame)
        title_frame.pack(fill="x", pady=(0, 15))
        title_frame.columnconfigure(1, weight=1)
        
        if self.theme_icon:
            icon_label = ttk.Label(title_frame, image=self.theme_icon)
            icon_label.grid(row=0, column=0, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="HackForge Theme Editor", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, sticky="w")
        
        # Color selection section
        colors_frame = ttk.LabelFrame(scrollable_frame, text="Color Settings", padding=15)
        colors_frame.pack(fill="x", pady=10)
        colors_frame.columnconfigure(1, weight=1)
        
        color_options = [
            ("Background Color", "bg"),
            ("Text Color", "fg"),
            ("Button Background", "button_bg"),
            ("Button Text Color", "button_fg"),
            ("Text Area Background", "text_bg"),
            ("Text Area Text Color", "text_fg"),
            ("Accent Color", "accent")
        ]
        
        self.color_widgets = {}
        
        for i, (label, color_type) in enumerate(color_options):
            row_frame = ttk.Frame(colors_frame)
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", pady=8)
            row_frame.columnconfigure(1, weight=1)
            
            # Label
            ttk.Label(row_frame, text=label, font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=(0, 10))
            
            # Color preview button
            color_btn = tk.Button(
                row_frame,
                text="   ",
                bg=self.custom_colors[color_type],
                command=lambda ct=color_type: self.choose_custom_color(ct, theme_window),
                relief="solid",
                bd=2,
                width=4,
                height=1,
                cursor="hand2"
            )
            color_btn.grid(row=0, column=1, sticky="w", padx=(0, 10))
            
            # Hex value display
            hex_var = tk.StringVar(value=self.custom_colors[color_type])
            hex_label = ttk.Label(row_frame, textvariable=hex_var, font=("Arial", 9), width=10)
            hex_label.grid(row=0, column=2, sticky="w")
            
            # Store widgets for updates
            self.color_widgets[color_type] = {
                'button': color_btn,
                'hex_var': hex_var
            }
        
        # Preview section
        preview_frame = ttk.LabelFrame(scrollable_frame, text="Live Preview", padding=15)
        preview_frame.pack(fill="x", pady=10)
        
        # Create preview widgets that mimic the main UI
        self.create_theme_preview(preview_frame)
        
        # Action buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", pady=20)
        button_frame.columnconfigure((0, 1, 2), weight=1)
        
        apply_btn = ttk.Button(
            button_frame,
            text="Apply Theme",
            command=lambda: self.apply_custom_theme(theme_window),
            style="Accent.TButton"
        )
        apply_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        reset_btn = ttk.Button(
            button_frame,
            text="Reset to Default",
            command=self.reset_custom_theme
        )
        reset_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            command=theme_window.destroy
        )
        close_btn.grid(row=0, column=2, padx=5, sticky="ew")
        
        # Store reference for updates
        self.theme_window = theme_window
        self.preview_frame = preview_frame

    def create_theme_preview(self, parent):
        """Create live preview of the theme"""
        # Preview container
        preview_container = ttk.Frame(parent)
        preview_container.pack(fill="x", expand=True)
        
        # Sample widgets that mimic the main UI
        sample_label = ttk.Label(preview_container, text="Sample Label", font=("Arial", 11))
        sample_label.pack(pady=5, anchor="w")
        
        sample_button = ttk.Button(preview_container, text="Sample Button")
        sample_button.pack(pady=5, fill="x")
        
        sample_entry = ttk.Entry(preview_container, text="Sample Entry Text")
        sample_entry.pack(pady=5, fill="x")
        
        sample_text = tk.Text(preview_container, height=3, width=40)
        sample_text.insert("1.0", "Sample text area with multiple lines...")
        sample_text.pack(pady=5, fill="x")
        
        # Store preview widgets for updates
        self.preview_widgets = {
            'container': preview_container,
            'label': sample_label,
            'button': sample_button,
            'entry': sample_entry,
            'text': sample_text
        }
        
        # Update preview immediately
        self.update_theme_preview()

    def update_theme_preview(self):
        """Update the theme preview with current colors"""
        if not hasattr(self, 'preview_widgets'):
            return
            
        try:
            # Apply colors to preview widgets
            for widget in [self.preview_widgets['container']]:
                for child in widget.winfo_children():
                    try:
                        if isinstance(child, tk.Label):
                            child.configure(bg=self.custom_colors["bg"], fg=self.custom_colors["fg"])
                        elif isinstance(child, ttk.Button):
                            style = ttk.Style()
                            style.configure("Preview.TButton", 
                                         background=self.custom_colors["button_bg"],
                                         foreground=self.custom_colors["button_fg"])
                            child.configure(style="Preview.TButton")
                        elif isinstance(child, tk.Entry):
                            child.configure(bg=self.custom_colors["text_bg"], fg=self.custom_colors["fg"],
                                          insertbackground=self.custom_colors["fg"])
                        elif isinstance(child, tk.Text):
                            child.configure(bg=self.custom_colors["text_bg"], fg=self.custom_colors["fg"],
                                          insertbackground=self.custom_colors["fg"])
                    except:
                        pass
        except Exception as e:
            print(f"Error updating preview: {e}")

    def choose_custom_color(self, color_type, theme_window):
        """Choose color for custom theme"""
        current_color = self.custom_colors[color_type]
        color = colorchooser.askcolor(
            title=f"Choose {color_type.replace('_', ' ').title()}",
            initialcolor=current_color
        )
        
        if color[1]:
            # Update color
            self.custom_colors[color_type] = color[1]
            
            # Update color button
            self.color_widgets[color_type]['button'].configure(bg=color[1])
            
            # Update hex display
            self.color_widgets[color_type]['hex_var'].set(color[1])
            
            # Update preview
            self.update_theme_preview()
            
            # Bring theme window back to front
            theme_window.lift()
            theme_window.focus_force()

    def apply_custom_theme(self, theme_window):
        """Apply the custom theme"""
        self.themes["Custom"] = self.custom_colors.copy()
        self.current_theme = "Custom"
        self.theme_var.set("Custom")
        self.apply_theme()
        theme_window.destroy()
        messagebox.showinfo("Success", "Custom theme applied successfully!")

    def reset_custom_theme(self):
        """Reset custom theme to default"""
        default_colors = {
            "bg": "#1a1a1a",
            "fg": "#00ff00",
            "button_bg": "#2a2a2a",
            "button_fg": "#00ff00",
            "text_bg": "#1a1a1a",
            "text_fg": "#00ff00",
            "accent": "#00ff00"
        }
        
        self.custom_colors = default_colors.copy()
        
        # Update all color widgets
        for color_type, widgets in self.color_widgets.items():
            widgets['button'].configure(bg=default_colors[color_type])
            widgets['hex_var'].set(default_colors[color_type])
        
        # Update preview
        self.update_theme_preview()

    # ============ VIDEO SETUP ==============
    def setup_video(self):
        """Setup video playback in the video frame"""
        video_path = r"C:\Users\User\Downloads\streamlit_launcher\streamlit_launcher\assets\intro.mp4"
        
        if os.path.exists(video_path):
            try:
                self.video_capture = cv2.VideoCapture(video_path)
                self.update_video_frame()
            except Exception as e:
                print(f"[WARNING] Gagal load video: {e}")
                self.load_image_fallback()
        else:
            print("[WARNING] File video tidak ditemukan, menggunakan gambar fallback.")
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
            "title": "HackForge Launcher",
            "script": "Script:",
            "run": "Run Script",
            "stop": "Stop Script",
            "log": "Terminal Output",
            "status_ready": "Ready",
            "language": "Language:",
            "theme": "Theme:",
            "customize": "Customize",
            "welcome_speech": "Welcome to HackForge Launcher",
            "start_speech": "Starting Python Script",
            "stop_speech": "Stopping Python Script",
            "enable_draw": "🎨 Enable Drawing",
            "disable_draw": "🎨 Disable Drawing",
            "draw_color": "🌈 Color",
            "clear_draw": "🧹 Clear All",
            "draw_size": "Size:",
            "eraser": "📝 Eraser",
            "hide_window": "⬇️ Hide to Tray",
            "drawing_tools": "🎨 Drawing Tools",
            "remove_bg": "🖼️ Remove BG",
            "developer_info": "👨‍💻 Developer",
            "custom_theme": "🎨 Custom Theme",
            "open_terminal": "💻 Open Terminal"
        }

    def chinese_texts(self):
        return {
            "title": "HackForge 启动器",
            "script": "脚本:",
            "run": "运行脚本",
            "stop": "停止脚本",
            "log": "终端输出",
            "status_ready": "准备就绪",
            "language": "语言:",
            "theme": "主题:",
            "customize": "自定义",
            "welcome_speech": "欢迎使用 HackForge 启动器",
            "start_speech": "正在启动 Python 脚本",
            "stop_speech": "正在停止 Python 脚本",
            "enable_draw": "🎨 启用绘图",
            "disable_draw": "🎨 禁用绘图",
            "draw_color": "🌈 颜色",
            "clear_draw": "🧹 全部清除",
            "draw_size": "大小:",
            "eraser": "📝 橡皮擦",
            "hide_window": "⬇️ 隐藏到托盘",
            "drawing_tools": "🎨 绘图工具",
            "remove_bg": "🖼️ 去除背景",
            "developer_info": "👨‍💻 开发者信息",
            "custom_theme": "🎨 自定义主题",
            "open_terminal": "💻 打开终端"
        }

    def japanese_texts(self):
        return {
            "title": "HackForge ランチャー",
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
            "enable_draw": "🎨 描画を有効",
            "disable_draw": "🎨 描画を無効",
            "draw_color": "🌈 色",
            "clear_draw": "🧹 全て消去",
            "draw_size": "サイズ:",
            "eraser": "📝 消しゴム",
            "hide_window": "⬇️ トレイに隠す",
            "drawing_tools": "🎨 描画ツール",
            "remove_bg": "🖼️ 背景削除",
            "developer_info": "👨‍💻 開発者情報",
            "custom_theme": "🎨 カスタムテーマ",
            "open_terminal": "💻 ターミナルを開く"
        }
        
    def russian_texts(self):
        return {
            "title": "HackForge Launcher",
            "script": "Скрипт:",
            "run": "Запустить скрипт",
            "stop": "Остановить скрипт",
            "log": "Вывод терминала",
            "status_ready": "Готово",
            "language": "Язык:",
            "theme": "Тема:",
            "customize": "Настроить",
            "welcome_speech": "Добро пожаловать в HackForge Launcher",
            "start_speech": "Запуск Python скрипта",
            "stop_speech": "Остановка Python скрипта",
            "enable_draw": "🎨 Включить рисование",
            "disable_draw": "🎨 Выключить рисование",
            "draw_color": "🌈 Цвет",
            "clear_draw": "🧹 Очистить всё",
            "draw_size": "Размер:",
            "eraser": "📝 Ластик",
            "hide_window": "⬇️ Скрыть в трей",
            "drawing_tools": "🎨 Инструменты рисования",
            "remove_bg": "🖼️ Удалить фон",
            "developer_info": "👨‍💻 Разработчик",
            "custom_theme": "🎨 Пользовательская тема",
            "open_terminal": "💻 Открыть терминал"
        }
        
    def jawa_texts(self):
        return {
            "title": "HackForge Launcher",
            "script": "Script:",
            "run": "Jalankan Script",
            "stop": "Stop Script",
            "log": "Output Terminal",
            "status_ready": "Siap",
            "language": "Basa:",
            "theme": "Tema:",
            "customize": "Sesuaikan",
            "welcome_speech": "Sugeng Rawuh ing HackForge Launcher",
            "start_speech": "Miwiti Script Python",
            "stop_speech": "Script Python Mungkasi",
            "enable_draw": "🎨 Aktifake Gambar",
            "disable_draw": "🎨 Matiake Gambar",
            "draw_color": "🌈 Warna",
            "clear_draw": "🧹 Bersihke Kabeh",
            "draw_size": "Ukuran:",
            "eraser": "📝 Penghapus",
            "hide_window": "⬇️ Sembunyi neng Tray",
            "drawing_tools": "🎨 Alat Gambar",
            "remove_bg": "🖼️ Hapus Background",
            "developer_info": "👨‍💻 Pengembang",
            "custom_theme": "🎨 Tema Kostum",
            "open_terminal": "💻 Bukak Terminal"
        }

    def find_main_script(self):
        base_dir = r"C:\Users\User\Downloads\hackforge\hackforge"
        main_path = os.path.join(base_dir, "main.py")
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
        for i in range(11):
            self.main_frame.rowconfigure(i, weight=0)
        self.main_frame.rowconfigure(10, weight=1)
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
            command=self.start_server,
            image=self.start_icon if self.start_icon else None,
            compound="left"
        )
        self.start_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        self.stop_btn = ttk.Button(
            button_frame, 
            command=self.stop_server, 
            state=tk.DISABLED,
            image=self.stop_icon if self.stop_icon else None,
            compound="left"
        )
        self.stop_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        # Hide to tray button
        self.hide_btn = ttk.Button(
            button_frame,
            command=self.toggle_window,
            image=self.hide_icon if self.hide_icon else None,
            compound="left"
        )
        self.hide_btn.grid(row=0, column=2, padx=2, sticky="ew")

        # Additional Tools Buttons
        tools_frame = ttk.Frame(self.main_frame)
        tools_frame.grid(row=6, column=0, pady=5, sticky="ew")
        tools_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Drawing tools button
        self.drawing_btn = ttk.Button(
            tools_frame,
            command=self.open_drawing_popup,
            image=self.drawing_icon if self.drawing_icon else None,
            compound="left"
        )
        self.drawing_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        # Remove BG button
        self.remove_bg_btn = ttk.Button(
            tools_frame,
            command=self.open_remove_bg_popup,
            image=self.remove_bg_icon if self.remove_bg_icon else None,
            compound="left"
        )
        self.remove_bg_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        # Developer info button
        self.developer_btn = ttk.Button(
            tools_frame,
            command=self.open_developer_popup,
            image=self.developer_icon if self.developer_icon else None,
            compound="left"
        )
        self.developer_btn.grid(row=0, column=2, padx=2, sticky="ew")
        
        # Open terminal button
        self.terminal_btn = ttk.Button(
            tools_frame,
            command=self.open_terminal,
            text="💻",
            compound="left"
        )
        self.terminal_btn.grid(row=0, column=3, padx=2, sticky="ew")

        # Log
        log_frame = ttk.LabelFrame(self.main_frame, text="Terminal Output", padding=5)
        log_frame.grid(row=10, column=0, sticky="nsew", pady=5)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.config(state=tk.DISABLED)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor="w")
        status_bar.grid(row=11, column=0, sticky="ew")

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
        self.hide_btn.config(text=texts["hide_window"])
        self.drawing_btn.config(text=texts["drawing_tools"])
        self.remove_bg_btn.config(text=texts["remove_bg"])
        self.developer_btn.config(text=texts["developer_info"])
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

    # ============ SCRIPT CONTROL ==============
    def start_server(self):
        filename = self.script_path
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File '{filename}' not found")
            return
            
        self.play_start_speech()
        thread = threading.Thread(target=self.run_python_script, args=(filename,), daemon=True)
        thread.start()
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Running: {os.path.basename(filename)}")
        self.log_message(f"Starting Python script: {filename}")
        self.log_message("=" * 50)
        self.update_tray_icon(True)

    def run_python_script(self, filename):
        try:
            # Run Python script directly and capture output
            self.process = subprocess.Popen(
                [sys.executable, filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace"
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
        self.update_tray_icon(False)

    def log_message(self, message):
        def update():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self.root.after(0, update)

    def stop_server(self):
        self.play_stop_speech()
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
        """Handle window closing - minimize to tray instead of closing"""
        self.toggle_window()

    def quit_application_completely(self):
        """Quit application completely"""
        if self.is_running:
            self.stop_server()
        if self.tray_icon:
            self.tray_icon.stop()
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

    def show_context_menu(event):
        try:
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Quit Application", command=app.quit_application_completely)
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    root.bind("<Button-3>", show_context_menu)  
    root.mainloop()

if __name__ == "__main__":
    run_gui()