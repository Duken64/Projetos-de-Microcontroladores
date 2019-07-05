# importação de bibliotecas
from os import system
from mplayer import Player
from gpiozero import LED
from gpiozero import Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")


# definição de funções
def Renomeia():
    lcd.clear()
    lcd.message(player.metadata["Title"])

def Play():
    player.pause()
    if player.paused:
        led1.blink()
    else:
        led1.on()

def Avança():
    player.pt_step(1)
    Renomeia()

def Recua():
    if player.time_pos>2:
        player.time_pos=0
    else:
        player.pt_step(-1)
        Renomeia()


# criação de componentes
player = Player()
player.loadlist("playlist.txt")

b1 = Button(11)
b1.when_pressed = Recua
b2 = Button(12)
b2.when_pressed = Play
b3 = Button(13)
b3.when_pressed = Avança
led1 = LED(21)
led3 = LED(23)
led3.off()
led1.on()
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# loop infinito
while True:
    metadados = player.metadata
    if metadados !=None:
        lcd.clear()
        lcd.message(metadados["Title"])
    sleep(0.2)
