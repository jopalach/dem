import os
from zipfile import ZipFile


class ArchiveInstaller:
    def __init__(self, config, packages):
        self._config = config
        self._packages = packages

    def install_packages(self):
        if self._packages.has_a_library():
            libs_dir = os.path.join('devenv', 'libs')
            os.makedirs(libs_dir)

        for p in self._packages.archive_packages():
            if self._config.has_remote_locations():
                for remote_location in self._config['remote_locations']:
                    package_file = "{}-{}.zip".format(os.path.join(remote_location, p['name']), p['version'])
                    if os.path.isfile(package_file):
                        with ZipFile(package_file, 'r') as archive:
                            archive.extractall(os.path.join(libs_dir, p['name']))
                    else:
                        print("Could not find package: {}, version: {}".format(p['name'], p['version']))
