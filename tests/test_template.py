import os, unittest
from os import path
from pathlib import Path
from lib import rails_cmds
from tests import helper
import yaml



class TestGeneratedFiles(helper.TestCase):
    def test_files(self):
        rails_cmds.create_files_for_the_project('rails-tag:1.0','mysql', str(self._helper.project_path))
        f = open(self._helper.config_path.joinpath('database.yml'))
        config = yaml.safe_load(f)
        f.close()
        password = 'example'
        for env in ['development', 'production']:
            self.assertEqual(config[env]['database'], f'{self._helper.project_name}_{env}')
            self.assertEqual(config[env]['host'], f'db')
            self.assertTrue(password in config[env]['password'])

        f = open(self._helper.project_path.joinpath('docker-compose.yml'))
        docker_compose = yaml.safe_load(f)
        f.close()

        web = docker_compose['services']['web']
        db = docker_compose['services']['db']
        self.assertTrue("bundle exec rails s -p 3000 -b '0.0.0.0'" in web['command'])
        self.assertTrue("mariadb" in db['image'])

        self.assertTrue(Path(self._helper.project_path.joinpath('rod')).is_symlink())

        with open(self._helper.project_path.joinpath('Dockerfile')) as f:
            dockerfile = f.read()
            self.assertTrue('RUN bundle install' in dockerfile)

if __name__ == '__main__':
    unittest.main()
