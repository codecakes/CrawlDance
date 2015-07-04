#Unrolled Linked List

from math import sqrt, ceil

class Node(object):
    
    def __init__(self,data=None, prev=None, nxt=None, level = 0):
        self.data = data
        self.prev = prev if isinstance(prev, Node) else None
        self.next = nxt if isinstance(nxt, Node) else None
        self.firstChild= None
        self.level = level
    
    def addfirstChild(self, data):
        '''Each firstChild links to a TreeNode/BLL'''
        if isinstance(self.firstChild, TreeNode):
            #adding a sibling to first child
            self.firstChild.addNode(data)
        else:
            #adding the first child
            self.firstChild = TreeNode(data=data, level = self.level+1)
    
    def getfirstChild(self): return self.firstChild
            


class CircularBlock(object):
    '''A block of Circular Linked List w/ Bidirectional navigation.
    Basic Circular Linked List building block'''
    
    def __init__(self, data=None, nextBlock=None, prevBlock=None, level=0):
        self.count = 0
        self.block_level = level
        #head is a Node or None
        self.tail = self.head = Node(data=data, level=self.block_level)
        if self.tail or self.head:
            self.count += 1
        self.size = self.count
        self.nextBlock = nextBlock
        self.prevBlock = prevBlock
        
        
    def reinit(self, data=None, nextBlock=None, prevBlock=None, level=0):
        self.__init__(data=data, nextBlock=nextBlock, \
        prevBlock=prevBlock, level=level)
        
    def setSize(self, size):
        if self.count <= size:
            self.size = size
        else:
            raise Exception("""SizeUnderFlowError: 
            Size smaller than block count.""")
    
    def getHead(self):
        '''Returns a Node i,e. the Head of this Block'''
        return self.head
    
    def addHead(self, data):
        if data:
            headNode = Node(data=data, level=self.block_level)
            thead = self.head
            self.head = headNode
            self.head.next = thead
            self.tail.next = self.head
            self.head.prev = self.tail
            self.count += 1
    
    def addTail(self, data):
        if data:
            tailNode = Node(data=data, level=self.block_level)
            ttail = self.tail
            self.tail = tailNode
            ttail.next = self.tail
            self.tail.next = self.head
            self.head.prev = self.tail
            self.count += 1
    
    def getNode(self, index):
        if 0 <= index-1 < self.count:
            currentNode = self.head
            thereYet = 0
            #O(root(N))max
            while thereYet != index-1:
                currentNode = currentNode.next
                thereYet += 1
            return currentNode
    
    def __getitem__(self, index):
        return self.getNode(index)
    
    def __setitem__(self, index, data):
        node = self[index]
        if node: node.data = data
        elif index == self.count+1:
            self.addTail(data)
                
    def addNode(self, data, index):
        if data:
            if index-1 == 0:
                self.addHead(data, level=self.block_level)
            elif index == self.count:
                self.addTail(data, level=self.block_level)
            elif 0 < index-1 < self.count:
                node = self[index]
                #prevNode = self[index-1]
                newNode = Node(data=data, level=self.block_level)
                if node.next:
                    newNode.next = node.next
                    node.next.prev = newNode
                node.next = newNode
                newNode.prev = node
                self.count += 1
    
    def delNode(self, index):
        if index == self.count:
            node = self[index]
            self.tail=self.head=None
            return node
        elif 0 <= index-1 < self.count:
            node = self[index]
            #print node.data
            #print node.prev
            #print node.next
            if node == self.head:
                self.head = node.next
                self.head.prev = self.tail
                self.tail.next = self.head
            elif node == self.tail:
                #lastNode = self[self.count - 1]
                #self.tail = lastNode
                self.tail = self.tail.prev
                self.tail.next = self.head
                self.head.prev= self.tail
            else:
                #prevNode = self[index-1]
                #if prevNode: prevNode.next = node.next
                if node.prev: node.prev.next = node.next
                if node.next: node.next.prev = node.prev
            self.count -= 1
            return node
    
    def __str__(self):
        msg = ''
        currentNode = self.head
        msg += "{}-->".format(currentNode.data)
        if currentNode.next:
            while currentNode.next != self.head:
                #print currentNode.data
                currentNode = currentNode.next
                try:
                    msg += "{}-->".format(currentNode.data)
                except UnicodeEncodeError:
                    msg += "{}-->".format("SomeUnicode")                
            #msg += "{}-->".format(currentNode.data)
        return msg
    
    def __repr__(self):
        msg = super(type(self), self).__repr__()
        return "{}: {}".format(msg, self.__str__())
        

