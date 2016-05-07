import os
import wget

from . ArchiveInstaller import ArchiveInstaller
from . DevEnvReader import Config


class UrlInstaller:
    def __init__(self, project, packages):
        self._packages = packages
        self._project = project
        self._download_directory = os.path.join('.devenv', project, 'downloads')
        self._config = Config({'remote_locations': [self._download_directory]})

    def install_packages(self):
        installed_packages = []

        for p in self._packages:
            if 'url' in p:
                file_extension = UrlInstaller._get_ext(p['url'])
                file_name = '{}-{}{}'.format(p['name'], p['version'], file_extension)
                local_file = os.path.join(self._download_directory, file_name)
                if not os.path.exists(local_file):
                    wget.download(p['url'], out=local_file)
                    installed_packages.append(p)
        local_installer = ArchiveInstaller(self._project, self._config, installed_packages)
        return local_installer.install_packages()

    @staticmethod
    def _get_ext(url):
        root, ext = os.path.splitext(url.split('/')[-1])
        if ext in ['.gz', '.bz2']:
            ext = os.path.splitext(root)[1] + ext
        return ext

