import random
import time
from kubernetes import client, config
import argparse

# Define arguments
argParser = argparse.ArgumentParser(
    prog='hello-greeter-chaos-monkey',
    description='Kills random pods in a namespace'
)
argParser.add_argument("-c", "--config", type=str, default='~/.kube/config', help="Kube config location")
argParser.add_argument("-d", "--delay", type=int, default='60', help="Delay between pod shutdown")
argParser.add_argument("-n", "--namespace", type=str, default='default', help="Target namespace")
argParser.add_argument("-t", "--timeout", type=int, default='60', help="Timeout in seconds")
args = argParser.parse_args()

# Load Kubernetes config
config.load_kube_config(config_file=args.config)

# Create a Kubernetes API client
v1 = client.CoreV1Api()

# Function to delete a random pod in the namespace
def delete_pod():
    pod_list = v1.list_namespaced_pod(args.namespace).items
    if pod_list:
        random_pod = random.choice(pod_list)
        v1.delete_namespaced_pod(random_pod.metadata.name, args.namespace)
        print(f"Deleted pod {random_pod.metadata.name} in namespace {args.namespace}")
    else:
        print(f"No pods in namespace {args.namespace}")

timeout = time.time() + args.timeout

if __name__ == "__main__":
    while time.time() < timeout:
        delete_pod()
        time.sleep(args.delay)