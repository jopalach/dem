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
        self._update_package_with_install_path()

        for p in self._packages.archive_packages():
            if 'install_from' not in p:
                print("Could not find package: {}, version: {}".format(p['name'], p['version']))
            else:
                with ZipFile(p['install_from'], 'r') as archive:
                    archive.extractall(os.path.join(libs_dir, p['name']))

    def _update_package_with_install_path(self):
        for p in self._packages.archive_packages():
            for remote_location in self._config.remote_locations():
                    package_file = "{}-{}.zip".format(os.path.join(remote_location, p['name']), p['version'])
                    if os.path.isfile(package_file) and 'install_from' not in p:
                        p['install_from'] = package_file
