import os, unittest
from os import path
from pathlib import Path
from lib import rails_cmds, template, args_helper, config
from tests import helper
import yaml

class TestGeneratedFiles(helper.TestCase):
    def test_files(self):
        args_helper.set_global_arg('name', self._helper.project_name)
        app_name = self._helper.project_name

        project_dir = str(self._helper.project_path)
        tag = f'{app_name}:latest'
        release_tag = f'{app_name}-release:latest'
        rails_base_tag = 'wxwmatt/rails:7.0.2.2-alpine3.15'
        config.write_rod(rails_base_tag, tag, release_tag, 'web', project_dir)
        rails_cmds.create_files_for_the_project(rails_base_tag, 'mysql', project_dir);

        # Database config
        f = open(self._helper.config_path.joinpath('database.yml'))
        cfg = yaml.safe_load(f)
        f.close()
        password = 'example'
        for env in ['development', 'production']:
            self.assertEqual(cfg[env]['database'], f'{self._helper.project_name}_{env}')
            self.assertEqual(cfg[env]['host'], f'db')
            self.assertTrue(password in cfg[env]['password'])

        # Docker compose
        f = open(self._helper.project_path.joinpath('docker-compose.yml'))
        docker_compose = yaml.safe_load(f)
        f.close()

        web = docker_compose['services']['web']
        db = docker_compose['services']['db']
        self.assertTrue("bundle exec rails s -p 3000 -b '0.0.0.0'" in web['command'])
        self.assertTrue("mariadb" in db['image'])

        self.assertTrue(Path(self._helper.project_path.joinpath('rod')).is_symlink())

        # Dockerfile
        with open(self._helper.project_path.joinpath('Dockerfile')) as f:
            dockerfile = f.read()
            self.assertTrue('RUN bundle install' in dockerfile)

        with open(self._helper.project_path.joinpath('config/database.yml')) as f:
            cfg = f.read()
            self.assertTrue('mysql2' in cfg)

    def test_template(self):
        postgres = template.dc_rails_postgres_template('myapp',networks=['rod-network'])
        self.assertTrue('postgres' in postgres)
        mariadb = template.dc_rails_mariadb_template('myapp',networks=['rod-network'])
        self.assertTrue('mariadb' in mariadb)
        sqlite3 = template.dc_rails_sqlite3_template('myapp',networks=['rod-network'])
        self.assertTrue('sqlite3' not in sqlite3)


if __name__ == '__main__':
    unittest.main()
