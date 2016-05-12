===============================
Development Environment Manager
===============================
.. image:: https://travis-ci.org/nitehawck/dem.svg?branch=master 
        :target: https://travis-ci.org/nitehawck/dem

.. image:: https://img.shields.io/pypi/v/dem.svg 
        :target: https://pypi.python.org/pypi/dem
        
.. image:: https://readthedocs.org/projects/dem/badge/?version=latest
        :target: http://dem.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

==================
Overview
==================

*"Go get dem packages!" - dem creators*

Development Environment Manager (dem) is a python library used to manage a project dependencies in a consistent fashion.  This is most useful
when working on a large project where multiple dependencies are required.

Benefits:

* Easily setup the project in the same way every time
* Get new team members setup faster
* Keeps the system environment from getting polluted with project specifics
* Install dependencies from many different mediums

Types of dependencies supported:

* local/network archives and URLs (zips and tar.gz)
* `git <https://git-scm.com/>`_ repositories
* `yum <http://yum.baseurl.org/>`_ packages (Fedora based systems)
* `pip <https://pip.pypa.io>`_ packages

==================
Requirements
==================

dem is a multi-platform tool which currently works on Fedora and Windows based platforms.

Supported python versions:

* 2.7
* 3.3
* 3.4
* 3.5


==================
Install
==================

Installing dem is easily done using
`pip`_. Assuming it is
installed, just run the following from the command-line:

.. sourcecode:: none

    # pip install dem

This command will download the latest version of dem from the
`Python Package Index <http://pypi.python.org/pypi/dem>`_ and install it
to your system. More information about ``pip`` and pypi can be found
here:

* `install pip <https://pip.pypa.io/en/latest/installing.html>`_
* `pypi <https://pypi.python.org/pypi/dem>`_

.. _pip: https://pip.pypa.io/en/latest/installing.html

Alternatively, you can install from the distribution using the ``setup.py``
script:

.. sourcecode:: none

    # python setup.py install

.. note:: In this case, you have to manually install all requirements as well. It would be recommended to use the :ref:`git source repository <source-code-label>` in that case.

.. _source-code-label:
Source Code
===========

Development Environment Manager git repo is available on GitHub, which can be browsed at:
    * https://github.com/nitehawck/dem

and cloned using::

	$ git clone https://github.com/nitehawck/dem

Finally verify the installation by running the `nose powered <http://code.google.com/p/python-nose/>`_ unit tests::

    $ nosetests
