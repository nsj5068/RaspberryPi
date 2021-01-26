/*************************************************** 
  This is a library example for the MLX90614 Temp Sensor

  Designed specifically to work with the MLX90614 sensors in the
  adafruit shop
  ----> https://www.adafruit.com/products/1748
  ----> https://www.adafruit.com/products/1749

  These sensors use I2C to communicate, 2 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_MLX90614.h>
#define IR1 0x5A
#define IR2 0x5C
#define IR3 0x5B
Adafruit_MLX90614 mlx;

void setup() {
  Serial.begin(9600);
  

  Serial.println("Adafruit MLX90614 test");  

  mlx.begin(); 
  
  
}

void loop() {
  //readAmbientTempF : 공기 중 온도(화씨, F) , readAmbientTempC : 공기 중 온도(섭씨, C)
  //readObjectTempF : 물체의 표면 온도(화씨, F), readObjectTempC : 물체의 표면 온도(섭씨, C)
  
  mlx.AddrSet(IR1); 
  Serial.print("IR1: ");
  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC()); 
  Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");
  mlx.temp1 = mlx.readObjectTempF();
  delay(250);
  mlx.AddrSet(IR2); 
  Serial.print("IR2: ");
  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC()); 
  Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");
  mlx.temp2 = mlx.readObjectTempF();
  delay(250);
  mlx.AddrSet(IR3); 
  Serial.print("IR3: ");
  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC()); 
  Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");
  mlx.temp3 = mlx.readObjectTempF();
  delay(250);
  Serial.print("\n***********F Average Temp:"); Serial.print(mlx.avgF=(mlx.temp1+mlx.temp2+mlx.temp3)/3); 
  Serial.print("***********\n");
  Serial.println();
  delay(5000);
}
