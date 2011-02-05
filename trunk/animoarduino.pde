/*

  RGB_LED_Color_Fade_Cycle.pde
  
  Cycles through the colors of a RGB LED

  Written for SparkFun Arduino Inventor's Kit CIRC-RGB
  Modified by Daniel Guerrero to talk with La Fonera
  via serial connection

*/

// LED leads connected to PWM pins
const int RED_LED_PIN = 9;
const int GREEN_LED_PIN = 10;
const int BLUE_LED_PIN = 11;

// Used to store the current intensity level of the individual LEDs
int redIntensity = 0;
int greenIntensity = 0;
int blueIntensity = 0;

// Length of time we spend showing each color
const int DISPLAY_TIME = 1000; // In milliseconds

void setup() {
  // set the data rate for the SoftwareSerial port
  Serial.begin(9600);
  delay(1000);
  //Serial.println("Tell me the color: ");
}

void loop() {

  //We read one byte that indicates the color to set R,G,B..  
  if (Serial.available() > 0) {
      byte p = Serial.read();
      //Red, Anger      
      if(p == '3'){
        redIntensity = 255;
        greenIntensity = 0;
        blueIntensity = 0;
        analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //Green, Envy
      else if(p == '4'){
        redIntensity = 0;
        greenIntensity = 255;
        blueIntensity = 0;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //Blue, Sadness
      else if(p == '2'){
        redIntensity = 0;
        greenIntensity = 0;
        blueIntensity = 255;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //Pink, Love
      else if(p == '0'){
        redIntensity = 255;
        greenIntensity = 128;
        blueIntensity = 128;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //Yellow, Happy
      else if(p == '1'){
        redIntensity = 255;
        greenIntensity = 255;
        blueIntensity = 0;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //Orange, Surprise
      else if(p == '5'){
        redIntensity = 255;
        greenIntensity = 96;
        blueIntensity = 0;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
      //White, Fear  
      else if(p == '6'){
        redIntensity = 255;
        greenIntensity = 255;
        blueIntensity = 255;
	analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);}
   }

  // delay 10 milliseconds before the next reading:
  delay(10);

/*  // Cycle color from green through to blue
  // (In this loop we move from 100% green, 0% blue to 0% green, 100% blue)  
  for (blueIntensity = 0; blueIntensity <= 255; blueIntensity+=5) {
        greenIntensity = 255-blueIntensity;
        analogWrite(BLUE_LED_PIN, blueIntensity);
        analogWrite(GREEN_LED_PIN, greenIntensity);
        delay(DISPLAY_TIME);
  }

  // Cycle cycle from blue through to red
  // (In this loop we move from 100% blue, 0% red to 0% blue, 100% red)    
  for (redIntensity = 0; redIntensity <= 255; redIntensity+=5) {
        blueIntensity = 255-redIntensity;
        analogWrite(RED_LED_PIN, redIntensity);
        analogWrite(BLUE_LED_PIN, blueIntensity);
        delay(DISPLAY_TIME);
  } */
}


