##This module will be responsible for creating the relevant parse Tree for the given tokeniser

##importing the SymbolTable and VMWriter modules:
from SymbolTable import SymbolTable as st
from VMWriter import VMWriter as vm

"""
Type/Interpretation:
    This module will be responsible for ingesting a tokeniser object and parsing through each token to generate a list of VM commands, 
    which will be eventually transferred to a .vm file (transfer outside scope of this module)
    Key fields:
        - Tokeniser: which will have the self.finalTokenList to be parsed into vm code
        - SymbolTable: we will have 2 separate instances of this class:
            - classSymbolTable: to keep track of class level variables
            - subroutineSymbolTable: to keep track of subroutine level variables
        - VMWriter: this will be responsible for:
            - Managing the list of VM commands generated so far - through the field 'self.commandList'
            - Generates relevant commands and appends it to the 'self.commandList' 

    Semantics:
        Naming Convention:
            <xxx.jack> compiled to <xxx.vm>
            <yyy> subroutine in file <xxx>.jack compiled as <xxx.yyy>, however:
                Constructor/Functions defined with K args compiled with K args, but Method compiiled with K+1 args
        Mapping:
            Variables: STATIC: static 0/1/2.. | LOCAL: local 0/1/2... | ARG: argument 0/1/2... | FIELD: this 0/1/2
            Constants: false/null: push constant 0 | true: push constant 1, neg | this: push pointer 0
            Objects: To align virtual segment THIS: push argument 0, pop pointer 0
            Arrays: high-level reference arr[expression] is compiled by setting pointer 1 to (arr+ expression) and accessing that 0
        Handling Variables
            Declaration: No code generated, update symbol table only
            Assignment: Check symbol table, get the typeOf (argument, static, this etc. ) and the index (0,1,2...) and use normal pop segment i command
        Handling other semantics mentioned wherever they are applicable
"""





class Engine():
    """
    TEMPLATE:
        FIELDS:
            ...self.tokeniser: TOKENISER
            ...self.classSymbolTable: SYMBOLTABLE
            ...self.subroutineSymbolTable: SYMBOLTABLE
            ...self.vmWriter: VMWriter
            ...self.currentSubroutineName: Str
            ...self.currentSubroutineIsVoid: Boolean
            ...self.currentSubroutinetype: Str (Constructor | Method | Function)
            ...self.opDict: Dict
        METHODS:
            ...self.compileXXX (self)                           ...No return (Updates vmWriter.commandList)
            ...self.compileExpressionList(self)                 ...Count of expressions passed as params: Int
            ...self.generateLabel(self)                         ...Str
    """

    ##----------------------------------------------------------------------------------------------------------------------------------------------------------------##
    """
    Signature: self, tokeniser: TOKENISER, classSymbolTable: SYMBOLTABLE, subroutineSymbolTable > No return, initialises our Engine
    Purpose:
        Initialises the tokeniser field to the input TOKENISER object (should have completed parsing of the input file), 
        And initialises the vmWriter field, which will generate and store the VM commands
        And initialises class and subroutine level symbol table
        And initialises subRoutineName and SubroutineisVoid and currentSubroutineType or not
        And initilaises the opDict
        Calls on compileClass function on the first token from tokeniser field 
    """
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser 
        self.classSymbolTable = st()
        self.subroutineSymbolTable = st()
        self.vmWriter = vm()
        self.labelCounter = 0
        self.currentSubRoutineName = ""
        self.currentSubroutineIsVoid = False
        self.currentSubroutineType = ""
        self.opDict = {'+': 'add', '-': 'sub', '&': 'and', '|': 'or', '<': 'lt', '>': 'gt', '=': 'eq'}
        self.compileClass() ##This will be called on the first token

    """
    Signature: self > No return
    Purpose:
        Returns a unique label to be used by branching commands of type <filename>.label<labelCounter>
        Uses self.labelCounter variable and increments after generating the label
    """
    def generateLabel(self):
        tempLabel = self.tokeniser.filename + "." + str(self.labelCounter)
        self.labelCounter = self.labelCounter + 1
        return tempLabel

    
