import argparse
from copy import copy
import time
from Scanner import Scanner
from Parser import Parser
from Reader import Reader
from Tokens import Tokens

from IR import IR
import time
import sys
import getopt

from DoublyLinkedList import DoublyLinkedList


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:p:r:h')
    except:
        print("ERROR: No file specified")
        print("Usage: 412fe.py [options] filename")
        print("Options:")
        print("-h\t\t\tPrints this help message")
        print("-s\t\t\tPrints tokens in token stream")
        print("-p\t\t\tInvokes parser and reports on success or failure")
        print("-r\t\t\tPrints human readable version of parser's IR")
        print("Priority of flags: -p, -s, -r")
        return

    try:
        for o, a in opts:
            allFlags = []
            for o, a in opts:
                allFlags.append(o)
                allFlags.append(a)
            for a in args:
                allFlags.append(a)
            # print(allFlags)
            filename = allFlags[-1]

            if len(allFlags) == 1:
                parse(filename)
                return
            else:
                if '-h' in allFlags:
                    print("Usage: 412fe.py [options] filename")
                    help()
                    return
                elif '-r' in allFlags:
                    read(filename)
                    return
                if '-p' in allFlags:
                    parse(filename)
                    return
                elif '-s' in allFlags:
                    scan(filename)
                    return
        parse(args[0])
    except:
        print("ERROR: No file specified")

        help()


def help():
    print("ERROR: No file specified")
    print("Usage: 412fe.py [options] filename")
    print("Options:")
    print("-h\t\t\tPrints this help message")
    print("-s\t\t\tPrints tokens in token stream")
    print("-p\t\t\tInvokes parser and reports on success or failure")
    print("-r\t\t\tPrints human readable version of parser's IR")
    print("Multiple flags will lead to parsing file only")
    print("Priority of flags: -h, -r, -p, -s")
    return


def scan(filename):
    try:
        f = open(filename, 'r')
    except:
        print("ERROR: Error occured when opening file: " + filename)
    try:
        print("Scanning file: " + filename)
        block = f.readlines()
        block.append("EOF")
        scanner = Scanner()
        token = Tokens()
    except:
        print("ERROR: Error occured when reading file: " + filename)

    numTokens = 0
    with open(filename) as f:
        for line in f:
            # print("line: " + line)
            scanner.buffer = line
            scanner.pointer = 0
            currToken = scanner.scanNextWord(line)
            while currToken[0] != 11 and currToken[0] != None and currToken[0] != -2 and currToken[0] != -1:
                token.printToken(currToken[0], currToken[1])
                numTokens += 1
                currToken = scanner.scanNextWord(line)
    print("SUCCESS: Scan successful, finding " + str(numTokens) + " tokens")
    f.close()


def parse(filename):
    try:
        f = open(filename, 'r')
    except:
        print("ERROR: Error occured when opening file: " + filename)
    print("Reading file: " + filename)
    start = time.time()
    count = 1
    numReads = 0
    # ir = IR(None)
    parser = Reader()
    scanner = Scanner()
    doubleList = DoublyLinkedList()
    parser.errorExists = False
    with open(filename) as f:
        for line in f:
            scanner.setLineNum(count)
            scanner.pointer = 0
            parser.pointer = 0
            parser.fullLine = line
            parser.lineNum = count
            if parser.getIR()[0]:  # and not parser.errorExists
                doubleList.push(IR(parser.getIR()[0]))
                numReads += 1
                # print("{Line: "+ str(ir[0]) +" || Opcode: "+ ir[1] + " || Op1: " + str(ir[2]) + " || Op2:" + str(ir[3]) + " || Op3: " + str(ir[4]) +"}")
            burp = parser.parseLine(line, count)
            if burp == 11:  # 11 means there was a \r or \n detected, move on to next line
                count += 1
                continue  # go to next line
            count += 1
    end = time.time()
    print("time: " + str(end - start))
    # if parser.getErrorExists(): print("ERROR: Error occured when reading file: " + filename)
    # else: 
    print("SUCCESS: Read successful, finding " + str(numReads) + " ILOC operations")
    # doubleList.listprint(doubleList.head)

    # count = 1
    # iloc = 0
    # start = time.time()
    # parser = Parser()
    # scanner = Scanner()
    # parser.scanner = scanner
    # ir = IR(None)
    # doubleList = DoublyLinkedList()
    # print("Parsing file: " + filename)
    # try:
    #     with open(filename) as f:
    #         for line in f:

    #             scanner.setLineNum(count)
    #             scanner.pointer = 0
    #             parser.pointer = 0
    #             parser.fullLine = line
    #             parser.lineNum = count
    #             #####currToken = scanner.scanNextWord(line)

    #             burp = parser.parseLine()

    #             iloc +=1
    #             # if burp == 11: # 11 means there was a \r or \n detected, move on to next line
    #             #     count+=1
    #             #     continue # go to next line
    #             count += 1
    #         parser.parseLine()
    #     print("SUCCESS: Parse successful, finding " +str(parser.numILOC) + " ILOC operations")
    # except: print("ERROR: Error occured when opening file: " + str(filename))


def read(filename):
    try:
            f = open(filename, 'r')
    except:
            print("ERROR: Error occured when opening file: " + filename)
    print("Reading file: " + filename)

    parser = Reader()
    parseret = parser.parseFile(filename)[0]
    while parseret.head != None:
        print(parseret.head.item)
        parseret.head = parseret.head.next
        
    # try:
    #     f = open(filename, 'r')
    # except:
    #     print("ERROR: Error occured when opening file: " + filename)
    # print("Reading file: " + filename)

    # count = 1
    # numErrors = 0
    # numReads = 0
    # ir = IR(None)
    # parser = Reader()
    # doubleList = DoublyLinkedList()
    # parser.errorExists = False

    # with open(filename) as f:
    #     for line in f:
    #         if parser.getIR()[0]:  # and not parser.errorExists
    #             print(parser.getIR()[0])
    #             cop = copy(parser.getIR())
    #             doubleList.push(cop)
    #             numReads += 1
    #         burp = parser.parseLine(line, count)
    #         if burp == 11:  # 11 means there was a \r or \n detected, move on to next line
    #             count += 1
    #             continue  # go to next line
    #         count += 1
    # # if parser.getErrorExists(): print("ERROR: Error occured when reading file: " + filename)
    # # else: 
    # print("SUCCESS: Read successful, finding " + str(numReads) + " ILOC operations")
    # #doubleList.listprint(doubleList.head)
    # numErrors = parser.numErrors
    # print("Number of lines with errors: " + str(numErrors))
    # # while doubleList.head is not None:
    # #     print(doubleList.head.item)
    # #     doubleList.head = doubleList.head.next
    # parser.doubleList = doubleList

    #return doubleList, parser.numErrors > 0, parser.numErrors, parser.numOps


if __name__ == "__main__":
    main()
