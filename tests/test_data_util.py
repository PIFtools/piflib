import pandas as pd
from piflib.data_util import complete_feature_priors

data = {'A': [1, 1, 2, 2],
        'B': ['a', 'a', 'b', 'b'],
        'C': ['blue', 'green', 'red', 'cyan']}
df_mix = pd.DataFrame(data)


def test_complete_feauture_priors_empty_prior():
    priors = complete_feature_priors(df_mix, {})
    assert len(priors) == len(df_mix.columns)
    # check we have an entry for every element
    for i, column in enumerate(df_mix.columns):
        assert set(df_mix[column].unique()) == priors[i].keys()
    for pv in priors[0].values():
        assert pv == 0.5
    for pv in priors[1].values():
        assert pv == 0.5
    for pv in priors[2].values():
        assert pv == 0.25
    for prior in priors.values():
        assert sum(prior.values()) == 1


def test_complete_feature_priors_full_prior():
    given_priors = {0: {1: 0.4, 2: 0.6},
                    1: {'a': 0.6, 'b': 0.4},
                    2: {'blue': 0.2, 'green': 0.3, 'red': 0.4, 'cyan': 0.1}}
    priors = complete_feature_priors(df_mix, given_priors)
    assert given_priors == priors


def test_complete_feature_priors_partial_prior():
    given_priors = {0: {1: 0.4, 2: 0.6}}
    priors = complete_feature_priors(df_mix, given_priors)
    assert len(priors) == len(df_mix.columns)
