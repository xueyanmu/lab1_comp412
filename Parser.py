from Scanner import Scanner
from Tokens import Tokens

class Parser:
    def __init__(self):
        #line num, opcode, op1, op2, op3
        #self.IR = IR()
        #self.newIR = ['', '', [], [], []]
        self.parsedTokens = []
        self.currToken = 10
        self.scanner = Scanner()
        self.tokens = Tokens()
        self.pointer = 0
        self.lineNum = 1
        self.fullLine = ''
        #self.queue = []
        self.totalLines = 0
        self.errorExists = False
        self.FIRST_SET = [0, 1, 2, 3, 4, 9, 11]
        self.errorSet = [-1, -2, None]
        self.numILOC = 0

    def inFirstSet(self, tokenType):
        if tokenType in self.FIRST_SET:
            return True
        return False

    #@profile
    def parseLine(self):
        #self.lineNum = lineNum
        # #self.scanner = Scanner()
        #self.scanner.setLineNum(lineNum)
        #self.pointer = self.scanner.pointer
        #self.fullLine = line
        self.currToken = self.scanner.scanNextWord(self.fullLine)
        try:
            # print("in first set" + str(self.currToken))
            if self.inFirstSet(self.currToken[0]):
                try:
                #ARITHOP
                    if self.currToken[0] == 2:
                        #self.newIR[0] = self.lineNum
                        #self.newIR[1] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        self.currToken = self.scanner.scanNextWord(self.fullLine)

                        if self.currToken[0] == 6:
                            #self.newIR[2] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)

                            if self.currToken[0] == 7:
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                #self.pointer = self.scanner.getPointer()
                                
                                if self.currToken[0] == 6:
                                    #self.newIR[3] = self.currToken[2]
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                                                            
                                    if self.currToken[0] == 8:
                                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                                        
                                        if self.currToken[0] == 6:
                                            #self.newIR[4] = self.currToken[2]
                                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                                            #self.pointer = self.scanner.getPointer()
                                            if self.currToken[0] == 11 or self.currToken in self.errorSet:
                                                #self.queue.append(self.newIR)
                                                self.numILOC += 1
                                                if self.currToken[0] == 11:
                                                    return 11
                                                return True
                                            else:
                                                self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                        else:
                                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                                    else:
                                        self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "COMMA")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                    #MEMOP
                    elif self.currToken[0] == 0:
                        #self.newIR[0] = self.lineNum
                        #self.newIR[1] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        #print(self.IR[1])
                        #MEMOP
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0] == 6: #register
                            #self.newIR[2] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            #self.pointer = self.scanner.getPointer()
                            if self.currToken[0] == 8: #into
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                #self.pointer = self.scanner.getPointer()
                                if self.currToken[0] == 6: #register
                                    #self.newIR[3] = self.currToken[2]
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                    #self.pointer = self.scanner.getPointer()
                                    if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                                        #self.queue.append(self.newIR)
                                        #print(self.linkedIRs)
                                        self.numILOC += 1
                                        if self.currToken[0] == 11:
                                            return 11
                                        return True
                                    else:
                                        self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                
                    #LOADI
                    elif self.currToken[0] == 1:
                        #self.newIR[0] = self.lineNum
                        #self.newIR[1] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        if self.currToken[0] == 5: #constant
                            #self.newIR[2] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            if self.currToken[0] == 8: #into
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                if self.currToken[0] == 6: #register
                                    #self.newIR[3] = self.currToken[2]
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                    #self.pointer = self.scanner.getPointer()
                                    if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                                        self.queue.append(self.newIR)
                                        # self.IR = ['', '', [], [], []]
                                        self.numILOC += 1

                                        if self.currToken[0] == 11:
                                            return 11
                                        return True
                                    else:
                                        self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                                else:
                                    self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")
                            else:
                                self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "INTO")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")

                    #OUTPUT
                    elif self.currToken[0] == 3:
                        #self.newIR[0] = self.lineNum
                        #self.newIR[1] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        #MEMOP
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0] == 5: #constant
                            #self.newIR[2] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            if self.currToken[0]==11 or self.currToken in self.tokens.errorSet or self.scanner.getPointer() == len(self.fullLine):
                                #self.queue.append(self.newIR)
                                self.numILOC += 1
                                if self.currToken[0] == 11:
                                    return 11
                                return True
                            else:
                                self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")

                    #NNOP
                    elif self.currToken[0] == 4:
                        #self.newIR[0] = self.lineNum
                        #self.newIR[1] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                            self.numILOC += 1
                            #self.queue.append(self.newIR)
                            if self.currToken[0] == 11:
                                return 11
                            return True
                        else:
                            self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                        

                    #EOF
                    elif self.currToken[0] == 9:
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0] == 10:
                            return True
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "EOF")
                    
            
                except Exception as error:
                    self.errorExists = True
                    #self.queue = []
                    arrDontThrowError = [12, 11, 10, 9, -1, -2, None]
                    if self.currToken[0] not in arrDontThrowError:
                        print("ERROR: Parsing Error: " + self.fullLine[self.pointer] +" at line: " + str(self.lineNum) + " and character position: " + str(self.pointer))

            else: #toekn not in first set
                if self.currToken[0] == 12: #ignore comments
                    return
                elif self.currToken[0] == 10: #ignore lexeme error since scanner prints error
                    return
                else:
                    self.errorExists = True
                    #self.queue = []
                    self.parserErrorTerminal("Operation starts with an invalid opcode: %s." % self.currToken[1])

        except:
                pass

    def parserErrorNonTerminal(self, msg):
        self.errorExists = True
        #self.queue = []
        print( 'ERROR: %i: %s' % (self.lineNum, msg))


    def parserErrorTerminal(self, msg):
        self.errorExists = True
        #self.queue = []
        if self.currToken == None:
            print("ERROR: Missing token at line " + str(self.lineNum))
        elif self.currToken not in self.tokens.errorSet and self.currToken[0] not in self.tokens.errorSet:
            print('ERROR: %i: %s' % (self.lineNum, msg))
            
    def setLineNumber(self, lineNum):
        self.lineNum = lineNum
        
    def getLinkedIRs(self):
        return self.queue

    def getIR(self):
        return self.newIR
        
    def getErrorExists(self):
        return self.errorExists
    