import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import sys
import os
from ClickController import ClickController

def _resource(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, relative_path)

ALL_KEYS = [
    "Left Click", "Right Click", "Middle Click",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "space", "enter", "escape", "tab", "backspace", "delete", "insert",
    "home", "end", "page up", "page down",
    "up", "down", "left", "right",
    "caps lock", "num lock", "scroll lock", "print screen", "pause",
    "left shift", "right shift", "left ctrl", "right ctrl",
    "left alt", "right alt", "left win", "right win",
    "numpad 0", "numpad 1", "numpad 2", "numpad 3", "numpad 4",
    "numpad 5", "numpad 6", "numpad 7", "numpad 8", "numpad 9",
    "numpad +", "numpad -", "numpad *", "numpad /", "numpad .",
    "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",
    "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
    "{", "}", "|", ":", "\"", "<", ">", "?",
]

CLICK_TYPES = ["Single Click", "Double Click", "Tripple Click"]


class AutoClickerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.resizable(False, False)
        self.root.iconbitmap(_resource("Pointer.ico"))

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # --- Top bar: click counter (left) and mouse position (right) ---
        self.click_count_var = tk.StringVar(value="Clicks: 0")
        ttk.Label(self.root, textvariable=self.click_count_var).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(6, 0))

        self.mouse_pos_var = tk.StringVar(value="X: 0   Y: 0")
        ttk.Label(self.root, textvariable=self.mouse_pos_var).grid(row=0, column=0, columnspan=2, sticky="e", padx=12, pady=(6, 0))
        self._update_mouse_pos()
        self._update_click_count()

        # --- Click Interval ---
        interval_frame = ttk.LabelFrame(self.root, text="Click Interval")
        interval_frame.grid(row=1, column=0, columnspan=2, sticky="ew", **pad)

        ttk.Label(interval_frame, text="Minutes:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.minutes_var = tk.IntVar(value=0)
        self.minutes_spin = ttk.Spinbox(interval_frame, from_=0, to=999, width=6, textvariable=self.minutes_var)
        self.minutes_spin.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(interval_frame, text="Seconds:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.seconds_var = tk.IntVar(value=1)
        self.seconds_spin = ttk.Spinbox(interval_frame, from_=0, to=59, width=6, textvariable=self.seconds_var)
        self.seconds_spin.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(interval_frame, text="Milliseconds:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.ms_var = tk.IntVar(value=0)
        self.ms_spin = ttk.Spinbox(interval_frame, from_=0, to=999, width=6, textvariable=self.ms_var)
        self.ms_spin.grid(row=0, column=5, padx=6, pady=4)

        self.randomize_var = tk.BooleanVar(value=False)
        self.randomize_check = ttk.Checkbutton(
            interval_frame,
            text="Human randomization",
            variable=self.randomize_var,
        )
        self.randomize_check.grid(row=1, column=0, columnspan=6, sticky="w", padx=6, pady=(0, 6))

        # --- Click Options (key, type, location) ---
        options_frame = ttk.LabelFrame(self.root, text="Click Options")
        options_frame.grid(row=2, column=0, columnspan=2, sticky="ew", **pad)

        ttk.Label(options_frame, text="Key to press:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.key_var = tk.StringVar(value="Left Click")
        self.key_combo = ttk.Combobox(
            options_frame,
            textvariable=self.key_var,
            values=ALL_KEYS,
            state="readonly",
            width=18,
        )
        self.key_combo.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(options_frame, text="Click type:").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.click_type_var = tk.StringVar(value="Single Click")
        self.click_type_combo = ttk.Combobox(
            options_frame,
            textvariable=self.click_type_var,
            values=CLICK_TYPES,
            state="readonly",
            width=14,
        )
        self.click_type_combo.grid(row=0, column=3, padx=6, pady=6)

        self.hold_var = tk.BooleanVar(value=False)
        self.hold_check = ttk.Checkbutton(
            options_frame,
            text="Hold down",
            variable=self.hold_var,
            command=self._set_hold_widgets,
        )
        self.hold_check.grid(row=1, column=0, sticky="w", padx=6, pady=(2, 6))

        hold_ms_frame = ttk.Frame(options_frame)
        hold_ms_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=(12, 6), pady=(2, 6))
        ttk.Label(hold_ms_frame, text="Hold (ms):").pack(side="left")
        self.hold_ms_var = tk.IntVar(value=500)
        self.hold_ms_spin = ttk.Spinbox(hold_ms_frame, from_=1, to=99999, width=7, textvariable=self.hold_ms_var)
        self.hold_ms_spin.pack(side="left", padx=(4, 0))

        self._set_hold_widgets()

        self.fixed_location_var = tk.BooleanVar(value=False)
        self.fixed_location_check = ttk.Checkbutton(
            options_frame,
            text="Fixed position",
            variable=self.fixed_location_var,
            command=self._set_fixed_location_widgets,
        )
        self.fixed_location_check.grid(row=2, column=0, sticky="w", padx=6, pady=(2, 6))

        xy_frame = ttk.Frame(options_frame)
        xy_frame.grid(row=2, column=1, columnspan=3, sticky="w", padx=(12, 6), pady=(2, 6))
        ttk.Label(xy_frame, text="X:").pack(side="left")
        self.location_x_var = tk.IntVar(value=0)
        self.location_x_spin = ttk.Spinbox(xy_frame, from_=0, to=99999, width=7, textvariable=self.location_x_var)
        self.location_x_spin.pack(side="left", padx=(4, 16))
        ttk.Label(xy_frame, text="Y:").pack(side="left")
        self.location_y_var = tk.IntVar(value=0)
        self.location_y_spin = ttk.Spinbox(xy_frame, from_=0, to=99999, width=7, textvariable=self.location_y_var)
        self.location_y_spin.pack(side="left", padx=(4, 0))

        self._set_fixed_location_widgets()

        # --- Repeat Limit ---

        repeat_frame = ttk.LabelFrame(self.root, text="Repeat Limit")
        repeat_frame.grid(row=3, column=0, columnspan=2, sticky="ew", **pad)

        self.repeat_limit_var = tk.BooleanVar(value=False)
        self.repeat_limit_check = ttk.Checkbutton(
            repeat_frame,
            text="Limit repeats",
            variable=self.repeat_limit_var,
            command=self._set_repeat_limit_widgets,
        )
        self.repeat_limit_check.grid(row=0, column=0, columnspan=4, sticky="w", padx=6, pady=(6, 2))

        self.repeat_mode_var = tk.StringVar(value="clicks")

        # Mode: click count
        self.repeat_radio_clicks = ttk.Radiobutton(
            repeat_frame, text="Number of clicks:", variable=self.repeat_mode_var,
            value="clicks", command=self._set_repeat_mode_widgets,
        )
        self.repeat_radio_clicks.grid(row=1, column=0, sticky="w", padx=(18, 4), pady=2)
        self.repeat_clicks_var = tk.IntVar(value=10)
        self.repeat_clicks_spin = ttk.Spinbox(
            repeat_frame, from_=1, to=999999, width=8, textvariable=self.repeat_clicks_var
        )
        self.repeat_clicks_spin.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        # Mode: run for duration
        self.repeat_radio_duration = ttk.Radiobutton(
            repeat_frame, text="Run for:", variable=self.repeat_mode_var,
            value="duration", command=self._set_repeat_mode_widgets,
        )
        self.repeat_radio_duration.grid(row=3, column=0, sticky="w", padx=(18, 4), pady=(2, 8))

        duration_inner = ttk.Frame(repeat_frame)
        duration_inner.grid(row=3, column=1, columnspan=3, sticky="w", pady=(2, 8))

        self.dur_hours_var   = tk.IntVar(value=0)
        self.dur_minutes_var = tk.IntVar(value=0)
        self.dur_seconds_var = tk.IntVar(value=30)

        self.dur_hours_spin  = ttk.Spinbox(duration_inner, from_=0, to=999, width=5, textvariable=self.dur_hours_var)
        self.dur_hours_spin.grid(row=0, column=0, padx=(0, 2))
        ttk.Label(duration_inner, text="h").grid(row=0, column=1, padx=(0, 6))
        self.dur_minutes_spin = ttk.Spinbox(duration_inner, from_=0, to=59, width=4, textvariable=self.dur_minutes_var)
        self.dur_minutes_spin.grid(row=0, column=2, padx=(0, 2))
        ttk.Label(duration_inner, text="m").grid(row=0, column=3, padx=(0, 6))
        self.dur_seconds_spin = ttk.Spinbox(duration_inner, from_=0, to=59, width=4, textvariable=self.dur_seconds_var)
        self.dur_seconds_spin.grid(row=0, column=4, padx=(0, 2))
        ttk.Label(duration_inner, text="s").grid(row=0, column=5)

        self._duration_widgets = [self.dur_hours_spin, self.dur_minutes_spin, self.dur_seconds_spin]

        self._set_repeat_limit_widgets()

        # --- Controls ---
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(4, 12))

        self.start_btn = ttk.Button(control_frame, text="Start", command=self._on_start)
        self.start_btn.grid(row=0, column=0, padx=12)

        self.stop_btn = ttk.Button(control_frame, text="Stop (esc)", command=self._on_stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=12)

        # --- Footer ---
        footer_frame = ttk.Frame(self.root)
        footer_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 6))
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(1, weight=1)

        ttk.Label(footer_frame, text="Created by Benjamin Manwell", foreground="gray", font=("TkDefaultFont", 7)).grid(row=0, column=0, sticky="w")
        ttk.Label(footer_frame, text="v1.0.0", foreground="gray", font=("TkDefaultFont", 7)).grid(row=0, column=1, sticky="e")

    # --- Helpers ---

    def _update_mouse_pos(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.mouse_pos_var.set(f"X: {x}   Y: {y}")
        self.root.after(50, self._update_mouse_pos)

    def _update_click_count(self):
        self.click_count_var.set(f"Clicks: {ClickController.numberOfClicks}")
        self.root.after(50, self._update_click_count)

    def _set_hold_widgets(self):
        state = "normal" if self.hold_var.get() else "disabled"
        self.hold_ms_spin.configure(state=state)

    def _set_fixed_location_widgets(self):
        state = "normal" if self.fixed_location_var.get() else "disabled"
        self.location_x_spin.configure(state=state)
        self.location_y_spin.configure(state=state)

    def _set_repeat_limit_widgets(self):
        enabled = self.repeat_limit_var.get()
        radio_state = "normal" if enabled else "disabled"
        self.repeat_radio_clicks.configure(state=radio_state)
        self.repeat_radio_duration.configure(state=radio_state)
        if enabled:
            self._set_repeat_mode_widgets()
        else:
            self.repeat_clicks_spin.configure(state="disabled")
            for w in self._duration_widgets:
                w.configure(state="disabled")

    def _set_repeat_mode_widgets(self):
        mode = self.repeat_mode_var.get()
        self.repeat_clicks_spin.configure(state="normal" if mode == "clicks" else "disabled")
        dt_state = "normal" if mode == "datetime" else "disabled"
        dur_state = "normal" if mode == "duration" else "disabled"
        for w in self._duration_widgets:
            w.configure(state=dur_state)

    # --- Signal handlers ---

    def _on_start(self):
        settings: dict = {}

        # settings["minutes"] = self.minutes_var.get()                # 0
        # settings["seconds"] = self.seconds_var.get()                # 1
        # settings["milliseconds"] = self.ms_var.get()                # 500
        # settings["randomize"] = self.randomize_var.get()
        
        settings["waitTime"] = (self.minutes_var.get() * 60) + self.seconds_var.get() + (self.ms_var.get() / 1000.0)
        settings["humanRandomize"] = self.randomize_var.get()

        settings["key"] = self.key_var.get()                        # "Left Click"
        settings["clickType"] = self.click_type_var.get()           # "Single Click"
        settings["hold"] = self.hold_var.get()                      # False
        settings["holdMs"] = self.hold_ms_var.get()                 # 500
        settings["fixedPos"] = self.fixed_location_var.get()        # False
        settings["locationX"] = self.location_x_var.get()           # 960
        settings["locationY"] = self.location_y_var.get()           # 540

        settings["limitRepeats"] = self.repeat_limit_var.get()      # True
        settings["repeatMode"] = self.repeat_mode_var.get()         # "clicks" | "duration"

        settings["repeatClicks"] = self.repeat_clicks_var.get()     # 10

        settings["durationLimit"] = (self.dur_hours_var.get() * 60 * 60) + (self.dur_minutes_var.get() * 60) + self.dur_seconds_var.get()

        # settings["repeatDurHours"] = self.dur_hours_var.get()       # 0
        # settings["repeatDurMinutes"] = self.dur_minutes_var.get()   # 5
        # settings["repeatDurSeconds"] = self.dur_seconds_var.get()   # 30

        threading.Thread(target=self._listenForStop, daemon=True).start()

        ClickController.start(settings)

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="enabled")

    def _on_stop(self):
        ClickController.stop()
        self.start_btn.config(state="enabled")
        self.stop_btn.config(state="disabled")
    
    def _listenForStop(self):
        while not ClickController.shouldStop:
            if keyboard.is_pressed("esc"):
                break
        self._on_stop()
