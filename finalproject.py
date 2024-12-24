import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random


sound_speed = 340 
source_position = 0  
observer_position = 0  
wavefronts = []  
running = False  
challenge_active = False  
try_count = 0  
target_frequency = 0  
challenge_params = {}  
mach_wave_dynamic_running = False   
mach_wave_step = 0 

def doppler_effect(frequency, source_v, observer_v):
    if abs(source_v) >= sound_speed:
        return None  
    return frequency * ((sound_speed + observer_v) / (sound_speed - source_v))


def initialize_display():
    global wavefronts, source_position, observer_position
    source_position = 0
    observer_position = 0
    wavefronts = []  
    frequency = freq_slider.get()
    for i in range(10): 
        wavefronts.append([source_position, 0, i * sound_speed / frequency])
    update_plot(initial=True)


def update_plot(initial=False):
    global source_position, observer_position, running, wavefronts, mach_wave_dynamic_running, mach_wave_step
    source_velocity = source_slider.get()
    observer_velocity = observer_slider.get()
    frequency = freq_slider.get()

    if abs(source_velocity) > sound_speed:
        if not mach_wave_dynamic_running:
            mach_wave_dynamic_running = True
            mach_wave_step = 0
        result_label.config(text="观察到的频率: 超音波!")
        draw_dynamic_mach_wave(source_velocity)
        return

    if abs(source_velocity) == sound_speed:
        draw_sonic_boom()
        result_label.config(text="观察到的频率: 音爆!")
        return

    if abs(source_velocity) < sound_speed:
        observed_frequency = doppler_effect(frequency, source_velocity, observer_velocity)
        result_label.config(text=f"观察到的频率: {observed_frequency:.2f} Hz")

    if running and not initial:
        source_position += source_velocity * 0.01
        observer_position += observer_velocity * 0.01
        wavefronts.append([source_position, 0, sound_speed / frequency])

        for wave in wavefronts:
            wave[2] += sound_speed * 0.01

    elif not running:
        wavefronts = [[source_position, 0, i * sound_speed / frequency] for i in range(10)]

    ax.clear()

    theta = np.linspace(0, 2 * np.pi, 100)
    for x, y, radius in wavefronts[-10:]:
        wave_x = radius * np.cos(theta)
        wave_y = radius * np.sin(theta)
        ax.plot(wave_x + x, wave_y + y, 'g', alpha=0.6)

    ax.scatter(source_position, 0, color='red', label="Source")
    ax.scatter(observer_position, 0, color='blue', label="Observer")
    ax.legend()
    ax.axis([-10, 10, -10, 10])
    canvas.draw_idle()

    if running or initial:
        root.after(100, update_plot)

def start_simulation():
    global running, wavefronts
    running = True
    wavefronts = [] 
    freq_slider.config(state="disabled")
    source_slider.config(state="disabled")
    observer_slider.config(state="disabled")
    update_plot()


def start_challenge():
    global challenge_active, try_count, target_frequency, challenge_params
    challenge_active = True
    try_count = 0
    source_velocity = random.randint(10, 350)
    observer_velocity = random.randint(-150, 150)
    base_frequency = random.randint(200, 800)
    target_frequency = doppler_effect(base_frequency, source_velocity, observer_velocity)
    challenge_params = {
        "source_velocity": source_velocity,
        "observer_velocity": observer_velocity,
        "base_frequency": base_frequency,
        "target_frequency": target_frequency,}

    challenge_label.config(
        text=f"挑战已开始！\n声源频率: {base_frequency} Hz\n声源速度: {source_velocity} m/s\n观察者速度: {observer_velocity} m/s")
    freq_slider.config(state="disabled")
    source_slider.config(state="disabled")
    observer_slider.config(state="disabled")


