// Stepper Motor Speed and Direction Control
// Using MX1508 (H-Bridge)
// Motor: Microstepper (Bipolar)
// Serial Monitor: 9600 baud (Arduino's serial library)
// By: Ege Erdem

// NOTE: Since this is a bipolar step motor, H-Bridge 
//         is used because "it allows the polarity of the 
//         power applied to be controlled independently"     

// Connections
// A+ Black -> Out 1
// A- Brown -> Out 2
// B- Red -> Out 3
// B+ Orange -> Out 4
// IR Control signal -> PB5

// Motor 1
// PB4 -> In 1
// PB3 -> In 2
// PB2 -> In 3
// PB1 -> In 4

// Motor 2
// PC3 -> In 1
// PC2 -> In 2
// PC1 -> In 3
// PC0 -> In 4

// Motor 3
// PD4 -> In 1
// PD3 -> In 2
// PD2 -> In 3
// PC5 -> In 4

// Motor 4
// PB0 -> In 1
// PD7 -> In 2
// PD6 -> In 3
// PD5 -> In 4

#include <avr/io.h>
#include <util/delay.h>
#include <IRremote.h>

// Mapping of IR Remote (bottom version), Contact me for the top version
#define R_OK 0xFF38C7  // OK
#define R_RIGHT 0xFF5AA5  // →
#define R_UP 0xFF18E7  // ↑
#define R_LEFT 0xFF10EF  // ←
#define R_DOWN 0xFF4AB5  // ↓
#define R_1 0xFFA25D  // 1
#define R_2 0xFF629D  // 2
#define R_3 0xFFE21D  // 3
#define R_4 0xFF22DD  // 4
#define R_5 0xFF02FD  // 5
#define R_6 0xFFC23D  // 6
#define R_7 0xFFE01F  // 7
#define R_8 0xFFA857  // 8
#define R_9 0xFF906F  // 9
#define R_0 0xFF9867  // 0
#define R_STAR 0xFF6897  // *
#define R_HASH 0xFFB04F  // #

// Global Variables
int direc=0; //Binary variable, direction of rotation in continuous mode (CW:0 CCW:1)
int spd=30; //Speed of the motor when continuous rotation, 1-30
int input_mode = 1;  //Type of the input entered by the user (step:1, disp:2, speed:3, zero:4, coil mode:5) Also strain/total_disp/force can be added
String input = "";  //Numerical input entered by the user with IR control
int steps = 0;  //Number of steps to be executed
int st_pos = 0;  //Current step position
float disp = 0; //Current displacement position of a microstepper
bool coil = 1; //Holding energization of the coils (energized:0, not energized:1)
unsigned long key_value = 0;  //IR control pressed button

// Pins (see ATmega328 layout)
int RECV_PIN = 13; //Pin of the IR control receiver PB5

// Physical constants of the buckling setup (unused)
float E = 1.6; // Young's Modulus of the PDMS specimen (in MPA)
float L = 10; // Thickness of the PDMS specimen (in mm)
float A = 6.0; // Area of the PDMS where force is applied (10mm x 600µm, in mm^2)
float k = (2*A*E*1000)/L;  // Spring constant = 2AE/L ≈ 1920 N/m

// Functions

void init_step (void)  ; 
void init_step (void)  // Initializes the stepper and connected ports
{
  DDRB |= 0b00011111;  // PORTB <0-4> Output
  DDRC |= 0b00101111;  // PORTC <0-3, 5> Output
  DDRD |= 0b11111100;  // PORTD <2-7> Output
  PORTB = 0;        // Initialize ports as zero to avoid floating values
  PORTC = 0;
  PORTD = 0;

  PORTB |= 0b00001100;  // State 1
  PORTC |= 0b00000110;
  PORTD |= 0b11001100;
}

