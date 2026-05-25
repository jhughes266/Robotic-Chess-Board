// setting up pin numbers
// pos enc sensor pins
int bit_0_pin = 2;
int bit_1_pin = 3;
int bit_2_pin = 4;
int bit_3_pin = 5;
int bit_4_pin = 6;
int bit_5_pin = 7;
int bit_6_pin = 8;
// motor direction pins
int mot_pos_pin = 9;
int mot_neg_pin = 10;
// motor pwm speed control pin
int motor_pwm_pin = 11;

// store the binary numbers coming in from the sensor
int bit_0;
int bit_1;
int bit_2;
int bit_3;
int bit_4;
int bit_5;
int bit_6;

// PID constants
float Kp = 1;
float Ki = 1;
float Kd = 1;



void move_to(int targ) {
  //controller variables
  float cur; 
  float err = 0;
  float prev_err;
  float err_int 0;
  float err_der = 0;
  float controller_output;
  float ideal_controller_output;
  float controller_max = 255;
  float controller_min = -255;
  // itteration tracker
  bool first_itteration = true;
  //time variable set up
  float cur_time = 0;
  float prev_time = 0;
  float dt = 0;

  while (true){
    // read the pos bit pins
    bit_0 = digitalRead(bit_0_pin);
    bit_1 = digitalRead(bit_1_pin);
    bit_2 = digitalRead(bit_2_pin);
    bit_3 = digitalRead(bit_3_pin);
    bit_4 = digitalRead(bit_4_pin);
    bit_5 = digitalRead(bit_5_pin);
    bit_6 = digitalRead(bit_6_pin);

    // time calculations when measurements are taken
    prev_time = cur_time;
    cur_time = (float)millis() / 1000;
    dt = cur_time - prev_time;

    // calculate the current position
    cur = bit_0 * 1 + bit_1 * 2 + bit_2 * 4 + bit_3 * 8 + bit_4 * 16 + bit_5 * 32 + bit_6 * 64;
    
    // error calculations
    prev_err = err;
    err = targ - cur;

    //system has settled stop driving the motor
    if(prev_err == err && err == 0){
      digitalWrite(mot_neg_pin, LOW);
      digitalWrite(mot_pos_pin, LOw);
      analogWrite(motor_pwm_pin, 255);
      break;
    }
    
    // different calculations based on whether or not it is the first loop itteration
    if(first_itteration){
      first_itteration = false; // change the flag
      controller_output = (Kp * err)
    }else{
      err_der = (err - prev_err) / dt; // error derivative
      ideal_controller_output = (Kp * err) + (Ki * err_int) + (Kd * err_der);

      //integral clamping prevents integral term from accumulating if the exceeding maximum or minimum of controller.
      if (ideal_controller_output >= controller_max && err > 0){ //motor going full tilt in a positive dirrection and reducing the error (error is positive)
      } else if (ideal_controller_output <= controller_min && err < 0) //motor going full tilt in a negative dirrection and reducing the error (error is negative)
      else{
        err_int += err * dt; //dont need to clamp
      }
      controller_output = (Kp * err) + (Ki * err_int) + (Kd * err_der);
    }


    // determing which way to spin the motor
    if (controller_output > 0){
      digitalWrite(mot_neg_pin, LOW);
      digitalWrite(mot_pos_pin, HIGH);
    } else if (controller_output < 0){
      digitalWrite(mot_pos_pin, LOW);
      digitalWrite(mot_neg_pin, HIGH);
      controller_output *= -1; // pwm doesnt excpet negative. Negative only affects direction of motor spin so now that we have done that we can change to positive
    }

    // 255 is 100% duty cycle control signal can not exceed 255
    if(controller_output > controller_max){
      contoller_output = controller_max;
    }

    // Control the motor
    analogWrite(motor_pwm_pin, controller_output);
  }
}


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
  pinMode(mot_pos_pin, OUTPUT);
  pinMode(mot_neg_pin, OUTPUT);
  pinMode(motor_pwm_pin, OUTPUT);
}

void loop() {


}
