# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from lirc import init, nextcode
# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


# definição de funções
def validar_apartamento(num):
    busca = {"apartamento":num}
    resultado = colecao.find_one(busca)
    if resultado == None:
        return False
    return True
    
def retornar_nome_do_morador(num, senha):
    busca = {"apartamento":num,"senha":senha}
    resultado = colecao.find_one(busca)
    if resultado == None:
        return None
    return resultado["nome"]

def coletar_digitos(mensagem):
    lcd.clear()
    lcd.message(mensagem +"\n")
    senha = ""
    while True:
        codigo = nextcode()
        if codigo != []:
            if codigo[0] == "KEY_OK":
                return senha
            else:
                senha += codigo[0][-1]
                lcd.message("*")
    
# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# loop infinito
init("aula", blocking=False)
#print(coletar_digitos("Digite senha:"))
while True:
    apt = coletar_digitos("Digite apto")
    #print("inicio")
    verifica = validar_apartamento(apt)
    if verifica == True:
        senha = coletar_digitos("Digite senha:")
        morador = retornar_nome_do_morador(apt,senha)
        if morador != None:
            lcd.clear()
            lcd.message("Bem vindo\n" + morador)
            
        else:
            lcd.clear()
            lcd.message("Acesso\n1negado")
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido")
    sleep(1.5)