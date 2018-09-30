# What is `dlist`?

dlist is a `pandas`-like API for working with lists of dictionaries.

```python
>>> from dlist import dlist
>>> dl = dlist([ { 'a': 1 }, { 'a': 2, 'b': 'cat' } ])
>>> dl.a # [ 1, 2 ]
>>> dl['b'] == 'cat' # [ False, True ]
>>> dl.c # [ None, None ]
>>> dl[dl.a >= 2] # [ { 'a': 2, 'b': 'cat' } ]
>>> dl.c = [ True, set(1,2) ] # dlist([ { 'a': 1, 'c': True }, { 'a': 2, 'b': 'cat', 'c': set(1,2) } ])
>>> dl.d = 4 # dlist([ { 'a': 1, 'c': True, 'd': 4 }, { 'a': 2, 'b': 'cat', 'c': set(1,2), 'd': 4 } ])
>>> dl.d = [ 'first', 'second' ] # dlist([ { 'a': 1, 'c': True, 'd': 'first' }, { 'a': 2, 'b': 'cat', 'c': set(1,2), 'd': 'second' } ])
```

## Why didn't you just use `pandas`?

`pandas` wants to aggressively type everything.  I like the flexibility of dictionaries.  

## Why didn't you just use `<mongo/sqlite/something>`?

I'm sure something like this already exists.  Making this sounded fun.
