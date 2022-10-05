from collections import deque
import getopt
import sys
from Renamer import Renamer
from Scanner import Scanner
from Parser import Parser
from Reader import Reader
from Tokens import Tokens
from IR import IR
import time
import getopt
# import 412fe.read() as read
from DoublyLinkedList import DoublyLinkedList

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'x:h')
    except:
        print("ERROR: No file specified")
        print("Usage: 412fe.py [options] filename")
        print("Options:")
        print("-h\t\t\tPrints this help message")
        print("-x\t\t\tPrints ILOC block with renamed virtual registers")
        print("Priority of flags: -h, -x")
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
            if '-h' in allFlags:
                print("Usage: 412fe.py [options] filename")
                # help()
                return
            elif '-x' in allFlags:
                # print("Renaming virtual registers...")
                # print("filename: " + filename)
                rename(filename)
                return

        rename(args[0])


    except:
        print("ERROR: No file specified")
        # help()



def rename(filename):
    # parser = Reader()
    # scanner = Scanner()
    # parser.errorExists = False
    # count = 1
    # numOps = 0
    # doubleList = DoublyLinkedList()

    # with open(filename) as f:
    #     for line in f:
    #         #initialize the scanner and parser variables
    #         scanner.setLineNum(count)
    #         scanner.pointer = 0
    #         parser.pointer = 0
    #         parser.fullLine = line
    #         parser.lineNum = count
    #         if parser.getIR()[0]:  # and not parser.errorExists
    #             print(parser.getIR())
    #             doubleList.push(IR(parser.getIR()))
    #             numOps += 1
            
    #         burp = parser.parseLine(line, count)
    #         if burp == 11:  # 11 means there was a \r or \n detected, move on to next line
    #             count += 1
    #             continue  # go to next line
    #         count += 1

    # while doubleList.head is not None:
    #     print(doubleList.head.item)
    #     doubleList.head = doubleList.head.next
    renamer = Renamer(filename=filename)
    
    
    # while dll.head is not None:
    #     print(dll.head.item)
    #     dll.head = dll.head.next
    
    if renamer.numErrors == 0:
        if renamer.numOps > 0: #if there are more than 0 ILOC ops
            renamer.renameSRtoLiveRange()
            renamer.printRenamedIR()
            # with open("412alloc.out", "w") as sys.stdout:
                # renamer.printRenamedIR()
            
        else:
            print >> sys.stderr, "ERROR: 0 ILOC operations found"
            print >> sys.stdout, "ERROR: Terminating."
    else:
        print >> sys.stderr, "ERROR: Building ILOC IR failed due to errors in the input" 
        print >> sys.stdout, "ERROR: Terminating."
 
        
if __name__ == "__main__":
    main()
