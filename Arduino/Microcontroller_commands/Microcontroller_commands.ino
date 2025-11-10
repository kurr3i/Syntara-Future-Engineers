#include <RotaryEncoder.h>
#include <Servo.h>
#define Boton PORDEFINIR



const int IN2 = 2; //DC Motor pins
const int IN1 = 3;


const char DCST = 'A';  // DC Motor straight movement
const char DCB = 'B'; // DC Motor backwards movement
const char DCS = 'B'; // DC Motor stop
const char DL = 'B'; // Dodge left
const char DR = 'B'; // Dodge right
const char CCH = 'Z'; // Confirmation character

Servo D; // Created servo object "D" for direction control

long DU;  // Required variables for distance calculations
int DICM;
long RT = 0; // Encoder right ticks counted
long LT = 0; // Encoder left ticks counted
int posicion_anterior = 0; 
int posicion_actual = 0; 

void setup() {
  D.attach(4);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  Serial.begin(115200);
}

void loop() {

        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);

}