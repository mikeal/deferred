"""
Support for results that aren't immediately available.
"""

from deferred._defer import AlreadyCalledError, Deferred, DeferredList
from deferred._defer import DeferredLock, DeferredQueue, DeferredSemaphore
from deferred._defer import deferredGenerator, fail, FAILURE, FirstError
from deferred._defer import gatherResults, getDebugging, inlineCallbacks
from deferred._defer import maybeDeferred, QueueOverflow, QueueUnderflow
from deferred._defer import returnValue, setDebugging, succeed, SUCCESS
from deferred._defer import waitForDeferred

from deferred._failure import Failure, NoCurrentExceptionError
