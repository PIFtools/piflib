Weighted Cell Information Gain
==============================

The CIG assumes that the unknown feature is independent from all other features.
Features containing personal information often have inter-dependencies, e.g. firstnames and gender, or postcode
and income.

One can look at the CIG as the worst-case scenario. Nothing of the uncertainty of the unknown feature can be explained
by the other features.

The Weighted Cell Information Gain explores the best-case scenario: we assume that all observed correlations are due to
causal dependencies between the features.

Let :math:`X_j` be the unknown feature. Then :math:`H(X_j)`, the entropy of feature :math:`j`, describes the amount of
information contained in that feature.
The conditional entropy :math:`H\left(X_{j} \mid X_{1}, \ldots, X_{j-1}, X_{j+1}, \ldots, X_{m}\right)` describes the
amount of information contained in feature :math:`j`, given that all other feature values are known (taking all possible
correlations into account).

Dividing the conditional entropy by the entropy of the feature, we get a factor that describes what fraction of the
information in a feature can not be explained by the correlations with all other features.

.. math::
 w_j =\frac{H\left(X_{j} \mid X_{1}, \ldots, X_{j-1}, X_{j+1}, \ldots, X_{m}\right)}{H(X_j)},

The wCIG is defined as the CIG value multiplied by factor :math:`w_j`.

.. math::
 wCIG(i,j) = w_j * CIG(i, j)

Caution
~~~~~~~
Correlation does not mean causation. A trivial counterexample is the following dataset:

== ==
A  B
== ==
a  b
c  r
f  e
== ==

There is a perfect correlation between feature A and B, thus all wCIG values are zero. However, there is no causal
relationship between the two.
In fact, the CIG values are quite high, as all values are unique.