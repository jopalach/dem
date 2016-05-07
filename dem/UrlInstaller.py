import os
import wget

from . ArchiveInstaller import ArchiveInstaller
from . DevEnvReader import Config


class UrlInstaller:
    def __init__(self, project, packages, cache):
        self._packages = packages
        self._project = project
        self._download_directory = os.path.join('.devenv', project, 'downloads')
        self._config = Config({'remote_locations': [self._download_directory]})
        self._cache = cache

    def install_packages(self):
        installed_packages = []

        for p in self._packages:
            if 'url' in p:
                file_extension = UrlInstaller._get_ext(p['url'])
                file_name = '{}-{}.{}'.format(p['name'], p['version'], file_extension)
                local_file = os.path.join(self._download_directory, file_name)
                if not os.path.exists(local_file):
                    wget.download(p['url'], out=local_file)
                    installed_packages.append(p)
        local_installer = ArchiveInstaller(self._project, self._config, installed_packages, self._cache)
        return local_installer.install_packages()

    @staticmethod
    def _get_ext(url):
        return url.split('/')[-1].split('.', 1)[1]

