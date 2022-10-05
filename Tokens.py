class Tokens:
    def __init__(self):
        self.TOKENS = [None for i in range(13)]
        self.TOKENS[0] = ["MEMOP", "store", "load"]
        self.TOKENS[1] = ["LOADI", "loadI"]
        self.TOKENS[2] = ["ARITHOP", "add", "sub", "mult", "lshift", "rshift"]
        self.TOKENS[3] = ["OUTPUT", "output"]
        self.TOKENS[4] = ["NOP", "nop"]
        self.TOKENS[5] = ["CONSTANT", 0]
        self.TOKENS[6] = ["REGISTER", "r"] #needs to be followed by a number in handleR()
        self.TOKENS[7] = ["COMMA", ","]
        self.TOKENS[8] = ["INTO", "=>"]
        self.TOKENS[9] = ["EOF", ""]
        self.TOKENS[10] = ["ERROR", ""]
        self.TOKENS[11] = ["EOL", "\n"]
        self.TOKENS[12] = ["COMMENT", "comment"]
    
        self.FIRST_SET = [0, 1, 2, 3, 4, 9, 11]
        self.errorSet = [-1, -2, None]

    def getToken(self, tokenType, lexemeIndex):
        return self.TOKENS[tokenType][lexemeIndex]
    def getLexeme(self, tokenType, lexemeIndex):
        return self.TOKENS[tokenType][lexemeIndex]
    def inFirstSet(self, tokenType):
        if tokenType in self.FIRST_SET:
            return True
        return False

    def printToken(self, tokenType, lexemeIndex):
        print("<" + self.TOKENS[tokenType][0] + ", '" + str(self.TOKENS[tokenType][lexemeIndex]) + "'>")
