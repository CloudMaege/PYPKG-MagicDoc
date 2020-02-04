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

### `magicdoc gen config`

```yaml
magicdoc gen config:
  Examples:
    magicdoc gen config
    magicdoc -p terraform -d /path/to/module/sourcecode gen config
    magicdoc -p terraform gen config /path/to/module/sourcecode
  Arguments:
      directory:
          Description: The destination directory where the config file will be written to upon rendering.
          Value: /path/to/project/files
          Default: ./
          Required: No, If no directory is specified then magicdoc will use the current working directory.
  Options:
      template_dir:
          Description: Specify the directory path location of the directory that contains the desired config jinja template. Default settting will use the packaged template.
          Value: /path/to/templates/directory
          Flag: --template_dir, -td
          Environment Variable: MAGICDOC_GEN_CONFIG_TEMPLATE_DIR
          Default: None (Class assign's default value of the internal package template directory.)
          Required: No
      template:
          Description: Specify the jinja template file that will be used to generate the project config. Default value is the packaged magicdoc config template.
          Value: /path/to/templates/template
          Flag: --template, -t
          Environment Variable: MAGICDOC_GEN_CONFIG_TEMPLATE
          Default: magicdoc_config.j2
          Required: No
      filename:
          Description: Specify the name that will be used for the config file output. Default is README.yaml.
          Value: magicdoc.yaml (Must be saved as YAML for future processing and usage)
          Flag: --filename, -f
          Environment Variable: MAGICDOC_GEN_CONFIG_FILENAME
          Default: README.yaml
          Required: No
      overwrite:
          Description: Flag to allow over writing the current configuration file if one already exists in the provided config output path.
          Value:
            - True
            - False
          Flag: --overwrite, -ow
          Environment Variable: MAGICDOC_GEN_CONFIG_OVERWRITE
          Default: False
          Required: No
```

<br>

```bash
#############################
# Repository Configuration: #
#############################
Repository:
    OwnerOverride:
    NameSpace:
    Name:
    Version:

############################
# README.md Configuration: #
############################
README:
    Title: 
    HeroImage:
    DocLink:
    #=====================#
    # README.md Sections: #
    #=====================#
    GettingStarted: >-
        Project Description.....
    PreRequisites: >-
        This module does not currently have any pre-requisites or dependency requirements.
    Usage:
        ExampleResourceName:
############################
# Variables Configuration: #
############################
Variables:
    #=====================#
    # Required Variables: #
    #=====================#
    Required:
        Image:
        codebuild_project_name:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the Name that will be given to the CodeBuild project that will be deployed.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_project_desc:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify a description for the CodeBuild project that will be deployed.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_service_role_arn:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the ARN of the role that will be assumed by the CodeBuild service to execute the build job.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_source_type:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the source repository type or vendor that this CodeBuild job will use. Valid Values are CODECOMMIT, CODEPIPELINE, GITHUB, GITHUB_ENTERPRISE, BITBUCKET, S3 or NO_SOURCE
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_source_url:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the source repository URL that CodeBuild will clone from. This is the repository of the project that will be build by this CodeBuild job.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_vpc:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the Id of the VPC that CodeBuild will be launched into. Example: vpc-xxxxxxxx
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_subnet_list:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the subnets that CodeBuild will be placed on within the specified VPC
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_sg_list:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the Security Groups that will be applied to the CodeBuild job within the specified VPC
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
    #=====================#
    # Optional Variables: #
    #=====================#
    Optional:
        Image:
        codebuild_timeout:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the max amount of time in minutes that the CodeBuild job can run. Value must between 5 Min and 480 Min or 8 hours. Default value 15 min
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_badge:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify if CodeBuild should construct a build state badge for the project. Default True
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_artifact_type:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify type of artifact that the provisioned CodeBuild job will produce. Valid values are CODEPIPELINE, S3, or NO_ARTIFACTS. Default set NO_ARTIFACTS
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_artifact_encryption:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify if any CodeBuild artifacts should be encrypted. This option only applies to artifacts that will be pushed to S3. Default False
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_encryption_key:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the ARN of the KMS CMK that will be used to encrypt object pushed to the supplied S3 bucket. This option only applies if codebuild_artifact_encryption is true
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_artifact_bucket:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the Name of the S3 bucket that will be used for built artifact storage.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_artifact_path:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the path in the destination artifact bucket where produced artifacts will be pushed. Default set to /
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_source_branch:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the GIT repository branch that the codebuild job will monitor and pull from.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_buildspec:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the local path or repo file name of the buildspec file that will used during build execution. Available pre-built buildspecs are 'LambdaPy' and LambdaJar
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_buildspec_type:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify if the provided buildspec file value references a pre-built file template or simply a file name. Valid values are 'FILE', 'FILENAME' and 'PREBUILT'
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_env_compute_type:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the CodeBuild environment Compute Type to be provisioned. Valid Values are BUILD_GENERAL1_SMALL, BUILD_GENERAL1_MEDIUM and BUILD_GENERAL1_LARGE.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_env_image:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the image that CodeBuild will use for the build environment. Default set to Ubuntu aws/codebuild/standard:1.0
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_env_type:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify the CodeBuild environment type. Valid Values are 'LINUX_CONTAINER' and 'WINDOWS_CONTAINER'. Default set to LINUX_CONTAINER
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        codebuild_env_variables:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify a map of environment variables that will be passed to and used by the CodeBuild job.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        webhook_enable:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify if a webhook should be created and added to the CodeBuild job to build on commit.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
        webhook_trigger:
            ExampleValue:
            GeneralDetails:
                Description: >-
                    Specify a comma separated string of event types that will trigger the execution of this job. Valid values are PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED, PULL_REQUEST_REOPENED, PULL_REQUEST_MERGED.
                Note:
                Image:
            VarDetails:
                Description:
                Note:
                Image:
            UsageDetails:
                Description:
                Note:
                Image:
```

<br><br>
