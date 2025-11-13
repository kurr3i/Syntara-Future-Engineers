#include <RotaryEncoder.h>
#include <Servo.h>

const int BUTTON_PIN = 7;     
const int IN2 = 2;
const int IN1 = 3;

const char DCST = 'A';  // Motor forward
const char DCB  = 'B';  // Motor backward
const char DCS  = 'C';  // Motor stop
const char DL   = 'D';  // Dodge left
const char DR   = 'E';  // Dodge right
const char CCH  = 'Z';  // Confirm
const char FSIG = 'q';  // Signal sent when button pressed

Servo D;

long DU;
int DICM;
long RT = 0;
long LT = 0;
int posicion_anterior = 0;
int posicion_actual = 0;
char command = '\0';
const unsigned long DEBOUNCE_TIME = 150; // Tiempo de rebote en milisegundos
unsigned long lastPressTime = 0;
bool lastButtonState = LOW;


void setup() {
  D.attach(4);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Usa resistencia interna pull-up
  Serial.begin(115200);
  delay(100); // tiempo de estabilización
}

void loop() {
    bool buttonState = !digitalRead(BUTTON_PIN); 
  // (botón a GND: presionado = HIGH lógico, por eso el !)

  // Si el botón se presionó y pasó el tiempo de rebote
  if (buttonState && (millis() - lastPressTime) > DEBOUNCE_TIME) {
    Serial.write(FSIG);     // Enviar señal única 'q'
    lastPressTime = millis();
  }
    lastButtonState = buttonState;
     }

void serialEvent() {
  while (Serial.available()) {
    command = (char)Serial.read();

    Serial.print("Comando recibido: ");
    Serial.println(command);
    
    switch (command) {
      case DCST:

        break;

      case DCB:

        break;

      default:
        break;
    }
  }
}

