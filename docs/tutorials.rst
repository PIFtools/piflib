Tutorials
=========



running the tutorials
^^^^^^^^^^^^^^^^^^^^^

The notebooks can run online using binder.

.. image:: https://mybinder.org/badge_logo.svg
  :target: https://mybinder.org/v2/gh/PIFtools/piflib/master?filepath=docs/tutorials


Or you can download the tutorials from `github <https://github.com/PIFtools/piflib/tree/master/docs/tutorials>`_.
The dependencies are listed in `tutorials-requirements.txt`. Install and start Jupyter from the ``docs/tutorials``
directory::

    pip install -r tutorials-requirements.txt
    python -m jupyter lab


Finally, you can view a static version of the tutorials here.


.. toctree::
   :maxdepth: 1

   tutorials/tutorial_cig.ipynb
   tutorials/tutorial_csf.ipynb