def check_challenge():
    global try_count, challenge_params
    try:
        user_frequency = float(challenge_entry.get())
        if abs(user_frequency - challenge_params["target_frequency"]) < 1:
            challenge_label.config(text="WIN", fg="green")
            display_challenge_result()
        else:
            try_count += 1
            if try_count < 3:
                challenge_label.config(
                    text=f"请再试一次 (剩余尝试次数: {3 - try_count})\n"
                         f"声源频率: {challenge_params['base_frequency']} Hz\n"
                         f"声源速度: {challenge_params['source_velocity']} m/s\n"
                         f"观察者速度: {challenge_params['observer_velocity']} m/s", fg="red"
                )
            else:
                challenge_label.config(
                    text=f"失败！正确答案是: {challenge_params['target_frequency']:.2f} Hz",
                    fg="blue",
                )
                challenge_active = False
    except ValueError:
        challenge_label.config(text="无效输入，请输入数字。", fg="red")


def display_challenge_result():
    ax.clear()
    base_frequency = challenge_params["base_frequency"]
    source_velocity = challenge_params["source_velocity"]
    observer_velocity = challenge_params["observer_velocity"]

    for i in range(10):
        radius = 0.5 * (i + 1)
        theta = np.linspace(0, 2 * np.pi, 100)
        x = radius * np.cos(theta) - source_velocity * 0.01 * i
        y = radius * np.sin(theta)
        ax.plot(x, y, 'g', alpha=0.6)

    ax.scatter(0, 0, color='red', label=f"Source ({source_velocity} m/s)")
    ax.scatter(observer_velocity * 0.01 * 10, 0, color='blue', label=f"Observer ({observer_velocity} m/s)")

    ax.axis("equal")
    ax.legend()
    ax.set_title(f"Challenge Result\nFrequency: {base_frequency} Hz")
    canvas.draw_idle()


