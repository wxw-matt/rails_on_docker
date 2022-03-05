import os, unittest
from os import path
from pathlib import Path
from lib import rails_cmds, template, args_helper, config
from tests import helper
import yaml

class TestConfig(helper.TestCase):
    def test_config(self):
        args_helper.set_global_arg('name', self._helper.project_name)
        app_name = self._helper.project_name

        project_dir = str(self._helper.project_path)
        tag = f'{app_name}:latest'
        release_tag = f'{app_name}-release:latest'
        rails_base_tag = 'wxwmatt/rails:7.0.2.2-alpine3.15'
        file = config.write_rod(rails_base_tag, app_name, tag, project_dir, 'app')
        rod_config = config.RodConfig(file)

        self.assertEqual(rod_config.image.tag, tag)
        self.assertEqual(rod_config.image.release_tag, release_tag)
        self.assertEqual(rod_config.image.base, rails_base_tag)

        self.assertEqual(rod_config.docker_compose.service, 'app')
        self.assertEqual(rod_config.docker_compose.project_name, app_name)

        self.assertEqual(rod_config.app.env, 'development')

if __name__ == '__main__':
    unittest.main()
