from tests import helper
from lib import minikube
class TestDockerCmds(helper.TestCase):
    def test_get_minikube_envs(self):
        if minikube.is_minikube_running():
            envs = minikube.get_minikube_envs()
            self.assertTrue('DOCKER_HOST' in envs)
            self.assertTrue('DOCKER_CERT_PATH' in envs)
