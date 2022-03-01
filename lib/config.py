import os, configparser

"""
Note: when creating a project, the current directory is where rod is excuting.
Project directory will be passed as a parameter to some functions.
If rod executes in project directory, `os.getcwd()` can be used to get the right
path.
"""

# Decorator
def rod_config(func):
    def wrapper(*args, **kwargs):
        RodConfig.load('.rod')
        func(*args, **kwargs)
    return wrapper


class RodConfig(object):
    instance = None
    def __init__(self, config_file):
        super().__init__()
        self._config_file = config_file
        self._config = read_config(config_file)

        self._docker_compose = RodConfigDockerCompose(self._config['docker-compose'])
        self._app= RodConfigApp(self._config['app'])
        self._image= RodConfigImage(self._config['image'])

    @classmethod
    def load(self, config_file):
        self.instance = RodConfig(config_file)
        return self.instance

    @property
    def config(self):
        return self._config

    @property
    def docker_compose(self):
        return self._docker_compose

    @property
    def app(self):
        return self._app

    @property
    def image(self):
        return self._image


class RodConfigImage(object):
    def __init__(self, image):
        super().__init__()
        self._tag = image['tag']
        self._release_tag = image['release_tag']
        self._base = image['base']

    @property
    def tag(self):
        return self._tag

    @property
    def release_tag(self):
        return self._release_tag

    @property
    def base(self):
        return self._base


class RodConfigDockerCompose(object):
    def __init__(self, docker_compose):
        super().__init__()
        self._service = docker_compose['service']
        self._project_name = docker_compose['project_name']

    @property
    def service(self):
        return self._service

    @property
    def project_name(self):
        return self._project_name

class RodConfigApp(object):
    def __init__(self, rails):
        super().__init__()
        self._env = rails['env']

    @property
    def env(self):
        return self._env


_options = {}
def get_options(options):
    global _options
    return _options

def set_options(options):
    global _options
    _options = options

def read_config(config_file=f'{os.getcwd()}/.rod'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def get_rails_base_tag(project_dir=None):
    cwd = project_dir or os.getcwd()
    if RodConfig.instance:
        cfg = RodConfig.instance
    else:
        cfg = RodConfig.load(f'{cwd}/.rod')
    return cfg.image.base

def get_docker_compose_service(project_dir=None):
    cwd = project_dir or os.getcwd()
    if RodConfig.instance:
        cfg = RodConfig.instance
    else:
        cfg = RodConfig.load(f'{cwd}/.rod')
    return cfg.docker_compose.service

def get_project_tags(project_dir=None):
    cwd = project_dir or os.getcwd()
    if RodConfig.instance:
        cfg = RodConfig.instance
    else:
        cfg = RodConfig.load(f'{cwd}/.rod')
    tag = cfg.image.tag
    release_tag = cfg.image.release_tag
    return (tag, release_tag)

def write_rod(rails_base_tag, tag, release_tag, service,project_dir):
    fn = f'{project_dir}/.rod'
    config = read_config(fn)
    for item in ['image', 'docker-compose', 'app']:
        if item not in config:
            config[item] = {}

    with open(fn, 'w+') as configfile:
        # tag is used by docker, service name `web` is for docker-compose
        config['docker-compose']['service'] = service
        config['docker-compose']['project_name'] = tag.split(':')[0]

        config['image']['tag'] = tag
        config['image']['release_tag'] = release_tag
        config['image']['base'] = rails_base_tag

        config['app']['env'] = 'development'
        config.write(configfile)
    return fn

# image_tag is without image name, i.e., latest, 1.0.1
def generate_project_tags(image_tag, project_dir):
    tag = project_dir.split('/')[-1]
    release_tag = tag
    if image_tag:
        if ':' in image_tag:
            # sth:version
            tag = image_tag
            t1,t2 = image_tag.split(':')
            release_tag = f'{t1}-release:{t2}'
        else:
            # version
            tag = f'{tag}:{image_tag}'
            release_tag = f'{tag}-release:{image_tag}'
    else:
        tag = tag + ":latest"
        release_tag =  release_tag + "-release:latest"
    return (tag, release_tag)
