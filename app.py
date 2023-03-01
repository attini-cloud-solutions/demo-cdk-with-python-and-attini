#!/usr/bin/env python3
import os

import aws_cdk as cdk

from attini_cdk import AttiniRuntimeVariables as RuntimeVars

from infrastructure.cdk_project_stack import CdkProjectStack

app = cdk.App()

if RuntimeVars.ENVIRONMENT not in os.environ:
    os.environ[RuntimeVars.ENVIRONMENT] = "dev"


hello_world_stack = CdkProjectStack(app, "hello-world-stack",
                                    stack_name=f"{os.environ[RuntimeVars.ENVIRONMENT]}-hello-world-stack",
                                    env=cdk.Environment(
                                        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                        region=os.environ["CDK_DEFAULT_REGION"]
                                    ))

app.synth()
