from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3deploy
)
from aws_cdk.core import Stack

from aws_cdk.aws_iam import (
    Role,
    ServicePrincipal,
    ManagedPolicy
)

class DeepcellPublicSiteS3(Stack):
    def __init__(
        self,
        scope,
        construct_id,
        site_domain_name,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = None
        self.certificate = None
        self.distribution = None
        self._site_domain_name = site_domain_name


        self._build_site()
        
    def _build_site(self):

        self._create_site_bucket()
        
        self._create_s3_deployment()
        

    def _create_site_bucket(self):
        self.bucket = s3.Bucket(
            self,
            "site_bucket",
            bucket_name=self._site_domain_name,
            website_index_document="index.html",
            website_error_document="404.html",
            public_read_access=True
        )
        bucket_policy = iam.PolicyStatement(
            actions=["*"],
            resources=[
                self.bucket.bucket_arn,
                self.bucket.arn_for_objects('*')],
            principals=[iam.AnyPrincipal()],
        )

        self.bucket.add_to_resource_policy(bucket_policy)
        
        self.bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethods.POST, s3.HttpMethods.GET],
            allowed_origins=["*"]
        )
        
    def _create_s3_deployment(self):
        s3_role = Role(
            self, 'DeepcellS3Role',
            assumed_by=ServicePrincipal('lambda.amazonaws.com')
        )

        s3_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                'AdministratorAccess'
            )
        )
        
        s3deploy.BucketDeployment(
            self,'DeepcellEvaluatorDeploySite',
            destination_bucket=self.bucket,
            sources=[s3deploy.Source.asset("./deepcell_evaluator/views")],
            role=s3_role
        )
    