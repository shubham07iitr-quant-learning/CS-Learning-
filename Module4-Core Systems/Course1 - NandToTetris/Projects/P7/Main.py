##This is the main module (also known as the VMTranslator) which will bring in all the other modules i.e. Parser and CodeWrtiter

from Parser import Parser as Parser
from CodeWriter import CodeWriter as code
import sys ##For acceping a command line argument

def main():
    if len(sys.argv) < 2:
        raise NameError("Please enter name of the file to be translated")
    else:

        filename = sys.argv[1]
        parser = Parser(filename)
        codeWriter = code(filename)
        ##Let's first update the codeWriter.codedict with all instructions: list of assembly code
        while True:
            if parser.commandType() == "C_ARITHEMETIC":
                codeWriter.writeArithemetic(parser.arg1())
            elif parser.commandType() == "C_PUSH":
                codeWriter.writePushPop("push", parser.arg1(), str(parser.arg2()))
            else:
                codeWriter.writePushPop("pop", parser.arg1(), str(parser.arg2()))
            if parser.hasMoreLines():
                parser.advance()
            else:
                break

        ##Now that we have the codedict for all instructions, let's just push all values in an asm file 

        with open (filename[:-3]+".asm", "w") as file:
            for i in codeWriter.codelist:
                file.write(i+"\n")


if __name__ == "__main__":
    main()



        




