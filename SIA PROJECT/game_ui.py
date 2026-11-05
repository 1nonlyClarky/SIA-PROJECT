import tkinter as tk
from tkinter import messagebox
from trivia_service import TriviaService


class GameView:

  def __init__(self, app, username):
    self.app = app
    self.root = app.root
    self.db = app.db
    self.username = username
    self.api = TriviaService()

    self.selected_category = tk.StringVar(value="VIDEO GAMES")
    self.questions = []
    self.q_index = 0
    self.score = 0

  def show_lobby(self):
    self.app.clear_screen()

    banner = self.app.create_brutalist_card(
        40, 20, 370, 50, bg_color=self.app.accent_yellow
    )
    tk.Label(
        banner,
        text=f"PLAYER // {self.username.upper()}",
        font=(self.app.font_mono, 14, "bold"),
        bg=self.app.accent_yellow,
        fg=self.app.ink,
    ).pack(expand=True)

    card = self.app.create_brutalist_card(40, 90, 370, 415)

    tk.Label(
        card,
        text="SELECT CATEGORY_",
        font=(self.app.font_mono, 11, "bold"),
        bg=self.app.card_bg,
        fg=self.app.ink,
    ).pack(anchor="w", padx=24, pady=(20, 8))

    for cat in self.api.CATEGORIES:
      rb = tk.Radiobutton(
          card,
          text=cat,
          variable=self.selected_category,
          value=cat,
          font=(self.app.font_mono, 10, "bold"),
          bg=self.app.card_bg,
          fg=self.app.ink,
          activebackground=self.app.card_bg,
          selectcolor=self.app.accent_yellow,
          cursor="hand2",
      )
      rb.pack(anchor="w", padx=32, pady=2)

    tk.Frame(card, bg=self.app.ink, height=2).pack(fill="x", padx=24, pady=12)

    self.app.create_brutalist_button(
        card, "[ START 10-Q RUN ]", self.app.accent_green, self.start_game
    )
    self.app.create_brutalist_button(
        card, "HALL OF FAME (SCORES)", self.app.secondary, self.show_leaderboard
    )
    self.app.create_brutalist_button(
        card, "LOG OUT", self.app.accent_pink, self.app.show_login_screen
    )

  def start_game(self):
    category = self.selected_category.get()
    success, result = self.api.get_questions(category, amount=10)

    if not success:
      messagebox.showerror("API_ERR", result)
      return

    self.questions = result
    self.q_index = 0
    self.score = 0
    self.show_question_screen()

  def show_question_screen(self):
    self.app.clear_screen()

    if self.q_index >= len(self.questions):
      self.finish_game()
      return

    q_data = self.questions[self.q_index]

    banner = self.app.create_brutalist_card(
        40, 20, 370, 50, bg_color=self.app.accent_yellow
    )
    hud_text = (
        f"Q {self.q_index + 1}/10  |  SCORE: {self.score}  |"
        f"  {q_data['difficulty']}"
    )
    tk.Label(
        banner,
        text=hud_text,
        font=(self.app.font_mono, 11, "bold"),
        bg=self.app.accent_yellow,
        fg=self.app.ink,
    ).pack(expand=True)

    card = self.app.create_brutalist_card(40, 90, 370, 415)

    q_box = tk.Frame(
        card,
        bg=self.app.bg_main,
        highlightbackground=self.app.ink,
        highlightthickness=2,
    )
    q_box.pack(fill="x", padx=24, pady=(18, 12))

    tk.Label(
        q_box,
        text=q_data["question"],
        font=(self.app.font_mono, 10, "bold"),
        bg=self.app.bg_main,
        fg=self.app.ink,
        wraplength=290,
        justify="left",
        pady=12,
        padx=10,
    ).pack()

    for opt in q_data["options"]:
      self.app.create_brutalist_button(
          card,
          opt,
          self.app.secondary,
          lambda selected=opt: self.check_answer(selected),
          height=40,
          pady=5,
      )

    tk.Button(
        card,
        text="<- ABORT RUN",
        font=(self.app.font_mono, 9, "bold"),
        bg=self.app.card_bg,
        fg=self.app.ink,
        bd=0,
        cursor="hand2",
        command=self.show_lobby,
    ).pack(pady=(6, 0))

  def check_answer(self, selected):
    correct = self.questions[self.q_index]["correct"]
    if selected == correct:
      self.score += 1
    self.q_index += 1
    self.show_question_screen()

  def finish_game(self):
    category = self.selected_category.get()
    self.db.save_score(
        self.username, category, self.score, len(self.questions)
    )

    self.app.clear_screen()
    banner = self.app.create_brutalist_card(
        40, 25, 370, 55, bg_color=self.app.accent_green
    )
    tk.Label(
        banner,
        text="RUN COMPLETE!",
        font=(self.app.font_mono, 16, "bold"),
        bg=self.app.accent_green,
        fg=self.app.ink,
    ).pack(expand=True)

    card = self.app.create_brutalist_card(40, 100, 370, 390)

    tk.Label(
        card,
        text=f"CATEGORY:\n{category}",
        font=(self.app.font_mono, 11, "bold"),
        bg=self.app.card_bg,
        fg=self.app.ink,
        justify="left",
    ).pack(anchor="w", padx=28, pady=(30, 10))

    tk.Label(
        card,
        text=f"FINAL SCORE: {self.score} / {len(self.questions)}",
        font=(self.app.font_mono, 16, "bold"),
        bg=self.app.accent_yellow,
        fg=self.app.ink,
        padx=12,
        pady=8,
    ).pack(anchor="w", padx=28, pady=(5, 25))

    self.app.create_brutalist_button(
        card, "PLAY AGAIN", self.app.accent_green, self.start_game
    )
    self.app.create_brutalist_button(
        card, "HALL OF FAME", self.app.secondary, self.show_leaderboard
    )
    self.app.create_brutalist_button(
        card, "MAIN LOBBY", self.app.bg_main, self.show_lobby
    )

  def show_leaderboard(self):
    self.app.clear_screen()

    banner = self.app.create_brutalist_card(
        40, 20, 370, 50, bg_color=self.app.accent_yellow
    )
    tk.Label(
        banner,
        text="HALL OF FAME // TOP 8",
        font=(self.app.font_mono, 14, "bold"),
        bg=self.app.accent_yellow,
        fg=self.app.ink,
    ).pack(expand=True)

    card = self.app.create_brutalist_card(40, 90, 370, 415)

    board_box = tk.Frame(
        card,
        bg=self.app.bg_main,
        highlightbackground=self.app.ink,
        highlightthickness=2,
    )
    board_box.pack(fill="both", expand=True, padx=24, pady=(20, 10))

    records = self.db.get_top_scores(limit=8)
    if not records:
      tk.Label(
          board_box,
          text="NO SCORES RECORDED YET.",
          font=(self.app.font_mono, 10, "bold"),
          bg=self.app.bg_main,
          fg=self.app.ink,
      ).pack(pady=40)
    else:
      header = f"{'USER':<10} {'CAT':<12} {'SCORE':<6}"
      tk.Label(
          board_box,
          text=header,
          font=(self.app.font_mono, 9, "bold"),
          bg=self.app.accent_yellow,
          fg=self.app.ink,
          anchor="w",
          padx=8,
      ).pack(fill="x")

      for user, cat, sc, tot, _ in records:
        row_txt = f"{user[:9]:<10} {cat[:11]:<12} {sc}/{tot}"
        tk.Label(
            board_box,
            text=row_txt,
            font=(self.app.font_mono, 9),
            bg=self.app.bg_main,
            fg=self.app.ink,
            anchor="w",
            padx=8,
            pady=3,
        ).pack(fill="x")

    self.app.create_brutalist_button(
        card, "<- BACK TO LOBBY", self.app.secondary, self.show_lobby
    )