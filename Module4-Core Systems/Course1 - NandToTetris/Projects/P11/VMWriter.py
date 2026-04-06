##This module will be called upon by the Engine module to push actual commands in a dictionary

"""
Type/Interpretation:
    - While Engine will be our brain/logic/CPU of overall compilation, VMWriter would be just the typewriter
    - It is suppsoed to generate the relevant, push, pop commands and will add it to a dictionary (field of the module)
    - Eventually this dict will be transformed into a final output .vm file
    - As we know that our VM can consume the following 5 types of commmands:
        - push segment i
        - pop segment i
        - arithemetic commands: add, sub, neg, eq, gt, lt, and, or , not
        - Branching (3 commands):
            - label <label>
            - goto <label>
            - if-goto <label>
        - Function (3 commands):
            - function <functionName> <nVars>
            - call <functionName> <nArgs>
            - return
    - Our VMWriter module will be responsible for generating all of these commands and adding in the self.commandList field for us
"""

class VMWriter():
    
    """
    TEMPLATE:
        FIELDS:
            ...self.commandList: List
        METHODS:
            ...self.__init__()                                                      ...No return - only initialises our class and field variables
            ...self.writePush(segment: Str, index: Int)                             ...No return - only adds relevant commands in our commandList field
            ...self.writePop(segment Str, index: Int)                               ...No return - only adds relevant commands in our commandList field
            ...self.writeArithemetic(command: Str)                                  ...No return - only adds relevant commands in our commandList field
            ...self.writeLabel(label: Str)                                          ...No return - only adds relevant commands in our commandList field
            ...self.writeGoto(label: Str)                                           ...No return - only adds relevant commands in our commandList field
            ...self.writeIf(label: Str)                                             ...No return - only adds relevant commands in our commandList field
            ...self.writeCall(name: Str, nArgs: int)                                ...No return - only adds relevant commands in our commandList field
            ...self.writeFunction(name:Str, nVars: int)                             ...No return - only adds relevant commands in our commandList field
            ...self.writeReturn()                                                   ...No return - only adds relevant commands in our commandList field

    """
    
    """
    Signature: self > No return
    Purpose:
        Simply initialises an empty commandList field for the module
    """
    def __init__(self):
        self.commandList = []

#----------------------------------------------PUSH POP COMMANDS--------------------------------------------------------------------------------------------#

    """
    Signature: self, segment: Str, index: Int > No return
    Purpose:
        Writes a VM push command
        "push segment index" is the general pattern of the push command 
        segment one of: "constant" | "argument" | "local' | 'static' | 'this' | 'that' | 'pointer' | 'temp'
        Appends the string "push segment index" in commandList field
    """
    def writePush(self, segment, index):
        self.commandList.append("push"+" " + segment + " " + str(index))


    """
    Signature: self, segment: Str, index: Int > No return 
    Purpose:
        Writes a VM pop command
        "push segment index" is the general pattern of the push command 
        segment one of:  "argument" | "local' | 'static' | 'this' | 'that' | 'pointer' | 'temp'
        Appends the string "push segment index" in commandList field
    """
    def writePop(self, segment, index):
        self.commandList.append("pop"+" " + segment + " " + str(index))


#----------------------------------------------ARITHEMETIC COMMAND--------------------------------------------------------------------------------------------#
    """
    Signature: self, op: Str > No return
    Purpose:
        Writes a VM Arithemetic-logical command
        "op" is the general VM syntax for an arithemetic command
        op one of: add | sub | neg | eq | gt | lt | and | or | not
        Appends the string "op" in commandList field
    """
    def writeArithemetic(self, op):
        self.commandList.append(op)


#----------------------------------------------BRANCHING COMMANDS--------------------------------------------------------------------------------------------#

    """
    Signature: self, label: str > No return
    Purpose:
        Writes VM label command
        General syntax: "label <label>"
        Appends the string "label <label>" in commandList field
    """
    def writeLabel(self,label):
        self.commandList.append("label" + " " + label)



    """
    Signature: self, label: str > No return
    Purpose:
        Writes VM goto command
        General syntax: "goto <label>"
        Appends the string "goto <label>" in commandList field
    """
    def writeGoto(self,label):
        self.commandList.append("goto" + " " + label)


    """
    Signature: self, label: str > No return
    Purpose:
        Writes VM if-goto command
        General syntax: "if-goto <label>"
        Appends the string "if-goto <label>" in commandList field
    """
    def writeIf(self,label):
        self.commandList.append("if-goto" + " " + label)

#----------------------------------------------FUNCTION COMMAND--------------------------------------------------------------------------------------------#


    """
    Signature: self, name: str, nArgs:int > No return
    Purpose:
        Writes VM call command
        General syntax: "call <name> <nArgs>"
        Appends the string "call <name> <nArgs" in commandList field
    """
    def writeCall(self,name, nArgs):
        self.commandList.append("call" + " " + name + " " + str(nArgs))


    """
    Signature: self, name: str, nVars:int > No return
    Purpose:
        Writes VM function declaration command
        General syntax: "function <name> <nVars>"
        Appends the string "function <name> <nVars" in commandList field
    """
    def writeFunction(self,name, nVars):
        self.commandList.append("function" + " " + name + " " + str(nVars))


    """
    Signature: self> No return
    Purpose:
        Writes VM return declaration command
        General syntax: "return"
        Appends the string "return" in commandList field
    """
    def writeReturn(self):
        self.commandList.append("return")