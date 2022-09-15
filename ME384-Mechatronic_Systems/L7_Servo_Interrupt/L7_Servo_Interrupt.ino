// INTO interrupt enabled, with a button on INT0 (PD2) and on INT1 (PD3)
// PCINT21 (PD5) is enabled 
// Servo input on PB0, buttons on PD2, PD3 and PB4

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

#define turnon(inbyte, loct) inbyte |=(1<<loct)
#define turnoff(inbyte, loct) inbyte &= ~(1<<loct)
int r_direction = 1;
int interruption = 0;

void rotate_servo(int angle);
void rotate_servo(int angle)
{
  int t_count = angle*1.15; //how many microseconds to count
  
                for(int i=0;i<20;i++)  //send the position information twenty times
                {
                  if (interruption == 1) {  // to check for interruption
                     break;
 
                      }
                      
                  turnon(PORTB,PB0);
                  _delay_ms(0.5);
                  for(int j=0;j<t_count ; j++)
                      {
                        _delay_us(9);
                        
                      }
                  turnoff(PORTB,PB0);
                  _delay_ms(18.5);
                }
}

ISR (INT0_vect){  // PD2 => INT0 => when interrupt is triggered, jump here

  {
      if (bit_is_clear(PIND,PD2)) {  // to prevent occasional debouncing
               rotate_servo(45);
               _delay_ms(2000);
               interruption = 1;
 
      }
  }
}

ISR (INT1_vect){  // PD3 => INT1 => when interrupt is triggered, jump here

  {
      if (bit_is_clear(PIND,PD3)) {  // to prevent occasional debouncing
               rotate_servo(90);
               _delay_ms(2000);
               interruption = 1;
               
      }
  }
}

ISR (PCINT0_vect){  // any enabled PCINT0 pin can trigger here (0 to 7)
   
  if (bit_is_clear(PINB,PB4)) {  // specifically checking for PB4
               rotate_servo(135);
               _delay_ms(2000);
               interruption = 1;
               
  }
}

void initInterrupt0(void)
{
  EIMSK |= (1<<INT0);  // enable INT0 - which is PD2
  EIMSK |= (1<<INT1);  // enable INT1 - which is PD3
  EICRA |= (1<< ISC01); // makes (1 0) so triggers on the falling edge
  turnoff(EICRA, ISC00);

  // EICRA should have been modified for INT1 interrupt too! (controlled by ISC11, ISC10)

  // configure Pin Change Interrupt to use PICINT4 a.k.a. PB4
  PCICR |= (1<<PCIE0);
  PCMSK0 |= (1<<PCINT4);
  sei(); // Set enable interrupt, global stitch for interrupts
}


int main (void)
{
  DDRB=0b00000001;
  DDRD=0;
  PORTD=0b11111111; // all PORTD pull up resistors are enabled 
  PORTB=0b00010000;
  initInterrupt0();


  while(1){
         if (r_direction)  {
          r_direction = 0;
          rotate_servo(180);
           _delay_ms(1000); 
          interruption = 0;   
          }
          else {
          r_direction = 1;
          rotate_servo(0);
           _delay_ms(1000);
          interruption = 0;
           }

             
  } // infinite loop
  return 0;
}
