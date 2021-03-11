import collections

import matplotlib.pyplot as plt
import numpy as np

from piflib.data_util import calculate_distribution


def horizontal_bar_plot(results, category_names):

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(round(c, 2)) if c > 0 else '', ha='center', va='center',
                    color=text_color)
    fig.legend(ncol=len(category_names),
               loc='lower center', fontsize='small')

    return fig, ax


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
