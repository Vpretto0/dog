#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h" 


static const uint8_t PIN_MP3_TX = 2; // Connects to module's RX
static const uint8_t PIN_MP3_RX = 3; // Connects to module's TX
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);


const int pot = A5;
int potValue = 0;
bool verif = false;
bool green = false;
bool warn = false;
bool again_try = false;

DFRobotDFPlayerMini player;

void setup() {

  pinMode(pot, INPUT);

  
  Serial.begin(9600);
  softwareSerial.begin(9600);


  if (player.begin(softwareSerial)) {
    Serial.println("OK");

    player.volume(15);
  } else {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }      
}
/*_____________________________________________________Functions______________________________________________*/
void sound(int number, int duration_ms){
  potValue = analogRead(pot);

	if(potValue > 500 ){ 

	 static unsigned long timer = millis();
 	 if (millis() - timer > duration_ms) { //duration_ms is the duration of the audio(number)
  		timer = millis();

   		//(number) is the file number in the sd card, the order = the order you copied the file to it
   		player.play(number);  
    }
	}
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
  sound(1, 1500);
}
void warning(){
  warn = true;
  Serial.print("WARNING_MODE");
  sound(1, 1500);
}
void try_again(){

}
void verification(){

}

/*_____________________________________________________LOOP___________________________________________________*/
void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); //esto se puede cambiar a \r, pero no se si funcione
    if (command == "PASS_MODE") {
      pass();

    }else if (command == "WARNING_MODE") {
      warning(); 
    }
  }


  leds;
}