import os

from PackagesReader import packages_from_file as read


def get_dem_packages():
    packages = read('dependencies.yaml')

    os.makedirs('dependencies')
