#include <Servo.h>
Servo servoLower;
Servo servoUpper;
int lowerPos = 0;
int upperPos = 0;

int lowerStartPos = 95;
int upperStartPos = 141;

int lowerFinishPos = 20;
int upperFinishPos = 110;
void setup() {
  // put your setup code here, to run once:
  servoLower.attach(9);
  servoUpper.attach(10);
}

void loop() {
  delay(1000);
  servoLower.write(lowerStartPos);
  servoUpper.write(upperStartPos);
  delay(1000);
  servoLower.write(lowerFinishPos);
  delay(1000);
  servoUpper.write(upperFinishPos);
  /*
for(pos = 175; pos >= 90; pos -= 1)
  {
    testServo.write(pos);
    delay(50);
  }

  for(pos = 90; pos <= 175; pos += 1)
  {
    testServo.write(pos);
    delay(50);
  }
  */
}
