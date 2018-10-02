
import numpy as np
import copy
import operator

class dlist:

    def __init__(self, items, default=None):
        self._items = list(items)
        self._default = default
        
    def attrs(self):
        attrs = set()
        for item in self._items:
            attrs.update(item.keys())
        return attrs

    def __len__(self):
        return len(self._items)
    
    def __getattr__(self, attr):
        return self.get(attr)

    # [] is for positional indexing
    def __getitem__(self, other):
        if isinstance(other, dlmask) or callable(other):
            return self.where(other)
        elif isinstance(other, slice):
            return dlist(self._items[other])
        elif isinstance(other, int):
            return self._items[other]
        else:
            raise TypeError("indices must be integers, slices, or dlmasks, not %s" % type(other))

    def where(self, mask_or_cb):
        if callable(mask_or_cb):
            mask = dlmask([ mask_or_cb(x) for x in self._items ])
        else:
            mask = mask_or_cb

        return dlist([ self._items[i] for i,tf in enumerate(mask) if tf ])

    # () is for attribute fetching
    def __call__(self, key):
        return self.get(key)

    def get(self, *attrs):
        nattrs = len(attrs)
        if nattrs == 1:
            return dlseries([v.get(attrs[0], self._default) for v in self._items])
        elif nattrs > 1:
            return dlist([ { k:item.get(k, self._default) for k in attrs } for item in self._items ])
        else:
            raise IndexError("must pass at least one attribute to get")

    def _validate(self):
        assert all(isinstance(i, dict) for i in self._items)

    def append(self, d):
        if isinstance(d, dict):
            self._items.append(d)
        else:
            raise TypeError("Can only append dict (not %s)" % type(d))
        
    def __iadd__(self, other):
        if isinstance(other, list):
            self._items += other
        elif isinstance(other, dlist):
            self._items += other.items
        else:
            raise TypeError("cannot append object of type %s" % type(other))

        return self

    def __add__(self, other):
        if isinstance(other, list):
            return dlist(self._items + other)
        elif isinstance(other, dlist):
            return dlist(self._items + other.items)
        else:
            raise TypeError("cannot append object of type %s" % type(other))

    def __contains__(self, other):
        return other in self._items

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return "dlist(%s)" % str(self)

    def __setitem__(self, attr, vals):
        self._set(attr, vals)

    def __setattr__(self, attr, vals):
        # internal vars can use the normal behavior
        if attr.startswith('_'):
            object.__setattr__(self, attr, vals)
        else:
            # external attrs are treated as dict keys
            self._set(attr, vals)
        
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
            # return dlist([ self._items[i] for i,tf in enumerate(other) if not tf ])
            return self.where(~other)
        elif is_sequence(other):
            return dlist([ item for item in self._items if item not in other ])
        else:
            return dlist([ item for item in self._items if item is not other ])

    def __isub__(self, other):
        if isinstance(other, dlmask):
            self._items = [ self._items[i] for i,tf in enumerate(other) if not tf ]
        elif is_sequence(other):
            self._items = [ item for item in self._items if item not in other ]
        else:
            self._items = [ item for item in self._items if item is not other ]

        return self

    def apply(self, fn, reraise=False):
        out = dlist([])

        for item in self:
            try:
                out_item = fn(item)
            except:
                if reraise:
                    raise
                else:
                    out_item = {}

            out.append(out_item)
            
        return out

    def kapply(self, **kwargs):
        out = dlist([])
        for item in self:
            item = copy.deepcopy(item)

            for k,fn in kwargs.items():
                try:
                    item[k] = fn(item.get(k, self._default))
                except:
                    pass

            out.append(item)

        return out
            
                
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
    
