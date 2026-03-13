##importing the relevant modules
import math

##WThis module will enable us to transform C Instructions into its respective opcodes
##For this we will need 3 data dictionaries to capture mapping of str>binar opcodes as below

##Denotes the mapping for destination at which we want to store the values
destdict = {None: "000", "M": "001", "D": "010", "DM": "011", "A": "100", "AM": "101", "AD": "110", "ADM": "111"}

##Denotes the mapping for jump instructions
jumpdict = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

##Denotes the mapping for comp insrtuctions
compdict = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

"""
    Signature: (deststr, compstr, jumpstr):(Str, Stri, Str) > Opcode (Str)
    Purpose: To translate destination, comp, and jump string such as D=M+1;JEQ to its corresponding opcode such as 011010101000010101
"""


def generateopcode(deststr, compstr, jumpstr):
    if deststr not in destdict or compstr not in compdict or jumpstr not in jumpdict: 
        raise ValueError("Input values incorrect")
    else:
        destcode = destdict[deststr]
        compcode = compdict[compstr]
        jumpcode = jumpdict[jumpstr]
        copcode = "111"+compcode+destcode+jumpcode
        return copcode
    
"""
    Signature: num:Int > binary:Str
    Purpose: Converts a decimal number into its corresponding 16 bit binary representation (Str)
"""

def convertbinary(num):
    if num < 0 or num > 32767:
        raise ValueError("Input values incorrect")
    else:
        listof1s = [] 
        while num > 0:
            i = int(math.log2(num))
            listof1s.append(i+1)
            num = num - 2**i
        binarylist = ["0", "0", "0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        
        for i in listof1s:
            binarylist[16-i] = "1"
        return "".join(binarylist)
