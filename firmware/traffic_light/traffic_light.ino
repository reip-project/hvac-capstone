// most launchpads have a red LED
//#define 

/*
  Blink
  The basic Energia example.
  Turns on an LED on for one second, then off for one second, repeatedly.
  Change the LED define to blink other LEDs.
  
  Hardware Required:
  * LaunchPad with an LED
  
  This example code is in the public domain.
*/

// most launchpads have a red LED
//#define 


#define LED_RED PB_5
#define LED_WHITE PB_1
#define LED_YELLOW PB_4
#define GRAND1 PB_2
//String Chart ="";     
int current_state = 0; 
bool start_with_red = false;
// the setup routine runs once when you press reset:
void setup() {                

  //establishContact(); 
  pinMode(LED_RED, OUTPUT); 
  pinMode(LED_WHITE, OUTPUT);  
  pinMode(LED_YELLOW, OUTPUT);   
  pinMode(GRAND1, OUTPUT);
  digitalWrite(GRAND1, LOW);
  Serial.begin(9600); 
  while(Serial.read() >= 0){}
    
}

void breakloop()
 {
  //Chart="";
    if (Serial.available() > 0) 
    {
    char Chart = Serial.read(); 
    if (Chart == 'n')
    {
      current_state = 1;
      }
    }    
  }



void checkCommands()
{
    //Chart="";
    if (Serial.available() > 0) 
    {
    char Chart = Serial.read(); 
    
      if (Chart == 'r')
      {
        
        digitalWrite(LED_YELLOW, HIGH);
        delay(1000);
        digitalWrite(LED_YELLOW, LOW);
        delay(1000);
        digitalWrite(LED_RED, HIGH);
       // while(true)delay(1);
        
       while(current_state==0) {
            
             //digitalWrite(LED_RED, HIGH);
             breakloop();            
             //delay(1);
            }
       start_with_red = false;
         
        
        }
      
      
       else if (Chart == 'g')
      {
        digitalWrite(LED_YELLOW, HIGH);
        delay(1000);
        digitalWrite(LED_YELLOW, LOW);
        delay(1000);
        digitalWrite(LED_WHITE, HIGH);
        while(current_state==0) {
            
             //digitalWrite(LED_WHITE, HIGH);
             breakloop();            
            }
       start_with_red = true;
       
       } 
       
      
     
  }
  current_state = 0;
}

 


// the loop routine runs over and over again forever:
void loop() {
  //if (start_with_red) {
  digitalWrite(start_with_red ? LED_RED : LED_WHITE, HIGH);
  checkCommands();
  delay(1000); 
  checkCommands();// wait for a second
  digitalWrite(start_with_red ? LED_RED : LED_WHITE, LOW);    // turn the LED off by making the voltage LOW
  checkCommands();
  delay(1000);               // wait for a second
  digitalWrite(LED_YELLOW, HIGH);   // turn the LED on (HIGH is the voltage level)
  checkCommands();
  delay(1000); 
  checkCommands();// wait for a second
  digitalWrite(LED_YELLOW, LOW);    // turn the LED off by making the voltage LOW
  checkCommands();
  delay(1000);               // wait for a second
  checkCommands();
  digitalWrite(start_with_red ? LED_WHITE : LED_RED, HIGH);   // turn the LED on (HIGH is the voltage level)
  checkCommands();
  delay(1000);               // wait for a second
  checkCommands();
  digitalWrite(start_with_red ? LED_WHITE : LED_RED,LOW );    // turn the LED off by making the voltage LOW
  checkCommands();
  delay(1000);
  checkCommands();// wait for a second
  //}
  
//  else
//  {
//  digitalWrite(LED_WHITE, HIGH);   // turn the LED on (HIGH is the voltage level)
//  checkCommands();
//  delay(1000);               // wait for a second
//  checkCommands();
//  digitalWrite(LED_WHITE,LOW );    // turn the LED off by making the voltage LOW
//  checkCommands();
//  delay(1000);
//  digitalWrite(LED_RED, HIGH);
//  checkCommands();
//  delay(1000); 
//  checkCommands();// wait for a second
//  digitalWrite(LED_RED, LOW);    // turn the LED off by making the voltage LOW
//  checkCommands();
//  delay(1000);               // wait for a second
//  digitalWrite(LED_YELLOW, HIGH);   // turn the LED on (HIGH is the voltage level)
//  checkCommands();
//  delay(1000); 
//  checkCommands();// wait for a second
//  digitalWrite(LED_YELLOW, LOW);    // turn the LED off by making the voltage LOW
//  checkCommands();
//  delay(1000);               // wait for a second
//  checkCommands();
//  
//  }
  }
  
