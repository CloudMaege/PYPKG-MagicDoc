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
###############################################
# Add Show subcommands to Show Command Group: #
###############################################
gen.add_command(dirtree)
gen.add_command(config)
