"""Implement various entropy measures to improve CIG, RIG."""
import itertools
import numpy as np
import pandas as pd


def get_marginal(df, columns):
    """Return joint distribution of given columns.

    :param df: DataFrame that contains all observations
    :param columns: list of features to get joint distribution from

    :return dist: dict of outcome and corresponding probability
    """
    feature = list(df.columns)[0]
    d = pd.DataFrame(df.groupby(columns)[feature].count() / len(df))
    dist = d[feature].to_dict()
    return dist


def entropy(df, rvs):
    """Compute entropy of given random variables.

    :param df: Dataframe that contains all data
    :param rvs: list of feature names

    :return H: entropy of rvs
    """
    dist = get_marginal(df, rvs)
    ps = np.array(list(dist.values()))
    H = -sum(ps * np.log2(ps))
    return H


def mutual_information(df, rvs_X, rvs_Y):
    """Compute mutual information of two sets of random variables - MI(X; Y).

    :param df: Dataframe that contains all data
    :param rvs_X: list of feature names for set X
    :param rvs_Y: list of feature names for set Y

    :return I: mutual information
    """
    H_X = entropy(df, rvs_X)
    H_Y = entropy(df, rvs_Y)
    H_XY = entropy(df, rvs_X + rvs_Y)
    MI = H_X + H_Y - H_XY
    return(MI)


def pairwise_mutual_information(df):
    """Compute the mutual information between all pairs of features in the dataset.

    Returns 3 lists, names of first feature, names of second feature, mutual information between the two.

    :param df: Dataframe that contains all data

    :return x: list of names of first feature
    :return y: list of names of second feature
    :return mi_xy: list of mutual information between every pair of feature names
    """
    x = []
    y = []
    mi_xy = []
    for feature_1, feature_2 in itertools.combinations(df.columns, 2):
        x.append(feature_1)
        y.append(feature_2)
        mi_xy.append(mutual_information(df, [feature_1], [feature_2]))
    return x, y, mi_xy


def create_entropy_mi_table(df, round_digits=2):
    """Create a dataframe containing the individual features' entropies and the pairwise mutual information.

    :param df: Dataframe that contains all data
    :round_digits: integer that specifies the number of decimal to disply

    :return emi_df: DataFrame that contains all pairs of mutual information
    """
    x, y, mi = pairwise_mutual_information(df)
    entropies = {name: entropy(df, [name]) for name in df}
    hx = [entropies[i] for i in x]
    hy = [entropies[i] for i in y]
    emi_df = pd.DataFrame({'X': x, 'Y': y, 'H(X)': hx, 'H(Y)': hy, 'I(X;Y)': mi}).round(round_digits)
    return emi_df


def conditional_entropy(df, rvs_X, rvs_Y):
    """Compute conditional entropy of set X given set Y - H(X|Y).

    :param df: Dataframe that contains all data
    :param rvs_X: list of feature names for set X
    :param rvs_Y: list of feature names for set Y

    :return H_XgY: conditional entropy
    """
    MI_XY = mutual_information(df, rvs_X, rvs_Y)
    H_X = entropy(df, rvs_X)
    H_XgY = H_X - MI_XY
    return H_XgY


def create_conditional_entropy_table(df, round_digits=2):
    """Create a dataframe containing the individual features' entropies and the conditional entropy
    given the rest of all features.

    :param df: Dataframe that contains all data
    :round_digits: integer that specifies the number of decimal to disply

    :return cond_df: DataFrame that contains conditional entropy of every feature given the rest of features
    """
    x, y, hx, hy, co_en = [], [], [], [], []
    for feature in df.columns:
        f_ys = list(df.columns.drop(feature))
        x.append(feature)
        y.append(f_ys)
        hx.append(entropy(df, [feature]))
        hy.append(entropy(df, f_ys))
        co_en.append(conditional_entropy(df, [feature], f_ys))
    cond_df = pd.DataFrame({'X': x, 'Y': y, 'H(X)': hx, 'H(Y)': hy, 'H(X|Y)': co_en}).round(round_digits)
    return cond_df


def _set_diff(rv, rvs):
    return list(set(rvs) - set(rv))


def dual_total_correlation(df, rvs):
    """Compute dual total correlation of given rvs.

    It is the amount of information that is shared among the variables.

    :param df: Dataframe that contains all data
    :param rvs: list of feature names

    :return tc: total correlation
    """

    sum_cond_entropy = sum(conditional_entropy(df, [rv], _set_diff([rv], rvs)) for rv in rvs)
    joint_entropy = entropy(df, rvs)
    tc = joint_entropy - sum_cond_entropy
    return tc


def residual_entropy(df, rvs):
    """Compute dual total correlation of given rvs.

    It is dual in the sense that together they form the entropy of the distribution.

    :param df: Dataframe that contains all data
    :param rvs: list of feature names

    :return sum_cond_entropy: residual entropy
    """
    sum_cond_entropy = sum(conditional_entropy(df, [rv], _set_diff([rv], rvs)) for rv in rvs)
    return sum_cond_entropy
