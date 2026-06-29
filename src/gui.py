import tkinter as tk
from tkinter import ttk
import keyboard
import sys
import os
from ClickController import ClickController

VERSION_NUMBER = "v1.0.1"

def _resource(relativePath):
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, relativePath)

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

        self._buildUi()

    def _buildUi(self):
        pad = {"padx": 10, "pady": 6}

        # --- Top bar: click counter (left) and mouse position (right) ---
        self.clickCountVar = tk.StringVar(value="Clicks: 0")
        ttk.Label(self.root, textvariable=self.clickCountVar).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(6, 0))

        self.mousePosVar = tk.StringVar(value="X: 0   Y: 0")
        ttk.Label(self.root, textvariable=self.mousePosVar).grid(row=0, column=0, columnspan=2, sticky="e", padx=12, pady=(6, 0))
        self._updateMousePos()
        self._updateClickCount()
        self._pollHotkeys()

        # --- Click Interval ---
        intervalFrame = ttk.LabelFrame(self.root, text="Click Interval")
        intervalFrame.grid(row=1, column=0, columnspan=2, sticky="ew", **pad)

        ttk.Label(intervalFrame, text="Minutes:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.minutesVar = tk.IntVar(value=0)
        self.minutesSpin = ttk.Spinbox(intervalFrame, from_=0, to=999, width=6, textvariable=self.minutesVar)
        self.minutesSpin.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(intervalFrame, text="Seconds:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.secondsVar = tk.IntVar(value=1)
        self.secondsSpin = ttk.Spinbox(intervalFrame, from_=0, to=59, width=6, textvariable=self.secondsVar)
        self.secondsSpin.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(intervalFrame, text="Milliseconds:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.msVar = tk.IntVar(value=0)
        self.msSpin = ttk.Spinbox(intervalFrame, from_=0, to=999, width=6, textvariable=self.msVar)
        self.msSpin.grid(row=0, column=5, padx=6, pady=4)

        self.randomizeVar = tk.BooleanVar(value=False)
        self.randomizeCheck = ttk.Checkbutton(
            intervalFrame,
            text="Human randomization",
            variable=self.randomizeVar,
        )
        self.randomizeCheck.grid(row=1, column=0, columnspan=6, sticky="w", padx=6, pady=(0, 6))

        # --- Click Options (key, type, location) ---
        optionsFrame = ttk.LabelFrame(self.root, text="Click Options")
        optionsFrame.grid(row=2, column=0, columnspan=2, sticky="ew", **pad)

        ttk.Label(optionsFrame, text="Key to press:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.keyVar = tk.StringVar(value="Left Click")
        self.keyCombo = ttk.Combobox(
            optionsFrame,
            textvariable=self.keyVar,
            values=ALL_KEYS,
            state="readonly",
            width=18,
        )
        self.keyCombo.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(optionsFrame, text="Click type:").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.clickTypeVar = tk.StringVar(value="Single Click")
        self.clickTypeCombo = ttk.Combobox(
            optionsFrame,
            textvariable=self.clickTypeVar,
            values=CLICK_TYPES,
            state="readonly",
            width=14,
        )
        self.clickTypeCombo.grid(row=0, column=3, padx=6, pady=6)

        self.holdVar = tk.BooleanVar(value=False)
        self.holdCheck = ttk.Checkbutton(
            optionsFrame,
            text="Hold down",
            variable=self.holdVar,
            command=self._setHoldWidgets,
        )
        self.holdCheck.grid(row=1, column=0, sticky="w", padx=6, pady=(2, 6))

        holdMsFrame = ttk.Frame(optionsFrame)
        holdMsFrame.grid(row=1, column=1, columnspan=3, sticky="w", padx=(12, 6), pady=(2, 6))
        ttk.Label(holdMsFrame, text="Hold (ms):").pack(side="left")
        self.holdMsVar = tk.IntVar(value=500)
        self.holdMsSpin = ttk.Spinbox(holdMsFrame, from_=1, to=99999, width=7, textvariable=self.holdMsVar)
        self.holdMsSpin.pack(side="left", padx=(4, 0))

        self._setHoldWidgets()

        self.fixedLocationVar = tk.BooleanVar(value=False)
        self.fixedLocationCheck = ttk.Checkbutton(
            optionsFrame,
            text="Fixed position",
            variable=self.fixedLocationVar,
            command=self._setFixedLocationWidgets,
        )
        self.fixedLocationCheck.grid(row=2, column=0, sticky="w", padx=6, pady=(2, 6))

        xyFrame = ttk.Frame(optionsFrame)
        xyFrame.grid(row=2, column=1, columnspan=3, sticky="w", padx=(12, 6), pady=(2, 6))
        ttk.Label(xyFrame, text="X:").pack(side="left")
        self.locationXVar = tk.IntVar(value=0)
        self.locationXSpin = ttk.Spinbox(xyFrame, from_=0, to=99999, width=7, textvariable=self.locationXVar)
        self.locationXSpin.pack(side="left", padx=(4, 16))
        ttk.Label(xyFrame, text="Y:").pack(side="left")
        self.locationYVar = tk.IntVar(value=0)
        self.locationYSpin = ttk.Spinbox(xyFrame, from_=0, to=99999, width=7, textvariable=self.locationYVar)
        self.locationYSpin.pack(side="left", padx=(4, 0))

        self._setFixedLocationWidgets()

        # --- Repeat Limit ---

        repeatFrame = ttk.LabelFrame(self.root, text="Repeat Limit")
        repeatFrame.grid(row=3, column=0, columnspan=2, sticky="ew", **pad)

        self.repeatLimitVar = tk.BooleanVar(value=False)
        self.repeatLimitCheck = ttk.Checkbutton(
            repeatFrame,
            text="Limit repeats",
            variable=self.repeatLimitVar,
            command=self._setRepeatLimitWidgets,
        )
        self.repeatLimitCheck.grid(row=0, column=0, columnspan=4, sticky="w", padx=6, pady=(6, 2))

        self.repeatModeVar = tk.StringVar(value="clicks")

        # Mode: click count
        self.repeatRadioClicks = ttk.Radiobutton(
            repeatFrame, text="Number of clicks:", variable=self.repeatModeVar,
            value="clicks", command=self._setRepeatModeWidgets,
        )
        self.repeatRadioClicks.grid(row=1, column=0, sticky="w", padx=(18, 4), pady=2)
        self.repeatClicksVar = tk.IntVar(value=10)
        self.repeatClicksSpin = ttk.Spinbox(
            repeatFrame, from_=1, to=999999, width=8, textvariable=self.repeatClicksVar
        )
        self.repeatClicksSpin.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        # Mode: run for duration
        self.repeatRadioDuration = ttk.Radiobutton(
            repeatFrame, text="Run for:", variable=self.repeatModeVar,
            value="duration", command=self._setRepeatModeWidgets,
        )
        self.repeatRadioDuration.grid(row=3, column=0, sticky="w", padx=(18, 4), pady=(2, 8))

        durationInner = ttk.Frame(repeatFrame)
        durationInner.grid(row=3, column=1, columnspan=3, sticky="w", pady=(2, 8))

        self.durHoursVar   = tk.IntVar(value=0)
        self.durMinutesVar = tk.IntVar(value=0)
        self.durSecondsVar = tk.IntVar(value=30)

        self.durHoursSpin  = ttk.Spinbox(durationInner, from_=0, to=999, width=5, textvariable=self.durHoursVar)
        self.durHoursSpin.grid(row=0, column=0, padx=(0, 2))
        ttk.Label(durationInner, text="h").grid(row=0, column=1, padx=(0, 6))
        self.durMinutesSpin = ttk.Spinbox(durationInner, from_=0, to=59, width=4, textvariable=self.durMinutesVar)
        self.durMinutesSpin.grid(row=0, column=2, padx=(0, 2))
        ttk.Label(durationInner, text="m").grid(row=0, column=3, padx=(0, 6))
        self.durSecondsSpin = ttk.Spinbox(durationInner, from_=0, to=59, width=4, textvariable=self.durSecondsVar)
        self.durSecondsSpin.grid(row=0, column=4, padx=(0, 2))
        ttk.Label(durationInner, text="s").grid(row=0, column=5)

        self._durationWidgets = [self.durHoursSpin, self.durMinutesSpin, self.durSecondsSpin]

        self._setRepeatLimitWidgets()

        # --- Controls ---
        controlFrame = ttk.Frame(self.root)
        controlFrame.grid(row=4, column=0, columnspan=2, pady=(4, 12))

        self.startBtn = ttk.Button(controlFrame, text="Start (F6)", command=self._onStart)
        self.startBtn.grid(row=0, column=0, padx=12)

        self.stopBtn = ttk.Button(controlFrame, text="Stop (F7)", command=self._onStop, state="disabled")
        self.stopBtn.grid(row=0, column=1, padx=12)

        # --- Footer ---
        footerFrame = ttk.Frame(self.root)
        footerFrame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 6))
        footerFrame.columnconfigure(0, weight=1)
        footerFrame.columnconfigure(1, weight=1)

        ttk.Label(footerFrame, text="Created by Benjamin Manwell", foreground="gray", font=("TkDefaultFont", 7)).grid(row=0, column=0, sticky="w")
        ttk.Label(footerFrame, text=VERSION_NUMBER, foreground="gray", font=("TkDefaultFont", 7)).grid(row=0, column=1, sticky="e")

    # --- Helpers ---

    def _updateMousePos(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.mousePosVar.set(f"X: {x}   Y: {y}")
        self.root.after(50, self._updateMousePos)

    def _updateClickCount(self):
        self.clickCountVar.set(f"Clicks: {ClickController.numberOfClicks}")
        self.root.after(50, self._updateClickCount)

    def _pollHotkeys(self):
        if not ClickController.shouldStop:
            if keyboard.is_pressed("f7"):
                self._onStop()
        else:
            if keyboard.is_pressed("f6"):
                self._onStart()
        self.root.after(50, self._pollHotkeys)

    def _setHoldWidgets(self):
        state = "normal" if self.holdVar.get() else "disabled"
        self.holdMsSpin.configure(state=state)

    def _setFixedLocationWidgets(self):
        state = "normal" if self.fixedLocationVar.get() else "disabled"
        self.locationXSpin.configure(state=state)
        self.locationYSpin.configure(state=state)

    def _setRepeatLimitWidgets(self):
        enabled = self.repeatLimitVar.get()
        radioState = "normal" if enabled else "disabled"
        self.repeatRadioClicks.configure(state=radioState)
        self.repeatRadioDuration.configure(state=radioState)
        if enabled:
            self._setRepeatModeWidgets()
        else:
            self.repeatClicksSpin.configure(state="disabled")
            for w in self._durationWidgets:
                w.configure(state="disabled")

    def _setRepeatModeWidgets(self):
        mode = self.repeatModeVar.get()
        self.repeatClicksSpin.configure(state="normal" if mode == "clicks" else "disabled")
        durState = "normal" if mode == "duration" else "disabled"
        for w in self._durationWidgets:
            w.configure(state=durState)

    # --- Signal handlers ---

    def _onStart(self):
        settings: dict = {}

        settings["waitTime"] = (self.minutesVar.get() * 60) + self.secondsVar.get() + (self.msVar.get() / 1000.0)
        settings["humanRandomize"] = self.randomizeVar.get()

        settings["key"] = self.keyVar.get()                         # "Left Click"
        settings["clickType"] = self.clickTypeVar.get()            # "Single Click"
        settings["hold"] = self.holdVar.get()                      # False
        settings["holdMs"] = self.holdMsVar.get()                  # 500
        settings["fixedPos"] = self.fixedLocationVar.get()         # False
        settings["locationX"] = self.locationXVar.get()            # 960
        settings["locationY"] = self.locationYVar.get()            # 540

        settings["limitRepeats"] = self.repeatLimitVar.get()       # True
        settings["repeatMode"] = self.repeatModeVar.get()          # "clicks" | "duration" | "datetime"

        settings["repeatClicks"] = self.repeatClicksVar.get()      # 10

        settings["durationLimit"] = (self.durHoursVar.get() * 60 * 60) + (self.durMinutesVar.get() * 60) + self.durSecondsVar.get()

        ClickController.start(self.root, settings)

        self.startBtn.config(state="disabled")
        self.stopBtn.config(state="enabled")

    def _onStop(self):
        ClickController.stop()
        self.startBtn.config(state="normal")
        self.stopBtn.config(state="disabled")
