
import collections
import math
import operator
import random
import itertools


import pandas as pd
import numpy as np

from piflib.data_util import calculate_distribution, complete_feature_priors
from piflib.entropy import create_conditional_entropy_table


def compute_cigs(dataframe,
                 feature_priors={},
                 feature_accuracies={},
                 samples=None):
    """Compute the cell information gain (CIG) for all cells in the dataset.

    Find the risk (as KL divergence from prior) for all attributes.

    :param dataframe: a Pandas DataFrame object containing tabular data
    :param feature_priors: feature_priors are optional. It is a dictionary mapping the
        feature index to an assumed prior. If not provided, the prior for
        the feature is calculated from the global distribution.
    :param feature_accuracies: `feature_accuracies` maps the feature index to the accuracy of the
        feature. If not provided for a feature, it defaults to 1.
    :return: a Pandas DataFrame containing the CIG values. The CIG values are at the same index as their corresponding
        cell values in the input dataframe.
    """
    unknown_features = 1
    dataset = dataframe.values
    l = len(dataset[0])
    assert all(len(row) == l for row in dataset)

    feature_priors = complete_feature_priors(dataframe, feature_priors)

    feature_accuracies = feature_accuracies.copy()
    for i in range(l):
        if i not in feature_accuracies:
            feature_accuracies[i] = 1

    feature_counts = [0] * l
    feature_kls = [[0] * len(dataset) for _ in range(l)]
    for is_ in sample_is(l, unknown_features, samples):
        feature_kls_this = find_kls_for_features(
            dataset,
            is_,
            feature_priors,
            feature_accuracies)
        for i, feature_kl in zip(is_, feature_kls_this):
            feature_kl_previous = feature_kls[i]
            feature_kls[i] = tuple(map(
                operator.add, feature_kl, feature_kl_previous))

        for i in is_:
            feature_counts[i] += 1

    for i, denom in enumerate(feature_counts):
        feature_kls[i] = tuple(map(
            operator.truediv,
            feature_kls[i],
            itertools.repeat(denom)))

    return pd.DataFrame(list(zip(*feature_kls)), columns=dataframe.columns)


def compute_weighted_cigs(dataframe, feature_priors={}, feature_accuracies={}):
    """Compute the Weighted Cell Information Gain (wCIG) for all cells in the dataset.

    Find the risk (as KL divergence from prior) for all attributes.

    :param dataframe: a Pandas DataFrame object containing tabular data
    :param feature_priors: feature_priors are optional. It is a dictionary mapping the
        feature index to an assumed prior. If not provided, the prior for
        the feature is calculated from the global distribution.
    :param feature_accuracies: `feature_accuracies` maps the feature index to the accuracy of the
        feature. If not provided for a feature, it defaults to 1.
    :return: a Pandas DataFrame containing the wCIG values. The wCIG values are at the same index as their
        corresponding cell values in the input dataframe.
        """
    cigs = compute_cigs(dataframe, feature_priors=feature_priors, feature_accuracies=feature_accuracies)
    cond_entropy = create_conditional_entropy_table(dataframe)
    weights = cond_entropy['H(X|Y)'].values / cond_entropy['H(X)']
    weights = np.nan_to_num(weights)
    return (cigs * weights).round(2)


def compute_csfs(df, feature_priors={}, feature_accuracies={}):
    """Compute the Cell Surprise Factor (CSF) for all cells in the dataset.

    The CSF id defined as the change in probability for a cell value between the prior and the posterior distribution.

    :param dataframe: a Pandas DataFrame object containing tabular data
    :param feature_priors: feature_priors are optional. It is a dictionary mapping the
        feature index to an assumed prior. If not provided, the prior for
        the feature is calculated from the global distribution.
    :param feature_accuracies: `feature_accuracies` maps the feature index to the accuracy of the
        feature. If not provided for a feature, it defaults to 1.
    :return: a Pandas DataFrame containing the CSF values. The CSF values are at the same index as their
        corresponding cell values in the input dataframe.
    """
    dataset = df.values
    l = len(dataset[0])
    # compute priors
    feature_priors = complete_feature_priors(df, feature_priors)
    feature_accuracies = feature_accuracies.copy()
    for i in range(l):
        if i not in feature_accuracies:
            feature_accuracies[i] = 1
    feature_csfs = [[0] * len(dataset) for _ in range(l)]
    for is_ in sample_is(l, 1, None):
        feature_csfs[is_[0]] = apply_to_posterior_and_prior(
            dataset,
            is_,
            feature_priors,
            feature_accuracies,
            calculate_prob_change)

    return pd.DataFrame(list(zip(*feature_csfs)), columns=df.columns)


