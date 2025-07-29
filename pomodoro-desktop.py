import tkinter as tk
from tkinter import ttk
import sv_ttk
import pywinstyles
import sys
import itertools
from countdown_timer import CountdownTimer

root = tk.Tk()
root.title("PD")
root.iconbitmap("./assets/tomato.ico")
root.geometry("250x225")

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

sv_ttk.set_theme("dark")
apply_theme_to_titlebar(root)

label_status = ttk.Label(root, text="", font=("Consolas", 24), justify="left")
label_status.state(["disabled"])
label_status.pack(padx=5, pady=5)

label_var = tk.StringVar(value="Ready")
label = ttk.Label(root, textvariable=label_var, font=("Consolas", 36), anchor="center")
label.pack(padx=5, pady=5)

frame = ttk.Frame(root)
frame.pack()

# Instantiate the timer
timer = CountdownTimer(label_var, root)
stage1_duration = 0
stage2_duration = 0

working_animation_chars = ('🌚', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌑')
cycler = itertools.cycle(working_animation_chars)

# Stage control
timer_stage = 1

def start_timer_cycle(stage1_minutes, stage2_minutes):
    global timer_stage, stage1_duration, stage2_duration
    timer_stage = 1
    label_status.config(text="Working....")
    label_status.state(["!disabled"])
    stage1_duration = stage1_minutes
    stage2_duration = stage2_minutes
    timer.reset(stage1_duration)
    timer.start()

def on_timer_done(event):
    global timer_stage
    if timer_stage == 1:
        timer_stage = 2
        timer.reset(stage2_duration)
        timer.start()
    elif timer_stage == 2:
        label_status.state(["!disabled"])
        label_var.set("Done ✅")
        root.title("PD Done ✅")

def on_timer_tick(event):
    label_status.config(text=next(cycler))
    
    minutes = timer.remaining_seconds // 60
    if timer_stage == 1:
        root.title(f"PD Work {minutes:02}m")
    elif timer_stage == 2:
        root.title(f"PD Break {minutes:02}m")

# Start button
btn_25_5 = ttk.Button(frame, text="25m Work / 5m Break", command=lambda: start_timer_cycle(25, 5))
btn_25_15 = ttk.Button(frame, text="25m Work / 15m Break", command=lambda: start_timer_cycle(25, 15))

btn_25_5.grid(row=0, column=0, padx=10, pady=10)
btn_25_15.grid(row=1, column=0, padx=10, pady=10)

# Event binding
root.bind("<<TimerDone>>", on_timer_done)
root.bind("<<TimerTick>>", on_timer_tick)

root.mainloop()