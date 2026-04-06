##This module will be responsible for decomposing a given VM instruction such as pop local 2 into its components 

"""
    Type/Interpretation:
        This module/class will be responsible for taking in a VM instruction and splitting it up into its constitutents 
        The constituents will then be worked up by CodeWriter class
        There are 4 categries of instructions to be parsed:
            - Arithemetic (9 commands): add, sub, neg, eq, gt, lt, and, or , not
            - Memory Access (2 commands): 
                - push <segment> <xxx>
                - pop <segment> <xxx>
                - Segment could be of 8 types: ARG, LCL, THIS, THAT, TEMP, POINTER, STATIC, CONSTANT
            - Branching (3 commands):
                - label <label>
                - goto <label>
                - if-goto <label>
            - Function (3 commands):
                - function <functionName> <nVars>
                - call <functionName> <nArgs>
                - return

        Parsing would involve 3 steps:
            - Identifying whether the given command is one of arithemeitc, push, pop, label, goto, if, fucntion, return, or call
            - Return arg 1 (segment xxx , or functionName or add, sub etc. for arithemetic ops)
            - Returns arg 2 (such as <label> or <segment value> or <nVars> etc.)
        
        It would have a constructor, which would take in the name of the file, or directory , and read the corresponding file from memory and store each instruction as a list
        CLass will also have a private function called getWord to get the corresponding word from an instruction 
"""

class Parser():
    """
        Signature: self, filename: str > Parser object
        Purpose:
            This is the constructor/initialise funciton which will create a new Parser object
            We will initialise a listall field which will capture all the instructions read from the filename in a list of strings of instructions
            We will also initialise an index which will be 0 when it is pointing to start of the list, and will be len(list) - 1, when pointing to end of list
            We will also initialise a lenlistall field, which will store how many total instructions are there to be parsed
            Based on the given filename, constructor function will read the file and store all the instructions in listall field
    """
    
    """
    TEMPLATE:
        FIELDS:
        ...self.filename (Str)
        ...self.listall (List)
        ...self.listindex (List)
        ...self.lenlistall (List)
        ...self.currentcommand (Str)
        ...self.arithdict (Dict)
        ...self.commanddict (Dict)
        METHODS:
        ...self.__init__                               ...No return (Initialises the object including its fields)
        ...self.hasMoreLines(self)                     ...boolean
        ...self.advance (self)                         ...No return (Updates listindex and currentcommmand fields)
        ...self.commandType(self)                      ...Str
        ...self.arg1(self)                             ...Str
        ...self.arg2(self)                             ...Int
        ...self.getWord(self, position:Int)            ...Int
        
    """



    def __init__(self, filename):
        if filename[-3:] != ".vm":
            raise NameError("Please only input .vm file extensions")
        else:
            self.filename = filename
            self.listall = [] ##Defining a blank list
            with open (self.filename) as file:
                listfile = file.readlines()
            for line in listfile:
                if line.strip() == "" or line.strip()[0:2] == "//":
                    continue
                else:
                    self.listall.append(line.strip()) ##We update our listall field with all the instructions from the compiled .vm file
            self.listindex = 0 ##We initialise the listindex to be set to 0 pointing at the base of listall file
            self.lenlistall = len(self.listall) 
            self.currentcommand = self.listall[self.listindex] ##Will represent the current command 
            ##We will also define 2 data structires, one  list for identifying arithemteic commadns, and one map for other commands:
            self.arithdict = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or" , "not"]
            self.commanddict = {"push": "C_PUSH", "pop": "C_POP", "label": "C_LABEL", "if-goto": "C_IF","goto": "C_GOTO", "function": "C_FUNCTION", "return": "C_RETURN", "call": "C_CALL"}
            


    """
        Signature: self > boolean
        Purpose:
            Checks listindex and if it is <= self.lenlistall - 1, will return truen else will return false
    """
    def hasMoreLines(self):
        return self.listindex < self.lenlistall - 1
        
    """
        Signature: self > None (Only mutates listindex and currentcommand)
        Purpose: If hasMoreLines is true, will move the listindex forward by 1, and acccordingly the currentcommand will also be updated
    """
    def advance(self):
        if self.hasMoreLines():
            self.listindex = self.listindex + 1
            self.currentcommand = self.listall[self.listindex]
        
    """
    Signature: self> commandType: Str
    Purpose:
        Will use listindex field to get the current instruction, and for that instruction identify if it is one of:
        C_ARITHEMETIC , C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
    """
    def commandType(self):
        firstWord = self.getWord(1) ##This is a private function to be used by our Class, to be solved
        if firstWord in self.arithdict:
            return "C_ARITHEMETIC"
        else:
            return self.commanddict[firstWord]
        
    
    """
    Signature: self > 2nd word: String
    Purpose:
        Returns the first argument of the current command , for e.g. for push this 3, will return "this", for function new 3, will return "new"
        In case of C_ARITHEMETIC, command itself (add, sub) is returned
        Should not be called with C_RETURN command
    """
    def arg1(self):
        if self.commandType() == "C_ARITHEMETIC":
            return self.currentcommand
        elif self.commandType() == "C_RETURN":
            raise ValueError("Cannot call arg1 method with C_RETURN type command")
        else:
            return self.getWord(2) ##Again something we need to define soon - we use the same function but with the argument 2 which means we want access to 2nd word
        

    """
    Signature: self > 3rd word: Int
    Purpose:
        Returns the 2nd arugment of the current command, for e.g. for push this 3, will return 3, for function new 3, will return 3
        Should be called only if currentcommand is C_PUSH, C_POP, C_FUNCTION, C_CALL
    """
    def arg2(self):
        if self.commandType() not in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            raise ValueError("Cannot call arg2 with this instruction")
        else:
            return self.getWord(3)  ##Again using getWord method and saying we want 3rd word 
        


    """
    Signature: self, int > Str
    Purpose:
        Takes in the current command, and returns the 1st, 2nd , or 3rd word from the command based on the argument received
        We will first split the current command based on spaces, and then 
    """
    def getWord(self, position):
        splitWord = self.currentcommand.split()
        return splitWord[position - 1]


        



        
