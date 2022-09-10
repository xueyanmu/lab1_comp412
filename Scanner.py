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
        self.pointer = 0
        
        
        self.reportError = False
        self.lexemeIndex = 0
        self.eolFlag = False

        self.indexError = False
        self.tokenType = None, 0

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
    def scanNextChar(self):
        #print("charcter: " + self.nextCharsInLine[self.pointer:])
        #get the next char and move the pointer
        if self.pointer < len(self.nextCharsInLine):
            #print("there are next chars ")
            self.nextChar = self.nextCharsInLine[self.pointer]
            self.pointer += 1
            #print(self.nextCharsInLine[self.pointer:])
            #if self.nextChar == '\n' or self.nextChar == '\r':
                #print("IF STEnew line detected in scanner scannewchar") 
        # else:

        #     return -1, 0



                # if self.nextCharsInLine and self.nextChar != '':
                #     print("unscan char")
                #     #unscn char
                #     self.lexeme = self.lexeme[:-1]
                #     if self.nextChar == '\n' or self.nextChar == '\r':
                #         peekNext = ''
                #         if self.pointer < len(self.nextCharsInLine):
                #             peekNext = self.nextCharsInLine[self.pointer]
                        
                #         if peekNext == '\n' or peekNext == '\r':
                #             self.nextChar = ''
                        
                        
                #     else:
                #         self.pointer -= 1
                # else:
                #     return self.handleNonSyntacticWords()



        #TODO: THIS CN BE REMOVED EASILY, REFACTOR TOMORROW
        # if self.nextChar == '\n' or self.nextChar == '\r': #TODO: handle /r/n
        #     print("line num: " + str(self.nextLineNum))
        #     print("in the newline") 
        #     self.eolFlag = True #3

        self.lexeme += self.nextChar




    # handle everything with wrong syntax or extra chars. Trashes comments and error-giving lines
    def handleNonSyntacticWords(self):
        peek = ''
        if self.pointer < len(self.nextCharsInLine):
            peek = self.nextCharsInLine[self.pointer]
        #     #return self.nextCharsInLine[0]

        if self.tokenType == 10:
            #this error will be covered by the parser i guess
            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
            return 10, 1

        if peek == ' ' or peek == '\t' or peek == '\n' or peek == '\r' or peek == '=' or peek == ',' or peek == '':
            if self.tokenType == None:
                self.scanNextChar()
            else:
                return self.tokenType, self.lexemeIndex

        elif self.indexError == True or self.nextChar == -1 or peek == '':
            if self.tokenType != -1 and self.lexemeIndex != -1:
                return self.tokenType, self.lexemeIndex
            else:
                return -1, 0
        else:
            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
            self.tokenType = 10
            self.lexemeIndex = 1
            return 10, 1

    def unScanChar(self):

        self.lexeme = self.lexeme[:-1]
        # if self.nextChar == '\n' or self.nextChar == '\r':
        #     peekNext = ''
        #     if self.pointer < len(self.nextCharsInLine):
        #         peekNext = self.nextCharsInLine[self.pointer]
            
        #     if peekNext == '\n' or peekNext == '\r':
        #         self.nextChar = ''            
        # else:
        self.pointer -= 1

    #@profile
    def scanNextWord(self, currLine):
        
        self.lexeme = ""
        #print("curr line: " + currLine)
        self.nextCharsInLine = currLine
        
        if self.eolFlag == True:
            self.eolFlag = False
            return 11, 1
        # if self.eolFlag == "12312312": 
        #     pass
        # else:
        self.scanNextChar() #nextchar in error is going to be set to True
        numsToChars = [str(i) for i in range(10)]

        #print(self.pointer)
        #print(len(self.nextCharsInLine))
        #print(self.nextCharsInLine[self.pointer])
        if self.pointer >= len(self.nextCharsInLine):
            #print("here")
            return 11, 1
        while self.pointer < len(self.nextCharsInLine): 

            # use these to move placeholders for charPos and lineNum
            while self.nextChar == ' ' or self.nextChar == '\t':
                self.lexeme += ' '
                self.scanNextChar()

            if self.nextChar == 'r':
                self.scanNextChar()
                # if self.nextChar.isdigit():
                if self.nextChar <= '9' and self.nextChar >= '0':
                    while self.nextChar <= '9' and self.nextChar >= '0':
                        if self.nextCharsInLine:
                            self.nextChar = self.nextCharsInLine[self.pointer]
                            self.pointer += 1
                        if self.nextChar == '\n' or self.nextChar == '\r': #TODO: handle /r/n
                            self.eolFlag = True
                        else:
                            #default case
                            self.lexeme += self.nextChar

                    # get rid of extra space
                    if self.lexeme[-1].isdigit() == False:
                        self.lexeme = self.lexeme[:-1]
                        # if self.nextChar == '\n' or self.nextChar == '\r':
                        #     peekNext = ''
                        #     if self.pointer < len(self.nextCharsInLine):
                        #         peekNext = self.nextCharsInLine[self.pointer]
                            
                        #     if peekNext == '\n' or peekNext == '\r':
                        #         self.nextChar = '\n'
                        # else:
                        self.pointer -= 1
                    return 6, 1

                    
                elif self.nextChar == 's':
                    self.scanNextChar()
                    if self.nextChar == 'h':
                        self.scanNextChar()
                        if self.nextChar == 'i':
                            self.scanNextChar()
                            if self.nextChar == 'f':
                                self.scanNextChar()
                                if self.nextChar == 't':
                                    peek = ''
                                    if self.pointer < len(self.nextCharsInLine):
                                        peek = self.nextCharsInLine[self.pointer]
                                    if peek == ' ' or peek == '\t':
                                        return 2, 5

                                else:
                                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                                    
                                    return 10, 1
                            else:
                                print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                                
                                return 10, 1
                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                            
                            return 10, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
            
                    return 10, 1

            elif self.nextChar == ',':
                return 7, 1

            elif self.nextChar == '=':
                self.scanNextChar()
                if self.nextChar == '>':
                    return 8, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                    return 10, 1

            elif self.nextChar == 'a':
                self.scanNextChar()
                if self.nextChar == 'd':
                    self.scanNextChar()
                    if self.nextChar == 'd':
                        peek = ''
                        if self.pointer < len(self.nextCharsInLine):
                            peek = self.nextCharsInLine[self.pointer]
                        if peek == ' ' or peek == '\t':
                            return 2, 1

                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                    return 10, 1

            elif self.nextChar == 'l':
                self.scanNextChar()
                if self.nextChar == 'o':
                    self.scanNextChar()
                    if self.nextChar == 'a':
                        self.scanNextChar()
                        if self.nextChar == 'd':
                            peek = ''
                            if self.pointer < len(self.nextCharsInLine):
                                peek = self.nextCharsInLine[self.pointer]
                            if peek == "I":
                                self.scanNextChar()
                                if self.nextChar == 'I':
                                    # self.tokenType = 1 #LOADI
                                    # self.lexemeIndex = 1 #LOADI
                                    return 1, 1
                            else:
                                peek = ''
                                if self.pointer < len(self.nextCharsInLine):
                                    peek = self.nextCharsInLine[self.pointer]
                                if peek == ' ' or peek == '\t':
                                    return 0, 2
                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                            return 10, 1

                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                        return 10, 1
                elif self.nextChar == 's':
                    self.scanNextChar()
                    if self.nextChar == 'h':
                        self.scanNextChar()
                        if self.nextChar == 'i':
                            self.scanNextChar()
                            if self.nextChar == 'f':
                                self.scanNextChar()
                                if self.nextChar == 't':
                                    peek = ''
                                    if self.pointer < len(self.nextCharsInLine):
                                        peek = self.nextCharsInLine[self.pointer]
                                    if peek == ' ' or peek == '\t':
                                        return 2, 4

                                else:
                                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                                    return 10, 1
                            else:
                                print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                                return 10, 1
                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                            return 10, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                    return 10, 1

            elif self.nextChar in numsToChars:
                self.scanNextChar()
                peek = ''
                if self.pointer < len(self.nextCharsInLine):
                    peek = self.nextCharsInLine[self.pointer]
                while str(self.nextChar).isdigit() and str(peek).isdigit():
                    self.scanNextChar()
                if self.lexeme[-1].isdigit() == False:
                    self.unScanChar()

                peek = ''
                if self.pointer < len(self.nextCharsInLine):
                    peek = self.nextCharsInLine[self.pointer]
                if peek.isalpha():
                    self.tokenType = 10
                    self.lexemeIndex = 1
                else:
                    self.tokenType = 5 #CONSTANT
                    self.lexemeIndex = 1

                    self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
                return 5, 1

            elif self.nextChar == 's':
                self.scanNextChar()
                if self.nextChar == 't':
                    self.scanNextChar()
                    if self.nextChar == 'o':
                        self.scanNextChar()
                        if self.nextChar == 'r':
                            self.scanNextChar()
                            if self.nextChar == 'e':
                                peek = ''
                                if self.pointer < len(self.nextCharsInLine):
                                    peek = self.nextCharsInLine[self.pointer]
                                if peek == ' ' or peek == '\t':
                                    return 0, 1
                            else:
                                print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                                return 10, 1
                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                            return 10, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                        return 10, 1

                elif self.nextChar == 'u':
                    self.scanNextChar()
                    if self.nextChar == 'b':
                        peek = ''
                        if self.pointer < len(self.nextCharsInLine):
                            peek = self.nextCharsInLine[self.pointer]
                        if peek == ' ' or peek == '\t':
                            return 2, 2
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                    return 10, 1


            elif self.nextChar == 'm':
                self.scanNextChar()
                if self.nextChar == 'u':
                    self.scanNextChar()
                    if self.nextChar == 'l':
                        self.scanNextChar()
                        if self.nextChar == 't':
                            peek = ''
                            if self.pointer < len(self.nextCharsInLine):
                                peek = self.nextCharsInLine[self.pointer]
                            if peek == ' ' or peek == '\t':
                                return 2, 3

                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                            return 10, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                    return 10, 1

            elif self.nextChar == '/':
                self.scanNextChar()
                #print("slash self.nextChar is: ", self.nextChar)
                if self.nextChar == '/':
                    self.indexError = True
                    return -1, 0
                else:
                    print("ERROR: the symbol " + self.lexeme + " uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                    ##self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                
                    return 10, 1
            elif self.nextChar == 'n':
                self.scanNextChar()
                if self.nextChar == 'o':
                    self.scanNextChar()
                    if self.nextChar == 'p':
                        return 4, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer))
                    return 10, 1

            elif self.nextChar == 'o':
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
                                    peek = ''
                                    if self.pointer < len(self.nextCharsInLine):
                                        peek = self.nextCharsInLine[self.pointer]
                                    if peek == ' ' or peek == '\t':
                                        return 3, 1
                                else:
                                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                                    return 10, 1
                            else:
                                print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                                
                                return 10, 1
                        else:
                            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                            
                            return 10, 1
                    else:
                        print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                        
                        return 10, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                    
                    return 10, 1
            elif self.nextChar == 'E':
                self.scanNextChar()
                if self.nextChar == 'O':
                    self.scanNextChar()
                    if self.nextChar == 'F':
                        return -2
                    elif self.nextChar == 'L':
                        return 11, 1
                else:
                    print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
                    
                    return 10, 1
            
            elif self.nextChar == '\n' or self.nextChar == '\r':
                #print("bibambap #2")
                # self.indexError = True #1
                # self.nextChar = -1 #2
                self.eolFlag = True
                return 11, 1
            else: # avoid infinite loop
                return self.handleNonSyntacticWords()
            
        if self.indexError:
            self.indexError = False
            return -1, 0

    def handleE(self):
        self.scanNextChar()
        if self.nextChar == 'O':
            self.scanNextChar()
            if self.nextChar == 'F':
                return -2
            elif self.nextChar == 'L':
                return 11, 1
        else:
            print("ERROR: there is an invalid lexical error for the word ' "+ self.lexeme +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
            return 10, 1

    # def handleS(self):
    #     self.scanNextChar()
    #     if self.nextChar == 't':
    #         self.scanNextChar()
    #         if self.nextChar == 'o':
    #             self.scanNextChar()
    #             if self.nextChar == 'r':
    #                 self.scanNextChar()
    #                 if self.nextChar == 'e':
    #                     self.tokenType = 0 #MEMOP
    #                     self.lexemeIndex = 1 #STORE
    #                     return self.handleNonSyntacticWords()
    #                 else:
    #                     self.tokenType = 10
    #                     return self.handleNonSyntacticWords()
    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()

    #     elif self.nextChar == 'u':
    #         self.scanNextChar()
    #         if self.nextChar == 'b':
    #             self.tokenType = 2 #ARITHOP
    #             self.lexemeIndex = 2 #SUB
    #             return self.tokenType, self.lexemeIndex

    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()


    # def handleL(self):
    #     self.scanNextChar()
    #     if self.nextChar == 'o':
    #         self.scanNextChar()
    #         if self.nextChar == 'a':
    #             self.scanNextChar()
    #             if self.nextChar == 'd':
                    
    #                 if self.peekNextChar() == "I":
    #                     self.scanNextChar()
    #                     if self.nextChar == 'I':
    #                         self.tokenType = 1 #LOADI
    #                         self.lexemeIndex = 1 #LOADI
    #                         return self.handleNonSyntacticWords()
    #                 else:
    #                     self.tokenType = 0 #MEMOP
    #                     self.lexemeIndex = 2 #LOAD
    #                     return self.handleNonSyntacticWords()
    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     elif self.nextChar == 's':
    #         self.scanNextChar()
    #         if self.nextChar == 'h':
    #             self.scanNextChar()
    #             if self.nextChar == 'i':
    #                 self.scanNextChar()
    #                 if self.nextChar == 'f':
    #                     self.scanNextChar()
    #                     if self.nextChar == 't':
    #                             self.tokenType = 2 #ARITHOP
    #                             self.lexemeIndex = 4 #LSHIFT
    #                             return self.handleNonSyntacticWords()

    #                     else:
    #                         self.tokenType = 10
    #                         return self.handleNonSyntacticWords()
    #                 else:
    #                     self.tokenType = 10
    #                     return self.handleNonSyntacticWords()
    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()
    
    # #@profile
    # def handleR(self):
    #     self.scanNextChar()
    #     if self.nextChar.isdigit():
    #         while self.nextChar.isdigit():
    #             self.scanNextChar()

    #         # get rid of extra space
    #         if self.lexeme[-1].isdigit() == False:
    #             self.unScanChar()

    #         self.tokenType = 6
    #         self.lexemeIndex = 1

    #         #store the register name
    #         self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
            
    #         return self.tokenType, self.lexemeIndex
    #         # return self.handleNonSyntacticWords()

            
    #     elif self.nextChar == 's':
    #         self.scanNextChar()
    #         if self.nextChar == 'h':
    #             self.scanNextChar()
    #             if self.nextChar == 'i':
    #                 self.scanNextChar()
    #                 if self.nextChar == 'f':
    #                     self.scanNextChar()
    #                     if self.nextChar == 't':
    #                         self.tokenType = 2 #ARITHOP
    #                         self.lexemeIndex = 5 #RSHIFT
    #                         return self.handleNonSyntacticWords()

    #                     else:
    #                         self.tokenType = 10
    #                         return self.handleNonSyntacticWords()
    #                 else:
    #                     self.tokenType = 10
    #                     return self.handleNonSyntacticWords()
    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()

    # def handleM(self):
    #     self.scanNextChar()
    #     if self.nextChar == 'u':
    #         self.scanNextChar()
    #         if self.nextChar == 'l':
    #             self.scanNextChar()
    #             if self.nextChar == 't':
    #                     self.tokenType = 2 #ARITHOP
    #                     self.lexemeIndex = 3 #MULT
    #                     return self.handleNonSyntacticWords()

    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()

    # def handleA(self):
    #     self.scanNextChar()
    #     if self.nextChar == 'd':
    #         self.scanNextChar()
    #         if self.nextChar == 'd':
    #             self.tokenType = 2 #ARITHOP
    #             self.lexemeIndex = 1 #ADD
    #             return self.handleNonSyntacticWords()

    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()

    #     else:
    #         print("in handleA else")
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()


    # def handleN(self):
    #     self.scanNextChar()
    #     if self.nextChar == 'o':
    #         self.scanNextChar()
    #         if self.nextChar == 'p':
    #             self.tokenType = 4 #NOP
    #             self.lexemeIndex = 1 #NOP

    #             return self.tokenType, self.lexemeIndex
    #             #return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()

    # def handleO(self):
    #     self.scanNextChar()
    #     if self.nextChar == 'u':
    #         self.scanNextChar()
    #         if self.nextChar == 't':
    #             self.scanNextChar()
    #             if self.nextChar == 'p':
    #                 self.scanNextChar()
    #                 if self.nextChar == 'u':
    #                     self.scanNextChar()
    #                     if self.nextChar == 't':
    #                             self.tokenType = 3 #OUTPUT
    #                             self.lexemeIndex = 1 #OUTPUT
    #                             return self.handleNonSyntacticWords()

    #                     else:
    #                         self.tokenType = 10
    #                         return self.handleNonSyntacticWords()
    #                 else:
    #                     self.tokenType = 10
    #                     return self.handleNonSyntacticWords()
    #             else:
    #                 self.tokenType = 10
    #                 return self.handleNonSyntacticWords()
    #         else:
    #             self.tokenType = 10
    #             return self.handleNonSyntacticWords()
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()


    # def handleEquals(self):
    #     self.scanNextChar()
    #     if self.nextChar == '>':
    #             self.tokenType = 8 #INTO
    #             self.lexemeIndex = 1 #=>
    #             #self.charPos
    #             return self.tokenType, self.lexemeIndex
    #     else:
    #         self.tokenType = 10
    #         return self.handleNonSyntacticWords()

    # def handleComma(self):
    #     self.tokenType = 7 #COMMA
    #     self.lexemeIndex = 1 #,
    #     return self.tokenType, self.lexemeIndex    

    # def handleNums(self):
    #     self.scanNextChar()
    #     peek = ''
    #     if self.pointer < len(self.nextCharsInLine):
    #         peek = self.nextCharsInLine[self.pointer]
    #     while str(self.nextChar).isdigit() and str(peek).isdigit():
    #         self.scanNextChar()
    #     if self.lexeme[-1].isdigit() == False:
    #         self.unScanChar()

    #     peek = ''
    #     if self.pointer < len(self.nextCharsInLine):
    #         peek = self.nextCharsInLine[self.pointer]
    #     if peek.isalpha():
    #         self.tokenType = 10
    #         self.lexemeIndex = 1
    #     else:
    #         self.tokenType = 5 #CONSTANT
    #         self.lexemeIndex = 1

    #         self.TOKENS[self.tokenType][self.lexemeIndex] = self.lexeme
            
    #     return self.handleNonSyntacticWords()

    # def handleSlash(self):
    #     self.scanNextChar()
    #     #print("slash self.nextChar is: ", self.nextChar)


    #     if self.nextChar == '/':
    #         self.tokenType = 12 #COMMENT
    #         self.lexemeIndex = 1
    #         # return self.tokenType, self.lexemeIndex

    #         self.indexError = True
    #         return -1
    #     else:
    #         self.tokenType = 10
    #         self.lexemeIndex = 1
    #         print("ERROR: the symbol " + self.lexeme + " uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos))
    #         ##self.TOKENS[self.tokenType][self.lexemeIndex] = "ERROR: "+ self.lexeme +" uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
        
    #         return self.tokenType, self.lexemeIndex
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
    def setPointer(self, pointer):
        self.pointer = pointer
    def getPointer(self):
        return self.pointer
