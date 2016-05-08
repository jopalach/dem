import os, shutil, errno, stat


class Utils(object):
    @staticmethod
    def remove_directory(path):
        shutil.rmtree(path, ignore_errors=False, onerror=remove_read_only)


# http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
def remove_read_only(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise
