# What is `dlist`?

dlist is a `pandas`-like API for working with lists of dictionaries.

```python
from dlist import dlist

# initialize from a list of dicts
dl = dlist([ { 'a': 1 }, { 'a': 2, 'b': 'cat' } ])

# access keys as attributes or string keys
dl.a # [ 1, 2 ]
dl['a'] # ditto

# make masks via all the normal operators
dl['b'] == 'cat' # [ False, True ]

# caseless comparison, since that's nice
dl['b'].caseless_eq('CAT') # [ False, True ]
dl['b'].isin([ 1, 'CAT'], case=False) # [ False, True ]

# access things that don't exist (possibly a bad idea, but fun)
dl.c # [ None, None ]

# mildly fancy indexing
dl[dl.a >= 2] # [ { 'a': 2, 'b': 'cat' } ]

# assignment from a properly-sized sequence
dl.c = [ True, set([1,2]) ] # dlist([ { 'a': 1, 'c': True }, { 'a': 2, 'b': 'cat', 'c': {1, 2} } ])

# assignment from a non-sequence
dl.d = 4 # dlist([ { 'a': 1, 'c': True, 'd': 4 }, { 'a': 2, 'b': 'cat', 'c': {1, 2}, 'd': 4 } ])

# create a new attribute
dl.e = [ '1', 2 ] # dlist([{ ..., 'e': '1' }, { ..., 'e': 2 } ]) 
```

## Why didn't you just use `pandas`?

`pandas` wants to aggressively type everything.  I like the flexibility of dictionaries.  I suppose I could `dtype=object` and get most of this, but that felt icky.

## Why didn't you just use `<mongo/sqlite/tinydb/some-other-thing>`?

Sure, something like this probably already exists.  Also, maybe it's not even a good idea.  But it was fun to make.
