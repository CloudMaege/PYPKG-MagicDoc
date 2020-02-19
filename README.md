# MagicDoc Automatated Project Documentation CLI Utility Package

> __NOTE: This Project is currently IN Beta as of this latest push on 02/19/2020.__

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

<br><br>

## MagicDoc Commands

```yaml
magicdoc:
    Examples:
        magicdoc --help
    Arguments: None
    Options: None
```

<br><br>

## MagicDoc Provider Sub-Command Groups:

```yaml
tf:
    Descripton: the tf subcommand sets the engine provider to terraform, loads the necessary terraform parsing libraries, and instantiates the necessary terraform objects to initialize terraform parsing capabilities.
    Examples:
        magicdoc tf
        magicdoc tf --help
    Arguments: None
    Options:
        verbose:
            Description: Enables / Disables Verbose logging
            Value: bool
            Flag: --verbose, -v
            Environment Variable: MAGICDOC_TF_VERBOSE
            Required: No
            Default: False
        verbose_level:
            Description: |
                    All application processes use standard logging format to include DEBUG, INFO, WARNING, and ERROR. By passing the -l flag the user user can specify the level of verbosity that they wish to see. Passing -l INFO for example will exclude debug logs, yet still allow INFO, WARNING, and ERROR messages to display in the cli console.
            Value: DEBUG | INFO | WARNING | ERROR
            Flag: --logging_level, -l
            Environment Variable: MAGICDOC_TF_VERBOSE_LEVEL
            Required: No
            Default: DEBUG
        directory:
            Description: |
                    By default magicdoc will use the current directory path, however if an alternative directory is desired, then the -d flag can be used to specify the desired target directory path for the command execution.
            Value: Must be valid directory path.
            Flag: --dir, -d
            Environment Variable: MAGICDOC_TF_DIRECTORY
            Required: No
            Default: Current Working Directory
        exclude_dir:
            Description: |
                    When searching a directory location for terraform files to parse, in the event that a directory exists in the parent target directory, that is not a desired search directory, it can be excluded using the -e flag. If specified, then the file search operation will ignore the specified subdirectory if it exists.
            Value: Must be valid directory path.
            Flag: --exclude_dir, -e
            Environment Variable: MAGICDOC_TF_EXCLUDE_DIR
            Required: No
            Default: None
        config:
            Description: |
                    The -c flag allows the user to specify the location of the target project magicdoc configuration file. By default magicdoc will look for the presense of a `magicdoc.yaml` file. Users can name the config file by another filename when creating the config, however the file must be a yaml formatted file, and if an alternative filename is specified then this option must be issued in order for magicdoc to be able to effectively find the config file that will be used to generate the documentation.
            Value: Must be valid file path.
            Flag: --config, -c
            Environment Variable: MAGICDOC_TF_CONFIG
            Required: No
            Default: magicdoc.yaml
        no_recursion:
            Description: |
                    The -nr flag is used to tell magicdoc to not search any subdirectories in a target project path. If the -nr flag is set, then only the parent target directory will be searched for terraform files, which will also automatically exclude subdirectories from variables and outputs search.
            Value: bool
            Flag: --no_recursion, -nr
            Environment Variable: MAGICDOC_TF_NO_RECURSION
            Required: No
            Default: True (Recursion enabled)
    Available Sub-Commands:
        - env
        - show
        - create
```

<br><br>

## MagicDoc TF Show Env

The `magicdoc tf env` command will display information about the tf provider environment. It will display information such as if default template directory was found, what target directory path was specified, if a terraform object could be instantiated, meaning that magicdoc was able to find parsable terraform files in the target directory, and what flags where passed to the command. Its a simple check command for a quick look at how the tf provider environment is constructed when issued against a target project directory.

<br>

```yaml
env:
    Examples:
        magicdoc tf env
    Arguments: None
    Options: None
```
<br><br>

## MagicDoc TF Show Commands

The `magicdoc tf show` command is a container for show subcommands. By itself this command will not return anything other then the help menu.

```bash
Usage: magicdoc tf show [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  files      Display the terraform target project file lists.
  git        Display Terraform Project Git Config Data
  graph      Display Terraform Project dot Graph Object
  outputs    Display Terraform Project Outputs
  release    Display Terraform Project Latest Release
  repo       Display Terraform Project Git Repository Data
  tree       Display Terraform Project Directory Tree
  variables  Display Terraform Project Variables.
```

<br>

### `magicdoc tf show files`

