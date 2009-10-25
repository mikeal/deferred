"""
Support for results that aren't immediately available.
"""

from deferred._defer import AlreadyCalledError, Deferred, DeferredList
from deferred._defer import DeferredLock, DeferredQueue, DeferredSemaphore
from deferred._defer import fail, FAILURE, FirstError, gatherResults
from deferred._defer import getDebugging, maybeDeferred, QueueOverflow
from deferred._defer import QueueUnderflow, setDebugging, succeed, SUCCESS

from deferred._failure import Failure, NoCurrentExceptionError