def findBlockSize(block_size, totCtr):
    newSize = int(ceil(sqrt(totCtr)))
    return newSize if newSize > block_size else block_size

class BLL(object):
    '''Blocked Linked List'''
    
    def __init__(self, blockHead):
        self.block_head = blockHead  #blockHead is CircularBlock or None
        #self.totCtr = self.block_head.totCtr if self.block_head else 0
        #self.setBlockSize()
        self.level = self.block_head.block_level
        self.totCtr = 0
        self.block_size = 3
        self.num_blocks = int(ceil(sqrt(self.totCtr))) or 1
        self.resizeBlocks()
        
    
    def setBlockSize(self):
        self.block_size = findBlockSize(self.block_size, self.totCtr)
    
    def _refreshCtr_BlockSize(self):
        '''Sets: 
        totCtr:Total Counts
        self.block_size: Size/Block
        '''
        currentBlock = self.block_head
        self.num_blocks = 1
        totCtr = currentBlock.count
        #O(root(N))max
        while currentBlock.nextBlock != None:
            totCtr += currentBlock.count
            currentBlock = currentBlock.nextBlock
            self.num_blocks += 1
        self.totCtr = totCtr
        self.setBlockSize()
    
    #O(root(N))
    def resizeBlocks(self):
        self._refreshCtr_BlockSize()
        currentBlock = self.block_head
        while currentBlock.nextBlock != None:
            currentBlock.setSize(self.block_size)
            currentBlock = currentBlock.nextBlock
        
    def getBlockHead(self): return self.block_head
    
    #Add Block
    def _addBlock(self, data):
        currentBlock = self.block_head
        if currentBlock.head != None:
            #O(root(N))
            while currentBlock.nextBlock != None:
                currentBlock = currentBlock.nextBlock
            currentBlock.nextBlock = CircularBlock(data=data, level=self.level)
            cBlock = currentBlock
            currentBlock = currentBlock.nextBlock
            currentBlock.prevBlock = cBlock
            self.num_blocks += 1
        else:
            currentBlock.reinit(data=data, level= self.level)
        currentBlock.setSize(self.block_size)
        self.totCtr += 1
                
    def addNode(self, data):
        currentBlock = self.block_head
        #assert currentBlock.count < self.block_size
        if currentBlock.count < self.block_size:
           currentBlock.addTail(data)
           self.totCtr += 1
           return
        else:
            while currentBlock.nextBlock != None:
                currentBlock = currentBlock.nextBlock
                if currentBlock.count < self.block_size:
                    currentBlock.addTail(data)
                    self.totCtr += 1
                    return
        #If all else fails
        if currentBlock.count == self.block_size or \
        currentBlock == None: self._addBlock(data)
        #This Only runs when condition True
        if findBlockSize(self.block_size, self.totCtr) > self.block_size:
            self._rescale()
    
    def unShift(self, prevBlock, currentBlock, diff):
        '''Shift as many as first diff nodes from currentBlock to prevBlock'''
        if diff > currentBlock.count:
            diff = currentBlock.count
        #print """diff is {},
        #prevBlock: {} and currentBlock: {}""".format(diff, prevBlock, \
        #currentBlock)
        assert isinstance(prevBlock, CircularBlock)
        for _ in xrange(diff):
            if currentBlock.head.data:
                node = currentBlock.delNode(1)
                prevBlock.addTail(node.data)
        #if not (currentBlock.head == currentBlock.tail == None):
            #print """After Unshift 
            #prevBlock: {} and currentBlock: {}""".format(\
            #prevBlock, \
            #currentBlock)
        #else:
            #print """After Unshift 
            #prevBlock: {} """.format(prevBlock)
            
        #else:
        #    raise Exception("""NodesOverflowError: More nodes than 
        #    Current count is for CurrentBlock. 
        #    Count is {} while transfer Nodes are {}
        #    """.format(currentBlock.count, diff))
    
    def shift(self, currentBlock, nextBlock, diff):
        '''Shift as many as last diff nodes from currentBlock to nextBlock'''
        if diff <= currentBlock.count:
            for _ in xrange(diff):
                if currentBlock.tail.data:
                    node = currentBlock.delNode(currentBlock.count)
                    nextBlock.addHead(node.data)
        else:
            raise Exception("""NodesOverflowError: More nodes than 
            Current count is for CurrentBlock. 
            Count is {} while transfer Nodes are {}
            """.format(currentBlock.count, diff))
    
    def _rescale(self):
        '''Shifts as each Block size increases.
        This doesn't change over all Node Count'''
        old_size = self.block_size
        self.setBlockSize()
        assert self.block_size > old_size
        diff = 0
        currentBlock = self.block_head
        if currentBlock.head != None:
            currentBlock.setSize(self.block_size)
            diff = self.block_size - currentBlock.count
            #O(root(N))
            while currentBlock.nextBlock != None:
                currentBlock = currentBlock.nextBlock
                if currentBlock.count < self.block_size:
                    currentBlock.setSize(self.block_size)
                    prevBlock = currentBlock.prevBlock
                    #print "prevBlock:{}".format(prevBlock)
                    self.unShift(prevBlock, currentBlock, diff)
                    if currentBlock.head == currentBlock.tail == None:
                        prevBlock.nextBlock = None
                        currentBlock.prevBlock = None
                        del currentBlock
                        currentBlock = prevBlock
                    else:
                        diff = self.block_size - currentBlock.count
                else:
                    raise Exception("""Block count greater than 
                    size you are setting. Cannot Shrink size.""")
            self.resizeBlocks()
    
    def getBlock(self, index):
        if 0 <= index-1 < self.num_blocks:
            currentBlock = self.block_head
            thereYet = 0
            #O(N)max
            while thereYet != index-1:
                currentBlock = currentBlock.nextBlock
                thereYet += 1
            return currentBlock
            
    def __getitem__(self, index): return self.getBlock(index)
    
    def getBlockNode(self, item):
        if 0 < item <= self.totCtr:
            blockNum = (item+self.block_size-1)//self.block_size - 1
            nodeNum = item%self.block_size
            if nodeNum == 0:
                nodeNum = self.block_size
            c = 0
            block = self.block_head
            while c < blockNum:
                block = block.nextBlock
                c += 1
            return block[nodeNum]
    
    def delBlock(self, index):
        if 0 <= index-1 < self.num_blocks:
            block = self[index]
            block.prevBlock.nextBlock = block.nextBlock
            block.nextBlock.prevBlock = block.prevBlock
            return block

    
    #Insert Node in a Block = InsertNode Op + shiftNode from above
    def insertnode(self): pass

class TreeNode(BLL):
    '''Each Tree Node is a BLL'''
    def __init__(self, data, level = 0):
        super(type(self), self).__init__(CircularBlock(data=data, level=level))

        
        
if __name__ == "__main__":
    dll = BLL(CircularBlock(data=1))
    
    dll.addNode(20)
    dll.addNode(30)
    dll.addNode(40)
    dll.addNode(50)
    dll.addNode(60)
    dll.addNode(70)
    dll.addNode(80)
    dll.addNode(90)
    dll.addNode(100)
    print dll.block_size
    print dll.num_blocks
    dll.addNode(110)
    dll.addNode(120)
    print dll.block_size
    print dll.num_blocks
    dll.addNode(130)
    dll.addNode(140)
    print dll.block_size
    print dll.num_blocks
    dll.addNode(150)
    dll.addNode(160)
    print dll.block_size
    print dll.num_blocks
    dll.addNode(170)
    dll.addNode(180)
    print dll.block_size
    print dll.num_blocks
    for i in xrange(190, 301):
        dll.addNode(i)