//Pressing a key down for long enough will set screen to black
//When we hold up the finger it will again return to all white

//Remember KBD = 24576, SCREEN = 16384, with 8192 registers
// Value at KBD == 0, when no key is pressed
// If value at 241576 is not zero, then we jump to some function which blacken the whole screen

//First check whether any key is presse
(LISTEN) //We define a new label , if no key is being pressed, we will jump here
//First we will clear the screen - we will follow exactly the same recipe as blackening

//TURNING SCREEN WHITE

//We will define two variables, one static 24576 - no of times loop to run, and one i, which will increase for every run (to start from SCREEN)
@SCREEN
D=A
@iwhite
M=D //Here we setup i to 16384
@KBD //Loading up KBD counter, we will run our loop just before KBD
D=A
@endloopwhite //Defining he endloop variable which will be static
M=D
//Now we loop through 8192 time, and set each address to -1
//First we idneitify which register to set black
(LOOPWHITE)
@iwhite
A=M //Now address register has the address which we want to turn black
M=0 //turns black
//Now we increment i
@iwhite
M=M+1
D=M
//Now we check the loop condition if RAM[i] - RAM[endloop] not equal to 0, then loop, else go to LISTEN
//First we load up runcount
@endloopwhite
D=D-M
@LOOPWHITE
D;JNE //We will loop until D-M=0

//Otherwise we will check value of KBD if it is 0 or not
@KBD 
D=M //D register now has 24576
//We will jump back to listen, when D == 0
@LISTEN
D;JEQ
//If KBD not equal to 0, then we move on to update lal the screen pixels to -1

//TURNING SCREEN BLACK IF A KEY IS PRESSED

//We will define two variables, one static 24576 - no of times loop to run, and one i, which will increase for every run (to start from SCREEN)
@SCREEN
D=A
@i
M=D //Here we setup i to 16384
@KBD //Loading up KBD counter, we will run our loop just before KBD
D=A
@endloop //Defining he endloop variable which will be static
M=D
//Now we loop through 8192 time, and set each address to -1
//First we idneitify which register to set black
(LOOP)
@i
A=M //Now address register has the address which we want to turn black
M=-1 //turns black
//Now we increment i
@i
M=M+1
D=M
//Now we check the loop condition if RAM[i] - RAM[endloop] not equal to 0, then loop, else go to LISTEN
//First we load up runcount
@endloop
D=D-M
@LOOP
D;JNE //We will loop until D-M=0

//And then we will switch to listening mode again
@LISTEN
0;JMP






