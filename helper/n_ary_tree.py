#Custom made WebCrawler ADT N-Tree w/o deletion 

from collections import deque

from unrolledLinkedList import TreeNode


class nTree(object):
    
    def __init__(self, data):
        self.root = TreeNode(data=data)
        self.size = 1
    
    
    def scanfirstChild(self, block, stack):
        '''Scan head to Tail for firstChildren and add to stack'''
        curNode = block.head
        #print "curNode data: {}".format(curNode.data)
        count = block.count
        #O(root(N))
        #while curNode.next != block.head:
        while count > 0:
            if curNode.firstChild:
                stack.appendleft(curNode.firstChild)
                #print "curNode.firstChild: {}\n curNode.firstChild.block_head: {} ".format(curNode.firstChild, curNode.firstChild.block_head)
            curNode = curNode.next
            #print "curNode data: {}".format(curNode.data if curNode else "None")
            if curNode == None: break
            count -= 1
        return
    
    def scanBLL(self, currentBlock, stack):
        #O(N) complexity
        block = currentBlock.block_head
        # 1 BLL scan takes O(N) => root(N) node scans per block
        while block != None:
            #Scan head to Tail for firstChildren and add to stack
            self.scanfirstChild(block, stack) #O(root(N))
            #print "scanBLL block: {}".format(block)
            block = block.nextBlock
            #print "scanBLL blockNext: {}".format(block)
        return
    
    def scanSize(self):
        #Scan by Level Order Traversal
        #Each Block is a TreeNode BLL in itself
        stack = deque()
        self.size = 0
        currentBlock = self.root  #This is a BLL
        stack.appendleft(currentBlock)
        #I don't this while loops runtime complexity bt each time inside ~O(N)
        #must be some polynomial of O(Mmax * N)
        while stack:
            currentBlock = stack.pop()
            #print currentBlock.block_head
            self.size += currentBlock.totCtr
            self.scanBLL(currentBlock, stack)  #O(N)
        return self.size


    
if __name__ == "__main__":
    T = nTree(1)
    T.root.addNode('www.google.com')
    T.root.block_head[2].addfirstChild('yahoo.com')
    T.root.block_head[1].addfirstChild('xyz')
    T.root.block_head[1].firstChild.addNode('baaadeyy!')
    T.root.block_head[1].firstChild.block_head[1].addfirstChild('yaay!')
    T.root.block_head[2].firstChild.block_head[1].addfirstChild('pey')
    #print T.root.block_head[2].firstChild.block_head[1].firstChild
    T.root.block_head[2].firstChild.block_head[1].firstChild.addNode('Jaitley')
    T.root.block_head[2].firstChild.block_head[1].firstChild.addNode('pratley!')
    T.root.block_head[2].firstChild.block_head[1].firstChild.addNode('Totally')
    T.root.block_head[2].firstChild.block_head[1].firstChild.block_head[1].addfirstChild("Sun")
    print "="*10
    print T.scanSize()
    
    
