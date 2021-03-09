Summarizing Personal Information Factors
========================================

The proposed personal information factors provide a detailed risk landscape across the whole dataset.
Sometimes it is useful to have single number representing the overall risk.
However, summarizing values removes some of the details, e.g.: an average removes the extreme values.


Feature Information Gain
--------------------------
FIG is given by summing all CIG values for each feature. The FIG can be
used to identify the features that provides the highest information gain. Higher information gain
corresponds to higher risk of of re-identification.
The risk of inclusion can be compared to the feature's
utility when making the decision to include or exclude it.


Row Information Gain
--------------------------

RIG is determined by summing all the CIG values in the row and is a
measure of the information gain associated with a particular individual if
their information is revealed through re-identification.

Caution
--------
We believe that single value summaries are too simplistic and should be used with caution.
