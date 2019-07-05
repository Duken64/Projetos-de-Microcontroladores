# importação de bibliotecas
from Adafruit_CharLCD import Adafruit_CharLCD
from os import system
from gpiozero import Button,LED
from time import sleep
from requests import get,post
# parâmetros iniciais do Telegram
chave = "805503665:AAFhhkcb5PuDuwyY_sWd8TFQJ5c0p2q_ncw"
id_da_conversa = "175473424"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
def Envio():
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": "Oi!"}
    resposta = post(endereco, json=dados)

def TiraFoto():
    for i in range(0,5):
        system("fswebcam --resolution 640x480 foto" + str(i+1)+ ".jpeg")
        led1.blink(n=1)
        sleep(2)
        
def Gravacao():
    lcd.clear()
    lcd.message("Gravando ...")
    system("arecord --duration 5 --format cd teste.wav")
    lcd.clear()
# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
botao1.when_pressed = Gravacao
botao2.when_pressed = TiraFoto
botao3.when_pressed = Envio
while True:
    sleep(0.5)
