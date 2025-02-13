from turtle import *


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
    
    
# Bandeira 1
desenha_retangulo(0,    0, 33.3, 60, 'blue')
desenha_retangulo(33.3, 0, 33.3, 60, 'white')
desenha_retangulo(66.6, 0, 33.3, 60, 'red')


# Bandeira 2
desenha_retangulo(0, 130, 100, 20, 'orange')
desenha_retangulo(0, 110, 100, 20, 'white')
desenha_retangulo(0, 90,  100, 20, 'green')

desenha_circulo(50, 100, 10, 'orange')

# Bandeira 3
desenha_retangulo(0, 260, 100, 60, 'green')
desenha_poligono([{'x':50, 'y':255}, {'x':5, 'y':230}, {'x':50, 'y':205}, {'x':95, 'y':230}], 'yellow')
desenha_circulo(50, 230, 13, 'blue')