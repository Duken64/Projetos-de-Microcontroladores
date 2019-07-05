# importação de bibliotecas
from flask import Flask, render_template, redirect
from lirc import init, nextcode
from py_irsend.irsend import *
from threading import Timer
import json
# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
with open('templates/canais.json') as F:
          json_data = json.loads(F.read())

def Temp():
    send_once("aquario",["KEY_POWER"])
print(json_data[0]['nome'])
@app.route("/")
def funcao_da_pagina_home():
    return render_template("pagina2.html",data = json_data)

@app.route("/ligar")
def funcao_da_pagina_ligar():
    send_once("aquario",["KEY_POWER"])
    return redirect("/")

@app.route("/volumeup")
def funcao_da_pagina_volumeup():
    send_once("aquario",["KEY_VOLUMEUP"])
    send_once("aquario",["KEY_VOLUMEUP"])
    return redirect("/")

@app.route("/volumedown")
def funcao_da_pagina_volumedown():
    send_once("aquario",["KEY_VOLUMEDOWN"])
    send_once("aquario",["KEY_VOLUMEDOWN"])
    return redirect("/")

@app.route("/mudo")
def funcao_da_pagina_mudo():
    send_once("aquario",["KEY_MUTE"])
    return redirect("/")

@app.route("/mudacanal/<string:numeros>")
def funcao_da_pagina_mudacanal(numeros):
    for i in range(0,4):
        send_once("aquario",["KEY_"+numeros[i]])
    return redirect("/")

@app.route("/timer/<int:tempo>")
def funcao_da_pagina_timer(tempo):
    t = Timer(tempo, Temp)
    t.start() 
    return redirect("/")

# rode o servidor
app.run(port=5000)

