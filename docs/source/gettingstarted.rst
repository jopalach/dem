.. _gettingstarted_toplevel:

==================
Getting Started
==================

Setting up a new or existing project is easy.

At the project's root directory create a configuration file that defines all the project's dependencies.
For now simply create **'devenv.yaml'**.  `YAML <http://yaml.org/>`_ was chosen as the configuration format so that anyone can easily modify the dependency list with ease.

.. note:: The configuration file must be **'devenv.yaml'**.

At this point, the dem tool can be run.  No dependencies have been configured yet, but the isolated environment can still be created.

.. sourcecode:: python

    from dem import dem
    dem.get_dem_packages()

The isolated environment is created at the root level of the project:
::
    <PROJECT_ROOT>/.devenv/<PROJECT_ROOT_NAME>
Inside the *.devenv* directory is the `python virtual environment <https://virtualenv.pypa.io/en/latest/>`_.
Technically designed for python, the virtual environment can be used for any project to create an isolated environment that does not pollute the system environment (Similar to a chroot or root jail).
::
    i.e Environment variables such as PATH, can impact other projects or applications

To enter the isolated environment:

:Windows:

::
    1. Open a Windows Command Prompt at the <PROJECT_ROOT>
        2. $ .devenv\\<PROJECT_ROOT_NAME>\\Scripts\\activate.bat

:Linux:

    ::
    1. Open a Bash Shell at the <PROJECT_ROOT>
    2. $ source .devenv/<PROJECT_ROOT_NAME>/bin/activate.bash

Notice the shell or command prompt now shows the project name:
::
        <PROJECT_ROOT_NAME>$

To leave the project environment simply run:
::
    $ deactivate

Now the system environment is back.

==================
Dependencies
==================
