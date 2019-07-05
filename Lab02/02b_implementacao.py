# importação de bibliotecas
from flask import Flask
from lirc import init, nextcode
from py_irsend.irsend import *
from threading import Timer
# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
def Temp():
    send_once("aquario",["KEY_POWER"])


@app.route("/home")
def funcao_da_pagina_home():
    return "Funcionou"
@app.route("/ligar")
def funcao_da_pagina_ligar():
    send_once("aquario",["KEY_POWER"])
    return "Ligou"
@app.route("/volumeup")
def funcao_da_pagina_volumeup():
    send_once("aquario",["KEY_VOLUMEUP"])
    send_once("aquario",["KEY_VOLUMEUP"])
    return "Aumentou o volume"
@app.route("/volumedown")
def funcao_da_pagina_volumedown():
    send_once("aquario",["KEY_VOLUMEDOWN"])
    send_once("aquario",["KEY_VOLUMEDOWN"])
    return "Diminuiu o volume"
@app.route("/mudo")
def funcao_da_pagina_mudo():
    send_once("aquario",["KEY_MUTE"])
    return "Mute"
@app.route("/mudacanal/<string:numeros>")
def funcao_da_pagina_mudacanal(numeros):
    for i in range(0,4):
        send_once("aquario",["KEY_"+numeros[i]])
    return "Mudou"
@app.route("/timer/<int:tempo>")
def funcao_da_pagina_timer(tempo):
    t = Timer(tempo, Temp)
    t.start() 
    return "Temporizador ligado"
# rode o servidor
app.run(port=5000)