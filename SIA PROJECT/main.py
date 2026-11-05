import tkinter as tk
from tkinter import messagebox
from auth import AuthManager
from database import Database

class LoginApp:

  def __init__(self, root):
    self.root = root
    self.root.title("LOGIN // REGISTER")
    self.root.geometry("460x540")

    self.bg_main = "#F2EDE3"
    self.card_bg = "#FFFDF8"
    self.ink = "#252525"
    self.accent_yellow = "#E9B949"
    self.accent_green = "#68D170"
    self.accent_pink = "#FF0000"
    self.secondary = "#E6DFD2"
    self.font_mono = "Consolas"
    self.root.configure(bg=self.bg_main)
    self.root.resizable(False, False)
    self.db = Database()
    self.auth = AuthManager(self.db)
    self.current_user = None

    self.show_login_screen()

  def clear_screen(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  def create_brutalist_card(self, x, y, width, height, bg_color=None):
    if bg_color is None:
      bg_color = self.card_bg

    shadow = tk.Frame(self.root, bg=self.ink)
    shadow.place(x=x + 7, y=y + 7, width=width, height=height)

    card = tk.Frame(
        self.root,
        bg=bg_color,
        highlightbackground=self.ink,
        highlightcolor=self.ink,
        highlightthickness=3,
    )
    card.place(x=x, y=y, width=width, height=height)
    return card

  def create_brutalist_entry(self, parent, show=None):
    entry = tk.Entry(
        parent,
        font=(self.font_mono, 12, "bold"),
        bg=self.bg_main,
        fg=self.ink,
        insertbackground=self.ink,
        relief="flat",
        highlightbackground=self.ink,
        highlightcolor=self.ink,
        highlightthickness=2,
        bd=6,
        show=show,
    )
    return entry

  def create_brutalist_button(self, parent, text, bg_color, command):
    wrapper = tk.Frame(parent, bg=parent["bg"], height=46)
    wrapper.pack(fill="x", padx=28, pady=8)
    wrapper.pack_propagate(False)

    shadow = tk.Frame(wrapper, bg=self.ink)
    shadow.place(x=4, y=4, relwidth=1.0, relheight=1.0, width=-4, height=-4)

    btn = tk.Button(
        wrapper,
        text=text,
        font=(self.font_mono, 11, "bold"),
        bg=bg_color,
        fg=self.ink,
        activebackground=bg_color,
        activeforeground=self.ink,
        relief="flat",
        bd=0,
        highlightbackground=self.ink,
        highlightcolor=self.ink,
        highlightthickness=2,
        cursor="hand2",
        command=command,
    )
    btn.place(x=0, y=0, relwidth=1.0, relheight=1.0, width=-4, height=-4)

    def on_press(e):
      btn.place_configure(x=3, y=3)

    def on_release(e):
      btn.place_configure(x=0, y=0)

    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)
    return btn

  def show_login_screen(self):
    self.clear_screen()

    banner = self.create_brutalist_card(
        40, 25, 370, 55, bg_color=self.accent_yellow
    )

    tk.Label(
        banner,
        text="LOGIN",
        font=(self.font_mono, 16, "bold"),
        bg=self.accent_yellow,
        fg=self.ink,
    ).pack(expand=True)

    card = self.create_brutalist_card(40, 100, 370, 390)

    tk.Label(
        card,
        text="USERNAME_",
        font=(self.font_mono, 10, "bold"),
        bg=self.card_bg,
        fg=self.ink,
    ).pack(anchor="w", padx=28, pady=(25, 4))

    self.login_user_entry = self.create_brutalist_entry(card)
    self.login_user_entry.pack(fill="x", padx=28, pady=(0, 15))

    tk.Label(
        card,
        text="PASSWORD_",
        font=(self.font_mono, 10, "bold"),
        bg=self.card_bg,
        fg=self.ink,
    ).pack(anchor="w", padx=28, pady=(5, 4))

    self.login_pass_entry = self.create_brutalist_entry(card, show="█")
    self.login_pass_entry.pack(fill="x", padx=28, pady=(0, 20))

    self.create_brutalist_button(
        card, "LOGIN", self.accent_yellow, self.handle_login
    )

    self.create_brutalist_button(
        card, "REGISTER", self.secondary, self.show_register_screen
    )

  def show_register_screen(self):
    self.clear_screen()

    banner = self.create_brutalist_card(
        40, 25, 370, 55, bg_color=self.accent_green
    )

    tk.Label(
        banner,
        text="REGISTER",
        font=(self.font_mono, 16, "bold"),
        bg=self.accent_green,
        fg=self.ink,
    ).pack(expand=True)

    card = self.create_brutalist_card(40, 100, 370, 390)

    tk.Label(
        card,
        text="NEW_USERNAME_",
        font=(self.font_mono, 10, "bold"),
        bg=self.card_bg,
        fg=self.ink,
    ).pack(anchor="w", padx=28, pady=(25, 4))

    self.reg_user_entry = self.create_brutalist_entry(card)
    self.reg_user_entry.pack(fill="x", padx=28, pady=(0, 15))

    tk.Label(
        card,
        text="NEW_PASSWORD_",
        font=(self.font_mono, 10, "bold"),
        bg=self.card_bg,
        fg=self.ink,
    ).pack(anchor="w", padx=28, pady=(5, 4))

    self.reg_pass_entry = self.create_brutalist_entry(card, show="█")
    self.reg_pass_entry.pack(fill="x", padx=28, pady=(0, 20))

    self.create_brutalist_button(
        card, "REGISTER", self.accent_green, self.handle_register
    )

    self.create_brutalist_button(
        card, "<- BACK TO LOGIN", self.secondary, self.show_login_screen
    )

  def handle_register(self):
    username = self.reg_user_entry.get().strip()
    password = self.reg_pass_entry.get().strip()

    success, message = self.auth.register_user(username, password)

    if success:
      messagebox.showinfo("SYS_MSG // SUCCESS", message)
      self.show_login_screen()
    else:
      messagebox.showerror("SYS_ERR // FAILED", message)

  def handle_login(self):
    username = self.login_user_entry.get().strip()
    password = self.login_pass_entry.get().strip()

    success, message = self.auth.verify_login(username, password)

    if success:
      self.current_user = username
      self.show_placeholder_dashboard()
    else:
      messagebox.showerror("SYS_ERR // DENIED", message)

  def show_placeholder_dashboard(self):
    self.clear_screen()

    banner = self.create_brutalist_card(
        40, 25, 370, 55, bg_color=self.accent_yellow
    )

    tk.Label(
        banner,
        text=f"USER // {self.current_user.upper()}",
        font=(self.font_mono, 15, "bold"),
        bg=self.accent_yellow,
        fg=self.ink,
    ).pack(expand=True)

    card = self.create_brutalist_card(40, 100, 370, 360)

    tk.Label(
        card,
        text="STATUS\nSPRINT 01: COMPLETE",
        font=(self.font_mono, 12, "bold"),
        bg=self.card_bg,
        fg=self.ink,
        justify="left",
    ).pack(pady=(50, 15), padx=28, anchor="w")

    tk.Label(
        card,
        text="Namimili pa ng\nFunctions",
        font=(self.font_mono, 10),
        bg=self.card_bg,
        fg=self.ink,
        justify="left",
    ).pack(pady=(0, 40), padx=28, anchor="w")

    self.create_brutalist_button(
        card, "LOG OUT", self.accent_pink, self.show_login_screen
    )

if __name__ == "__main__":
  root = tk.Tk()
  app = LoginApp(root)
  root.mainloop()
