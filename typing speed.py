import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import string
from time import time

# Sample Prompts
PROMPTS = [
    "Hi, I am your coding instructor.",
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a useful skill for programmers and writers.",
    "Python is a versatile and beginner-friendly programming language.",
    "Never give up because great things take time."
]

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed & Accuracy Tester")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.prompt = ""
        self.start_time = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Typing Speed & Accuracy Tester", font=("Helvetica", 16, "bold"), pady=10).pack()

        self.prompt_label = tk.Label(self.root, text="", wraplength=650, justify="left", font=("Arial", 12))
        self.prompt_label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(self.root, height=10, font=("Arial", 12), wrap=tk.WORD)
        self.text_area.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Test", command=self.start_test, bg="green", fg="white", width=15)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.submit_btn = tk.Button(btn_frame, text="Submit", command=self.evaluate, bg="blue", fg="white", width=15, state="disabled")
        self.submit_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset, bg="gray", fg="white", width=15)
        self.reset_btn.grid(row=0, column=2, padx=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), fg="purple")
        self.result_label.pack(pady=10)

    def start_test(self):
        self.prompt = random.choice(PROMPTS)
        self.prompt_label.config(text=self.prompt)
        self.text_area.delete('1.0', tk.END)
        self.text_area.focus()
        self.text_area.tag_remove("error", "1.0", tk.END)
        self.start_time = time()
        self.submit_btn.config(state="normal")
        self.result_label.config(text="")

    def evaluate(self):
        if self.start_time is None:
            messagebox.showwarning("Warning", "Please click 'Start Test' first.")
            return

        end_time = time()
        typed_text = self.text_area.get('1.0', tk.END).strip()

        original_words = self.clean_text(self.prompt).split()
        typed_words = self.clean_text(typed_text).split()

        # Highlight errors
        self.text_area.tag_remove("error", "1.0", tk.END)
        self.highlight_errors(self.prompt.split(), typed_text.split())

        # Calculate metrics
        time_taken = round(end_time - self.start_time, 2)
        word_count = len(typed_words)
        speed = round(word_count / time_taken * 60, 2) if time_taken > 0 else 0

        errors = 0
        for i in range(min(len(original_words), len(typed_words))):
            if original_words[i] != typed_words[i]:
                errors += 1
        errors += abs(len(original_words) - len(typed_words))

        correct = max(len(original_words) - errors, 0)
        accuracy = round((correct / len(original_words)) * 100, 2)

        result = f"Time Taken: {time_taken} seconds\nTyping Speed: {speed} WPM\nAccuracy: {accuracy}%\nErrors: {errors}"
        self.result_label.config(text=result)
        self.submit_btn.config(state="disabled")

    def highlight_errors(self, original_words, typed_words):
        self.text_area.tag_config("error", foreground="red")
        index = "1.0"

        for i, word in enumerate(typed_words):
            word_start = self.text_area.search(word, index, stopindex=tk.END, nocase=True)
            if not word_start:
                continue
            word_end = f"{word_start}+{len(word)}c"

            # Compare cleaned versions of the words
            typed_clean = word.strip(string.punctuation).lower()
            orig_clean = original_words[i].strip(string.punctuation).lower() if i < len(original_words) else ""

            if typed_clean != orig_clean:
                self.text_area.tag_add("error", word_start, word_end)

            index = word_end

    def clean_text(self, text):
        return ' '.join(word.strip(string.punctuation).lower() for word in text.strip().split())

    def reset(self):
        self.text_area.delete('1.0', tk.END)
        self.prompt_label.config(text="")
        self.result_label.config(text="")
        self.start_time = None
        self.submit_btn.config(state="disabled")
        self.text_area.tag_remove("error", "1.0", tk.END)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
