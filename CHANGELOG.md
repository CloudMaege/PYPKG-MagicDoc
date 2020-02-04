# MagicDoc Project Repository Automatic Documentation Generation Utility Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.0.0 - [2-1-2020]

Initial Development:

### Added

- Parse through a given Terraform Module, and Parse/Construct a list of all of the modules variables from parsing variables.tf
- Parse through a given Terraform Module, and Parse/Construct a tfvars file from parsing variables.tf
- Parse through a given Terraform Module, and Parse/Construct a list of all of the modules outputs from parsing outputs.tf
- Generate a Terraform Module Graph, and automatically include it in the generated readme document
- Automatically Generate a ToC for the generated readme document
- Generate a project config file that is used to generate a more detailed readme.md file.
- Commands Added:
  - magicdoc show files - Shows a list of all terraform files within a project root
  - magicdoc show variables - Shows a list of all variables from the variables.tf file
  - magicdoc show outputs - shows a list of all outputs from the outputs.tf file
  - magicdoc show repo - sends a call to github and returns some repository information
  - magicdoc show releases - sends a call to github releases and returns the most current release
  - magicdoc gen config - Generates a config file for the project with a full list of all of the projects variables ready in the config
  - magicdoc gen readme - Generates a readme.md file for the project.

### Changed

- None

### Removed

- None
