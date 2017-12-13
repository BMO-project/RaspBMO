#include <OneWire.h>  // 디지털 온도 센서를 사용하기 위해서는 이 라이브러리를 사용해야 한다.
#include <Wire.h>

//#include <Adafruit_Sensor.h> //기울기센서
//#include <Adafruit_ADXL345_U.h>

#include <SD.h>                      // need to include the SD library
#define SD_ChipSelectPin 4  //using digital pin 4 on arduino nano 328
//#include <TMRpcm.h>           //  also need to include this library...
#include <SPI.h> 

/* Assign a unique ID to this sensor at the same time */
//Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

//TMRpcm tmrpcm;

OneWire ds(8); // 2번 핀에 연결된 OneWire 개체 생성

int btn_ESC = A1;
int btn_PONG = A0;
int btn_TEMP = A2;
int btn_FACE = 5;

int btn_UP = 0;
int btn_DOWN = 2;
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

//  if(!accel.begin())
{
/* There was a problem detecting the ADXL345 … check your connections */
//Serial.println("Ooops, no ADXL345 detected … Check your wiring!");
//while(1);
//delay(1000);
Serial.println("OPEN FACE");
delay(1000);
}
}

void loop() {
//  delay(1000);
//  Serial.println("OPEN FACE");
  
  int pressed_PONG = digitalRead(btn_PONG);
  int pressed_TEMP = digitalRead(btn_TEMP);
  int pressed_FACE = 1;
  int pressed_ESC = digitalRead(btn_ESC);
  int pressed_UP = digitalRead(btn_UP);
  int pressed_DOWN = digitalRead(btn_DOWN);
  
//  Serial.println(pressed_ESC);

  if (!isRunning){
    if (pressed_PONG == 0){
//      delay(1000);
      Serial.println("OPEN PONG");
      delay(1000);
      Serial.println("OPEN PONG");
//      delay(1000);
      isRunning = true;
    }else if (pressed_TEMP == 0){
      Serial.println("OPEN TEMP");
      delay(1000);
      Serial.println("OPEN TEMP");
      delay(1000);
    float curTemp;
    curTemp = getTemperature();
    if (curTemp != -256){
      Serial.print("MSG TEMP ");
      Serial.println(curTemp);
    }
      isRunning = true;
    }else if (pressed_FACE == 0){
//      delay(1000);
      Serial.println("OPEN FACE");
      delay(1000);
      isRunning = true;
   }
   
  }else{
    if (pressed_ESC == 0){
    isRunning = false;
    Serial.println("PRESS ESC");
    delay(500);
    Serial.println("OPEN FACE");
    Serial.println("OPEN FACE");
    delay(1000);
  }
  }
  

  if (pressed_UP == 0 && isUp == false){
    Serial.println("PRESS UP");
    delay(200);
    isUp = true;
  }else if (pressed_UP == 1 && isUp == true){
    Serial.println("RELEASE UP");
    delay(200);
    isUp = false;
  }
  
  if (pressed_DOWN == 0 && isDown == false){
    Serial.println("PRESS DOWN");
    delay(200);
    isDown = true;
  }else if (pressed_DOWN == 1 && isDown == true){
    Serial.println("RELEASE DOWN");
    delay(200);
    isDown = false;
  }
}

//void getTilt(){
//  /* Get a new tilt sensor event */ 
//sensors_event_t event; 
//accel.getEvent(&event);
//
// float x= event.acceleration.x,y= event.acceleration.y,z= event.acceleration.z
//}
//
//void getVoice(){//play BMO voice!
//  tmrpcm.speakerPin = 9; //11 on Mega, 9 on Uno, Nano, etc
//
// 
//
//  if (!SD.begin(SD_ChipSelectPin)) {  // see if the card is present and can be initialized:
//
//  return;   // don't do anything more if not
//
//  }
// tmrpcm.volume(7);
// tmrpcm.setVolume(7);      //Serial.print("hi1");
//
// //tmrpcm.play("6.wav"); //the sound file "1" will play each time the arduino powers up, or is reset
//tmrpcm.play("0002.wav");
//}

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

