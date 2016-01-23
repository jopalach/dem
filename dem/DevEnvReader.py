import yaml

from .Packages import Packages
from .Config import Config


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


def devenv_from_file(devenv_file_path):
    with open(devenv_file_path, 'r') as f:
        devenv = yaml.load(f)
    packages = {}
    if devenv is not None and 'packages' in devenv:
        packages = devenv['packages']
    _auto_populate_missing_fields(packages)
    _reformat_versions(packages)

    config = {}
    if devenv is not None and 'config' in devenv:
        config = devenv['config']
    _fixup_remote_locations(config)

    return (Config(config), Packages(packages))