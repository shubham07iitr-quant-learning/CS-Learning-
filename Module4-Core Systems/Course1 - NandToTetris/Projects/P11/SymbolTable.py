##This module will be responsible for creating and managing symbol tables to hold class and subroutine level vairables in our Engine class

"""
Type/Interpretation:
    A simple module which creates and manages symboltable - to be used during class declaration and subroutine declaration
    Variables in our compiler will broadly have two scopes:
        - Class level: Avilable for all subroutines throughout the class
            - Field: Instantiated during object creation
            - Static: Instantiated during Class declaration itself - cannot be changed for a particular instance of a class
        - Subroutine level: Available only within the subroutines in which they are defined:
            - Arg: Passed during subroutine call
            - Local: defined during subroutine declaration

    Hence we will manage 2 symbol tables inside our compiler - one for class and one for subroutine
    And this will be done through our SymbolTable, which will be a dictionary of the form:
    {'name': {'type': int|char|boolean|className, 'kind': STATIC|FIELD|ARG|VAR, 'index': int}}
    And the module will offer multiple methods to manage the symboltable
"""
class SymbolTable():
    """
    TEMPLATE:
        FIELDS:
            ...self.table: Dict of the form {'name': {'type': int|char|boolean|className, 'kind': STATIC|FIELD|ARG|VAR, 'index': int}}
            ...self.indexTable: Dict 

        METHODS:
            ...self.__init__()                                  ...No return (only initialises the class fields)
            ...self.reset()                                     ...No return (empties the symbol table)
            ...self.define(name: Str, type: Str, kind: Str)     ...No return (adds a new entry to our table)
            ...self.varCount(kind: Str)                         ...Int
            ...self.kindOf(name:Str)                            ...String(STATIC | FIELD | ARG | VAR)
            ...self.typeOf(name:Str)                            ...String(int | char | boolean | className) 
            ...self.indexOf(name:Str)                           ...Int
    """

    """
    Signature: None > No return (Only initialises the class/object variables)
    Purpose: Initialises the following fields:
            - self.table: Dict of the form {'name': {'type': int|char|boolean|className, 'kind': STATIC|FIELD|ARG|VAR, 'index': int}}
            - self.indexTable of the form {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}
    """
    def __init__(self):
        self.table = {}
        self.indexTable = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}


    
    """
    Signature: self > None 
    Purpose:
        - Empties the symbol table, and resets the 4 indices to 0
        - Should be called when starting to compile a new subroutine declaration
    """
    def reset(self):
        self.table.clear() ##Deletes all entries from the dict
        self.indexTable = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0} ##Resets all indices to 0

    """
    Signature: 
        self, name: Str, type: Str, kind: Str > No return , just updates our table
        kind is one of: STATIC|FIELD|ARG|VAR

    Purpose:
        - Adds to the table a new variable of the given name, type ,and kind
        - Assigns index value to the entry, and then increments the index value of that kind
    """
    def define(self, name, type, kind):
        self.table[name] = {"type": type, "kind": kind, "index": self.indexTable[kind]}
        self.indexTable[kind] = self.indexTable[kind] + 1 ##Incrementing the index value for the specific kind of variable
    

    """
    Signauture: kind: Str (one of STATIC | FIELD | ARG | VAR) > Int
    Purpose: Returns the number of variables of the given kind already defined in the table
    """
    def varCount(self, kind):
        return self.indexTable[kind]
    
    """
    Signature: self, name: Str > Str (one of STATIC | FIELD | ARG | VAR)
    Purpose: 
        Returns the kind of named identifier
        If identifier is not found, returns NONE
    """
    def kindOf(self, name):
        if name in self.table:
            return self.table[name]["kind"]
        else:
            return None
        
    """
    Signature: self, name: Str > Str 
    Purpose: 
        Returns the type of of named identifier
        If identifier is not found, returns NONE
    """
    def typeOf(self, name):
        if name in self.table:
            return self.table[name]["type"]
        else:
            return None
        
    """
    Signature: self, name: int
    Purpose: 
        Returns the index of named identifier
        If identifier is not found, returns NONE
    """
    def indexOf(self, name):
        if name in self.table:
            return self.table[name]["index"]
        else:
            return None
    




