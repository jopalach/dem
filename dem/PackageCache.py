import os
import hashlib
import json
BLOCKSIZE = 65536


class PackageCache(object):
    def __init__(self, base_path):
        self._yaml_file = os.path.join(base_path, 'devenv.yaml')
        self._cache_file = os.path.join(base_path, '.devenv', 'cache.json')

    def needs_update(self):
        if os.path.exists(self._cache_file):
            if self._verify_md5():
                return False
        return True

    def update(self):
        self._update_hash()

    def _update_hash(self):
        digest = self._hash_yaml()
        data = self._cache_data()
        data['md5'] = digest
        with open(self._cache_file, 'w+') as f:
            json.dump(data, f)

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

