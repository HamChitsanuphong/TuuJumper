import pgzrun
import random

''' LEVEL                             แก้ภาพเลื่อน กูเปลี่ยนจาก Meter เป็น ระยะทางแทน เปลี่ยนตัวแปลด้วยก็ได้จะได้ไม่งง จาก Meter เป็น meter

    Easy : อนุสวรี อย่างเดียว
    Medium : เครื่องบินเข้ามา
    Hard : ผู้คนเข้ามา ขยับ ขึ้นมาเหยียบบนหญ้าดา

'''

def draw():
    global status_game, Object, Meter, Max_Meter, health, blood, text_space
    screen.clear()
    if status_game == "menu":
        img_home.draw()
        text_space.draw()
        head_tuu.draw()
        tank_home.draw()
    elif status_game == "start" or status_game == "boom":
        for i in bg:
            i.draw()
        screen.draw.text(f"{Meter}  M", (50,40), fontsize=30, color=(0,104,10))
        if Max_Meter > 0:
            if len(str(Max_Meter)) > 2 :
                screen.draw.text(f"MAX : {Max_Meter} M", (WIDTH/2-70,20), fontsize=20, color=(0,42,104))
            else :
                screen.draw.text(f"MAX : {Max_Meter} M", (WIDTH/2-66,20), fontsize=20, color=(0,42,104))
        if health[1] > 0:
            for head in range(health[1]):
                blood[head].draw()
        player.draw()
        for item in Object:
            item.draw()
    elif status_game == "over":
        img_over.draw()
        text_space.draw()
        if (len(str(Max_Meter)) == 3) :
            screen.draw.text(str(Max_Meter), (646,260), fontsize=60)
            if (len(str(Meter)) == 3) :
                screen.draw.text(str(Meter), (80,260), fontsize=60)
            else :
                screen.draw.text(str(Meter), (98,260), fontsize=60)
        elif (len(str(Max_Meter)) > 3) :
            screen.draw.text(str(Max_Meter), (620,260), fontsize=60)
            if (len(str(Meter)) > 3) :
                screen.draw.text(str(Meter), (70,260), fontsize=60)
            else :
                screen.draw.text(str(Meter), (88,260), fontsize=60)
        else :
            screen.draw.text(str(Max_Meter), (648,260), fontsize=60)
            screen.draw.text(str(Meter), (98,260), fontsize=60)

def update():
    global Object, status_game, jump, speed, player, bg, home, health, Max_Meter, Meter, jump_down

    # HOME
    if status_game == "menu":
        head_tuu.x -= 2
        if head_tuu.x <= 700 :
            head_tuu.x = 700
            head_tuu.angle += 2
        tank_home.x += 2
        if tank_home.x > WIDTH+60 :
            tank_home.x = -60
        if tank_home.x > 200 and tank_home.x < 600 and home[0] == "not":
            home[0] = "jump"
            tank_home.image = "tank_up_0"


        if home[0] == "jump":
            tank_home.y -= 4
            if tank_home.y <= 200:
                home[0] = "down"
        if home[0] == "down":
            tank_home.y += 4
            tank_home.image = "tank_down_0"
            if tank_home.y > 400:
                tank_home.image = "tank_stay_0"
                home[0] = "not"
                tank_home.y = 400

    elif status_game == "start":
        max_speed = 20
        Sum = 0
        for i in bg:
            if Meter >= 1000:
                i.x -= 12
            else:
                i.x -= 8
            if i.x <= -600:
                if Meter >= 1000:
                    i.x = WIDTH*2+170
                else:
                    i.x = WIDTH*2+190
        if jump[0] == True:
            if jump[1] == "UP":
                speed += 1
                player.y -= speed
                if speed >= max_speed:
                    jump[1] = "Floating"
            elif jump[1] == "Floating":
                speed -= 1
                player.y -= speed
                if speed <= 0:
                    jump[1] = "Down"
                    jump[0] = False
        else:
            if jump[1] == "Down":
                speed += 1
                player.y += speed
                if speed >= max_speed+8:
                    speed = 0
                    jump[1] = "Not"
            if player.y > 500:
                player.y = 500

        # Object
        for item in Object:

            # Move
            if Meter >= 1000:
                item.x -= 12
            else:
                item.x -= 8

            if health[0]:
                if player.colliderect(item):
                    if health[1] > 1:
                        health[1] -= 1
                        health[0] = False
                        clock.schedule(cooldown, 2)
                    else:
                        health[1] -= 1
                        music.stop()
                        if Meter > Max_Meter:
                            Max_Meter = Meter
                        sounds.boom.play()
                        status_game = "boom"
                        clock.unschedule(Meter_check)
                        clock.unschedule(animation)
                        clock.schedule_interval(boom, 0.150)

def on_key_down(key, mod, unicode):
    global status_game, jump, speed, Meter, Max_Meter
    if status_game == "menu":
        if key == keys.SPACE:
            status_game = "start"
            music.stop()
            music.play("main")
    elif status_game == "start":
        if key == keys.SPACE or key == keys.W or key == keys.UP:
            if jump[0] == False and jump[1] == "Not":
                jump[0] = True
                sounds.jump.play()
                jump[1] = "UP"
    elif status_game == "over":
        if key == keys.SPACE:
            status_game = "start"
            restart()

