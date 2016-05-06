import gzip
import os
from tarfile import TarFile
from zipfile import ZipFile


class ArchiveInstaller:
    def __init__(self, project, config, packages):
        self._config = config
        self._packages = packages
        self._project = project

    def install_packages(self):
        libs_dir = os.path.join('.devenv', self._project, 'dependencies')
        self._update_package_with_install_path()

        for p in self._packages.archive_packages():
            if 'install_from' not in p:
                print("Could not find package: {}, version: {}".format(p['name'], p['version']))
            else:
                if p['install_from_ext'] == 'zip':
                    with ZipFile(p['install_from'], 'r') as archive:
                        archive.extractall(os.path.join(libs_dir, p['name']))
                elif p['install_from_ext'] == 'tar.gz':
                    with TarFile.open(p['install_from'], 'r:gz') as archive:
                        archive.extractall(os.path.join(libs_dir, p['name']))
                elif p['install_from_ext'] == 'tar.bz2':
                    with TarFile.open(p['install_from'], 'r:bz2') as archive:
                        archive.extractall(os.path.join(libs_dir, p['name']))
                elif p['install_from_ext'] == 'gz':
                    with gzip.open(p['install_from'], 'r') as archive:
                        archive.extractall(os.path.join(libs_dir, p['name']))

    def _update_package_with_install_path(self, supported_extensions=['zip', 'tar.gz', 'tar.bz2', '.gz']):
        for p in self._packages.archive_packages():
            for remote_location in self._config.remote_locations():
                for extension in supported_extensions:
                    package_file = "{}-{}.{}".format(os.path.join(remote_location, p['name']), p['version'], extension)
                    if os.path.isfile(package_file) and 'install_from' not in p:
                        p['install_from'] = package_file
                        p['install_from_ext'] = extension
