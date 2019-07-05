#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

GFButton button1(A1);
GFButton button2(A2);
ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
RotaryEncoder encoder(20, 21);

int leds[] = {13, 12, 11, 10};
int beep = 5, terra = A5, soundSensor = 19;
unsigned long lastTime = 0, lastPos = 0;
int count = 0;
int currentLED = 0;

void button1Pressed(GFButton& but) {
  tone(beep, 440, 500);
  Serial.println("button pressed");
}

void button2Pressed(GFButton& but) {
  Serial.println("button pressed");
  tone(beep, 220);
}

void button2Released(GFButton& but) {
  noTone(beep);
}

void soundDetected() {
  unsigned long now = millis();
  if (now > lastTime + 10) {
    Serial.println("som!");
    lastTime = now;
    display.set(++count);
    display.update();
  }
}

void enconderTick() {
  encoder.tick();
}

void rotaryChanged(int dir) {  
  for(int i = 0; i < 4; i++)
    digitalWrite(leds[currentLED], HIGH);
  //calcula novo current
  if (dir > 0)
    currentLED = (currentLED+1)%4;
  else if (dir<0){
    if(currentLED!= 0)
    {
      currentLED = abs(currentLED-1)%4 ;
    }
  }
    currentLED = abs(currentLED-1)%4 ;
  digitalWrite(leds[abs(currentLED)], LOW);
}

void setup() {
    Serial.begin(9600);
    pinMode(beep, OUTPUT);
    pinMode(terra, OUTPUT);
    pinMode(soundSensor, INPUT);
    
    for (int i=0; i<4; i++) {
      pinMode(leds[i], OUTPUT);
      digitalWrite(leds[i], HIGH);
    }
    digitalWrite(leds[0], LOW);
    digitalWrite(terra, LOW);
    
    button1.setPressHandler(button1Pressed);
    button2.setPressHandler(button2Pressed);
    button2.setReleaseHandler(button2Released);

    int origin = digitalPinToInterrupt(soundSensor);
    attachInterrupt(origin, soundDetected, RISING);

    int origin1 = digitalPinToInterrupt(20);
    attachInterrupt(origin1, enconderTick, CHANGE);
    int origin2 = digitalPinToInterrupt(21);
    attachInterrupt(origin2, enconderTick, CHANGE);
    
    display.set(0);
    display.update();
}

void loop() {
    button1.process();
    button2.process();

   int pos = abs(encoder.getPosition()%4);
   if (pos != lastPos) {
     digitalWrite(leds[lastPos],HIGH);
     digitalWrite(leds[pos],LOW);
     lastPos = pos;
   }
//  if (pos != lastPos) {
//     Serial.println("changed");
//     rotaryChanged(pos);
//     lastPos = pos; 
//   }
   display.update();
}
