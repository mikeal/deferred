import sys,os
here = os.path.abspath(sys.modules[__name__].__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(here))))
print(sys.path[-1])
