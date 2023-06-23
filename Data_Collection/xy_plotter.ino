#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield s = Adafruit_MotorShield();
Adafruit_StepperMotor *x = s.getStepper(400, 2);
Adafruit_StepperMotor *y = s.getStepper(400, 1);

//int x_target = 0;
//int y_target = 0;
int x_pos = 30; // Set this to 90 so as to avoid the bars
int y_pos = 0;
char mode = 'D';
int sleep_time = 0;
int step_mode = SINGLE;

float x_delta;
float y_delta;

//These let us know when the motor has reached (0,0)
const int y_limit_pin = 4;
const int x_limit_pin = 3;

// This is a digital out that will be used to
// let us know that the motors are in motion
const int movement_output = 13;
const int record_tgl = 12;
const int enable_pin = 11;
int record_signal_in = 0;

bool x_coarse = false;
bool y_coarse = false;
bool x_homed = false;
bool y_homed = false;

bool break_tgl = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(y_limit_pin, INPUT);
  pinMode(x_limit_pin, INPUT);
  pinMode(movement_output, OUTPUT);
  digitalWrite(movement_output, LOW);
  pinMode(record_tgl, OUTPUT);
  digitalWrite(record_tgl, LOW);
  pinMode(enable_pin, OUTPUT);
  digitalWrite(enable_pin, HIGH);



  Serial.begin(9600);
  // Let python know we are online
  Serial.write(1);
  while (!Serial.available()) {} //wait for input
  //Let python know we are homing
  Serial.write(0);
  s.begin();
  x->setSpeed(100);
  y->setSpeed(100);

  // ==========
  // X homing
  // ==========
  digitalWrite(movement_output, HIGH);

  while (!x_coarse) {
    x->step(1, BACKWARD, DOUBLE);
    if (digitalRead(x_limit_pin) == HIGH) {
      x_coarse = true;
    }
  }
  x->step(20, FORWARD, DOUBLE);
  while (!x_homed) {
    x->step(1, BACKWARD, MICROSTEP);
    if (digitalRead(x_limit_pin) == HIGH) {
      x_homed = true;
    }
  }
  x->step(x_pos * 5.5556, FORWARD, DOUBLE);

  // ============
  // Y homing
  // ============
  while (!y_coarse) {
    y->step(1, FORWARD, DOUBLE);
    if (digitalRead(y_limit_pin) == HIGH) {
      y_coarse = true;
    }
  }

  y->step(20, BACKWARD, DOUBLE);

  while (!y_homed) {
    y->step(1, FORWARD, MICROSTEP);
    if (digitalRead(y_limit_pin) == HIGH) {
      y_homed = true;
    }
  }
  digitalWrite(movement_output, LOW);
  Serial.write(1);
  Serial.flush();
  x->release();
  y->release();
  while (Serial.available()) {
    Serial.read(); //clear serial input
  }
}

void loop() {
  // =====================
  // Check for record signal
  // =====================
  while (!Serial.available()) {} // wait for input
  record_signal_in = Serial.read();
  if (record_signal_in == 2) { // If the recording is starting, send a toggle pulse
    digitalWrite(enable_pin, LOW);
    delay(100);
    digitalWrite(record_tgl, HIGH);
    delay(1);
    digitalWrite(enable_pin, HIGH);
    delay(1);
    digitalWrite(record_tgl, LOW);
    delay(100);


  }
  else if (record_signal_in == 3) { //If the recording is over, send a record toggle pulse, release the motors, and dont continue on
    digitalWrite(enable_pin, LOW);
    delay(100);
    digitalWrite(record_tgl, HIGH);
    delay(1);
    digitalWrite(enable_pin, HIGH);
    delay(1);
    digitalWrite(record_tgl, LOW);
    
    delay(100);
    x->release();
    y->release();
    while (true) {
      delay(1000);
    }
  }
  Serial.write(1);

  // ================================ //
  // Get X target
  // ================================ //
  while (!Serial.available()) {} //wait for input
  int x_target = Serial.parseInt();
  // Prevent stupid inputs
  if (x_target > 390) {
    x_target = 390;
  }
  if (x_target < 0) {
    x_target = 0;
  }
  // Let python know the message was received
  Serial.write(1);

  // ================================ //
  // Get Y target
  // ================================ //
  while (!Serial.available()) {} //wait for input

  int y_target = Serial.parseInt();
  // Prevent stupid inputs
  if (y_target > 325) {
    y_target = 325;
  }
  if (y_target < 0) {
    y_target = 0;
  }

  // Let python know the message was received
  Serial.write(1);
  // ================================ //
  // Get mode ('S','D','M','I')
  // ================================ //
  while (!Serial.available()) {} //wait for input
  char mode = Serial.read();
  // Let python know the message was received
  Serial.write(1);

  // ================================ //
  // Calculate Delta
  // ================================ //
  x_delta = (x_target - x_pos) * 5.55556;
  y_delta = (y_target - y_pos) * 5.55556;

  // Wrie message of new coordinates
  Serial.println("X target:");
  Serial.println(x_target, DEC);

  Serial.println("Y target:");
  Serial.println(y_target, DEC);


  // ================================ //
  // Set step_mode
  // ================================ //

  if (mode == 'S') {
    step_mode = SINGLE;
  }
  else if (mode == 'D') {
    step_mode = DOUBLE;
  }
  else if (mode == 'I') {
    step_mode = INTERLEAVE;
  }
  else if (mode == 'M') {
    step_mode = MICROSTEP;
  }


  digitalWrite(movement_output, HIGH);
  // ================================ //
  // Move Y
  // ================================ //
  if (y_delta >= 0) {
    y->step(y_delta, BACKWARD, step_mode);
  }
  else {
    y_delta = -y_delta;
    y->step(y_delta, FORWARD, step_mode);
  }

  // ================================ //
  // Move X
  // ================================ //

  if (x_delta >= 0) {
    x->step(x_delta, FORWARD, step_mode);
  }
  else {
    x_delta = -x_delta;
    x->step(x_delta, BACKWARD, step_mode);
  }
  digitalWrite(movement_output, LOW);
  // ================================ //
  // Set new position
  // ================================ //
  x_pos = x_target;
  y_pos = y_target;

  // Let python know the motors have finished moving
  Serial.write(2);

  x->release();
  y->release();
}

