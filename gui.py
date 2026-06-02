"""
GUI Interface for Xbox Autoclaimer
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from claimer import XboxAutoclaimer
from datetime import datetime


class XboxAutoClaimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Xbox Autoclaimer Tool v1.0")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0d1117")
        
        self.claimer = None
        self.claimer_thread = None
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure color scheme"""
        style = ttk.Style()
        style.theme_use('clam')

    def setup_ui(self):
        """Build the user interface"""
        title = tk.Label(
            self.root,
            text="🎮 Xbox Gamertag Autoclaimer Tool",
            font=("Arial", 22, "bold"),
            bg="#0d1117",
            fg="#58a6ff"
        )
        title.pack(pady=10)
        
        control_frame = tk.Frame(self.root, bg="#0d1117")
        control_frame.pack(pady=10, padx=10, fill="x")
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ START",
            command=self.start_claimer,
            bg="#238636",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ STOP",
            command=self.stop_claimer,
            bg="#da3633",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        reload_btn = tk.Button(
            control_frame,
            text="🔄 RELOAD",
            command=self.reload_files,
            bg="#1f6feb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=10
        )
        reload_btn.pack(side="left", padx=5)
        
        folder_btn = tk.Button(
            control_frame,
            text="📁 DATA FOLDER",
            command=self.open_data_folder,
            bg="#1f6feb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=10
        )
        folder_btn.pack(side="left", padx=5)
        
        stats_frame = tk.Frame(self.root, bg="#161b22")
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.stat_labels = {}
        for stat in ["Checked: 0", "Available: 0", "Claimed: 0", "Rate: 0/sec"]:
            lbl = tk.Label(
                stats_frame,
                text=stat,
                font=("Arial", 10),
                bg="#161b22",
                fg="#79c0ff"
            )
            lbl.pack(side="left", padx=20)
            self.stat_labels[stat.split(":")[0]] = lbl
        
        log_frame = tk.Frame(self.root, bg="#0d1117")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        log_label = tk.Label(
            log_frame,
            text="EXECUTION LOG",
            font=("Arial", 10, "bold"),
            bg="#0d1117",
            fg="#58a6ff"
        )
        log_label.pack(anchor="w", pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            bg="#0d1117",
            fg="#c9d1d9",
            font=("Courier", 9)
        )
        self.log_text.pack(fill="both", expand=True)
        
        self.log_text.tag_config("success", foreground="#3fb950")
        self.log_text.tag_config("error", foreground="#f85149")
        self.log_text.tag_config("available", foreground="#ffa657")
        self.log_text.tag_config("claimed", foreground="#3fb950")
        
        self.log_entry("[*] Xbox Autoclaimer initialized", "success")
        
    def log_entry(self, message: str, tag: str = "success"):
        """Add entry to log"""
        self.log_text.insert("end", f"{message}\\n", tag)
        self.log_text.see("end")
        self.root.update()
        
    def update_status(self, message: str):
        """Update status from claimer"""
        if "AVAILABLE" in message:
            tag = "available"
        elif "CLAIMED" in message:
            tag = "claimed"
        else:
            tag = "success"
        
        self.log_entry(message, tag)
    
    def start_claimer(self):
        """Start the claimer"""
        if self.claimer_thread and self.claimer_thread.is_alive():
            messagebox.showwarning("Running", "Claimer is already running!")
            return
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        self.log_entry("[*] Starting Xbox Autoclaimer...")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        self.claimer = XboxAutoclaimer(on_status_update=self.update_status)
        self.claimer_thread = threading.Thread(target=self.claimer.run, daemon=True)
        self.claimer_thread.start()
        
    def stop_claimer(self):
        """Stop the claimer"""
        if self.claimer:
            self.log_entry("[*] Stopping claimer...")
            self.claimer.stop()
        
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
    def reload_files(self):
        """Reload files"""
        if not self.claimer:
            messagebox.showinfo("Info", "Start the claimer first")
            return
        
        self.log_entry("[*] Reloading files...")
        self.claimer.load_gamertags()
        self.claimer.load_accounts()
        self.log_entry("[+] Files reloaded")
    
    def open_data_folder(self):
        """Open data folder"""
        if not os.path.exists("data"):
            os.makedirs("data")
        
        if os.name == 'nt':
            os.startfile("data")
        elif os.name == 'posix':
            os.system("open data")


def main():
    root = tk.Tk()
    app = XboxAutoClaimerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
