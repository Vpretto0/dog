#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

SoftwareSerial mySoftwareSerial(2, 3); // RX, TX        o si no, cambiar
DFRobotDFPlayerMini myDFPlayer;

void setup()
{
  Serial.begin(9600);
  mySoftwareSerial.begin(9600);
  
  if (!myDFPlayer.begin(mySoftwareSerial)) {
    Serial.println("No detected DFPlayer Mini.");
    while (true); 
  }
  Serial.println("DFPlayer Mini conected");
}

void loop()
{
  myDFPlayer.play(1); 
  delay(1000);
}
