#include <meArm.h>
#include <GFButton.h>

int base = 12, ombro = 11, cotovelo = 10, garra = 9;

meArm braco(
180, 0, -pi/2, pi/2, // ângulos da base
135, 45, pi/4, 3*pi/4, // ângulos do ombro
180, 90, 0, -pi/2, // ângulos do cotovelo
30, 0, pi/2, 0 // ângulos da garra
);

int valorLido,valorFinal;
GFButton botaoA(2);
GFButton botaoB(3);
int Xglobal = 0;
int Yglobal = 150;
int xFinal,yFinal;
int x,y;
int eixoX = A0;
int eixoY = A1;
int potenciometro = A5;
boolean modo = false;


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

}

void loop() {
  botaoA.process();
  botaoB.process();
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
}

void fechaGarra(){
  braco.closeGripper();
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