def compute_posterior_distributions(feature, df):
    known_features = tuple(col_name for col_name in df.columns if col_name != feature)
    bucket = collections.defaultdict(list)
    bucket_map = []
    for idx, row in df.iterrows():
        key = tuple(row[known_feature] for known_feature in known_features)
        bucket[key].append(row[feature])
        bucket_map.append(key)
    bucket_distributions = {key: calculate_distribution(el_bucket) for key, el_bucket in bucket.items()}
    feature_vals = df[feature].unique()
    dists = {}
    for key, distribution in bucket_distributions.items():
        dists[str(key)] = [distribution.get(feature_val, 0) for feature_val in feature_vals]
    return dists, feature_vals


def binom(n, r):
    """ return binomial coefficient: n choose k"""
    return math.factorial(n) // math.factorial(n - r) // math.factorial(r)


def sample_is(n, r, samples):
    if samples is None:
        yield from itertools.combinations(range(n), r)
    else:
        total_combinations = binom(n, r)
        if samples > total_combinations:
            raise ValueError('more samples than combinations')
        if samples >= total_combinations >> 1:
            all_combinations = list(itertools.combinations(range(n), r))
            random.shuffle(all_combinations)

            num_produced = 0
            feature_produced = [False] * n
            for i, comb in enumerate(all_combinations):
                if num_produced >= samples:
                    break
                if all(map(feature_produced.__getitem__, comb)):
                    continue
                for j in comb:
                    feature_produced[j] = True
                num_produced += 1
                all_combinations[i] = None
                yield comb

            for comb in all_combinations:
                if num_produced >= samples:
                    break
                if comb is not None:
                    yield comb
        else:
            already_produced = set()
            feature_produced = [False] * n
            while len(already_produced) < samples:
                comb = random.sample(range(n), r)
                comb = tuple(sorted(comb))
                if (comb not in already_produced
                        and (all(already_produced)
                             or not all(map(already_produced.__getitem__,
                                            comb)))):
                    already_produced.add(comb)
                    for i in comb:
                        feature_produced[i] = True
                    yield comb


def apply_to_posterior_and_prior(dataset, feature_idx, prior_distributions, accuracies, fun):
    l = len(dataset[0])
    assert all(len(row) == l for row in dataset)
    feature_idx = feature_idx[0]
    buckets = collections.defaultdict(list)
    bucket_map = []
    for row in dataset:
        key = tuple(row[i] for i in range(l) if not i == feature_idx)
        buckets[key].append(row[feature_idx])
        bucket_map.append((key, row[feature_idx]))
    bucket_values = {
            key: fun(
                calculate_distribution(bucket,
                                       accuracy=accuracies[feature_idx],
                                       feature_distribution=prior_distributions[feature_idx]),
                prior_distributions[feature_idx])
            for key, bucket in buckets.items()}
    return [bucket_values[post_key][val] for post_key, val in bucket_map]


def find_kls_for_features(dataset, feature_is, feature_distributions, accuracies):
    """Find the KL divergence of feature values against the prior.

    We find the true distribution of the features taking into account
    the accuracy. We then compute the KL divergence.
    """
    l = len(dataset[0])
    assert all(len(row) == l for row in dataset)

    # one bucket per set of 'known' features
    buckets = [collections.defaultdict(list) for _ in range(len(feature_is))]
    bucket_map = [[] for _ in range(len(feature_is))]  ########
    for row in dataset:
        key = tuple(row[i] for i in range(l) if i not in feature_is)
        for i, j in enumerate(feature_is):
            buckets[i][key].append(row[j])
            bucket_map[i].append(key)

    bucket_kls = [
        {
            key: calculate_kl(
                calculate_distribution(bucket,
                                       accuracy=accuracies[feature_is[i]],
                                       feature_distribution=feature_distributions[feature_is[i]]),
                feature_distributions[feature_is[i]])
            for key, bucket in feature_buckets.items()}
        for i, feature_buckets in enumerate(buckets)]

    return [tuple(map(bucket_kls[i].__getitem__, bucket_map[i]))
            for i in range(len(feature_is))]


def calculate_kl(p, q):
    """Calculate D_KL(P || Q) (the KL-divergence) in bits.

    D_KL(P || Q) is the `information gained when one revises one's
    beliefs from the prior probability distribution Q to the posterior
    probability distribution P`. (Wikipedia, Kullback–Leibler
    divergence)

    `p` and `q` are both dictionaries mapping some hashable to a number.
    It is assumed that they are both normalised: their values should add
    up to 0. `q` must not have any 0 values unless the corresponding `p`
    value is also 0.
    """
    return sum(pk * math.log2(pk / q[k])
               for k, pk in p.items()
               if pk > 0)


def calculate_prob_change(p, q):
    """ calculate the change in probability for each element of the posterior compared to the prior"""
    return {k: abs(v - q[k]) for k, v in p.items()}
