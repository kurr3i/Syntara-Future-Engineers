// Definición de pines para los 5 sensores de línea
const int SS1_PIN = 2; // Sensor 1 (Izquierda)
const int SS2_PIN = 3; // Sensor 2
const int SS3_PIN = 4; // Sensor 3 (Centro)
const int SS4_PIN = 5; // Sensor 4
const int SS5_PIN = 6; // Sensor 5 (Derecha)

void setup() {
  // Inicializa la comunicación serial para mostrar los valores
  Serial.begin(9600);
  
  // Configura los pines de los sensores como ENTRADAS (INPUT)
  pinMode(SS1_PIN, INPUT);
  pinMode(SS2_PIN, INPUT);
  pinMode(SS3_PIN, INPUT);
  pinMode(SS4_PIN, INPUT);
  pinMode(SS5_PIN, INPUT);
  
  Serial.println("Monitor de Sensores BFD-1000 Iniciado...");
}

void loop() {
  // Lee el estado digital de cada sensor
  int sensor1 = digitalRead(SS1_PIN);
  int sensor2 = digitalRead(SS2_PIN);
  int sensor3 = digitalRead(SS3_PIN);
  int sensor4 = digitalRead(SS4_PIN);
  int sensor5 = digitalRead(SS5_PIN);
  
  // Imprime los estados en el Monitor Serial (ej. 1 1 0 1 1)
  // Nota: La lógica HIGH/LOW depende de la configuración de tu módulo,
  // pero generalmente LOW (0) = detecta la línea negra.
  Serial.print(sensor1);
  Serial.print(" ");
  Serial.print(sensor2);
  Serial.print(" ");
  Serial.print(sensor3);
  Serial.print(" ");
  Serial.print(sensor4);
  Serial.print(" ");
  Serial.println(sensor5);
  
  delay(100); // Pequeña pausa para hacer la lectura legible
}