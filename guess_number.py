import tkinter as tk
import random

class GuessTheNumberGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Guess the Number")
        self.window.geometry("400x300")

        self.target_number = random.randint(1, 100)
        self.attempts = 0

        self.instructions = tk.Label(self.window, text="Guess a number between 1 and 100:")
        self.instructions.pack(pady=10)

        self.guess_entry = tk.Entry(self.window)
        self.guess_entry.pack(pady=10)

        self.submit_button = tk.Button(self.window, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack(pady=10)

        self.reset_button = tk.Button(self.window, text="Play Again", command=self.reset_game, state="disabled")
        self.reset_button.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < 1 or guess > 100:
                self.result_label.config(text="Please guess a number between 1 and 100!")
            elif guess < self.target_number:
                self.result_label.config(text="Too low! Try again.")
            elif guess > self.target_number:
                self.result_label.config(text="Too high! Try again.")
            else:
                self.result_label.config(text=f"Congratulations! You guessed it in {self.attempts} attempts!")
                self.submit_button.config(state="disabled")
                self.reset_button.config(state="normal")

        except ValueError:
            self.result_label.config(text="Please enter a valid number!")

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.submit_button.config(state="normal")
        self.reset_button.config(state="disabled")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = GuessTheNumberGame()
    game.run()
