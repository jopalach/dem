import gzip
import os, sys
from tarfile import TarFile
from zipfile import ZipFile


class ArchiveInstaller:
    def __init__(self, project, config, packages, cache):
        self._config = config
        self._packages = packages
        self._project = project
        self._cache = cache
        self._path_mapping = dict(linux={'bin': ['.devenv', self._project, 'bin'],
                                         'python-site-packages': ['.devenv', self._project, 'lib', 'python2.7', 'sitepackages'],
                                         'dependency-lib': ['.devenv', self._project, 'dependencies']},
                                  win32={'bin': ['.devenv', self._project, 'Scripts'],
                                         'python-site-packages': ['.devenv', self._project, 'Lib', 'site-packages'],
                                         'dependency-lib': ['.devenv', self._project, 'dependencies']},)

    def install_packages(self):
        self._update_package_with_install_path()
        installed_packages = []

        for p in self._packages.archive_packages():
            if 'install_from' not in p:
                print("Could not find package: {}, version: {}".format(p['name'], p['version']))
            else:
                if not self._cache.is_package_installed(p['name'], p['version']):
                    print('[dem] installing {}-{}'.format(p['name'], p['version']))
                    if p['install_from_ext'] == 'zip':
                        with ZipFile(p['install_from'], 'r') as archive:
                            location = self._extract(archive, p)
                    elif p['install_from_ext'] == 'tar.gz':
                        with TarFile.open(p['install_from'], 'r:gz') as archive:
                            location = self._extract(archive, p)
                    elif p['install_from_ext'] == 'tar.bz2':
                        with TarFile.open(p['install_from'], 'r:bz2') as archive:
                            location = self._extract(archive, p)
                    elif p['install_from_ext'] == 'gz':
                        with gzip.open(p['install_from'], 'r') as archive:
                            location = self._extract(archive, p)
                else:
                    print('[dem] {}-{} already installed'.format(p['name'], p['version']))
                    location = self._cache.install_location(p['name'])
                package = dict()
                package[p['name']] = {'version': p['version'], 'type': 'local', 'install_location': location}
                installed_packages.append(package)

        return installed_packages

    def _extract(self, archive, p):
        destination_dir = self._platform_destination_path(p['destination'])
        if p['destination'] == 'dependency-lib':
            destination_dir = os.path.join(destination_dir, p['name'])
            archive.extractall(destination_dir)
            return destination_dir
        else:
            if p['destination'] == 'bin':
                self._extract_all_stripping_parent_directory(destination_dir, p, archive)
            if p['destination'] == 'python-site-packages':
                self._extract_all_stripping_parent_directory(os.path.join(destination_dir, p['name']), p, archive)
            return ''

    def _extract_all_stripping_parent_directory(self, destination_dir, p, archive):
        if p['install_from_ext'] == 'zip':
            members = archive.infolist()
            for member in reversed(members):
                if '/' in member.filename:
                    value = member.filename.split('/', 1)[1]
                    member.filename = value
                else:
                    members.remove(member)
            archive.extractall(destination_dir, members=members)
        elif p['install_from_ext'] == 'tar.gz' or p['install_from_ext'] == 'tar.bz2':
            members = archive.getmembers()
            for member in reversed(members):
                if '/' in member.name:
                    value = member.name.split('/', 1)[1]
                    member.name = value
                else:
                    members.remove(member)
            archive.extractall(destination_dir, members=members)

    def _update_package_with_install_path(self, supported_extensions=['zip', 'tar.gz', 'tar.bz2', '.gz']):
        for p in self._packages.archive_packages():
            for remote_location in self._config.remote_locations():
                for extension in supported_extensions:
                    package_file = "{}-{}.{}".format(os.path.join(remote_location, p['name']), p['version'], extension)
                    if os.path.isfile(package_file) and 'install_from' not in p:
                        p['install_from'] = package_file
                        p['install_from_ext'] = extension

    def _platform_destination_path(self, destination):
        return os.path.join(*self._path_mapping[self._platform()][destination])

    def _platform(self):
        if sys.platform.startswith("linux"):
            return "linux"
        return "win32"

