##This module will be responsible for identifying tokens from the given jack code

"""
Type/interpretation:
    This module will be responsible for a <filename>.jack file and producing a list ok tuples of type (TokenName, TokenType)
    There are 5 categories/headers of tokens as expressed by Jack Grammar:
        - keyword: class | constructor | function | method | field | static | var | int | char | boolean | void | true | false | null | this | let | do | if | else | while | return 
        - symbol: { | } | ( | ) [ | ] | . | , | ; | + | - | * | / | & | '|' | < | > | = | ~
        - integerConstant: Decimal integer from 0..32767
        - stringConstant: "Sequence of characters not including double quotes or new line"
        - identifier: Sequence of letters, digits, and underscore ('_'), not starting with a digit

    Mechanics of this module will be as follows:
        - __init__ module would open the given .jack file and do readLines
        - Each space separated word will be added to a baseTokenList 
        - Then we will loop through each individual word and parse it into a separate token and token category using advance until we have more tokens
        - This token and category tuple can be added to FinalTokenList which will be utilised by our Engine.py module
"""
import re
class Tokeniser():
    """
    TEMPLATE
        FIELDS
        ...self.filename(Str)
        ...self.currentWordIndex(Int)
        ...self.currentTokenIndex(Int)
        ...self.baseWordList (List)
        ...self.finalTokenList (List)
        ...self.currentToken (Str)
        ...self.KeyWordList (List)
        ...self.SymbolList (List)
        METHODS
        ...self.__init(self, filename:Str)                       ...No return (initialises the object and the fields)
        ...self.hasMoreTokens(self)                              ...Boolean
        ...self.advance(self)                                    ...No return (Will update the FinalTokenList with the tuple of (Token, Category))
        ...self.tokenType(self, Token: Str)                      ...tokenType: Str
        ...self.getCurrentToken(self)                            ...currentToken: Str
        PRIVATE METHODS
        ...self.solveForSingleCommentAndNewLine(listfile: List)  ...finalList: List
        ...self.solveForMultiComment(listfile)                   ...finalList: List
        ...self.reconfigureStringConstant(listfile)              ...finalList: List
    """
    ##----------------------------------------------------------------------------------------------------------------------------------------------------------------##
    """
    Signature: filename: Str > No Return (only initialises our field variables)
    Purpose:
        Init method would be responsible for:
            - Reading file from the current folder based on the filename provided
            - Initialise baseWordList which will have the following thigns sorted:
                - newLine characters removed
                - Comments at beginning of line of type // to be removed
                - Comments at end of line of type // to be removed
                - Multi line comments at the start of the line of type /* sorted
                - Multi line comments at the end of the line of type /* sorted
                - Separate the remaining text based on spaces - however this will split text of the form "Shubham gupta survi" in 3 separate words
                - Rebuild the tokenList, by clubbing these separated words
            - First 3 points to be solved by the method 'self.solveForSingleCommentAndNewLine()'
            - Multi line comment to be solved by the method 'self.solveForMultiComment()'
            - And reconfiguring string constant to be solved by 'self.reconfigureStringConstant()' method
            - Create a TokenDict variable with mapping of all the standard keywords from our JACK language
            - Initialise the currentToken to 0, and finalTokenList to []
    """
    
    def __init__(self, filename):
        if filename[-5:] != ".jack":
            raise NameError("Please only input .jack file extensions")
        else:
            self.filename = filename      
            self.currentWordIndex = 0 ##Will be used by hasMoreTokens to check if we have reached the end of baseWordList
            self.currentTokenIndex = 0 ##initialising currentTokenIndex which will reference finalTokenList and will be used by Engine class to go through each token one by one
            self.baseWordList = []  ##initilaise the baseWordList
            self.finalTokenList = [] ##initilaise the finalTokenList
            self.currentToken = "" ##Defining a current token which will be used extensively by our compilationEngine, will be updated after we have built the list
            ##Now initialising the lists for keywords and symbols
            self.keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
            self.symbolList = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
            with open (self.filename) as file:
                listfile = file.readlines()
            
            ##Solving for single line comment and newline character
            listfile = self.solveForSingleCommentAndNewLine(listfile)
            ##solving for multi line comment 
            listfile = self.solveForMultiComment(listfile)
            ##Now lets split by spaces, each indiviudla element
            listfile =  " ".join(listfile).split()
            ##And finally reconfiguring split words
            self.baseWordList = self.reconfigureStringConstant(listfile)

    
