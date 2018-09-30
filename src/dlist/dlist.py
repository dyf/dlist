import numpy as np
import uuid
import operator

class dlist:

    def __init__(self, items, default=None):
        self._items = list(items)
        self._default = default
        self._attrs = set()
        
        self.reindex()

    def reindex(self):
        self._attrs = set()
        for item in self._items:
            self._attrs.update(item.keys())

    def __len__(self):
        return len(self._items)
    
    def __getattr__(self, attr):
        return self._get_simple_attr(attr)

    def __getitem__(self, key):
        if isinstance(key, dlmask):
            return dlist([ self._items[i] for i,tf in enumerate(key) if tf ])
        if isinstance(key, slice):
            return self._items[key]
        else:
            return self._get_simple_attr(key)

    def _get_simple_attr(self, attr):
        return dlseries([v.get(attr, self._default) for v in self._items])

    def _validate(self):
        assert all(isinstance(i, dict) for i in self._items)
        
    def __iadd__(self, other):
        if isinstance(other, dict):
            self._items.append(other)
        elif isinstance(other, list):
            self._items += other
        elif isinstance(other, dlist):
            self._items += other.items

        self.reindex()

        return self

    def __add__(self, other):
        if isinstance(other, dict):
            return dlist(self._items + [other])
        elif isinstance(other, list):
            return dlist(self._items + other)
        elif isinstance(other, dlist):
            return dlist(self._items + other.items)

    def __contains__(self, other):
        return other in self._items

    def __str__(self):
        return str(self._items)

    def __setitem__(self, attr, vals):
        self._set(attr, vals)

    def __setattr__(self, attr, vals):
        # internal vars can use the normal behavior
        if attr.startswith('_'):
            object.__setattr__(self, attr, vals)
        else:
            # external attrs are treated as dict keys
            self._set(attr, vals)
            self.reindex()
        
    def _set(self, key, vals):
        if is_sequence(vals):
            self._set_sequence(key, vals)
        else:
            self._set_single(key, vals)

    def _set_sequence(self, key, vals):
        n = len(vals)
        ilen = len(self)
        if n != ilen:
            raise IndexError("sequence length (%d) not equal to dlist length (%d)" % (n, ilen))
        for i in range(n):
            self._items[i][key] = vals[i]

    def _set_single(self, key, val):
        for item in self._items:
            item[key] = val
        
    def __sub__(self, other):
        if isinstance(other, dlmask):
            return dlist([ self._items[i] for i,tf in enumerate(other) if not tf ])

    def __isub__(self, other):
        if isinstance(other, dlmask):
            self._items = [ self._items[i] for i,tf in enumerate(other) if not tf ]
        return self
            
            

    
    
def is_sequence(arg):
    return (
        not hasattr(arg, "strip") and
        ( hasattr(arg, "__getitem__") or
          hasattr(arg, "__iter__") )
    )

class dlmask(np.ndarray):
    def __new__(cls, tf):
        obj = np.array(tf, dtype=bool)
        return obj.view(cls)


class dlseries(list): 
    @staticmethod
    def accept_loop(items, op, other):
        out_items = []
        for item in items:
            try:
                out_items.append(op(item,other))
            except:
                out_items.append(False)

        return dlmask(out_items)

    
    def __gt__(self, v):
        return self.accept_loop(self, operator.gt, v)

    def __ge__(self, v):
        return self.accept_loop(self, operator.ge, v)

    def __lt__(self, v):
        return self.accept_loop(self, operator.lt, v)

    def __le__(self, v):
        return self.accept_loop(self, operator.le, v)

    def __eq__(self, v):
        return self.accept_loop(self, operator.eq, v)

    def __ne__(self, v):
        return self.accept_loop(self, operator.ne, v)

    def __is__(self, v):
        return self.accept_loop(self, operator.is_, v)

    def isin(self, v, case=True):
        if case:
            return self.accept_loop(self, lambda x,y: x in y, v)
        else:
            return self.accept_loop(self, lambda x,y: lowerish(x) in y, list(map(lowerish, v)))

    def caseless_eq(self, v):
        return self.accept_loop(self, lambda x,y: x.lower() == y.lower(), v)

        
    
def lowerish(v):
    try:
        return v.lower()
    except:
        return v
    
