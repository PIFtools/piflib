import pandas as pd
import piflib.pif_calculator as pif

data = {'A': [1, 2, 3, 4],
        'B': ['a', 'b', 'c', 'd'],
        'C': ['blue', 'green', 'red', 'cyan']}
df_diverse = pd.DataFrame(data)

data = {'A': [1, 1, 1, 1],
        'B': ['a', 'a', 'a', 'a'],
        'C': ['red', 'red', 'red', 'red']}
df_same = pd.DataFrame(data)

data = {'A': [1, 1, 2, 2],
        'B': ['a', 'a', 'b', 'b'],
        'C': ['blue', 'green', 'red', 'cyan']}
df_fully_dependent = pd.DataFrame(data)



def test_compute_cigs():
    # if every value in a column is the same, then there is no information gain
    cigs = pif.compute_cigs(df_same)
    assert (cigs.A == 0).all()
    assert (cigs.B == 0).all()
    assert (cigs.C == 0).all()
    # every value has the same likelihood
    cigs = pif.compute_cigs(df_diverse)
    assert cigs.A.unique() == cigs.B.unique() == cigs.C.unique()
    assert len(cigs.A.unique() == 1)
    cigs = pif.compute_cigs(df_fully_dependent)
    assert (cigs.A == 1).all()
    assert (cigs.B == 1).all()
    assert (cigs.C == 1).all()


def test_compute_weighted_cigs():
    w_cigs = pif.compute_weighted_cigs(df_diverse)
    assert w_cigs.max().max() == 0
    assert w_cigs.min().min() == 0
    w_cigs = pif.compute_weighted_cigs(df_same)
    assert w_cigs.max().max() == 0
    assert w_cigs.min().min() == 0
    w_cigs = pif.compute_weighted_cigs(df_fully_dependent)
    # column A and B are fully dependent, thus weights are 0.
    assert (w_cigs.A == 0).all()
    assert (w_cigs.B == 0).all()
    assert (w_cigs.C == 0.5).all()


def test_compute_csfs():
    csfs = pif.compute_csfs(df_same)
    assert (csfs.A == 0).all()
    assert (csfs.B == 0).all()
    assert (csfs.C == 0).all()
    csfs = pif.compute_csfs(df_diverse)
    assert (csfs.A == 0.75).all()
    assert (csfs.B == 0.75).all()
    assert (csfs.C == 0.75).all()
    csfs = pif.compute_csfs(df_fully_dependent)
    assert (csfs.A == 0.5).all()
    assert (csfs.B == 0.5).all()
    assert (csfs.C == 0.25).all()
