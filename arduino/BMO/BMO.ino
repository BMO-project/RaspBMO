#include <OneWire.h>  // 디지털 온도 센서를 사용하기 위해서는 이 라이브러리를 사용해야 한다.

OneWire ds(8); // 2번 핀에 연결된 OneWire 개체 생성

int btn_ESC = 2;
int btn_PONG = 3;
int btn_TEMP = 4;
int btn_FACE = 5;

int btn_UP = 11;
int btn_DOWN = 12;
boolean isRunning = false;

boolean isUp = false;
boolean isDown = false;

void setup() {
  Serial.begin(9600);
  pinMode(btn_PONG, INPUT_PULLUP);
  pinMode(btn_TEMP, INPUT_PULLUP);
  pinMode(btn_FACE, INPUT_PULLUP);
  pinMode(btn_ESC, INPUT_PULLUP);
  pinMode(btn_UP, INPUT_PULLUP);
  pinMode(btn_DOWN, INPUT_PULLUP);
}

void loop() {
  
  int pressed_PONG = digitalRead(btn_PONG);
  int pressed_TEMP = digitalRead(btn_TEMP);
  int pressed_FACE = digitalRead(btn_FACE);
  int pressed_ESC = digitalRead(btn_ESC);
  int pressed_UP = digitalRead(btn_UP);
  int pressed_DOWN = digitalRead(btn_DOWN);
  
  //Serial.println(pressed_PONG);

  if (!isRunning){
    if (pressed_PONG == 0){
      Serial.println("OPEN PONG");
      isRunning = true;
    }else if (pressed_TEMP == 0){
      Serial.println("OPEN TEMP");
//    float curTemp;
//    curTemp = getTemperature();
//    if (curTemp != -256){
//      Serial.print("MSG TEMP ");
//      Serial.println(curTemp);
//    }
      isRunning = true;
    }else if (pressed_FACE == 0){
      Serial.println("OPEN FACE");
      isRunning = true;
   }
   
  }else{
    if (pressed_ESC == 0){
    isRunning = false;
    Serial.println("PRESS ESC");
  }
  }
  

  if (pressed_UP == 0 && isUp == false){
    Serial.println("PRESS UP");
    isUp = true;
  }else if (pressed_UP == 1 && isUp == true){
    Serial.println("RELEASE UP");
    isUp = false;
  }
  
  if (pressed_DOWN == 0 && isDown == false){
    Serial.println("PRESS DOWN");
    isDown = true;
  }else if (pressed_DOWN == 1 && isDown == true){
    Serial.println("RELEASE DOWN");
    isDown = false;
  }
  
}

float getTemperature() {
  byte i;
  byte present = 0;

  byte data[12];
  byte addr[8];
  float Temp;

  if (!ds.search(addr)) {
    ds.reset_search();
    return -1;
  }
  
  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end
  //delay(500);

  present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad

  for (i = 0; i < 9; i++) { // 센서에서 가져온 값을 정리하고 난 후 배열에 순서대로 넣어 둔다.
    data[i] = ds.read();
  }

  Temp=(data[1]<<8)+data[0];
  Temp=Temp/16;
  // 위에서 받아온 값중에 1번 배열에 있는 값을 256배(2의 8승) 해주고 0번 배열에 있는 값과 더해준다.
  // 그 값을 16으로 나누면 섭씨 온도가 된다.

  // Serial.print("C=");
  // Serial.print(Temp);
  // Serial.print(", ");
  // 섭씨 출력
   return Temp;
}

