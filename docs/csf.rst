Cell Surprise Factor
====================

Whereas the CIG measures try to quantify the consequences of a breach, the Cell surprise factor (CSF) focuses on the
likelihood of a breach.

The different values of the known features form cohorts. The CIG describes the change in entropy of the unknown feature.
Thus, all cell values of the unknown features within the same cohort get assigned the same CIG value, irrespective of
how much the actual cell value contributed to the change in entropy.

We keep the same setting as with the CIG, assume we know all values of an entity but one. This gives us a prior and
posterior distribution. But instead of measuring the change of entropy of the unknown feature, we now look at the change of
probability for each value of the unknown feature separately.

Difference to CIG
~~~~~~~~~~~~~~~~~
Whereas the CIG quantifies the difference in information of a unknown cell value, the CSF measures the change in its
probability. The CIG measure the difference of two distributions, the CSF the difference of two probabilities.
There is a nice visualization of this in the CSF tutorial in the :doc:`tutorials` section.

The CSF is a measure of how unexpected a specific value is, given its context. Whereas the CIG measure how much
information is contained in that value within its contextual cohort.