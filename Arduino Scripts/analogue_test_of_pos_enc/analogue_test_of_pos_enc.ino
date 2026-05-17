
int bit_0_pin = 2;
int bit_1_pin = 3;
int bit_2_pin = 4;
int bit_3_pin = 5;
int bit_4_pin = 6;
int bit_5_pin = 7;
int bit_6_pin = 8;

int bit_0 = 0;
int bit_1 = 0;
int bit_2 = 0;
int bit_3 = 0;
int bit_4 = 0;
int bit_5 = 0;
int bit_6 = 0;

float dec_number = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(bit_0_pin, INPUT);
  pinMode(bit_1_pin, INPUT);
  pinMode(bit_2_pin, INPUT);
  pinMode(bit_3_pin, INPUT);
  pinMode(bit_4_pin, INPUT);
  pinMode(bit_5_pin, INPUT);
  pinMode(bit_6_pin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  bit_0 = digitalRead(bit_0_pin);
  bit_1 = digitalRead(bit_1_pin);
  bit_2 = digitalRead(bit_2_pin);
  bit_3 = digitalRead(bit_3_pin);
  bit_4 = digitalRead(bit_4_pin);
  bit_5 = digitalRead(bit_5_pin);
  bit_6 = digitalRead(bit_6_pin);

  dec_number = bit_0 * pow(2,0) + bit_1 * pow(2,1) + bit_2 * pow(2,2) + bit_3 * pow(2,3) + bit_4 * pow(2,4) + bit_5 * pow(2,5) + bit_6 * pow(2,6);
  if (dec_number > 0.5){
    Serial.println(dec_number);
  //delay(100);
  }
}
