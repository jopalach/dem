import yaml


def _auto_populate_missing_fields(packages):
    for p in packages.values():
        if 'version' not in p:
            p['version'] = 'latest'


def _reformat_versions(packages):
    for p in packages.values():
        if p['version'] is not str:
            p['version'] = str(p['version'])


def packages_from_data(data):
    packages = yaml.load(data)
    _auto_populate_missing_fields(packages)
    _reformat_versions(packages)
    return packages
