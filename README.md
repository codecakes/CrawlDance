# CrawlDance
A WebCrawler using efficient LinkedList ADT to store Deep Page links in an N Tree

Run it like:

```
python dance.py http://www.facebook.com <depth level of tree> <max links>
```

```
python dance.py http://www.facebook.com 2 40
```

Running len(result) and nTree.scanSize() comparison yields good Tree scanning time:

```
start = time.time()
print len(result)
print "len time:{}".format(time.time()-start)

start = time.time()
print root.scanSize()
print "scanSize time:{}".format(time.time()-start)
```

In the print screen below, the format is like this:

<result count>
<len time>
<Tree scan count>
<scan time>

![1](http://picpaste.com/pics/raGGw8nW.1436088103.png)

![2](http://picpaste.com/pics/Pukod5f7.1436088005.png)

![3](http://picpaste.com/pics/DaMgo0kq.1436088116.png)

![4](http://picpaste.com/pics/py9F6Mse.1436088317.png)

This is all without optimization.
Cythonizing variables C style usually yields speed gains 10x. using numpy for  contingent arrays may increase retrieval time and overall speed.

### TODOs:
 - Clean code
 - Replace result with numpy array
 - Cythonze helper libs
 - Use something like joblib to parallelize parsing in parseurl
Using 

