//setting up pin numbers
int x_bit_0_pin = 2;
int x_bit_1_pin = 3;
int x_bit_2_pin = 4;
int x_bit_3_pin = 5;
int x_bit_4_pin = 6;
int x_bit_5_pin = 7;
int x_bit_6_pin = 8;

int x_mot_pos_pin = 9;
int x_mot_neg_pin = 10;

int x_bit_0;
int x_bit_1;
int x_bit_2;
int x_bit_3;
int x_bit_4;
int x_bit_5;
int x_bit_6;

int x_motor_pwm_pin = 11;

int x_cur;

void move_to(int x_targ) {
  x_cur = -1; // init the current x_val to -1
  int max_val = 120;
  int min_val = 1;
  int x_err;
  float
  float x_err_min_max_scaled;
  float x_err_motor_moving_scaled;
  float min_moving_pwm_prop = 0.75;


  while (true){
    // read the x_pos bit pins
    x_bit_0 = digitalRead(x_bit_0_pin);
    x_bit_1 = digitalRead(x_bit_1_pin);
    x_bit_2 = digitalRead(x_bit_2_pin);
    x_bit_3 = digitalRead(x_bit_3_pin);
    x_bit_4 = digitalRead(x_bit_4_pin);
    x_bit_5 = digitalRead(x_bit_5_pin);
    x_bit_6 = digitalRead(x_bit_6_pin);

    //calculate the current x value
    x_cur = x_bit_0 * 1 + 
               x_bit_1 * 2 + 
               x_bit_2 * 4 + 
               x_bit_3 * 8 + 
               x_bit_4 * 16 + 
               x_bit_5 * 32 + 
               x_bit_6 * 64;
    
    //calculate the x error
    x_err = x_targ - x_cur;
    //gets the error as a proportion min max scaled
    x_err_min_max_scaled = (x_err - min_val)/(max_val - min_val);
    //scaling the error again so that even on lower errors the motor can still move. This forces the scaled error between the minimum moving proportion and 1
    x_err_motor_moving_scaled = x_err_min_max_scaled * (1 - min_moving_pwm_prop) + min_moving_pwm_prop;
    //determing which way to spin the motor
    if (x_err > 0){
      digitalWrite(x_mot_neg_pin, LOW);
      digitalWrite(x_mot_pos_pin, HIGH);
    } else if ( x_err < 0){
      digitalWrite(x_mot_pos_pin, LOW);
      digitalWrite(x_mot_neg_pin, HIGH);
    } else {
      digitalWrite(x_mot_pos_pin, LOW);
      digitalWrite(x_mot_neg_pin, LOW);
      analogWrite(x_motor_pwm_pin, 0);

    }
    //pwm the error. The "x_err_motor_moving_scaled" is a proportion * 255 gets it in the right range
    analogWrite(x_motor_pwm_pin, x_err_motor_moving_scaled * 255);
    
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
  pinMode(x_mot_pos_pin, OUTPUT);
  pinMode(x_mot_neg_pin, OUTPUT);
  pinMode(x_motor_pwm_pin, OUTPUT);
}

void loop() {

  //analogWrite(x_motor_pwm_pin, 255);
  //digitalWrite(x_motor_pwm_pin, HIGH);

}
