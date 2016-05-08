import os

from git import Repo


class GitProjectInstaller:
    def __init__(self, packages, cache):
        self._packages = packages
        self._cache = cache

    def install_packages(self):
        installed_packages = []

        for p in self._packages:
            if not GitProjectInstaller._can_clone(p):
                continue

            if self._cache.is_package_installed(p['name'], p['version']):
                print('[dem] {}-{} already git cloned'.format(p['name'], p['version']))
            else:
                print('[dem] cloning git {}-{}'.format(p['name'], p['version']))
                clone_location = os.path.join(p['platform-destination-path'], p['name'])
                repo = Repo.clone_from(p['url'], clone_location)
                repo.git.checkout(p['version'])
                package = dict()
                package[p['name']] = {'version': p['version'], 'type': 'local', 'install_location': clone_location}
                installed_packages.append(package)

        return installed_packages

    @staticmethod
    def _can_clone(p):
        if 'url' not in p:
            print('[dem] cannot clone {}-{} - URL missing'.format(p['name'], p['version']))
            return False
        return True

