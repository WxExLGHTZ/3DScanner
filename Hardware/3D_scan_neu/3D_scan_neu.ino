#include <Stepper.h>
const int steps_pro_revolution = 2048;
const int rpm = 10;
Stepper steppermotor = Stepper(steps_pro_revolution, 8, 10, 9, 11);

void setup(){
  steppermotor.setSpeed(rpm);
  Serial.begin(9600);
}
void loop(){
  if (Serial.available() > 5) {
    bool befehl = Serial.read();
    long steps = 0;
    for (int i = 0; i <= 5; i++){
      steps = (steps * 10) + Serial.read();
    }
    steps = (steps+1)/10;
    if (befehl){
      steps = -steps;
    }
    steppermotor.step(steps);
    Serial.print(steps);
  }
}
