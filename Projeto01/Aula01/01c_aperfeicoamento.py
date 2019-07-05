# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from os import system
from mplayer import Player
from gpiozero import LED
from gpiozero import Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")


# definição de funções

def Play():
    player.pause()
    if player.paused:
        led1.blink()
    else:
        led1.on()

def Avança():
    player.speed=2

def Passa():
    if player.speed == 1:
         player.pt_step(1)
    else:
        player.speed = 1

def Recua():
    if player.time_pos>2:
        player.time_pos=0
    else:
        player.pt_step(-1)



# criação de componentes
player = Player()
player.loadlist("playlist.txt")

b1 = Button(11)
b1.when_pressed = Recua
b2 = Button(12)
b2.when_pressed = Play
b3 = Button(13)
b3.when_held = Avança
b3.when_released = Passa
led1 = LED(21)
led3 = LED(23)
led3.off()
led1.on()
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
pos = player.time_pos
n=0
# loop infinito
while True:
    pos = player.time_pos
    Mpos = pos/60
    Spos = pos%60
    t = player.length
    Mt = t/60
    St = t%60
    metadados = player.metadata
    if metadados !=None:
        lcd.clear()
        
        lcd.message(metadados["Title"][n:16+n] + "\n" + "%.2d" % Mpos + ":" + "%.2d" % Spos + " de %.2d" %Mt + ":%.2d" %St)
    if (len(metadados["Title"])-n)> 16:
        n += 1
    else:
        n=0
    sleep(0.2)

