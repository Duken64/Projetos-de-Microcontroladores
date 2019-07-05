# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
#from py.irsend.irsend import *
from lirc import init, nextcode

# definição de funções
def AcendeTudo():
    for elem in leds:
        elem.on()
def ApagaTudo():
    for elem in leds:
        elem.off()
def Seleciona(num):
    lcd.clear()
    lcd.message("Tecla " + str(num) + "\npressionada")
def Toggle_LED():
    if led_atual == -1:
        return
    leds[led_atual].toggle()

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)
b1 = Button(11)
b1.when_pressed = AcendeTudo
b2 = Button(12)
b2.when_pressed = ApagaTudo
receptor = init("aula", blocking = False)
led_atual = -1
# loop infinito
while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
        codigo = lista_com_codigo[0]
        if codigo == "KEY_1" :
            Seleciona(1)
            led_atual = 0
        elif codigo == "KEY_2" :
            Seleciona(2)
            led_atual = 1
        elif codigo == "KEY_3" :
            Seleciona(3)
            led_atual = 2
        elif codigo == "KEY_4" :
            Seleciona(4)
            led_atual = 3
        elif codigo == "KEY_5" :
            Seleciona(5)
            led_atual = 4
        elif codigo == "KEY_OK" :
            Toggle_LED()
        elif codigo == "KEY_UP" :
            if led_atual > 0 and led_atual < 5:
                led_atual-= 1
                Seleciona(led_atual+1)
        elif codigo == "KEY_DOWN" :
            if led_atual >= 0 and led_atual < 4:
                led_atual+= 1
                Seleciona(led_atual+1)
        
    sleep(0.2)