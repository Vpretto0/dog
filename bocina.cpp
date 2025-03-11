/*
  A sketch that will play sounds through a DFPlayer Mini
*/

// SoftwareSerial
#include <SoftwareSerial.h>
// DFRobot DFPlayer Mini
#include <DFRobotDFPlayerMini.h>

// DFPlayer Audio Board Declarations
#define SFX_RX 11                         // DIGITAL 11 pin for Serial Receive from DFPlayer
#define SFX_TX 12                         // DIGITAL 12 pin for Serial Transmit to DFPlayer
SoftwareSerial DFSerial(SFX_RX, SFX_TX);  // Create DFSerial object via SoftwareSerial defined pins
DFRobotDFPlayerMini myDFPlayer;           // Call DFRobot library to create myDFPlayer object
byte sfxVolume = 30;                      // Declare Initial audio volume variable and value: 0 NONE to 30 MAX

void setup() {
  // Initialize Serial Monitor Output @ 9600 baud
  Serial.begin(9600);
  
  // Setup DFPlayer
  DFSerial.begin(9600);               // Start DFSerial (SoftwareSerial) communication @ 9600 baud
  if (!myDFPlayer.begin(DFSerial)) {  // Start DFPlayer board and wait for initialization to complete
    while (true);
  }
  myDFPlayer.setTimeOut(100);     // Set Timeout on DFPlayer commands
  myDFPlayer.volume(sfxVolume);   // Set initial DFPlayer volume 
}

void loop() {
  myDFPlayer.play(1);   // Play 'Power ON' sound 0001-Lets's-See-Galaxy-Class.mp3
  delay(1s000);
  
  myDFPlayer.play(2);   // Play 'Power OFF' sound 0002-Dismissed.mp3
  delay(2000);
  
  myDFPlayer.loop(3);   // Play 'Impulse Engine' sound 0003-ImpulseEngine.mp3
  delay(5000);
  
  myDFPlayer.stop();    // Stop all sounds (including the looping sound)
  delay(1000);
}