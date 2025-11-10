#include <RotaryEncoder.h>
#include <Servo.h>


const int IN2 = 2; //DC Motor pins
const int IN1 = 3;
const char DCST = 'A';  // DC Motor straight movement
const char DCB = 'B'; // DC Motor backwards movement
const char DCS = 'B'; // DC Motor stop
const char DL = 'B'; // Dodge left
const char DR = 'B'; // Dodge right
const char ACK_OK = 'Z'; // Confirmation character
Servo D;


void setup() {
  miServo.attach(4);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {

    char incomingByte = Serial.read(); 
    
    // 3. Lógica de Control
    if (incomingByte == S) {
      
      // Comando 'A' recibido: Encender el LED
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
      Serial.write(ACK_OK); // Enviar confirmación a Python
      
    } else if (incomingByte == S) {
      
      // Comando 'B' recibido: Apagar el LED
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
      Serial.write(ACK_OK); // Enviar confirmación a Python
      
    } else {
      
      // Carácter no reconocido
      Serial.print("Comando desconocido: ");
      Serial.println(incomingByte); // Muestra el carácter recibido
      // No enviamos ACK_OK, o podrías usar 'E' de Error si Python lo espera
    }
  }
}