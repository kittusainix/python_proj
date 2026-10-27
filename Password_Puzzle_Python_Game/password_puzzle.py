import tkinter as tk
from tkinter import messagebox
import random
import string
import hashlib

class PasswordPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Puzzle - Crack the Code")
        self.root.geometry("560x470")
        self.root.resizable(False, False)
        self.secret = ""
        self.attempts = 0
        self.max_attempts = 8
        self.finished = False

        tk.Label(root, text="🔐 PASSWORD PUZZLE", font=("Arial", 20, "bold")).pack(pady=(16, 5))
        tk.Label(root, text="Guess the secret 4-digit code before you run out of tries.",
                 font=("Arial", 10)).pack(pady=3)

        self.info = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.info.pack(pady=10)

        self.entry = tk.Entry(root, font=("Consolas", 20), justify="center", width=12)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        tk.Button(root, text="Check Code", command=self.check_guess,
                  font=("Arial", 11, "bold"), padx=15, pady=5).pack(pady=7)

        self.feedback = tk.Label(root, text="Hints will appear here.", font=("Arial", 11),
                                 wraplength=500, justify="center")
        self.feedback.pack(pady=12)

        self.history_title = tk.Label(root, text="Your guesses", font=("Arial", 12, "bold"))
        self.history_title.pack()
        self.history = tk.Listbox(root, width=55, height=7, font=("Consolas", 10))
        self.history.pack(pady=5)

        tk.Button(root, text="New Game", command=self.new_game,
                  font=("Arial", 10), padx=12, pady=4).pack(pady=8)
        self.new_game()

    def new_game(self):
        self.secret = ''.join(random.choices(string.digits, k=4))
        self.attempts = 0
        self.finished = False
        self.history.delete(0, tk.END)
        self.entry.config(state="normal")
        self.info.config(text=f"Attempts left: {self.max_attempts}")
        self.feedback.config(text="Hint: the code contains four digits (0–9).")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def check_guess(self):
        if self.finished:
            return
        guess = self.entry.get().strip()
        if len(guess) != 4 or not guess.isdigit():
            messagebox.showwarning("Invalid code", "Please enter exactly 4 digits.")
            return

        self.attempts += 1
        exact = sum(a == b for a, b in zip(guess, self.secret))
        common = sum(min(guess.count(d), self.secret.count(d)) for d in set(guess))
        misplaced = common - exact
        self.history.insert(tk.END, f"Try {self.attempts}: {guess} | Correct place: {exact}, Wrong place: {misplaced}")
        self.info.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.entry.delete(0, tk.END)

        if guess == self.secret:
            self.finished = True
            self.feedback.config(text="🎉 Correct! You cracked the password code!")
            self.entry.config(state="disabled")
            messagebox.showinfo("You Win!", f"Great job! The secret code was {self.secret}.")
        elif self.attempts >= self.max_attempts:
            self.finished = True
            self.feedback.config(text=f"Game over! The secret code was {self.secret}.")
            self.entry.config(state="disabled")
            messagebox.showinfo("Game Over", f"No attempts left. The code was {self.secret}.")
        else:
            self.feedback.config(
                text=f"Hint: {exact} digit(s) are in the correct place; "
                     f"{misplaced} digit(s) are in the code but in the wrong place."
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordPuzzle(root)
    root.mainloop()
