import customtkinter as ctk
import threading
import time
import math
import socket
import urllib.request
import json
import sqlite3
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Physics - 2D Engine")
        self.geometry("800x600")
        self.configure(fg_color="#1a1a24")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Zero Physics - 2D Engine", font=("Helvetica", 24, "bold"), text_color="#00C7FF")
        self.header.pack(pady=20)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        import tkinter as tk
        self.canvas = tk.Canvas(self.main_frame, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        self.balls = []
        for _ in range(10):
            x, y = random.randint(50, 700), random.randint(50, 300)
            vx, vy = random.choice([-3, 3]), random.choice([-3, 3])
            c = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#00C7FF")
            self.balls.append({"id": c, "vx": vx, "vy": vy})
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()
        
    def loop(self):
        while self.running:
            for b in self.balls:
                self.canvas.move(b["id"], b["vx"], b["vy"])
                pos = self.canvas.coords(b["id"])
                if pos[0] <= 0 or pos[2] >= self.canvas.winfo_width(): b["vx"] *= -1
                if pos[1] <= 0 or pos[3] >= self.canvas.winfo_height(): b["vy"] *= -1
            time.sleep(0.016)


if __name__ == "__main__":
    app = App()
    app.mainloop()
