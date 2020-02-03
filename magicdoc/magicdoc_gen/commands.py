##############################################################################
# CloudMage : MagicDoc
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#
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

# Import Base Python Modules
from datetime import datetime
import logging

# Import MagicDoc classes
from libs import tfdoc

# Instantiate Logger
logging.basicConfig(filename='magicdoc.log', filemode='w', format='%(levelname)s:    %(message)s', level=logging.DEBUG)


##################
# MagicDoc Main: #
##################
@click.group()
@click.option(
    '--provider', '-p', show_envvar=True,
    type=click.Choice(['tf', 'terraform']),
    help="Specify the code provider that will be used. If the project is constructed in Terraform use terraform, or tf, if CloudFormation, use cloudformation or cf, etc..."
)
@click.option(
    '--src', '-s', show_envvar=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default="./",
    help="The directory location path to the target directory containing the project to be documented."
)
@click.pass_context
def main(ctx, provider: str, src: str):
    cprint("Using Provider: {}".format(provider), 'blue')
    cprint("Using Directory Path: {}".format(path), 'blue')



##############################
# MagicDoc Show SubCommands: #
##############################
# Create the CLI List command group
@click.group()
def show():
    pass

@show.command()
@click.option('--project_type', '-pt', default="terraform", help="Set the project type such as 'terraform'. Supported Project types: terraform")
@click.option('--path', '-p', default=".", help="The directory location path to the target project directory. Default: [./]")
@click.option('--subdir', '-s', default=True, help="Flag to signal the inclusion or exclusion of subdirectories. Default: True")
@click.pass_context
def files(project_type, path):
    click.echo(colored("Gathering {} file list from: {}".format(project_type, path), 'blue'))

    # Identify any selected options so that we can pass them to the class.
    command_options = {'project_type': project_type, 'path': path, 'subdir': subdir}

    if project_type.lower() == 'terraform':
        Files = tfdoc(path, subdir).FetchFileList()

    click.echo(Files)


cli = click.CommandCollection(sources=[main, show])

if __name__ == '__main__':
    main(auto_envvar_prefix="MAGICDOC", click.CommandCollection(sources=[show]))
