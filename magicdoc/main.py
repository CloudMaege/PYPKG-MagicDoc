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

# Import Base Python Modules
import os, sys

# Set the Click Context for Environment Variable Name Generation
CONTEXT_SETTINGS = dict(auto_envvar_prefix='MAGICDOC')
# Set the location where the CLI should look for all of the subcommands and templates.
COMMANDS = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))

# Click Dynamic Command Loader Class
class MagicDocCLI(click.MultiCommand):
    """ Custom Command Loader Class"""

    def list_commands(self, ctx):
        """
        Look in the COMMANDS location and gather all command python files
        - Verify that any files in the CMD_FOLDER location end with .py
        - Append each found file to the command list excluding .py extention.
        """
        rv = []
        for filename in os.listdir(COMMANDS): 
            if filename.endswith('.py'):
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    rv.append(filename[:-3])
            # if filename.endswith('.py') and filename.startswith('cmd_'):
                # rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """
        Go through each of the py files in the command directory and import them to the cli.
        This model allows for each subcommand to be its own file keeping code organized, and modular.
        """
        try:
            ns = {}
            fn = os.path.join(COMMANDS, "{}.py".format(name))
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['cli']
            # imbue = __import__('magicdoc.commands.cmd_' + name, None, None, ['cli'])
            # return imbue.cli
        except ImportError:
            return
        
@click.command(cls=MagicDocCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def cli(ctx):
    """CloudMage: MagicDoc Project Documentation Utility"""
    pass

if __name__ == '__main__':
    cli()
