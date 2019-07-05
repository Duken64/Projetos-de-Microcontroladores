# importação de bibliotecas
from gpiozero import Button, Buzzer, DistanceSensor
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from lirc import init, nextcode
from datetime import datetime

# a linha abaixo apaga todo o banco e reinsere os moradores
#redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
colecao2 = banco["tentativas"]
colecao3 = banco["contadores"]

# definição de funções
def validar_apartamento(num):
    busca = {"apartamento":num}
    resultado = colecao.find_one(busca)
    tentativas = colecao3.find_one({"apartamento":num}, sort = [ ["data", ASCENDING] ])
    
    if resultado == None:
        return False
    return True
    
def retornar_nome_do_morador(num, senha):
    busca = {"apartamento":num,"senha":senha}
    resultado = colecao.find_one(busca)
    if resultado == None:
        tentativas = colecao3.find_one({"apartamento":apt})
        if tentativas["tentativas incorretas"] == []: 
            colecao3.insert({"apartamento"apt, "data": datetime.now(), "tentativas incorretas": 0})
        else:
            colecao3.insert({"apartamento"apt, "data": datetime.now(), "tentativas incorretas": tentativas["tentativas incorretas"]+1})
        return None
    colecao3.insert({"apartamento"apt, "data": datetime.now(), "tentativas incorretas": 0})
    return resultado["nome"]

def coletar_digitos(mensagem):
    lcd.clear()
    lcd.message(mensagem +"\n")
    digitos = ""
    while True:
        codigo = nextcode()
        if codigo != []:
            if codigo[0] == "KEY_OK":
                return digitos
            else:
                digitos += codigo[0][-1]
                lcd.message("*")
                buzzer.beep(n=1, on_time=0.25)
                
def administrador():
    apto = coletar_digitos("Adm: Digite apto")
    busca = {"apartamento":apto}
    ordenacao = [ ["data/hora", DESCENDING] ]
    resultados = list(colecao2.find(busca, sort=ordenacao))
    for resultado in resultados:
        if "morador" in resultado:
            print(resultado["data/hora"].strftime("%d/%m (%H:%M): ") + resultado["morador"])
        else:
            print(resultado["data/hora"].strftime("%d/%m (%H:%M): SENHA INCORRETA"))

# criação de componentes

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
buzzer = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
botao = Button(11)

# loop infinito
init("aula", blocking=False)
botao.when_pressed = administrador

#print(coletar_digitos("Digite senha:"))
while True:
    if(sensor.distance <= 0.2):
        apt = coletar_digitos("Digite apto")
        #print("inicio")
        verifica = validar_apartamento(apt)
        if verifica == True:
            senha = coletar_digitos("Digite senha:")
            morador = retornar_nome_do_morador(apt,senha)
            if morador != None:
                lcd.clear()
                lcd.message("Bem vindo\n" + morador)
                colecao2.insert({"apartamento":apt, "data/hora": datetime.now(),"morador": morador})
            else:
                lcd.clear()
                lcd.message("Acesso\ninvalido")
                buzzer.beep(n=3, on_time=0.125, off_time=0.125)
                colecao2.insert({"apartamento":apt, "data/hora": datetime.now()})
        else:
            lcd.clear()
            lcd.message("Apartamento\ninvalido")
            buzzer.beep(n=2, on_time=0.25, off_time=0.25)
    sleep(1.5)

