from collections import deque


class Scanner():
    def __init__(self, filename):
        self.filename = filename
        self.nextLine = ""
        self.nextChar = ""
        self.EOF = False
        self.nextLineNum = 0
        self.tokenType = ""
        self.charPos = 0
        self.lexeme = ""
        self.EOF = -1
        self.ERROR = -2
        

        # End State #
        self.se = -1
        #Store the stream of tokens
        self.tokens = deque()

        #store strings as integers
        self.tokenTypeStringTable = []
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


    def EOLHandler():
        self.charPos = 0
        self.nextLineNum += 1
        self.scanNextLine()
  
    def EOFHandler():
        self.charPos += 1
        return self.tokenType, self.lexeme


    #what is a lexeme
    def scanNextChar(self):
        try :
            self.nextChar = self.nextLine[0] #TODO: check if this is correct
            self.nextLine = self.nextLine[1:] #TODO: check if this is correct
        except IndexError:
            self.EOF = True
            self.nextChar = self.EOF
            print("Error with reading in character")

        if self.nextChar == '\n':
            self.EOFHandler()

        if self.nextChar == self.EOF:
            self.EOFHandler()

        else:
            #default case
            self.charPos += 1
            self.lexeme += self.nextChar
   

    def scanNextLine(self):
        self.nextLine = self.filename.readline()
        self.nextLineNum += 1
        self.scanNextWord()


