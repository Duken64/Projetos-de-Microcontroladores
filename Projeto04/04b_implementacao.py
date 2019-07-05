# importação de bibliotecas
from os import system
from gpiozero import Button, LED, Buzzer
from time import sleep
from requests import get, post


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")


# parâmetros iniciais do Telegram
chave = "805503665:AAFhhkcb5PuDuwyY_sWd8TFQJ5c0p2q_ncw"
id_da_conversa = "175473424"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
def buttonPressed():
    #ligar campainha
    buz.on()
    
    
def buttonReleased():
    #desligar campainha
    buz.off()
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": "Alguem esta na porta"}
    resp = post(endereco, json=dados)
    
    system("fswebcam --resolution 640x480 --skip 10 foto.jpeg")
    endereco = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    file = {"photo": open("foto.jpeg", "rb")}
    resp = post(endereco, data=dados, files=file)
    
def openDoor():
    led1.on()
    
def closeDoor():
    led1.off()
    
def alarm():
    buz.beep(n=5, on_time=0.5, off_time=0.5)
    
def getMessage():
    global lastUpdate
    data = {"offset": lastUpdate}
    resp = get(endereco_base + "/getUpdates", json=data)
    dict = resp.json()
    text = ""
    for result in dict["result"]:
        msgDict = result["message"]
        if "text" in msgDict:
            text = msgDict["text"]
            if text == "Abrir":
                openDoor()
            elif text == "Alarme":
                alarm()
        lastUpdate = result["update_id"] + 1
    return

# criação de componentes
but1 = Button(11)
but2 = Button(12)
led1 = LED(21)
buz = Buzzer(16)

but1.when_released = buttonReleased
but1.when_pressed = buttonPressed
but2.when_pressed = closeDoor

lastUpdate = 0

# loop infinito
while True:
    getMessage()
    sleep(1)