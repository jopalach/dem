import os
import subprocess


class RpmInstaller:
    def __init__(self, project, config, packages):
        self._config = config
        self._packages = packages
        self._project = project

    def install_packages(self):
        for p in self._packages:
            installed = False
            for remote in self._config.remote_locations():
                package_file = "{}-{}.{}".format(os.path.join(remote, p['name']), p['version'], 'rpm')
                if os.path.exists(package_file):
                    self._execute_rpm(package_file)
                    installed = True
                    break
            if not installed:
                package_file = "{}-{}".format(p['name'], p['version'])
                self._execute_yum(package_file)

    @staticmethod
    def _execute_rpm(package):
        subprocess.call(['rpm', '-i', package])

    @staticmethod
    def _execute_yum(package):
        subprocess.call(['sudo', 'yum', 'install', package, '-y'])

