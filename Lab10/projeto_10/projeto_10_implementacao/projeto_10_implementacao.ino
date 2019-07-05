#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
JKSButton botao1, botao2, botao3, botao4, botao5;
//const int TS_LEFT = 145, TS_RT = 887, TS_TOP = 934, TS_BOT = 158;
int n = 0;


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  //Serial1.begin(9600);
  tela.begin( tela.readID() );
  tela.fillScreen(TFT_BLACK);

  botao1.init(&tela, &touch, 50, 50, 100, 50, TFT_WHITE, TFT_GREEN,
              TFT_BLACK, "Decolar", 2);

  botao2.init(&tela, &touch, 170, 50, 110, 50, TFT_WHITE, TFT_RED,
              TFT_WHITE, "Pousar", 2);

  botao3.init(&tela, &touch, 35, 110, 60, 40, TFT_WHITE, TFT_LIGHTGREY,
              TFT_BLACK, "<", 2);

  botao4.init(&tela, &touch, 115, 110, 70, 40, TFT_WHITE, TFT_LIGHTGREY,
              TFT_BLACK, "^", 2);

  botao5.init(&tela, &touch, 195, 110, 70, 40, TFT_WHITE, TFT_LIGHTGREY,
              TFT_BLACK, ">", 2);

  //desenhaBateria("bateria 54");

  tela.drawRect(10, 160, 200, 150, TFT_WHITE);
  desenhaBateria();

  botao1.setPressHandler(decolar);
  botao2.setPressHandler(pousar);
  botao3.setPressHandler(esquerda);
  botao4.setPressHandler(frente);
  botao5.setPressHandler(direita);
  botao3.setReleaseHandler(parar);
  botao4.setReleaseHandler(parar);
  botao5.setReleaseHandler(parar);
}

void loop() {
  desenhaBateria();
  botao1.process();
  botao2.process();
  botao3.process();
  botao4.process();
  botao5.process();
}

void escreveTexto(int x, int y, String palavra, int cor )
{
  tela.setCursor(x, y);
  tela.setTextColor(cor);
  tela.setTextSize(2);
  tela.print(palavra);
}

void desenhaBateria()
{ String texto = Serial.readString();
  texto.trim();
  tela.setCursor(10, 140);
  tela.setTextColor(TFT_YELLOW);
  tela.setTextSize(2);
  tela.print("Bateria:");
  if (texto != "") {
    if (texto.startsWith("bateria"))
    {
      String percent = texto.substring(8);
      tela.setCursor(110, 140);
      tela.setTextColor(TFT_YELLOW);
      tela.setTextSize(2);
      tela.print(percent + "%");
    }
    else {
      tela.fillRect(10, 160, 200, 150, TFT_BLACK);
      tela.drawRect(10, 160, 200, 150, TFT_WHITE);
      String x = texto.substring(10, 13);
      int numX = x.toInt();
      String y = texto.substring(14, 17);
      int numY = y.toInt();
      String comp = texto.substring(18, 21);
      int numComp = comp.toInt();
      String alt = texto.substring(22, 25);
      int numAlt = alt.toInt();

      int mapX = map(numX, 0, 480, 0, 200) + 10;
      int mapY = map(numY, 0, 640, 0, 150) + 180;
      int mapComp = map(numComp, 0, 480, 0, 200);
      int mapAlt = map(numAlt, 0, 640, 0, 150);
      tela.fillRect(mapX, mapY, mapComp, mapAlt, TFT_YELLOW);
      tela.drawRect(mapX, mapY, mapComp, mapAlt, TFT_YELLOW);
    }
  }
}

void decolar()
{
  Serial.println("decolar");
}
void pousar()
{
  Serial.println("pousar");
}
void esquerda()
{
  Serial.println("esquerda");
}
void frente()
{
  Serial.println("frente");
}
void direita()
{
  Serial.println("direita");
}
void parar()
{
  Serial.println("parar");
}
