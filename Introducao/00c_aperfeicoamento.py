from json import load
from turtle import *

# Copie as funções da Implementação aqui


def Inicia(x,y,cor):
    fillcolor(cor)
    penup()
    goto(x,y)
    pendown()
    begin_fill()
    return

def desenha_retangulo(x, y, comprimento, altura, cor):
    Inicia(x,y,cor)
    setheading(0)
    forward(comprimento)
    setheading(-90)
    forward(altura)
    setheading(-180)
    forward(comprimento)
    setheading(90)
    forward(altura)
    end_fill()
    return
    
    
def desenha_circulo(x, y, raio, cor):
    Inicia(x,y+raio,cor)
    setheading(-180)
    circle(raio)
    end_fill()
    return
    
    
def desenha_poligono(lista_pontos, cor):
    Inicia(lista_pontos[0]["x"],lista_pontos[0]["y"],cor)
    for i in range(len(lista_pontos)):
        goto(lista_pontos[i]["x"],lista_pontos[i]["y"])
    goto(lista_pontos[0]["x"],lista_pontos[0]["y"])
    end_fill()
    return
    
    



    

# Implemente a função abaixo
def desenha_bandeira(dicionario_do_pais):
    #nome = textinput("Pais","Digite o nome do pais:")
    lista = dicionario_do_pais["elementos"]
    for i in range(len(lista)):
         if lista[i]["tipo"] == "retângulo":
           desenha_retangulo(lista[i]["x"],lista[i]["y"],lista[i]["comprimento"],lista[i]["altura"],lista[i]["cor"])
         elif lista[i]["tipo"] == "polígono":
             desenha_poligono(lista[i]["pontos"],lista[i]["cor"])
         elif lista[i]["tipo"] == "círculo":
            desenha_circulo(lista[i]["x"],lista[i]["y"],lista[i]["raio"],lista[i]["cor"])
         else:
            print("Tipo nao encontrado")
    return

dicionarios_de_paises = load(open('paises.json', encoding="UTF-8"))
#desenha_bandeira(dicionarios_de_paises[0])


# Ao clicar na tela, solicitar o nome de um país, busque-o na lista de dicionários de países e desenhe-o.
def test(x,y):
    nome = textinput("Pais","Digite o nome do pais:")
    for elem in dicionarios_de_paises:
        if nome == elem["nome"]:
            desenha_bandeira(elem)
    return
onscreenclick(test)
# Por fim, adicione uma nova bandeira no arquivo JSON e teste seu desenho.