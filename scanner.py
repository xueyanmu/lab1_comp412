from collections import deque


class Scanner():
    def __init__(self, filename):
        self.filename = filename
        self.nextLine = ""
        self.nextChar = ""
        self.EOF = False
        self.lineNum = 0

        #Store the stream of tokens
        self.tokens = deque()




    def scanNextLine(self):
        self.nextLine = self.filename.readline()
        self.lineNum += 1
        self.nextChar


#try to return a <token, lexeme> pair
    def scanNextWord(self):
        lexeme = ""

        #
