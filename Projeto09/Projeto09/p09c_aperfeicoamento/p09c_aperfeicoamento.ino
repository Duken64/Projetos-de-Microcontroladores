//libs
#include <GFButton.h>
#include <ShiftDisplay.h>

//variables
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
String  comandos[4] = { "frente", "tras", "esquerda", "direita" };
int led1 = 10;
int led2 = 11;
ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int globalState = 0;
String modo = "manual";
unsigned long tempo = 0;

//functions

void sendCommand() {
  //Serial.println("teste");
  if (modo != "automatico") {
    Serial1.println(comandos[globalState]);
    //Serial.println(comandos[globalState]);
  }
}

void alteraModo() {
  if (modo == "manual") {
    modo = "automatico";
  }
  else {
    modo = "manual";
  }
  Serial1.println(modo);
  //Serial.println(modo);
}

void mandaParar() {
  if (modo != "automatico") {
    Serial1.println("parar");
    //Serial.println("parar");
  }
}


void switchState() {
  globalState = (globalState + 1) % 4 ;
  if (modo != "automatico") {
    display.set(comandos[globalState]);
    //Serial.println(comandos[globalState]);
  }
}

void checaTempo(){
  if (tempo  != 0) {
        if(millis() - tempo >= 1000){
          if(modo == "automatico"){
            modo = "manual"; 
            Serial1.println(modo);
          }
          tempo = 0;
        }
      }
  else {
     tempo = millis();
  }
}

//setup
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(115200);
  Serial1.setTimeout(10);
  botao1.setPressHandler(switchState);
  botao2.setPressHandler(sendCommand);
  botao2.setReleaseHandler(mandaParar);
  botao3.setPressHandler(alteraModo);
  display.set(comandos[globalState]);
  display.update();

}

void loop() {
  botao1.process();
  botao2.process();
  botao3.process();
  String texto = Serial1.readString();
  texto.trim();
  if (modo == "manual") {
    display.set(comandos[globalState]);
  }
  else if (modo == "automatico") {
    display.set("automatico");
  }
  
  if (texto != "") {
    if (texto[0] == '1') {
      tempo = millis();
      digitalWrite(led1, HIGH);
    }
    else if (texto[0] == '0') {
      digitalWrite(led1, LOW);
    }
    if (texto[2] == '1') {
      tempo = millis();
      digitalWrite(led2, HIGH);
    }
    else if (texto[2] == '0') {
      digitalWrite(led2, LOW);
    }
  
    if(millis() - tempo >= 1000){
      if(modo == "automatico"){
        modo = "manual"; 
        Serial1.println(modo);
      }
    }
  }
  display.update();
}
