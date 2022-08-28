import sys
import getopt
import argparse
import time
from scanner import Scanner

def main():
    #start_time = time.time()
    cmd_parser = argparse.ArgumentParser(description='COMP 412 Lab 1')
    # cmd_parser.add_argument('-h', action='store_true',)
    # cmd_parser.add_argument('-s', "--scan", help='prints tokens in token stream')
    # cmd_parser.add_argument('-p', "--parse", help='invokes parser and reports on success or failure')
    # cmd_parser.add_argument('-r', "--read", help='prints human readable version of parser\'s IR')
    # cmd_parser.print_usage('python 412fe.py [flags] filename')
    args = cmd_parser.parse_args()
    print("args: ", args)
    
    for arg in sys.argv:
        print(arg)
        if arg == '-h':
            cmd_parser.print_help()
        elif arg == '-s':
            scan(args.scan)
            print("scan")
        elif arg == '-p':
            print("parser")
        elif arg == '-r':
            print("read")

def scan(filename):
    print("scan")
    block = open("test_inputs/t8.i", "r")
    scanner = Scanner.Scanner(block)
    word = scanner.nextWord()

    while word != "EOF":
        print(word)
        word = scanner.nextWord()
    

if __name__ == "__main__":
    
    main()