int step_forward (int state_motor)  ; 
int step_forward (int state_motor) // Gets the current state, gives the command for next state, returns next state number
{
  if (state_motor==1)
        {PORTB |= 0b00001010; PORTC |= 0b00100101; PORTD |= 0b10101000;
        PORTB &= 0b11101010; PORTC &= 0b11110101; PORTD &= 0b10101011; return 2;}
  else if (state_motor==2)
        {PORTB |= 0b00010011; PORTC |= 0b00101001; PORTD |= 0b00110000;
        PORTB &= 0b11110011; PORTC &= 0b11111001; PORTD &= 0b00110011; return 3;}
  else if (state_motor==3)
        {PORTB |= 0b00010101; PORTC |= 0b00001010; PORTD |= 0b01010100;
        PORTB &= 0b11110101; PORTC &= 0b11011010; PORTD &= 0b01010111; return 4;}
  else if (state_motor==4)
        {PORTB |= 0b00001100; PORTC |= 0b00000110; PORTD |= 0b11001100;
        PORTB &= 0b11101100; PORTC &= 0b11010110; PORTD &= 0b11001111; return 1;}
}

int step_backward (int state_motor)  ; 
int step_backward (int state_motor) // Gets the current state, gives the command for previous state, returns previous state number
{
  if (state_motor==1)
        {PORTB |= 0b00010101; PORTC |= 0b00001010; PORTD |= 0b01010100;
        PORTB &= 0b11110101; PORTC &= 0b11011010; PORTD &= 0b01010111; return 4;}
  else if (state_motor==2)
        {PORTB |= 0b00001100; PORTC |= 0b00000110; PORTD |= 0b11001100;
        PORTB &= 0b11101100; PORTC &= 0b11010110; PORTD &= 0b11001111; return 1;}
  else if (state_motor==3)
        {PORTB |= 0b00001010; PORTC |= 0b00100101; PORTD |= 0b10101000;
        PORTB &= 0b11101010; PORTC &= 0b11110101; PORTD &= 0b10101011; return 2;}
  else if (state_motor==4)
        {PORTB |= 0b00010011; PORTC |= 0b00101001; PORTD |= 0b00110000;
        PORTB &= 0b11110011; PORTC &= 0b11111001; PORTD &= 0b00110011; return 3;}
}

int update_rate (void)  ; 
int update_rate (void) // Waits based on the chosen speed,  spd: 1-30
{
  for (int j=0;j<31-spd;j++)
       {_delay_ms(1);}
}

// Main loop 
 