##--------------------------------------------------------COMPILEXXX() METHODS-------------------------------------------------------------------------------------##
##Now we will write down all the compile Methods along with the corresponding Jack Grammar rules;


    """
    Signature: self > No return (only appends XML tags in our self.parseList)
    Purpose: 
        Compiles a complete Jack Class
        Corresponding Jack Grammar rule:
            - class: 'class' className '{' classVarDec* subroutineDec* '}'
    Execution:
        We continue advancing tokens until we reach static or field 
        At which point we call compileClassVarDec
        ONce done,  we call compileSubroutine untile we have constructor, function, or method
    """
    def compileClass(self):
        
        self.tokeniser.getCurrentToken() ##skip over "class"
        self.tokeniser.getCurrentToken()  ##skip over "className"
        self.tokeniser.getCurrentToken() ##skip over "{}"
        while self.tokeniser.currentToken in ("static", "field"):
            self.compileClassVarDec()
        ##Now let's call the compileSubRoutine() methods as many times as required
        while self.tokeniser.currentToken in ("constructor", "function", "method"):
            self.compileSubRoutine()
        self.tokeniser.getCurrentToken() ##skip over final '}'


    """
    Signature: 
    Purpose: 
        Compiles a static variable declaration , or a field declaration
        Corresponding Jack Grammar rule:
            - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        Execution:
            - store the current token in kindTemp variable
            - First get next token and store in type variable
            - then get next token and that will be name 
            - Update our class symbol table (kind will be either static or field)
            - Run a while loop to check while currentToken == ',', we skip over ',' and store continued varNames in symbolTable
            - skip over ';'
    """
    def compileClassVarDec(self):
        kindTemp = self.tokeniser.getCurrentToken() ##skip over static/field
        typeTemp = self.tokeniser.getCurrentToken() ##get type of variable such as int, char etc
        varNameTemp = self.tokeniser.getCurrentToken() ##get name of variable
        self.classSymbolTable.define(varNameTemp, typeTemp, "STATIC" if kindTemp == "static" else "FIELD") ##Addint to the symbol table
        ##Now we will solve for different case where we have syntax with multiple varName in a single line like static int x,y,z...
        while (self.tokeniser.currentToken == ","):
            self.tokeniser.getCurrentToken() ##skip over ','
            varNameTemp = self.tokeniser.getCurrentToken()
            self.classSymbolTable.define(varNameTemp, typeTemp, "STATIC" if kindTemp == "static" else "FIELD") ##Adding the variable to the symbol table
        self.tokeniser.getCurrentToken() ## skip over ";"
        


    """
    Signature: 
    Purpose: 
        Compiles a complete method, function, or constructor 
        Corresponding Jack Grammar rule:
            - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    Execution:
        - reset symbol table
        - self.currentsubRoutineType == currentToken
        - if currentToken == 'void' , self.currentSubroutineIsVoid = True
        - self.currentSubroutineName = currentToken
        - skip '('
        - call compileParamList
        - skip ')'
        - compileSubroutineBody
    """
    def compileSubRoutine(self):
        self.subroutineSymbolTable.reset()
        self.currentSubroutineType = self.tokeniser.getCurrentToken()
        self.currentSubroutineIsVoid = False
        if self.currentSubroutineType == "method":
            self.subroutineSymbolTable.define("this", self.tokeniser.filename[:-5], "ARG")
        if self.tokeniser.currentToken == "void":
            self.currentSubroutineIsVoid = True
        self.tokeniser.getCurrentToken()  ##skip over return type (void/int/etc.)
        self.currentSubRoutineName = self.tokeniser.filename[:-5] + "." + self.tokeniser.getCurrentToken()
        self.tokeniser.getCurrentToken() ##skip over "("
        self.compileParameterList() ##compiling param list
        self.tokeniser.getCurrentToken() ##skip over ")"
        self.compileSubroutineBody() ##This will do all the heavy lifting


    """
    Signature: 
    Purpose: 
        Compiles a (possibly empty) param list, does not handle enclosing parenthesis tokens ( and )
        Corresponding Jack Grammar rule:
            - parameterList: ( (type varName) (',' type varName)* )?
        Execution:
            Assuming symboltable for subroutine would have been reset during compileSubRoutine
            If currentToken is ')' then no params, so we just do nothing , else:
                - getcurrentToken - which will be typeTemp
                - getcurrentToken - which will be varName
                - Add this to subRoutineSymboltable where kind == argument
                - while currentToken == ',' repeat the 1st 3 steps
            
    """
    def compileParameterList(self):
        if self.tokeniser.currentToken == ')':
            pass
        else:
            typeTemp = self.tokeniser.getCurrentToken() ##setup type for symbol table
            varNameTemp = self.tokeniser.getCurrentToken() ##setup varName for symbol table
            self.subroutineSymbolTable.define(varNameTemp, typeTemp, "ARG") ##adding variables to the symbol table
            while self.tokeniser.currentToken == ",":
                self.tokeniser.getCurrentToken() ##skipping over ','
                typeTemp = self.tokeniser.getCurrentToken() ##setup type for symbol table
                varNameTemp = self.tokeniser.getCurrentToken() ##setup varName for symbol table
                self.subroutineSymbolTable.define(varNameTemp, typeTemp, "ARG") ##adding variables to the symbol table
        


    """
    Signature: 
    Purpose: 
        Compiles a (possibly empty) param list, does not handle enclosing parenthesis tokens ( and )
        Corresponding Jack Grammar rule:
            - subroutineBody: '{' varDec* statements '}'
    Execution:
        - skip over '{'
        - while current token == var, call compileVarDec
        - localVarCount = get local var count from subRoutineSymbolTable
        - if self.currentSubroutineType == "Function":
            - use writeFunction(self.currentSubroutineName, localVarCount)
        - if it is "Constructor:
            - use writeFunction(self.currentSubroutineName, localVarCount)
            - fieldCount = get fieldCount for the classSymbolTable
            - push constant fieldCount
            - call Memory.alloc 1
            - pop pointer 0
        - if it is a method:
            - use writeFunction(self.currentSubroutineName, localVarCount)
            - push argument 0
            - pop pointer 0
        - call compileStatements
        - check if void, if true then pop temp 0
    """
    def compileSubroutineBody(self):
        self.tokeniser.getCurrentToken() ## skip over '{'
        while self.tokeniser.currentToken == "var":
            self.compileVarDec()
        localVarCount = self.subroutineSymbolTable.varCount("VAR")
        self.vmWriter.writeFunction(self.currentSubRoutineName, localVarCount)
        if self.currentSubroutineType == "constructor":
            fieldCount = self.classSymbolTable.varCount("FIELD")
            self.vmWriter.writePush("constant" , fieldCount)
            self.vmWriter.writeCall("Memory.alloc", 1)
            self.vmWriter.writePop("pointer" , 0)
        elif self.currentSubroutineType == "method":
            self.vmWriter.writePush("argument" , 0)
            self.vmWriter.writePop("pointer" , 0)

        self.compileStatements()
        self.tokeniser.getCurrentToken() ##skip over '}'
    
    
    
    """
    Signature: 
    Purpose: 
        Compiles a var Declaration
        Corresponding Jack Grammar rule:
            - varDec: 'var' type varName (',' varName)* ';'
    Exeuction:
        - Skip over 'var'
        - Exactly same as parameter list declaration - exceltp kind would be "local", and type will not be defined again
        - skip over ;
    """
    def compileVarDec(self):
        self.tokeniser.getCurrentToken() ##skip over 'var'
        typeTemp = self.tokeniser.getCurrentToken() ##setup type for symbol table
        varNameTemp = self.tokeniser.getCurrentToken() ##setup varName for symbol table
        self.subroutineSymbolTable.define(varNameTemp, typeTemp, "VAR") ##adding variables to the symbol table
        while self.tokeniser.currentToken == ",":
            self.tokeniser.getCurrentToken() ##skipping over ','
            varNameTemp = self.tokeniser.getCurrentToken() ##setup varName for symbol table
            self.subroutineSymbolTable.define(varNameTemp, typeTemp, "VAR") ##adding variables to the symbol table
        self.tokeniser.getCurrentToken() ##skipping over ';'


    """
    Signature: 
    Purpose: 
        Compiles a sequence of statements. Does not handle enclosing curly bracket tokens { and }
        Corresponding Jack Grammar rule:
            - statements: statement*
            - statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
    Execution:
        Will only call other compileMethods as required - no code generation inside this
    """
    def compileStatements(self):
        while self.tokeniser.currentToken in ["let", "if", "while", "do", "return"]:
            if self.tokeniser.currentToken == "let":
                self.compileLet()
            elif self.tokeniser.currentToken == "if":
                self.compileIf()
            elif self.tokeniser.currentToken == "while":
                self.compileWhile()
            elif self.tokeniser.currentToken == "do":
                self.compileDo()
            elif self.tokeniser.currentToken == "return":
                self.compileReturn()

    """
    Signature: 
    Purpose: 
        Compiles a let statement
        Corresponding Jack Grammar rule:
            - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        Execition:
            Have separate branch to solve for possible array - need a lookahead token for this
    """
    def compileLet(self):
        self.tokeniser.getCurrentToken() ##skipping over 'let'
        if self.tokeniser.currentTokenIndex + 1 < len(self.tokeniser.finalTokenList):
            nextToken = self.tokeniser.finalTokenList[self.tokeniser.currentTokenIndex+1][0]
        else:
            nextToken = ""
        if nextToken == "[":
            if self.tokeniser.currentToken in self.subroutineSymbolTable.table:
                segmentName =  "local" if self.subroutineSymbolTable.table[self.tokeniser.currentToken]["kind"] == "VAR" else "argument"
                index = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["index"]
            else:
                segmentName =  "static" if self.classSymbolTable.table[self.tokeniser.currentToken]["kind"] == "STATIC" else "this"
                index = self.classSymbolTable.table[self.tokeniser.currentToken]["index"]
            self.vmWriter.writePush(segmentName, index=index) ##this will get address of array on heap on the global stack
            self.tokeniser.getCurrentToken() ##skip over varName
            self.tokeniser.getCurrentToken() ##skip over '['
            self.compileExpression() ##compute address of "arr + expression"
            self.vmWriter.writeArithemetic("add") ##to get the address of the value to be accessed on top of stack
            self.tokeniser.getCurrentToken() ##skipping over ']'
            self.tokeniser.getCurrentToken() ##skipping over '='
            self.compileExpression() ##Compuile RHS expression
            self.vmWriter.writePop("temp", 0) ##getting RHS value to be assgined in temp
            self.vmWriter.writePop("pointer", 1) ##getting array address to be modigied in RAM[THAT]
            self.vmWriter.writePush("temp", 0) ##getting the RHS valuue back to stack 
            self.vmWriter.writePop("that", 0) ##updateing the array valye 
            self.tokeniser.getCurrentToken() ##skip over ';'
        ##now solving for normal varName case:
        else:
            if self.tokeniser.currentToken in self.subroutineSymbolTable.table:
                segmentName =  "local" if self.subroutineSymbolTable.table[self.tokeniser.currentToken]["kind"] == "VAR" else "argument"
                index = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["index"]
            else:
                segmentName =  "static" if self.classSymbolTable.table[self.tokeniser.currentToken]["kind"] == "STATIC" else "this"
                index = self.classSymbolTable.table[self.tokeniser.currentToken]["index"]
            self.tokeniser.getCurrentToken() ##skipping over 'varName'
            self.tokeniser.getCurrentToken() ##skipping over '='
            self.compileExpression() ##geting the expression value on top of the stack 
            self.vmWriter.writePop(segmentName, index=index)
            self.tokeniser.getCurrentToken() ##skip over ';'




    """
    Signature: 
    Purpose: 
        Compiles an if statement , possibl with a trailing else clause
        Corresponding Jack Grammar rule:
            - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    Execution:
        generate two labels L1 and L2 to be used 
        Skip over 'if', and '(' and then compileExpression
        Negate compileExpression and generateLabel for else statement
        'if-goto' <label> to jump to else statement
        skip over ')' '{' and compile statements inside the if block
        generate label2 and 'goto' label2 and then 'label L1'
        skip over '}' and see if there is 'else' available, if yes then skip over '{' 'compileStatements()' and skip over '}'
        If else not available 'label L2' and skip over ')'
        
    """
    def compileIf(self):
        label1 = self.generateLabel()
        label2 = self.generateLabel()
        self.tokeniser.getCurrentToken() ##skip over if
        self.tokeniser.getCurrentToken() ##skip over '('
        self.compileExpression() ##compiling expression
        self.vmWriter.writeArithemetic("not") ##Negating the expression
        self.vmWriter.writeIf(label1)
        self.tokeniser.getCurrentToken() ##skip over ')'
        self.tokeniser.getCurrentToken() ##skip over '{'
        self.compileStatements()
        self.vmWriter.writeGoto(label2)
        self.tokeniser.getCurrentToken() ##skip over '}'
        self.vmWriter.writeLabel(label1) ##generating label for the else branch
        if self.tokeniser.currentToken == "else":
            self.tokeniser.getCurrentToken() ##skip over 'else' 
            self.tokeniser.getCurrentToken() ##skip over '{'
            self.compileStatements()
            self.tokeniser.getCurrentToken() ##skip over '}'
        self.vmWriter.writeLabel(label2) ## generating label for l2
        




    """
    Signature: 
    Purpose: 
        Compiles a while statement
        Corresponding Jack Grammar rule:
            - whileStatement: 'while' '(' expression ')' '{' statements '}'
    Execution:
        generate two labels L1 and L2 to be used 
        skip over 'while' and '(' and then compileExpression
        push 'neg' to the commandList and then push "if-goto L2"  
        skip  over ')' and '{' and then compileStatements and then push 'goto Label1'  and then 'label L2'
        And then finall skip over '}'

    """
    def compileWhile(self):
        label1 = self.generateLabel()
        label2 = self.generateLabel()
        self.vmWriter.writeLabel(label1) ##setting up label for the loop
        self.tokeniser.getCurrentToken() ##skip over 'while'
        self.tokeniser.getCurrentToken() ##skip over '('
        self.compileExpression()
        self.vmWriter.writeArithemetic("not") ##Negating the expression
        self.vmWriter.writeIf(label2) ##sending this to label2, basically loop ends 
        self.tokeniser.getCurrentToken() ##skip over ')'
        self.tokeniser.getCurrentToken() ##skip over '{'
        self.compileStatements()
        self.vmWriter.writeGoto(label1)
        self.vmWriter.writeLabel(label2) ##Continue executing after the loop
        self.tokeniser.getCurrentToken() ##skip over '}'

    """
    Signature: 
    Purpose: 
        Compiles a do statement
        Corresponding Jack Grammar rule:
            - doStatement: 'do' subroutineCall ';'
    Execution:
        skip over 'do'
        Use compileExpression()
        Use command "pop temp 0" to remove the top stack value
    """
    def compileDo(self):
        self.tokeniser.getCurrentToken() ##skip over 'do'
        self.compileExpression() ##treat subroutine call as an expression call
        self.vmWriter.writePop("temp", 0) ##Removing the top of stack value
        self.tokeniser.getCurrentToken()  #  skip over ';'
 

    """
    Signature: 
    Purpose: 
        Compiles a return statement
        Corresponding Jack Grammar rule:
            - returnStatement: 'return' expression? ';'
    Execution:
        We skip over return, then check if we have an expression
        If expression, we call compileExpression
            - if it is "this" - for constructor, we will use "push pointer 0"
        If no expression, we still need to push 0 to stack 
        Post which we call vmWrite.writeReturn, and then skip over semicolon
    """
    def compileReturn(self):
        self.tokeniser.getCurrentToken() ##to skip over "return" keyword
        if self.tokeniser.currentToken != ";":
            if self.tokeniser.currentToken == "this":
                self.vmWriter.writePush("pointer", 0)
                self.tokeniser.getCurrentToken() ##to move forward beyond 'this'
            else:
                self.compileExpression()
        else:
            self.vmWriter.writePush("constant", 0) ##if no expression, we will still push null to the top of the stack
        self.vmWriter.writeReturn()
        self.tokeniser.getCurrentToken() ##to skip over ";" symbol


    """
    Signature: 
    Purpose: 
        Compiles an Expression
        Corresponding Jack Grammar rule:
            - term (op term)*
    Execution:
        - Call compileTerm() on the first term
        - If currentToken is a symbol:
            - Call compileTerm() on second term
            - If op  not in [*, /] - use writeArithemetic from vmWriter as per Symbol
            - if * use call Math.multiply 2, if / use call Math.divide 2
    """
    def compileExpression(self):
        self.compileTerm()
        while self.tokeniser.currentToken in ['+' , '-' , '*' , '/' , '&' , '|' , '<' , '>' , '=']:
            opInstruction = self.tokeniser.getCurrentToken()
            self.compileTerm()
            if opInstruction not in ['*', '/']:
                self.vmWriter.writeArithemetic(self.opDict[opInstruction])
            elif opInstruction == '*':
                self.vmWriter.writeCall("Math.multiply", 2)
            elif opInstruction == '/':
                self.vmWriter.writeCall("Math.divide", 2)



    """
    Signature: 
    Purpose: 
        Compiles a term, if the current token is an identifier, the routine must resolve it into a variable , an array element, or a subroutinecall
        A single lookahead token , which may be [, (, . suffices to distinguish between the possibilities
        An other token is not part of this term and should not be advanced over
        Corresponding Jack Grammar rule:
            - term: integerConstant - DONE | stringConstant - DONE | keywordConstant  | varName - DONE | varName '[' expression ']' - DONE | '(' expression ')' - DONE| (unaryOp term) - DONE| subroutineCall
            - subroutineCall: subroutineName '(' expressionList ')' - DONE | (className | varName) '.' subroutineName '(' expressionList ')' - DONE
    Exeuction: Direclty implemeted in code, too long
        
        
    """
    def compileTerm(self):
        if self.tokeniser.currentTokenIndex + 1 < len(self.tokeniser.finalTokenList):
            nextToken = self.tokeniser.finalTokenList[self.tokeniser.currentTokenIndex+1][0]
        else:
            nextToken = ""
        ##Solving for array
        if nextToken == "[":
 
            if self.tokeniser.currentToken in self.subroutineSymbolTable.table:
                segmentName =  "local" if self.subroutineSymbolTable.table[self.tokeniser.currentToken]["kind"] == "VAR" else "argument"
                index = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["index"]
            else:
                segmentName =  "static" if self.classSymbolTable.table[self.tokeniser.currentToken]["kind"] == "STATIC" else "this"
                index = self.classSymbolTable.table[self.tokeniser.currentToken]["index"]
            self.vmWriter.writePush(segmentName, index=index) ##this will get address of array on heap on the global stack
            self.tokeniser.getCurrentToken() ##skip over varName
            self.tokeniser.getCurrentToken() ##skip over '['
            self.compileExpression() 
            self.vmWriter.writeArithemetic("add") ##to get the address of the value to be accessed on top of stack
            self.vmWriter.writePop("pointer", 1) ##get address to RAM[5]
            self.vmWriter.writePush("that", 0)#access value *(this)
            self.tokeniser.getCurrentToken() ##skip over ']'

        ##Solving for a function call
        elif nextToken == "(": ##to process subroutine call of type function(expressionlist)
            functionName = self.tokeniser.filename[0:-5] + "." + self.tokeniser.getCurrentToken()
            self.tokeniser.getCurrentToken()  ##skip over '('
            nArgs = self.compileExpressionList() ##will put n expressions on stack, plus will return the no. of expressions
            self.vmWriter.writeCall(functionName, nArgs=nArgs)
            self.tokeniser.getCurrentToken() ##skip over the final ')'
        ##Solving for constructor or method call
        elif nextToken == ".": ##to process method or constructor call
            ##case of constructor
            if self.subroutineSymbolTable.kindOf(self.tokeniser.currentToken) is None and self.classSymbolTable.kindOf(self.tokeniser.currentToken) is None:
                className = self.tokeniser.getCurrentToken() 
                self.tokeniser.getCurrentToken() ##skip over. '.'
                funcName = self.tokeniser.getCurrentToken() 
                self.tokeniser.getCurrentToken() ##skip over. '('
                nArgs = self.compileExpressionList() ##solving for expressions passed as arguments, each expressions to be put up at the top of the stack
                funcName = className + "." + funcName
                self.vmWriter.writeCall(funcName, nArgs)
                self.tokeniser.getCurrentToken() ##skip over. ')'
            ##case of method call
            else:
                if self.tokeniser.currentToken in self.subroutineSymbolTable.table:
                    className = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["type"]
                    segmentName =  "local" if self.subroutineSymbolTable.table[self.tokeniser.currentToken]["kind"] == "VAR" else "argument"
                    index = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["index"]
                else:
                    className = self.classSymbolTable.table[self.tokeniser.currentToken]["type"]
                    segmentName =  "static" if self.classSymbolTable.table[self.tokeniser.currentToken]["kind"] == "STATIC" else "this"
                    index = self.classSymbolTable.table[self.tokeniser.currentToken]["index"]
                self.vmWriter.writePush(segmentName, index=index) ##getting the address of the oibject as the first argument 
                self.tokeniser.getCurrentToken() ##skip over. '.'
                funcName = self.tokeniser.getCurrentToken()
                funcName = className + "." + funcName
                self.tokeniser.getCurrentToken() ##skip over. '('
                nArgs = self.compileExpressionList()
                nArgs = nArgs + 1 ##As we are passing n+1 args , 1 for the object itself
                self.vmWriter.writeCall(funcName, nArgs)
                self.tokeniser.getCurrentToken() ##skip over. ')'

        ##solving for '('expression')'
        elif self.tokeniser.currentToken == "(": ##this is for the case when we have '('expression')'
            self.tokeniser.getCurrentToken() ##skip over '('
            self.compileExpression()
            self.tokeniser.getCurrentToken() ##skip over ')'
        elif self.tokeniser.currentToken in ["~", "-"]: ##this is for the case when term is op type (unaryOp term)
            op = self.tokeniser.getCurrentToken() ##get the op and store it
            self.compileTerm() ##willl get expression value.on top of the stack
            if op == "~":
                self.vmWriter.writeArithemetic("not")
            else:
                self.vmWriter.writeArithemetic("neg")

        ##solving for string constant
        elif self.tokeniser.tokenType() == "stringConstant":
            stringConstant = self.tokeniser.currentToken
            lenString = len(stringConstant)
            self.vmWriter.writePush("constant", lenString)
            self.vmWriter.writeCall("String.new", 1)  # String.new takes 1 arg (the length)
            for ch in stringConstant:
                self.vmWriter.writePush("constant", ord(ch))
                self.vmWriter.writeCall("String.appendChar", 2)  # object + char
            self.tokeniser.getCurrentToken()

        ##solving for varName
        elif self.tokeniser.currentToken in self.subroutineSymbolTable.table or self.tokeniser.currentToken in self.classSymbolTable.table:
            if self.tokeniser.currentToken in self.subroutineSymbolTable.table:
                segmentName =  "local" if self.subroutineSymbolTable.table[self.tokeniser.currentToken]["kind"] == "VAR" else "argument"
                index = self.subroutineSymbolTable.table[self.tokeniser.currentToken]["index"]
            else:
                segmentName =  "static" if self.classSymbolTable.table[self.tokeniser.currentToken]["kind"] == "STATIC" else "this"
                index = self.classSymbolTable.table[self.tokeniser.currentToken]["index"]
        
            self.vmWriter.writePush(segmentName, index=index) ##this will get address of array on heap on the global stack
            self.tokeniser.getCurrentToken() #skipping over the varName
        
        ##solving for intConstant
        elif self.tokeniser.tokenType() =="intConstant":
            self.vmWriter.writePush("constant", int(self.tokeniser.currentToken))
            self.tokeniser.getCurrentToken() #move beyond the intConstant
        
        ##solving for keywordConstant
        else:    
            if self.tokeniser.currentToken == "true":
                self.vmWriter.writePush("constant", 1)
                self.vmWriter.writeArithemetic("neg")
            elif self.tokeniser.currentToken in ["false", "null"]:
                self.vmWriter.writePush("constant", 0)
            elif self.tokeniser.currentToken == "this":
                self.vmWriter.writePush("pointer", 0)
            self.tokeniser.getCurrentToken() ##move forward and get the next token

        

    """
    Signature: 
    Purpose: 
        
        Compiles a (possibly empty) comma separated list of expressions , returns number of expressions in the list
        Corresponding Jack Grammar rule:
            - expressionList: (expression (',' expression)*)?
        
    """
    def compileExpressionList(self):
        counter = 0
        if self.tokeniser.currentToken != ")":
            self.compileExpression()
            counter = 1
            while self.tokeniser.currentToken == ",":
                self.tokeniser.getCurrentToken() ##skip over ,
                self.compileExpression()
                counter += 1
        return counter




