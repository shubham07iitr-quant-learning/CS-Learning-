##This module will be responsible for creating the relevant parse Tree for the given tokeniser

"""
Type/Interpretation:
    This module will be taking in a tokensier object as one of its fields - which would have been processed completely (finalTokenList) fully updated
    It will also maintain a list of all the parsed tokens as self.parseList
    In terms of mechanics, when the object is created it will call __init__ method which will in turn call "compileClass" method which will update our self.parseList class
    Once compileClass method finishes , self.parseList will be completely updated
    Parsing will be done as per JackGrammar which is mentioned separately for each of the method calls
    We will not have compileMethod for the following rules:
        - type
        - className
        - subroutineName
        - varName
        - statement
        - subroutineCall
    These rules will be handled by the methods which use them directly
    Grammar rules which have not been described in the methods:
        - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        - unaryOp: '-' | '~'
        - keywordConstant: 'true' | 'false' | 'null' | 'this'
        - statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
        - className: identifier
        - subroutineName: identifier
        - varName: identifier
        - type: 'int' | 'char' | 'boolean' | className

"""


class Engine():
    """
    TEMPLATE:
        FIELDS:
            ...self.tokeniser: TOKENISER
            ...self.parseList: LIST
        METHODS:
            ...self.compileXXX (self)                           ...No return (Updates Parse List with the relevant XML files)
            ...self.compileExpressionList(self)                 ...Count of expressions passed as params: Int
            ...self.process(token: Str)                         ...No return (Updates Parse List with the relevant XML files)
    """

    ##----------------------------------------------------------------------------------------------------------------------------------------------------------------##
    """
    Signature: self, tokeniser: TOKENISER > No return, initialises our Engine
    Purpose:
        Initialises the tokeniser field to the input TOKENISER object, and initialises the parseList to be empty
        Calls on compileClass function on the first token from tokeniser field 
    """
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.parseList = []
        self.compileClass() ##This will be called on the first token

    
    """
    Signature: self, token: String
    Purpose: 
        Check if the current token matches that which is passed as argument while function call, if not raises a shyntax error
        If it matches, then method adds XML tag in our parseList against the corresponding category
    Example:
        If we call process('while'), then self.parseList gets the following added [...."<keyword> while </keyword>" ]

    """
    def process(self, str):
        if self.tokeniser.currentToken == str:
            tokenType = self.tokeniser.tokenType()
            tokenValue = self.tokeniser.getCurrentToken()
            self.parseList.append("<" + tokenType + "> " + tokenValue + " </" + tokenType + ">")
        else:
            raise ValueError("Passed string does not match the current token")

    ##Now we will write down all the compile Methods along with the corresponding Jack Grammar rules;


    """
    Signature: self > No return (only appends XML tags in our self.parseList)
    Purpose: 
        Compiles a complete Jack Class
        Corresponding Jack Grammar rule:
            - class: 'class' className '{' classVarDec* subroutineDec* '}'
        Will process the current token and update the parseList
    """
    def compileClass(self):
        self.parseList.append("<class>")
        self.process("class")
        self.process(self.tokeniser.currentToken)
        self.process("{")
        while self.tokeniser.currentToken in ("static", "field"):
            self.compileClassVarDec()
        ##Now let's call the compileSubRoutine() methods as many times as required
        while self.tokeniser.currentToken in ("constructor", "function", "method"):
            self.compileSubRoutine()
        self.process("}")
        self.parseList.append("</class>")


    """
    Signature: 
    Purpose: 
        Compiles a static variable declaration , or a field declaration
        Corresponding Jack Grammar rule:
            - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        Will process the current token and update the parseList
    """
    def compileClassVarDec(self):
        
        self.parseList.append("<classVarDec>")
        if self.tokeniser.currentToken == "static":
            self.process("static")
        elif self.tokeniser.currentToken == "field":
            self.process("field")
        else:
            raise ValueError("Syntax error, current token should be either static or field")
        self.process(self.tokeniser.currentToken) ##Simply passing the type in process method, as we dont have separate compile statement for type
        self.process(self.tokeniser.currentToken) ##Simply passing the varName in process method, as we dont have separate compile statement for varName
        while (self.tokeniser.currentToken != ";"):
            self.process(",")
            self.process(self.tokeniser.currentToken) ##passing varName to be processed
        self.process(";")
        self.parseList.append("</classVarDec>")

    """
    Signature: 
    Purpose: 
        Compiles a complete method, function, or constructor 
        Corresponding Jack Grammar rule:
            - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        Will process the current token and update the parseList
    """
    def compileSubRoutine(self):
        self.parseList.append("<subroutineDec>")
        if self.tokeniser.currentToken == "constructor":
            self.process("constructor")
        elif self.tokeniser.currentToken == "function":
            self.process("function")
        elif self.tokeniser.currentToken == "method":
            self.process("method")
        else:
            raise ValueError("Syntax error, current token should be either method or constructor or function")
        self.process(self.tokeniser.currentToken) ##Simply passing the void|type in process method, as we dont have separate compile statement for type
        self.process(self.tokeniser.currentToken) ##Simply passing the subRoutineName in process method, as we dont have separate compile statement for subRoutineName
        self.process("(")
        if self.tokeniser.currentToken != ")":
            self.compileParameterList()
        self.process(")")
        self.compileSubroutineBody()
        self.parseList.append("</subroutineDec>")

        



    """
    Signature: 
    Purpose: 
        Compiles a (possibly empty) param list, does not handle enclosing parenthesis tokens ( and )
        Corresponding Jack Grammar rule:
            - parameterList: ( (type varName) (',' type varName)* )?
        Will process the current token and update the parseList
        As per compileSubRoutine, if this method is called we know at least one param declaration exist 
    """
    def compileParameterList(self):
        self.parseList.append("<parameterList>")
        self.process(self.tokeniser.currentToken) ##processing type of variable declaration as we dont have separate compile for this
        self.process(self.tokeniser.currentToken) ##processing name of variable as we dont have separate compile for this
        while self.tokeniser.currentToken != ")":
            self.process(",")
            self.process(self.tokeniser.currentToken) ##processing type of variable declaration as we dont have separate compile for this
            self.process(self.tokeniser.currentToken) ##processing name of variable as we dont have separate compile for this
        self.parseList.append("</parameterList>")


    """co
    Signature: 
    Purpose: 
        Compiles a (possibly empty) param list, does not handle enclosing parenthesis tokens ( and )
        Corresponding Jack Grammar rule:
            - subroutineBody: '{' varDec* statements '}'
        Will process the current token and update the parseList
    """
    def compileSubroutineBody(self):
        self.parseList.append("<subroutineBody>")
        self.process("{")
        while self.tokeniser.currentToken == "var":
            self.compileVarDec()
        self.compileStatements()
        self.process("}")
        self.parseList.append("</subroutineBody>")
    """
    Signature: 
    Purpose: 
        Compiles a var Declaration
        Corresponding Jack Grammar rule:
            - varDec: 'var' type varName (',' varName)* ';'
        Will process the current token and update the parseList
    """
    def compileVarDec(self):
        self.parseList.append("<varDec>")
        self.process("var")
        self.process(self.tokeniser.currentToken)  ##type
        self.process(self.tokeniser.currentToken)  ##varName
        while self.tokeniser.currentToken != ";":
            self.process(",")
            self.process(self.tokeniser.currentToken)  ##varName
        self.process(";")
        self.parseList.append("</varDec>")


    """
    Signature: 
    Purpose: 
        Compiles a sequence of statements. Does not handle enclosing curly bracket tokens { and }
        Corresponding Jack Grammar rule:
            - statements: statement*
            - statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
        Will process the current token and update the parseList
    """
    def compileStatements(self):

        self.parseList.append("<statements>")
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
        self.parseList.append("</statements>")

    """
    Signature: 
    Purpose: 
        Compiles a let statement
        Corresponding Jack Grammar rule:
            - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        Will process the current token and update the parseList
    """
    def compileLet(self):
        self.parseList.append("<letStatement>")
        self.process("let")
        self.process(self.tokeniser.currentToken) ##processing varName as we dont have a compileStatement for this
        if self.tokeniser.currentToken == "[":
            self.process("[")
            self.compileExpression()
            self.process("]")
        self.process("=")
        self.compileExpression()
        self.process(";")
        self.parseList.append("</letStatement>")




    """
    Signature: 
    Purpose: 
        Compiles an if statement , possibl with a trailing else clause
        Corresponding Jack Grammar rule:
            - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        Will process the current token and update the parseList
    """
    def compileIf(self):
        pass
        self.parseList.append("<ifStatement>")
        self.process("if")
        self.process("(")
        self.compileExpression()
        self.process(")")
        self.process("{")
        self.compileStatements()
        self.process("}")
        if self.tokeniser.currentToken == "else":
            self.process("else")
            self.process("{")
            self.compileStatements()
            self.process("}")
        self.parseList.append("</ifStatement>")




    """
    Signature: 
    Purpose: 
        Compiles a while statement
        Corresponding Jack Grammar rule:
            - whileStatement: 'while' '(' expression ')' '{' statements '}'
        Will process the current token and update the parseList
    """
    def compileWhile(self):
        self.parseList.append("<whileStatement>")
        self.process("while")
        self.process("(")
        self.compileExpression()
        self.process(")")
        self.process("{")
        self.compileStatements()
        self.process("}")
        self.parseList.append("</whileStatement>")



    """
    Signature: 
    Purpose: 
        Compiles a do statement
        Corresponding Jack Grammar rule:
            - doStatement: 'do' subroutineCall ';'
        Will process the current token and update the parseList
    """
    def compileDo(self):
        self.parseList.append("<doStatement>")
        self.process("do")
        self.process(self.tokeniser.currentToken)  ##subroutineName or className/varName
        if self.tokeniser.currentToken == ".":
            self.process(".")
            self.process(self.tokeniser.currentToken)  ##subroutineName
        self.process("(")
        self.compileExpressionList()
        self.process(")")
        self.process(";")
        self.parseList.append("</doStatement>")

    """
    Signature: 
    Purpose: 
        Compiles a return statement
        Corresponding Jack Grammar rule:
            - returnStatement: 'return' expression? ';'
        Will process the current token and update the parseList
    """
    def compileReturn(self):
        self.parseList.append("<returnStatement>")
        self.process("return")
        if self.tokeniser.currentToken != ";":
            self.compileExpression()
        self.process(";")
        self.parseList.append("</returnStatement>")

    """
    Signature: 
    Purpose: 
        Compiles an Expression
        Corresponding Jack Grammar rule:
            - term (op term)*
        Will process the current token and update the parseList
    """
    def compileExpression(self):
        self.parseList.append("<expression>")
        self.compileTerm()
        while self.tokeniser.currentToken in ['+' , '-' , '*' , '/' , '&' , '|' , '<' , '>' , '=']:
            self.process(self.tokeniser.currentToken)
            self.compileTerm()
        self.parseList.append("</expression>")



    """
    Signature: 
    Purpose: 
        Compiles a term, if the current token is an identifier, the routine must resolve it into a variable , an array element, or a subroutinecall
        A single lookahead token , which may be [, (, . suffices to distinguish between the possibilities
        An other token is not part of this term and should not be advanced over
        Corresponding Jack Grammar rule:
            - term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | '(' expression ')' | (unaryOp term) | subroutineCall
            - subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        Will process the current token and update the parseList
    """
    def compileTerm(self):
        self.parseList.append("<term>")
        if self.tokeniser.currentTokenIndex + 1 < len(self.tokeniser.finalTokenList):
            nextToken = self.tokeniser.finalTokenList[self.tokeniser.currentTokenIndex+1][0]
        else:
            nextToken = ""
        if nextToken == "[":
            self.process(self.tokeniser.currentToken) ##Since we dont have compile method for varName
            self.process("[")
            self.compileExpression()
            self.process("]")
        elif nextToken == "(": ##to process subroutine call of type function(expressionlist)
            self.process(self.tokeniser.currentToken) ##since subroutineName does not have any compile Method
            self.process("(")
            self.compileExpressionList()
            self.process(")")
        elif nextToken == ".": ##to process method or constructor call
            self.process(self.tokeniser.currentToken) ##for varNamr or className
            self.process(".") 
            self.process(self.tokeniser.currentToken) ##for subroutineName
            self.process("(")
            self.compileExpressionList()
            self.process(")")
        elif self.tokeniser.currentToken == "(": ##this is for the case when we have '('expression')'
            self.process("(")
            self.compileExpression()
            self.process(")")
        elif self.tokeniser.currentToken in ["~", "-"]: ##this is for the case when term is op type (unaryOp term)
            self.process(self.tokeniser.currentToken)
            self.compileTerm()
        else: ##Case when term is either integerConstant | stringConstant | keywordConstant | varName
            self.process(self.tokeniser.currentToken)
        self.parseList.append("</term>")

        

    """
    Signature: 
    Purpose: 
        
        Compiles a (possibly empty) comma separated list of expressions , returns number of expressions in the list
        Corresponding Jack Grammar rule:
            - expressionList: (expression (',' expression)*)?
        Will process the current token and update the parseList
        We will use the number of commas + 1 as our number of Expressions in the list
    """
    def compileExpressionList(self):
        counter = 0
        self.parseList.append("<expressionList>")
        if self.tokeniser.currentToken != ")":
            self.compileExpression()
            counter = 1
            while self.tokeniser.currentToken == ",":
                self.process(",")
                self.compileExpression()
                counter += 1
        self.parseList.append("</expressionList>")
        return counter




