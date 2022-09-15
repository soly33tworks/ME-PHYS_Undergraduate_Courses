// DC Motor Speed and Direction Control
// Using L293D H Bridge

#include <avr/io.h>
#include <util/delay.h>
#define biryap(inbyte, loct) inbyte |=(1<<loct)
#define sifiryap(inbyte, loct) inbyte &= ~(1<<loct)

int N=40;
int M1 = PB0; // Motor pins 1 and 2
int M2 = PB2; 
void PWM_HBridge_port (int x, bool mode, int port1, int port2)  ; 
void PWM_HBridge_port (int x, bool mode, int port1, int port2)  // function body
{
    if (mode){
                  sifiryap(PORTB,port2);
                  for (int j=0;j<10;j++) {
                                       biryap(PORTB,port1);
                                       for(int i=0;i<x;i++)
                                       _delay_ms(1);
                                        
                                       sifiryap(PORTB,port1);
                                       for(int i=0;i<N-x;i++)
                                       _delay_ms(1);
                                       }
    }
    else { //port1 already ground
                    sifiryap(PORTB,port1);
                    for (int j=0;j<10;j++) {
                                        biryap(PORTB,port2);
                                        for(int i=0;i<x;i++)
                                        _delay_ms(1);
                                        
                                        sifiryap(PORTB,port2);
                                        for(int i=0;i<N-x;i++)
                                        _delay_ms(1);
                                         }
    }
}
int main (void)
{
  DDRB=0b00000000;
  biryap(DDRB,M1); // B0 and B2 will be used 
  biryap(DDRB,M2);
  DDRD=0;
  bool dir=0; // direction 0 FWD, 1 BWD
  int counter =20 ; //PWM speed 
  PORTD |= (1<<PD2);  // internal pull-up 
                      // not needed if external pull up is used                          
  PORTD |= (1<<PD4); 
  PORTD |= (1<<PD6); 
  PORTB = 0; // both B1 and B4 are 0 initially
  while(1){

    if(bit_is_clear(PIND,PD6) & counter<40)  //speed up 
      {counter++;}
  
     if(bit_is_clear(PIND,PD4) & counter >0 )  //speed down 
      {counter--;}
    
    if (bit_is_clear(PIND,PD2) )   //Change direction button
      {dir = !dir;
       _delay_ms(400); // stops the motor first
      }
    PWM_HBridge_port(counter,dir,M1,M2);
  }

  return 0;
}
