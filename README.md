
# Welcome to your CDK Python project with Attini

This is an example project that shows how to deploy a Python CDK App
using the Attini. 

## Install python dependency's

```bash
python -m pip install -r requirements.txt
```

## Usage

Find detailed information [here](https://attini.io/guides/get-started/).

### Deploy instructions

1. First make sure you are logged in to AWS using the AWS CLI
2. Bootstrap the CDK in your AWS account (`cdk bootstrap`)
2. Clone this Git repo
3. Open a shell in the repo

Install Attini CLI (ca 30 sec)
```bash
/bin/bash -c "$(curl -fsSL https://docs.attini.io/blob/attini-cli/install-cli.sh)"
```
Onboard the Attini framework (ca 4 min)
```bash
attini setup --give-admin-access --create-deployment-plan-default-role --create-init-deploy-default-role --accept-license-agreement 
```
Deploy to dev
```bash
attini environment create dev --env-type test 
attini deploy run . --environment dev 
```
Deploy to prod
```bash
attini environment create prod
attini deploy run . -e prod
```

# Fixes for common issues

### ModuleNotFoundError: No module named 'app'
Make sure you have set the PYTHONPATH environment to include your 
project.
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```