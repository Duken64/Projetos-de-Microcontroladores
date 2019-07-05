# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from os import system
from gpiozero import Button, LED, Buzzer, DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from requests import get, post
from subprocess import Popen
from mplayer import Player
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import unicodedata
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
    
def SendText(texto, custom):
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": texto}
    if custom:
        dados["reply_markup"] = {
            "keyboard": [["Abrir"],["Soar Alarme"],["Ignorar"]],
            "resize_keyboard": True,
            "one_time_keyboard": True}
    post(endereco, json=dados)
    
def buttonReleased():
    #desligar campainha
    buz.off()
    SendText("Alguem esta na porta", True)
    
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
    
def popMsg(text):
    lcd.message(text)
    buz.beep(n=1, on_time = 0.4)
    sleep(0.4)
    lcd.clear()

def displayText(text):
    lcd.clear()
    popMsg("Mensagem Recebida");
    sleep(0.5);
    popMsg("Mensagem Recebida");
    msg = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf8')
    for i in range(0,len(msg)-15):
        lcd.clear()
        lcd.message(msg[i:i+16])
        sleep(0.3)
        
def getVoice(id):
    endereco = endereco_base + "/getFile"
    dados = {"file_id": id}
    resposta = get(endereco, json=dados)
    dict = resposta.json()
    final_link = dict["result"]["file_path"]
    link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_link
    arquivo_de_destino = "voice.ogg"
    urlretrieve(link_do_arquivo, arquivo_de_destino)
    player.loadfile(arquivo_de_destino)

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
            elif text == "Soar Alarme":
                alarm()
            elif (text != "Ignorar"):
                displayText(text)
        elif "voice" in msgDict:
            voice = msgDict["voice"]
            id = voice["file_id"]
            getVoice(id)
        lastUpdate = result["update_id"] + 1
    return

def Gravacao():
    global aplicativo
    comando = ["arecord","--duration","30", "audio.wav"]
    aplicativo = Popen(comando)
    
def Envio_Audio(nome):
    endereco = endereco_base + "/sendVoice"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"voice": open(nome, "rb")}
    post(endereco, data=dados, files=arquivo)
    
def parar_gravacao():
    global aplicativo
    if aplicativo != None:
        print("parando gravacao")
        aplicativo.terminate()
        system("opusenc audio.wav audio.ogg")
        aplicativo = None
        Envio_Audio("audio.ogg")

def Entrou():
    global tempo
    tempo = datetime.now()
    
def Saiu():
    intervalo = datetime.now() - tempo
    if (intervalo.seconds >= 10):
        SendText("Pessoa saiu", False)
# criação de componentes
tempo = datetime.now()
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1
player = Player()
aplicativo = None
but1 = Button(11)
but2 = Button(12)
but3 = Button(13)
led1 = LED(21)
buz = Buzzer(16)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

but1.when_released = buttonReleased
but1.when_pressed = buttonPressed
but2.when_pressed = closeDoor
but3.when_pressed = Gravacao
but3.when_released = parar_gravacao
sensor.when_in_range = Entrou
sensor.when_out_of_range = Saiu
lastUpdate = 0

# loop infinito
while True:
    getMessage()
    sleep(1)
