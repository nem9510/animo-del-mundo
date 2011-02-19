/*
  Author: Daniel Guerrero
  Colors structure by http://www.instructables.com/member/RandomMatrix/
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

// Initialize the variable that memorize the actual color
// for later fading it.
int last_color = 0;

// LED leads connected to PWM pins
const int RED_LED_PIN = 9;
const int GREEN_LED_PIN = 10;
const int BLUE_LED_PIN = 11;

// Used to store the current intensity level of the individual LEDs
int redIntensity = 0;
int greenIntensity = 0;
int blueIntensity = 0;

// Length of time we spend showing each color
const int DISPLAY_TIME = 10; // In milliseconds

void setup() {
  // set the data rate for the SoftwareSerial port
  Serial.begin(9600);
  delay(1000);
  analogWrite(RED_LED_PIN, Colors[last_color].r);
  analogWrite(GREEN_LED_PIN, Colors[last_color].g);
  analogWrite(BLUE_LED_PIN, Colors[last_color].b);
  //Serial.println("Tell me the color: ");
}

void flash(int lastcolorID) {
  Serial.println("last color was: ");
  Serial.println(lastcolorID);
  for (int numflashes = 5; numflashes >= 0; numflashes-=1){
    analogWrite(RED_LED_PIN,0);
    analogWrite(GREEN_LED_PIN,0);
    analogWrite(BLUE_LED_PIN,0);
    delay(1000);
    analogWrite(RED_LED_PIN,Colors[lastcolorID].r);
    analogWrite(GREEN_LED_PIN,Colors[lastcolorID].g);
    analogWrite(BLUE_LED_PIN,Colors[lastcolorID].b);
    delay(1000);
  }
}
  
void setcolor_withfade(int newcolorID, int lastcolorID) {
  Serial.println("new color will be: ");
  Serial.println(newcolorID);
    Serial.println("last color was: ");
  Serial.println(lastcolorID);
        if (Colors[newcolorID].r == Colors[lastcolorID].r){
          redIntensity = Colors[lastcolorID].r;
          Serial.println("Maintaining R channel");
          Serial.println(redIntensity);
          analogWrite(RED_LED_PIN, redIntensity);
          delay(DISPLAY_TIME);
        }
        else if (Colors[newcolorID].r > Colors[lastcolorID].r){
          for (redIntensity = Colors[lastcolorID].r; redIntensity <= Colors[newcolorID].r ; redIntensity+=1) {
                  Serial.println("changing R channel");
                  Serial.println(redIntensity);
                  analogWrite(RED_LED_PIN, redIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        else if (Colors[newcolorID].r < Colors[lastcolorID].r){
          for (redIntensity = Colors[lastcolorID].r; redIntensity >= Colors[newcolorID].r ; redIntensity-=1) {
                  Serial.println("changing R channel");
                  Serial.println(redIntensity);
                  analogWrite(RED_LED_PIN, redIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        if (Colors[newcolorID].g == Colors[lastcolorID].g){
          greenIntensity = Colors[lastcolorID].g;
          Serial.println("Maintaining G channel");
          Serial.println(greenIntensity);
          analogWrite(GREEN_LED_PIN, greenIntensity);
          delay(DISPLAY_TIME);
        }
        else if (Colors[newcolorID].g > Colors[lastcolorID].g){
          for (greenIntensity = Colors[lastcolorID].g; greenIntensity <= Colors[newcolorID].g ; greenIntensity+=1) {
                  Serial.println(greenIntensity);
                  Serial.println("changing G channel");
                  analogWrite(GREEN_LED_PIN, greenIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        else if (Colors[newcolorID].g < Colors[lastcolorID].g){
          for (greenIntensity = Colors[lastcolorID].g; greenIntensity >= Colors[newcolorID].g ; greenIntensity-=1) {
                  Serial.println("changing G channel");
                  Serial.println(greenIntensity);
                  analogWrite(GREEN_LED_PIN, greenIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        if (Colors[newcolorID].b == Colors[lastcolorID].b){
          blueIntensity = Colors[lastcolorID].b;
          Serial.println("Maintaining B channel");
          Serial.println(blueIntensity);
          analogWrite(BLUE_LED_PIN, blueIntensity);
          delay(DISPLAY_TIME);
        }
        else if (Colors[newcolorID].b > Colors[lastcolorID].b){
          for (blueIntensity = Colors[lastcolorID].b; blueIntensity <= Colors[newcolorID].b ; blueIntensity+=1) {
                  Serial.println("changing B channel");
                  Serial.println(blueIntensity);
                  analogWrite(BLUE_LED_PIN, blueIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        else if (Colors[newcolorID].b < Colors[lastcolorID].b){
          for (blueIntensity = Colors[lastcolorID].b; blueIntensity >= Colors[newcolorID].b ; blueIntensity-=1) {
                  Serial.println("changing B channel");
                  Serial.println(blueIntensity);
                  analogWrite(BLUE_LED_PIN, blueIntensity);
                  delay(DISPLAY_TIME);
                }
        }
        last_color = newcolorID;
}

void loop() {
  COLORID colorID;
  //We read one byte that indicates the color to set R,G,B..
  if (Serial.available() > 0) {
      byte p = Serial.read();
      //normalize value to work with it
      int q = int(p)-48;
      if(q >= 0 && q <= 7){
            Serial.println ("Trying to setup color: ");
            Serial.println (q);
	    setcolor_withfade(q,last_color);}
      else if (q = 9){
            Serial.println (q);
            Serial.println ("Lets flash");
            flash(last_color);}
      else {
	    Serial.println ("byte received outside scope");
	  }
   }

  // delay 10 milliseconds before the next reading:
  delay(10);
}
