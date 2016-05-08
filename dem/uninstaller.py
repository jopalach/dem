import shutil
import os, subprocess
import errno, stat

class PackageUninstaller(object):
    def __init__(self, cache, packages):
        self._cache = cache
        self._packages = packages

    def uninstall_changed_packages(self):
        for name, version in self._packages_to_remove(self._cache.local_installed_packages()):
            location = self._cache.install_location(name)
            if location and os.path.exists(location):
                self._remove_archive_package(location, name, version)

        for name, version in self._packages_to_remove(self._cache.system_installed_packages()):
            self._remove_system_package(name, version)

        for name, version in self._packages_to_remove(self._cache.custom_installed_packages()):
            #todo: handle custom installed packages
            pass

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
    def _remove_archive_package(location, package, version):
        print('[dem] uninstalling {}-{}'.format(package, version))
        shutil.rmtree(location, ignore_errors=False, onerror=remove_read_only)

    @staticmethod
    def _remove_system_package(package, version):
        print('[dem] uninstalling {}-{}'.format(package, version))
        subprocess.call(['sudo', 'yum', 'remove', package, '-y'])


# http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
def remove_read_only(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise

