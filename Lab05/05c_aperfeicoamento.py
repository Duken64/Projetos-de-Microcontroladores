# importação de bibliotecas
from gpiozero import LED, Button, LightSensor
from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta

# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/led/<int:led>/<string:state>")
def change_led_to_state(led, state):
    if(state == "on"):
        leds[led].on()
    else:
        leds[led].off()
    SaveLedState()
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
lightSensor.when_dark = leds[4].on
lightSensor.when_light = leds[4].off

# rode o servidor
app.run(port=5000, debug=True)
