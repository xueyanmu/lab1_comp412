from collections import deque
import sys

from Reader import Reader


class Renamer():
    def __init__(self, filename):
        self.filename = filename
        
        parser = Reader()
        self.parseRet = parser.parseFile(filename)
        self.numOps = self.parseRet[1]
        self.OPS = self.parseRet[0]
        self.numErrors = self.parseRet[2]
        self.maxSR = self.parseRet[3]
        self.n = self.numOps - 1
        #self.IR = parser.IR
        #TODO: NEED THE ENTIRE QUEUE OF IR LINES TO BE COMPILED HERE
        self.permHead = self.OPS.head
        self.sr2vr = [None for i in range(self.maxSR + 1)]
        self.lu = [float('inf') for j in range(self.maxSR + 1)]
        self.maxLive = 0
        self.op = None
        self.vrName = 0
        self.index = self.n
        self.renamedBlock = deque()
        # define ops
        # self.record_index = ("Opcode", "SR", "VR", "PR", "NU", "SR", "VR", "PR", "NU", "SR", "VR", "PR", "NU", "INDEX", "PRINT")


        self.OP3NU = 12

        self.OP1isReg = {"load", "store", "add", "sub", "mult", "lshift", "rshift"}
        self.OP2isReg = {"add", "sub", "mult", "lshift", "rshift", "store"}

        # OPCODE Type Dictionary
        self.OpType = {"load": "MEMOP", "store": "MEMOP", "loadI": "LOADI", "add": "ARITHOP", "sub": "ARITHOP",
                     "mult": "ARITHOP", "lshift": "ARITHOP", "rshift": "ARITHOP", "output": "OUTPUT", "nop": "NOP"}

    def renameSRtoLiveRange(self):
        #======================
        # for each Op in the block, bottom to top
        self.OPS.reverse()
        while self.OPS.head is not None:
           
            liveCount = (self.maxSR + 1) - self.sr2vr.count(None)
            if liveCount > self.maxLive:
                self.maxLive = liveCount
            
            self.op = self.OPS.head
            
            
            for i in [1, 5, 9]:
                #print("here")
                if self.op[i] and str(self.op[i]).isdigit():
                    self.op[i] = int(self.op[i])
                    # break
                elif self.op[i] and self.op[i][0] == "r":
                    self.op[i] = int(self.op[i][1:])

            # for each operand O that OP ~~defines~~
            # if self.op[0] is not None:
            #     for i in self.op:
                    

            if self.op[0] != 'nop' and self.op[0] != 'output':
                if self.op[9] is not None:

                    # Unused DEF
                    if self.sr2vr[self.op[9]] == None:
                        self.sr2vr[self.op[9]] = self.vrName
                        self.vrName += 1
                    self.op[10] = self.sr2vr[self.op[9]]

                    self.op[12] = self.lu[self.op[9]]
                    self.sr2vr[self.op[9]] = None #kill OP3
                    self.lu[self.op[9]] = float("inf")
                    # if self.op[0] == 'store':
                    #     print( self.op.item)
                    # if self.op[0] == 'add':
                    #     print( self.op.item)
                # for each operand O that OP ~~uses~~
                if self.op[1] is not None and self.op[0] != 'loadI':
                    # Last USE
                    #print(isinstance(self.op[1], str))
                    # print(self.sr2vr[self.op[1]])

                    if self.sr2vr[self.op[1]] == None:
                        self.sr2vr[self.op[1]] = self.vrName
                        self.vrName += 1
                    self.op[2] = self.sr2vr[self.op[1]]
                    self.op[4] = self.lu[self.op[1]]
                    self.lu[self.op[1]] = self.index

                if self.op[5] is not None:
                    if self.sr2vr[self.op[5]] == None:
                        self.sr2vr[self.op[5]] = self.vrName
                        self.vrName += 1
                    self.op[6] = self.sr2vr[self.op[5]]
                    self.op[8] = self.lu[self.op[5]]
                    self.lu[self.op[5]] = self.index
                #print(self.op.item)
                self.index -=1
                # print(self.index >= 0)
            
        
            self.OPS.head = self.OPS.head.next
    
  

    def printRenamedIR(self):
        
        while self.permHead:
            op = self.permHead
            # print(op.item)
 
            
            # op = self.renamedBlock.popleft()
            if self.OpType[op[0]] == "MEMOP":

                
                if op[0] == 'store':
                    print >> sys.stdout, "%s  r%i    =>  r%i" % (op[0], op[2], op[6])
                elif op[0] == 'output':
                    print >> sys.stdout, "%s  r%i" % (op[0], op[2])
                else:
                    print >> sys.stdout, "%s  r%i    =>  r%i" % (op[0], op[2], op[10])
            elif self.OpType[op[0]] == "LOADI":

                
                
                # print >> sys.stdout, "%s  %i    =>  r%i" % (op[0], op[2], op[10])
                print >> sys.stdout, "%s  %i    =>  r%i" % (op[0], op[1], op[10])
            elif self.OpType[op[0]] == "ARITHOP":
                
                print >> sys.stdout, "%s  r%i, r%i    =>  r%i" \
                    % (op[0], op[2], op[6], op[10])
            elif self.OpType[op[0]] == "OUTPUT" :

                print >> sys.stdout, "%s  %i" % (op[0], op[1])

            elif self.OpType[op[0]] == "NOP" :
                    
                    print >> sys.stdout, "%s" % (op[0])
            self.permHead = self.permHead.prev      
        
        # print("here")
        # while self.OPS.head:
        #     op = self.OPS.head
        #     print(self.OPS.tail)
        #     print(op.item)
        #     # op = self.renamedBlock.popleft()
        #     if self.OpType[op[0]] == "MEMOP":
        #         if op[0] == 'store':
        #             print >> sys.stdout, "%s  r%i    =>  r%i" % (op[0], op[1], op[5])
        #         else:
        #             print >> sys.stdout, "%s  r%i    =>  r%i" % (op[0], op[1], op[9])
        #     elif self.OpType[op[0]] == "LOADI":
        #         print >> sys.stdout, "%s  %i    =>  r%i" % (op[0], op[1], op[9])
        #     elif self.OpType[op[0]] == "ARITHOP":
        #         print >> sys.stdout, "%s  r%i, r%i    =>  r%i" \
        #             % (op[0], op[1], op[5], op[9])
        #     elif self.OpType[op[0]] == "OUTPUT":
        #         print >> sys.stdout, "%s  %i" % (op[0], op[1])
        #     self.OPS.head = self.OPS.head.prev