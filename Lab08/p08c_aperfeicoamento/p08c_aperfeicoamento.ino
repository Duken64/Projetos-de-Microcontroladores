#include <meArm.h>
#include <GFButton.h>
#include <EEPROM.h>

int base = 12, ombro = 11, cotovelo = 10, garra = 9;
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
int Xglobal = 0;
int Yglobal = 150;
int xFinal,yFinal;
int x,y;
int eixoX = A0;
int eixoY = A1;
int potenciometro = A5;
int estadoGarra = 0;
boolean modo = false;
int endereco = 0;


void setup() {
    Serial.begin(9600);
    pinMode(potenciometro, INPUT);
    pinMode(eixoX, INPUT);
    pinMode(eixoY, INPUT);
    braco.begin(base, ombro, cotovelo, garra);
    braco.closeGripper();
    braco.gotoPoint(0, 150, 0);
    botaoA.setPressHandler(abreGarra);
    botaoA.setReleaseHandler(fechaGarra);
    botaoB.setPressHandler(AlteraModo);
    botaoC.setPressHandler(salvaPosicao);
    botaoD.setPressHandler(vaiLaXerifao);
    EEPROM.get(endereco, pontosSalvos);
}

void loop() {
  botaoA.process();
  botaoB.process();
  botaoC.process();
  botaoD.process();
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
  estadoGarra = 1;
}

void fechaGarra(){
  braco.closeGripper();
  estadoGarra = 0;
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
  if(i<4){
  pontosSalvos[i][0] = braco.getX();
  pontosSalvos[i][1] = braco.getY();
  pontosSalvos[i][2] = braco.getZ();
  pontosSalvos[i][3] = estadoGarra;
  EEPROM.put(endereco + 16*i, pontosSalvos[i]);
  Serial.println(pontosSalvos[i][3]);
  i++;
  }
}

void vaiLaXerifao(){
  for(int j=0; j<4; j++){
    braco.gotoPoint(pontosSalvos[j][0], pontosSalvos[j][1], pontosSalvos[j][2]);
    if(pontosSalvos[j][3] == 1){
      braco.openGripper();
    }
    else if(pontosSalvos[j][3] == 0){
      braco.closeGripper();
    }
  }
  delay(50);
}
