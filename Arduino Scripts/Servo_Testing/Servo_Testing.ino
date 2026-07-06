#include <Servo.h>
Servo testServo;
int pos = 0;
void setup() {
  // put your setup code here, to run once:
  testServo.attach(9);
}

void loop() {
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
}
