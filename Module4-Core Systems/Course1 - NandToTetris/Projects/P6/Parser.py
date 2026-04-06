##Module to decompose different instructions into individual strings, which could then be further worked on


"""
    Type/Interpretation: 
        Class to operate on a .asm file , and parse each instruction into its sub-components
        It will take a file name <xxx>.asm as ipnut, constructor and try and read that from the system
"""

class Parser():
    def __init__(self, filename):
        if filename[-4:] != ".asm":
            raise TypeError("Please only input .asm file extensions")
        else:
            self.filename = filename
            self.listall = [] ##will capture all instructions including comments but excluding empty lines
            self.listofinstructions = [] ##Will capture all instructions line by line w/o comments
            self.listinstructiontuple = [] ##This will be of type [(instruction, A_TYPE)] etc

    """
    TEMPLATE:
        FIELDS:
        ...self.filename (Str)
        ...self.listall (List)
        ...self.listofinstructions (List)
        ...self.listcomponents(List)
        ...self.dictinstructions(Dict)
        METHODS:
        ...self.updatelistall                          ...No return (Mutates self.listall)
        ...self.updatelistofinstructions(self)         ...No return (Mutates self.listofinstructions)
        ...self.instructionType(self, Str)             ...Type of Instruction (Str)
        ...self.symbol(self, instruction:Str)           ...Str
        ...self.cdecode(self,instruction:Str)           ...Opcode(Str) 
        ...self.updatelistinstructiontuple(self)       ...No return (Mutates listinstructiontuple)
        
    """

    #------------------------------------------------------------------------------------------------------------------------------------------------------------#
    """
    Signature: 
        Input (Self)
        Output : No returns, just updates the listall field of the object
    Purpose: 
        Reads through each line from the given filename, and adds each line as string to the original object's listall field
        A blank line is read as '' and any whitespaces in front of a line are automatically dropped
    """
    def updatelistall(self):
        with open(self.filename) as file:
            listfile = file.readlines()

        for line in listfile:
            self.listall.append(line.strip())
        
    """
    Signature: self > No return (only mutates self.listofinstructions)
    Purpose: 
        Takes in self.listall , and drops in any comments beginning with //, and drops any blank lines
        We will not solve for cases when comment can appear later after an instruction 
    """

    def updatelistofinstructions(self):
        
        for line in self.listall:
            if line =='' or line[0:2] == "//":
                continue
            else:
                self.listofinstructions.append(line)
        

    """ 
    Signature: self, instruction: Str> instType: Str
    Purpose: 
        Takes in a string of instruction and confirms whether it is an A instruction or C instruction or L instruction
        If instruction is of type (xxx), then L_Instruction
        If it is of type @xxx, then A instruction
        If it is of type x=y;z then it is of C instruction 
    """
    def instructionType(self, instruction):
        if instruction[0] == "(" and instruction[-1] == ")":
            return "L_TYPE"
        if instruction[0] == "@":
            return "A_TYPE"
        else:
            return "C_TYPE"
        
    """
    Signature: self , instruction: Str > symbol: Str
    Purpose:
        If current instruction is (xxx), returns symbol 'xxx'
        If current instruction is @xxx, returns the symbol or decimal 'xxx' (as a string)
        Should be called only if instructionTpe is A_TYPE or L_TYPE
    """
    def symbol(self, instruction):
        if self.instructionType(instruction) not in ['A_TYPE', 'L_TYPE']:
            raise ValueError("Pls input only A or L type instructions")
        else:
            if instruction[0] == "@":
                return instruction[1:] ##Corresponding to A 
            else:
                return instruction[1:-1] ##Corresponding to Symbol
    
    """
    Signature: self, instruction:Str > (dest:Str, comp: Str, jump: Str) 
    Purpose:
        Takes in a C instruction , and returns a tuple of respective dest, comp and jump strings, if dest and jump are not there, it will be updated as None
        We will build a simple assmebler which will look for only the first instance of "=" and ";"
    """
    def cdecode(self,instruction):
        if self.instructionType(instruction) != "C_TYPE":
            raise ValueError("Pls input only C type instructions")
        else:
            leninstruction = len(instruction)
            equalindex = None 
            colonindex = None
            for i in range(leninstruction):
                if instruction[i] == ";":
                    colonindex = i 
                else:
                    if instruction[i] == "=":
                        equalindex = i
            if colonindex is not None and equalindex is not None:
                jumpstr = instruction[colonindex+1:]
                deststr = instruction[0: equalindex]
                compstr = instruction[equalindex+1:colonindex]
            elif colonindex is not None and equalindex == None:
                deststr = None
                compstr = instruction[0:colonindex]
                jumpstr = instruction[colonindex+1:]
            elif equalindex is not None and colonindex == None:
                jumpstr = None
                deststr = instruction[0: equalindex]
                compstr = instruction[equalindex+1:]
            else: 
                jumpstr = None 
                deststr = None 
                compstr = instruction

            return (deststr, compstr, jumpstr)
        

    """
    Signature: Self > No returns (Just mutates listinstructiontuple):
    Purpose:
        Loops through listofinstructions, identifies it as A or C or L, and then breaks it down into indiviudla components 
    """
    def updatelistinstructiontuple(self):
        for i in self.listofinstructions:
            if self.instructionType(i) == "A_TYPE":
                components = self.symbol(i)
                self.listinstructiontuple.append((components, "A_TYPE"))
            elif self.instructionType(i) == "L_TYPE":
                components = self.symbol(i)
                self.listinstructiontuple.append((components, "L_TYPE"))
            else:
                components = self.cdecode(i)
                self.listinstructiontuple.append((components, "C_TYPE"))
                        




