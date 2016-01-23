class Packages():
    def __init__(self, dictionary={}):
        self._packages = dictionary

    def has_a_library(self):
        for p in self._packages.values():
            if p['type'] == 'archive':
                return True
        return False

    def values(self):
        return self._packages.values()
