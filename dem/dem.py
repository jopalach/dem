import os
from zipfile import ZipFile

from . import DevEnvReader as reader


def get_dem_packages():
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    os.makedirs('devenv')

    if packages.has_a_library():
        libs_dir = os.path.join('devenv', 'libs')
        os.makedirs(libs_dir)

        for p in packages.archive_packages():
            if config.has_remote_locations():
                for remote_location in config['remote_locations']:
                    package_file = "{}-{}.zip".format(os.path.join(remote_location, p['name']), p['version'])
                    with ZipFile(package_file, 'r') as archive:
                        archive.extractall(os.path.join(libs_dir, p['name']))
