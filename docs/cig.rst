Cell Information Gain
=====================

For simplicity, it is assumed that every cell belongs to a row, and every individual is
represented by exactly one row.
The CIG quantifies the information gained by learning the value of a cell, given that one already knows all the other
cell values of this individual.

We use entropy to measure information. The entropy of a random variable is the average level of uncertainty inherent in
the variable's possible outcomes.

As the attacker already has an expectation of the distribution (prior) of that variable, we define the CIG as the
change in entropy (or KL-divergence) between the prior and posterior distribution.

Example
-------
Consider the following dataset

======= ========= =============
Gender  Eye color Occupation
======= ========= =============
male    blue      dentist
female  blue      dentist
male    green     accountant
male    green     accountant
======= ========= =============

For the sake of exposition, we focus on the feature 'Gender'.

First, we need the 'Gender's prior distribution. There are
51% males and 49% females in the Australian population. Then 0.51 and 0.49 form the prior distribution.

========  ==================
Feature   Prior Distribution
========  ==================
male      0.51
female    0.49
========  ==================

Knowing values for 'Eye color' and 'Occupation' gives context. The posterior distribution of 'Gender' is the conditional
distribution given its context.

The posterior of 'Gender' is given by P(Gender|Eye color, Occupation) as follows:

=========  ==========  ====================================  ======================================
Eye color  Occupation  P(Gender=male|Eye color, Occupation)  P(Gender=female|Eye color, Occupation)
=========  ==========  ====================================  ======================================
blue       dentist     0.5                                   0.5
green      accountant  1                                     0
=========  ==========  ====================================  ======================================

We can see that the posterior distribution for the blue-eyed dentists is very similar to the population prior.
As the distribution of 'Gender' within the cohort of blue-eyed dentists is essentially the same as the population prior,
we associate little risk with 'Gender' values for this cohort. The posterior distribution of 'Gender' for the green-eyed
accountants on the other hand is significantly different from the prior. Thus there is more information to be gained.