#--------------------------------------PRIVATE FUNCTIONS TO SORT our baseWordList--------------------------------------------------------------------------------

    """
    Signature: self, listfile: List > List
    Purpose: 
        Removes lines that are purely newlines, strips trailing newline characters, 
        and removes inline // comments while preserving any code before the comment
    """
    def solveForSingleCommentAndNewLine(self, finalList):
        finalListFinal = []
        for i in finalList:
            matches =re.search(r"(.*)[/][/](.*)", i)
            if matches:
                first, last = matches.groups()
                if first.strip() != "":
                    finalListFinal.append(first.strip())
            elif i == "\n":
                continue
            elif i[-1:] == "\n":
                stripped = i[:-1].strip()
                if stripped != "":
                    finalListFinal.append(stripped)
            else:
                finalListFinal.append(i.strip())
        return finalListFinal
    

    """
    Signature: self, listfile: List > List
    Purpose: 
        Removes multi-line comments of type /* ... */ whether they span a single line 
        or multiple lines, while preserving any code before and after the comment block
    """

    def solveForMultiComment(self, finalList):
        finalListFinal = []
        checkForCloseComment = False
        for i in finalList:
            if checkForCloseComment:
                matches0 = re.search(r"(.*)[*][/](.*)", i)
                if matches0:
                    first0, last0 = matches0.groups()
                    if last0.strip() != "":
                        finalListFinal.append(last0.strip())
                    checkForCloseComment = False
                else:
                    continue
            ##Solving for case of type "shubham /*xxx*/ gupta" in a single line
            else:
                matches1 =re.search(r"(.*)[/][*](.*)[*][/](.*)", i)
                matches2 = re.search(r"(.*)[/][*](.*)", i)
                if matches1:
                    first, mid, last = matches1.groups()
                    if first.strip() != "":
                        finalListFinal.append(first.strip())
                    if last.strip() != "":
                        finalListFinal.append(last.strip())
                elif matches2:
                    first2, last2 = matches2.groups()
                    if first2.strip() != "":
                        finalListFinal.append(first2.strip())
                    checkForCloseComment = True
                else:
                    finalListFinal.append(i.strip())
        return finalListFinal
    """
    Signature: self, listfile: List > List
    Purpose: 
        Recombines space-separated words that belong to the same string constant, 
        stripping the enclosing double quotes, so that "hello world" becomes a single 
        element hello world instead of two separate elements
        """    
    def reconfigureStringConstant(self, listFinal):
        finalListFinal = []
        waitForConfigure = False
        reconfiguredWord = ""
        for i in listFinal:
            if waitForConfigure:
                quoteIndex = i.find('"')
                if quoteIndex != -1:
                    reconfiguredWord = reconfiguredWord + " " + i[:quoteIndex+1]
                    finalListFinal.append(reconfiguredWord)
                    remainder = i[quoteIndex+1:]
                    if remainder != "":
                        finalListFinal.append(remainder)
                    waitForConfigure = False
                    reconfiguredWord = ""
                else:
                    reconfiguredWord = reconfiguredWord + " " + i
            else:
                quoteIndex = i.find('"')
                if quoteIndex != -1:
                    before = i[:quoteIndex]
                    if before != "":
                        finalListFinal.append(before)
                    reconfiguredWord = i[quoteIndex:]
                    waitForConfigure = True
                else:
                    finalListFinal.append(i)
        return finalListFinal
    
    
    
    
    """
    Signature: Self > Boolean
    Purpose: 
        References the finalTokenList - and check if there are still tokens to be processed 
    """
    def hasMoreTokens(self):
        return self.currentWordIndex <= len(self.baseWordList) - 1

    """
    Signature: Self > No return (updates our finalTokenList data structure)
    Purpose:
        Takes in the current space separated word (based on self.currentWordIndex) from baseWordList , and updates the finalTokenList with the relevant tokens and corresponding category 
        Will also increment currenWordIndex after done processing
    Mechanics:
        - We notice that a single word in baseWordFinal could comprise of multiple tokens
        - For e.g. if it is x=(5+a); - it will have 8 tokens in a single word
        - So how do we decide , well we follow the following logic:
            - If we find the current word in our KeyWordList then we will just directly append it to our finalTokenList
            - If not, we will check if the word has any of the symbols as mentioned SymbolList, if yes then string before and after the symbol should be taken as separate tokens
            - If there are no symbols in the word, we will just identify it as:
                - stringConstant - if starts with " and ends with "
                - intConstant - if all chars in the string are integers
                - varName - if neither of the above

    Example
        If current word is "class": tokensiser.advance() > [...("class", "KEYWORD")] 
        If current word is "sum=35": tokensier.advance() > [...("sum", "IDENTIFIER"), ("=", "SYMBOL"), ("35", "INT_CONST")]
    """
    def advance(self):
        currentWord = self.baseWordList[self.currentWordIndex]
        if currentWord in self.keywordList:
            self.finalTokenList.append((currentWord, "keyword"))
        else:
            symbolIndexList = [] ##will store all the indices at which we have a 
            loopCounter = len(currentWord) 
            for i in range(loopCounter):
                if currentWord[i] in self.symbolList:
                    symbolIndexList.append(i)
            ##Now let's build all the tokens for us separated by symbols 
            listOfTokens = []
            if not symbolIndexList:
                listOfTokens = [currentWord]
            else:
                index1 = 0
                for i in symbolIndexList:
                    listOfTokens.append(currentWord[index1:i]) ##Appending either stringConstant,intConstant or varName
                    listOfTokens.append(currentWord[i]) ##Appending the symbol to the token list
                    index1 = i+1 ##So that next iteration works well
                ##And updating for hte last token
                listOfTokens.append(currentWord[symbolIndexList[-1]+1:]) ##Now we have all the tokens separated by symbols
                ##However one issue with listoftokens is if we don't have anything before a symbol or after the symbol like (x=1), then it will poduce empty tokens which must be taken care of
                listOfTokens = [t for t in listOfTokens if t != ""]
            ##Let's categorise each of these
            for i in listOfTokens:
                if i in self.symbolList:
                    self.finalTokenList.append((i, "symbol"))
                elif i in self.keywordList:
                    self.finalTokenList.append((i, "keyword"))
                elif i[0] == '"':
                    self.finalTokenList.append((i[1:-1], "stringConstant")) ##we skip the quotes
                else:
                    try:
                        intConstant = int(i)
                        if intConstant >= 0 and intConstant <= 32767:
                            self.finalTokenList.append((i, "intConstant"))
                        else:
                            raise ValueError("IntConstant cannot be more than 32767 or less than 0")
                    except:
                        self.finalTokenList.append((i, "varName"))

        ##After all this remember to increment the currentWordIndex for next advance 
        self.currentWordIndex = self.currentWordIndex + 1


    """
    Signature: self> tokenType: Str
    Purpose:
        Uses currentTokenIndex to reference finalTokenList and returns the second value from the tuple referenced by currentTokenIndex
    """
    def tokenType(self):
        return self.finalTokenList[self.currentTokenIndex][1]
    
    
    
    """
    Signature: self > currentToken: Str
    Purpose:
        Will be used by Engine to get the current token, when called uses currentTokenIndex to get 1st value from the tuple referenced by currentTokenIndex
        And when used will also update the currentTokenIndex to currentTokenIndex + 1
        And we will also update our current Token
    """
    
    def getCurrentToken(self):
        currentToken = self.currentToken
        self.currentTokenIndex = self.currentTokenIndex + 1
        if self.currentTokenIndex < len(self.finalTokenList):
            self.currentToken = self.finalTokenList[self.currentTokenIndex][0]
        return currentToken



    




