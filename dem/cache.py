import os
import hashlib
import json
BLOCKSIZE = 65536


class PackageCache(object):
    def __init__(self, base_path):
        self._yaml_file = os.path.join(base_path, 'devenv.yaml')
        self._base = base_path
        self._devenv = os.path.join(base_path, '.devenv')
        self._cache_file = os.path.join(self._devenv, 'cache.json')

    def needs_update(self):
        if os.path.exists(self._cache_file):
            if self._verify_md5():
                return False
        return True

    def update(self, installed_packages):
        digest = self._hash_yaml()
        data = self._cache_data()
        data['md5'] = digest
        packages = {}
        for p in installed_packages:
            for name, info in p.items():
                packages[name] = info
        data['packages'] = packages
        with open(self._cache_file, 'w+') as f:
            json.dump(data, f)

    def local_installed_packages(self):
        return self._packages_of_type('local')

    def system_installed_packages(self):
        return self._packages_of_type('system')

    def install_location(self, name):
        data = self._cache_data().get('packages', {})
        location = data.get(name, {}).get('install_location', None)
        if location:
            location = location.replace('/', os.sep)
            return os.path.join(self._base, location)
        return None

    def _hash_yaml(self):
        hasher = hashlib.md5()
        with open(self._yaml_file, 'rb') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)
        return hasher.hexdigest()

    def _cache_data(self):
        try:
            with open(self._cache_file, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print('[dem] {}'.format(e))
                    data = {}
                return data
        except IOError:
            return {}

    def _verify_md5(self):
        digest = self._hash_yaml()
        current_md5 = self._cache_data().get('md5', '')
        return digest == current_md5

    def _packages_of_type(self, type_to_find):
        installed_packages = {}
        packages = self._cache_data().get('packages', {})
        for name, info in packages.items():
            package_type = info.get('type', None)
            if package_type == type_to_find:
                installed_packages[name] = info
        return installed_packages
