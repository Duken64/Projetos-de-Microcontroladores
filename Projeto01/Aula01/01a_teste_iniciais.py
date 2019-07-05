# importação de bibliotecas
from gpiozero import LED
from gpiozero import Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD


# definição de funções
def Pisca2():
    global cont
    led2.blink(n=4)
    cont= cont + 1
    

# criação de componentes
cont  = 0
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

led1 = LED(21)
led2 = LED(22)
led3 = LED(23)
led3.blink(on_time=1,off_time=3)
led5 = LED(25)

b1 = Button(11)
b2 = Button(12)
b3 = Button(13)
b4 = Button(14)
b1.when_pressed = led1.toggle
b2.when_pressed = Pisca2
# loop infinito
while True:
    lcd.clear()
    lcd.message(str(cont))
    if b3.is_pressed and b4.is_pressed:
        led5.on()
    else:
        led5.off()
    sleep(0.2)
    
    