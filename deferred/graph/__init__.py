#import locator
import deferred
import graph
from deferred._defer import passthru

import traceback
import sys

contexts = {}

oldacbs = deferred.Deferred.addCallbacks
def newacbs(self, callback, errback=None,
                     callbackArgs=None, callbackKeywords=None,
                     errbackArgs=None, errbackKeywords=None):
    for cb in (callback,errback):
        if cb:
            print('adding',cb)
            try:
                raise ZeroDivisionError
            except ZeroDivisionError:
                contexts[cb] = sys.exc_info()[2].tb_frame.f_back.f_back
    return oldacbs(self,callback,errback,callbackArgs,callbackKeywords,errbackArgs,errbackKeywords)
if oldacbs is not newacbs:
    deferred.Deferred.addCallbacks = newacbs

def graphtree(d,graph):
    def doCTX(cb,ctx):
        graph.function(cb,ctx)
        while ctx.f_back:
            graph.back(ctx,ctx.f_back)
            ctx = ctx.f_back
    for stage,thing in enumerate(d.callbacks):
        cb = thing[0][0]
        if stage>0:
            graph.bump(stage-1,stage)
        eb = thing[1][0]
        def derp(cb):
            ctx = contexts.get(cb)
            if ctx:
                contexts.pop(cb)
                doCTX(cb,ctx)
        graph.callback(stage,cb)
        graph.errback(stage,eb)
        derp(eb)
        derp(cb)
    for cb,ctx in contexts.items():
        doCTX(cb,ctx)
