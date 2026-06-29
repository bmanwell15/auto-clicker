# Auto Clicker

**Version 1.0.1**

A lightweight Windows auto clicker with a simple GUI. Supports mouse buttons and keyboard keys, configurable intervals, repeat limits, and fixed click positions. The entire app runs on a single thread using tkinter's event loop — no background worker threads.

---

## Running from source

**Requirements:** Python 3.8+

```
pip install pyautogui keyboard
```

```
cd src
python main.py
```

---

## Building a standalone executable

Run this from inside the `src/` directory:

```
python -m PyInstaller --onefile --noconsole --optimize 2 --icon Pointer.ico --add-data "Pointer.ico;." main.py
```

The output `.exe` will be in `src/dist/`.

| Flag | Purpose |
|------|---------|
| `--onefile` | Bundle everything into a single `.exe` |
| `--noconsole` | Suppress the terminal window at launch |
| `--optimize 2` | Strip assertions and docstrings from bytecode for a smaller bundle |
| `--icon Pointer.ico` | Set the `.exe` file icon shown in Explorer |
| `--add-data "Pointer.ico;."` | Bundle the icon file so the window icon works at runtime |

---

## Settings

### Status bar

A status bar runs along the top of the window:

- **Clicks (top-left)** — a live counter of how many clicks/keypresses have been performed in the current run. Resets to 0 each time you start.
- **X / Y (top-right)** — a live readout of the current screen-absolute cursor position, updated every 50 ms. Useful for finding the exact coordinates to use with Fixed Position.

---

### Click Interval

How long to wait between each click/keypress.

| Field | Description |
|-------|-------------|
| **Minutes** | Whole minutes to wait (0–999) |
| **Seconds** | Additional seconds (0–59) |
| **Milliseconds** | Additional milliseconds (0–999) |

**Human randomization** — when checked, makes the auto clicker behave less mechanically in two ways:

- The wait between clicks gets a random offset of up to ±1 second.
- Each mouse click's target lands within ±1 pixel of the intended X/Y position.

This applies to both cursor-following and fixed-position clicks. (Position jitter only affects mouse clicks, since keyboard presses have no coordinates.)

---

### Click Options

#### Key to press
A dropdown containing every keyboard key as well as **Left Click**, **Right Click**, and **Middle Click**. This is what gets pressed on each interval.

#### Click type
Controls how many times the key or button is activated per interval.

| Option | Behaviour |
|--------|-----------|
| **Single Click** | One press per interval |
| **Double Click** | Two rapid presses per interval |
| **Triple Click** | Three rapid presses per interval |

> Click type only applies to mouse buttons (Left/Right/Middle Click). Keyboard keys always produce a single keypress regardless of this setting.

#### Hold down
When checked, the button is held for the specified number of milliseconds before being released, instead of a normal click. The **Hold (ms)** field sets the hold duration (1–99999 ms).

#### Fixed position
When checked, every click is sent to a specific screen coordinate instead of wherever the cursor happens to be. Set the **X** and **Y** fields to the target pixel position.

Use the live coordinate display in the top-right corner to find the coordinates of the position you want to click.

---

### Repeat Limit

By default the auto clicker runs indefinitely until stopped. Check **Limit repeats** to enable one of these stop conditions:

| Mode | Description |
|------|-------------|
| **Number of clicks** | Stop after the specified number of clicks/keypresses |
| **Run for** | Stop after a set duration (hours, minutes, seconds) |

---

## Starting and stopping

- **Start (F6)** — begins the auto clicker with the current settings. The Start button disables while running. You can also press **F6** on the keyboard.
- **Stop (F7)** — halts the auto clicker immediately. You can also press **F7** on the keyboard.

The F6/F7 hotkeys work globally, so you can start and stop the clicker without the window focused.
