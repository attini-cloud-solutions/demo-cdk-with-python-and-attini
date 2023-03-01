from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)

from constructs import Construct


class CdkProjectStack(Stack):
    # These attributes will be used for the CFN Output names, and they will be used by the deployment plan
    # to reference the CFN Output.
    function_url = "FunctionUrl"
    load_test_data_function_name = "LoadTestDataFunction"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        database = dynamodb.Table(self, "table",
                                  partition_key=dynamodb.Attribute(
                                      name="Id",
                                      type=dynamodb.AttributeType.STRING
                                  ),
                                  billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
                                  )

        hello_world_role = iam.Role(self, "hello_world_role",
                                    assumed_by=iam.ServicePrincipal(
                                        "lambda.amazonaws.com"
                                    ))

        database.grant_read_write_data(hello_world_role)

        hello_world = lambda_.Function(self, "hello_world",
                                       runtime=lambda_.Runtime.PYTHON_3_9,
                                       handler="hello_world.lambda_handler",
                                       code=lambda_.Code.from_asset("hello_world/function/"),
                                       memory_size=256,
                                       timeout=Duration.minutes(2),
                                       log_retention=logs.RetentionDays.THREE_MONTHS,
                                       role=hello_world_role,
                                       environment={
                                           "DATABASE_NAME": database.table_name
                                       })

        hello_world_url = hello_world.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE
        )

        CfnOutput(self, self.function_url,
                  value=hello_world_url.url
                  )

        create_test_data_role = iam.Role(self, "create_test_data_role",
                                         assumed_by=iam.ServicePrincipal(
                                             "lambda.amazonaws.com"
                                         ))

        database.grant_read_write_data(create_test_data_role)

        create_test_data_function = lambda_.Function(self, "create_test_data_function",
                                                     runtime=lambda_.Runtime.PYTHON_3_9,
                                                     handler="test_data.lambda_handler",
                                                     code=lambda_.Code.from_asset("hello_world/test_data/"),
                                                     log_retention=logs.RetentionDays.THREE_MONTHS,
                                                     role=create_test_data_role,
                                                     environment={
                                                         "DATABASE_NAME": database.table_name,
                                                     })

        CfnOutput(self, self.load_test_data_function_name,
                  value=create_test_data_function.function_name
                  )
