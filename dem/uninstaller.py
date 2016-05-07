import shutil
import os, sys


class PackageUninstaller(object):
    def __init__(self, cache, packages):
        self._cache = cache
        self._packages = packages

    def uninstall_changed_packages(self):
        for name, version in self._archive_packages_to_remove():
            location = self._cache.install_location(name)
            if location and os.path.exists(location):
                print('[dem] uninstalling {}-{}'.format(name, version))
                shutil.rmtree(location)

    def _archive_packages_to_remove(self):
        packages_to_remove = []
        for name, info in self._cache.local_installed_packages().items():
            if name not in self._packages.values():
                packages_to_remove.append((name, info['version']))
            else:
                package_in_yaml = self._packages[name]
                if info['version'] != package_in_yaml['version']:
                    packages_to_remove.append((name, info['version']))
        return packages_to_remove



