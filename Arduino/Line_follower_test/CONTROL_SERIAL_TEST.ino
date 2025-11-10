#include <Servo.h>

// Definiciones de Hardware
const int PIN_SERVO = 2; // Conecta la señal del servo al pin digital 2 (idealmente un pin PWM)

// El valor 90 es la posición de "detenido" para muchos servos de rotación continua.
// El valor 180 (o 0) es la velocidad máxima en una dirección.
const int VELOCIDAD_MOVER = 180;
const int VELOCIDAD_PARAR = 90;

Servo miServo;
char comando_recibido = ' ';

void setup() {
  // Inicia la comunicación serial a 115200 baudios
  Serial.begin(115200);
  while (!Serial); // Espera a la conexión serial (necesario para placas con USB nativo)
  
  // Conecta el objeto Servo al pin
  miServo.attach(PIN_SERVO);
  
  // Inicializa el servo en la posición de "parado"
  miServo.write(VELOCIDAD_PARAR);
  
  Serial.println("Servo Controller Ready. Waiting for M or S.");
  // PARA ENCODER, ESTUDIAR DESPUÉS
  pinMode(Boton, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(3), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(4), checkPosition, CHANGE);
  Serial.println("Contadores de Izquierda/Derecha Inicializados. (Escala NO absoluta)");
}

void loop() {
  if (Serial.available() > 0) {
    comando_recibido = Serial.read();
    
    switch (comando_recibido) {
      case 'M':
        // Mover el motor (Cerrar la mano)
        miServo.write(VELOCIDAD_MOVER);
        Serial.write('A'); // Enviar ACK
        break;
        
      case 'S':
        // Parar el motor (Abrir la mano)
        miServo.write(VELOCIDAD_PARAR);
        Serial.write('A'); // Enviar ACK
        break;
        
      default:
        // Comando no reconocido
        Serial.write('E'); // Enviar Error
        break;    
    }
  }
}
