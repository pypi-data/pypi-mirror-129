.. -*- mode: rst -*-

chainladder (python)
====================

|PyPI version| |Conda Version| |Build Status| |codecov io| |Documentation Status|

chainladder - Property and Casualty Loss Reserving in Python
------------------------------------------------------------

This package gets inspiration from the popular `R ChainLadder package`_.

This package strives to be minimalistic in needing its own API. Think in
`pandas`_ for data manipulation and `scikit-learn`_ for model
construction. An actuary already versed in these tools will pick up this
package with ease. Save your mental energy for actuarial work.


Documentation
-------------

Please visit the `Documentation`_ page for examples, how-tos, and source
code documentation.


Available Estimators
--------------------

``chainladder`` has an ever growing list of estimators that work seemlessly together:

.. _R ChainLadder package: https://github.com/mages/ChainLadder
.. _pandas: https://pandas.pydata.org/
.. _scikit-learn: https://scikit-learn.org/latest/index.html

.. |PyPI version| image:: https://badge.fury.io/py/chainladder.svg
   :target: https://badge.fury.io/py/chainladder

.. |Conda Version| image:: https://img.shields.io/conda/vn/conda-forge/chainladder.svg
   :target: https://anaconda.org/conda-forge/chainladder

.. |Build Status| image:: https://github.com/casact/chainladder-python/workflows/Unit%20Tests/badge.svg

.. |Documentation Status| image:: https://readthedocs.org/projects/chainladder-python/badge/?version=latest
   :target: http://chainladder-python.readthedocs.io/en/latest/?badge=latest

.. |codecov io| image:: https://codecov.io/github/casact/chainladder-python/coverage.svg?branch=latest
   :target: https://codecov.io/github/casact/chainladder-python?branch=latest


+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| Loss                         | Tails Factors    | IBNR Models             | Adjustments           | Workflow              |
| Development                  |                  |                         |                       |                       |
+==============================+==================+=========================+=======================+=======================+
| `Development`_               | `TailCurve`_     | `Chainladder`_          | `BootstrapODPSample`_ | `VotingChainladder`_  |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `DevelopmentConstant`_       | `TailConstant`_  | `MackChainladder`_      | `BerquistSherman`_    |  `Pipeline`_          |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `MunichAdjustment`_          | `TailBondy`_     | `BornhuettterFerguson`_ | `ParallelogramOLF`_   | `GridSearch`_         |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `ClarkLDF`_                  | `TailClark`_     | `Benktander`_           | `Trend`_              |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `IncrementalAdditive`_       |                  | `CapeCod`_              |                       |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `CaseOutstanding`_           |                  |                         |                       |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `TweedieGLM`_                |                  |                         |                       |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `DevelopmentML`_             |                  |                         |                       |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+
| `BarnettZehnwirth`_          |                  |                         |                       |                       |
+------------------------------+------------------+-------------------------+-----------------------+-----------------------+


