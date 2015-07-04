#####################################################################
# Web Crawler
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a web crawler in a custom N-ary Tree format that: 
# - parses a given url.
# - Stores parsed url as children of the parent url.
# - Repeats the same step for each Url Node.
# ------------------------------------------------------------------
# Original Author: Akul Mathur - @codecakes
# Maintainer(s):
# - Akul Mathur - @codecakes
#####################################################################

from collections import deque

from lxml.html import fromstring
import requests

from helper.n_ary_tree import nTree

def parseLinks(url):
    url_content = requests.get(url).content
    dom = fromstring(url_content)
    dom.make_links_absolute(url)
    anchors = dom.cssselect('a')
    return anchors

## Block by Block Nodes Parser
def parsefirstChild(block, stack, result):
    '''Scan head to Tail for firstChildren and add to stack'''
    curNode = block.head
    #print "curNode data: {}".format(curNode.data)
    count = block.count
    
    #O(N)
    try:
        anchors = parseLinks(curNode.data)
    except:
        anchors = []
    for anchor in anchors:
        if curNode.data:
            link = anchor.get("href")
            result.append(link)
            curNode.addfirstChild(link)
    #[curNode.addfirstChild(anchor.get("href")) for anchor in parseLinks(curNode.data) if curNode.data]
    
    #O(root(N))
    while count > 0:
        if curNode.firstChild:
            stack.appendleft(curNode.firstChild)
            #print "curNode.firstChild: {}\n curNode.firstChild.block_head: {} ".format(curNode.firstChild, curNode.firstChild.block_head)
        
        curNode = curNode.next
        #print "curNode data: {}".format(curNode.data if curNode else "None")
        if curNode == None: break
        count -= 1
    return

def parseBLL(currentBlock, stack, result):
    #O(N) complexity
    block = currentBlock.block_head
    # 1 BLL scan takes O(N) => root(N) node scans per block
    while block != None:
        #Scan head to Tail for firstChildren and add to stack
        parsefirstChild(block, stack, result) #O(root(N))
        #print "scanBLL block: {}".format(block)
        block = block.nextBlock
        #print "scanBLL blockNext: {}".format(block)
    return

def parse(root, max_level, numlinks):
    #Scan by Level Order Traversal
    #Each Block is a TreeNode BLL in itself
    stack = deque()
    result = []
    currentBlock = root.root  #This is a BLL
    stack.appendleft(currentBlock)
    #I don't know this while loop's runtime complexity but each time inside ~O(N)
    #must be some polynomial of O(Mmax * Nmax) 
    #where Mmax = Total Nodes
    #Nmax = max nodes from a single url
    while stack:
        currentBlock = stack.pop()
        #print currentBlock.level
        if currentBlock.level > max_level: break
        #print currentBlock.block_head
        parseBLL(currentBlock, stack, result)  #~O(N)
        #print result
        if numlinks > 0 and len(result) >= numlinks: break
    return root, result


def crawl_dance(url, max_level = 2, numlinks = 0):
    '''
    #Pop the TreeNode/BLL
    #Scan and yield each Node Per Block
    #add all child url links in the curNode
    #Scan and push All firstChild Nodes in curNode to Stack
    '''
    root = nTree(url)
    return parse(root, max_level, numlinks)

if __name__ == "__main__":
    import sys
    
    url = sys.argv[1]
    maxlevel = int(sys.argv[2])
    numlinks = int(sys.argv[3])
    
    print "Crawling for url: {} at a max depth of: {} for a total # of links:{}".format(url, maxlevel, numlinks)
    
    print crawl_dance(url, max_level=maxlevel, numlinks = numlinks)