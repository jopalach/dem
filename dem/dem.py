import os

from . import PackagesReader as reader


def get_dem_packages():
    packages = reader.packages_from_file('devenv.yaml')

    os.makedirs('devenv')

    if packages.has_a_library():
        os.makedirs(os.path.join('devenv', 'libs'))
