# MagicDoc Automatated Project Documentation CLI Utility Package

__NOTE: This Library is STILL IN DEV as of this latest push on 02/02/2020.__

<br>

## Description

Documentation is a tedious task that most of the time is either ignored or completed with minimal detail and effort, potentially making it difficult for others to consume and adequately use the project being developed. For example, when building IaC for cloud environments, it can become an aggravating burden to take the time to document each module or project required to create and test the actual infrastructure necessary for personal or business workloads. MagicDoc is a tool that aims to help resolve that very problem and help to lessen and eventually eliminate that very burden. The goal of this project is to be able to very quickly and easily produce detailed, quality documentation within minutes, and without the need to write any markdown manually. A command here, a few sentences there, and poof, just like magic, MagicDoc has saved hours of time and created beautiful documentation for your project!

<br><br>

## Python Version

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br><br>

## Installation

This library has been published to [PyPi](https://pypi.org/project/magicdoc/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br>

```python
pip3 install magicdoc
```

<br>

## MagicDoc Commands

```yaml
magicdoc:
  Examples:
    magicdoc --help
    magicdoc -p terraform
    magicdoc -p terraform -d /path/to/module/sourcecode
  Arguments: None
  Options:
      provider:
          Description: The type of project or platform provider that is being used as the documentation source
          Value:
            - terraform | tf
            - Other platform providers currently in development
          Flag: --provider, -p
          Environment Variable: MAGICDOC_PROVIDER
          Required: Yes
      directory:
          Description: |
                The target directory containing the project source files that will be used as the documentation objective. This option exists so that the target directory can be set at the global level by an environment variable allowing all future commands to use its value. If this option is not set, then the target directory for the referenced command can take a directory argument directly when calling the command.
          Value: /path/to/project/files
          Flag: --directory, -d
          Environment Variable: MAGICDOC_DIRECTORY
          Required: No
  Commands:
    - show
```

<br><br>

## MagicDoc Show Commands

The `magicdoc show` command is a container for show subcommands. By itself this command will not return anything other then the help menu.

```bash
Usage: magicdoc.py show [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  files      Command that will retrieve a list of files from a target...
  outputs    Command that will retrieve a list of all of the project outputs...
  release    Command that will retrieve the project repository information...
  repo       Command that will retrieve the project repository information...
  variables  Command that will retrieve a list of all of the project...
```

<br>

### `magicdoc show files`

```yaml
magicdoc show files:
  Examples:
    magicdoc show files
    magicdoc -p terraform -d /path/to/module/sourcecode show files
    magicdoc -p terraform show files /path/to/module/sourcecode
  Arguments:
      directory:
          Description: The target directory containing the project source files that will be used as the documentation objective.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      subdir:
          Description: Flag to control recursive searchs through the target directory. If set to True, then the file search will be recursive, if False, then only the parent directory will be searched.
          Value:
            - True
            - False
          Flag: --directory, -d
          Environment Variable: MAGICDOC_SHOW_FILES_SUBDIR
          Default: True
          Required: No
```

<br>

```bash
Using Provider: tf
Using Directory Path: /Terraform/TF-AWS-CodeBuild-Module

7 tf files found in target directory: /Terraform/TF-AWS-CodeBuild-Module
outputs.tf
main.tf
variables.tf
/example => env.tfvars
/example => outputs.tf
/example => main.tf
/example => variables.tf
```

<br><br>

### `magicdoc show variables`

```yaml
magicdoc show variables:
  Examples:
    magicdoc show variables
    magicdoc -p terraform -d /path/to/module/sourcecode show variables
    magicdoc -p terraform show variables /path/to/module/sourcecode
  Arguments:
      directory:
          Description: The target directory containing the project source variables that will be used as the documentation objective.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      subdir:
          Description: Flag to control recursive searchs through the target directory. If set to True, then the file search will be recursive, if False, then only the parent directory will be searched.
          Value:
            - True
            - False
          Flag: --directory, -d
          Environment Variable: MAGICDOC_SHOW_FILES_SUBDIR
          Default: True
          Required: No
```

<br>

```bash
Using Provider: tf
Using Directory Path: /Terraform/TF-AWS-CodeBuild-Module

8 tf required variables found in target project: /Terraform/TF-AWS-CodeBuild-Module
codebuild_project_name     = Value Required
codebuild_project_desc     = Value Required
codebuild_service_role_arn = Value Required
codebuild_source_type      = Value Required
codebuild_source_url       = Value Required
codebuild_vpc              = Value Required
codebuild_subnet_list      = Value Required
codebuild_sg_list          = Value Required


16 tf optional variables found in target project: /Terraform/TF-AWS-CodeBuild-Module
codebuild_timeout             = 15
codebuild_badge               = True
codebuild_artifact_type       = NO_ARTIFACTS
codebuild_artifact_encryption = False
codebuild_encryption_key      = NULL
codebuild_artifact_bucket     = NULL
codebuild_artifact_path       = /
codebuild_source_branch       = master
codebuild_buildspec           = buildspec.yml
codebuild_buildspec_type      = FILENAME
codebuild_env_compute_type    = BUILD_GENERAL1_SMALL
codebuild_env_image           = aws/codebuild/standard:1.0
codebuild_env_type            = LINUX_CONTAINER
codebuild_env_variables       = [
{
    "name": "ENV_UPDATE",
    "value": "false"
}
{
    "name": "ENV_PKGS",
    "value": ""
}
{
    "name": "SOURCE_DIR_PREFIX",
    "value": ""
}
{
    "name": "LAMBDA_INDEX",
    "value": ""
}
{
    "name": "LAMBDA_FN_NAME",
    "value": ""
}
{
    "name": "LAMBDA_RUNTIME",
    "value": "python3.8"
}
{
    "name": "LAMBDA_ROLE",
    "value": ""
}
{
    "name": "LAMBDA_HANDLER_NAME",
    "value": ""
}
{
    "name": "LAMBDA_TIMEOUT",
    "value": "180"
}
{
    "name": "LAMBDA_VPC_SUBNETS",
    "value": ""
}
{
    "name": "LAMBDA_VPC_SGS",
    "value": ""
}
{
    "name": "LAMBDA_MEM",
    "value": ""
}
]
webhook_enable                = True
webhook_trigger               = PUSH
```

<br><br>

### `magicdoc show outputs`

```yaml
magicdoc show outputs:
  Examples:
    magicdoc show outputs
    magicdoc -p terraform -d /path/to/module/sourcecode show outputs
    magicdoc -p terraform show outputs /path/to/module/sourcecode
  Arguments:
      directory:
          Description: The target directory containing the project output files that will be used as the documentation objective.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      subdir:
          Description: Flag to control recursive searchs through the target directory. If set to True, then the file search will be recursive, if False, then only the parent directory will be searched.
          Value:
            - True
            - False
          Flag: --directory, -d
          Environment Variable: MAGICDOC_SHOW_FILES_SUBDIR
          Default: True
          Required: No
```

<br>

```bash
Using Provider: tf
Using Directory Path: /TF-AWS-CodeBuild-Module

3 tf outputs found in target project: /TF-AWS-CodeBuild-Module
codebuild_project_id        = aws_codebuild_project.this.id
codebuild_project_arn       = aws_codebuild_project.this.arn
codebuild_project_badge_url = aws_codebuild_project.this.badge_url
```

<br><br>

### `magicdoc show repo`

```yaml
magicdoc show files:
  Examples:
    magicdoc show repo
    magicdoc -p terraform -d /path/to/module/sourcecode show repo
    magicdoc -p terraform -d /path/to/module/sourcecode show repo -n rnason -r myRepo
    magicdoc -p terraform -d /path/to/module/sourcecode show repo -n rnason -r myRepo -t 12345678901....
    magicdoc -p terraform show repo /path/to/module/sourcecode -n rnason -r myRepo -t 12345678901...
  Arguments:
      directory:
          Description: The target directory containing the project source files that will be used as the documentation objective, this argument can be used to automatically pull the git repo options from .git/config.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      namespace:
          Description: Specify the repository namespace that will be used to search for the git repository.
          Value: rnason
          Flag: --namespace, -n
          Environment Variable: MAGICDOC_SHOW_REPO_NAMESPACE
          Default: None
          Required: Yes, unless it is desired to allow the command to attempt to configure this value from the .git/config file.
      repo:
          Description: Specify the repository to query for the targeted project data.
          Value: myModule
          Flag: --repo, -r
          Environment Variable: MAGICDOC_SHOW_REPO_REPO
          Default: None
          Required: Yes, unless it is desired to allow the command to attempt to configure this value from the .git/config file.
      token:
          Description: Specify a personal access token to use to access a private repository.
          Value: '1234567890098765432112345678900987654321'
          Flag: --token, -t
          Environment Variable: MAGICDOC_SHOW_REPO_TOKEN
          Default: None
          Required: No, only necessary if the repository is not public, then it would be required to gain access to the repo data.
```

<br>

```json
Using Provider: tf
Using Directory Path: /TF-AWS-CodeBuild-Lambda-Deployment-Pipeline-Common-Root

{
    "latest_release": "v1.1.1",
    "repo_description": "Terraform Root Project Module to deploy CodeBuild Lambda Common Resources",
    "repo_fullname": "NameSpace-TF/MyRepositoryName",
    "repo_name": "MyRepositoryName",
    "repo_owner": "NameSpace-TF",
    "repo_owner_url": "https://github.com/NameSpace-TF",
    "state": "pass",
    "status_code": 200
}
```

<br><br>

### `magicdoc show release`

```yaml
magicdoc show release:
  Examples:
    magicdoc show release
    magicdoc -p terraform -d /path/to/module/sourcecode show release
    magicdoc -p terraform -d /path/to/module/sourcecode show release -n rnason -r myRepo
    magicdoc -p terraform -d /path/to/module/sourcecode show release -n rnason -r myRepo -t 12345678901....
    magicdoc -p terraform show release /path/to/module/sourcecode -n rnason -r myRepo -t 12345678901...
  Arguments:
      directory:
          Description: The target directory containing the project source files that will be used as the documentation objective, this argument can be used to automatically pull the git repo options from .git/config.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      namespace:
          Description: Specify the repository namespace that will be used to search for the git repository.
          Value: rnason
          Flag: --namespace, -n
          Environment Variable: MAGICDOC_SHOW_REPO_NAMESPACE
          Default: None
          Required: Yes, unless it is desired to allow the command to attempt to configure this value from the .git/config file.
      repo:
          Description: Specify the repository to query for the targeted project data.
          Value: myModule
          Flag: --repo, -r
          Environment Variable: MAGICDOC_SHOW_REPO_REPO
          Default: None
          Required: Yes, unless it is desired to allow the command to attempt to configure this value from the .git/config file.
      token:
          Description: Specify a personal access token to use to access a private repository.
          Value: '1234567890098765432112345678900987654321'
          Flag: --token, -t
          Environment Variable: MAGICDOC_SHOW_REPO_TOKEN
          Default: None
          Required: No, only necessary if the repository is not public, then it would be required to gain access to the repo data.
```

<br>

```json
Using Provider: tf
Using Directory Path: /TF-AWS-CodeBuild-Lambda-Deployment-Pipeline-Common-Root

Latest Release: v1.1.1
```

<br><br>

## MagicDoc Gen Commands

The `magicdoc gen` command is a container for show subcommands. By itself this command will not return anything other then the help menu.

```bash
Usage: magicdoc.py show [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  files
```

<br>

### `magicdoc gen dirtree`

```yaml
magicdoc gen dirtree:
  Examples:
    magicdoc gen dirtree
    magicdoc -p terraform -d /path/to/module/sourcecode gen dirtree
    magicdoc -p terraform gen dirtree /path/to/module/sourcecode
  Arguments:
      directory:
          Description: The target directory containing the project source files that will be used as the documentation objective.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options: None
```

<br>

```bash
Using Provider: tf
Using Directory Path: /TF-AWS-CodeBuild-Module

.
├── outputs.tf
├── main.tf
├── CHANGELOG.md
├── images
│   ├── tf_s3.png
│   ├── optional.png
│   ├── neon_optional.png
│   ├── required.png
│   └── neon_required.png
├── example
│   ├── env.tfvars
│   ├── outputs.tf
│   ├── main.tf
│   ├── README.md
│   └── variables.tf
├── README.md
├── variables.tf
└── templates
    ├── LambdaPy_BuildSpec.yml
    └── LambdaJar_BuildSpec.yml
```

<br><br>
