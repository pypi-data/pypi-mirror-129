==============
preprocmachine
==============


.. image:: https://img.shields.io/pypi/v/preprocmachine.svg
        :target: https://pypi.python.org/pypi/preprocmachine

.. image:: https://img.shields.io/travis/yashm28sjsu/preprocmachine.svg
        :target: https://travis-ci.com/yashm28sjsu/preprocmachine

.. image:: https://readthedocs.org/projects/preprocmachine/badge/?version=latest
        :target: https://preprocmachine.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A tool to automate preprocessing phase.


* Free software: MIT license
* Documentation: https://preprocmachine.readthedocs.io.


Features
--------

* Takes a pandas dataframe as input along with target attribute
* Expandable library of self-contained modules containing preprocessing techniques available to use
        * Normalization
        * Imputation
        * Feature Selection
        * Outlier Detection
        * Duplicate Detection
* Provides flexibility to include a user defined preprocessing method if required
* Algorithm is flexible enough to work with any user defined ML algorithm
* Utilizes Epsilon greedy algorithm to determine the preprocessing steps
* Once algorithm execution is complete, it will return following:
        * Processed Dataset
        * metric to evaluate the performance  with comparison to performance before preprocessing
        * Series of Preprocessing Steps involved to reach this performance


Credits
-------

* Inspiration was taken from a published paper and open source project Learn2Clean: https://github.com/LaureBerti/Learn2Clean