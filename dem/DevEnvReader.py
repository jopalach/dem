import os

import yaml
import sys
import platform

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
        packages = []
        for p in self._packages.values():
            if p['type'] == 'archive':
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
        _add_additional_search_locations_based_on_platform(config)


def _add_additional_search_locations_based_on_platform(config):
    (os_short, arch) = _os_info()
    remote_locations = config['remote_locations'][:]
    for location in remote_locations:
        config['remote_locations'].insert(config['remote_locations'].index(location), os.path.join(location, os_short, arch))
        config['remote_locations'].insert(config['remote_locations'].index(location), os.path.join(location, os_short))

    _add_additional_search_locations_based_on_centos_or_rhel(config)


def _add_additional_search_locations_based_on_centos_or_rhel(config):
    (os_short, arch) = _os_info()
    os_short_original = os_short
    if os_short.startswith('centos'):
        os_short = os_short.replace('centos', 'rhel')
    elif os_short.startswith('rhel'):
        os_short = os_short.replace('rhel', 'centos')
    else:
        return
    remote_locations = config['remote_locations'][:]
    for location in remote_locations:
        if os_short_original in location:
            replace_location = location.replace(os_short_original, os_short)
            config['remote_locations'].insert(config['remote_locations'].index(location) + 1, replace_location)


def _os_info():
    if _is_linux():
        (os_short, version_long, label) = platform.linux_distribution(full_name=False)
        return (os_short.lower() +  version_long.split('.')[0], _arch())
    else:
        return ('win32', _arch())

def _arch():
    if platform.machine().lower() == 'amd64':
        return 'x86_64'
    else:
        return 'i386'

def _is_linux():
    return sys.platform.lower() == 'linux'

def _add_names(packages):
    for key in packages.keys():
        packages[key]['name'] = key


def devenv_from_file(devenv_file_path):
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
