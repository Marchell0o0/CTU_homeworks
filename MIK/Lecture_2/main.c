/*
    Cilem projektu je zobrazit text na alfanumerickem LCD.
    Postup:
    - provedte inicializace radice LCD podle str.45 v manualu lcd_hitachi44780.pdf
    - provedte nastaveni parametru radice LCD podle str.43 v manualu lcd_hitachi44780.pdf
*/

#include <xc.h>
#include <pic18f4620.h>
#include "lcd_PIC18F4620.h"

#define _XTAL_FREQ 8000000

#pragma config OSC = INTIO67, FCMEN = OFF, IESO = OFF, PWRT = OFF, BOREN = OFF, WDT = OFF, PBADEN = OFF, MCLRE = ON, LVP = OFF, DEBUG = OFF, 


void main(void) 
{
    OSCCONbits.IRCF = 0b111;    // 8MHz
    ADCON1bits.PCFG = 0b1111;   // Vsechny vstupy digitalni (str. 224)
    CMCONbits.CM = 0b111;       // Odpojeni komparatoru (str. 234)
    
    
    TRISA = 0;
    TRISB = 0;
    TRISC = 0;
    TRISD = 0;
    TRISE = 0;
    LATA = 0b00000000;
    LATB = 0b00000000;
    LATC = 0b00000000;
    LATD = 0b00000000;
    LATE = 0b00000000;
 
 // Inicializace radice LCD - str. 45 v lcd_hitachi44780.pdf
    Send_Command (0b00111000);
    Send_Command (0b00111000);
    Send_Command (0b00111000);
    Send_Command (0b00111000);
    Send_Command (0b00001100);
    Send_Command (0b00000001);
    Send_Command (0b00000110);

 // Nastaven� parametru a zobrazen� znaku - str. 43 v lcd_hitachi44780.pdf
    Send_Command (0b00111000);          //krok 2
    Send_Command (0b00001110);          //krok 3
    Send_Command (0b00000110);          //krok 4
          
    Send_Data ('H');
    Send_Data ('e');
    Send_Data ('l');
    Send_Data ('l');
    Send_Data ('o');
    Send_Data (' ');
    Send_Data ('W');
    Send_Data ('o');
    Send_Data ('r');
    Send_Data ('l');
    Send_Data ('d');
    Send_Data ('!');

    __delay_ms(1000);
    Send_Command(0b00000001);
    Send_Data ('C');
    Send_Data ('y');
    Send_Data ('b');
    Send_Data ('e');
    Send_Data ('r');
    Send_Data ('p');
    Send_Data ('u');
    Send_Data ('n');
    Send_Data ('k');
    Send_Command(0b11000000); 
    Send_Data ('P');
    Send_Data ('h');
    Send_Data ('a');
    Send_Data ('n');
    Send_Data ('t');
    Send_Data ('o');
    Send_Data ('m');
    Send_Data (' ');
    Send_Data ('L');
    Send_Data ('i');
    Send_Data ('b');
    Send_Data ('e');
    Send_Data ('r');
    Send_Data ('t');
    Send_Data ('y');

    while(1)
    {
    }
    
    return;
}
