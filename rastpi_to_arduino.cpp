#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h" 

static const uint8_t PIN_MP3_TX = 12; // Connects to module's RX
static const uint8_t PIN_MP3_RX = 11; // Connects to module's TX
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);


bool verif = false;
bool green = false;
bool warn = false;
bool again_try = false;

DFRobotDFPlayerMini player;

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
}
/*_____________________________________________________Functions______________________________________________*/
void sound(int number){
  player.play(number);  
}

void leds(){
   if (green == true){
        //green
        //flashing green
        green = false;
   }else if (warn == true){
        // led red, blue and white;
    warn = false;
   }else if (again_try == true){
        //red and white
   }else if (verif == true){
        //leds flashing white and green and red
   }else{
        //leds flashing white
   }
}

void scanner(){
  //bolean default False
  /*if true
      stepper = ciertos grados o algo parecido
      scanner on, or just no hiden

    else:
      return
  */  
}

/*______________________________________________________REAL FUNCTIONS________________________________________*/
void pass(){
  green = true;
  Serial.print("PASS_MODE");
  sound(2);
}
void warning(){
  warn = true;
  Serial.print("WARNING_MODE");
  sound(4);
}
void try_again(){

}
void verification(){

}
void end_sound(){
  delay(10000);
  player.pause();   
}
/*_____________________________________________________LOOP___________________________________________________*/
void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readString(); 
    command.trim(); //trim for the spaces
    if (command == "PASS_MODE") {
      pass();
      end_sound();

    }else if (command == "WARNING_MODE") {
      warning(); 
      end_sound();
    }
  }

  leds();
  delay(100);
}