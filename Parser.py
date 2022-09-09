from Scanner import Scanner
from Tokens import Tokens

class Parser:
    def __init__(self):
        self.IR = []
        self.parsedTokens = []
        self.currToken = 10
        self.scanner = Scanner()
        self.tokens = Tokens()
        self.pointer = 0
        self.lineNum = 1
        self.fullLine = ''
    
    #@profile
    def parseLine(self, line):
        self.scanner.setLineNum(self.lineNum)
        self.pointer = self.scanner.getPointer() #todo: maybe dont function call this
        self.fullLine = line
        #chwck w piazza this is stored corectly
        #check time library 
        self.currToken = self.scanner.scanNextWord(self.fullLine)
        
        try:
            # print("in first set" + str(self.currToken))
            if self.tokens.inFirstSet(self.currToken[0]):
                try:
                    #ARITHOP
                    if self.currToken[0] == 2:
                        #ARITHOP   
                        if self.accept(2):
                            #print("accept arithop " + str(self.currToken))
                            if self.accept(6):
                                #print("accept reg " + str(self.currToken))
                                if self.accept(7):
                                    #print("accept comma " + str(self.currToken))
                                    if self.accept(6):
                                        #print("accept reg " + str(self.currToken))
                                        if self.accept(8):
                                            #print("accept into " + str(self.currToken))
                                            if self.accept(6):
                                                #print("accept reg " + str(self.currToken))
                                                if self.accept(11) or self.currToken in self.tokens.errorSet:
                                                    return True
                                                # elif self.accept(11): #eol
                                                #     #print("accept EOL " + str(self.currToken))
                                                #     return True
                                                else:
                                                    #print(self.scanner.getLineNum())
                                                    self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                            else:
                                                #print(self.scanner.getLineNum())
                                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                                        else:
                                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                                    else:
                                        self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "COMMA")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "ARITHOP")

                    #EOL
                    elif self.currToken[0] == 11:
                        #EOL
                        if self.accept(11):
                            #print("accept eol " + str(self.currToken))
                            return True
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "EOL")

                    #MEMOP
                    elif self.currToken[0] == 0:
                        #MEMOP
                        if self.accept(0): #load or store
                            #print("accept load or store " + str(self.currToken))
                            if self.accept(6): #register
                                #print("accept reg " + str(self.currToken))
                                if self.accept(8): #into
                                    #print("accept into " + str(self.currToken))
                                    if self.accept(6): # register
                                        #print("accept reg " + str(self.currToken))
                                        #print("peeepee" + self.currToken)
                                        if self.accept(11) or self.currToken in self.tokens.errorSet:
                                            
                                            return True
                                        # elif self.accept(11): #eol
                                        #     #print("accept EOL " + str(self.currToken))
                                        #     return True
                                        else:
                                            self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                    else:
                                        self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "LOAD or STORE")

                    #LOADI
                    elif self.currToken[0] == 1:
                        if self.accept(1):
                            #print("accept loadi " + str(self.currToken))
                            if self.accept(5):
                                #print("accept number " + str(self.currToken))
                                if self.accept(8):
                                    #print("accept into " + str(self.currToken))
                                    if self.accept(6):
                                        #print("accept reg " + str(self.currToken))
                                        if self.accept(11) or self.currToken in self.tokens.errorSet or self.currToken[0] in self.tokens.errorSet or self.currToken[0] == 10:
                                            return True
                                        # elif self.accept(11): #eol
                                        #     #print("accept EOL " + str(self.currToken))
                                        #     return True
                                        else:
                                            self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                    else:
                                        self.parserErrorNonTerminal(": Wrong or missing token type - expected REG")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INT")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "LOADI")

                    #OUTPUT
                    elif self.currToken[0] == 3:
                        if self.accept(3):
                            if self.accept(5):
                                if self.accept(11) or self.currToken in self.tokens.errorSet:
                                    return True
                                else:
                                    self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "CONSTANT")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "OUTPUT")

                    #NOP
                    elif self.currToken[0] == 4:
                        if self.accept(4):
                            #print("accept nop " + str(self.currToken))
                            if self.accept(11) or self.currToken in self.tokens.errorSet:
                                #print("2 peeepee" + self.currToken)
                                return True
                            # elif self.accept(11): #eol
                            #     #print("accept EOL " + str(self.currToken))
                            #     return True
                            else:
                                self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "NOP")

                    #EOF
                    elif self.currToken[0] == 9:
                        if self.accept(10):
                        #print("accept eof " + str(self.currToken))
                            return True
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "EOF")
                
                except Exception as error:
                    arrDontThrowError = [12, 11, 10, 9, -1, -2, None]
                    if self.currToken[0] not in arrDontThrowError:
                        print("ERROR: Parsing Error at line: " + str(self.lineNum) + " and character position: " + str(self.pointer))

            else: #toekn not in first set
                if self.currToken[0] == 12: #ignore comments
                    return
                elif self.currToken[0] == 10: #ignore lexeme error since scanner prints error
                    return
                else:
                    self.parserErrorTerminal("Operation starts with an invalid opcode: %s." % self.currToken[1])
                
        except:
            pass

    #@profile
    def accept(self, token):
        try:
            self.pointer = self.scanner.getPointer()
            #print("acceptance of token: "+str(self.currToken) +" at pointer position: " + str(self.pointer))
            if self.currToken[0] == token:
                # self.currToken = self.scanner.scanNextWord(self.fullLine[self.pointer:])
                self.currToken = self.scanner.scanNextWord(self.fullLine)
                self.pointer = self.scanner.getPointer()
                return True
            else:
                return False
        except Exception as error:
            print("ERROR: Error with accepting token: " + token + " at line: " + str(self.lineNum) + " pointer: " + str(self.pointer))
            return False


    # memop is load and store, it is followed by a register
    def handleMEMOP(self): 
        #print("load")
        #print("curr token " + str(self.currToken))
        if self.accept(0): #load or store
            #print("accept load or store " + str(self.currToken))
            if self.accept(6): #register
                #print("accept reg " + str(self.currToken))
                if self.accept(8): #into
                    #print("accept into " + str(self.currToken))
                    if self.accept(6): # register
                        #print("accept reg " + str(self.currToken))
                        #print("peeepee" + self.currToken)
                        if self.accept(11) or self.currToken in self.tokens.errorSet:
                            
                            return True
                        # elif self.accept(11): #eol
                        #     #print("accept EOL " + str(self.currToken))
                        #     return True
                        else:
                            self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                    else:
                        self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                else:
                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
            else:
                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "LOAD or STORE")


    # loadi is followed by a register and a number
    def handleLOADI(self):
        #print("loadi")
        if self.accept(1):
            #print("accept loadi " + str(self.currToken))
            if self.accept(5):
                #print("accept number " + str(self.currToken))
                if self.accept(8):
                    #print("accept into " + str(self.currToken))
                    if self.accept(6):
                        #print("accept reg " + str(self.currToken))
                        if self.accept(11) or self.currToken in self.tokens.errorSet or self.currToken[0] in self.tokens.errorSet or self.currToken[0] == 10:
                            return True
                        # elif self.accept(11): #eol
                        #     #print("accept EOL " + str(self.currToken))
                        #     return True
                        else:
                            self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                    else:
                        self.parserErrorNonTerminal(": Wrong or missing token type - expected REG")
                else:
                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
            else:
                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INT")
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "LOADI")


    def handleARITHOP(self):
        #print("arithop")
        if self.accept(2):
            #print("accept arithop " + str(self.currToken))
            if self.accept(6):
                #print("accept reg " + str(self.currToken))
                if self.accept(7):
                    #print("accept comma " + str(self.currToken))
                    if self.accept(6):
                        #print("accept reg " + str(self.currToken))
                        if self.accept(8):
                            #print("accept into " + str(self.currToken))
                            if self.accept(6):
                                #print("accept reg " + str(self.currToken))
                                if self.accept(11) or self.currToken in self.tokens.errorSet:
                                    return True
                                # elif self.accept(11): #eol
                                #     #print("accept EOL " + str(self.currToken))
                                #     return True
                                else:
                                    #print(self.scanner.getLineNum())
                                    self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                            else:
                                #print(self.scanner.getLineNum())
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                    else:
                        self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                else:
                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "COMMA")
            else:
                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "ARITHOP")

    def handleOUTPUT(self):
        if self.accept(3):
            if self.accept(5):
                if self.accept(11) or self.currToken in self.tokens.errorSet:
                    return True
                else:
                    self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
            else:
                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "CONSTANT")
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "OUTPUT")

    def handleNOP(self):
        #print("nop")
        #print("peeepee" + self.currToken)
        if self.accept(4):
            #print("accept nop " + str(self.currToken))
            if self.accept(11) or self.currToken in self.tokens.errorSet:
                #print("2 peeepee" + self.currToken)
                return True
            # elif self.accept(11): #eol
            #     #print("accept EOL " + str(self.currToken))
            #     return True
            else:
                self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "NOP")

    def handleComment(self):
        #print("comment")
        if self.accept(9):
            #print("accept comment " + str(self.currToken))
            return True
        # else:
        #     self.parserError(": Wrong or missing token type - expected %s" % "COMMENT")

    def handleEOF(self):
        #print("eof")
        if self.accept(10):
            #print("accept eof " + str(self.currToken))
            return True
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "EOF")
    
    def handleEOL(self):
        #print("eol")
        if self.accept(11):
            #print("accept eol " + str(self.currToken))
            return True
        else:
            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "EOL")

    # call these errors when you havent finished making an ILOC operation
    #this will include premature Nones, and missing tokens
    def parserErrorNonTerminal(self, msg):
        print( 'ERROR: %i: %s' % (self.lineNum, msg))
        #print >> sys.stderr, "On line "+ str(self.lineNum) + msg
        #return

    def parserErrorTerminal(self, msg):
        ##print(self.scanner.getLineNum())
        #print(self.currToken)
        #print(self.currToken not in self.tokens.errorSet)

        #the errors alredy covered in scanner are 10
        #the errors to ignore are -1, -2, and None
        #actually dont ignore None errors, they can determine is something is missing
        #print(self.currToken[0] not in self.tokens.errorSet)
        if self.currToken == None:
            print("ERROR: Missing token at line " + str(self.lineNum))
            
        elif self.currToken not in self.tokens.errorSet and self.currToken[0] not in self.tokens.errorSet:
            if self.currToken[0] != 11:
                #print("in here")
                print('ERROR: %i: %s' % (self.lineNum, msg))
                #print >> sys.stderr, "On line "+ str(self.lineNum) + msg
            
    def setLineNumber(self, lineNum):
        self.lineNum = lineNum
        