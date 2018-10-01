import pytest
from dlist import dlist
import numpy as np

@pytest.fixture()
def dl():
    return dlist([{'a':1}, {'b':2}, {'b': 3}])

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
    dl = dl + {'c': 2}
    assert len(dl) == old_len+1

    dl += {'c': 3}
    assert len(dl) == old_len+2

    assert np.nansum(np.array(dl.c, dtype=float)) == 5

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

    print(dl.s.isin(['hi',10],case=True))
    assert np.sum(dl.s.isin(['hi',10],case=False)) == 3

def test_sub(dl):
    newlen = len(dl - (dl.a == 1))
    assert newlen == (len(dl) - 1)
    dl -= (dl.a == 1)
    assert len(dl) == newlen
