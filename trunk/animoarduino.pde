/*

  Colors structure by http://www.instructables.com/member/RandomMatrix/
  Modified by Daniel Guerrero.

*/
enum COLORID {
  PINK = 0,
  YELLOW,
  ORANGE,
  RED,
  GREEN,
  BLUE,
  WHITE,
  NUM_COLORS,
};

// simple colour structure
typedef struct
{
  int r;
  int g;
  int b;
} Color;
  
// default colours
const Color Colors[] = {
  (Color){255, 128, 128}, // pink
  (Color){255, 255, 0},   // yellow
  (Color){255, 96, 0},    // orange
  (Color){255, 0,   0},   // red
  (Color){0,   255, 0},   // green
  (Color){0,   0,   255}, // blue
  (Color){255, 255, 255}, // white
};


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

void setcolor(colorID) {
	analogWrite(RED_LED_PIN, Colors[colorID].r);
	analogWrite(GREEN_LED_PIN, Colors[colorID].g);
	analogWrite(BLUE_LED_PIN, Colors[colorID].b);}
}

void loop() {

  //We read one byte that indicates the color to set R,G,B..  
  if (Serial.available() > 0) {
      byte p = Serial.read();
      //Red, Anger      
      if(p >= '0' && p <= NUMCOLORS){
		setcolor(p);
	  else
	    println 'byte received outside scope';
	  }
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


