from collections import deque


class Scanner():
    def __init__(self):
        # self.filename = filename
        self.nextLine = ""
        self.nextChar = ""
        self.stateError = False
        self.nextLineNum = 0
        self.tokenType = ""
        self.charPos = 0
        self.lexeme = ""
        self.stateError = -1
        self.ERROR = -2
        

        # End State #
        self.se = -1
        #Store the stream of tokens
        self.tokens = deque()

        #store strings as integers
        self.tokenTypeStringTable = [None for i in range(11)]
        self.tokenTypeStringTable[0] = "MEMOP"
        self.tokenTypeStringTable[1] = "LOADI"
        self.tokenTypeStringTable[2] = "ARITHOP"
        self.tokenTypeStringTable[3] = "OUTPUT"
        self.tokenTypeStringTable[4] = "NOP"
        self.tokenTypeStringTable[5] = "CONSTANT"
        self.tokenTypeStringTable[6] = "REGISTER"
        self.tokenTypeStringTable[7] = "COMMA"
        self.tokenTypeStringTable[8] = "INTO"
        self.tokenTypeStringTable[9] = "EOF"
        self.tokenTypeStringTable[10] = "EOL"

    # def readFile(self):
    #     with open(self.filename) as f:
    #         # readlines = f.read() 
    #         # readlines += "\n EOF"
    #         # print(readlines)
    #         # print(len(readlines))


    #         arrayOfLines = f.readlines()
    #         # print(arrayOfLines)
    #         arrayOfLines.append("\n EOF")
    #         # print(arrayOfLines)

    #         for line in arrayOfLines:
    #             self.nextLine = line
    #             print("self.nextLine: ", self.nextLine)
    #             if self.nextLine == '\n EOF':
    #                 print("poggy woggy")
                    
    #                 self.EOF = True
    #                 self.nextChar = self.EOF
    #                 print("self.nextChar: ", self.nextChar)
    #             self.scanNextWord()
            

    """
    Function is called by scanNextWord() 
    Therefore, it should handle EOL, EOF, and Space
    EOL: eat up the characters
    EOF: return the token
    Space: ???
    """
    def scanNextChar(self):
        try :
            self.nextChar = self.nextLine[0]
            self.nextLine = self.nextLine[1:]
        except IndexError: #TODO: this wont always be a an EOF related error, so catch more 
            self.stateError = True
            self.nextChar = self.stateError
            print("Error with reading in character")

        if self.nextChar == '\n' or self.nextChar == '\r': #TODO: how do we handle a carraige return and do we ned to handle /r/n
            self.charPos = 0
            self.nextLineNum += 1



        if self.nextChar == self.stateError:
            self.stateErrorHandler()

        elif self.nextChar != self.stateError and self.nextChar != '\n' and self.nextChar != '\r':
            #default case
            self.charPos += 1
            self.lexeme += self.nextChar
   

    def scanNextLine(self):
        self.nextLine = self.filename.readline()

    def resetCharPos(self):
        self.charPos = 0
        pass
  
    def stateErrorHandler(self):
        
        return self.tokenType, self.lexeme

    def peekNextChar(self):
        try:
            return self.nextLine[0]
        except IndexError:
            return self.stateError