The `magicdoc tf show files` command will display all of the .tf and .tfvar files in the target project directory that magicdoc was able to find and will use to perform its search and parse operation for Terraform variables and outputs.

<br>

```yaml
magicdoc tf show files:
  Examples:
    magicdoc tf show files
    magicdoc tf -d /path/to/module/sourcecode show files
  Arguments: None
  Options: None
```

<br>

```bash
MagicDoc Terraform Project File Summary:
========================================

MagicDoc [tf show files] Command Environment:
Gathering Terraform Project Files...

Terraform file search target directory location: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
  -> 6 terraform file(s) found in target directory.
  -> 1 tfvar file(s) found in target directory.

Terraform .tf files:
====================
outputs.tf
main.tf
variables.tf
example/outputs.tf
example/main.tf
example/variables.tf

Terraform .tfvar files:
=======================
example/env.tfvars
```

<br><br>

### `magicdoc tf show variables`

The `magicdoc tf show variables` command will display an output of all terraform variables that were found in the `variables.tf` file within the target project directory. Magicdoc will use the variables that it was able to parse from any found variable.tf files when constructing both the config file as well as the readme documentation.

<br>

```yaml
magicdoc show variables:
  Examples:
    magicdoc tf show variables
    magicdoc tf -d /path/to/module/sourcecode show variables
  Arguments: None
  Options:
      include_examples:
          Description: Instructs the variables execution environment to include and parse files in any `example` or `examples` subdirectories located in the parent target project directory. By default directories named `example`, or `examples` are excluded from the file/variable/output search results, and are not parsed or included.
          Value: bool
          Flag: --include_examples, -1
          Environment Variable: MAGICDOC_TF_SHOW_VARIABLES_INCLUDE_EXAMPLES
          Required: No
          Default: False
```

<br>

```bash
  Environment: Verbose Attribute Set:                False
  Log: Verbose Attribute Set:                        False
  Environment: Verbose Level Attribute Set:          debug

MagicDoc Terraform Project Variable Summary:
============================================
  Include Example Directories:                       False

MagicDoc [tf show variables] Command Environment:
Gathering Terraform Project Files...

Parsing variables.tf files for Terraform variables...
Scanning project directory for defined module variables...
Terraform variable search target directory location: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
 -> 8 required terraform project variables found in target project: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
 -> 13 optional terraform project variables found in target project: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module

Terraform Project Required Variables:
=====================================
codebuild_project_name     = 'Required Value'
codebuild_project_desc     = 'Required Value'
codebuild_service_role_arn = 'Required Value'
codebuild_source_type      = 'Required Value'
codebuild_source_url       = 'Required Value'
codebuild_vpc              = 'Required Value'
codebuild_subnet_list      = [
    'Required_Value_1'
    'Required_Value_2'
]
codebuild_sg_list          = [
    'Required_Value_1'
    'Required_Value_2'
]

Terraform Project Optional Variables:
=====================================
codebuild_timeout             = 15
codebuild_badge               = 'True'
codebuild_artifact_type       = 'NO_ARTIFACTS'
codebuild_artifact_encryption = 'False'
codebuild_encryption_key      = 'NULL'
codebuild_artifact_bucket     = 'NULL'
codebuild_artifact_path       = '/'
codebuild_source_branch       = 'master'
codebuild_buildspec           = 'buildspec.yml'
codebuild_buildspec_type      = 'FILENAME'
codebuild_env_compute_type    = 'BUILD_GENERAL1_SMALL'
codebuild_env_image           = 'aws/codebuild/standard:1.0'
codebuild_env_type            = 'LINUX_CONTAINER'
```

<br><br>

### `magicdoc tf show outputs`

The `magicdoc tf show outputs` command will display an output of all terraform outputs that were found in the `outputs.tf` file within the target project directory. Magicdoc will use the outputs that it was able to parse from any found outputs.tf files when constructing the readme documentation.

<br>

```yaml
magicdoc tf show outputs:
  Examples:
    magicdoc tf show outputs
    magicdoc tf -d /path/to/module/sourcecode show outputs
  Arguments: None
  Options:
      include_examples:
          Description: Instructs the variables execution environment to include and parse files in any `example` or `examples` subdirectories located in the parent target project directory. By default directories named `example`, or `examples` are excluded from the file/variable/output search results, and are not parsed or included.
          Value: bool
          Flag: --include_examples, -i
          Environment Variable: MAGICDOC_TF_SHOW_VARIABLES_INCLUDE_EXAMPLES
          Required: No
          Default: False
```

