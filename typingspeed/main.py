import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("600x400")

        self.sample_text = "The quick brown fox jumps over the lazy dog."

        # Variables
        self.start_time = None
        self.end_time = None

        # GUI Elements
        self.label = tk.Label(root, text="Type the text below:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.text_display = tk.Label(root, text=self.sample_text, font=("Helvetica", 12), wraplength=500)
        self.text_display.pack(pady=10)

        self.input_field = tk.Text(root, height=5, width=60, font=("Helvetica", 12))
        self.input_field.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_test, font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

    def start_test(self):
        self.input_field.delete(1.0, tk.END)
        self.input_field.focus()
        self.start_time = time.time()
        self.start_button.config(text="Submit", command=self.end_test)

    def end_test(self):
        self.end_time = time.time()
        input_text = self.input_field.get(1.0, tk.END).strip()
        self.calculate_speed(input_text)

    def calculate_speed(self, input_text):
        time_taken = self.end_time - self.start_time
        time_taken_minutes = time_taken / 60
        word_count = len(input_text.split())
        wpm = word_count / time_taken_minutes

        accuracy = self.calculate_accuracy(input_text, self.sample_text)

        self.result_label.config(text=f"Speed: {wpm:.2f} WPM | Accuracy: {accuracy:.2f}%")
        self.start_button.config(text="Start", command=self.start_test)

    def calculate_accuracy(self, input_text, sample_text):
        input_words = input_text.split()
        sample_words = sample_text.split()

        correct_words = sum(1 for i, word in enumerate(input_words) if i < len(sample_words) and word == sample_words[i])

        accuracy = (correct_words / len(sample_words)) * 100
        return accuracy

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
