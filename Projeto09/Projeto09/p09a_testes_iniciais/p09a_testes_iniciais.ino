//bibliotecas
#include <ShiftDisplay.h>
#include <GFButton.h>

//variaveis
int campainha = 3;
int potenciometro = A10;
GFButton botao1(A1);
GFButton botao2(A2);

int minimo = 0;
int maximo = 255;

int globalN = 0;

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

//funcoes
void frente_N() {
  Serial1.println("frente " + String(globalN)); 
}

void tras_N() {
  Serial1.println("tras " + String(globalN));
}

//setup
void setup () {
  //Mudar a Serial
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(9600);
  Serial1.setTimeout(10);
  pinMode(campainha, OUTPUT);
  pinMode(potenciometro, INPUT);
  digitalWrite(campainha, HIGH);
  display.set("Init");
  display.show(1000);
  botao1.setPressHandler(frente_N);
  botao2.setPressHandler(tras_N);
}

//loop
void loop() {
  botao1.process();
  botao2.process();
  String texto = Serial1.readString();
  int valorAnalogico = analogRead(potenciometro);
  int valorMapeado = map(valorAnalogico, 0, 1023, minimo, maximo);
  bool contagemX = texto.startsWith("contagem");
  texto.trim();
  if (texto != "") {
    if (texto == "tocar") {
      // toca a campainha
      digitalWrite(campainha, LOW);
      delay(200);
      digitalWrite(campainha, HIGH);
    }
    else if (contagemX == true) {
      display.set((texto.substring(9)).toInt());
      display.show(1000);
    }
    else {
     // Serial.println("Errou!");
    }
  }
  globalN = valorMapeado;
  display.set(valorMapeado);
  display.update();
}
