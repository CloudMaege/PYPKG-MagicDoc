# MagicDoc Project Repository Automatic Documentation Generation Utility Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<br>

## v0.1.1 - [2-19-2020]

### Added

- No new features added in this release

<br>

### Removed

- No removals in this release

<br>

### Changed

- Gitparser was set to warning for any failures as failures are not process ending. Commands can continue executing without git data.
- Template modified to properly display all required variables when generating examples
- Template modified to include better icons
- magicdoc tf create config argument was set to non requitable, by default if another filename is not specified, the config file will be named magicdoc.yaml.

<br><br>

## v0.1.0 - [2-17-2020]

Initial Development:

### Added

- Parse through a given Terraform Module, and Parse/Construct a list of all of the modules variables from parsing variables.tf
- Parse through a given Terraform Module, and Parse/Construct a tfvars file from parsing variables.tf
- Parse through a given Terraform Module, and Parse/Construct a list of all of the modules outputs from parsing outputs.tf
- Generate a Terraform Module Graph, and automatically include it in the generated readme document
- Automatically Generate a ToC for the generated readme document
- Generate a project config file that is used to generate a more detailed readme.md file.
- Automatically look for a .git/config file and if present parse the git repository URL from the config and send request to repo for latest release.
- Commands Added:
  - magicdoc tf show files - Shows a list of all terraform files within a project root
  - magicdoc tf show variables - Shows a list of all variables from the variables.tf file
  - magicdoc tf show outputs - shows a list of all outputs from the outputs.tf file
  - magicdoc tf show git - shows .git/config information if present in the target directory
  - magicdoc tf show repo - sends a call to github and returns some repository information
  - magicdoc tf show releases - sends a call to github releases and returns the most current release
  - magicdoc tf show tree - outputs an ascii console directory structure
  - magicdoc tf create config - Generates a config file for the project with a full list of all of the projects variables ready in the config
  - magicdoc tf create doc - Generates a readme.md file for the project.

### Changed

- None

### Removed

- None
