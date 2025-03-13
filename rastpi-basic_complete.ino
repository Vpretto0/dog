#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>
#include <Servo.h>

static const uint8_t PIN_MP3_TX = 12; //RX dfplayer module
static const uint8_t PIN_MP3_RX = 11; //TX dfplayer module
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);

//BOOLEANS:
bool verif = false;
bool green = false;
bool warn = false;
bool again_try = false;
bool while_true = true;

//LED #1:
int red_pin_led1 = 2;
int green_pin_led1 = 3;
int blue_pin_led1 = 4;

//LED #2:
int red_pin_led2 = 5;
int green_pin_led2 = 6;
int blue_pin_led2 = 7;

//LED #3:
int red_pin_led3 = 8;
int green_pin_led3 = 9;
int blue_pin_led3 = 10;

//SERVO:
int servo_pin = 13;
int servo_position = 0;

//library name:
DFRobotDFPlayerMini player;
Servo servo;

void setup() {
  Serial.begin(9600);
  softwareSerial.begin(9600);
  Serial.println("speaker ready");

  if (player.begin(softwareSerial)) {
    Serial.println("OK, it is connected to the Speaker");
    player.volume(15);
    player.play(2);
    delay(3000);
    player.pause(); 
  } else {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }  
  
  pinMode(red_pin_led1,  OUTPUT);              
  pinMode(green_pin_led1, OUTPUT);
  pinMode(blue_pin_led1, OUTPUT);

  pinMode(red_pin_led2,  OUTPUT);              
  pinMode(green_pin_led2, OUTPUT);
  pinMode(blue_pin_led2, OUTPUT);

  pinMode(red_pin_led3,  OUTPUT);              
  pinMode(green_pin_led3, OUTPUT);
  pinMode(blue_pin_led3, OUTPUT);

  servo.attach(servo_pin);
}
/*_____________________________________________________Functions______________________________________________*/
void sound(int number){
  player.play(number);  
}

