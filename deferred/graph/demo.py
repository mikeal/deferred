import locator
from deferred.graph import graph,graphtree
import deferred

import subprocess,webbrowser
import random

def doAorB(d,a,b):
    if random.randint(0,1)==0:
        return d.addCallback(a).addErrback(b)
    else:
        return d.addCallback(b).addErrback(a)

def doList(d,op,n):
    for i in range(n):
        d = d.addCallback(op,i)
    return d

def errorout(derp):
    raise RuntimeException('hi')

d = deferred.Deferred()
def feep(d):
    d = doList(d,lambda thing,i: i,5)
    d = doAorB(d,lambda thing: deferred.succeed('whee'),errorout)
    d = doList(d,lambda thing,i: i,5)
feep(d)
feep(d)
with graph('demo.dot') as g:
    graphtree(d,g)

subprocess.call(["neato","-T","png","-o","demo.png","demo.dot"])
webbrowser.open('demo.png')
