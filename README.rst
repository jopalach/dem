Development Environment Manager
========================
.. image:: https://travis-ci.org/nitehawck/dem.svg?branch=master
    :target: https://travis-ci.org/nitehawck/dem
    
Overview
------------------------
An agnostic library/package manager for setting up a development project environment.  Dependencies are necessary for most projects and are seldom installed and maintained correctly.

Key features:
- Installs a Python virtual environment
- Installs packages within the project only

Supports installing from packages existing in:
 - Local filesystem
 - URL's
 - Yum packages

Getting Started
------------------------
Create a devenv.yaml configuration file in your project's root directory.

.. code-block:: yaml

    config:
       remote-locations: ['/var/myRepo/', '//network/myRepo']
    packages:
      json:
          version: 1.53.3
          type: archive
          destination: python-site-packages
      git-python:
          version: 2
          type: url
          url: https://github.com/gitpython-developers/GitPython/archive/0.3.6.tar.gz
     packages-linux:
      alien:
          version: 2.3
          type: rpm

