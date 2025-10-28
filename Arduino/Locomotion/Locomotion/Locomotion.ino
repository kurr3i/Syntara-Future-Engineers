#include <RotaryEncoder.h>

RotaryEncoder encoder(3, 4); 
#define Boton 2


long giros_derecha = 0;
long giros_izquierda = 0;

int posicion_anterior = 0; 
int posicion_actual = 0; 



void checkPosition() {
  encoder.tick(); 
}

void setup() {
  Serial.begin(9600);
  pinMode(Boton, INPUT_PULLUP);
  

  attachInterrupt(digitalPinToInterrupt(3), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(4), checkPosition, CHANGE);

  Serial.println("Contadores de Izquierda/Derecha Inicializados. (Escala NO absoluta)");
}


void loop() {
  

  posicion_actual = encoder.getPosition();


  if (posicion_actual != posicion_anterior) {
    
    if (posicion_actual > posicion_anterior) {

      giros_derecha++;
      Serial.print("DERECHA. Ticks: ");
      Serial.println(giros_derecha);
      
    } else {

      giros_izquierda++;
      Serial.print("IZQUIERDA. Ticks: ");
      Serial.println(giros_izquierda);
    }
    

    posicion_anterior = posicion_actual;
  }
  

  if (!digitalRead(Boton)) {
    Serial.println("\nBOTON PRESIONADO - Reiniciando ambos contadores a CERO.");
    

    giros_derecha = 0;
    giros_izquierda = 0;

    
    delay(250); 
  }
}