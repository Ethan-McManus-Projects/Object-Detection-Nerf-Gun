#include <Arduino.h>

// Define motor control pins
const int forwardPin = 8;
const int backwardPin = 12;

void setup() {
  // Start serial communication at a baud rate of 9600
  Serial.begin(9600);
  
  // Set motor control pins as outputs
  pinMode(forwardPin, OUTPUT);
  pinMode(backwardPin, OUTPUT);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte
    char command = Serial.read();
    
    // Based on the command, control the motor
    if (command == 'F') {
      // Spin motor forward
      digitalWrite(forwardPin, HIGH);
      digitalWrite(backwardPin, LOW);
    }
    else if (command == 'B') {
      // Spin motor backward
      digitalWrite(forwardPin, LOW);
      digitalWrite(backwardPin, HIGH);
    }
    else if (command == 'S') {
      // Stop the motor
      digitalWrite(forwardPin, LOW);
      digitalWrite(backwardPin, LOW);
    }
  }
}