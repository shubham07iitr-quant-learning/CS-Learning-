##This will be the main file for our Prelim Compiler - will call on the services of Tokeniser and Engine to generate .xml file

"""
Mechanics of this module is given below:
    - We will first identify if the given CL argument is a .jack file or a directory
    - if it is a directory, we will look for all the jack files in the directory
    - For each jack file we will create a tokeniser first, which will initialise its baseWordList
    - Then we will run .advance() method on the tokeniser so that its finalTokenList is updated 
    - ONce finalTokenLIst for the tokeniser of the given module is available, we will create an Engine object 
    - As soon as the engine object is initialised, it will update its parseList field which will have the entire parseTree in .xml format
    - This parseList will then be transferred onto a single .xml file
    - This will be repeated for all the .jack files in the module
"""

from Tokeniser_P11 import Tokeniser
from Engine_P11 import Engine
import sys
import os


"""
Signature: filename: Str > <filename>.xml : XML file outputed in the same folder
Purpose:
    This is our function which will be called up by the main functino to process a single jack file into xml file
    Mechanics explained above
"""
def processFile(filename):
    ##We initialise a tokeniser object which will create its internal finalTokenList as empty 
    #and baseWordList as list of space spearated words but w/o any comments or newLine statements
    tokeniser = Tokeniser(filename) 
    tokeniser.filename = os.path.basename(filename) ##just to pass clean filenames especially for directories
    while tokeniser.hasMoreTokens():
        tokeniser.advance() ##Running this multiple itmes will ensure finalTokenList is available for this file
    tokeniser.currentToken = tokeniser.finalTokenList[0][0]  ##ensuring currentToken starts at the beginning
    engine = Engine(tokeniser)  ##Once finalTokenList is avaiable , we initalise our Engine object, which as soon as initialised will complete the parseList for us
    outputfilename = filename.replace(".jack", ".vm")
    with open(outputfilename, "w") as file:
        for i in engine.vmWriter.commandList:
            file.write(i + "\n")
    
"""
Signature: None > None
Purpose;
    Will take a CL argument and check if it is a single jack file or a directory
    And then call processFile method on each of the files
"""
def main():
    if len(sys.argv) < 2:
        raise NameError("Please enter name of the file or directory to be translated")
    
    argument = sys.argv[1]
    
    if os.path.isfile(argument):
        if argument[-5:] != ".jack":
            raise TypeError("Please only enter file names ending with .jack")
        else:
            processFile(argument)
    
    elif os.path.isdir(argument):
        dirName = os.path.basename(argument.rstrip("/"))
        jackFiles = [f for f in os.listdir(argument) if f.endswith(".jack")]
        
        if not jackFiles:
            raise FileNotFoundError("No .jack files found in the directory")
        
        for jackFile in jackFiles:
            processFile(os.path.join(argument, jackFile))
    
    else:
        raise FileNotFoundError("The given argument is not a valid file or directory")

if __name__ == "__main__":
    main()

    
