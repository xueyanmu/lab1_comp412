from copy import copy
from re import T
from Scanner import Scanner
from Tokens import Tokens
from collections import deque
from IR import IR
from DoublyLinkedList import DoublyLinkedList
from collections import deque
class Reader:
    def __init__(self):
         
        self.IR = IR(None)
        # self.newIR = ["Opcode", "SR", "VR", "PR", "NU", "SR", "VR", "PR", "NU", "SR", "VR", "PR", "NU", "INDEX", "PRINT"]

        self.newIR = [None for i in range(15)] #14 shits here
        self.newIR[14] = True

        self.parsedTokens = []
        self.currToken = 10
        self.scanner = Scanner()
        self.tokens = Tokens()
        self.pointer = 0
        self.lineNum = 1
        self.fullLine = ''
        self.dq = deque()
        self.totalLines = 0
        self.errorExists = False
        self.numErrors = 0
        self.doubleList = None
        self.numOps = 0
        self.maxSR = 0
        self.isStore = False
        self.doubleList = DoublyLinkedList()



    #@profile
    def parseLine(self, line, lineNum):
        self.newIR =  [None for i in range(15)]
        self.lineNum = lineNum
        self.currToken = 10
        self.scanner = Scanner()
        self.pointer = 0
        self.scanner.setLineNum(lineNum)
        #self.pointer = self.scanner.getPointer() #todo: maybe dont function call this
        self.fullLine = line
        self.currToken = self.scanner.scanNextWord(self.fullLine)
        try:
            #print("in first set" + str(self.currToken))
            if self.tokens.inFirstSet(self.currToken[0]):
                #print("beginning curr token = " + str(self.currToken))
                try:
                #ARITHOP
                    if self.currToken[0] == 2:
                        self.newIR[13] = self.lineNum
                        self.newIR[0] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        self.currToken = self.scanner.scanNextWord(self.fullLine)

                        if self.currToken[0] == 6:
                            # print("curr maxSR = " + str(self.maxSR) + ", new reg = " + str(self.currToken[2][1:]))
                            # print( "new reg = " + str(self.currToken[2][1:]))
                            # print("curr maxSR = " + str(self.maxSR))
                            # print("compare max = " + str(self.maxSR < int(self.currToken[2][1:])))
                            self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                            self.newIR[1] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)

                            if self.currToken[0] == 7:
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                #self.pointer = self.scanner.getPointer()
                                
                                if self.currToken[0] == 6:
                                    self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                                    self.newIR[5] = self.currToken[2]
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                                                            
                                    if self.currToken[0] == 8:
                                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                                        
                                        if self.currToken[0] == 6:
                                            self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                                            self.newIR[9] = self.currToken[2]
                                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                                            #self.pointer = self.scanner.getPointer()
                                            if self.currToken[0] == 11 or self.currToken in self.tokens.errorSet:
                                                
                                                #print(self.newIR)
                                                self.dq.append(self.newIR)
                                                
                                                self.numOps += 1
                                                # #self.doubleList.InsertToEnd(self.newIR)
                                                #self.IR = ['', '', [], [], []]
                                                

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
                        self.newIR[13] = self.lineNum
                        self.newIR[0] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        if self.newIR == "store":
                            self.isStore = True
                        #print(self.IR[1])
                        #MEMOP
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0] == 6: #register
                            self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                            self.newIR[1] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            #self.pointer = self.scanner.getPointer()
                            if self.currToken[0] == 8: #into
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                #self.pointer = self.scanner.getPointer()
                                if self.currToken[0] == 6: #register
                                    self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                                    if self.newIR[0] == "store":
                                        self.newIR[5] = self.currToken[2]
                                    else:
                                        self.newIR[9] = self.currToken[2]
                                    self.isStore = False
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                    #self.pointer = self.scanner.getPointer()
                                    if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                                        self.dq.append(self.newIR)
                                        self.numOps += 1
                                        #print(self.linkedIRs)
                                        #self.IR = ['', '', [], [], []]
                                        ##self.doubleList.InsertToEnd(self.newIR)
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
                        self.newIR[13] = self.lineNum
                        self.newIR[0] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        if self.currToken[0] == 5: #constant
                            self.newIR[1] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            if self.currToken[0] == 8: #into
                                self.currToken = self.scanner.scanNextWord(self.fullLine)
                                if self.currToken[0] == 6: #register
                                    self.maxSR = max(self.maxSR, int(self.currToken[2][1:]))
                                    self.newIR[9] = self.currToken[2]
                                    self.currToken = self.scanner.scanNextWord(self.fullLine)
                                    #self.pointer = self.scanner.getPointer()
                                    if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                                        self.dq.append(self.newIR)
                                        self.numOps += 1
                                        ##self.doubleList.InsertToEnd(self.newIR)
                                        # self.IR = ['', '', [], [], []]

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
                        self.newIR[13] = self.lineNum
                        self.newIR[0] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        #MEMOP
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0] == 5: #constant
                            self.newIR[1] = self.currToken[2]
                            self.currToken = self.scanner.scanNextWord(self.fullLine)
                            #self.pointer = self.scanner.getPointer()
                            if self.currToken[0]==11 or self.currToken in self.tokens.errorSet or self.scanner.getPointer() == len(self.fullLine):
                                # print("OUTPUT")
                                self.dq.append(self.newIR)
                                # print(self.newIR)
                                self.numOps += 1
                                #self.doubleList.InsertToEnd(self.newIR)
                                if self.currToken[0] == 11:
                                    return 11
                                return True
                            else:
                                self.parserErrorTerminal(": Wrong or missing token type - expected %s" % "no more tokens")
                        else:
                            self.parserErrorNonTerminal(": Wrong or missing token type - expected %s" % "REG")

                    #NNOP
                    elif self.currToken[0] == 4:
                        self.newIR[13] = self.lineNum
                        self.newIR[0] = self.tokens.getLexeme(self.currToken[0], self.currToken[1])
                        
                        self.currToken = self.scanner.scanNextWord(self.fullLine)
                        #self.pointer = self.scanner.getPointer()
                        if self.currToken[0]==11 or self.currToken in self.tokens.errorSet:
                            self.dq.append(self.newIR)
                            self.numOps += 1
                            #self.doubleList.InsertToEnd(self.newIR)
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
                    
                    
                    # print(self.newIR)
                    # if not self.errorExists:
                    #     print(self.newIR)
                    #     self.IR.addList(self.newIR)
                    #     print(self.newIR)
                except Exception as error:
                    self.newIR =  [None for i in range(15)]
                    self.errorExists = True
                    self.dq = []
                    arrDontThrowError = [12, 11, 10, 9, -1, -2, None]
                    if self.currToken[0] not in arrDontThrowError:
                        print("ERROR: Parsing Error: " + self.fullLine[self.pointer] +" at line: " + str(self.lineNum) + " and character position: " + str(self.pointer))

            else: #toekn not in first set
                self.newIR =  [None for i in range(15)]
                if self.currToken[1] == 12: #ignore comments
                    #print("comment")
                    # self.newIR =  [None for i in range(15)]
                    return
                elif self.currToken[0] == 10: #ignore lexeme error since scanner prints error
                    self.numErrors += 1
                    return
                else:
                    self.errorExists = True
                    self.numErrors += 1
                    print("self.numErrors = " + str(self.numErrors))
                    self.dq = []
                    self.parserErrorTerminal("Operation starts with an invalid opcode: %s." % self.currToken[1])

        except:
                pass

    def parserErrorNonTerminal(self, msg):
        
        #print("NT curr token = " + str(self.currToken))
        if self.currToken[1] == 12:
            return
        self.numErrors += 1
        self.errorExists = True
        self.dq = []
        print( 'ERROR: %i: %s' % (self.lineNum, msg))


    def parserErrorTerminal(self, msg):                
        #print("T curr token = " + str(self.currToken))
        if self.currToken[1] == 12:
            return
        self.numErrors += 1
        self.errorExists = True
        self.dq = []
        if self.currToken == None:
            print("ERROR: Missing token at line " + str(self.lineNum))
        elif self.currToken not in self.tokens.errorSet and self.currToken[0] not in self.tokens.errorSet:
            print('ERROR: %i: %s' % (self.lineNum, msg))
            
    def setLineNumber(self, lineNum):
        self.lineNum = lineNum
        
    def getLinkedIRs(self):
        return self.dq

    def getIR(self):

        return self.newIR
        
    def getErrorExists(self):
        return self.errorExists
    
    def display(self):
        self.doubleList.listprint()

    def parseFile(self, filename):
        try:
            f = open(filename, 'r')
        except:
            print("ERROR: Error occured when opening file: " + filename)
        #print("Reading file: " + filename)

        count = 1
        numErrors = 0
        numReads = 0
        parser = Reader()
        doubleList = DoublyLinkedList()
        parser.errorExists = False

        with open(filename) as f:
            for line in f:
                burp = parser.parseLine(line, count)
                # print(line)
                # print(parser.getIR()[0])
                if parser.getIR()[0]:  # and not parser.errorExists
                    cop = copy(parser.getIR())
                    doubleList.push(cop)
                    self.newIR =  [None for i in range(15)]
                    #print(cop)
                    numReads += 1
                
                

                # print(burp == 11)
                if burp == 11:  # 11 means there was a \r or \n detected, move on to next line
                    
                    count += 1
                    continue  # go to next line

                # self.newIR =  [None for i in range(15)]
                count += 1
        # if parser.getErrorExists(): print("ERROR: Error occured when reading file: " + filename)
        # else: 
        #print("SUCCESS: Read successful, finding " + str(numReads) + " ILOC operations")
        #doubleList.listprint(doubleList.head)
        numErrors = parser.numErrors
        #print("Number of lines with errors: " + str(numErrors))
        
        # while doubleList.head is not None:
        #     print(doubleList.head.item)
        #     doubleList.head = doubleList.head.next
        parser.doubleList = doubleList
        return doubleList, parser.numOps, numErrors, parser.maxSR