def restart():
    global Object, speed, health, Index, Meter, jump, Object, player, bg
    Object = []
    speed = 0
    health = [True, 3]
    Index = [0,0,0]
    Meter = 0
    bg[0].pos = (WIDTH/2,HEIGHT/2)
    bg[1].pos = (WIDTH*2,HEIGHT/2)
    jump = [False, "Not"]
    Object = []
    clock.schedule_interval(Meter_check, 0.1)
    clock.schedule_interval(animation, 0.250)
    player.image = "tank_stay_0"
    player.pos = (150, 500)
    sounds.oh.stop()
    music.play("main")

def Meter_check():
    global Meter, status_game
    if status_game == 'start':
        Meter += 1

def spawn():
    global Object, block, Meter
    if Meter > 1000:
        item = random.randrange(2)
        if item == 1:
            Object.append(Actor(block[item], (WIDTH+100, 200)))
        else:
            Object.append(Actor(block[item], (WIDTH+100, 530)))
    else:
        Object.append(Actor(block[0], (WIDTH+100, 530)))

def boom():
    global Index, status_game, animation_boom, player
    Index[1] += 1
    if Index[1] > 2:
        clock.unschedule(boom)
        sounds.oh.play()
        status_game = "over"
        Index[1] = 0
    player.image = animation_boom[Index[1]]
        

def animation():
    global Index, jump, speed, player, idel, jump_up, jump_down, health, Immortal, Immortal_jump

    Index[0] += 1
    if Index[0] > 2:
        Index[0] = 0

    if jump[0] == True and jump[1] == "UP" or jump[1] == "Floating":
        if health[0]:
            player.image = jump_up[Index[0]]
        else:
            player.image = Immortal_jump[Index[0]]
    else:
        if health[0]:
            player.image = idle[Index[0]]
        else:
            player.image = Immortal[Index[0]]

def cooldown():
    global health
    health[0] = True

def animation_text():
    global Index, text_space, animation_text_play, status_game
    Index[2] += 1
    if Index[2] > 7:
        Index[2] = 0
    if status_game == "menu":
        text_space.image = animation_text_play[Index[2]]
    else:
        text_space.image = animation_text_again[Index[2]]


# Main program
WIDTH = 800
HEIGHT = 600
TITLE = "TUU Jumper"

health = [True, 3]
Index = [0,0,0]
Meter = 0
Max_Meter = 0
status_game = "menu"
jump = [False, "Not"]
Object = []

# HOME & OVER
home = ["not", False]
text_space = Actor('text_play/play_0')
animation_text_play = ["text_play/play_0","text_play/play_1","text_play/play_2","text_play/play_3","text_play/play_4","text_play/play_5","text_play/play_6","text_play/play_7"]
img_home = Actor("home", (WIDTH/2,HEIGHT/2))
head_tuu = Actor("head_tuu_home", (WIDTH+10,110))
tank_home = Actor("tank_stay_0", (-60, HEIGHT/1.5))
img_over = Actor("bg_game_over", (WIDTH/2, HEIGHT/2))

# IN GAME
bg = [Actor("background", (WIDTH/2,HEIGHT/2)),Actor("background", (WIDTH*2,HEIGHT/2))]
idle = ["tank_stay_0","tank_stay_1","tank_stay_2"]
Immortal = ["immortal/tank_stay_0","immortal/tank_stay_1","immortal/tank_stay_2"]
Immortal_jump = ["immortal/tank_jump_0","immortal/tank_jump_1","immortal/tank_jump_2"]
jump_up = ["tank_jump_0","tank_jump_1","tank_jump_2"]
# jump_down = ["tank_stay_0","tank_stay_1","tank_stay_2"] # ------------------ แก้ ไม่เอาลงแล้ว เอาแต่ up ถ้าแก้ตรงหน้า HOME ได้ก็ดีเหมือนกัน กระโดดแล้วเปลี่ยนภาพหนะ
block = ["block_1", "block_2"] # -------------------------------- แก้หน่อย เอาออก เหลือ 2 อัน
player = Actor("tank_stay_0", (150,500))
blood = [Actor("blood", (600, 40)),Actor("blood", (650, 40)),Actor("blood", (700, 40))]
animation_boom = ["boom/boom_0","boom/boom_1","boom/boom_2"]
speed = 0

# Over
animation_text_again = ["text_again/again_0","text_again/again_1","text_again/again_2","text_again/again_3","text_again/again_4","text_again/again_5","text_again/again_6","text_again/again_7"]

clock.schedule_interval(Meter_check, 0.030)  # ถ้าฉากเร็วขึ้น ให้ลดลงมาตามฉาก เช่น 0.025 มี 5 step ฉากอะ ก็ลดไปเรื่อยๆ 0.020, 0.015, 0.010 นับเมตรไง
clock.schedule_interval(animation, 0.150)
clock.schedule_interval(spawn, 1.5)
clock.schedule_interval(animation_text, 0.070)

music.play("menu")

pgzrun.go()