<br>

```bash
  Environment: Verbose Attribute Set:                False
  Log: Verbose Attribute Set:                        False
  Environment: Verbose Level Attribute Set:          debug

MagicDoc Terraform Project Outputs Summary:
===========================================
  Include Example Directories:                       False

MagicDoc [tf show outputs] Command Environment:
Gathering Terraform Project Variables...

Parsing outputs.tf files for Terraform outputs...
Scanning project directory for defined module outputs...
Terraform output search target directory location: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
 -> 3 terraform project outputs found in target project: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module

codebuild_project_id        = {
    aws_codebuild_project.this.id
}

codebuild_project_arn       = {
    aws_codebuild_project.this.arn
}

codebuild_project_badge_url = {
    aws_codebuild_project.this.badge_url
}
```

<br><br>

### `magicdoc tf show graph`

The `magicdoc tf show graph` command will tell magicdoc to initialize the terraform project directory by issuing a `terraform init` on the directory. It will then run a `terraform graph` command and store the dot formatted graph data, and display it to the screen. Magicdoc will use this data to automatically construct, and render the terraform graph in PNG format if the `dot` binary file can be found within the executing systems path. If magicdoc is successful in rendering the dot graph into a PNG file, the file will be placed into a images directory in the target project path, and then included in the readme documentation when renderend.

<br>

```yaml
magicdoc tf show graph:
  Examples:
    magicdoc tf show graph
    magicdoc tf -d /path/to/module/sourcecode show graph
  Arguments: None
  Options:
      overwrite:
          Description: Instructs magicdoc to overwrite any existing .terraform directory if one is already found in the target project directory. If magicdoc does not find a .terraform directory, it will perform the `terraform init` run the graph dot file generation, and then remove the .terraform directory that it created in generating the graph data.
          Value: bool
          Flag: --overwrite, -o
          Environment Variable: MAGICDOC_TF_SHOW_GRAPH_OVERWRITE
          Required: No
          Default: False
```

<br>

```bash
MagicDoc Terraform Project Graph dot Structure:
===============================================
  Overwrite Existing .terraform Directory:           False

MagicDoc [tf show graph] Command Environment:
Generating Terraform Project Graph...

Generating terraform graph dot object...
CLS->TFMagicDoc.terraform_init: Executing `terraform init` on target project directory: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module

Initializing the backend...

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "aws" (hashicorp/aws) 2.49.0...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.aws: version = "~> 2.49"

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
CLS->TFMagicDoc.terraform_init: Execution of `terraform init` completed successfully against the target directory: /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
digraph {
        compound = "true"
        newrank = "true"
        subgraph "root" {
                "[root] aws_codebuild_project.this" [label = "aws_codebuild_project.this", shape = "box"]
                "[root] aws_codebuild_webhook.this" [label = "aws_codebuild_webhook.this", shape = "box"]
                "[root] local.buildspec_file" [label = "local.buildspec_file", shape = "note"]
                "[root] local.codebuild_compute_env" [label = "local.codebuild_compute_env", shape = "note"]
                "[root] local.prebuilt_buildspec" [label = "local.prebuilt_buildspec", shape = "note"]
                "[root] output.codebuild_project_arn" [label = "output.codebuild_project_arn", shape = "note"]
                "[root] output.codebuild_project_badge_url" [label = "output.codebuild_project_badge_url", shape = "note"]
                "[root] output.codebuild_project_id" [label = "output.codebuild_project_id", shape = "note"]
                ...etc
        }
}
```

<br><br>

### `magicdoc tf show git`

The `magicdoc tf show git` command will display the git repository information that it was able to parse from the existing `.git/config` directory if one is present in the target project directory. Magicdoc will use the information that its able to parse from the .git/config file to form the requests to github to query for latest release data prior to document generation.

<br>

```yaml
magicdoc tf show git:
  Examples:
    magicdoc tf show git
    magicdoc tf -d /path/to/module/sourcecode show git
  Arguments: None
  Options:
      auth:
          Description: Passed a git repository personal access token to magicdoc, and is used to construct the appropriate header auth request when requesting data from the configured git repository.
          Value: token
          Flag: --auth, -a
          Environment Variable: MAGICDOC_TF_SHOW_REPO_AUTH
          Required: No
          Default: None
```

<br>

