import os

import wget
from dem.dependency.archive import ArchiveInstaller
from dem.project.reader import Config


class UrlInstaller:
    def __init__(self, project, packages, cache):
        self._packages = packages
        self._project = project
        self._download_directory = os.path.join('.devenv', project, 'downloads')
        self._config = Config({'remote-locations': [self._download_directory]})
        self._cache = cache

    def install_packages(self):
        installed_packages = []

        for p in self._packages:
            if 'url' in p:
                file_extension = UrlInstaller._get_ext(p['url'])
                file_name = '{}-{}{}'.format(p['name'], p['version'], file_extension)
                local_file = os.path.join(self._download_directory, file_name)
                if not os.path.exists(local_file) and not self._cache.is_package_installed(p['name'], p['version']):
                    print('Fetching {}'.format(p['url']))
                    wget.download(p['url'], out=local_file)
                    print()
                installed_packages.append(p)
        local_installer = ArchiveInstaller(self._project, self._config, installed_packages, self._cache)
        return local_installer.install_packages()

    @staticmethod
    def _get_ext(url):
        root, ext = os.path.splitext(url.split('/')[-1])
        if ext in ['.gz', '.bz2']:
            ext = os.path.splitext(root)[1] + ext
        return ext

