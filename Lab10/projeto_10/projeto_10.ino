
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
JKSButton botao;
int n = 0;

void setup() {
  tela.begin( tela.readID() );
  tela.fillScreen(TFT_BLACK);

  tela.fillRect(0,20, 110, 50, TFT_GREEN);
  tela.fillRect(130, 20, 110, 50, TFT_RED);
  tela.fillRect(0, 90, 70, 40, TFT_LIGHTGREY);
  tela.fillRect(80, 90, 70, 40, TFT_LIGHTGREY);
  tela.fillRect(160, 90, 70, 40, TFT_LIGHTGREY);


  for (int i=10;i>0;i--){
  tela.drawCircle(120, 170, 50/i, TFT_WHITE);
  }
  botao.init(&tela, &touch, 160, 270, 130, 80, TFT_WHITE, TFT_PURPLE,
  TFT_WHITE, "Contar", 2);
  botao.setPressHandler(desenhaRetangulo);
  botao.setReleaseHandler(apagaRetangulo);


}

void loop() {

botao.process();


}
void desenhaRetangulo (JKSButton &botaoPressionado) {
//tela.fillRect(50, 200, 140, 70, TFT_RED);
}
void apagaRetangulo (JKSButton &botaoPressionado) {
  tela.fillRect(20, 270, 140, 70, TFT_BLACK);
  
  n += 1;
 
  tela.setCursor(20, 270);
  tela.setTextColor(TFT_YELLOW);
  tela.setTextSize(4);
  tela.print(String(n));
}
