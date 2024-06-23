#include <math.h>
#include <DHT.h>

//Temperatura
#define DHTTYPE DHT11
#define DHTPIN 9

DHT dht(DHTPIN,DHTTYPE);

// Definición de pines para los dos sensores
const int TEMP_0 = A0;
const int TEMP_R = A1;

float R2 = 100000;

//Datos obtenidos por la calculadora
//https://www.thinksrs.com/downloads/programs/Therm%20Calc/NTCCalibrator/NTCcalculator.htm
//Valores de resistencias basados en el datasheet:
// 539171 -10°C
// 100000  25°C
// 17253   70°C

float A = 0.7633730310E-3; 
float B = 2.088658820E-4; 
float C = 1.218774455E-7;  

float termistor(int RawADC) {
  long resistencia;  
  float temp;
  resistencia = R2*((1024.0 / RawADC) - 1); //Calculamos R1 mediante la lectura analogica
  temp = log(resistencia);
  temp = 1 / (A + (B * temp) + (C * temp * temp * temp));
  temp = temp - 273.15;  // Kelvin a grados centigrados                     
  return temp;
}

void setup() {
  Serial.begin(9600); // Iniciar la comunicación serial
  dht.begin();
}

void loop() {
  float t_0;
  float t_r;
  float t_inf;
  t_0 = termistor(analogRead(TEMP_0));
  t_r = termistor(analogRead(TEMP_R));
  t_inf = dht.readTemperature();
  // Enviar los datos por el puerto serial separados por comas
  Serial.print(t_inf,3);
  Serial.print(",");
  Serial.print(t_0,3);
  Serial.print(",");
  Serial.println(t_r,3);

  delay(1500); // Esperar 1.5 segundos entre lecturas

    float t_0;
  float t_r;
  float t_inf;
  t_0 = termistor(analogRead(TEMP_0));
  t_r = termistor(analogRead(TEMP_R));
  t_inf = dht.readTemperature();
  // Enviar los datos por el puerto serial separados por comas
  Serial.print(t_inf,3);
  Serial.print(",");
  Serial.print(t_0,3);
  Serial.print(",");
  Serial.println(t_r,3);

  delay(1500); // Esperar 1.5 segundos entre lecturas
  
  float t_0;
  float t_r;
  float t_inf;
  t_0 = termistor(analogRead(TEMP_0));
  t_r = termistor(analogRead(TEMP_R));
  t_inf = dht.readTemperature();
  // Enviar los datos por el puerto serial separados por comas
  Serial.print(t_inf,3);
  Serial.print(",");
  Serial.print(t_0,3);
  Serial.print(",");
  Serial.println(t_r,3);

  delay(1500); // Esperar 1.5 segundos entre lecturas
  delay(299000);
}