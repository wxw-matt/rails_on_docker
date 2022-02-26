import os, configparser

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

def get_rails_base_tag():
    cwd = os.getcwd()
    config = read_config(f'{cwd}/.rod')
    base = config['image']['base']
    return base

def get_docker_compose_service():
    cwd = os.getcwd()
    config = read_config(f'{cwd}/.rod')
    service = config['service']['web']
    return service

def get_project_tags():
    cwd = os.getcwd()
    config = read_config(f'{cwd}/.rod')
    tag = config['image']['tag']
    release_tag = config['image']['release_tag']
    return (tag, release_tag)

def write_rod(rails_base_tag, tag, release_tag, service,project_dir):
    fn = f'{project_dir}/.rod'
    config = read_config(fn)
    if 'image' not in config:
        config['image'] = {}
        config['service'] = {}
        config['rails'] = {}
    with open(fn, 'w+') as configfile:
        # tag is used by docker, service name `web` is for docker-compose
        config['service']['web'] = service
        config['image']['tag'] = tag
        config['image']['release_tag'] = release_tag
        config['image']['base'] = rails_base_tag
        config['rails']['env'] = 'development'
        config.write(configfile)


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
