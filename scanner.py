from collections import deque
from curses.ascii import isalnum, isalpha, isdigit
from distutils.command.install_egg_info import to_filename


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
        self.reportError = False
        

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
    #         # #print(readlines)
    #         # #print(len(readlines))


    #         arrayOfLines = f.readlines()
    #         # #print(arrayOfLines)
    #         arrayOfLines.append("\n EOF")
    #         # #print(arrayOfLines)

    #         for line in arrayOfLines:
    #             self.nextLine = line
    #             #print("self.nextLine: ", self.nextLine)
    #             if self.nextLine == '\n EOF':
    #                 #print("poggy woggy")
                    
    #                 self.EOF = True
    #                 self.nextChar = self.EOF
    #                 #print("self.nextChar: ", self.nextChar)
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
            #print("Error with reading in character")

        if self.nextChar == '\n' or self.nextChar == '\r': #TODO: how do we handle a carraige return and do we ned to handle /r/n
            self.charPos = 0
            self.nextLineNum += 1
        # if self.nextChar == ' ':
        #     self.lexeme += self.nextChar
        #     self.charPos += 1

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
        # #print("self.nextLine: ", self.nextLine)
        # #print("=====================================")

        self.scanNextChar()

        # #print("self.nextChar", self.nextChar)
        # #print("=====================================")
        numsToChars = [str(i) for i in range(10)]

        # handle each character until the End of File
        while self.nextChar != self.stateError: #TODO: THIS IS EOL CASE
            # use these to move placeholders for charPos and lineNum
            while self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r':
                #eat whitespace, tab, newline chars
                self.scanNextChar()
                continue
            #print("back here")

            if self.nextChar == 's':
                return self.handleS()
            elif self.nextChar == 'l':
                return self.handleL()
            elif self.nextChar == 'r':
                return self.handleR()
            elif self.nextChar == 'm':
                return self.handleM()
            elif self.nextChar == 'a':
                return self.handleA()
            elif self.nextChar == 'n':
                return self.handleN()
            elif self.nextChar == 'n':
                return self.handleN()
            elif self.nextChar == 'o':
                return self.handleO()
            elif self.nextChar == '=':
                return self.handleEquals()
            elif self.nextChar == ',':
                return self.handleComma()

            
            elif self.nextChar in numsToChars:
                return self.handleNums()

            elif self.nextChar == '/':
                return self.handleSlash()

            else: # avoid infinite loop
                break
            

            # if self.tokenType != "INTO" or self.tokenType != "COMMA" or self.tokenType != "COMMENT":
            #     nextNextChar = self.peekNextChar()
            #     if self.tokenType == "CONSTANT":
            #         if nextNextChar.isdigit() == False:
            #             self.tokenType = "ERROR"
            #             self.lexeme = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            #             return self.tokenType, self.lexeme
            #     else:
            #         if nextNextChar != " " and nextNextChar != "\n" and nextNextChar != "\r":
            #             self.tokenType = "ERROR"
            #             self.lexeme = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            #             return self.tokenType, self.lexeme
                

            # else:
            #     #TODO: INSERT ERROR TOKEN
            #     self.tokenType = "ERROR"
            #     self.lexeme = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            #     break
                         
            # handle words with nonsyntactic characters
            # dont include numbers since it must take care of its error in its own function
            

             
        
        #return self.tokenType, self.lexeme

    def handleNonSyntacticWords(self):
        self.scanNextChar()
        #print(self.nextChar == ' ' or self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r')
        if self.nextChar.isspace() or self.nextChar == '\n' or self.nextChar == '\r':
            #print("in the right place in handle nonsynt")
            return self.tokenType, self.lexeme
        else:
            while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ':
                self.scanNextChar()
            self.tokenType = "ERROR"
            self.lexeme = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        self.nextChar = self.stateError

        return self.tokenType, self.lexeme
        # #print(self.nextChar)
        # #print(self.nextChar != " " and self.nextChar != "\n" and self.nextChar != "\r")
        # if self.nextChar != " " and self.nextChar != "\n" and self.nextChar != "\r":
        #     self.tokenType = "ERROR"
        #     self.lexeme = "ERROR: there is an invalid syntax error for the word at line " + str(self.nextLineNum) + " and position " + str(self.charPos) +". The incorrect word is: " + self.lexeme

            
        # else:
        #     return self.tokenType, self.lexeme


    def handleNonSyntacticNums(self):

        while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ' and self.nextChar != ',':
            self.scanNextChar()
            
        self.tokenType = "ERROR"
        self.lexeme = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        return self.tokenType, self.lexeme
        # if self.peekNextChar() != " " and self.peekNextChar() != "\n" and self.peekNextChar() != "\r" and self.peekNextChar().isdigit() == False:
        #     self.tokenType = "ERROR"
        #     self.lexeme = "ERROR: there is an invalid syntax error for the number at line " + str(self.nextLineNum) + " and position " + str(self.charPos) +". The incorrect number is: " + self.lexeme
        #     while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ' and self.nextChar.isdigit() == False:
        #         self.scanNextChar()
            
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
                        return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()

        elif self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'b':
                self.tokenType = "ARITHOP"
                self.lexeme = "sub"
                return self.tokenType, self.lexeme

            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()


    def handleL(self):
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'a':
                self.scanNextChar()
                if self.nextChar == 'd':
                    self.tokenType = "MEMOP"
                    self.lexeme = "load"
                    if self.peekNextChar() == "I":
                        self.scanNextChar()
                        if self.nextChar == 'I':
                            self.tokenType = "LOADI"
                            self.lexeme = "loadI"
                            ##print(self.handleNonSyntacticWords())
                            return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    #print("error with scanning word")
                    pass
            else:
                #print("error with scanning word")
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
                            #print("error with scanning word")
                            pass
                    else:
                        #print("error with scanning word")
                        pass
                else:
                    #print("error with scanning word")
                    pass
            else:
                #print("error with scanning word")
                pass
        else:
            #print("error with scanning word")
            pass
    def handleR(self):
    
        self.scanNextChar()
        if self.nextChar.isdigit():
            while self.nextChar.isdigit():
                self.scanNextChar()

            if self.lexeme[-1].isdigit():
                self.tokenType = "REG"
                return self.tokenType, self.lexeme
            else:
                self.unScanChar()

                self.tokenType = "REG"
                return self.tokenType, self.lexeme
            
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
                            self.lexeme = "rshift"
                            return self.tokenType, self.lexeme

                        else:
                            #print("error with scanning word")
                            pass
                    else:
                        #print("error with scanning word")
                        pass
                else:
                    #print("error with scanning word")
                    pass
            else:
                #print("error with scanning word")
                pass

        else:
            return self.handleNonSyntacticWords()
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
                    #print("error with scanning word")
                    pass
            else:
                #print("error with scanning word")
                pass
        else:
            #print("error with scanning word")
            pass

    def handleA(self):
        self.scanNextChar()
        if self.nextChar == 'd':
            self.scanNextChar()
            if self.nextChar == 'd':
                    self.tokenType = "ARITHOP"
                    self.lexeme = "add"
                    return self.handleNonSyntacticWords()

            else:
                return self.handleNonSyntacticWords()

        else:
            return self.handleNonSyntacticWords()


    def handleN(self):
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'p':

                    self.tokenType = "NOP"
                    self.lexeme = "nop"
                    return self.tokenType, self.lexeme

            else:
                #print("error with scanning word")
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
                            #print("error with scanning word")
                            pass
                    else:
                        #print("error with scanning word")
                        pass
                else:
                    #print("error with scanning word")
                    pass
            else:
                #print("error with scanning word")
                pass
        else:
            #print("error with scanning word")
            pass
    def handleEquals(self):
        self.scanNextChar()
        if self.nextChar == '>':
                self.tokenType = "INTO"
                self.lexeme = "=>"
                return self.tokenType, self.lexeme

        else:
            #print("error with scanning word")
            pass

        """
            def handleNonSyntacticWords(self):
        self.scanNextChar()
        #print(self.nextChar == ' ' or self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r')
        if self.nextChar.isspace() or self.nextChar == '\n' or self.nextChar == '\r':
            #print("in the right place in handle nonsynt")
            return self.tokenType, self.lexeme
        else:
            while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ':
                self.scanNextChar()
            self.tokenType = "ERROR"
            self.lexeme = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        self.nextChar = self.stateError

        """
    def handleComma(self):
        #print("HANDLE COMMA")
        # if self.nextChar == ' ' or self.nextChar == 'r':
        #     self.tokenType = "COMMA"
        #     self.lexeme = ","
        #     return self.tokenType, self.lexeme
        # else:
        #     self.tokenType = "ERROR"
        #     self.lexeme = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        # self.nextChar = self.stateError
        self.tokenType = "COMMA"
        self.lexeme = ","
        return self.tokenType, self.lexeme
            #TODO: DECIDE HOW ERROR IS TRIGGERED HERE
        

    def handleNums(self):
        self.scanNextChar()
        
        while self.nextChar.isdigit():
            self.scanNextChar()
            
        # #print ("self.lexeme POWERPWERJ" + self.lexeme)
        
        if self.lexeme[-1].isdigit():
            self.tokenType = "CONSTANT"
            return self.tokenType, self.lexeme
        else:
            # #print("peeeee")
            # if self.lexeme.isalpha():
            #     self.tokenType = "ERROR"
            #     self.lexeme = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            #     self.nextChar = self.stateError
            # else: #TODO: if its a letter, then its an error but literally anything else is fine??
            # elif self.lexeme[-1] == "=": 
                self.unScanChar()
                self.tokenType = "CONSTANT"
                return self.tokenType, self.lexeme


        #     if self.nextChar.isdigit() == False:
        #         # self.tokenType = "ERROR"
        #         # self.lexeme = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        #         # return self.tokenType, self.lexeme
        #         return self.handleNonSyntacticNums()
        # self.tokenType = "CONSTANT"
        # return self.tokenType, self.lexeme

        # if self.lexeme[-1].isdigit():
        #     self.tokenType = "CONSTANT"
        #     self.lexeme = str(globalNum)
        #     return self.tokenType, self.lexeme

        # else:
        #     #print("ERROR WITH SCANNING NUMBER AT LINE " + str(self.nextLineNum)) + " AND POSITION " + str(self.charPos)
        #     #self.unScanChar()
        #     # self.tokenType = "CONSTANT"
        #     # return self.tokenType, self.lexeme
        #     self.tokenType = "ERROR"
        #     self.lexeme = "ERROR: there is an invalid syntax error at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        #     return self.tokenType, self.lexeme

        # self.scanNextChar()
        # globalNum = None

        # if self.nextChar < '0' or self.nextChar > '9':
        #         #print ("error with scanning number")
        #         pass
        # else:
        #     num = 0
        #     while self.nextChar >= '0' and self.nextChar <= '9' and self.isCharAnInt(self.nextChar):
        #         num = 10 * num + int(self.nextChar)
        #         globalNum = num
        #         self.scanNextChar()
                
        # self.tokenType = "CONSTANT"
        # if globalNum != None:
        #     self.lexeme = str(globalNum)
        # return self.tokenType, self.lexeme




    def unScanChar(self):
        self.reportError = True
        unScanThisChar = self.lexeme[-1]
        self.lexeme = self.lexeme[:-1]
        if self.nextChar == '\n' or self.nextChar == '\r':
            self.nextLineNum -= 1
            
        else:
            self.charPos -= 1
            self.nextLine = unScanThisChar + self.nextLine
        
        self.tokenType = "ERROR"
        # self.lexeme = "ERROR: there is an invalid syntax error at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        return self.tokenType, self.lexeme
        
        # if self.isCharAnInt(self.nextChar):

        #     if self.nextChar < '0' or self.nextChar > '9':
        #         #print ("error with scanning number")
        #         pass
        #     else:
        #         num = 0
        #         while self.nextChar >= '0' and self.nextChar <= '9':
        #             self.scanNextChar()
        #             num = num * 10 + int(self.nextChar)
        #         globalNum = num
        # else:
        #     self.tokenType = "CONSTANT"
        #     self.lexeme = str(globalNum)
        #     return self.tokenType, self.lexeme

    def handleSlash(self):
        # #print("self.nextChar is: ", self.nextChar)
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
