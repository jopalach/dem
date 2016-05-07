import sys
import subprocess


class RpmInstaller:
    def __init__(self, packages):
        self._packages = packages

    def install_packages(self):
        installed_packages = []
        for p in self._packages:
            print('[dem] installing {}-{}'.format(p['name'], p['version']))
            package_file = "{}-{}".format(p['name'], p['version'])
            self._execute_yum(package_file)
            package = dict()
            package[p['name']] = {'version': p['version'], 'type': 'system'}
            installed_packages.append(package)
        return installed_packages

    @staticmethod
    def _execute_yum(package):
        subprocess.call(['sudo', 'yum', 'install', package, '-y'])

