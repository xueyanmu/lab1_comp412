from collections import deque
from curses.ascii import isalnum, isalpha, isdigit
import time
import sys
import cProfile
# import line_profiler
class Scanner():
    def __init__(self):
        # self.filename = filename
        self.buffer = ""
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
        self.tokenType = None

        # End State #
        self.se = -1
        #Store the stream of tokens
        self.tokens = deque()

        #store strings as integers
        self.TOKENS = [None for i in range(13)]
        self.TOKENS[0] = ["MEMOP", "store", "load"]
        self.TOKENS[1] = ["LOADI", "loadI"]
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
        print >> sys.stderr, "<" + self.TOKENS[tokenType][0] + ", '" + self.TOKENS[tokenType][lexemeIndex] + "'>"
        return self.TOKENS[tokenType][lexemeIndex]

    def scanNextChar(self):
            self.nextChar = self.buffer[self.pointer]
            self.pointer += 1
            self.lexeme += self.nextChar


    # handle everything with wrong syntax or extra chars. Trashes comments and error-giving lines
    def handleNonSyntacticWords(self):
        peek = ''
        if self.pointer < len(self.buffer):
            peek = self.buffer[self.pointer]
        #     #return self.nextCharsInLine[0]

        if self.tokenType == 10:
            #this error will be covered by the parser i guess
            print >> sys.stderr, "ERROR " + str(self.nextLineNum) + ": there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
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
            print >> sys.stderr, "ERROR " + str(self.nextLineNum) + ": there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
            self.tokenType = 10
            self.lexemeIndex = 1
            return 10, 1

    #@profile
    def scanNextWord(self, currLine):
        
        self.lexeme = ""
        self.buffer = currLine
        
        if self.eolFlag == True:
            self.eolFlag = False
            return 11, 1
            
        numsToChars = [str(i) for i in range(10)]

        if self.pointer >= len(self.buffer):
            return -1, 0

        while self.pointer < len(self.buffer): 
            # use these to move placeholders for charPos and lineNum
            while self.buffer[self.pointer] == ' ' or self.buffer[self.pointer] == '\t':
                #self.lexeme += ' '
                self.pointer+=1
                if self.pointer >= len(self.buffer):
                    return 11, 1


            if self.buffer[self.pointer] == 'r':

                self.lexeme += 'r'
                self.pointer+=1
                
                if self.buffer[self.pointer] <= '9' and self.buffer[self.pointer] >= '0':
                    while self.buffer[self.pointer] <= '9' and self.buffer[self.pointer] >= '0':
     
                        self.lexeme += self.buffer[self.pointer]

                        if self.pointer < len(self.buffer):
                            self.pointer += 1
                        if self.buffer[self.pointer] == '\n' or self.buffer[self.pointer] == '\r':
                            self.eolFlag = True
                        # else:
                        #     self.lexeme += self.buffer[self.pointer]
                    #print >> sys.stderr, "lexeme is " + self.lexeme
                    return 6, 1, self.lexeme
            
                elif self.buffer[self.pointer] == 's':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'h':
                        self.pointer+=1
                        if self.buffer[self.pointer] == 'i':
                            self.pointer+=1
                            if self.buffer[self.pointer] == 'f':
                                self.pointer+=1
                                if self.buffer[self.pointer] == 't':
                                    self.pointer+=1
                                    return 2, 5
                                else:
                                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                    return 10, 1
                            else:
                                print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                
                                return 10, 1
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                            
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    return 10, 1


            elif self.buffer[self.pointer] == ',':
                self.pointer+=1
                return 7, 1

            elif self.buffer[self.pointer] == '=':
                self.pointer+=1
                if self.buffer[self.pointer] == '>':
                    self.pointer+=1
                    return 8, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    return 10, 1

            elif self.buffer[self.pointer] == 'a':
                self.pointer+=1
                if self.buffer[self.pointer] == 'd':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'd':
                        self.pointer+=1
                        return 2, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    return 10, 1

            elif self.buffer[self.pointer] == 'l':
                self.pointer+=1
                if self.buffer[self.pointer] == 'o':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'a':
                        self.pointer+=1
                        if self.buffer[self.pointer] == 'd':
                            self.pointer+=1
                            peek = ''
                            if self.pointer < len(self.buffer):
                                peek = self.buffer[self.pointer]

                            if peek == 'I':
                                self.pointer+=1
                                return 1, 1

                            elif peek == ' ' or peek == '\t':
                                return 0, 2
                            else:
                                print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                return 10, 1
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                        return 10, 1
                elif self.buffer[self.pointer] == 's':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'h':
                        self.pointer+=1
                        if self.buffer[self.pointer] == 'i':
                            self.pointer+=1
                            if self.buffer[self.pointer] == 'f':
                                self.pointer+=1
                                if self.buffer[self.pointer] == 't':
                                    self.pointer+=1
                                    return 2, 4
                                else:
                                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                    
                                    return 10, 1
                            else:
                                print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                
                                return 10, 1
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                            
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    return 10, 1

            elif self.buffer[self.pointer] in numsToChars:
                while self.pointer < len(self.buffer) and self.buffer[self.pointer] >= '0' and self.buffer[self.pointer] <= '9':
                    if self.pointer >= len(self.buffer):
                        break
                    else:
                        self.lexeme += self.buffer[self.pointer]
                        self.pointer+=1
                peek = ''
                if self.pointer < len(self.buffer):
                    peek = self.buffer[self.pointer]
                if peek.isalpha():
                    return 10, 1
                else:
                    #print >> sys.stderr, self.lexeme)
                    return 5, 1, self.lexeme

            elif self.buffer[self.pointer] == 's':
                self.pointer+=1
                if self.buffer[self.pointer] == 't':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'o':
                        self.pointer+=1
                        if self.buffer[self.pointer] == 'r':
                            self.pointer+=1
                            if self.buffer[self.pointer] == 'e':
                                self.pointer+=1
                                return 0, 1
                            else:
                                print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                                return 10, 1
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                        return 10, 1
                elif self.buffer[self.pointer] == 'u':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'b':
                        self.pointer+=1
                        return 2, 2
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                    return 10, 1

            elif self.buffer[self.pointer] == 'm':
                self.pointer+=1
                if self.buffer[self.pointer] == 'u':
                    self.pointer+=1
                    if self.buffer[self.pointer] == 'l':
                        self.pointer+=1
                        if self.buffer[self.pointer] == 't':
                            self.pointer+=1
                            return 2, 3
                        
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                    return 10, 1

            elif self.buffer[self.pointer] == '/':
                self.pointer+=1
                if self.buffer[self.pointer] == '/':
                    self.indexError = True
                    return -1, 12
                else:
                    print >> sys.stderr, "ERROR: the symbol " + self.buffer[self.pointer] + " uses invalid syntax at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    return 10, 1
            elif self.buffer[self.pointer] == 'n':
                self.pointer += 1
                if self.buffer[self.pointer] == 'o':
                    self.pointer += 1
                    if self.buffer[self.pointer] == 'p':
                        self.pointer += 1
                        return 4, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                    return 10, 1

            
            elif self.buffer[self.pointer] == 'o':
                self.pointer += 1
                if self.buffer[self.pointer] == 'u':
                    self.pointer += 1
                    if self.buffer[self.pointer] == 't':
                        self.pointer += 1
                        if self.buffer[self.pointer] == 'p':
                            self.pointer += 1
                            if self.buffer[self.pointer] == 'u':
                                self.pointer += 1
                                if self.buffer[self.pointer] == 't':
                                    self.pointer += 1
                                    return 3, 1
                                else:
                                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                    return 10, 1
                            else:
                                print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                                
                                return 10, 1
                        else:
                            print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                            
                            return 10, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                        
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.charPos)
                    
                    return 10, 1

            elif self.buffer[self.pointer] == 'E':
                self.pointer += 1
                if self.buffer[self.pointer] == 'O':
                    self.pointer += 1
                    if self.buffer[self.pointer] == 'F':
                        return -2
                    elif self.buffer[self.pointer] == 'L':
                        return 11, 1
                    else:
                        print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                        return 10, 1
                else:
                    print >> sys.stderr, "ERROR: there is an invalid lexical error for the word ' "+ self.buffer[self.pointer] +"' at line " + str(self.nextLineNum) + " and position " + str(self.pointer)
                    return 10, 1
        
            elif self.buffer[self.pointer] == '\n' or self.buffer[self.pointer] == '\r':
                self.pointer+=1
                self.eolFlag = True
                return 11, 1
            else: # avoid infinite loop
                return self.handleNonSyntacticWords()
            
        if self.indexError:
            self.indexError = False
            return -1, 0

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