```bash
MagicDoc Terraform Project Git Config:
======================================

MagicDoc [tf show git] Command Environment:
Parsing Terraform Project Git Config...

Attempting to parse target project git config...
{
    url       = 'git@github.com:CloudMage-TF/TF-AWS-Test-Module.git'
    namespace = 'CloudMage-TF'
    name      = 'TF-AWS-Test-Module.git'
    provider  = 'github.com'
}
```

<br><br>

### `magicdoc tf show repo`

The `magicdoc tf show repo` command will display the git repository information that it was able to get from performing an API request to the repository found in the .git/config directory. The API collects just relevant information that was determined to be useful in aiding to provide data to the readme document that will be constructed. If the repository is a private repository an auth token can be passed using the -a flag.

<br>

```yaml
magicdoc tf show repo:
  Examples:
    magicdoc tf show repo
    magicdoc tf show repo -a "0123456789109876543210"
    magicdoc tf -d /path/to/module/sourcecode show repo
  Arguments: None
  Options:
      auth:
          Description: Passed a git repository personal access token to magicdoc, and is used to construct the appropriate header auth request when requesting data from the configured git repository.
          Value: token
          Flag: --auth, -a
          Environment Variable: MAGICDOC_TF_SHOW_REPO_AUTH
          Required: No
          Default: None
```

<br>

```bash
MagicDoc Terraform Project Latest Release:
==========================================
  Git Authentication Token Provided:                 True


MagicDoc [tf show release] Command Environment:
Sending Terraform Project Git Release Request...


Project Latest Release:
=======================
  TF-AWS-ResourceNaming-Module Latest Release:            v1.0.5
```

<br><br>

### `magicdoc tf show tree`

The `magicdoc tf show tree` command will construct and display an ascii style directory tree listing for the target project directory. During the data gathering stage, magicdoc will construct this tree view of the target project directory and include the output into the readme documentation.

<br>

```yaml
magicdoc tf show tree:
  Examples:
    magicdoc tf show tree
    magicdoc tf -d /path/to/module/sourcecode show tree
  Arguments: None
  Options: None
```

<br>

```bash
  Environment: Verbose Attribute Set:                False
  Log: Verbose Attribute Set:                        False
  Environment: Verbose Level Attribute Set:          debug
  Log: Verbose Level Attribute Set:                  debug
  Environment: Template Path Set:                    /Volumes/MacData/Work/CloudMage/PythonLibs/PyPkgs-MagicDoc/magicdoc/templates
  Environment: Directory Recursion Set:              False

Scanning project directory for terraform .tf and .tfvar files...
Usage: main.py tf create [OPTIONS] COMMAND [ARGS]...

  Create a Magicdoc config or Documentation for your project.


MagicDoc Terraform Project Directory Tree Structure:
====================================================

MagicDoc [tf show tree] Command Environment:
Gathering Terraform Project Outputs...

.
├── outputs.tf
├── .DS_Store
├── Makefile
├── README.md
├── .gitignore
├── variables.tf
└── magicdoc.yaml
```

<br><br>

## MagicDoc TF Create Commands

The `magicdoc tf create` command is a container for create subcommands. By itself this command will not return anything other then the help menu.

<br>

```bash
Usage: magicdoc.py create [OPTIONS] COMMAND [ARGS]...

  Environment: Verbose Attribute Set:                False
  Log: Verbose Attribute Set:                        False
  Environment: Verbose Level Attribute Set:          debug
  Log: Verbose Level Attribute Set:                  debug
  Environment: Template Path Set:                    /Volumes/MacData/Work/CloudMage/PythonLibs/PyPkgs-MagicDoc/magicdoc/templates
  Environment: Directory Recursion Set:              False

Scanning project directory for terraform .tf and .tfvar files...
Usage: main.py tf create [OPTIONS] COMMAND [ARGS]...

  Create a Magicdoc config or Documentation for your project.

Options:
  --help  Show this message and exit.

Commands:
  config  Create a magicdoc project configuration file.
  doc     Create a terraform module or project README.md file.
```

<br>

### `magicdoc tf create config`

Command to generate a magicdoc config file for the target terraform project. The config file allows a user to supply additional information that will be rendered into the generated readme document. The command takes 1 option, being the type, identifying the type of project/the template used to render the document. The valid available option choices are `module` and `root`, although currently only module will work as a root template is still currently in development. If no option is selected, then magicdoc will default to module. The `create config` command also takes a single optional argument that will allow the command issuer the ability to name the config file something other then magicdoc.yaml. If a custom config name is specified then subsequent commands to generate or regenerate the document will require that the `magicdoc tf -c /path/to/confg` option is set. The file must be a yaml file extention, and this is forced, meaning that even if a custom file name is provided without a yaml extention, magicdoc will remove the extention and append .yaml to the custom config name.

