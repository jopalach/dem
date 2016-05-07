import unittest, mock
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
import hashlib
import json
import os

from dem.cache import PackageCache

SAMPLE_YAML_CONTENT = '''
config:
    remote_locations:
        ['/opt',
        'http://github.com']
packages:
    qt:
        version: 4.8.6
        type: rpm
    json:
        version: 1.8
        type: archive
'''

DIFFERENT_SAMPLE_YAML_CONTENT = '''
config:
    remote_locations:
        ['/opt',
        'http://github.com']
packages:
    qt:
        version: 4.8.6
        type: rpm
    json:
        version: 1.9
        type: archive
'''


SAMPLE_CACHE_CONTENT = '''
{
    "md5": "b084deb42d4daefe7c29d4eae24c2d2d"
}
'''

class MyTestCase(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_will_hash_yaml_file(self):
        self.fs.CreateDirectory(os.path.abspath('base_path'))
        self.fs.CreateDirectory(os.path.join('base_path', '.devenv'))
        self.fs.CreateFile(os.path.join('base_path', 'devenv.yaml'), contents=SAMPLE_YAML_CONTENT)

        cache = PackageCache(os.path.abspath('base_path'))
        cache.update([])

        hasher = hashlib.md5()
        hasher.update(SAMPLE_YAML_CONTENT.encode('utf-8'))
        expected_hash = hasher.hexdigest()
        print(expected_hash)
        with open(os.path.join('base_path', '.devenv', 'cache.json')) as f:
            data = json.load(f)
            self.assertEqual(data.get('md5', ''), expected_hash)

    def test_needs_update_when_cache_file_does_not_exist(self):
        self.fs.CreateDirectory(os.path.abspath('base_path'))
        cache = PackageCache(os.path.abspath('base_path'))
        self.assertTrue(cache.needs_update())

    def test_needs_update_when_md5_hash_mismatch(self):
        self.fs.CreateDirectory(os.path.abspath('base_path'))
        self.fs.CreateDirectory(os.path.join('base_path', '.devenv'))
        self.fs.CreateFile(os.path.join('base_path', 'devenv.yaml'), contents=DIFFERENT_SAMPLE_YAML_CONTENT)
        self.fs.CreateFile(os.path.join('base_path', '.devenv', 'cache.json'), contents=SAMPLE_CACHE_CONTENT)

        cache = PackageCache(os.path.abspath('base_path'))
        self.assertTrue(cache.needs_update())

    def test_does_not_need_update_when_md5_hash_match(self):
        self.fs.CreateDirectory(os.path.abspath('base_path'))
        self.fs.CreateDirectory(os.path.join('base_path', '.devenv'))
        self.fs.CreateFile(os.path.join('base_path', 'devenv.yaml'), contents=SAMPLE_YAML_CONTENT)
        self.fs.CreateFile(os.path.join('base_path', '.devenv', 'cache.json'), contents=SAMPLE_CACHE_CONTENT)

        cache = PackageCache(os.path.abspath('base_path'))
        self.assertFalse(cache.needs_update())


if __name__ == '__main__':
    unittest.main()
