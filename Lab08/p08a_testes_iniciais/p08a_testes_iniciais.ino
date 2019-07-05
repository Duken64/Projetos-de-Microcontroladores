#include <GFButton.h>
#include <EEPROM.h>
#include <Servo.h>

GFButton botaoB(3);
int botaoA = 2;
int botaoC = 4;
int contador = 0;
int endereco = 0;
int AnguloOmbro = 90;
int potenciometro = A5;
int base = 12, ombro = 11;
Servo servoBase;
Servo servoOmbro;

void setup() {
    Serial.begin(9600);
    botaoB.setPressHandler(contaB);
    pinMode(potenciometro, INPUT);
    pinMode(botaoA, INPUT);
    pinMode(botaoC, INPUT);
    servoBase.attach(base);
    servoBase.write(45);
    servoOmbro.attach(ombro);
    servoOmbro.write(AnguloOmbro);
    EEPROM.get(endereco,contador);
}

void loop() {
    int contador1 = contador;
    botaoB.process();
    
    int valorLido = analogRead(potenciometro);
    int valorFinal = map(valorLido, 0, 1023, 0, 180);
//    Serial.println(valorFinal);
    servoBase.write(valorFinal);
    if(digitalRead(botaoA) == LOW && AnguloOmbro > 45){
      AnguloOmbro--;
      servoOmbro.write(AnguloOmbro);
      delay(15);
    }
    if(digitalRead(botaoC) == LOW && AnguloOmbro < 135){
      AnguloOmbro++;
      servoOmbro.write(AnguloOmbro);
      delay(15);
    }
    delay(50);
}

void contaB(){
  contador++;
  Serial.println(contador);
  EEPROM.put(endereco,contador);
}
