from prefect.run_configs import KubernetesRun, RunConfig
from prefect.storage.github import GitHub
from prefect.client.secrets import Secret

def set_run_config() -> RunConfig:
    return KubernetesRun(
        labels=["aws"],
        image="docker push purplebeast786/dummy:latest",
        image_pull_policy="IfNotPresent",
        cpu_request="1",
        memory_request="2G",
        job_template={
            "apiVersion": "batch/v1",   
            "kind": "Job",
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "execution-model": "provisioned"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "flow"
                            }
                        ],
                        # "nodeSelector": {
                        #     "execution-model": "serverless"
                        # },
                        # "tolerations": [
                        #     {
                        #         "key": "virtual-kubelet.io/provider",
                        #         "operator": "Exists"
                        #     }
                        # ]
                    }
                }
            }
        }
    )


def set_storage(flow_name: str) -> GitHub:
    return GitHub(
        repo="k1ngAlakazam/prefect-k8s",
        path=f"flows/{flow_name}.py",
        access_token_secret="GITHUB_ACCESS_TOKEN",
    )