#try to return a <token, lexeme> pair
    def scanNextWord(self):
        lexeme = ""
        self.scanNextChar()

        while self.nextChar != self.EOF: #TODO: THIS IS EOL CASE
            self.nextChar = self.nextChar
            if self.nextChar == ' ' \
            or self.nextChar == '\t' \
            or self.nextChar == '\n' \
            or self.nextChar == '\r': \
                self.EOLHandler()



            if self.nextChar == 's':
                pass
            if self.nextChar == 'l':
                pass
            if self.nextChar == 'r':
                pass
            if self.nextChar == 'm':
                pass
            if self.nextChar == 'a':
                pass
            if self.nextChar == 'n':
                pass
            if self.nextChar == 'n':
                pass
            if self.nextChar == 'o':
                pass
            if self.nextChar == '=':
                pass
            if self.nextChar == ',':
                pass

            # if self.nextChar == 's' \
            # or self.nextChar == 'l' \
            # or self.nextChar == 'r' \
            # or self.nextChar == 'm' \
            # or self.nextChar == 'a' \
            # or self.nextChar == 'n' \
            # or self.nextChar == 'o' \
            # or self.nextChar == '=' \
            # or self.nextChar == ',':

            else:
                pass
        

    def handleS():
        self.scanNextChar()
        if self.nextChar == 't':
            self.scanNextChar()
            if self.nextChar == 'o':
                self.scanNextChar()
                if self.nextChar == 'r':
                    self.scanNextChar()
                    if self.nextChar == 'e':
                        self.scanNextChar()
                        if self.nextChar == ' ' \
                        or self.nextChar == '\t' \
                        or self.nextChar == '\n' \
                        or self.nextChar == '\r':
                            # STORE TOKEN #
                            self.EOLHandler()
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
            else:
                print("error with scanning word")
                pass

        elif self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'b':
                self.scanNextChar()
                if self.nextChar == ' ' \
                or self.nextChar == '\t' \
                or self.nextChar == '\n' \
                or self.nextChar == '\r':
                    # SUB TOKEN #
                    self.EOLHandler()
                    self.tokenType = "ARITHOP"
                    self.lexeme = "sub"
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


    def handleL():
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'a':
                self.scanNextChar()
                if self.nextChar == 'd':
                    self.scanNextChar()
                    if self.nextChar == ' ' \
                        or self.nextChar == '\t' \
                        or self.nextChar == '\n' \
                        or self.nextChar == '\r':
                            # LOAD TOKEN #
                            self.EOLHandler()
                            self.tokenType = "MEMOP"
                            self.lexeme = "load"
                            return self.tokenType, self.lexeme
                    else:
                        print("error with scanning word")
                        pass

                    if self.nextChar == 'I':
                        self.scanNextChar()
                        if self.nextChar == ' ' \
                        or self.nextChar == '\t' \
                        or self.nextChar == '\n' \
                        or self.nextChar == '\r':
                            # LOADI TOKEN #
                            self.EOLHandler()
                            self.tokenType = "LOADI"
                            self.lexeme = "loadI"
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
        elif self.nextChar == 's':
            self.scanNextChar()
            if self.nextChar == 'h':
                self.scanNextChar()
                if self.nextChar == 'i':
                    self.scanNextChar()
                    if self.nextChar == 'f':
                        self.scanNextChar()
                        if self.nextChar == 't':
                            self.scanNextChar()
                            if self.nextChar == ' ' \
                            or self.nextChar == '\t' \
                            or self.nextChar == '\n' \
                            or self.nextChar == '\r':
                                # LSHIFT TOKEN #
                                self.EOLHandler()
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
        else:
            print("error with scanning word")
            pass
    def handleR():
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
                            self.scanNextChar()
                            if self.nextChar == ' ' \
                            or self.nextChar == '\t' \
                            or self.nextChar == '\n' \
                            or self.nextChar == '\r':
                                # RSHIFT TOKEN #
                                self.EOLHandler()
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
        else:
            print("error with scanning word")
            pass

    def handleM():
        self.scanNextChar()
        if self.nextChar == 'u':
            self.scanNextChar()
            if self.nextChar == 'l':
                self.scanNextChar()
                if self.nextChar == 't':
                    self.scanNextChar()
                    if self.nextChar == ' ' \
                    or self.nextChar == '\t' \
                    or self.nextChar == '\n' \
                    or self.nextChar == '\r':
                        # MULT TOKEN #
                        self.EOLHandler()
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
        else:
            print("error with scanning word")
            pass

    def handleA():
        self.scanNextChar()
        if self.nextChar == 'd':
            self.scanNextChar()
            if self.nextChar == 'd':
                self.scanNextChar()
                if self.nextChar == ' ' \
                or self.nextChar == '\t' \
                or self.nextChar == '\n' \
                or self.nextChar == '\r':
                    # ADD TOKEN #
                    self.EOLHandler()
                    self.tokenType = "ARITHOP"
                    self.lexeme = "add"
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
    def handleN():
        self.scanNextChar()
        if self.nextChar == 'o':
            self.scanNextChar()
            if self.nextChar == 'p':
                self.scanNextChar()
                if self.nextChar == ' ' \
                or self.nextChar == '\t' \
                or self.nextChar == '\n' \
                or self.nextChar == '\r':
                    # NOP TOKEN #
                    self.EOLHandler()
                    self.tokenType = "NOP"
                    self.lexeme = "nop"
                    return self.tokenType, self.lexeme
                else:
                    print("error with scanning word")
                    pass
            else:
                print("error with scanning word")
                pass
    def handleO():
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
                            self.scanNextChar()
                            if self.nextChar == ' ' \
                            or self.nextChar == '\t' \
                            or self.nextChar == '\n' \
                            or self.nextChar == '\r':
                                # OUTPUT TOKEN #
                                self.EOLHandler()
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
        else:
            print("error with scanning word")
            pass
    def handleEqual():
        self.scanNextChar()
        if self.nextChar == '>':
            self.scanNextChar()
            if self.nextChar == ' ' \
            or self.nextChar == '\t' \
            or self.nextChar == '\n' \
            or self.nextChar == '\r':
                # INTO TOKEN #
                self.EOLHandler()
                self.tokenType = "INTO"
                self.lexeme = "INTO"
                return self.tokenType, self.lexeme
            else:
                print("error with scanning word")
                pass
        else:
            print("error with scanning word")
            pass
    def handleComma():
        if self.nextChar == ' ' \
            or self.nextChar == '\t' \
            or self.nextChar == '\n' \
            or self.nextChar == '\r':
                # COMMA TOKEN #
                self.EOLHandler()
                self.tokenType = "COMMA"
                self.lexeme = ","
                return self.tokenType, self.lexeme
        else:
            print("error with scanning word")
            pass

