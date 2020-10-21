#include <Servo.h> // Include the servo library to control our servos

Servo Pan_Servo;
Servo Tilt_Servo;
int Pan_Sig_Pin = 9;
int Tilt_Sig_Pin = 10;
int Pan_Current = 90;
int Tilt_Current = 90;
int Camera_Direction = -1; // Value that changes whther the camera is mounted upside down or not. 1 is hanging and -1 is sitting on something

String s;
int hor_error = 0; // Default the position to be in the center of the range
int vert_error = 0; // Default the position to be in the center of the range
bool is_connected = false;

int tol = 25; //The tolerance for the servo to get within to be considered centered
int Jump_Size = 1;

void setup() {
  //Attach the two servos to their respective pins
  Pan_Servo.attach(Pan_Sig_Pin);
  Tilt_Servo.attach(Tilt_Sig_Pin);

  Serial.begin(115200);
  Pan_Servo.write(90); //Default the servo to 90 degrees (Centered)
  Tilt_Servo.write(90); //Default the servo to 90 degrees (Centered)
}

void loop() {
  //Check to see if we have position data coming from the camera
  if (Serial.available()) { //Check if there is serial data to be read

    //Read the current podition of the face
    s = Serial.readStringUntil('\n'); //Read a line of data until a '\n' character is found
    hor_error = s.substring(0, s.indexOf(',')).toInt(); //Break the string where a comma is found, the first half is the horizontal position and the second part is the vertical postion
    vert_error = s.substring(s.indexOf(',') + 1).toInt(); //Grab the vertical position
  }

  //Move the horizontal first
  if (hor_error < 0 && abs(hor_error) > tol) { // If the error is negative and greater than the tolerance, it needs to move
    Pan_Current += Camera_Direction * Jump_Size; // Add jump angle to the current angle
    Pan_Servo.write(Pan_Current); // and move to that angle
  } else if (hor_error > 0 && abs(hor_error) > tol) {
    Pan_Current -= Camera_Direction * Jump_Size;
    Pan_Servo.write(Pan_Current);
  }

  //Move the vertical axis
  if (vert_error < 0 && abs(vert_error) > tol) {
    Tilt_Current += Camera_Direction * Jump_Size;
    Tilt_Servo.write(Tilt_Current);
  } else if (vert_error > 0 && abs(vert_error) > tol) {
    Tilt_Current -= Camera_Direction * Jump_Size;
    Tilt_Servo.write(Tilt_Current);
  }

  delay(50); // Delay just about the same time as a single frame to avoid jitter
}
