#include <Servo.h>

// Define los servos
Servo servo_0;
Servo servo_1;
Servo servo_2;

// Variables para almacenar los comandos y ángulos
String comando = ""; // Variable para almacenar el comando recibido
int angulo_0 = 90; // Ángulo inicial para servo_0
int angulo_1 = 90; // Ángulo inicial para servo_1
int angulo_2 = 90; // Ángulo inicial para servo_2

// Configuración inicial
void setup() {
    servo_0.attach(4);
    servo_1.attach(5);
    servo_2.attach(6);
    Serial.begin(9600);

    // Establecer posiciones iniciales
    servo_0.write(angulo_0);
    servo_1.write(angulo_1);
    servo_2.write(angulo_2);
}

// Bucle principal
void loop() {
    // Si hay datos disponibles en el puerto serial, lee y procesa los comandos
    while (Serial.available() > 0) {
        // Lee el siguiente byte disponible
        char caracter = Serial.read();

        // Si el caracter es un dígito, un signo menos (para números negativos) o una coma
        if (isdigit(caracter) || caracter == '-' || caracter == ',') {
            // Agrega el caracter al comando
            comando += caracter;
        } else if (caracter == '\n') { // Si el caracter es un salto de línea
            // Separa el comando en los tres ángulos
            int separador_1 = comando.indexOf(',');
            int separador_2 = comando.indexOf(',', separador_1 + 1);
            int angulo_servo_0 = comando.substring(0, separador_1).toInt(); // Primer valor para servo_0
            int angulo_servo_1 = comando.substring(separador_1 + 1, separador_2).toInt(); // Segundo valor para servo_1
            int angulo_servo_2 = comando.substring(separador_2 + 1).toInt(); // Tercer valor para servo_2

            // Mueve el servo_0 al ángulo especificado
            servo_0.write(angulo_servo_0);
            angulo_0 = angulo_servo_0;

            // Mueve el servo_1 al ángulo especificado
            servo_1.write(angulo_servo_1);
            angulo_1 = angulo_servo_1;

            // Mueve el servo_2 al ángulo especificado
            servo_2.write(angulo_servo_2);
            angulo_2 = angulo_servo_2;

            // Reinicia el comando para el próximo
            comando = "";
        }
    }
}
