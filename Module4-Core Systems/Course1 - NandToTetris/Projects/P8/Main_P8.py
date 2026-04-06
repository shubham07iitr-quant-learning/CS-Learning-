##This is the main module (also known as the VMTranslator) which will bring in all the other modules i.e. Parser and CodeWrtiter

from Parser_P8 import Parser as Parser
from CodeWriter_P8 import CodeWriter as code
import sys
import os

def processFile(parser, codeWriter):
    while True:
        if parser.commandType() == "C_ARITHEMETIC":
            codeWriter.writeArithemetic(parser.arg1())
        elif parser.commandType() == "C_PUSH":
            codeWriter.writePushPop("push", parser.arg1(), str(parser.arg2()))
        elif parser.commandType() == "C_POP":
            codeWriter.writePushPop("pop", parser.arg1(), str(parser.arg2()))
        elif parser.commandType() == "C_LABEL":
            codeWriter.writeLabel("label", parser.arg1())
        elif parser.commandType() == "C_GOTO":
            codeWriter.writeGo("goto", parser.arg1())
        elif parser.commandType() == "C_IF":
            codeWriter.writeIf("if-goto", parser.arg1())
        elif parser.commandType() == "C_FUNCTION":
            codeWriter.writeFunction("function", parser.arg1(), parser.arg2())
        elif parser.commandType() == "C_CALL":
            codeWriter.writeCall("call", parser.arg1(), parser.arg2())
        elif parser.commandType() == "C_RETURN":
            codeWriter.writeReturn("return")
        if parser.hasMoreLines():
            parser.advance()
        else:
            break

def main():
    if len(sys.argv) < 2:
        raise NameError("Please enter name of the file or directory to be translated")
    
    argument = sys.argv[1]
    
    if os.path.isfile(argument):
        codeWriter = code(argument, bootstrap=False)
        parser = Parser(argument)
        processFile(parser, codeWriter)
        outputFile = argument[:-3] + ".asm"
    
    elif os.path.isdir(argument):
        dirName = os.path.basename(argument.rstrip("/"))
        codeWriter = code(dirName + ".vm", bootstrap=True)
        
        vmFiles = [f for f in os.listdir(argument) if f.endswith(".vm")]
        
        if not vmFiles:
            raise FileNotFoundError("No .vm files found in the directory")
        
        for vmFile in vmFiles:
            filePath = os.path.join(argument, vmFile)
            codeWriter.filename = vmFile
            parser = Parser(filePath)
            processFile(parser, codeWriter)
        
        outputFile = os.path.join(argument, dirName + ".asm")
    
    else:
        raise FileNotFoundError("The given argument is not a valid file or directory")
    
    with open(outputFile, "w") as file:
        for i in codeWriter.codelist:
            file.write(i + "\n")

if __name__ == "__main__":
    main()