.. _Development: https://chainladder-python.readthedocs.io/en/latest/development.html#development
.. _TailCurve: https://chainladder-python.readthedocs.io/en/latest/tails.html#tailcurve
.. _Chainladder: https://chainladder-python.readthedocs.io/en/latest/methods.html#chainladder
.. _BootstrapODPSample: https://chainladder-python.readthedocs.io/en/latest/adjustments.html#bootstrapodpsample
.. _DevelopmentConstant: https://chainladder-python.readthedocs.io/en/latest/development.html#developmentconstant
.. _TailConstant: https://chainladder-python.readthedocs.io/en/latest/tails.html#tailconstant
.. _MackChainladder: https://chainladder-python.readthedocs.io/en/latest/methods.html#mackchainladder
.. _BerquistSherman: https://chainladder-python.readthedocs.io/en/latest/adjustments.html#berquistsherman
.. _MunichAdjustment: https://chainladder-python.readthedocs.io/en/latest/development.html#munichadjustment
.. _TailBondy: https://chainladder-python.readthedocs.io/en/latest/tails.html#tailbondy
.. _BornhuettterFerguson: https://chainladder-python.readthedocs.io/en/latest/methods.html#bornhuetterferguson
.. _Pipeline: https://chainladder-python.readthedocs.io/en/latest/workflow.html#pipeline
.. _ClarkLDF: https://chainladder-python.readthedocs.io/en/latest/development.html#clarkldf
.. _TailClark: https://chainladder-python.readthedocs.io/en/latest/tails.html#tailclark
.. _Benktander: https://chainladder-python.readthedocs.io/en/latest/methods.html#benktander
.. _GridSearch: https://chainladder-python.readthedocs.io/en/latest/workflow.html#gridsearch
.. _IncrementalAdditive: https://chainladder-python.readthedocs.io/en/latest/development.html#incrementaladditive
.. _CapeCod: https://chainladder-python.readthedocs.io/en/latest/methods.html#capecod
.. _ParallelogramOLF: https://chainladder-python.readthedocs.io/en/latest/adjustments.html#parallelogramolf
.. _VotingChainladder: https://chainladder-python.readthedocs.io/en/latest/workflow.html#votingchainladder
.. _Trend: https://chainladder-python.readthedocs.io/en/latest/adjustments.html#trend
.. _CaseOutstanding: https://chainladder-python.readthedocs.io/en/latest/development.html#caseoutstanding
.. _TweedieGLM: https://chainladder-python.readthedocs.io/en/latest/development.html#tweedieglm
.. _DevelopmentML: https://chainladder-python.readthedocs.io/en/latest/development.html#developmentml
.. _BarnettZehnwirth: https://chainladder-python.readthedocs.io/en/latest/development.html#barnettzehnwirth
.. _Documentation: https://chainladder-python.readthedocs.io/en/latest/

Getting Started Tutorials
-------------------------

Tutorial notebooks are available for download `here`_.

* `Working with Triangles`_
* `Selecting Development Patterns`_
* `Extending Development Patterns with Tails`_
* `Applying Deterministic Methods`_
* `Applying Stochastic Methods`_
* `Large Datasets`_

Installation
------------

To install using pip: ``pip install chainladder``

To instal using conda: ``conda install -c conda-forge chainladder``

Alternatively for pre-release functionality, install directly from github:
``pip install git+https://github.com/casact/chainladder-python/``

Note: This package requires Python>=3.5 pandas 0.23.0 and later,
sparse 0.9 and later, scikit-learn 0.23.0 and later.

Questions or Ideas?
--------------------

Join in on the `github discussions`_.  Your question is more likely to get answered
here than on Stack Overflow.  We're always happy to answer any usage
questions or hear ideas on how to make ``chainladder`` better.


Want to contribute?
-------------------

Check out our `contributing guidelines`_.

.. _here: https://github.com/casact/chainladder-python/tree/latest/docs/tutorials
.. _Working with Triangles: https://chainladder-python.readthedocs.io/en/latest/tutorials/triangle-tutorial.html
.. _Selecting Development Patterns: https://chainladder-python.readthedocs.io/en/latest/tutorials/development-tutorial.html
.. _Extending Development Patterns with Tails: https://chainladder-python.readthedocs.io/en/latest/tutorials/tail-tutorial.html
.. _Applying Deterministic Methods: https://chainladder-python.readthedocs.io/en/latest/tutorials/deterministic-tutorial.html
.. _Applying Stochastic Methods: https://chainladder-python.readthedocs.io/en/latest/tutorials/stochastic-tutorial.html
.. _Large Datasets: https://chainladder-python.readthedocs.io/en/latest/tutorials/large-datasets.html
.. _github discussions: https://github.com/casact/chainladder-python/discussions
.. _contributing guidelines: https://chainladder-python.readthedocs.io/en/latest/contributing.html
