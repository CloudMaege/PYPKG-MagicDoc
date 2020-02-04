##############################################################################
# CloudMage : MagicDoc Gen Commands
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#  - Gen Subcommand List
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:
###############
# Import Pip Installed Modules:
import click
from termcolor import colored, cprint

# Import MagicDoc classes
from libs.utils import SetPath, DirTree
from libs.config import Config
from libs.jinja import Jinja
from libs.tfdoc import TFDoc
from libs.github import Github

# Import Base Python Modules
from pathlib import Path
import logging, sys, json, os

# Instantiate Logger
log = logging.getLogger('magicdoc.gen.commands')


##############################
# MagicDoc Show Subcommands: #
##############################
@click.group()
@click.pass_context
def gen(ctx):
    cprint("Using Provider: {}".format(ctx.obj.get('provider')), 'blue')
    log.debug("Gen command called using provided context: {}".format(ctx.obj))
    pass


##############################
# MagicDoc Gen DirTree:      #
##############################
@gen.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Pass context
@click.pass_context

# File subcommand call.
def dirtree(ctx, directory: str):
    """Command that will create an ascii directory tree listing that can be used within the generated documentation."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)
        
        log.debug("Attempting to build directory tree variable...")
        # Set a variable for the Directory tree, and then call the Directory Tree Generator
        FileTree = DirTree(path)

        # Add the Dir Tree Variable to the Template Dictionary:
        print(FileTree)
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to build directory structure tree", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to build directory structure tree")
        log.error(str(e))
        sys.exit()


################################
# MagicDoc Gen Project Config: #
################################
@gen.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Set the path location of the directory that contains the jinja template that will be created.
@click.option(
    '--template_dir', '-td', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the directory path location of the directory that contains the desired config jinja template. Default settting will use the packaged template."
)

# Set the desired jinja template name to load.
@click.option(
    '--template', '-t', show_envvar=True,
    type=click.STRING,
    default="magicdoc_config.j2",
    help="Specify the jinja template file that will be used to generate the project config. Default value is the packaged magicdoc config template."
)

# Set the output file name.
@click.option(
    '--filename', '-f', show_envvar=True,
    type=click.STRING,
    default="README.yaml",
    help="Specify the name that will be used for the config file output. Default is README.yaml."
)

# Set the default value for Overwrite
@click.option(
    '--overwrite', '-ow', show_envvar=True,
    type=click.BOOL,
    default=False,
    help="Flag to allow over writing the current configuration file if one already exists in the provided config output path."
)

# Pass context
@click.pass_context

# File subcommand call.
def config(ctx, directory: str, template_dir: str, template: str, filename: str, overwrite: bool):
    """Command that will create a project config file that can be used to supply additional information for the documentation generation process."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)
        
        # Gather the project variables to construct the object that the template will use to generate the config file.
        # Set the type of provider class to call
        if ctx.obj.get('provider').lower() == 'terraform' or ctx.obj.get('provider') == 'tf':
            Variables = TFDoc(path).BuildVarList()
            log.debug("Variable list retrieved from provided file path...")
        
        # Load, render and write the Jinja Template
        log.debug("Attempting to build project config file...")
        ConfigFile = Jinja(TemplateDir=template_dir, Template=template, OutputDir=path, OutputFile=filename)
        ConfigFile.LoadTemplate()
        ConfigFile.RenderTemplate(Variables)
        ConfigFile.WriteTemplate(Overwrite=overwrite)
        # Add the Dir Tree Variable to the Template Dictionary:
        cprint("Config file successfully written to: {}".format(os.path.join(path, filename)))
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to complete config file creation", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to complete config file creation")
        log.error(str(e))
        raise
        sys.exit()


################################
# MagicDoc Gen Project Config: #
################################
@gen.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Set the path location of the directory that contains the jinja template that will be created.
@click.option(
    '--template_dir', '-td', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the directory path location of the directory that contains the desired config jinja template. Default settting will use the packaged template."
)

# Set the desired jinja template name to load.
@click.option(
    '--template', '-t', show_envvar=True,
    type=click.STRING,
    default="tf_module_readme.j2",
    help="Specify the jinja template file that will be used to generate the project config. Default value is the packaged tf_module_readme.j2 readme markdown template."
)

# Set the config file name.
@click.option(
    '--configfile', '-c', show_envvar=True,
    type=click.STRING,
    default="README.yaml",
    help="Specify the name of the repository config file. Default is README.yaml"
)

# Set the output file name.
@click.option(
    '--filename', '-f', show_envvar=True,
    type=click.STRING,
    default="README.md",
    help="Specify the name of the output file that will be written. This defaults to README.md"
)

# Set the default value for Overwrite
@click.option(
    '--overwrite', '-ow', show_envvar=True,
    type=click.BOOL,
    default=False,
    help="Flag to allow over writing the current configuration file if one already exists in the provided config output path."
)

# Set the default value for Overwrite
@click.option(
    '--backup', '-b', show_envvar=True,
    type=click.BOOL,
    default=True,
    help="Flag to allow backup an existing readme.md file if one exists in the repository that magicdoc was called against."
)

# Provide an access token to make the repository request.
@click.option(
    '--token', '-tk', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the git provider access token that will be used to authenticate the repository and release requests."
)

# Set repository namespace
@click.option(
    '--namespace', '-n', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the repository namespace under which the target repository exists."
)

