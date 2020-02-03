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
import logging, os

# Import MagicDoc sub commands
from magicdoc_show import commands as show_commands
# from magicdoc_gen import commands as gen

# Instantiate Logger
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/magicdoc.log', filemode='w', format='%(asctime)-15s-%(levelname)s:    %(message)s', level=logging.DEBUG)
log = logging.getLogger('magicdoc')


##################
# MagicDoc Main: #
##################
@click.group()
# Pass provider:
@click.option(
    '--provider', '-p', show_envvar=True,
    type=click.Choice(['tf', 'terraform']),
    help="Specify the code provider that will be used. If the project is constructed in Terraform use terraform, or tf, if CloudFormation, use cloudformation or cf, etc..."
)

# Pass directory path to search for all commands:
@click.option(
    '--directory', '-d', show_envvar=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    help="The directory path location to the target directory containing the project files that the command will be ran against. This setting is optional allowing the directory be set via an associated environment variable."
)

# Pass object context
@click.pass_context

# Entry Point Function:
def main(ctx, provider: str, directory: str):
    ctx.obj.update(provider=provider, directory=directory)


# Add Subcommand groups to main command entry point.
main.add_command(show_commands.show)


if __name__ == '__main__':
    main(auto_envvar_prefix="MAGICDOC", obj={})
