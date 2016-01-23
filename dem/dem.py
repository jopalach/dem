import os

from . import PackagesReader as reader


def get_dem_packages():
    packages = reader.packages_from_file('dependencies.yaml')

    os.makedirs('devenv')
