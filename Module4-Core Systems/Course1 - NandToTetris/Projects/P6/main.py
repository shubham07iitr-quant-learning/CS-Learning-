from Parser import Parser 
import CodeModule as code
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

        ##We will define a list structure which will hold all the opcodes for us
        listopcodes = []
        ##Now we will loop through each of the instructions and update the corresponding instruction into 0s and 1s
        for components, inst_type in assemblyfile.listinstructiontuple:
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



