import sys
import getopt
import argparse
import time
from Scanner import Scanner

def main():
    #start_time = time.time()
    cmd_parser = argparse.ArgumentParser(description='COMP 412 Lab 1', add_help=False)

    cmd_parser.add_argument('-h', action='store_true',)
    cmd_parser.add_argument('-s', "--scan", help='#rints tokens in token stream')
    cmd_parser.add_argument('-p', "--parse", help='invokes parser and reports on success or failure')
    cmd_parser.add_argument('-r', "--read", help='prints human readable version of parser\'s IR')
    if len(sys.argv) == 1:
        cmd_parser.print_help()
        sys.exit(1)
    args = cmd_parser.parse_args()    
    for arg in sys.argv:
        if arg == '--h':
            cmd_parser.print_help()
        elif arg == '--s':
            print("scan")
            scan(args.scan)
            
        elif arg == '--p':
            print("parser")
        elif arg == '--r':
            print("read")

def scan(filename):

        #store strings as integers
    TOKENS = [None for i in range(11)]
    TOKENS[0] = ["MEMOP", "store", "load"]
    TOKENS[1] = ["LOADI", "loadi"]
    TOKENS[2] = ["ARITHOP", "add", "sub", "mult", "lshift", "rshift"]
    TOKENS[3] = ["OUTPUT", "output"]
    TOKENS[4] = ["NOP", "nop"]
    TOKENS[5] = ["CONSTANT", 0]
    TOKENS[6] = ["REGISTER", "r", 0] #needs to be followed by a number in handleR()
    TOKENS[7] = ["COMMA", ","]
    TOKENS[8] = ["INTO", "=>"]
    TOKENS[9] = ["EOF", "eof"]
    TOKENS[10] = ["ERROR", "error"]
    # print( "Scanning file: " + filename)

    try: f = open(filename, 'r')
    except: print("Error: Error occured when opening file: " + filename)

    try:
        block = f.readlines()
        block.append("EOF")

        scanner = Scanner()
        # word = scanner.scanNextWord(block[0])
        # print(word)
    except:
        print("Error: Error occured when reading file: " + filename + " at line 0")

    word = ''

    while word != -2:
        charPos = scanner.getCharPos()
        lineNum = scanner.getLineNum()

        if word == -1 and lineNum < len(block):
            #print("index error")
            scanner.incrementLineNum()
            lineNum = scanner.getLineNum()

            scanner.resetCharPos()
            charPos = scanner.getCharPos()
        elif word == -2:
            return -2


        print(block[lineNum])
        word = scanner.scanNextWord(block[lineNum][charPos:])
        
        
        if word != -1 and word != -2:
            #print real words only
            print("token word = " + str(TOKENS[word[0]][word[1]]))

    f.close()


if __name__ == "__main__":
    main()