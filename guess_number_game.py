import ttkbootstrap as ttb
import random

# ...其余代码不变...

def restart():
    global player_hand, dealer_hand
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    result.set("")
    hit_btn['state'] = 'normal'
    stand_btn['state'] = 'normal'
    update()

root = ttb.Window()
root.title("21点纸牌游戏")

player_hand = []
dealer_hand = []

player_label = ttb.Label(root, font=("Arial", 14))
dealer_label = ttb.Label(root, font=("Arial", 14))
player_label.pack(pady=5)
dealer_label.pack(pady=5)

result = ttb.StringVar()
ttb.Label(root, textvariable=result, font=("Arial", 16), foreground='red').pack(pady=5)

hit_btn = ttb.Button(root, text="要牌", command=hit)
hit_btn.pack(side='left', padx=20)
stand_btn = ttb.Button(root, text="停牌", command=stand)
stand_btn.pack(side='left', padx=20)
ttb.Button(root, text="重新开始", command=restart).pack(side='left', padx=20)

restart()
root.mainloop() 
import random

def check_guess():
    guess = int(entry.get())
    if guess == number:
        result.set("恭喜你，猜对了！")
    elif guess < number:
        result.set("太小了，再试试！")
    else:
        result.set("太大了，再试试！")

def restart():
    global number
    number = random.randint(1, 100)
    result.set("请猜一个1~100的数字")

number = random.randint(1, 100)

root = tk.Tk()
root.title("猜数字游戏")

result = tk.StringVar()
result.set("请猜一个1~100的数字")

tk.Label(root, textvariable=result, font=("Arial", 16)).pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)
tk.Button(root, text="猜一猜", command=check_guess).pack(pady=5)
tk.Button(root, text="重新开始", command=restart).pack(pady=5)

root.mainloop()
