import os, sys
from os import path
from lib import config
from lib.docker_cmds import docker_compose_run_cmd, docker_compose_exec_cmd, docker_base_cmd, docker_project_base_cmd, docker_compose_up_cmd
from lib.cmd_helper import run_cmd, merge_cmds
from lib import args_helper, template, docker_cmds

_versions = {
    '7.0.1': 'wxwmatt/rails:7.0.1-alpine3.15',
    '7':'wxwmatt/rails:7.0.2.2-alpine3.15',
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

def rake_base_cmd(full_tag, args_for_docker=[]):
    return [
            docker_compose_exec_cmd(full_tag, args_for_docker) + ['rake'],
            docker_compose_run_cmd(full_tag, args_for_docker) + ['rake']
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
    app_name = args_helper.get_global_args().name
    with open(f'{project_dir}/Dockerfile', 'w+') as f:
        f.write(template.dockerfile_template(rails_base_tag))

    with open(f'{project_dir}/Dockerfile-pro', 'w+') as f:
        f.write(template.dockerfile_pro_template(rails_base_tag))

    kwargs = dict(networks=['rod-network'])
    with open(f'{project_dir}/docker-compose.yml', 'w+') as f:
        if database == 'mysql':
            f.write(template.dc_rails_mariadb_template(None, **kwargs))
        elif database == 'postgresql':
            f.write(template.dc_rails_postgres_template(None, **kwargs))
        else:
            f.write(template.dc_rails_sqlite3_template(None, **kwargs))

    with open(f'{project_dir}/docker-compose-pro.yml', 'w+') as f:
        image_tag = f'{app_name}:latest'
        kwargs = dict(rails_env='production',**kwargs)
        if database == 'mysql':
            f.write(template.dc_rails_mariadb_template(image_tag, **kwargs))
        elif database == 'postgresql':
            f.write(template.dc_rails_postgres_template(image_tag, **kwargs))
        else:
            f.write(template.dc_rails_sqlite3_template(image_tag, **kwargs))

    with open(f'{project_dir}/config/database.yml', 'w+') as f:
        kwargs = dict(app_name = app_name, dev_password = None)
        if database == 'mysql':
            f.write(template.dc_mariadb_config(None, **kwargs))
        elif database == 'postgresql':
            f.write(template.dc_rails_postgres_template(None, **kwargs))
        else:
            f.write(template.dc_rails_sqlite3_template(None, **kwargs))

    rod_path = path.join(project_dir, 'rod')
    if not path.exists(rod_path):
        os.symlink(path.abspath(sys.argv[0]), rod_path)

def build_image(tag, project_dir):
    cmd = docker_cmds.build_image_cmd(tag, project_dir)
    run_cmd(cmd)

# Docker version 20.10.11, build dea9396
def generate_rails_project(options, rails_options):
    rails_base_tag= get_rails_image_name(options.version)
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()

    cmd = docker_base_cmd(rails_base_tag) + ['rails'] + rails_options
    res =  run_cmd(cmd)
    if not args_helper.is_dry_run():
        if res.returncode == 0:
            project_dir = os.path.join(cwd, rails_options[1])
            tag, release_tag = config.generate_project_tags(options.tag, project_dir)
            create_files_for_the_project(rails_base_tag, options.database, project_dir);
            config.write_rod(rails_base_tag, tag, release_tag, 'web', project_dir)
            if not options.skip_bundle:
                build_image(tag, project_dir)
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
    args_helper.set_global_args({'name': args.name, 'version': args.version, 'database': args.database})
    if args.skip_bundle:
        rails_options.append('-B')
        args_helper.set_global_args({'skip_bundle': True})
    generate_rails_project(args, rails_options)

def rails_command_handler(args):
    print(args)

def rails_command_server_handler(args):
    cmd = docker_compose_up_cmd('web')
    run_cmd(cmd)

def rails_command_console_handler(args):
    options = []
    rails_project_command('console', options)

def rake_assets_compile():
    full_tag = config.get_docker_compose_service()
    rake_base_cmd(full_tag, 'assets:precompile')

def build_production_image(args):
    # Compile assets
    # Build the image
    rake_assets_compile()