# Set repository name
@click.option(
    '--repo', '-r', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the name of the repository being searched for."
)

# Pass context
@click.pass_context

# File subcommand call.
def readme(ctx, directory: str, template_dir: str, template: str, filename: str, configfile: str, overwrite: bool, backup: bool, namespace: str, repo: str, token: str):
    """Command that will create a project readme.md for a repository ."""
    try:
        # Define the dictionary object that will be passed to the readme template.
        ReadmeObj = {}
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)

        # Call the config parser to parse a config file if one exists within the target directory.
        ReadmeConfig = Config(path, configfile)
        # print(json.dumps(ReadmeConfig.config, indent=4, sort_keys=True))
        ReadmeObj.update(git=ReadmeConfig.config.get('GitConfig', {}))
        ReadmeObj.update(readme=ReadmeConfig.config.get('ReadMeConfig', {}))
        
        # Gather the project variables to construct the object that the template will use to generate the readme document.
        # Set the type of provider class to call
        if ctx.obj.get('provider').lower() == 'terraform' or ctx.obj.get('provider') == 'tf':
            Variables = TFDoc(path).BuildVarList()
            log.debug("Variable list retrieved from provided file path...")
            ReadmeObj.update(variables=Variables)
            # Add the required and optional images
            ReadMeObjVar = ReadmeObj.get('variables')
            ReadMeObjVar.update(required_image=ReadmeConfig.config.get('VariablesConfig').get('Required').get('Image'))
            ReadMeObjVar.update(optional_image=ReadmeConfig.config.get('VariablesConfig').get('Optional').get('Image'))
            
            # Gather the project outputs to use to construct the object that the template will use to generate the readme document.
            Outputs = TFDoc(path).BuildOutputList()
            log.debug("Output list retrieved from provided file path...")
            ReadmeObj.update(outputs=Outputs)

            # Graph the things
            GraphImage = TFDoc(path).BuildGraph()
            if GraphImage != "None":
                ReadmeObj.update(tfdiagram=GraphImage)

        # Update the variable objects with the data from the config pull
        ReadmeConfig.UpdateVars(ReadmeObj)
        log.info("ReadmeObj has been updated with variable data from the parsed config.")
        # print(json.dumps(ReadmeObj, indent=4, sort_keys=True))

        # Add the Build Tree
        BuildTree = DirTree(path)
        log.debug("Dirtree created:\n{}".format(BuildTree))
        ReadmeObj.update(tree=BuildTree)
        
        # Last attempt to fetch GitRepo Data and add it to the ReadMeObj before we generate the documentation.
        # If the namespace and repository were provided, then assign the values, if not check for .git/config file and parse.
        # Set variables to hold the Namespace and Repo
        GitNameSpace = None
        GitRepo = None  
        
        # Try and use the variables first
        if repo is not None and namespace is not None:
            GitNameSpace = namespace
            GitRepo = repo
            log.debug("Configuring Git NameSpace and Repo from command variables...")
            log.debug("GitNameSpace set to value: {}".format(namespace))
            log.debug("GitRepo set to value: {}".format(repo))
        # Try and fetch the repository URL from the configured directory.
        elif isinstance(ReadmeObj.get('git'), dict):
            GitNameSpace = ReadmeObj.get('git').get('NameSpace')
            GitRepo = ReadmeObj.get('git').get('Name')
            log.debug("Configuring Git NameSpace and Repo from the project config file...")
            log.debug("GitNameSpace set to value: {}".format(ReadmeObj.get('git').get('NameSpace')))
            log.debug("GitRepo set to value: {}".format(ReadmeObj.get('git').get('Name')))
        elif os.path.exists("{}/.git/config".format(path)):
            GitNameSpace, GitRepo = ParseRepoUrl(path)
            log.debug("Configuring Git NameSpace and Repo from the project .git/config file...")
            log.debug("GitNameSpace set to value: {}".format(GitNameSpace))
            log.debug("GitRepo set to value: {}".format(GitRepo))
        # Attempt to make the call to the repository to fetch repo and release data.
        log.debug("Attempting to make request from Github...")
        if GitNameSpace is not None and GitRepo is not None:
            RequestObj = Github(GitNameSpace, GitRepo, token).GetGitHubData()
            log.debug("Git Repository Request State: {}".format(RequestObj))
            if RequestObj.get('state') != "fail":
                ReadmeObj.update(repo=RequestObj)
                log.debug("Template Object has been updated to include the repository response object.")
        log.info("Generation of template dictionary object completed: {}".format(json.dumps(ReadmeObj, indent=4, sort_keys=True)))
        # Load, render and write the Jinja Template
        log.debug("Attempting to build project config file...")
        DocTemplate = Jinja(TemplateDir=template_dir, Template=template, OutputDir=path, OutputFile=filename)
        DocTemplate.LoadTemplate()
        DocTemplate.RenderTemplate(ReadmeObj)
        DocTemplate.WriteTemplate(Overwrite=overwrite, Backup=backup)
        # Add the Dir Tree Variable to the Template Dictionary:
        cprint("Template file successfully written to: {}".format(os.path.join(path, filename)))
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to complete config file creation", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to complete config file creation")
        log.error(str(e))
        raise
        sys.exit()


###############################################
# Add Show subcommands to Show Command Group: #
###############################################
gen.add_command(dirtree)
gen.add_command(config)
gen.add_command(readme)
