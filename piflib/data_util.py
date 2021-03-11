import collections
import operator


def calculate_distribution(values, accuracy=1, feature_distribution=None):
    """Calculate the distribution of the values.

    If `accuracy` == 1, this function simply counts the values and
    normalises their counts into probabilities.

    If `accuracy` < 1, then it mixes the counts with the
    `feature_distribution`, which you can think of as a prior for the
    feature. We assume that we draw from `values` `accuracy` of the time
    and from `feature_distribution` 1 - `accuracy` of the time.

    The case where `accuracy` < 1 is slow.
    """
    assert accuracy == 1 or feature_distribution is not None
    counts = collections.Counter(values)
    total_counts = sum(counts.values())
    if accuracy == 1:
        return {v: c / total_counts for v, c in counts.items()}
    else:
        assert counts.keys() <= feature_distribution.keys()
        acc_tc = accuracy / total_counts
        onemacc = 1 - accuracy
        probs = ((v, counts[v] * acc_tc + p * onemacc)
                 for v, p in feature_distribution.items())
        return {v: p for v, p in probs if p > 0}


def complete_feature_priors(df, feature_priors):
    feature_priors = feature_priors.copy()
    for i in range(len(df.columns)):
        if i in feature_priors:
            fd = feature_priors[i]
            # TODO: consider if we need to check if complete?
        else:
            ffs = tuple(map(operator.itemgetter(i), df.values))
            fd = calculate_distribution(ffs)
        feature_priors[i] = fd
    return feature_priors
