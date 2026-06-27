import time
startTime = time.time()

import tkinter as tk
from tkinter import ttk
from gui import AutoClickerApp

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    print("Loaded GUI in", time.time() - startTime, "seconds...");
    root.mainloop()

if __name__ == "__main__":
    main()
