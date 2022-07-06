#include <AccelStepper.h>           // Laden von AccelStepper Bibliothek

#define motorPin1  8                // IN1 pin on the ULN2003A driver
#define motorPin2  9                // IN2 pin on the ULN2003A driver
#define motorPin3  10               // IN3 pin on the ULN2003A driver
#define motorPin4  11               // IN4 pin on the ULN2003A driver

int stepsPerRevolution = 64;        // steps per revolution
float degreePerRevolution = 5.625;  // degree per revolution
int incomingByte;

AccelStepper stepper(AccelStepper::HALF4WIRE, motorPin1, motorPin3, motorPin2, motorPin4);

void setup() {
  Serial.begin(9600);               // Initialisierung von SerialMonitor

  stepper.setMaxSpeed(1000.0);      // Maximal Geschwindigkeit einstellen
  stepper.setAcceleration(100.0);   // Maximal Beschleunigung einstellen
  stepper.setSpeed(200);            // Geschwindig einstellen

  stepper.moveTo(degToSteps(360));   // Drehung des Motor um 360°

}

void loop() {
  if (Serial.available()>0)
  {
    incomingByte = Serial.read();
    if(incomingByte == 'S'){
      Serial.write("Starten");
      stepper.run(); 
    }
    if(incomingByte =='H'){
      Serial.write("Halten");
      stepper.stop();
    }
    
  }
                     // start moving the motor
}

//konvertiert Grad auf Stepps
float degToSteps(float deg) {
  return (stepsPerRevolution / degreePerRevolution) * deg;
}