int main (void)
{ 
  init_step();
  Serial.begin(9600);  // Initializes the serial
  IRrecv irrecv(RECV_PIN);
  decode_results IR_signal;
  irrecv.enableIRIn();
  int state=1; // Integer between 1,2,3,4
               // Describes the current configuration of the step motor
  
  while(1){
          if (irrecv.decode(&IR_signal)) {
            if (IR_signal.value == 0xFFFFFFFF & (key_value == R_UP || key_value == R_DOWN)) {//0xFFFFFFFF means cont. button pressing
                IR_signal.value = key_value; // set the value to the key value
                 }
            key_value = IR_signal.value; // store the value as key_value
               
            if (IR_signal.value == R_OK) { //(step:1, disp:2, speed:3, zero:4)
              
                if (input_mode==1) {
                   Serial.println("Step received, travelling...");
                   if (direc==0) {
                      for(int i=0;i<input.toInt();i++)
                         {update_rate(); state = step_forward(state); st_pos = st_pos + 1;}
                      disp = disp + input.toInt()*8.729050279;   // 12500 µm range / 1432 steps
                      }   
                   else if (direc==1) {
                      for(int i=0;i<input.toInt();i++)
                         {update_rate(); state = step_backward(state); st_pos = st_pos - 1;}
                      disp = disp - input.toInt()*8.729050279;   // 12500 µm / 1432 steps
                      } 
                   if (coil) {PORTB &= 0b11100000; PORTC &= 0b11010000; PORTD &= 0b00000011;}    
                   Serial.print("Executed: ");
                   Serial.print(input.toInt());
                   Serial.println(" many steps.");
                   Serial.print("Current step position: ");
                   if (st_pos<0) {Serial.print("-");}
                   Serial.println(abs(st_pos));
                   }
                      
                else if (input_mode==2) {
                   Serial.println("Displacement received, travelling...");
                   steps = round(abs(input.toInt() - disp)/8.729050279); // 12500 µm / 1432 steps
                   if (input.toInt() > disp) {                              
                      for(int i=0;i<steps;i++)   //If forwards                                   
                         {update_rate(); state = step_forward(state); st_pos = st_pos + 1;}
                      disp = disp + steps*8.729050279;   // 12500 µm / 1432 steps
                      }   
                   else if (input.toInt() < disp) {
                      for(int i=0;i<steps;i++)
                         {update_rate(); state = step_backward(state); st_pos = st_pos - 1;}
                      disp = disp - steps*8.729050279;   // 12500 µm / 1432 steps
                      }   
                   if (coil) {PORTB &= 0b11100000; PORTC &= 0b11010000; PORTD &= 0b00000011;}
                   Serial.print("Moved to: ");
                   if (disp<0) {Serial.print("-");}
                   Serial.print(abs(round(disp))); 
                   Serial.println(" µm");
                   }
                else if (input_mode==3 & input.toInt()>0 & input.toInt()<31) {
                   spd = input.toInt();
                   Serial.print("Speed of the motor is set to: ");
                   Serial.println(spd);
                   }
                else if (input_mode==4) {
                   Serial.println("The current position is set as zero.");
                   st_pos = 0;
                   disp = 0;
                   }
                else if (input_mode==5) {
                   Serial.print("The coils are "); // Results will apply after stepping
                   if (coil == 0) {
                       Serial.println("de-energized ");
                       coil = 1;
                       PORTB &= 0b11100000; PORTC &= 0b11010000; PORTD &= 0b00000011;
                       }
                   else if (coil == 1) {
                       Serial.println("energized ");
                       coil = 0;
                       }
                   }                  
                input = "";
                 }
                  
             if (IR_signal.value == R_RIGHT) {
                 direc = 0;
                 Serial.println("Direction: Forward ");
                }
             if (IR_signal.value == R_UP) {
                for(int i=0;i<32;i++)
                   {update_rate(); state = step_forward(state); st_pos = st_pos + 1;}
                if (coil) {PORTB &= 0b11100000; PORTC &= 0b11010000; PORTD &= 0b00000011;}
                } 
             if (IR_signal.value == R_LEFT) {
                 direc = 1;
                 Serial.println("Direction: Backwards ");
                }   
             if (IR_signal.value == R_DOWN) {
                 for(int i=0;i<32;i++)
                    {update_rate(); state = step_backward(state); st_pos = st_pos - 1;}
                 if (coil) {PORTB &= 0b11100000; PORTC &= 0b11010000; PORTD &= 0b00000011;}
                }
             if (IR_signal.value == R_1) {
                 input = input + "1";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_2) {
                 input = input + "2";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_3) {
                 input = input + "3";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_4) {
                 input = input + "4";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_5) {
                 input = input + "5";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_6) {
                 input = input + "6";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_7) {
                 input = input + "7";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_8) {
                 input = input + "8";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_9) {
                 input = input + "9";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_STAR & input.length()>0) {
                 input.remove(input.length()-1);
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_0) {
                 input = input + "0";
                 Serial.print("Entered value: ");
                 Serial.println(input.toInt());
                }
             if (IR_signal.value == R_HASH) {
                if (input_mode==1) {
                   input_mode = 2;
                   Serial.println("\r\n Input type: Displacement (µm)");
                   }   
                else if (input_mode==2) {
                   input_mode = 3;
                   Serial.println("\r\n Input type: Speed (1-30)");
                   }
                else if (input_mode==3) { // Also need to add a zeroing algorithm (step pack 1432 etc.)
                   input_mode = 4;
                   Serial.println("\r\n Input type: Zeroing");
                   Serial.println("Press OK to take the current position as zero");
                   }
                else if (input_mode==4) {
                   input_mode = 5;
                   Serial.println("\r\n Input type: Coil Power");
                   Serial.println("Press OK to turn on/off holding current");
                   }                   
                else if (input_mode==5) {
                   input_mode = 1;
                   Serial.println("\r\n Input type: Step (from current position)");
                   }
                   
                 Serial.print("Motor speed: ");
                 Serial.println(spd);
                 Serial.print("Direction (FWD:0 BWD:1): ");
                 Serial.println(direc);                 
                 Serial.print("Step position: ");
                 if (st_pos<0) {Serial.print("-");}
                 Serial.print(abs(st_pos));
                 Serial.println(" step");
                 Serial.print("Displacement position: ");
                 if (disp<0) {Serial.print("-");}
                 Serial.print(abs(round(disp)));
                 Serial.println(" µm");            
                 input = "";
                }
                
             irrecv.resume();
         }      
  }
  return 0;
}
