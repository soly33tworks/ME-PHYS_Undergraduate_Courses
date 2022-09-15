#include <avr/io.h>
#include <util/delay.h>
#include "USART.h"
#include "USART.c"

#define turnon(inbyte, loct) inbyte |=(1<<loct);
#define turnoff(inbyte, loct) inbyte &= ~(1<<loct)

void rotate_servo(int angle);
void rotate_servo(int angle)
{
  int t_count = angle*1.15; //how many microseconds to count
  int n = 5;
  
  for(int i=0;i<n;i++)  //send the position information n times
  {
    turnon(PORTB,PB1)
    _delay_ms(0.5);
    for(int j=0;j<t_count ; j++)
        {
          _delay_us(9);
        }
    turnoff(PORTB,PB1);
    _delay_ms(18.5);
  }
}

 void initADC0(void){
  ADMUX |= (1<<REFS0); // REFS1=0, REFS0=1 ref voltage on AVCC (internal 5V)

  //ADMUX |= (1<<MUX0) | (1<<MUX1);  // if you want to read sensor on ADC3 
  
  ADCSRA |= (1<<ADPS2) |  (1<<ADPS1) | (1 << ADPS0) ; //ADC clock prescaler: 128. 16 MHz / 128= 125kHz 
  ADCSRA |= (1<<ADEN); // enable ADC, "internal circuit gets ready"
} // note: mux=0 as initialized 

int main (void) {
  long int adcValue;
  long int angle_digi;
  DDRB=0b00000010; // B4 will be used as output
  DDRD=0;

  initADC0();
  initUSART();

  while (1) { 

    ADCSRA |= (1<<ADSC); // start ADC conversion 
    loop_until_bit_is_clear(ADCSRA, ADSC); // wait until done, think how to write this macro?
    adcValue = ADC;  // read ADC in  
    // long int ADC = (ADCH<<8) + ADCL

    angle_digi = (adcValue >>2)*180/255; 

//    printString("\r\n adcValue is: ");
//    printByte(adcValue);
    printString("\r\n angle is: ");
    printByte(angle_digi);
    rotate_servo(angle_digi);
    _delay_ms(10);
//    rotate_servo(0);               
  }
  
}
