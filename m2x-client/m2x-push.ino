#include "M2XStreamClient.h"

char deviceId[] = "d0007c1c2bf6b47b2b2ecb4e253eea29";      // Device you want to post to
char streamName[] = "temp";  // Stream you want to post to
char m2xKey[] = "a3a2829a4dac4a9f6caa14491dab16bf";

const int temperaturePin = 0;
TCPClient client;
M2XStreamClient m2xClient(&client, m2xKey);

float getVoltage(int pin) {
  return (analogRead(temperaturePin) * 3.3) / 4095;
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}


void setup() {
  pinMode(temperaturePin, INPUT);

  Serial.begin(9600);

  while (!WiFi.ready()) {
    Serial.println("Waiting for WIFI connection...");
    // wait 2 seconds for connection
    delay(10000);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();
}

void loop() {
  float voltage, degreesC, degreesF;

  voltage = getVoltage(temperaturePin);
  degreesC = (voltage - 0.5) * 100.0;
  degreesF = degreesC * (9.0/5.0) + 32.0;

  Serial.print("voltage: ");
  Serial.print(voltage);
  Serial.print("  deg C: ");
  Serial.print(degreesC);
  Serial.print("  deg F: ");
  Serial.println(degreesF);

  int response = m2xClient.updateStreamValue(deviceId, streamName, degreesC);
  Serial.print("M2x client response code: ");
  Serial.println(response);

  if (response == -1) while(1) ;

  delay(5000);
}

