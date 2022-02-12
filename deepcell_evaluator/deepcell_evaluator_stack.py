from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)


from aws_cdk.aws_appsync import (
    CfnGraphQLSchema,
    CfnGraphQLApi,
    CfnApiKey,
    CfnDataSource, 
    CfnResolver

)
from aws_cdk.aws_dynamodb import (
    Table,
    Attribute,
    AttributeType,
    StreamViewType,
    BillingMode,

)
from aws_cdk.aws_iam import (
    Role,
    ServicePrincipal,
    ManagedPolicy,
)
import os.path
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
import aws_cdk.aws_apigatewayv2 as apigwv2

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, "files/graphql/schema.txt"), 'r') as file:
            data_schema = file.read().replace('\n', '')
with open(os.path.join(dirname, "files/resolver_functions/create_evaluation"), 'r') as file:
            create_evaluation = file.read().replace('\n', '')              
with open(os.path.join(dirname, "files/resolver_functions/update_evaluation"), 'r') as file:
            update_evaluation = file.read().replace('\n', '')
with open(os.path.join(dirname, "files/resolver_functions/get_evaluation"), 'r') as file:
            get_evaluation = file.read().replace('\n', '')   
with open(os.path.join(dirname, "files/resolver_functions/all_evaluations"), 'r') as file:
            all_evaluation = file.read().replace('\n', '')   
with open(os.path.join(dirname, "files/resolver_functions/delete_evaluation"), 'r') as file:
            delete_evaluation = file.read().replace('\n', '')                               

class DeepcellEvaluatorStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        deepcell_lambda_role = Role(
            self, 'DeepcellLambdaRole',
            assumed_by=ServicePrincipal('lambda.amazonaws.com')
        )

        deepcell_lambda_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "AdministratorAccess"
            )
        )
        
        deepcell_rest_lambda = _lambda.DockerImageFunction(self, "deepcell_rest_lambda_docker_from_image_asset",
            code=_lambda.DockerImageCode.from_image_asset(os.path.join(dirname, "lambdas/rest_api")),
            role=deepcell_lambda_role
        )
        
        deepcell_graphql_lambda = _lambda.DockerImageFunction(self, "deepcell_graphql_lambda_docker_from_image_asset",
            code=_lambda.DockerImageCode.from_image_asset(os.path.join(dirname, "lambdas/graphql_api")),
            role=deepcell_lambda_role
        )
                              
        apigw.LambdaRestApi(
            self, 'DeepcellRestApi-LambdaRest',
            handler=deepcell_rest_lambda,
            proxy=True
        )
        
        table_name = "deepcell"

        deepcell_graphql_api = CfnGraphQLApi(
            self,
            'DeepcellApi',
            name="deepcell-api",
            authentication_type='API_KEY'
        )
        
        CfnApiKey(
            self,
            'DeepcellGraphqlApiKey',
            api_id = deepcell_graphql_api.attr_api_id
        )
        
        api_schema = CfnGraphQLSchema(
            self,"DeepcellSchema",
            api_id = deepcell_graphql_api.attr_api_id,
            definition=data_schema
        )

        deepcell_table = Table(
            self, 'DeepcellTable',
            table_name=table_name,
            partition_key=Attribute(
                name='id',
                type=AttributeType.STRING,
            ),      
            billing_mode=BillingMode.PAY_PER_REQUEST,
            stream=StreamViewType.NEW_IMAGE,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        
        deepcell_table.grant_full_access(deepcell_rest_lambda)
        deepcell_table.grant_full_access(deepcell_graphql_lambda)

        deepcell_table_role = Role(
            self, 'DeepcellDynamoDBRole',
            assumed_by=ServicePrincipal('appsync.amazonaws.com')
        )

        deepcell_table_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                'AdministratorAccess'
            )
        )
        
        data_source = CfnDataSource(
            self, 'DeepcellLambdaDataSource',
            api_id=deepcell_graphql_api.attr_api_id,
            name='DeepcellLambdaDataSource',
            type='AWS_LAMBDA',
            lambda_config=CfnDataSource.LambdaConfigProperty(
                lambda_function_arn=deepcell_graphql_lambda.function_arn
            ),
            service_role_arn=deepcell_table_role.role_arn
        )
        
        data_source.add_depends_on(api_schema)

        get_evaluation_resolver = CfnResolver(
            self, 'GetOneQueryResolver',
            api_id=deepcell_graphql_api.attr_api_id,
            type_name='Query',
            field_name='getEvaluation',
            data_source_name=data_source.name,
            # request_mapping_template=get_evaluation, #Direct interaction with DynamoDB
            response_mapping_template="$util.toJson($ctx.result)"
        )

        get_evaluation_resolver.add_depends_on(data_source)

        get_all_evaluation_resolver = CfnResolver(
            self, 'GetAllQueryResolver',
            api_id=deepcell_graphql_api.attr_api_id,
            type_name='Query',
            field_name='allEvaluations',
            data_source_name=data_source.name,
            # request_mapping_template=all_evaluation,
            response_mapping_template="$util.toJson($ctx.result)"
        )

        get_all_evaluation_resolver.add_depends_on(data_source)
     
        create_evaluation_resolver = CfnResolver(
            self, 'CreateDeepcellMutationResolver',
            api_id=deepcell_graphql_api.attr_api_id,
            type_name='Mutation',
            field_name='createEvaluation',
            data_source_name=data_source.name,
            # request_mapping_template=create_evaluation,
            response_mapping_template="$util.toJson($ctx.result)"
        )

        create_evaluation_resolver.add_depends_on(data_source)

        update_evaluation_resolver = CfnResolver(
            self,'UpdateMutationResolver',
            api_id=deepcell_graphql_api.attr_api_id,
            type_name="Mutation",
            field_name="updateEvaluation",
            data_source_name=data_source.name,
            # request_mapping_template=update_evaluation,
            response_mapping_template="$util.toJson($ctx.result)"
        )
        update_evaluation_resolver.add_depends_on(data_source)

        delete_evaluation_resolver = CfnResolver(
            self, 'DeleteMutationResolver',
            api_id=deepcell_graphql_api.attr_api_id,
            type_name='Mutation',
            field_name='deleteEvaluation',
            data_source_name=data_source.name,
            # request_mapping_template=delete_evaluation,
            response_mapping_template="$util.toJson($ctx.result)"
        )
        
        delete_evaluation_resolver.add_depends_on(data_source)
        
        deepcell_rest_lambda.add_environment(
            key="DYNAMODB_TABLE_NAME",
            value=deepcell_table.table_name
        )  
        
        deepcell_graphql_lambda.add_environment(
            key="DYNAMODB_TABLE_NAME",
            value=deepcell_table.table_name
        )  