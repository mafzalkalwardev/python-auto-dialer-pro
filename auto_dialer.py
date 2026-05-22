import pandas as pd
import pyautogui
import time
import random
from datetime import datetime
import csv
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pynput import keyboard

# ===== CONFIG ===== #
TYPE_DELAY = 0.05
CALL_DURATION = 15  # seconds per call

NUMBER_FIELD = (1514, 315)
CALL_BUTTON = (1848, 309)
END_CALL_BUTTON = (1693, 934)

LOG_FILE = "call_logs.csv"

pyautogui.FAILSAFE = True

# ===== GLOBAL STATE ===== #
contacts = []
current_index = 0
running = False
paused = False
call_active = False
start_time = None


# ===== UTIL ===== #
def human_delay(a=0.2, b=0.4):
    time.sleep(random.uniform(a, b))


def click_safe(pos, clicks=1):
    pyautogui.click(pos[0], pos[1], clicks=clicks)
    human_delay()


# ===== LOG SYSTEM ===== #
def log_call(number, status):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Time", "Phone", "Status"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            number,
            status
        ])


def get_completed_numbers():
    if not os.path.exists(LOG_FILE):
        return set()

    completed = set()

    with open(LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Status"] == "ENDED":
                completed.add(row["Phone"])

    return completed


# ===== CORE CALL ===== #
def make_call(number):
    global call_active, start_time

    formatted = f"+1{number}"

    click_safe(NUMBER_FIELD, 2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')

    pyautogui.write(formatted, interval=TYPE_DELAY)
    click_safe(CALL_BUTTON, 2)

    call_active = True
    start_time = time.time()

    log_call(formatted, "STARTED")


def hangup_call():
    global call_active

    if call_active:
        click_safe(END_CALL_BUTTON)
        call_active = False


# ===== LOAD DATA ===== #
def load_excel():
    global contacts

    file = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
    if not file:
        return

    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    possible = ['Phone', 'phone', 'PHONE', 'Phone Number', 'Mobile', 'Number']
    col = next((c for c in df.columns if c in possible), None)

    if not col:
        messagebox.showerror("Error", "No phone column found")
        return

    df = df[df[col].notna()]
    df[col] = df[col].astype(str).str.replace(r'\D+', '', regex=True)

    numbers = [p for p in df[col] if len(p) == 10]

    completed = get_completed_numbers()

    contacts.clear()
    for n in numbers:
        if f"+1{n}" not in completed:
            contacts.append(n)

    status_label.config(text=f"Loaded {len(contacts)} numbers (after resume)")
    log("Loaded contacts with resume filter")


# ===== UI HELPERS ===== #
def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def update_status():
    if running and current_index < len(contacts):
        progress = f"{current_index+1}/{len(contacts)}"
        status_label.config(text=f"Calling... {progress}")

        progress_bar["value"] = (current_index / len(contacts)) * 100

    root.after(500, update_status)


def update_timer():
    if call_active and start_time:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"⏱ {elapsed}s")
    else:
        timer_label.config(text="⏱ 0s")

    root.after(500, update_timer)


# ===== CALL LOOP ===== #
def call_loop():
    global current_index, running, paused

    while running and current_index < len(contacts):

        while paused:
            time.sleep(0.5)

        number = contacts[current_index]

        log(f"📞 Calling {number}")
        make_call(number)

        for _ in range(CALL_DURATION):
            if not running:
                return
            while paused:
                time.sleep(0.5)
            time.sleep(1)

        hangup_call()
        log_call(f"+1{number}", "ENDED")

        current_index += 1

    running = False
    log("✅ Finished all calls")


# ===== CONTROLS ===== #
def start():
    global running, current_index

    if not contacts:
        messagebox.showwarning("Warning", "Load Excel first")
        return

    running = True
    current_index = 0

    threading.Thread(target=call_loop, daemon=True).start()


def stop():
    global running
    running = False
    hangup_call()
    log("⛔ Stopped")


# ===== GLOBAL HOTKEYS ===== #
def on_press(key):
    global paused, running, current_index

    try:
        if key.char.lower() == 'x':
            log("⌨️ X → Next Call")
            hangup_call()

            if running:
                log_call(f"+1{contacts[current_index]}", "ENDED")
                current_index += 1

    except:
        pass

    if key == keyboard.Key.space:
        paused = not paused
        log("⏸ Paused" if paused else "▶️ Resumed")


listener = keyboard.Listener(on_press=on_press)
listener.start()


# ===== UI ===== #
root = tk.Tk()
root.title("Auto Dialer Pro")
root.geometry("550x600")

tk.Label(root, text="📞 Auto Dialer", font=("Arial", 18)).pack(pady=10)

tk.Button(root, text="Load Excel", command=load_excel).pack(pady=5)
tk.Button(root, text="Start", bg="green", fg="white", command=start).pack(pady=5)
tk.Button(root, text="Stop", bg="red", fg="white", command=stop).pack(pady=5)

status_label = tk.Label(root, text="Idle")
status_label.pack(pady=5)

timer_label = tk.Label(root, text="⏱ 0s")
timer_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, length=400)
progress_bar.pack(pady=10)

log_box = tk.Text(root, height=20)
log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

update_status()
update_timer()

root.mainloop()