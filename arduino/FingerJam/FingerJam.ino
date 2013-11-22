/* FingerJam

  This code allows you to send any of the RN-42 commands to the
  Bluetooth Mate via the Arduino Serial monitor. Characters sent
  over USB-Serial to the Arduino are relayed to the Mate, and
  vice-versa.
  
  Here are the connections necessary:
  Bluetooth Mate-----------------Arduino
      CTS-I    (not connected)
      VCC------------------------5V or 3.3V
      GND--------------------------GND
      TX-O-------------------------D2
      RX-I-------------------------D3
      RTS-O    (not connected)
  
  How to use:
  You can use the serial monitor to send any commands listed in
  the RN-42 Advanced User Manual
  (http://www.sparkfun.com/datasheets/Wireless/Bluetooth/rn-bluetooth-um.pdf)
  to the Bluetooth Mate.
  
  Open up the serial monitor to 9600bps, and make sure the 
  pull-down menu next to the baud rate selection is initially set
  to "No line ending". Now enter the configuration command $$$ in 
  the serial monitor and click Send. The Bluetooth mate should
  respond with "CMD".
  
  The RN-42 module expects a newline character after every command.
  So, once you're in command mode, change the "No line ending"
  drop down selection to "Newline". To test, send a simple command.
  For instance, try looking for other bluetooth devices by sending
  the I command. Type I and click Send. The Bluetooth Mate should
  respond with "Inquiry, COD", follwed by any bluetooth devices
  it may have found.
  
  To exit command mode, either connect to another device, or send
  ---.
  
  The newline and no line ending selections are very important! If
  you don't get any response, make sure you've set that menu correctly.
*/

// We'll use the newsoftserial library to communicate with the Mate
#include <SoftwareSerial.h>  


int bluetoothTx = 3;  // TX-O pin of bluetooth mate
int bluetoothRx = 2;  // RX-I pin of bluetooth mate
int fsrAnalogPin1 = 0;
int fsrAnalogPin2 = 1;
int fsrAnalogPin3 = 2;
int fsrAnalogPin4 = 3;
int fsrAnalogPin5 = 4;
int reading1,reading2,reading3,reading4,reading5;

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup()
{
  Serial.begin(9600);
  bluetooth.begin(9600);  // Start bluetooth serial at 9600
  bluetooth.print("$$$");
}

void loop()
{
  reading1 = map(analogRead(fsrAnalogPin1), 0, 1023, 0, 127);
  reading2 = map(analogRead(fsrAnalogPin2), 0, 1023, 0, 127);
  reading3 = map(analogRead(fsrAnalogPin3), 0, 1023, 0, 127);
  reading4 = map(analogRead(fsrAnalogPin4), 0, 1023, 0, 127);
  reading5 = map(analogRead(fsrAnalogPin5), 0, 1023, 0, 127);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  bluetooth.print((char)30);
  bluetooth.print((char)reading1);
  bluetooth.print((char)35);
  bluetooth.print((char)reading2);
  bluetooth.print((char)40);
  bluetooth.print((char)reading3);
  bluetooth.print((char)45);
  bluetooth.print((char)reading4);
  bluetooth.print((char)48);
  bluetooth.print((char)reading5);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  bluetooth.print((char)50);
  delay(100);
  // and loop forever and ever!
}
