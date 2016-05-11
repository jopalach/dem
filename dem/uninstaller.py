import os, subprocess

from . piprunner import PipRunner
from . utils import Utils


class PackageUninstaller(object):
    def __init__(self, cache, packages, pip_runner):
        self._cache = cache
        self._packages = packages
        self._pip_runner = pip_runner

    def uninstall_changed_packages(self):
        for name, version in self._packages_to_remove(self._cache.local_installed_packages()):
            locations = self._cache.install_locations(name)
            print('[dem] uninstalling {}-{}'.format(name, version))
            for location in locations:
                if os.path.isdir(location):
                    Utils.remove_directory(location)
                elif os.path.isfile(location):
                    os.remove(location)

        for name, version in self._packages_to_remove(self._cache.system_installed_packages()):
            self._remove_system_package(name, version)

            # for name, version in self._packages_to_remove(self._cache.pip_installed_packages()):
            # self._pip_runner.remove(name, version)

    def _packages_to_remove(self, installed_packages):
        packages_to_remove = []
        for name, info in installed_packages.items():
            if not self._packages.contains_package(name):
                packages_to_remove.append((name, info['version']))
            else:
                package_in_yaml = self._packages[name]
                if info['version'] != package_in_yaml['version']:
                    packages_to_remove.append((name, info['version']))
        return packages_to_remove

    @staticmethod
    def _remove_system_package(package, version):
        print('[dem] uninstalling {}-{}'.format(package, version))
        subprocess.call(['sudo', 'yum', 'remove', package, '-y'])



