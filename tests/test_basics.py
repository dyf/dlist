import pytest
from dlist import dlist
import numpy as np

@pytest.fixture()
def dl():
    return dlist([{'a':1}, {'b':2}, {'b': 3, 'x':4 }])

def assert_lists_equal(l1, l2):
    assert len(l1) == len(l2)
    assert all(a1==a2 for a1,a2 in zip(l1, l2))
    
def test_get(dl):
    expected = [1, None, None]

    assert_lists_equal(dl('a'), expected)

    assert_lists_equal(dl.a, expected)

    assert len(dl.notthere) == len(dl)
    assert all(x is None for x in dl.notthere)

def test_str(dl):
    print(dl)


def test_add(dl):
    old_len = len(dl)
    dl = dl + [{'c': 2}]
    assert len(dl) == old_len+1

    dl += [{'c': 3}]
    assert len(dl) == old_len+2

    dl.append({'c': 3})
    assert len(dl) == old_len+3

    assert np.nansum(np.array(dl.c, dtype=float)) == 8

def test_mask(dl):
    assert np.sum(dl('a')>0) == 1
    assert np.sum(dl.b>2) == 1
    assert np.sum(dl.a.isin([2,3])) == 0

    assert np.sum((dl.b>=2) & (dl('b')<3)) == 1
    assert len(dl[dl.a == 1]) == 1


def test_set(dl):
    dl.e = 4
    assert all(x == 4 for x in dl.e)

def test_case(dl):
    v = [ 'Hi', 'hi', 10 ]
    dl.s = v

    assert np.sum(dl.s.caseless_eq('HI')) == 2
    assert np.sum(dl.s.isin(['hi',10])) == 2

    assert np.sum(dl.s.isin(['hi',10],case=False)) == 3

def test_sub(dl):
    newlen = len(dl - (dl.a == 1))
    assert newlen == (len(dl) - 1)
    dl -= (dl.a == 1)
    assert len(dl) == newlen

def test_get(dl):
    gdl = dl.get('b','x')

    assert len(gdl) == 3
    assert 'a' not in gdl[0]
    assert all('x' in item for item in gdl)
    assert all('b' in item for item in gdl)
    
    
def test_apply(dl):
    gdl = dl.apply(lambda x: {})
    assert all(len(item) == 0 for item in gdl)

    with pytest.raises(KeyError):
        gdl = dl.apply(lambda x: x['hi'], reraise=True)

    gdl = dl.apply(lambda x: { 'a': x['a'] }, reraise=False)
    for d,gd in zip(dl, gdl):
        if 'a' in d:
            assert gd['a'] == d['a']
        else:
            assert len(gd) == 0
            

def test_kapply(dl):
    gdl = dl.kapply(a=lambda a: "HIHI")
    assert all(gdl.a == "HIHI")

    gdl = dl.kapply(a=lambda a: a+1, b=lambda b: b-1)

    for d,gd in zip(dl, gdl):
        if 'a' in d:
            assert gd['a'] == d['a']+1
        if 'b' in d:
            assert gd['b'] == d['b']-1



    
    
    
