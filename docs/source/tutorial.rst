.. _tutorial_toplevel:

==================
Tutorial
==================

dem uses a configuration `YAML <http://www.yaml.org/start.html>`_ file to define all the dependencies of the project.
Create the ``devenv.yaml`` file in the root directory of the project.

.. note:: The name of the file must be ``devenv.yaml``.

Add ``packages:`` to the top of the YAML file.  This denotes dependencies that are needed for all platforms.

List the first dependency under ``packages`` using the same syntax.  For example, the `boost library <http://www.boost.org/>`_ can be installed like this:

::

    packages:
        boost:
            version: 1.60.0
            type: url
            url: http://downloads.sourceforge.net/project/boost/boost/1.60.0/boost_1_60_0.zip
            destination: dependency

Running dem at this point will download and install boost to the ``PROJECT_ROOT/dependency``.  The download may take a long time so it would be recommended
to download large dependencies ahead of time and store them in a repository locally or on the local network.  This can be done by specifying a remote location.
Remote locations can be local or network locations.

Here the ``config`` block is introduced where ``remote_locations`` can be added.

::

    config:
        remote_locations: ['C:\repository', '\\mynetwork\repository]
    packages:
        boost:
            version: 1.60.0
            type: archive

A couple of things have been introduced here:

#. Two repositories were added where packages live
#. The package ``type`` has changed to archive
#. The package ``destination`` was removed

************
Destinations
************
 The destination property is used by dem to install the package into the preferred location.

* project-relative: Installs the dependency into the source tree of the project.  The value is a relative path from ``PROJECT_ROOT``.
* dependency-lib: A fixed type that installs the package into PROJECT_ROOT/.devenv/PROJECT_ROOT/dependencies
* python-site-packages: A fixed type that installs the package into PROJECT_ROOT/.devenv/PROJECT_ROOT/Lib/site-packages (Windows)
* bin: A fixed type that installs the package into PROJECT_ROOT/.devenv/PROJECT_ROOT/Scripts (Windows).  Packages installed in the bin will be on the %PATH%.

.. note::
On Linux

    * python packages get installed to PROJECT_ROOT/.devenv/PROJECT_ROOT/lib/python2.7/sitepackages
    * bin packages get installed to PROJECT_ROOT/.devenv/PROJECT_ROOT/bin

Usage

::

    boost:
        type: dependency-lib # Default
        type: python-site-packages
        type: bin
        type: code/source # Installs into PROJECT_ROOT/code/source