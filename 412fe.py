import sys
import getopt
import argparse
import time
from scanner import Scanner

def main():
    #start_time = time.time()
    cmd_parser = argparse.ArgumentParser(description='COMP 412 Lab 1', add_help=False)

    cmd_parser.add_argument('-h', action='store_true',)
    cmd_parser.add_argument('-s', "--scan", help='prints tokens in token stream')
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
    f = open(filename, 'r')
    block = f.readlines()
    print("block: ", block)
    print("=====================================")
    scanner = Scanner()
    word = scanner.scanNextWord(block[0])
    print("FIRST word: ", word)
    print("=====================================")

    while word != None:
        
        charPos = scanner.getCharPos()
        lineNum = scanner.getLineNum()
        print("word: ", word, "charPos: ", charPos, "lineNum: ", lineNum)    
        print("=====================================")

        word = scanner.scanNextWord(block[lineNum][charPos:])
        print("SECOND word: ", word, "charPos: ", charPos, "lineNum: ", lineNum)
        print("=====================================")
    # for line in block:
    #     print("line: ", line)
        
    #     word = scanner.scanNextWord(line)
    #     while word != None:
    #         print(word)
    #         charPos = scanner.getCharPos()
    #         word = scanner.scanNextWord(line[charPos:])
    #         #word = scanner.scanNextWord(line)
    

if __name__ == "__main__":
    main()