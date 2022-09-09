from collections import deque
from curses.ascii import isalnum, isalpha, isdigit
import time
import sys
import cProfile
# import line_profiler
class Scanner():
    def __init__(self):
        # self.filename = filename
        self.nextCharsInLine = ""
        self.nextChar = ""
        self.indexError = False
        self.nextLineNum = 0
        self.charPos = 0
        self.lexeme = ""

        self.reportError = False
        self.lexemeIndex = 0
        self.eolFlag = False

        self.indexError = False
        self.tokenType = None

        # End State #
        self.se = -1
        #Store the stream of tokens
        self.tokens = deque()

        #store strings as integers
        self.TOKENS = [None for i in range(13)]
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
        self.TOKENS[11] = ["EOL", "eol"]
        self.TOKENS[12] = ["COMMENT", "comment"]


    def getToken(self, tokenType, lexemeIndex):
        print("<" + self.TOKENS[tokenType][0] + ", '" + self.TOKENS[tokenType][lexemeIndex] + "'>")
        return self.TOKENS[tokenType][lexemeIndex]
    #@profile
    #@profile
    def scanNextChar(self):
        
        if self.nextCharsInLine != "":
            self.nextChar = self.nextCharsInLine[0]
            self.nextCharsInLine = self.nextCharsInLine[1:]
        else:
            try :
                self.nextChar = self.nextCharsInLine[0]
                self.nextCharsInLine = self.nextCharsInLine[1:]
            except:
                self.indexError = True
                self.nextChar = -1
                if self.nextCharsInLine != "" and self.nextChar != '':
                    self.unScanChar()
                else:
                    return self.handleNonSyntacticWords()

        if self.nextChar == ' ' or self.nextChar == '\t':
            self.lexeme += ' ' #maybe this will solve the number problem
            self.charPos += 1

        elif self.nextChar == '\n' or self.nextChar == '\r': #TODO: handle /r/n
            self.eolFlag = True
            self.charPos = 0
            self.nextLineNum += 1
            if self.nextCharsInLine != '':
                self.nextCharsInLine = self.nextCharsInLine[1:]
                
            #self.nextCharsInLine == ""
            # else:
            #     self.eolFlag = True
            #     self.charPos = 0
            #     self.nextLineNum += 1
            #     self.nextCharsInLine = self.nextCharsInLine[1:]


            # do we even need this? since the rest of the lines are being erased after this
            # peek = self.peekNextChar()
            # if peek == '\n' or peek == '\r':
            #     # get rid of the extra \n or \r
            #     self.nextCharsInLine = self.nextCharsInLine[1:]

        else:
        #elif self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != -1 and self.nextChar != '\t' and self.nextChar != ' ':
            #default case
            self.charPos += 1
            self.lexeme += self.nextChar

            # do we even need this? since the rest of the lines are being erased after this
            # peek = self.peekNextChar()
            # if peek == '\n' or peek == '\r':
            #     # get rid of the extra \n or \r
            #     self.nextCharsInLine = self.nextCharsInLin

    # handle everything with wrong syntax or extra chars. Trashes comments and error-giving lines
    def handleNonSyntacticWords(self):        
        peek = self.peekNextChar()
        if self.tokenType == 10:
            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))

            self.tokenType = 10
            self.lexemeIndex = 1
            #self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            
            self.nextLineNum += 1
            self.charPos = 0
            
            return self.tokenType, self.lexemeIndex
        if peek == ' ' or peek == '\t' or peek == '\n' or peek == '\r' or peek == '=' or peek == ',' or peek == '':
            if self.tokenType == None:
                self.scanNextChar()
            else:
                return self.tokenType, self.lexemeIndex

        elif self.indexError == True or self.nextChar == -1 or peek == '':
            if self.tokenType != -1 and self.lexemeIndex != -1:
                return self.tokenType, self.lexemeIndex
            else:
                return -1

        else:
            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))

            self.tokenType = 10
            self.lexemeIndex = 1
            #self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            
            self.nextLineNum += 1
            self.charPos = 0
            
            return self.tokenType, self.lexemeIndex


        # elif self.tokenType == 10:
        #     self.nextLineNum += 1
        #     self.charPos = 0
        #     self.lexemeIndex = 1
        #     ##self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: there is an invalid lexical error for the word '"+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)

        #     return self.tokenType, self.lexemeIndex
        # # check that the word is followed by a space or newline

        
        # theres a real lexical error here, so return an error token and trash the rest of the line
        #elif self.tokenType != 10:
    def peekNextChar(self):
        try:
            return self.nextCharsInLine[0]
        except IndexError:
            return ""

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
        
        

