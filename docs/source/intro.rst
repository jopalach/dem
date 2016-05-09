.. _intro_toplevel:

==================
Overview
==================

Development Environment Manager (dem) is a python library used to configure a project dependencies in a consistent fashion.  This is most useful
when working on a large project where multiple dependencies are required.

The dem tool creates an isolated environment that lives at the root level of project.  The environment contains a python virtual environment
and all of the project's dependencies.  Running the dem tool will initially setup the project's environment and download all dependencies of the project.
Running again will only update dependencies that have changed or will remove dependencies no longer needed.

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
