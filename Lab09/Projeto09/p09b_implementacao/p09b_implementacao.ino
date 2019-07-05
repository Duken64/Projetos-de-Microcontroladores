//libs
#include <GFButton.h>
#include <ShiftDisplay.h>

//variables
GFButton botao1(A1);
GFButton botao2(A2);
String  comandos[4] = { "frente", "tras", "esquerda","direita" };
int led1 = 10;
int led2 = 11;
ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int globalState = 0; 

//functions

void sendCommand(){
  //Serial.println("teste");
  Serial1.println(comandos[globalState]);
}

void mandaParar(){
  Serial1.println("parar");
}


void switchState(){
  globalState = (globalState + 1)%4 ;
  display.set(comandos[globalState]);
 }

//setup
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(9600);
  Serial1.setTimeout(10);
  botao1.setPressHandler(switchState);
  botao2.setPressHandler(sendCommand);
  botao2.setReleaseHandler(mandaParar);
  display.set(comandos[globalState]);
  display.update();

}

void loop() {
    botao1.process();
    botao2.process();
    String texto = Serial1.readString();
    texto.trim();
    Serial.println(texto);
    if(texto != "") {
        if(texto[0] == '1'){
          digitalWrite(led1, HIGH);
        }
        else if(texto[0] == '0'){
          digitalWrite(led1, LOW);
        }
        if(texto[2] == '1'){
          digitalWrite(led2, HIGH);
        }
        else if(texto[2] == '0'){
          digitalWrite(led2, LOW);
        }
    }
    display.update();
}
