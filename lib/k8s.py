import yaml
from kubernetes import client, config

def create_deployment(deployment_file):
    config.load_kube_config()

    with open(deployment_file) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment `%s` created." % resp.metadata.name)
