Introduction
------------
There are competing interests when it comes to data release:

- Privacy: The privacy of an individual's data must be preserved.
- Utility: The consumer of the data expects it to be complete and accurate.

In reality, these interests are often mutually exclusive. A complete and accurate dataset contains enough information to identify individuals.
Thus, a compromise has to be found that sits somewhere in between.

However, due to the lack of fine-grained metrics data custodians often err on the side of caution as privacy breaches have serious consequences.
This leads to datasets of limited use, or even data not being release at all.

What is a PIF
-------------
Risk can be divided into two parts:

- The likelihood of a breach
- And the severity (or consequences) of the breach.

In the context of data release, the likelihood of a breach is the chance of an attack succeeding, and the severity is the amount of information an attacker can gain.
The different PIFs are attempts to quantify these risks.

Attacker Model
~~~~~~~~~~~~~~
This risk cannot be evaluated in isolation, as personal information accumulates in the public space. In fact, most
recent data breaches utilized externally available personal data to de-identify individuals.

We model this from an attacker's point of view. The attacker's aim is to gain more information about individuals in the
dataset. Note that this is different to identifying the row associated with a specific individual. Narrowing down the possible rows for an individual
might already allow the attacker to reduce the uncertainty around some of the individual's personal information.

The attacker knows the distribution of the feature values for the population. This is not unrealistic, as many summary statistics are freely available (e.g. census).
In order to get the true risk, we model the worst case as this represent the highest risk. In terms of auxiliary data,
the worst case is that the attacker already knows everything about a target person but one value.

Our personal information factors aim to quantify the risk for that specific value, given that the attacker know all
other values of the corresponding individual.

Personal Information Factors
----------------------------
The personal information factors compute a risk value for each cell, thus providing a detailed risk landscape for the
whole dataset.
We believe that these risk values allow a data analyst to

- better understand the risk associated with the release of a dataset
- identify the areas in the dataset that need the most attention
- evaluate different treatments to identify the most suited one.

The cell information gain (CIG) quantifies the information that can be learned by an attacker,
whereas the cell surprise factor (CSF) quantifies the likelihood of an attack succeeding.
