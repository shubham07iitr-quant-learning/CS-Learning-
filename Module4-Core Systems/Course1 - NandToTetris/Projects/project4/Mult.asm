//Multiply two numbers where num1 is in R0 and R1, and store result in R2
//Assume R0 >= 0, R2 >= 0, R0*R1 <32768


//Define a new variable i = 1, loop will run till i = R1
@i
M=1 //We initialise i to 1
//We will also define a new variable sum, which will hold intermediate sums
@sum
M=0 
//Define loop
(LOOP)
//Get R0 to D, and add to sum, and store at sum
@R0
D=M 
@sum
M=D+M
//Increment i, and storing it in its storage
@i
D=M //Getting value of i to D register
D=D+1 //Incrementing value of i
M=D //And storing it in i
//Now we will check whether i < R1 or not
@R1 //Selecting value in R1
D=D-M //D holds i, and we subtract from it , if D-M = 0, then loop will stop
@LOOP //We load up loop address, so that we jump to loop, if D-M <= 0
D;JLE

//Now we will get value of sum to R2
@sum
D=M
@R2
M=D // This will get sum to R2
//And now we will terminate using an infinite loop
(END)
@END
0;JMP