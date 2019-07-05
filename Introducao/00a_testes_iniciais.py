from turtle import *

def imprime_coordenadas(x, y):
    penup()
    goto(x,y)
    print("x = ", x)
    print("y = ", y)
    write("x = "+ str(x) + "," + "y = " + str(y))
    return

def Inicia(x,y):
    penup()
    goto(x,y)
    pendown()
    return

# Parte 1: desenhe o retângulo no topo

def desenha_retangulo(x, y, comprimento, altura):
    Inicia(x,y)
    setheading(0)
    forward(comprimento)
    setheading(90)
    forward(altura)
    setheading(180)
    forward(comprimento)
    setheading(270)
    forward(altura)
    return

#desenha_retangulo(-50,170,100,50)

# Parte 2: desenhe o triângulo equilátero à direita
def triangulo(x,y,lado):
    Inicia(x,y)
    setheading(60)
    forward(lado)
    setheading(-60)
    forward(lado)
    setheading(-180)
    forward(lado)
    return

#triangulo(100,0,70)

# Parte 3: desenhe o círculo na parte debaixo
def desenha_circulo(x, y, raio):
    Inicia(x,y)
    circle(raio)
    return
#desenha_circulo(0,-140,50)

# Parte 4: desenhe a espiral na esquerda
def espiral(x,y,raio):
    Inicia(x,y)
    i =raio
    while raio > 20 :
        circle(raio,70,10)
        raio = raio -1
    return
        

espiral(0,0,50)
# Parte 5: ao clicar em um ponto da tela, desenhe um texto com o valor das coordenadas x e y
onscreenclick(imprime_coordenadas)
