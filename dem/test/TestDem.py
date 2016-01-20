import unittest
import dem.PackagesReader as reader

SAMPLE = '''
qt:
    version: 4.8.6
    type: rpm
json:
    version: 1.8
    type: zip
Which:
    type: perl
git-python:
    type: python
x11:
    version: latest
    type: rpm
    system: yes
'''



class TestDem(unittest.TestCase):
    def test_willReadPackagesFromFile(self):
        packages = reader.packages_from_data(SAMPLE)

        self.assertNotEquals(packages['qt'], None)
        self.assertNotEquals(packages['json'], None)
        self.assertNotEquals(packages['Which'], None)
        self.assertNotEquals(packages['git-python'], None)
        self.assertNotEquals(packages['x11'], None)

    def test_willReadVersionFile(self):
        packages = reader.packages_from_data(SAMPLE)

        self.assertEquals(packages['qt']['version'], '4.8.6')
        self.assertEquals(packages['json']['version'], '1.8')
        self.assertEquals(packages['Which']['version'], 'latest')
        self.assertEquals(packages['git-python']['version'], 'latest')
        self.assertEquals(packages['x11']['version'], 'latest')



if __name__ == '__main__':
    unittest.main()
