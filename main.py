import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import datetime
import calendar

class ModernCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Aura Calendar Pro 2026")
        self.root.geometry("800x900")
        self.root.configure(padx=30, pady=30)

        # État initial
        self.is_dark_mode = True 
        self.today = datetime.now()
        self.current_month = self.today.month
        self.current_year = self.today.year
        self.data = {}

        # Palette de couleurs "Premium"
        self.themes = {
            "dark": {
                "bg": "#0F0F0F", 
                "card": "#1C1C1E", 
                "text": "#FFFFFF",
                "subtext": "#A1A1A6", 
                "accent": "#0A84FF", 
                "btn_bg": "#2C2C2E",
                "hover": "#3A3A3C"
            },
            "light": {
                "bg": "#F2F2F7", 
                "card": "#FFFFFF", 
                "text": "#1D1D1F",
                "subtext": "#86868B", 
                "accent": "#007AFF", 
                "btn_bg": "#E5E5EA",
                "hover": "#D1D1D6"
            }
        }

        self.connect_db()
        self.load_settings()
        self.load_data_from_db()

        self.setup_ui()
        self.apply_theme()

    # --- BASE DE DONNÉES ---
    def connect_db(self):
        try:
            # Assurez-vous que les paramètres correspondent à votre config SQL Server
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost,1433;'
                'DATABASE=BookShelf;'
                'UID=sa;'
                'PWD=;'
                'Encrypt=no;'
                'TrustServerCertificate=yes;'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            self.conn = None

    def load_settings(self):
        if not self.conn: return
        try:
            self.cursor.execute("SELECT is_dark_mode FROM Settings WHERE id = 1")
            row = self.cursor.fetchone()
            if row: self.is_dark_mode = bool(row[0])
        except: pass

    def save_settings(self):
        if self.conn:
            try:
                self.cursor.execute("UPDATE Settings SET is_dark_mode = ? WHERE id = 1", (1 if self.is_dark_mode else 0,))
                self.conn.commit()
            except: pass

    def load_data_from_db(self):
        self.data = {}
        if not self.conn: return
        try:
            self.cursor.execute("SELECT date_str, task_text, is_done FROM Tasks")
            for row in self.cursor.fetchall():
                self.data.setdefault(row[0], []).append({"task": row[1], "done": bool(row[2])})
        except: pass

    def save_task_to_db(self, date_str, task_text):
        if self.conn:
            self.cursor.execute("INSERT INTO Tasks (date_str, task_text, is_done) VALUES (?, ?, 0)", (date_str, task_text))
            self.conn.commit()

    # --- INTERFACE ET LOGIQUE ---

    def setup_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Header stylisé
        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(1, weight=1)

        btn_params = {"font": ("Segoe UI", 12, "bold"), "border": 0, "cursor": "hand2", "width": 4, "pady": 5}
        
        self.btn_prev = tk.Button(self.header_frame, text="", command=self.prev_month, **btn_params)
        self.btn_prev.grid(row=0, column=0)

        self.month_label = tk.Label(self.header_frame, text="", font=("Segoe UI", 28, "bold"))
        self.month_label.grid(row=0, column=1)

        self.btn_next = tk.Button(self.header_frame, text="", command=self.next_month, **btn_params)
        self.btn_next.grid(row=0, column=2)

        self.theme_btn = tk.Button(self.header_frame, text="🌙", command=self.toggle_theme, font=("Segoe UI", 14), border=0, cursor="hand2")
        self.theme_btn.grid(row=0, column=3, padx=(15, 0))

        # Conteneur du Calendrier
        self.calendar_container = tk.Frame(self.root)
        self.calendar_container.grid(row=1, column=0, sticky="nsew")
        for i in range(7): self.calendar_container.grid_columnconfigure(i, weight=1, uniform="group1")

        self.tooltip = tk.Label(self.root, text="", font=("Segoe UI", 10), relief="flat", padx=15, pady=12, justify="left")

        # --- FONCTIONNALITÉ SCROLL ---
        self.root.bind("<MouseWheel>", self.handle_scroll) # Windows
        self.root.bind("<Button-4>", self.handle_scroll)    # Linux Up
        self.root.bind("<Button-5>", self.handle_scroll)    # Linux Down

    def handle_scroll(self, event):
        # Détection du sens du scroll
        if event.delta > 0 or event.num == 4:
            self.prev_month()
        elif event.delta < 0 or event.num == 5:
            self.next_month()

    def apply_theme(self):
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        self.root.configure(bg=theme["bg"])
        self.header_frame.configure(bg=theme["bg"])
        self.month_label.configure(bg=theme["bg"], fg=theme["text"])
        self.calendar_container.configure(bg=theme["bg"])
        
        for btn in [self.btn_prev, self.btn_next, self.theme_btn]:
            btn.configure(bg=theme["btn_bg"], fg=theme["text"], activebackground=theme["hover"], activeforeground=theme["text"])
        
        self.theme_btn.config(text="☀️" if self.is_dark_mode else "🌙")
        self.draw_calendar()

    def draw_calendar(self):
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        for widget in self.calendar_container.winfo_children(): widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        days = ["LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_container, text=day, bg=theme["bg"], fg=theme["subtext"], font=("Segoe UI", 9, "bold")).grid(row=0, column=i, pady=(0, 15))

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        for r, week in enumerate(cal):
            self.calendar_container.grid_rowconfigure(r+1, weight=1, uniform="rowgroup")
            for c, day in enumerate(week):
                if day == 0: continue
                
                date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                is_today = date_str == self.today.strftime("%Y-%m-%d")
                
                # Couleur de l'indicateur
                status_color = theme["btn_bg"]
                if is_today: status_color = theme["accent"]
                if date_str in self.data and self.data[date_str]:
                    status_color = "#28CD41" if all(t['done'] for t in self.data[date_str]) else "#FF3B30"

                cell = tk.Canvas(self.calendar_container, bg=theme["bg"], highlightthickness=0, cursor="hand2")
                cell.grid(row=r+1, column=c, sticky="nsew", padx=4, pady=4)
                
                def render_cell(cvs, d, color, t, mode="normal"):
                    cvs.delete("all")
                    w, h = cvs.winfo_width(), cvs.winfo_height()
                    if w < 10: w, h = 90, 90
                    
                    bg_color = t["hover"] if mode == "hover" else t["card"]
                    # Fond
                    cvs.create_rectangle(5, 5, w-5, h-5, fill=bg_color, outline="", width=0)
                    # Point de statut
                    cvs.create_oval(w/2-4, h-15, w/2+4, h-7, fill=color, outline="")
                    # Numéro du jour
                    cvs.create_text(w/2, h/2-5, text=str(d), fill=t["text"], font=("Segoe UI", 14, "bold" if is_today else "normal"))

                cell.bind("<Configure>", lambda e, cvs=cell, d=day, col=status_color: render_cell(cvs, d, col, theme))
                cell.bind("<Enter>", lambda e, cvs=cell, d=day, col=status_color, ds=date_str: [
                    render_cell(cvs, d, col, theme, "hover"), 
                    self.show_tooltip(e, ds)
                ])
                cell.bind("<Leave>", lambda e, cvs=cell, d=day, col=status_color: [
                    render_cell(cvs, d, col, theme), 
                    self.tooltip.place_forget()
                ])
                cell.bind("<Button-1>", lambda e, ds=date_str: self.open_todo(ds))

    def show_tooltip(self, event, date_str):
        tasks = self.data.get(date_str, [])
        if not tasks: return
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        
        content = f"  {date_str}\n" + "  " + "─" * 15 + "\n"
        content += "\n".join([f"  {'●' if t['done'] else '○'} {t['task']}" for t in tasks])
        
        self.tooltip.config(text=content, bg=theme["card"], fg=theme["text"], highlightbackground=theme["accent"], highlightthickness=1)
        self.tooltip.place(x=event.x_root - self.root.winfo_rootx() + 20, y=event.y_root - self.root.winfo_rooty() + 20)

    def open_todo(self, date_str):
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        win = tk.Toplevel(self.root)
        win.title(f"Tasks - {date_str}")
        win.geometry("400x550")
        win.configure(bg=theme["card"], padx=20, pady=20)
        win.transient(self.root)

        tk.Label(win, text=date_str, bg=theme["card"], fg=theme["accent"], font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        
        e_frame = tk.Frame(win, bg=theme["btn_bg"], padx=10, pady=5)
        e_frame.pack(fill="x", pady=10)
        entry = tk.Entry(e_frame, font=("Segoe UI", 12), bg=theme["btn_bg"], fg=theme["text"], border=0, insertbackground=theme["text"])
        entry.pack(fill="x")

        listbox = tk.Listbox(win, bg=theme["card"], fg=theme["text"], font=("Segoe UI", 11), border=0, 
                            highlightthickness=0, selectbackground=theme["hover"], activestyle="none")
        listbox.pack(expand=True, fill="both", pady=15)

        def refresh():
            listbox.delete(0, tk.END)
            for t in self.data.get(date_str, []):
                icon = " ☑ " if t['done'] else " ☐ "
                listbox.insert(tk.END, f"{icon} {t['task']}")

        def add():
            txt = entry.get().strip()
            if txt:
                self.data.setdefault(date_str, []).append({"task": txt, "done": False})
                self.save_task_to_db(date_str, txt)
                entry.delete(0, tk.END); refresh(); self.draw_calendar()

        def toggle():
            sel = listbox.curselection()
            if sel:
                task = self.data[date_str][sel[0]]
                task['done'] = not task['done']
                if self.conn:
                    self.cursor.execute("UPDATE Tasks SET is_done = ? WHERE date_str = ? AND task_text = ?", 
                                       (1 if task['done'] else 0, date_str, task['task']))
                    self.conn.commit()
                refresh(); self.draw_calendar()

        btn_f = tk.Frame(win, bg=theme["card"])
        btn_f.pack(fill="x", side="bottom")
        tk.Button(btn_f, text="Add Task", command=add, bg=theme["accent"], fg="white", font=("Segoe UI", 10, "bold"), border=0, pady=8).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_f, text="Toggle Status", command=toggle, bg=theme["btn_bg"], fg=theme["text"], font=("Segoe UI", 10), border=0, pady=8).pack(side="left", expand=True, fill="x", padx=5)
        
        refresh()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.save_settings()
        self.apply_theme()

    def prev_month(self):
        self.current_month = 12 if self.current_month == 1 else self.current_month - 1
        self.current_year -= 1 if self.current_month == 12 else 0
        self.draw_calendar()

    def next_month(self):
        self.current_month = 1 if self.current_month == 12 else self.current_month + 1
        self.current_year += 1 if self.current_month == 1 else 0
        self.draw_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalendar(root)
    root.mainloop()