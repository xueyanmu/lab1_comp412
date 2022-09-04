from collections import deque
from curses.ascii import isalnum, isalpha, isdigit
#from distutils.command.install_egg_info import to_filename



class Scanner():
    def __init__(self):
        # self.filename = filename
        self.nextCharsInLine = ""
        self.nextChar = ""
        self.indexError = False
        self.nextLineNum = 0
        self.tokenType = 10 #default to error token
        self.charPos = 0
        self.lexeme = ""
        self.indexError = -1
        self.reportError = False
        self.lexemeIndex = 0

        # End State #
        self.se = -1
        #Store the stream of tokens
        self.tokens = deque()

        #store strings as integers
        self.TOKENS = [None for i in range(11)]
        self.TOKENS[0] = ["MEMOP", "store", "load"]
        self.TOKENS[1] = ["LOADI", "loadi"]
        self.TOKENS[2] = ["ARITHOP", "add", "sub", "mult", "lshift", "rshift"]
        self.TOKENS[3] = ["OUTPUT", "output"]
        self.TOKENS[4] = ["NOP", "nop"]
        self.TOKENS[5] = ["CONSTANT", 0]
        self.TOKENS[6] = ["REGISTER", ""] #needs to be followed by a number in handleR()
        self.TOKENS[7] = ["COMMA", ","]
        self.TOKENS[8] = ["INTO", "=>"]
        self.TOKENS[9] = ["EOF", "eof"]
        self.TOKENS[10] = ["ERROR", "error"]

    """
    Function is called by scanNextWord() 
    Therefore, it should handle EOL, EOF, and Space
    EOL: eat up the characters
    EOF: return the token
    Space: ???
    """
    def scanNextChar(self):
        self.indexError = False
        try :
            self.nextChar = self.nextCharsInLine[0]
            self.nextCharsInLine = self.nextCharsInLine[1:]

        except:
            # print("index error in scanNextChar")
            self.indexError = True
            self.nextChar = -1
            if self.nextCharsInLine != "" and self.nextChar != '':
                self.unScanChar()
    
        # if self.nextChar == '\t':
        #     self.charPos += 4
        #     #self.nextCharsInLine = self.nextCharsInLine[3:]
        if self.nextChar == ' ' or self.nextChar == '\t':
            self.charPos += 1
            #self.nextCharsInLine = self.nextCharsInLine[1:]

        if self.nextChar == '\n' or self.nextChar == '\r': #TODO: handle /r/n
            peek = self.peekNextChar()
            if peek == '\n' or peek == '\r':
                
                self.nextCharsInLine = self.nextCharsInLine[1:]
            self.charPos = 0
            self.nextLineNum += 1

        elif self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != -1 and self.nextChar != '\t' and self.nextChar != ' ':
            #default case
            self.charPos += 1
            self.lexeme += self.nextChar
  
        #print("nextChar: ", self.nextChar)
    def stateErrorHandler(self):
        #self.indexError = False
        print("in error function")
        #return -1
        print(self.nextCharsInLine)
        if self.nextCharsInLine == "" or self.nextChar == '': #-1 is EOL, -2 is EOF
            #if self.tokenType 
            return -1
        else:
            self.nextCharsInLine = self.nextCharsInLine[1:]  
            self.scanNextChar()

    # handle everything with wrong syntax or extra chars. Trashes comments and error-giving lines
    def handleNonSyntacticWords(self):

        self.scanNextChar()
        if self.indexError == True or self.nextChar == -1:
            if self.tokenType != -1 and self.lexemeIndex != -1:
                return self.tokenType, self.lexemeIndex
            else:
                return -1

        # check that the word is followed by a space or newline
        elif self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r' or self.nextChar == '\t' or self.nextChar == ',' or self.nextChar == '=':
            self.unScanChar()
        
        elif self.nextChar == ',':
            return self.tokenType, self.lexemeIndex
        
        # theres a real syntax error here, so return an error token and trash the rest of the line
        else:
            print("real syntax error with lexeme: " + self.lexeme)

            self.tokenType = 10
            self.lexemeIndex = 1
            self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            
            self.nextLineNum += 1
            self.charPos = 0

        #print("TOKENS: ", self.TOKENS[self.tokenType][self.lexemeIndex])
        return self.tokenType, self.lexemeIndex


    def peekNextChar(self):
        try:
            return self.nextCharsInLine[0]
        except IndexError:
            print ("Error with peeking the next character at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
            return self.indexError

    def unScanChar(self):
        # self.reportError = True
        unScanThisChar = self.lexeme[-1]
        self.lexeme = self.lexeme[:-1]
        if self.nextChar == '\n' or self.nextChar == '\r':
            peekNext = self.peekNextChar()
            if peekNext == '\n' or peekNext == '\r':
                self.nextChar = ''
            self.nextLineNum -= 1
            
        else:
            self.charPos -= 1
            self.nextCharsInLine = unScanThisChar + self.nextCharsInLine
            #print("we just unscanned char, next line is: ", self.nextCharsInLine)
        

#try to return a <token, lexeme> pair
    def scanNextWord(self, currLine):
        self.lexeme = ""
        self.nextCharsInLine = currLine
        # #print("self.nextLine: ", self.nextLine)
        # #print("=====================================")

        self.scanNextChar() #nextchar in error is going to be set to True
        #print("nextChar: ", self.nextChar)
        #print(self.indexError)
        # #print("self.nextChar", self.nextChar)
        # #print("=====================================")
        numsToChars = [str(i) for i in range(10)]

        # handle each character until the End of File
        while not self.indexError: #TODO: THIS IS EOL CASE
            # use these to move placeholders for charPos and lineNum
            while self.nextChar == ' ' or self.nextChar == '\n' or self.nextChar == '\r' or self.nextChar == '\t':
                #eat whitespace, tab, newline chars
                self.scanNextChar()
                continue
            #print("back here")
            #print("self.nextline: ", self.nextLine)

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
            elif self.nextChar == 'o':
                return self.handleO()
            elif self.nextChar == '=':
                return self.handleEquals()
            elif self.nextChar == ',':
                return self.handleComma()
            elif self.nextChar in numsToChars:
                return self.handleNums()
            elif self.nextChar == '/':
                print(self.nextCharsInLine)
                return self.handleSlash()
            elif self.nextChar == 'E':
                return self.handleE()
            else: # avoid infinite loop
                return self.handleNonSyntacticWords()
             
        if self.indexError:
            self.indexError = False
            return -1
        #return self.tokenType, self.lexeme



    def handleE(self):
        self.scanNextChar()
        if self.nextChar == 'O':
            self.scanNextChar()
            if self.nextChar == 'F':
                return -2
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()
    
    def handleNonSyntacticNums(self):

        # while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ' and self.nextChar != ',':
        #     self.scanNextChar()
            
        self.tokenType = 10
        self.lexemeIndex = 1
        self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: there is an invalid syntax error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        
        self.nextLineNum += 1
        self.charPos = 0
        return self.tokenType, self.lexemeIndex
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
                        self.tokenType = 0 #MEMOP
                        self.lexemeIndex = 1 #STORE
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
                self.tokenType = 2 #ARITHOP
                self.lexemeIndex = 2 #SUB
                return self.tokenType, self.lexemeIndex

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
                    self.tokenType = 0 #MEMOP
                    self.lexemeIndex = 2 #LOAD
                    if self.peekNextChar() == "I":
                        self.scanNextChar()
                        if self.nextChar == 'I':
                            self.tokenType = 1 #LOADI
                            self.lexemeIndex = 1 #LOADI
                            return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        elif self.nextChar == 's':
            self.scanNextChar()
            if self.nextChar == 'h':
                self.scanNextChar()
                if self.nextChar == 'i':
                    self.scanNextChar()
                    if self.nextChar == 'f':
                        self.scanNextChar()
                        if self.nextChar == 't':
                                self.tokenType = 2 #ARITHOP
                                self.lexemeIndex = 4 #LSHIFT
                                return self.handleNonSyntacticWords()

                        else:
                            return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()

    def handleR(self):
        self.scanNextChar()
        if self.nextChar.isdigit():
            while self.nextChar.isdigit():
                self.scanNextChar()

            # get rid of extra space
            if self.lexeme[-1].isdigit() == False:
                self.unScanChar()
            
            # if self.nextChar.isalpha:
            #     self.tokenType = 10
            #     self.lexemeIndex = 1
            #     self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            #     return self.tokenType, self.lexemeIndex

            self.tokenType = 6
            self.lexemeIndex = 1

            #store the register name
            print("register lexeme: " + self.lexeme)
            self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
            

            return self.tokenType, self.lexemeIndex
            # return self.handleNonSyntacticWords()

            
        elif self.nextChar == 's':
            self.scanNextChar()
            if self.nextChar == 'h':
                self.scanNextChar()
                if self.nextChar == 'i':
                    self.scanNextChar()
                    if self.nextChar == 'f':
                        self.scanNextChar()
                        if self.nextChar == 't':
                            self.tokenType = 2 #ARITHOP
                            self.lexemeIndex = 5 #RSHIFT
                            return self.handleNonSyntacticWords()

                        else:
                            return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()

    def handleM(self):
        self.scanNextChar()
        if self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'l':
                self.scanNextChar()
                if self.nextChar == 't':
                        self.tokenType = 2 #ARITHOP
                        self.lexemeIndex = 3 #MULT
                        return self.handleNonSyntacticWords()

                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()

    def handleA(self):
        self.scanNextChar()
        if self.nextChar == 'd':
            self.scanNextChar()
            if self.nextChar == 'd':
                self.tokenType = 2 #ARITHOP
                self.lexemeIndex = 1 #ADD
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
                self.tokenType = 4 #NOP
                self.lexemeIndex = 1 #NOP

                return self.tokenType, self.lexemeIndex
                #return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()

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
                                self.tokenType = 3 #OUTPUT
                                self.lexemeIndex = 1 #OUTPUT
                                return self.handleNonSyntacticWords()

                        else:
                            return self.handleNonSyntacticWords()
                    else:
                        return self.handleNonSyntacticWords()
                else:
                    return self.handleNonSyntacticWords()
            else:
                return self.handleNonSyntacticWords()
        else:
            return self.handleNonSyntacticWords()


    def handleEquals(self):
        self.scanNextChar()
        if self.nextChar == '>':
                self.tokenType = 8 #INTO
                self.lexemeIndex = 1 #=>
                return self.tokenType, self.lexemeIndex


        else:
            return self.handleNonSyntacticWords()

    def handleComma(self):
        self.tokenType = 7 #COMMA
        self.lexemeIndex = 1 #,
        return self.tokenType, self.lexemeIndex    

    def handleNums(self):
        self.scanNextChar()
        while str(self.nextChar).isdigit():
            self.scanNextChar()
        
        if self.lexeme[-1].isdigit() == False:
            self.unScanChar()

        self.tokenType = 5 #CONSTANT
        self.lexemeIndex = 1

        self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
        print("const lexeme: ", self.lexeme)
        
        
        return self.tokenType, self.lexemeIndex



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




        # self.tokenType = "ERROR"
        # self.lexeme = "ERROR: there is an invalid syntax error at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        # return self.tokenType, self.lexeme
        
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
        print("slash self.nextChar is: ", self.nextChar)
        self.scanNextChar()
        print("slash self.nextChar is: ", self.nextChar)


        if self.nextChar == '/':
            self.indexError = True
            return -1
        else:
            self.tokenType = 10
            self.lexemeIndex = 1
            self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        
            return self.tokenType, self.lexemeIndex
    def getLexeme(self):
        return self.lexeme
    def getCharPos(self):
        return self.charPos
    def getLineNum(self):
        return self.nextLineNum
    def getToken(self):
        return self.tokenType
    def incrementLineNum(self):
        self.nextLineNum += 1
    def resetCharPos(self):
        self.charPos = 0