from lib2to3.pgen2 import token
import sys
import getopt
import argparse
import time
from Scanner import Scanner
from Parser import Parser
from Tokens import Tokens
import time

def main():
    #FOR DEBUGGING PURPOSES ONLY
    parse("test_inputs/T128k.i")
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

        #for debugging purposes only
        

        #UNCOMMENT AFTER DEBUGGING
        if arg == '--h':
            cmd_parser.print_help()
        elif arg == '--s':
            print("scan")
            scan(args.scan)
        elif arg == '--p':
            print("parser")
            parse(args.parse)
        elif arg == '--r':
            print("read")


def scan(filename):
    try: f = open(filename, 'r')
    except: print("Error: Error occured when opening file: " + filename)
    try:
        block = f.readlines() 
        # block = block.replace("\\r\\n", "")
        block.append("EOF")
        scanner = Scanner()
    except:
        print("Error: Error occured when reading file: " + filename)

    word = ''
    #block = block.replace("\\r\\n", "")
    #print("block: " + str(block))
    # for debugging purposes only
    numErrors = 0
    numNewLines = 0
    tokens = Tokens()

    start = time.time()
    wordScanTime = 0
    while word != -2:
        charPos = scanner.getCharPos()
        lineNum = scanner.getLineNum()
        if word == -1 and lineNum < len(block): #-1 means go to the next line (due to comment, or an error catch)
            numNewLines += 1
            scanner.incrementLineNum()
            lineNum = scanner.getLineNum()
            scanner.resetCharPos()
            charPos = scanner.getCharPos()

        elif word == -2:
            return -2

        #print(lineNum < len(block))
        startScanning = time.time()
        word = scanner.scanNextWord(block[lineNum][charPos:])
        endScanning = time.time()
        wordScanTime += endScanning - startScanning
        #print("word scan time: " + str(endScanning - startScanning))

        #for debugging purposes only
        # if word != -1 and word != -2:
        #     # just wanna see if the errors will record their lexemes
        #     #print("=======================================")
        #     #tokens.getToken(word[0], word[1])
        #     #print("tokens.getToken(word[0], word[1])")

        #     if word[0] == 11: # 11 means there was a \r or \n detected, move on to next line
        #         numNewLines +=1


        # else:
        #     if word == -1:
        #         tokens.getToken(11, 1)
        #     else:
        #         tokens.getToken(9, 1)
    #print ("error count: " + str(numErrors))
    #print("numNewLines: " + str(numNewLines))
    end = time.time()
    print("time: " + str(end - start))
    print("word scan time: " + str(wordScanTime))
    f.close()

@profile
def parse(filename):
    count = 1
    start = time.time()
    parser = Parser()
    with open(filename) as f:
        for line in f:
            
            
            parser.setLineNumber(count)
            parser.parseLine(line)
            count += 1
    end = time.time()
    #print("time: " + str(end - start))



if __name__ == "__main__":
    main()