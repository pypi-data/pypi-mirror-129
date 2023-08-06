========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-publishnewsextratorp/badge/?style=flat
    :target: https://python-publishnewsextratorp.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/JonasBrother97/python-publishnewsextratorp.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/JonasBrother97/python-publishnewsextratorp

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/JonasBrother97/python-publishnewsextratorp?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/JonasBrother97/python-publishnewsextratorp

.. |requires| image:: https://requires.io/github/JonasBrother97/python-publishnewsextratorp/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/JonasBrother97/python-publishnewsextratorp/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/JonasBrother97/python-publishnewsextratorp/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/JonasBrother97/python-publishnewsextratorp

.. |version| image:: https://img.shields.io/pypi/v/publishnewsextratorp.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/publishnewsextratorp

.. |wheel| image:: https://img.shields.io/pypi/wheel/publishnewsextratorp.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/publishnewsextratorp

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/publishnewsextratorp.svg
    :alt: Supported versions
    :target: https://pypi.org/project/publishnewsextratorp

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/publishnewsextratorp.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/publishnewsextratorp

.. |commits-since| image:: https://img.shields.io/github/commits-since/JonasBrother97/python-publishnewsextratorp/v0.0.6.svg
    :alt: Commits since latest release
    :target: https://github.com/JonasBrother97/python-publishnewsextratorp/compare/v0.0.6...master



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install publishnewsextratorp

You can also install the in-development version with::

    pip install https://github.com/JonasBrother97/python-publishnewsextratorp/archive/master.zip


Documentation
=============


https://python-publishnewsextratorp.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
