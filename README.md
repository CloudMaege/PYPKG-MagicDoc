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

## MagicDoc Command

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

<br>

## MagicDoc Show Commands

The `magicdoc show` command is a container for show subcommands. By itself this command will not return anything other then the help menu.

```bash
Usage: magicdoc.py show [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  files
```

<br>

### `magicdoc show files`

```yaml
magicdoc show files:
  Examples:
    magicdoc show files
    magicdoc -p terraform -d /path/to/module/sourcecode show files
    magicdoc -p terraform show files /path/to/module/sourcecode show files
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
    magicdoc -p terraform show variables /path/to/module/sourcecode show variables
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
    magicdoc -p terraform show variables /path/to/module/sourcecode show outputs
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
Using Directory Path: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module

3 tf outputs found in target project: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
codebuild_project_id        = aws_codebuild_project.this.id
codebuild_project_arn       = aws_codebuild_project.this.arn
codebuild_project_badge_url = aws_codebuild_project.this.badge_url
```

<br><br>
