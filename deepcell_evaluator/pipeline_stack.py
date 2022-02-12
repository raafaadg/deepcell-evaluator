from aws_cdk import core
from aws_cdk import pipelines
from aws_cdk.aws_secretsmanager import Secret
from deepcell_evaluator.webservice_stage import WebServiceStage

class PipelineStack(core.Stack):
    def __init__(self, scope:core.Construct, id:str,**kwargs):
        super().__init__(scope,id,**kwargs)
        
        # docker_hub_secret = Secret.from_secret_complete_arn(
        #     self,
        #     "DHSecret",
        #     "arn:aws:secretsmanager:us-east-1:742781758581:secret:docker_hub_secret-pgpMDM"
        #     )
        
        pipeline = pipelines.CodePipeline(
            self, 'Pipeline',
            docker_enabled_for_self_mutation=True,
            docker_enabled_for_synth=True,
            # docker_credentials=[
            #     pipelines.DockerCredential.docker_hub(docker_hub_secret),
            #     pipelines.DockerCredential.custom_registry("https://index.docker.io/v1/", docker_hub_secret)
            # ],
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.git_hub(
                    repo_string=f"{self.node.try_get_context('owner')}/{self.node.try_get_context('repo')}",
                    branch=self.node.try_get_context('branch'),
                    authentication=core.SecretValue.secrets_manager('github')
                ),
                install_commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    ],
                commands=[
                    "pytest",
                    "cdk synth"
                ]
            )
        )
        
        pipeline.add_stage(
            WebServiceStage(
                self,
                'Production-Stack',
                )
            )