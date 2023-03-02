from attini_cdk import (
    AttiniDeploymentPlanStack,
    AttiniCdk,
    AttiniRunnerJob,
    AttiniLambdaInvoke,
    DeploymentPlan,
    AttiniPayload
)
from constructs import Construct
import aws_cdk as cdk
import app as hello_world_app


class DeploymentPlanStack(AttiniDeploymentPlanStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_world_stack = hello_world_app.hello_world_stack
        sfn = cdk.aws_stepfunctions

        deploy_cdk_app = AttiniCdk(self, "deploy_cdk_app",
                                   path="./"
                                   )

        is_dev_condition = sfn.Condition.string_equals(
            AttiniPayload.ENVIRONMENT_PATH, "dev"
        )

        create_test_data = AttiniLambdaInvoke(self, "load_test_data_into_database",
                                              function_name=deploy_cdk_app.get_output(
                                                  hello_world_stack.artifact_id,
                                                  hello_world_stack.load_test_data_function_name
                                              ))

        run_load_test = AttiniRunnerJob(self, 'run_load_test',
                                        environment={
                                            "URL": deploy_cdk_app.get_output(
                                                        hello_world_stack.artifact_id,
                                                        hello_world_stack.function_url
                                                    )
                                        },
                                        commands=[
                                            "bash ./deployment_plan/load-test.sh"
                                        ])

        load_test_branch = create_test_data.next(run_load_test)

        success = sfn.Succeed(self, "success")

        DeploymentPlan(self, "deployment_plan",
                       definition=deploy_cdk_app.next(
                           sfn.Choice(self, "should_run_load_test?")
                           .when(is_dev_condition, load_test_branch)
                           .otherwise(success))
                       )


deployment_plan_app = cdk.App()

DeploymentPlanStack(deployment_plan_app, "DeploymentPlanAppStack")

deployment_plan_app.synth()
