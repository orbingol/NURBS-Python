# callback handlers for list modification
# https://stackoverflow.com/a/13259435/1162349

import sys

_pyversion = sys.version_info[0]

def callback_method(func):
    def notify(self,*args,**kwargs):
        for _,callback in self._callbacks:
            callback()
        return func(self,*args,**kwargs)
    return notify

class NotifyList(list):
    extend = callback_method(list.extend)
    append = callback_method(list.append)
    remove = callback_method(list.remove)
    pop = callback_method(list.pop)
    __delitem__ = callback_method(list.__delitem__)
    __setitem__ = callback_method(list.__setitem__)
    __iadd__ = callback_method(list.__iadd__)
    __imul__ = callback_method(list.__imul__)

    #Take care to return a new NotifyList if we slice it.
    if _pyversion < 3:
        __setslice__ = callback_method(list.__setslice__)
        __delslice__ = callback_method(list.__delslice__)
        def __getslice__(self,*args):
            return self.__class__(list.__getslice__(self,*args))

    def __getitem__(self,item):
        if isinstance(item,slice):
            return self.__class__(list.__getitem__(self,item))
        else:
            return list.__getitem__(self,item)

    def __init__(self,*args):
        list.__init__(self,*args)
        self._callbacks = []
        self._callback_cntr = 0

    def register_callback(self,cb):
        self._callbacks.append((self._callback_cntr,cb))
        self._callback_cntr += 1
        return self._callback_cntr - 1

    def unregister_callback(self,cbid):
        for idx,(i,cb) in enumerate(self._callbacks):
            if i == cbid:
                self._callbacks.pop(idx)
                return cb
        else:
            return None

