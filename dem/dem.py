import os

from . import DevEnvReader as reader


def get_dem_packages():
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    os.makedirs('devenv')

    if packages.has_a_library():
        os.makedirs(os.path.join('devenv', 'libs'))