void leds(){
  int count = 0;
//GREEN MODE:
  if (green == true){
    verif = false;
    int count = 0;
    set_color_led1(0, 255, 0);
    set_color_led2(0, 255, 0);
    set_color_led3(0, 255, 0);
    delay(500);
    set_color_led1(0, 0, 0);
    delay(250);
    set_color_led2(0, 0, 0);
    delay(250);
    set_color_led3(0, 0, 0);
    count= 5;
    while(count > 0 ) 
    {
      delay(500);
      set_color_led1(0, 255, 0);
      set_color_led2(0, 255, 0);
      set_color_led3(0, 255, 0);
      delay(500);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      count = count -1;  
    }
    count= 10;
    while(count > 0 ) 
    {
      delay(250);
      set_color_led1(0, 255, 0);
      set_color_led2(0, 255, 0);
      set_color_led3(0, 255, 0);
      delay(250);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      count = count -1;  
    }
    count= 15;
    while(count > 0 ) 
    {
      delay(50);
      set_color_led1(0, 255, 0);
      set_color_led2(0, 255, 0);
      set_color_led3(0, 255, 0);
      delay(50);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      count = count -1;  
    }
    set_color_led1(0, 0, 0);
    set_color_led2(0, 0, 0);
    set_color_led3(0, 0, 0);
    green = false;

//WARN MODE:
  }else if (warn == true){
    verif = false; 
    sset_color_led1(255, 0, 0);
    set_color_led2(255, 0, 0);
    set_color_led3(255, 0, 0);
    delay(500);
    set_color_led1(0, 0, 255);
    set_color_led2(0, 0, 255);
    set_color_led3(0, 0, 255);
    delay(500);
    set_color_led1(255, 255, 255);
    set_color_led2(255, 255, 255);
    set_color_led3(255, 255, 255);
    delay(500);
    set_color_led1(255, 255, 255);
    set_color_led2(255, 255, 255);
    set_color_led3(255, 255, 255);
    delay(750);
    set_color_led1(255, 255, 255);
    set_color_led2(255, 255, 255);
    set_color_led3(255, 255, 255);
    delay(750);
    count = 50;
    while(count > 0 ) 
    {
      set_color_led1(255, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(255, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(255, 0, 0);
      delay(100);

      set_color_led1(255, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(255, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(255, 0, 0);
      delay(100);

      set_color_led1(255, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(255, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(255, 0, 0);


      delay(100);
      set_color_led1(0, 0, 255);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 255);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 255);
      delay(100);

      set_color_led1(0, 0, 255);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 255);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 255);
      delay(100);

      set_color_led1(0, 0, 255);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 255);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 255);
      delay(100);


      set_color_led1(255, 255, 255);
      set_color_led2(255, 255, 255);
      set_color_led3(255, 255, 255);
      delay(300);
      set_color_led1(255, 255, 255);
      set_color_led2(255, 255, 255);
      set_color_led3(255, 255, 255);
      delay(300);
      count = count -1;  
    }
    set_color_led1(255, 0, 0);
    set_color_led2(0, 0, 255);
    set_color_led3(255, 255, 255);
    delay(500);
    set_color_led1(0, 0, 0);
    set_color_led2(0, 0, 0);
    set_color_led3(0, 0, 0);
    warn = false;
  }else if (again_try == true){
    verif = false;
    set_color_led1(255, 0, 0);
    set_color_led2(255, 0, 0);
    set_color_led3(255, 0, 0);
    delay(50);
    set_color_led1(255, 255, 255);
    set_color_led2(255, 255, 255);
    set_color_led3(255, 255, 255);
    delay(50);
    set_color_led1(255, 0, 0);
    delay(50);
    set_color_led2(255, 0, 0);
    delay(50);
    set_color_led3(255, 0, 0);
    delay(50);
    count = 10;
    while(count > 0 ) 
    {
      delay(100);
      set_color_led1(255, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(255, 255, 255);
      set_color_led2(0, 0, 0);
      set_color_led3(0, 0, 0);
      count = count -1;  
    }
    count = 10;
    while(count > 0 ) 
    {
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(255, 0, 0);
      set_color_led3(0, 0, 0);
      delay(100);
      set_color_led1(0, 0, 0);
      set_color_led2(255, 255, 255);
      set_color_led3(0, 0, 0);
      count = count -1;  
    }
    count = 10;
    while(count > 0 ) 
    {
      delay(250);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(255, 0, 0);
      delay(250);
      set_color_led1(0, 0, 0);
      set_color_led2(0, 0, 0);
      set_color_led3(255, 255, 255);
      count = count -1;  
    }
    set_color_led1(0, 0, 0);
    set_color_led2(0, 0, 0);
    set_color_led3(0, 0, 0);
    again_try = false;

  }else if (verif == true){
      count = 50;
    while(count > 0 ) 
    {
      set_color_led1(255, 0, 0);
      set_color_led2(0, 255, 0);
      set_color_led3(255, 255, 255);
      delay(100);
      set_color_led1(255, 255, 255);
      set_color_led2(255, 0, 0);
      set_color_led3(0, 255, 0);
      delay(100);
      set_color_led1(0, 255, 0);
      set_color_led2(255, 255, 255);
      set_color_led3(255, 0, 0);
      delay(100);
      set_color_led1(0, 255, 0);
      set_color_led2(255, 0, 0);
      set_color_led3(255, 255, 255);
      delay(100);
      set_color_led1(255, 255, 255);
      set_color_led2(0, 255, 0);
      set_color_led3(255, 0, 0);
      delay(100);
      set_color_led1(255, 0, 0);
      set_color_led2(255, 255, 255);
      set_color_led3(0, 255, 0);
      delay(100);
      count = count -1;  
    }
    set_color_led1(0, 0, 0);
    set_color_led2(0, 0, 0);
    set_color_led3(0, 0, 0);
    verif = false;
  }else{
    if (while_true == true){
      count = 20;
      while(count > 0 ) 
      {
        set_color_led1(255, 255, 255);
        set_color_led2(255, 255, 255);
        set_color_led3(255, 255, 255);
          delay(100);
          set_color_led1(0, 0, 0);
          set_color_led2(0, 0, 0);
          set_color_led3(0, 0, 0);
          delay(100);
          count = count -1;
      }
    }  
  }
}

/*______________________________________________________REAL FUNCTIONS________________________________________*/
void pass(){
  while_true = false;
  green = true;
  Serial.print("PASS_MODE Started");
  sound(2);
}

void warning(){
  while_true = false;
  warn = true;
  Serial.print("WARNING_MODE Started");
  sound(4);
}

void try_again(){
  while_true = false;
  again_try = true;
  Serial.print("TRY_AGAIN_MODE Started");
  sound(3);
}

void verification_true(){
  while_true = false;
  verif = true;
  if (verif == true){
    Serial.print("VERIFICATION_MODE Activated");
    sound(3);
    for (servo_position = 0; servo_position <= 90; servo_position += 1) {  //va de a uno
    servo.write(servo_position);  
    delay(15);    
  }
  }
}
void verification_false(){
  while_true = false;
  verif = false;
  if (verif == false){
    Serial.print("VERIFICATION_MODE Deactivated");
    sound(1);
    for (servo_position = 90; servo_position >= 0; servo_position -= 1) { //este tambien
    servo.write(servo_position); 
    delay(15);
  }
  }
}

void end_sound(){
  delay(5000);
  player.pause();   
}

void set_color_led1( int red_led, int green_led, int blue_led){
  analogWrite(red_pin_led1, red_led);
  analogWrite(green_pin_led1, green_led);
  analogWrite(blue_pin_led1, blue_led);
}
void set_color_led2( int red_led, int green_led, int blue_led){
  analogWrite(red_pin_led2, red_led);
  analogWrite(green_pin_led2, green_led);
  analogWrite(blue_pin_led2, blue_led);
}
void set_color_led3( int red_led, int green_led, int blue_led){
  analogWrite(red_pin_led3, red_led);
  analogWrite(green_pin_led3, green_led);
  analogWrite(blue_pin_led3, blue_led);
}

/*_____________________________________________________LOOP___________________________________________________*/
void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); 
    command.trim(); //trim for the spaces

    if (command == "VERIFICATION_MODE_TRUE") {
        verification_true();
        leds();
        end_sound();
        return;
    }
    if (command == "VERIFICATION_MODE_FALSE") {
        verification_false();
        leds();
        end_sound();
        return;
    }
    if (command == "PASS_MODE") {
        pass();
        leds();
        end_sound();
        return;
    }
    if(command == "TRY_AGAIN_MODE"){
        try_again();
        leds();
        end_sound();
        return;
    }
    if (command == "WARNING_MODE") {
        warning();
        leds();
        end_sound();
        return;
    }
  }
  delay(100);
}