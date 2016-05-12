import gzip
import os
from tarfile import TarFile
from zipfile import ZipFile

from dem.project.pkgconfig import PkgConfigProcessor


class ArchiveInstaller:
    def __init__(self, project, config, packages, cache):
        self._config = config
        self._packages = packages
        self._project = project
        self._cache = cache

    def install_packages(self):
        self._update_package_with_install_path()
        installed_packages = []
        for p in self._packages:
            if 'install_from' not in p:
                print("[dem] Could not find package: {}, version: {}".format(p['name'], p['version']))
            else:
                if not self._cache.is_package_installed(p['name'], p['version']):
                    print('[dem] installing {}-{}'.format(p['name'], p['version']))
                    if p['install_from_ext'] == 'zip':
                        with ZipFile(p['install_from'], 'r') as archive:
                            locations = self._extract(archive, p)
                    elif p['install_from_ext'] == 'tar.gz':
                        with TarFile.open(p['install_from'], 'r:gz') as archive:
                            locations = self._extract(archive, p)
                    elif p['install_from_ext'] == 'tar.bz2':
                        with TarFile.open(p['install_from'], 'r:bz2') as archive:
                            locations = self._extract(archive, p)
                    elif p['install_from_ext'] == 'gz':
                        with gzip.open(p['install_from'], 'r') as archive:
                            locations = self._extract(archive, p)

                    if 'pkg-config' in p:
                        PkgConfigProcessor.replace_prefix(locations, p['pkg-config'])
                else:
                    print('[dem] {}-{} already installed'.format(p['name'], p['version']))
                    locations = self._cache.install_locations(p['name'])
                package = dict()
                package[p['name']] = {'version': p['version'], 'type': 'local', 'install_locations': locations}
                installed_packages.append(package)
        return installed_packages

    def _extract(self, archive, p):
        destination_dir = p['platform-destination-path']
        destination_dir = os.path.join(destination_dir)
        archive.extractall(destination_dir)
        return [os.path.join(destination_dir, path) for path in self._installed_file_base_paths(archive, p)]

    @staticmethod
    def _installed_file_base_paths(archive, p):
        installed_file_base_paths = []
        if p['install_from_ext'] == 'zip':
            members = archive.infolist()
            for member in members:
                if '/' not in member.filename:
                    installed_file_base_paths.append(member.filename)
                else:
                    base = member.filename.split('/')[0]
                    if base not in installed_file_base_paths:
                        installed_file_base_paths.append(base)
        elif p['install_from_ext'] == 'tar.gz' or p['install_from_ext'] == 'tar.bz2':
            members = archive.getmembers()
            for member in members:
                if '/' not in member.name:
                    installed_file_base_paths.append(member.name)
                else:
                    base = member.name.split('/')[0]
                    if base not in installed_file_base_paths:
                        installed_file_base_paths.append(base)
        return installed_file_base_paths

    def _update_package_with_install_path(self, supported_extensions=['zip', 'tar.gz', 'tar.bz2', '.gz']):
        for p in self._packages:
            for remote_location in self._config.remote_locations():
                for extension in supported_extensions:
                    package_file = "{}-{}.{}".format(os.path.join(remote_location, p['name']), p['version'], extension)
                    if os.path.isfile(package_file) and 'install_from' not in p:
                        p['install_from'] = package_file
                        p['install_from_ext'] = extension
