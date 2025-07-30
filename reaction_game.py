import tkinter as tk
import time
import random

start_time = 0
reaction_time = 0
waiting = False

root = tk.Tk()
root.title("计时反应游戏")

info = tk.StringVar()
info.set("点击开始，等提示后尽快点击！")

label = tk.Label(root, textvariable=info, font=("Arial", 16))
label.pack(pady=20)

result = tk.StringVar()
result.set("")
result_label = tk.Label(root, textvariable=result, font=("Arial", 14), fg='blue')
result_label.pack(pady=10)

btn = tk.Button(root, text="开始", font=("Arial", 14))
btn.pack(pady=20)

# 按钮事件

def start_game():
    global waiting
    info.set("准备...请等待提示！")
    result.set("")
    btn['state'] = 'disabled'
    waiting = True
    root.after(random.randint(1500, 4000), show_go)

def show_go():
    global start_time, waiting
    info.set("现在！快点点击按钮！")
    btn['text'] = "点击!"
    btn['state'] = 'normal'
    start_time = time.time()
    waiting = False

def click_btn():
    global reaction_time, waiting
    if waiting:
        result.set("太快了，还没到提示！")
        return
    reaction_time = time.time() - start_time
    info.set("点击开始，等提示后尽快点击！")
    btn['text'] = "开始"
    btn['state'] = 'normal'
    result.set(f"你的反应时间: {reaction_time:.3f} 秒")

btn.config(command=lambda: start_game() if btn['text']=="开始" else click_btn())

root.mainloop()
