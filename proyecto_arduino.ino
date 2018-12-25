#define LED 13
#include <Servo.h>

int mssg = 0; //variable para guardar el mensaje
Servo myservo; 
int pos = 0;

void setup()
{
   pinMode(LED, OUTPUT); //establecemos 13 como salida
   Serial.begin(9600); //iniciando Serial
   myservo.attach(9);
}
 
void loop()
{
   if (Serial.available())
   {
      char mssg = Serial.read(); //leemos el serial
 
      if(mssg == 'r')
      {
        //Rojo
         //digitalWrite(13, HIGH); //si entra una 'e' encendemos
         myservo.write(107);  
      }
       else if(mssg == 'b')
      {
        //Azul
         //digitalWrite(13, HIGH); //si entra una 'a' apagamos
         myservo.write(70);  
      }
       else if(mssg == 'y')
      {
         //digitalWrite(13, HIGH); //si entra una 'a' apagamos
         //Amarillo
         myservo.write(130);  
      }
      else if(mssg == 'a')
      {
         digitalWrite(13, LOW); //si entra una 'a' apagamos
      }
       
   }
}