#try to return a <token, lexeme> pair
    #@profile
    def scanNextWord(self, currLine):
        self.lexeme = ""
        self.nextCharsInLine = currLine
        if self.eolFlag == True:
            self.eolFlag = False
            return 11, 1

        else:
            self.scanNextChar() #nextchar in error is going to be set to True
            numsToChars = [str(i) for i in range(10)]

            # handle each character until the End of File
            while not self.indexError: #TODO: THIS IS EOL CASE
                # use these to move placeholders for charPos and lineNum
                while self.nextChar == ' ' or self.nextChar == '\t':
                    self.scanNextChar()
                if self.nextChar == 'r':
                    return self.handleR()
                elif self.nextChar == ',':
                    return self.handleComma()
                elif self.nextChar == '=':
                    return self.handleEquals()
                elif self.nextChar == 'a':
                    return self.handleA()
                elif self.nextChar == 'l':
                    return self.handleL()
                elif self.nextChar in numsToChars:
                    return self.handleNums()
                elif self.nextChar == 's':
                    return self.handleS()
                elif self.nextChar == 'm':
                    return self.handleM()
                elif self.nextChar == '/':
                    self.handleSlash()
                elif self.nextChar == 'n':
                    return self.handleN()
                elif self.nextChar == 'o':
                    return self.handleO()
                elif self.nextChar == 'E':

                    return self.handleE()
                elif self.nextChar == '\n' or self.nextChar == '\r':
                    return 11, 1
                else: # avoid infinite loop
                    return self.handleNonSyntacticWords()
                
            if self.indexError:
                self.indexError = False
                return -1

    def handleE(self):
        self.scanNextChar()
        if self.nextChar == 'O':
            self.scanNextChar()
            if self.nextChar == 'F':
                return -2
            elif self.nextChar == 'L':
                self.tokenType = 11
                self.lexemeIndex = 1
                return self.tokenType, self.lexemeIndex
        else:
            self.tokenType = 10
            return self.handleNonSyntacticWords()
    
    def handleNonSyntacticNums(self):

        # while self.nextChar != '\n' and self.nextChar != '\r' and self.nextChar != ' ' and self.nextChar != ',':
        #     self.scanNextChar()
            
        self.tokenType = 10
        self.lexemeIndex = 1
        #self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: there is an invalid lexical error for the number "+ self.lexeme +"at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        
        self.nextLineNum += 1
        self.charPos = 0
        return self.tokenType, self.lexemeIndex

            
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
                        self.tokenType = 10
                        return self.handleNonSyntacticWords()
                else:
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()

        elif self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'b':
                self.tokenType = 2 #ARITHOP
                self.lexemeIndex = 2 #SUB
                return self.tokenType, self.lexemeIndex

            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
            return self.handleNonSyntacticWords()


    def handleL(self):
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'a':
                self.scanNextChar()
                if self.nextChar == 'd':
                    
                    if self.peekNextChar() == "I":
                        self.scanNextChar()
                        if self.nextChar == 'I':
                            self.tokenType = 1 #LOADI
                            self.lexemeIndex = 1 #LOADI
                            return self.handleNonSyntacticWords()
                    else:
                        self.tokenType = 0 #MEMOP
                        self.lexemeIndex = 2 #LOAD
                        return self.handleNonSyntacticWords()
                else:
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
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
                            self.tokenType = 10
                            return self.handleNonSyntacticWords()
                    else:
                        self.tokenType = 10
                        return self.handleNonSyntacticWords()
                else:
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
            return self.handleNonSyntacticWords()
    #@profile
    def handleR(self):
        self.scanNextChar()
        if self.nextChar.isdigit():
            while self.nextChar.isdigit():
                self.scanNextChar()

            # get rid of extra space
            if self.lexeme[-1].isdigit() == False:
                self.unScanChar()

            self.tokenType = 6
            self.lexemeIndex = 1

            #store the register name
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
                            self.tokenType = 10
                            return self.handleNonSyntacticWords()
                    else:
                        self.tokenType = 10
                        return self.handleNonSyntacticWords()
                else:
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
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
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
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
                self.tokenType = 10
                return self.handleNonSyntacticWords()

        else:
            print("in handleA else")
            self.tokenType = 10
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
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
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
                            self.tokenType = 10
                            return self.handleNonSyntacticWords()
                    else:
                        self.tokenType = 10
                        return self.handleNonSyntacticWords()
                else:
                    self.tokenType = 10
                    return self.handleNonSyntacticWords()
            else:
                self.tokenType = 10
                return self.handleNonSyntacticWords()
        else:
            self.tokenType = 10
            return self.handleNonSyntacticWords()


    def handleEquals(self):
        self.scanNextChar()
        if self.nextChar == '>':
                self.tokenType = 8 #INTO
                self.lexemeIndex = 1 #=>
                #self.charPos
                return self.tokenType, self.lexemeIndex


        else:
            self.tokenType = 10
            return self.handleNonSyntacticWords()

    def handleComma(self):
        self.tokenType = 7 #COMMA
        self.lexemeIndex = 1 #,
        return self.tokenType, self.lexemeIndex    

    def handleNums(self):
        self.scanNextChar()
        peek = self.peekNextChar()
        while str(self.nextChar).isdigit() and str(peek).isdigit():
            self.scanNextChar()

        # while self.lexeme[-1].isdigit() == False:
        #     self.unScanChar()
        #     self.lexeme = self.lexeme[:-1]
        if self.lexeme[-1].isdigit() == False:
            self.unScanChar()

        peek = self.peekNextChar()
        if peek.isalpha():
            self.tokenType = 10
            self.lexemeIndex = 1
            ##self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
            
        
        else:
            self.tokenType = 5 #CONSTANT
            self.lexemeIndex = 1

            self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
            
        return self.handleNonSyntacticWords()

    def handleSlash(self):
        self.scanNextChar()
        #print("slash self.nextChar is: ", self.nextChar)


        if self.nextChar == '/':
            self.tokenType = 12 #COMMENT
            self.lexemeIndex = 1
            # return self.tokenType, self.lexemeIndex

            self.indexError = True
            return -1
        else:
            self.tokenType = 10
            self.lexemeIndex = 1
            print("ERROR: the symbol " + self.lexeme + " uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
            ##self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        
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
    def setLineNum(self, line):
        self.nextLineNum = line

    @staticmethod
    def lexError(word, lineNo):
        print >> sys.stderr, "Lexical Error: %i: \"%s\" is not a valid word." % (lineNo, word)