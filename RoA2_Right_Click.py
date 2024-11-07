import pyautogui
import time
from datetime import datetime
import tkinter as tk
from threading import Thread, Event
import keyboard  # Keep keyboard for hotkey functionality only

# Control flags
running = False
started_once = False 
stop_event = Event()
main_thread = None

def log(message):
    """Logs messages with a timestamp."""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def press_right():
    """Presses the right mouse button."""
    pyautogui.mouseDown(button='right')
    time.sleep(0.01) 
    pyautogui.mouseUp(button='right')
    pyautogui.mouseDown(button='right')
    time.sleep(0.01)
    pyautogui.mouseUp(button='right')
    pyautogui.mouseDown(button='right')
    time.sleep(0.01) 
    pyautogui.mouseUp(button='right')
    log("Right-click pressed")

def main_loop():
    """Main loop that presses right click with specified intervals."""
    global started_once
    if not started_once:
        log("Initial 5-second delay before loop starts")
        time.sleep(5)
        started_once = True

    while not stop_event.is_set():
        press_right()
        
        time.sleep(1)
        
        if stop_event.is_set(): break
        
        press_right()
        
        log("Starting 500-second wait")
        for i in range(1, 18): 
            time.sleep(30)
            if stop_event.is_set():
                log("Loop stopped during 500-second wait")
                return  # Exit if stopped during wait
            log(f"Waiting... {i * 30} seconds elapsed")

        press_right()
        if stop_event.is_set(): break

        time.sleep(1)

def toggle_script():
    global running, main_thread

    if running:
        running = False
        stop_event.set()
        log("Script stopped")
        start_stop_button.config(text="Start")
    else:
        running = True
        stop_event.clear()
        log("Script started")
        start_stop_button.config(text="Stop")
        main_thread = Thread(target=main_loop)
        main_thread.start()

def on_start_stop_button():
    toggle_script()

def update_button_label():
    start_stop_button.config(text="Stop" if running else "Start")

def setup_gui():
    global start_stop_button

    root = tk.Tk()
    root.title("RoA2")

    instructions = tk.Label(root, text="Press Ctrl+7 to Start/Stop\nOr use the button below.")
    instructions.pack(pady=10)

    start_stop_button = tk.Button(root, text="Start", command=on_start_stop_button)
    start_stop_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", root.quit) 
    root.mainloop()

# Use keyboard library's hotkey setup for toggling the script
keyboard.add_hotkey('ctrl+7', toggle_script)

log("Starting GUI... Press Ctrl+7 to start/stop.")

setup_gui()
