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

def get_docker_compose_service():
    cwd = os.getcwd()
    config = read_config(f'{cwd}/.rod')
    service = config['service']['web']
    return service

def write_rod(rails_base_tag, image_tag, service,project_dir):
    tag = get_project_tag(image_tag, project_dir)
    fn = f'{project_dir}/.rod'
    config = read_config(fn)
    if 'image' not in config:
        config['image'] = {}
        config['service'] = {}
    with open(fn, 'w+') as configfile:
        # tag is used by docker, service name `web` is for docker-compose
        config['service']['web'] = service
        config['image']['tag'] = tag
        config['image']['base'] = rails_base_tag
        config.write(configfile)

def get_project_tag(image_tag, project_dir):
    tag = project_dir.split('/')[-1]
    if image_tag:
        if ':' in image_tag:
            # sth:version
            tag = image_tag
        else:
            # version
            tag = f'{tag}:{image_tag}'
    else:
        tag = tag + ":latest"
    return tag
