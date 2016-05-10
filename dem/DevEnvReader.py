import yaml
import sys, os
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
        if self._config is None:
            return False
        return 'remote_locations' in self._config

    def http_proxy(self):
        if self.has_http_proxy():
            return self._config['http_proxy']
        return None

    def has_http_proxy(self):
        if not self._config:
            return False
        return 'http_proxy' in self._config


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

    def contains_package(self, name):
        for p in self._packages.values():
            if p['name'] == name:
                return True
        return False

    def archive_packages(self):
        return self._all_packages_of_type('archive')

    def rpm_packages(self):
        return self._all_packages_of_type('rpm')

    def url_packages(self):
        return self._all_packages_of_type('url')

    def git_packages(self):
        return self._all_packages_of_type('git')

    def pip_packages(self):
        return self._all_packages_of_type('pip')

    def _all_packages_of_type(self, type):
        packages = []
        for p in self._packages.values():
            if p['type'] == type:
                packages.append(p)
        return packages

def _fixup_remote_locations(config):
    if config is None:
        config = {}
    if 'remote_locations' not in config:
        config['remote_locations'] = []
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
        (os_short, version_long, label) = platform.linux_distribution(full_distribution_name=False)
        return (os_short.lower() +  version_long.split('.')[0], _arch())
    else:
        return ('win32', _arch())


def _arch():
    if platform.machine().lower() == 'amd64' or platform.machine().lower() == "x86_64":
        return 'x86_64'
    else:
        return 'i386'


def _is_linux():
    return sys.platform.startswith('linux')


def _add_names(packages):
    for key in packages.keys():
        packages[key]['name'] = key

def devenv_from_file(devenv_file_path):
    if not os.path.exists(devenv_file_path):
        print('[dem] Error: {} does not exists'.format(devenv_file_path))
        sys.exit(1)

    with open(devenv_file_path, 'r') as f:
        try:
            devenv = yaml.load(f)
        except yaml.YAMLError as exc:
            _exit_and_show_error(f, exc)
    packages = {}

    if devenv is not None and 'packages' in devenv:
        packages = devenv['packages']

    os_packages = "packages-{}".format(_platform())
    if devenv is not None and os_packages in devenv:
        packages.update(devenv[os_packages])
    _add_names(packages)

    config = {}
    if devenv is not None and 'config' in devenv:
        config = devenv['config']

    _fixup_remote_locations(config)

    return Config(config), Packages(packages)


def _exit_and_show_error(f, exc):
    # http://stackoverflow.com/questions/30269723/how-to-get-details-from-pyyaml-exception
    print("[dem] Error while parsing YAML file: {}".format(f.name))
    if hasattr(exc, 'problem_mark'):
        if exc.context != None:
            print ('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                   str(exc.problem) + ' ' + str(exc.context) +
                   '\nPlease correct data and retry.')
        else:
            print ('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                   str(exc.problem) + '\nPlease correct data and retry.')
    else:
        print ("[dem] Something went wrong while parsing yaml file")
    sys.exit(1)


def _platform():
    if sys.platform.startswith("linux"):
        return "linux"
    return "win32"


def fixup_packages(packages, cache):
    path_mapping = dict(linux={'bin': os.path.join(cache.project_path(), 'bin'),
                               'python-site-packages': os.path.join(cache.project_path(), 'lib', 'python2.7',
                                                        'site-packages'),
                               'dependency-lib': os.path.join(cache.project_path(), 'dependencies')},
                        win32={'bin':  os.path.join(cache.project_path(), 'Scripts'),
                               'python-site-packages': os.path.join(cache.project_path(),  'Lib',
                                                        'site-packages'),
                               'dependency-lib':  os.path.join(cache.project_path(), 'dependencies')})
    fixed_path_types = ['bin', 'python-site-packages',  'dependency-lib']
    packages._packages['dem'] = {'name': 'dem', 'version': 'latest', 'type': 'pip'}

    def fix_version(p):
        if 'version' not in p and 'type' in p and p['type'] == 'git':
            p['version'] = 'master'
        elif 'version' not in p:
            p['version'] = 'latest'

        if p['version'] is not str:
            p['version'] = str(p['version'])

    def setup_destination_paths(p):
        if 'destination' not in p:
            p['destination'] = 'dependency-lib'
        if p['type'] == 'pip':
            p['destination'] = 'python-site-packages'

        if 'platform-destination-path' not in p and p['destination'] in fixed_path_types:
            p['platform-destination-path'] = path_mapping[_platform()][p['destination']]
        else:
            p['platform-destination-path'] = os.path.join(cache.base_path(), p['destination'])

    def fixup_type(p):
        if 'type' not in p:
            if 'url' in p and p['url'].endswith('.tar.gz', '.zip'):
                p['type'] = 'url'
            elif 'url' in p:
                p['type'] = 'git'
            else : # Could be RPM, but lets just guess for archive
                p['type'] = 'archive'

    for p in packages.values():
        fix_version(p)
        fixup_type(p)

        setup_destination_paths(p)
