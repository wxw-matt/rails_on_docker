import os, unittest
from os import path
from pathlib import Path
from lib import rails_cmds
import yaml


def remove_dirs(path):
    for child in path.iterdir():
        if child.is_dir():
            for gc in child.iterdir():
                gc.unlink()
            child.rmdir()
        else:
            child.unlink()
    path.rmdir()

class TestDataConfigTemplate(unittest.TestCase):
    def setUp(self):
        self.current_dir = path.dirname(path.abspath(__file__))
        self.project_name = 'myapp_%s' % os.getpid()
        self.project_path = Path(self.current_dir, self.project_name)
        self.config_path = Path(self.project_path, 'config')
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.config_path.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        remove_dirs(self.project_path)

    def test_customer_count(self):
        rails_cmds.create_files_for_the_project('rails-tag:1.0','mysql', str(self.project_path))
        f = open(self.config_path.joinpath('database.yml'))
        config = yaml.safe_load(f)
        f.close()
        password = 'example'
        for env in ['development', 'production']:
            self.assertEqual(config[env]['database'], f'{self.project_name}_{env}')
            self.assertEqual(config[env]['host'], f'db')
            self.assertTrue(password in config[env]['password'])

if __name__ == '__main__':
    unittest.main()
