#include <meArm.h>
#include <GFButton.h>
#include <EEPROM.h>
#include <LinkedList.h>

struct Posicao {
float x;
float y;
float z;
bool garraAberta;
};

LinkedList<Posicao> listaDeEstruturas;

int base = 12, ombro = 11, cotovelo = 10, garra = 9;
Posicao novaPosicao;
float pontosSalvos[4][4];


meArm braco(
180, 0, -pi/2, pi/2, // ângulos da base
135, 45, pi/4, 3*pi/4, // ângulos do ombro
180, 90, 0, -pi/2, // ângulos do cotovelo
30, 0, pi/2, 0 // ângulos da garra
);

int i=0;
int valorLido,valorFinal;
GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);
GFButton botaoD(5);
GFButton botaoE(6);

int Xglobal = 0;
int Yglobal = 150;
int xFinal,yFinal;
int x,y;
int eixoX = A0;
int eixoY = A1;
int potenciometro = A5;
boolean estadoGarra = false; // false = garra fechada
boolean modo = false;
int endereco = 0;
int contador = 0;


void setup() {
    Serial.begin(9600);
    pinMode(potenciometro, INPUT);
    pinMode(eixoX, INPUT);
    pinMode(eixoY, INPUT);
    ler_eeprom();
    braco.begin(base, ombro, cotovelo, garra);
    braco.closeGripper();
    braco.gotoPoint(0, 150, 0);
    botaoA.setPressHandler(abreGarra);
    botaoA.setReleaseHandler(fechaGarra);
    botaoB.setPressHandler(AlteraModo);
    botaoC.setPressHandler(salvaPosicao);
    botaoD.setPressHandler(vaiLaXerifao);
    botaoE.setPressHandler(ZeraLista);

}

void loop() {
  botaoA.process();
  botaoB.process();
  botaoC.process();
  botaoD.process();
  botaoE.process();
  x = analogRead(eixoX);
  y = analogRead(eixoY);
  valorLido = analogRead(potenciometro);
  valorFinal = map(valorLido, 0, 1023, -30, 100);
  if(modo == false){
    Absoluto();
  }
  else{
    Relativo();
  }
}

void abreGarra(){
  braco.openGripper();
  estadoGarra = true;
}

void fechaGarra(){
  braco.closeGripper();
  estadoGarra = false;
}

void AlteraModo(){
  modo = !modo;
  Xglobal = braco.getX();
  Yglobal = braco.getY();
  Serial.println(modo);
}

void Absoluto(){
  int xMap = map(x, 0, 1023, -150, 150);
  int yMap = map(y, 0, 1023, 100, 200);
  xFinal = xMap;
  yFinal = yMap;
  braco.gotoPoint(xFinal, yFinal, valorFinal);
}

void Relativo(){
  int xMap = map(x, 0, 1023, -10, 10);
  int yMap = map(y, 0, 1023, -10, 10);
  Xglobal += xMap;
  Yglobal += yMap;
  if(Xglobal > 150){
    Xglobal = 150;
  }
  else if(Xglobal < -150){
    Xglobal = -150;
  }
  if(Yglobal > 200){
    Yglobal = 200;
  }
  else if(Yglobal < 100){
    Yglobal = 100;
  }
  xFinal = Xglobal;
  yFinal = Yglobal;
  braco.goDirectlyTo(xFinal, yFinal, valorFinal);
  delay(50);
}


void salvaPosicao(){
  Posicao novaPosicao;
  novaPosicao.x = braco.getX();
  novaPosicao.y = braco.getY();
  novaPosicao.z = braco.getZ();
  novaPosicao.garraAberta = estadoGarra;
  listaDeEstruturas.add(novaPosicao);
  int total = listaDeEstruturas.size();
  EEPROM.put(0, total);
  EEPROM.put(endereco + contador, novaPosicao);
  contador += sizeof(novaPosicao);
}


void vaiLaXerifao(){
  Posicao elemento;
  Serial.println(listaDeEstruturas.size());
  for(int j=0; j< listaDeEstruturas.size(); j++){
    Serial.println(j);
    elemento = listaDeEstruturas.get(j);
    braco.gotoPoint(elemento.x,elemento.y, elemento.z);
    if(elemento.garraAberta == true){
      braco.openGripper();
    }
    else if(elemento.garraAberta == false){
      braco.closeGripper();
    }
  }
  delay(50);
}

void ler_eeprom(){
  int total;
  Posicao elemento;
  EEPROM.get(endereco, total);
  endereco += 2;
  for(int i = 0; i < total; i++){
    EEPROM.get(endereco + contador, elemento);
    listaDeEstruturas.add(elemento);
    contador += sizeof(elemento);
  }
}

void ZeraLista(){
  listaDeEstruturas.clear();
  endereco = 0;
  contador = 0;
  int total = 0;
  EEPROM.put(0, total);
}
