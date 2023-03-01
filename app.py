#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.cdk_project_stack import CdkProjectStack

app = cdk.App()

if "ENV" not in os.environ:
    os.environ["ENV"]="dev"


hello_world_stack = CdkProjectStack(app, "hello-world-stack",
                                    stack_name=f"{os.environ['ENV']}-hello-world-stack",
                                    env=cdk.Environment(
                                        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                        region=os.environ["CDK_DEFAULT_REGION"]
                                    ))

app.synth()
