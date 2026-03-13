from Parser import Parser 
import CodeModule as code
from symbol import Symbol
import sys ##For acceping a command line argument

def main():
    if len(sys.argv) < 2:
        raise NameError("Please enter name of the file to be translated")
    else:
        filename = sys.argv[1]
        assemblyfile = Parser(filename)
        ##Let's first update the fields listall, and listofinstructions
        assemblyfile.updatelistall()
        assemblyfile.updatelistofinstructions()
        ##Now let's update the fields dictinstructions
        assemblyfile.updatelistinstructiontuple()

        
        ##Ok so only thing in terms of logic we need to change is that for all A_TYPE instructions , where int(value) raises an error, we will look for the corresponding address in the symbol table
        ##First let's construct the symbol table and run the methods for first and second pass
        symbol = Symbol()
        symbol.firstpass(assemblyfile.listinstructiontuple)
        symbol.secondpass(assemblyfile.listinstructiontuple)
        ##Now we will again go thoruhg our listinstructiontuple, and update the corresponding address from symbol table, we will create a new list
        listinstructiontupleupdated = []
        for i in assemblyfile.listinstructiontuple:
            if i[-1] == "C_TYPE":
                listinstructiontupleupdated.append(i)
            elif i[-1] == "L_TYPE":
                continue
            else:
                try:
                    int(i[0])
                    listinstructiontupleupdated.append(i)
                except:
                    if i[0] not in symbol.symboldict:
                        raise ValueError("This value was not available in Smbol Table")
                    else:
                        listinstructiontupleupdated.append((str(symbol.symboldict[i[0]]), "A_TYPE"))
        ##We will define a list structure which will hold all the opcodes for us
        listopcodes = []
        ##Now we will loop through each of the instructions and update the corresponding instruction into 0s and 1s
        for components, inst_type in listinstructiontupleupdated:
            if inst_type == "A_TYPE":
                listopcodes.append("0" + code.convertbinary(int(components))[1:] + "\n")
            elif inst_type == "C_TYPE":
                opcode = code.generateopcode(components[0], components[1], components[2])
                listopcodes.append(opcode + "\n")
        ##Now we return the correspoinding file as <xxx>.hack
        with open (filename[:-4]+".hack", "w") as file:
            for i in listopcodes:
                file.write(i)


if __name__ == "__main__":
    main()



