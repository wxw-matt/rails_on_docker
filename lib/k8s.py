import yaml
from kubernetes import client, config
from lib import cmd_helper, config

def create_deployment(deployment_file):
    config.load_kube_config()

    with open(deployment_file) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment `%s` created." % resp.metadata.name)


def create_service(service_file, namespace='default'):
    cmds = ['kubectl', 'apply', '-f', service_file]
    cmd_helper.run_cmd(cmds)
    # Get port
    tag, release_tag = config.get_project_tags()
    app_name = tag.split(':')[0]
    cmds = ["kubectl", "get", "svc", app_name, "--namespace", namespace,
            "-o", "jsonpath={.spec.ports[0].nodePort}"]
    result = cmd_helper.run_cmd(cmds, output_stdout=False)
    port = result.stdout.decode("UTF-8")

    # Get hostname
    cmds = ["kubectl", "get", "svc", app_name, "--namespace", namespace,
            "-o", "jsonpath={.status.loadBalancer.ingress[0].hostname}"]
    result = cmd_helper.run_cmd(cmds, output_stdout=False)
    hostname = result.stdout.decode("UTF-8")
    print(f'Service is listening at address http://{hostname}:{port}')
