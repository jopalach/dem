import yaml
import sys, os

class Config:
    def __init__(self, dictionary={}):
        self._config = dictionary

    def __getitem__(self, item):
        return self._config[item]

    def remote_locations(self):
        if not self.has_remote_locations():
            return []
        return self._config['remote_locations']

    def has_remote_locations(self):
        return 'remote_locations' in self._config


class Packages:
    def __init__(self, dictionary={}):
        self._packages = dictionary

    def __getitem__(self, item):
        return self._packages[item]

    def has_a_library(self):
        for p in self._packages.values():
            if p['type'] == 'archive':
                return True
        return False

    def values(self):
        return self._packages.values()

    def archive_packages(self):
        return self._all_packages_of_type('archive')

    def rpm_packages(self):
        return self._all_packages_of_type('rpm')

    def _all_packages_of_type(self, type):
        packages = []
        for p in self._packages.values():
            if p['type'] == type:
                packages.append(p)
        return packages

def _auto_populate_missing_fields(packages):
    for p in packages.values():
        if 'version' not in p:
            p['version'] = 'latest'


def _reformat_versions(packages):
    for p in packages.values():
        if p['version'] is not str:
            p['version'] = str(p['version'])


def _fixup_remote_locations(config):
    if 'remote_locations' in config and not isinstance(config['remote_locations'], list):
        config['remote_locations'] = [config['remote_locations']]


def _add_names(packages):
    for key in packages.keys():
        packages[key]['name'] = key


def devenv_from_file(devenv_file_path):
    if not os.path.exists(devenv_file_path):
        print('Error: {} does not exists'.format(devenv_file_path))
        sys.exit(1)

    with open(devenv_file_path, 'r') as f:
        devenv = yaml.load(f)
    packages = {}

    if devenv is not None and 'packages' in devenv:
        packages = devenv['packages']

    os_packages = "packages-{}".format(sys.platform.lower())
    if devenv is not None and os_packages in devenv:
        packages.update(devenv[os_packages])
    _auto_populate_missing_fields(packages)
    _reformat_versions(packages)
    _add_names(packages)

    config = {}
    if devenv is not None and 'config' in devenv:
        config = devenv['config']
    _fixup_remote_locations(config)

    return Config(config), Packages(packages)