#try to return a <token, lexeme> pair
    def scanNextWord(self, currLine):
        self.lexeme = ""
        self.nextLine = currLine
        print("self.nextLine: ", self.nextLine)
        print("=====================================")

        self.scanNextChar()

        print("self.nextChar", self.nextChar)
        print("=====================================")


        # handle each character until the End of File
        while self.nextChar != self.stateError: #TODO: THIS IS EOL CASE
            # use these to move placeholders for charPos and lineNum
            if self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r':
                #eat whitespace, tab, newline chars
                self.scanNextChar()
                continue

            if self.nextChar == 's':
                self.handleS()
            if self.nextChar == 'l':
                self.handleL()
            if self.nextChar == 'r':
                self.handleR()
            if self.nextChar == 'm':
                self.handleM()
            if self.nextChar == 'a':
                self.handleA()
            if self.nextChar == 'n':
                self.handleN()
            if self.nextChar == 'n':
                self.handleN()
            if self.nextChar == 'o':
                self.handleO()
            if self.nextChar == '=':
                self.handleEquals()
            if self.nextChar == ',':
                self.handleComma()

            numsToChars = [str(i) for i in range(10)]
            if self.nextChar in numsToChars:
                self.handleNums()

            if self.nextChar == '/':
                self.handleSlash()
            else:
                print("error with scanning word in beginning")
                break
        
        return self.tokenType, self.lexeme
        

    def handleS(self):
        self.scanNextChar()
        if self.nextChar == 't':
            self.scanNextChar()
            if self.nextChar == 'o':
                self.scanNextChar()
                if self.nextChar == 'r':
                    self.scanNextChar()
                    if self.nextChar == 'e':
                            self.tokenType = "MEMOP"
                            self.lexeme = "store"
                            return self.tokenType, self.lexeme
                    else:
                        print("error with scanning word")
                        pass
                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass

        elif self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'b':
                self.tokenType = "ARITHOP"
                self.lexeme = "sub"
                return self.tokenType, self.lexeme

            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass


    def handleL(self):
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'a':
                self.scanNextChar()
                if self.nextChar == 'd':
                    if self.peekNextChar() != 'I':
                        self.tokenType = "MEMOP"
                        self.lexeme = "load"
                        return self.tokenType, self.lexeme
                    else:
                        self.scanNextChar()
                        if self.nextChar == 'I':
                                self.tokenType = "LOADI"
                                self.lexeme = "loadI"
                                return self.tokenType, self.lexeme

                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
        elif self.nextChar == 's':
            self.scanNextChar()
            if self.nextChar == 'h':
                self.scanNextChar()
                if self.nextChar == 'i':
                    self.scanNextChar()
                    if self.nextChar == 'f':
                        self.scanNextChar()
                        if self.nextChar == 't':
                                self.tokenType = "ARITHOP"
                                self.lexeme = "lshift"
                                return self.tokenType, self.lexeme

                        else:
                            print("error with scanning word")
                            pass
                    else:
                        print("error with scanning word")
                        pass
                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass
    def handleR(self):
        self.scanNextChar()
        if self.nextChar == 's':
            self.scanNextChar()
            if self.nextChar == 'h':
                self.scanNextChar()
                if self.nextChar == 'i':
                    self.scanNextChar()
                    if self.nextChar == 'f':
                        self.scanNextChar()
                        if self.nextChar == 't':
                            self.tokenType = "ARITHOP"
                            self.lexeme = "rshift"
                            return self.tokenType, self.lexeme

                        else:
                            print("error with scanning word")
                            pass
                    else:
                        print("error with scanning word")
                        pass
                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass

        # HANDLE REGISTERS #
        self.scanNextChar()
        numsToChars = [str(i) for i in range(10)]
        if self.nextChar in numsToChars:
            self.handleNums()
            # we are done with the word bc handleNums() will end the word
            self.token = "REG"
            self.lexeme = "r" + self.lexeme
            return self.token, self.lexeme
            
    def handleM(self):
        self.scanNextChar()
        if self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'l':
                self.scanNextChar()
                if self.nextChar == 't':
                        self.tokenType = "ARITHOP"
                        self.lexeme = "mult"
                        return self.tokenType, self.lexeme

                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass

    def handleA(self):
        self.scanNextChar()
        if self.nextChar == 'd':
            self.scanNextChar()
            if self.nextChar == 'd':
                    self.tokenType = "ARITHOP"
                    self.lexeme = "add"
                    return self.tokenType, self.lexeme

            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass
    def handleN(self):
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'p':

                    self.tokenType = "NOP"
                    self.lexeme = "nop"
                    return self.tokenType, self.lexeme

            else:
                print("error with scanning word")
                pass
    def handleO(self):
        self.scanNextChar()
        if self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 't':
                self.scanNextChar()
                if self.nextChar == 'p':
                    self.scanNextChar()
                    if self.nextChar == 'u':
                        self.scanNextChar()
                        if self.nextChar == 't':
                                self.tokenType = "OUTPUT"
                                self.lexeme = "output"
                                return self.tokenType, self.lexeme

                        else:
                            print("error with scanning word")
                            pass
                    else:
                        print("error with scanning word")
                        pass
                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass
    def handleEquals(self):
        self.scanNextChar()
        if self.nextChar == '>':
                self.tokenType = "INTO"
                self.lexeme = "="
                return self.tokenType, self.lexeme

        else:
            print("error with scanning word")
            pass
    def handleComma(self):
            self.tokenType = "COMMA"
            self.lexeme = ","
            return self.tokenType, self.lexeme
        

    def isCharAnInt(self, char):
        numsToChars = [str(i) for i in range(10)]
        if char in numsToChars:
            return True
        else:
            return False

    def handleNums(self):
        self.scanNextChar()
        globalNum = 0
        if self.isCharAnInt(self.nextChar):

            if self.nextChar < '0' or self.nextChar > '9':
                print ("error with scanning number")
                pass
            else:
                num = 0
                while self.nextChar >= '0' and self.nextChar <= '9':
                    self.scanNextChar()
                    num = num * 10 + int(self.nextChar)
                globalNum = num
        else:
            self.tokenType = "CONSTANT"
            self.lexeme = str(globalNum)
            return self.tokenType, self.lexeme

    def handleSlash(self):
        print("self.nextChar is: ", self.nextChar)
        self.scanNextChar()
        if self.nextChar == '/':
            self.scanNextChar()
            while self.nextChar != '\n' and self.nextChar != '\r':
            
                if self.nextChar == '\n' or self.nextChar == '\r':
                    break
                else:
                    self.scanNextChar()

            self.tokenType = "COMMENT"
            return self.tokenType, self.lexeme

    def getLexeme(self):
        return self.lexeme
    def getCharPos(self):
        return self.charPos
    def getLineNum(self):
        return self.nextLineNum
    def getToken(self):
        return self.tokenType
