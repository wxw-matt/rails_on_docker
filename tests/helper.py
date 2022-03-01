import os, unittest
from os import path
from pathlib import Path
import yaml

def _current_dir():
    return path.dirname(path.abspath(__file__))

class Helper:
    def __init__(self, basename, current_dir=_current_dir()):
        self._current_dir = current_dir
        self._project_name = '%s_%s' % (basename, os.getpid())
        self._project_path = Path(self._current_dir, self._project_name)
        self._config_path = Path(self._project_path, 'config')
        self._project_path.mkdir(parents=True, exist_ok=True)
        self._config_path.mkdir(parents=True, exist_ok=True)

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_path(self):
        return self._project_path

    @property
    def config_path(self):
        return self._config_path

    def make_project_dirs(self):
        self._project_path.mkdir(parents=True, exist_ok=True)
        self._config_path.mkdir(parents=True, exist_ok=True)

    def remove_dirs(self, path=None):
        path = path or self.project_path
        for child in path.iterdir():
            if child.is_dir():
                for gc in child.iterdir():
                    gc.unlink()
                child.rmdir()
            else:
                child.unlink()
        path.rmdir()

class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._helper = Helper('myapp')

    def setUp(self):
        self._helper.make_project_dirs()

    def tearDown(self):
        if not os.getenv('KEEP'):
            self._helper.remove_dirs()


if __name__ == '__main__':
    helper = Helper('app')
    helper.make_project_dirs()
    helper.remove_dirs()
