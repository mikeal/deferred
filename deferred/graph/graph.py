import deferred
import random

from deferred._defer import passthru

def nameOf(node):
    if hasattr(node,'f_code'):
        return node.f_code.co_name
    elif hasattr(node,'__name__'):
        name = node.__name__
        if name == '<lambda>':
            co = node.__code__
            name = '<lambda '+co.co_filename+':'+str(co.co_firstlineno)+'>'
        return name
    elif isinstance(node,int):
        return 'stage '+str(node)
    else:
        print(node,type(node),dir(node))
        raise RuntimeError

def info(type):
    if type == 'errback':
        return '[color="0.0,1.0,1.0",label="errback",w=2.0,len=5]'
    elif type == 'function':
        return '[color="0.4,1.0,1.0",label="added by",w=1.0,len=2]'
    elif type == 'back':
        return '[color="0.8,1.0,1.0",label="back",w=1.0,len=2]'
    elif type== 'next':
        return '[color="0.0,0.0,0.0",label="next",w=2.0,len=1]'
    elif type == 'callback':
        return '[color="0.6,1.0,1.0",w=1.0,len=2]'
    elif type == 'same':
        return '[color="0.0,0.0,0.5",w=0.0]'
    else:
        raise RuntimeError("What is",type)

from functools import total_ordering
@total_ordering
class Node:
    def __init__(self,id,label):
        self.id = id
        self.name = str(id)
        self.label = label
    def __hash__(self):
        return hash(self.id)
    def __lt__(self,other):
        return self.id < other.id
    def __eq__(self,other):
        return self.id == other.id
    def __repr__(self):
        return repr(self.id)

class Graph:
    def __init__(self,dest):
        self.dest = dest
        dest.write('digraph {\n')
        self.nodes = set()
        self.donedid = set()
        self.counter = 0
    def hashh(self,a):
        if isinstance(a,Node): return a
        return Node(hash(a),nameOf(a))
    def bump(self,a,b):
        self.update(a,b,'next')
    def update(self,a,b,type):
        assert a is not None
        assert b is not None
        if a is passthru: return
        if b is passthru: return
        a = self.hashh(a)
        b = self.hashh(b)
        if (a,b) in self.donedid: return
        self.donedid.add((a,b))
        self.dest.write('"'+a.name+'" -> "'+b.name+'" '+info(type) + '\n')
        self.nodes.add(a)
        self.nodes.add(b)
    def callback(self,stage,cb):
        self.update(stage,cb,'callback')
    def errback(self,stage,eb):
        self.update(stage,eb,'errback')
    def function(self,cb,ctx):
        self.update(cb,ctx,'function')
    def back(self,low,high):
        self.update(low,high,'back')
    def finish(self):
        for node in self.nodes:
            self.dest.write('"'+node.name+'" [label="'+node.label+'"]'+'\n')
        self.dest.write('}\n')

from contextlib import contextmanager
@contextmanager
def withit(path):
    with open(path,'wt') as out:
        g = None
        try:
            g = Graph(out)
            yield g
        finally:
            if g:
                g.finish()

import sys
module=sys.modules[__name__]
withit.moduleboo = module
sys.modules[__name__] = withit
