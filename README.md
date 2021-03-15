# piflib - computing personal information factors (PIF)

[![Documentation Status](https://readthedocs.org/projects/piflib/badge/?version=latest)](https://piflib.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/PIFtools/piflib/actions/workflows/python-test.yml/badge.svg)](https://github.com/PIFtools/piflib/actions/workflows/python-test.yml)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=PIFtools/piflib)](https://dependabot.com)

## Installation
This library requires Python3. To install, execute

`pip install piflib`

## Usage
piflib expects the data as a [Pandas](https://pandas.pydata.org/) DataFrame. Luckily, [Pandas supports
a wide range](https://pandas.pydata.org/docs/user_guide/io.html) of input formats.

In this example, we have data in csv format. 

```
import pandas as pd
import piflib

dataframe = pd.read_csv('datafile.csv')
cigs = piflib.compute_cigs(dataframe)
csfs = piflib.compute_csfs(dataframe)
```

The `compute_cigs` and `compute_csfs` functions return a Pandas DataFrame, containing the CIG and CSF values 
respectively. The CIG and CSF values appear in the same position as in the input data.

You can run and experiment with the tutorials online here:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PIFtools/piflib/main?filepath=docs%2Ftutorials)


## What does it do? How does it work?
The documentation can be found [here](https://piflib.readthedocs.io/en/latest).

## Limitations
Piflib currently only supports discrete feature distributions.

## Copyright
Copyright 2021 CSIRO's Data61

## License
Piflib is released under the Apache-2 license.
Unless required by applicable law or agreed to in writing, software distributed under this license is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [license](https://github.com/PIFtools/piflib/blob/main/LICENSE) for the specific language governing permissions and limitations.

## Citing
Piflib is designed, developed and supported by [CSIRO's Data61](https://www.data61.csiro.au/). If you use any part
of this library in your research, please cite it using the following BibTex entry:

    @misc{piflib,
      author = {CSIRO's Data61},
      title = {piflib - computing personal information factors},
      year = {2021},
      publisher = {GitHub},
      journal = {GitHub Repository},
      howpublished = {\url{https://github.com/PIFtools/piflib}},
    }


## Thank You
We want to thank Jakub Nabaglo and Joyce Yu for their contributions to this codebase.
