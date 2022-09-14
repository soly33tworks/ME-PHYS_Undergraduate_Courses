// counts the number of button D1 presses (counter)
// until Button D2 pressed, then 
// LED on B0 is blinkes (counter) many times 

#include <avr/io.h>
#include <util/delay.h>

#define biryap(inbyte, loct) inbyte |= (1<<loct)
#define bit_is_clear(inbyte, loct) !(inbyte & (1<<loct)) 

void blink_please (int x)  ; 
void blink_please (int x)  // function body
{
   for (int i=0;i<x;i++) {
          PORTB =0b00000001;
          _delay_ms(500);
          PORTB =0b00000000;
          _delay_ms(500);
   }
       
}

int main (void)
{
  DDRB=0b00000001;
  DDRD=0;
  int counter =0 ;
  
  biryap(PORTD, PD2); // internal pull-up, not needed if external pull up is used 
  biryap(PORTD, PD4); // PD2 = 0b00000100, PD4 = 0b00010000
  biryap(PORTD, PD6); // PD6 = 0b01000000
   
  while(1){

    if(bit_is_clear(PIND,PD6)){  //red 
      counter++;
      _delay_ms(500);  // prevents the loop running infinite times (prevents high counter #, 1 press -> +1 count)
    }

    if(bit_is_clear(PIND,PD4)){  //blue 
      counter--;
      _delay_ms(500);  // prevents the loop running infinite times (prevents high counter #, 1 press -> +1 count)
    }
 
    if (bit_is_clear(PIND,PD2)) {  //yellow button
      blink_please(counter);
      counter=0;
    }
    
  }

  return 0;
}
