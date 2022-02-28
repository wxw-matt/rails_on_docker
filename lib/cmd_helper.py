import subprocess
from lib import args_helper

def merge_cmds(cmds, extra):
    return [ c + extra for c in cmds]

def is_load_supported():
    args = ["docker", "build", "-h"]
    result = run_cmd_no_dry_run(args, output_error = False, output_stdout = False)
    return '--load' in result.stdout.decode("UTF-8")


# Docker version 20.10.11, build dea9396
def run_cmd(cmd, cmd_alt=None, output_error=True, output_stdout=True):
    if args_helper.is_dry_run():
        print('Dry run: ' + ' '.join(cmd))
        return
    return run_cmd_no_dry_run(cmd, cmd_alt, output_error, output_stdout)


# Docker version 20.10.11, build dea9396
def run_cmd_no_dry_run(cmd, cmd_alt=None, output_error=True, output_stdout=True):
    kwargs = {}
    if not output_stdout:
        kwargs = dict(stdout=subprocess.PIPE, **kwargs)

    if not output_error:
        kwargs = dict(stderr=subprocess.PIPE, **kwargs)

    result = subprocess.run(cmd, **kwargs)
    if cmd_alt and result.returncode != 0:
        result = subprocess.run(cmd_alt, **kwargs)

    return result

