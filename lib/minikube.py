from lib import cmd_helper

def is_minikube_running():
    cmds = ['minikube', 'status']
    res = cmd_helper.run_cmd_no_dry_run(cmds, output_stdout=False)
    return res.returncode == 0

def get_minikube_envs():
    envs = {}
    cmds = ['minikube', 'docker-env']
    res = cmd_helper.run_cmd_no_dry_run(cmds, output_stdout=False)
    if res.returncode == 0:
        output = res.stdout.decode("UTF-8")
        env_data = list(filter(lambda x: '=' in x, output.split()))
        for data in env_data:
            name, value = data.replace('"', '').split('=')
            envs[name]=value
    return envs


