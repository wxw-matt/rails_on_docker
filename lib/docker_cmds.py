import os
from lib import config, args_helper, cmd_helper

def get_docker_compose_file():
    docker_compose_file = (args_helper.is_production() and 'docker-compose-pro.yml') or 'docker-compose.yml'
    return docker_compose_file

def docker_compose_run_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker-compose", '-f', get_docker_compose_file(), "run", "--rm", "--user", f'{uid}:{gid}',
        "-v", f'{cwd}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args

def docker_compose_exec_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker-compose", '-f', get_docker_compose_file(), "exec", "--user", f'{uid}:{gid}',
        "-e", "HOME=/app"] + args_for_docker + [full_tag]

    return args

def docker_base_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker", "run", "--rm", "-it","--user", f'{uid}:{gid}',
        "-v", f'{cwd}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args

def docker_project_base_cmd(full_tag, prject_dir,args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    args = ["docker", "run", "--rm", "-it","--user", f'{uid}:{gid}',
        "-v", f'{prject_dir}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args


def docker_compose_up_cmd(services=[]):
    if isinstance(services, str):
        services = [services]
    return ['docker-compose', '-f', get_docker_compose_file(), 'up', *services]

def docker_compose_shell_cmd(cmd, full_tag, args_for_docker=[]):
    cmds = [
        docker_compose_exec_cmd(full_tag, args_for_docker) + [cmd],
        docker_compose_run_cmd(full_tag, args_for_docker) + [cmd]
    ]
    return cmds

def get_minikube_envs():
    cmds = ['minikube', 'docker-env']
    res = cmd_helper.run_cmd_no_dry_run(cmds, output_stdout=False)
    output = res.stdout.decode("UTF-8")
    env_data = list(filter(lambda x: '=' in x, output.split()))
    envs = {}
    for data in env_data:
        name, value = data.replace('"', '').split('=')
        envs[name]=value
    return envs

def build_image_cmd(tag, project_dir, dockerfile='Dockerfile'):
    args = ['docker', 'build', '-f', os.path.join(project_dir,dockerfile), '-t', tag, project_dir]
    if cmd_helper.is_load_supported():
        args.insert(2, '--load')
    return args

