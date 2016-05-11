import subprocess


class PipRunner(object):
    def __init__(self, config, util):
        self.util = util
        self.config = config

    def install(self, package, version='latest'):
        command = self.util.get_activate_script_command()
        self._add_pip(command)

        if version == 'latest':
            subprocess.call(command + ['install', package])
        else:
            subprocess.call(command + ['install', '{}=={}'.format(package, version)])

    def _add_pip(self, command):
        command.extend(['&&', 'pip'])
        if self.config.has_http_proxy():
            command.extend(['--proxy={}'.format(self.config.http_proxy())])


class PipInstaller(object):
    def __init__(self, packages, config, cache, util):
        self.util = util
        self.config = config
        self.cache = cache
        self.packages = packages
        self.pip_runner = PipRunner(config, util)

    def install_packages(self):
        installed_packages = []
        for p in self.packages:
            if self.cache.is_package_installed(p['name'], p['version']):
                print('[dem] {}-{} already installed'.format(p['name'], p['version']))
            else:
                print('[dem] pip installing {}-{}'.format(p['name'], p['version']))
                self.pip_runner.install(p['name'], p['version'])
                package = dict()
                package[p['name']] = {'version': p['version'], 'type': 'pip'}
                installed_packages.append(package)

        return installed_packages
