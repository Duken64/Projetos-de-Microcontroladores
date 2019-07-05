# importação de bibliotecas
from gpiozero import LED, Button, Buzzer, DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from pymongo import MongoClient
from datetime import datetime

# definição de funções
def toca():
    buzzer.beep(on_time=0.5, n=1)
    
def pisca():
    led.blink(n=2, on_time=0.5, off_time=0.5)
    
def mede():
    lcd.clear()
    distancia = sensor.distance*100
    lcd.message("Distancia:"+"\n"+"%.1f" % (distancia) + "cm")
    dados = {"data/horario": datetime.now(), "distancia": distancia}
    colecao.insert(dados)
    

# criação de componentes
sensor = DistanceSensor(trigger=17, echo=18)
led = LED(21)
buzzer = Buzzer(16)
botao = Button(11)
botao2 = Button(12)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
cliente = MongoClient("localhost", 27017)
banco = cliente["teste_iniciais"]
colecao = banco["teste_inicial"]

sensor.max_distance = 1
sensor.threshold_distance = 0.1

botao.when_pressed = toca
botao2.when_pressed = mede

sensor.when_in_range = pisca
sensor.when_out_of_range = pisca

while True:
    sleep(0.5)