
#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

// 16 notas
int indicesDeNotaDaMusica[] = {7, 2, 0, 11, 9, 7, 2, 0, 11, 9, 7, 2, 0, 11, 0, 9};
int oitavasDaMusica[] = {0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0};
unsigned long intervalosEntreNotas[] = {1000, 1000, 167, 167, 167, 1000, 500, 167, 167, 167, 1000, 500, 167, 167, 167, 1000};
int oitava = 0;
int tempoAtual = 0;
int indiceOitavo = 0;
// COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};

GFButton button1(A1);
GFButton button2(A2);
GFButton button3(A3);

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
RotaryEncoder encoder(20, 21);

int beep = 5, terra = A5, soundSensor = 19;
int notaAtual = 0;
int flag = 0;
boolean escuta = false;
unsigned long lastTime = 0, lastPos = 0;
unsigned long contador = 0;

unsigned long periodoEmMs = 0, instante1 = 0, instante2 = 0;
char mensagem[10];


void enconderTick() {
  encoder.tick();
}
void button3Pressed(GFButton& but){
  if(tempoAtual == 0)
  {
    sprintf(mensagem,"%s%d",nomeDasNotas[indicesDeNotaDaMusica[indiceOitavo]],oitavasDaMusica[indiceOitavo]);
    display.set(mensagem);
    Serial.println(nomeDasNotas[notaAtual]);
    display.update();
    tone(beep,frequencias[indicesDeNotaDaMusica[0]]*pow(2,oitavasDaMusica[0]),intervalosEntreNotas[0]);
    tempoAtual = millis();
    Serial.println(tempoAtual);
  }
}


void button1Pressed(GFButton& but) {
  periodoEmMs = 0;
  sprintf(mensagem,"%s%d",nomeDasNotas[notaAtual],oitava);
  display.set(mensagem);
  Serial.println(mensagem);
  display.update();
  int nota  = frequencias[notaAtual]*pow(2,oitava);
  tone(beep, nota);
  Serial.println("button pressed");
}

void button2Pressed(GFButton& but) {
  periodoEmMs = 0;
  if(escuta == false){
    escuta = true;
  }
}

void button1Released(GFButton& but) {
  noTone(beep);
  Serial.println("button released");
}

void TocaBeep(){
  tone(beep,frequencias[notaAtual],200);
}
void ParaBeep(){
  noTone(beep);
}

void soundDetected() {
  if(escuta == true)
  {
    unsigned long now = millis();
    if (now > lastTime + 10) {
      if(flag == 0){
        instante1 = now;
        flag = 1;
      }
      else {
        instante2 = now;
        contador = instante2;
        flag = 0;
        periodoEmMs = instante2 - instante1;
        int batidasPorMinuto = 60000 / periodoEmMs;
        display.set(batidasPorMinuto);
        display.update();
        escuta = false;
        
      }
      //Serial.println("som!");
      lastTime = now;
    }
  }
  
}

void rotaryChanged(int dir) {  
  if (dir>0 && notaAtual<11)
    notaAtual = notaAtual + 1;
  else if(dir>0 && notaAtual==11)
  {
    if(oitava<4){
      oitava++; 
      notaAtual = 0;
    }
  }

  else if(dir<0 && notaAtual==0)
  {
    if(oitava>0){
      oitava--;
      notaAtual = 11; 
    }
  }
  else if(dir<0 && notaAtual>0)
    notaAtual = notaAtual -1;
  tone(beep,frequencias[notaAtual]*pow(2,oitava),200);
  sprintf(mensagem,"%s%d",nomeDasNotas[notaAtual],oitava);
  display.set(mensagem);
  Serial.println(dir);
  display.update();  
}

void setup() {
  Serial.begin(9600);
  button1.setPressHandler(button1Pressed);
  button2.setPressHandler(button2Pressed);
  button3.setPressHandler(button3Pressed);
  button1.setReleaseHandler(button1Released);
  pinMode(beep, OUTPUT);
  pinMode(terra, OUTPUT);
  digitalWrite(terra, LOW);

  int origin = digitalPinToInterrupt(soundSensor);
  attachInterrupt(origin, soundDetected, RISING);
  
  int origin1 = digitalPinToInterrupt(20);
  attachInterrupt(origin1, enconderTick, CHANGE);
  int origin2 = digitalPinToInterrupt(21);
  attachInterrupt(origin2, enconderTick, CHANGE);
  sprintf(mensagem,"%s%d",nomeDasNotas[notaAtual],oitava);
  display.set(mensagem);
  Serial.println(nomeDasNotas[notaAtual]);
  display.update();
    
}

void loop() {
  if(periodoEmMs != 0)
  {
    if(millis() - contador > periodoEmMs){
       TocaBeep();
       contador = millis();
    } 
  }
 
  if((millis() - tempoAtual) > intervalosEntreNotas[indiceOitavo] && tempoAtual!=0)
  {
    if(indiceOitavo<15){
      indiceOitavo++;
      sprintf(mensagem,"%s%d",nomeDasNotas[indicesDeNotaDaMusica[indiceOitavo]],oitavasDaMusica[indiceOitavo]);
      display.set(mensagem);
      Serial.println(nomeDasNotas[notaAtual]);
      display.update();
      tone(beep,frequencias[indicesDeNotaDaMusica[indiceOitavo]]*pow(2,oitavasDaMusica[indiceOitavo]),intervalosEntreNotas[indiceOitavo]);
      //Serial.println(oitavasDaMusica[indiceOitavo]);
      tempoAtual = millis();
    }
    else {
      tempoAtual = 0;
      indiceOitavo = 0;
    }
  }


  
  button1.process();
  button2.process();
  button3.process();
  int pos = encoder.getPosition();
    if (pos != lastPos) {
     Serial.println("changed");
     rotaryChanged(pos-lastPos);
     lastPos = pos;
     
   }
   display.update(); 
    
}

// DEPOIS FAÇA OS NOVOS RECURSOS
