# importação de bibliotecas
from gpiozero import LED, Button, LightSensor
from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from requests import post
from threading import Timer

# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/led/<int:led>/<string:state>")
def change_led_to_state(led, state):
    if(state == "on"):
        leds[led].on()
    else:
        leds[led].off()
    return "LED " + str(led) + ": " + str(state)

@app.route("/lastchange")
def find_last_change():
    ordenacao = [ [ "data", DESCENDING] ]
    resultado = colecao.find_one({}, sort=ordenacao)
    retorno = "<ul>"
    print(resultado)
    for i in range(5):
        if resultado["estado_dos_leds"][i] == True:
            estado = "acesa"
        else:
            estado = "apagada"
        
        retorno += "<li>Luz "+str(i+1) + ": " + estado + "</li>"
    retorno += "</ul>"
    return retorno

def SaveLedState():
    dados = {"data": datetime.now(), "estado_dos_leds": [led.is_lit for led in leds]}
    colecao.insert(dados)
    
def Button1():
    leds[0].toggle()
    SaveLedState()
def Button2():
    leds[1].toggle()
    SaveLedState()
def Button3():
    leds[2].toggle()
    SaveLedState()
def Button4():
    leds[3].toggle()
    SaveLedState()
    
def secondsAfterDate(led, date):
    busca = {
        "data":{"$gt":date}
        }
    ordenacao = [ [ "data", DESCENDING] ]
    resultado = list(colecao.find(busca, sort=ordenacao))
    totaltime = 0
    lasttime = datetime.now()
    for item in resultado:
        if item["estado_dos_leds"][led]:
            totaltime += (lasttime - item["data"]).seconds
        lasttime = item["data"]
    busca = {
        "data":{"$lt":date}
        }
    resultado = colecao.find_one(busca, sort=ordenacao)
    if resultado["estado_dos_leds"][led]:
        totaltime += (lasttime - date).seconds
    return totaltime
    
def getLedsTimes():
    now = datetime.now()
    time = now - timedelta(minutes=1)
    times = []
    dados = ""
    for i in range(5):
        times.append(secondsAfterDate(i, time))
        
    dados += str(times[0])+ "|||"
    dados += str(times[1])+ "|||"
    dados += str(times[2])+ "|||"
    dados += str(times[3])+ "|||"
    dados += str(times[4])
    
    chave = "bFkpPSRk6m_HENoq8Yoh9p"
    evento = "write_to_sheet3"
    endereco = "https://maker.ifttt.com/trigger/"+ evento +"/with/key/" + chave
    jason = {"value1": now.strftime("%m %d, %y at %H:%M")+"|||"+dados}
    resultado = post(endereco, json=jason)
    print(resultado.text)

def timerFunction():
    print("Acabou!\n")
    getLedsTimes()
    global timer
    timer = Timer(60, timerFunction)
    timer.start()
    
def isDark():
    leds[4].on()
    SaveLedState()

def isLight():
    leds[4].off()
    SaveLedState()

# criação dos componentes
cliente = MongoClient("localhost", 27017)
banco = cliente["lab5"]
colecao = banco["leds"]

leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed = Button1
botoes[1].when_pressed = Button2
botoes[2].when_pressed = Button3
botoes[3].when_pressed = Button4

lightSensor = LightSensor(8)
lightSensor.when_dark = isDark
lightSensor.when_light = isLight

timer = Timer(60, timerFunction)
timer.start()
# rode o servidor
app.run(port=5000, debug=False)

