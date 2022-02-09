import os, sys
from os import path
from lib import config
from lib.docker_cmds import docker_compose_run_cmd, docker_compose_exec_cmd, docker_base_cmd, docker_project_base_cmd, docker_compose_up_cmd
from lib.cmd_helper import run_cmd, merge_cmds
from lib import template
from lib import docker_cmds

_versions = {
    '7.0.1': 'wxwmatt/rails:7.0.1-alpine3.15',
    '7':'wxwmatt/rails:7.0.1-alpine3.15',
    '6':'wxwmatt/rails:6.1.4.4-alpine3.15'
}

def get_rails_image_name(version):
    global _versions
    return _versions[version]

def rails_base_cmd(full_tag, args_for_docker=[]):
    return [
            docker_compose_exec_cmd(full_tag, args_for_docker) + ['rails'],
            docker_compose_run_cmd(full_tag, args_for_docker) + ['rails']
            ]


def rails_project_command(command, options, args_for_docker=[]):
    cmds = merge_cmds(rails_base_cmd(config.get_docker_compose_service(), args_for_docker),  [command] + options)
    run_cmd(*cmds)

def rails_generate_cmd(full_tag):
    return merge_cmds(rails_base_cmd(full_tag),  ['generate'])

def rails_generate_controller_cmd(full_tag):
    return merge_cmds(rails_generate_cmd(full_tag),  ['controller'])

def rails_generate_model_cmd(full_tag):
    return merge_cmds(rails_generate_cmd(full_tag),  ['model'])

def rails_generate_scaffold_cmd(full_tag):
    return merge_cmds(rails_generate_cmd(full_tag),  ['scaffold'])

def generate_controller(full_tag, options):
    args = merge_cmds(rails_generate_controller_cmd(full_tag) , [options.NAME] + options.actions)
    run_cmd(*args)

def generate_model(full_tag, options):
    args = merge_cmds(rails_generate_model_cmd(full_tag) , [options.NAME] + options.fields)
    run_cmd(*args)

def generate_scaffold(full_tag, options):
    args = merge_cmds(rails_generate_scaffold_cmd(full_tag) , [options.NAME] + options.fields)
    run_cmd(*args)


def generate_controller_handler(args):
    generate_controller(config.get_docker_compose_service(), args)

def generate_model_handler(args):
    generate_model(config.get_docker_compose_service(), args)

def generate_scaffold_handler(args):
    generate_scaffold(config.get_docker_compose_service(), args)

def project_handler(args):
    print(args)

def create_files_for_the_project(rails_base_tag, database, project_dir):
    with open(f'{project_dir}/Dockerfile', 'w+') as f:
        f.write(template.dockerfile_template(rails_base_tag))

    with open(f'{project_dir}/docker-compose.yml', 'w+') as f:
        if database == 'mysql':
            f.write(template.dc_rails_mariadb_template(None,networks=['rod-network']))
        elif database == 'postgresql':
            f.write(template.dc_rails_postgres_template(None,networks=['rod-network']))
        else:
            f.write(template.dc_rails_sqlite3_template(None,networks=['rod-network']))

    rod_path = path.join(project_dir, 'rod')
    if not path.exists(rod_path):
        os.symlink(path.abspath(sys.argv[0]), rod_path)

def build_image_and_create_rod(rails_base_tag, image_tag, project_dir):
    cmd = docker_cmds.build_image(rails_base_tag, image_tag, project_dir)
    if run_cmd(cmd).returncode == 0:
        config.write_rod(rails_base_tag, image_tag, 'web', project_dir)

# Docker version 20.10.11, build dea9396
def generate_rails_project(options, rails_options):
    rails_base_tag= get_rails_image_name(options.version)
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()

    cmd = docker_base_cmd(rails_base_tag) + ['rails'] + rails_options
    if run_cmd(cmd).returncode == 0:
        tag_name = options.tag or "latest"
        project_dir = os.path.join(cwd, rails_options[1])
        create_files_for_the_project(rails_base_tag, options.database, project_dir);
        config.write_rod(rails_base_tag, tag_name,'web',project_dir)
        if not options.skip_bundle:
            build_image_and_create_rod(rails_base_tag, tag_name, project_dir)
        else:
            lock_gemfile(rails_base_tag,project_dir)

def new_project_handler(args):
    if not args.version:
        print ("Please specify a rails version, like `-v 7`")
        exit(1)
    print("Create a new Rails project")
    project_name = args.name
    rails_version = args.version
    database = args.database
    rails_options = ['new', project_name, f'--database={database}']
    if args.skip_bundle:
        rails_options.append('-B')
    generate_rails_project(args, rails_options)

def rails_command_handler(args):
    print(args)

def rails_command_server_handler(args):
    cmd = docker_compose_up_cmd('web')
    run_cmd(cmd)

def rails_command_console_handler(args):
    options = []
    rails_project_command('console', options)