<br>

```yaml
magicdoc tf create config -t <type> <filename>:
  Examples:
    magicdoc tf create config
    magicdoc tf create config - module
    magicdoc tf create config -t module project.yaml
    magicdoc tf -d /path/to/module/sourcecode create config
    magicdoc tf -d /path/to/module/sourcecode create config -t module
    magicdoc tf -d /path/to/module/sourcecode create config -t module config.yaml
  Arguments:
      filename:
          Description: The custom name that will be given to the config file that is produced and written to the target project directory.
          Value: Any string value that will be set as the project config file name.
          Required: No, If filename is specified, then magicdoc will use the provided filename to name the output config file.
          Default: magicdoc.yaml
  Options:
      type:
          Description: The type of project that magicdoc will parse and build documentation for. When using the terraform provider, `module` and `root` are the only valid options.
          Note: Magicdoc currently only supports module documentation generation. A root template is currently in development.
          Value: module, root
          Flag: --type, -t
          Environment Variable: MAGICDOC_TF_CREATE_CONFIG_TYPE
          Required: No
          Default: Module
```

<br>

```bash
MagicDoc Terraform Documentation Creator:
=========================================
  Config Output File:                                /Volumes/MacData/Work/Terraform/Modules/Documentation/TF-TestModule/magicdoc.yaml

MagicDoc Terraform Module Config Generator: [tf create config -t module <output_file>]:
Attempting to Gather Terraform Project Data...

Scanning project directory for defined module variables...

Generating Terraform Module Magicdoc Config: magicdoc.yaml

Magicdoc Terraform Module config file: magicdoc.yaml has been successfully created in :/Volumes/MacData/Work/Terraform/Modules/Documentation/TF-TestModule!
```

<br><br>

### `magicdoc tf create doc`

The `magicdoc tf create doc` command is the magic behind magicdoc. When this command is issued, magicdoc will run a data collection on all of the project outputs, variables, files, graph, git repository and release data, build the tree, and create the readme document. If a `README.md` file already exists in the target project directory then magicdoc will automatically backup this file, timestamp it, rename it as README_<date>_<timestamp>.bak and generate the new README file as `README.md` in the target project directory.

<br>

```yaml
magicdoc tf create doc <-t type>:
  Examples:
    magicdoc tf create doc
    magicdoc tf create doc --help
    magicdoc tf create doc -t module
    magicdoc tf -d /path/to/module/sourcecode create doc -t module
    magicdoc tf -d /path/to/module/sourcecode create doc -t module -a "0123456789109876543210"
  Arguments: None
  Options:
      type:
          Description: The type of project that magicdoc will parse and build documentation for. When using the terraform provider, `module` and `root` are the only valid options.
          Note: Magicdoc currently only supports module documentation generation. A root template is currently in development.
          Value: module, root
          Flag: --type, -t
          Environment Variable: MAGICDOC_TF_CREATE_CONFIG_TYPE
          Required: No
          Default: Module
      auth:
          Description: Passed a git repository personal access token to magicdoc, and is used to construct the appropriate header auth request when requesting data from the configured git repository.
          Value: token
          Flag: --auth, -a
          Environment Variable: MAGICDOC_TF_SHOW_REPO_AUTH
          Required: No
          Default: None
```

<br>

```bash
MagicDoc Terraform Documentation Creator:
=========================================
  Output File:                                       README.md

MagicDoc Terraform Module Doc Generator: [tf create doc -t module]:
Attempting to Gather Terraform Project Data...

MagicDoc git config file not found in /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
No git information about the target project can be provided at this time.
Scanning project directory for defined module variables...
Scanning project directory for defined module outputs...

MagicDoc Terraform Documentation Creator:
=========================================
  Output File:                                       README.md

MagicDoc Terraform Module Doc Generator: [tf create doc -t module]:
Attempting to Gather Terraform Project Data...

MagicDoc git config file not found in /Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module
No git information about the target project can be provided at this time.
Scanning project directory for defined module variables...
Scanning project directory for defined module outputs...

Generating Terraform Module Readme Documentation...
Magicdoc Terraform Module documentation file: README.md has been successfully created in :/Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Module!
```

<br><br>
