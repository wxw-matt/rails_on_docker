import subprocess
from lib import args_helper
from lib.docker_cmds import docker_compose_exec_cmd, docker_compose_run_cmd

def merge_cmds(cmds, extra):
    return [ c + extra for c in cmds]


def shell_cmd(cmd, full_tag, args_for_docker=[]):
    cmds = [
            docker_compose_exec_cmd(full_tag, args_for_docker) + [cmd],
            docker_compose_run_cmd(full_tag, args_for_docker) + [cmd]
            ]
    return cmds


# Docker version 20.10.11, build dea9396
def run_cmd(cmd, cmd_alt=None, output_error=True, output_stdout=True):
    if args_helper.is_dry_run():
        print('Dry run: ' + ' '.join(cmd))
        return
    if output_stdout:
        result = subprocess.run(cmd)
        if cmd_alt and result.returncode != 0:
            result = subprocess.run(cmd_alt)
    else:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        if cmd_alt and result.returncode != 0:
            result = subprocess.run(cmd_alt)
            if result.returncode != 0 and output_error:
                print(result.stdout.decode("UTF-8"))
    return result

