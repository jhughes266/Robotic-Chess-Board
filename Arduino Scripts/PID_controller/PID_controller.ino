
int x_bit_0_pin = 2;
int x_bit_1_pin = 3;
int x_bit_2_pin = 4;
int x_bit_3_pin = 5;
int x_bit_4_pin = 6;
int x_bit_5_pin = 7;
int x_bit_6_pin = 8;

int x_bit_0 = 0;
int x_bit_1 = 0;
int x_bit_2 = 0;
int x_bit_3 = 0;
int x_bit_4 = 0;
int x_bit_5 = 0;
int x_bit_6 = 0;

float dec_number = 0;

void move_to(int x_pos) {
  int x_cur = -1; // init the current x_val to -1

  while (true){
    // read the x_pos bit pins
    x_bit_0 = digitalRead(x_bit_0_pin);
    x_bit_1 = digitalRead(x_bit_1_pin);
    x_bit_2 = digitalRead(x_bit_2_pin);
    x_bit_3 = digitalRead(x_bit_3_pin);
    x_bit_4 = digitalRead(x_bit_4_pin);
    x_bit_5 = digitalRead(x_bit_5_pin);
    x_bit_6 = digitalRead(x_bit_6_pin);

  }

}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(x_bit_0_pin, INPUT);
  pinMode(x_bit_1_pin, INPUT);
  pinMode(x_bit_2_pin, INPUT);
  pinMode(x_bit_3_pin, INPUT);
  pinMode(x_bit_4_pin, INPUT);
  pinMode(x_bit_5_pin, INPUT);
  pinMode(x_bit_6_pin, INPUT);

  // turn
  dec_number = x_bit_0 * 1 + 
               x_bit_1 * 2 + 
               x_bit_2 * 4 + 
               x_bit_3 * 8 + 
               x_bit_4 * 16 + 
               x_bit_5 * pow(2,5) + 
               x_bit_6 * pow(2,6);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  x_bit_0 = digitalRead(x_bit_0_pin);
  x_bit_1 = digitalRead(x_bit_1_pin);
  x_bit_2 = digitalRead(x_bit_2_pin);
  x_bit_3 = digitalRead(x_bit_3_pin);
  x_bit_4 = digitalRead(x_bit_4_pin);
  x_bit_5 = digitalRead(x_bit_5_pin);
  x_bit_6 = digitalRead(x_bit_6_pin);

  dec_number = x_bit_0 * pow(2,0) + 
               x_bit_1 * pow(2,1) + 
               x_bit_2 * pow(2,2) + 
               x_bit_3 * pow(2,3) + 
               x_bit_4 * pow(2,4) + 
               x_bit_5 * pow(2,5) + 
               x_bit_6 * pow(2,6);
  if (dec_number > 0.5){
    Serial.println(dec_number);
  //delay(10);
  }
}
