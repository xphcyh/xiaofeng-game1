import pgzrun

def draw():
    screen.clear()
    screen.draw.text("正在播放bgm1.mp3...", center=(400, 300), fontsize=40, color="white", fontname="simhei.ttf")


def on_key_down():
    music.play("bgm1.mp3")

pgzrun.go()
