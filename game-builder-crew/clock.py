import tkinter as tk
from tkinter import font
import time

class DigitalClock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.time_label = tk.Label(self, font=("Arial", 150), bg="black", fg="white")
        self.time_label.pack(fill=tk.BOTH, expand=True)

        self.update_time()

    def update_time(self):
        now = time.strftime("%H:%M:%S")
        self.time_label.configure(text=now)
        self.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    clock = DigitalClock(root)
    clock.pack(fill=tk.BOTH, expand=True)
    root.mainloop()