def draw_dynamic_mach_wave(source_velocity):
    global mach_wave_step, mach_wave_dynamic_running
    ax.clear()

    mach_angle = np.arcsin(sound_speed / abs(source_velocity))
    for i in range(mach_wave_step):
        radius = 0.5 * (i + 1)
        theta = np.linspace(-mach_angle, mach_angle, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        ax.plot(x, y, 'r', alpha=0.6)
        ax.plot(x, -y, 'r', alpha=0.6)

    ax.plot([0, 10 * np.cos(mach_angle)], [0, 10 * np.sin(mach_angle)], 'g--', label=f"Mach Angle: {np.degrees(mach_angle):.2f}°")
    ax.plot([0, 10 * np.cos(mach_angle)], [0, -10 * np.sin(mach_angle)], 'g--')
    ax.scatter(0, 0, color='red', label="Source")

    ax.axis("equal")
    ax.legend()
    ax.set_title("Dynamic Mach Wave")
    canvas.draw_idle()

    if mach_wave_step < 10:
        mach_wave_step += 1
        root.after(300, lambda: draw_dynamic_mach_wave(source_velocity))
    else:
        mach_wave_dynamic_running = False


def draw_sonic_boom():
    ax.clear()
    for i in range(10):
        radius = 0.5 * (i + 1)
        offset = radius * 0.9
        theta = np.linspace(0, 2 * np.pi, 100)
        x = offset + radius * np.cos(theta)
        y = radius * np.sin(theta)
        ax.plot(x, y, 'b', alpha=0.6)
    ax.scatter(0, 0, color='red', label="Source")
    ax.axis("equal")
    ax.legend()
    ax.set_title("Sonic Boom")
    canvas.draw_idle()


def draw_mach_wave(source_velocity):
    ax.clear()
    mach_angle = np.arcsin(sound_speed / abs(source_velocity))
    for i in range(10):
        radius = 0.5 * (i + 1)
        theta = np.linspace(-mach_angle, mach_angle, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        ax.plot(x, y, 'r', alpha=0.6)
        ax.plot(x, -y, 'r', alpha=0.6)
    ax.plot([0, 10 * np.cos(mach_angle)], [0, 10 * np.sin(mach_angle)], 'g--', label=f"Mach Angle: {np.degrees(mach_angle):.2f}°")
    ax.plot([0, 10 * np.cos(mach_angle)], [0, -10 * np.sin(mach_angle)], 'g--')
    ax.scatter(0, 0, color='red', label="Source")
    ax.axis("equal")
    ax.legend()
    ax.set_title("Mach Wave")
    canvas.draw_idle()


def reset_all():
    global running, challenge_active, try_count, wavefronts, source_position, observer_position, mach_wave_dynamic_running, mach_wave_step
    running = False
    mach_wave_dynamic_running = False
    try_count = 0
    source_position = 0
    observer_position = 0
    wavefronts = []
    mach_wave_step = 0

    pending_after_calls = root.tk.call("after", "info")
    for job in pending_after_calls:
        try:
            root.after_cancel(job)
        except Exception:
            pass

    freq_slider.set(440)
    source_slider.set(0)
    observer_slider.set(0)
    source_velocity_entry.delete(0, tk.END)
    observer_velocity_entry.delete(0, tk.END)
    freq_entry.delete(0, tk.END)
    challenge_entry.delete(0, tk.END)

    challenge_label.config(text="")
    result_label.config(text="观察到的频率: -- Hz")

    initialize_display()

    freq_slider.config(state="normal")
    source_slider.config(state="normal")
    observer_slider.config(state="normal")


root = tk.Tk()
root.title("多普勒效应模拟器 - 挑战模式")

def on_frequency_change(val):
    if not running:
        initialize_display()

tk.Label(root, text="声源频率 (Hz)").grid(row=0, column=0)
freq_slider = tk.Scale(root, from_=100, to=1000, orient=tk.HORIZONTAL, length=300, command=on_frequency_change)
freq_slider.set(440)
freq_slider.grid(row=0, column=1)

freq_entry = tk.Entry(root)
freq_entry.grid(row=0, column=2)
freq_button = tk.Button(root, text="设置频率", command=lambda: freq_slider.set(int(freq_entry.get())))
freq_button.grid(row=0, column=3)

tk.Label(root, text="声源速度 (m/s)").grid(row=1, column=0)
source_slider = tk.Scale(root, from_=-400, to=400, orient=tk.HORIZONTAL, length=300)
source_slider.set(0)
source_slider.grid(row=1, column=1)

source_velocity_entry = tk.Entry(root)
source_velocity_entry.grid(row=1, column=2)
source_velocity_button = tk.Button(root, text="设置速度", command=lambda: source_slider.set(int(source_velocity_entry.get())))
source_velocity_button.grid(row=1, column=3)

tk.Label(root, text="观察者速度 (m/s)").grid(row=2, column=0)
observer_slider = tk.Scale(root, from_=-350, to=350, orient=tk.HORIZONTAL, length=300)
observer_slider.set(0)
observer_slider.grid(row=2, column=1)

observer_velocity_entry = tk.Entry(root)
observer_velocity_entry.grid(row=2, column=2)
observer_velocity_button = tk.Button(root, text="设置速度", command=lambda: observer_slider.set(int(observer_velocity_entry.get())))
observer_velocity_button.grid(row=2, column=3)

result_label = tk.Label(root, text="观察到的频率: -- Hz", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2)

start_button = tk.Button(root, text="开始", command=start_simulation)
start_button.grid(row=4, column=0)

challenge_button = tk.Button(root, text="开始挑战", command=start_challenge)
challenge_button.grid(row=4, column=1)

reset_button = tk.Button(root, text="重置", command=reset_all)
reset_button.grid(row=4, column=2)

tk.Label(root, text="输入答案: ").grid(row=5, column=0)
challenge_entry = tk.Entry(root)
challenge_entry.grid(row=5, column=1)

check_button = tk.Button(root, text="验证答案", command=check_challenge)
check_button.grid(row=5, column=2)

challenge_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
challenge_label.grid(row=6, column=0, columnspan=4)

fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=7, column=0, columnspan=4)

initialize_display()
root.mainloop()
