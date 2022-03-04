from tests import helper
from lib import docker_cmds
class TestDockerCmds(helper.TestCase):
    def test_get_minikube_envs(self):
        envs = docker_cmds.get_minikube_envs()
        self.assertTrue('DOCKER_HOST' in envs)
        self.assertTrue('DOCKER_CERT_PATH' in envs)

