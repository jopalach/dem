import os
import subprocess


class RpmInstaller:
    def __init__(self, packages):
        self._packages = packages

    def install_packages(self):
        for p in self._packages:
            package_file = "{}-{}".format(p['name'], p['version'])
            self._execute_yum(package_file)

    @staticmethod
    def _execute_yum(package):
        subprocess.call(['sudo', 'yum', 'install', package, '-y'])

