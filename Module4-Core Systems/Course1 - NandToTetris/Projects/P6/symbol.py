##Module to manage variable, label, and predefined symbols

"""
    Type/Interpretation: 
        Class to manage the symbol dictionary for our symbolic assembly program
        It will take a file name <xxx>.asm as ipnut, constructor , and also will a single dictionary during initialisation 
"""
class Symbol():
    def __init__(self):
        self.symboldict = symboltable = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,"R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,"R10": 10, "R11": 11, "R12": 12, "R13": 13,"R14": 14, "R15": 15,    "SCREEN": 16384, "KBD": 24576}
    
    """
    TEMPLATE:
        FIELDS:
        ...self.symboldict (Dict)

        METHODS:
        ...self.firstpass(self, listinstructiontuple)              ......No return (Mutates symboldict)
        ...self.secondpass(self, listinstructiontuple)              ......No return (Mutates symboldict)
    """
    #------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    """
    Signature: self, listinstructiontuple: List of Tuple of type (xxx, A_TYPE) - as stored in field listinstructiontuple for Parser > No return (mutates symboldict)
    Purpose:
        Runs through the List of Tuple provied, looks for L_TYPE and addds that into symbol table along with the corresponding address
    """
    def firstpass(self, listinstructiontuple):
        romaddress = 0
        for entry in listinstructiontuple:
            if entry[-1] == "L_TYPE":
                self.symboldict[entry[0]] = romaddress
            else:
                romaddress += 1


    """
    Signature: self, listinstructiontuple: List of Tuple of type (xxx, A_TYPE) - as stored in field listinstructiontuple for Parser > No return (mutates symboldict)
    Purpose:
        In the second pass, it will only evaluate A_TYPE instructions, if int(value_A_TYPE) raises an error - it means we have to first check whether for that smbol addressing exist
        If not we add that to our 
    """

    def secondpass(self, listinstructiontuple):
        nextavailable = 16
        for entry in listinstructiontuple:
            if entry[-1] == "A_TYPE":
                try:
                    int(entry[0])
                    continue
                except:
                    if entry[0] not in self.symboldict:
                        self.symboldict[entry[0]] = nextavailable
                        nextavailable += 1
