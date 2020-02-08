##############################################################################
# CloudMage : MagicDoc tf
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#  - tf subcommand set
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
import os, sys, json, ntpath

# MagicDoc Imports
from magicdoc.classes.terraform import TFMagicDoc
from magicdoc.commands.tf_commands import show as tf_show

# Set the Module Path for the Templates directory
CTX_TEMPLATE_DIR = COMMANDS = os.path.abspath(os.path.join(os.getcwd(), 'templates'))

# CLI Environment Class
class Environment(object):
    """Magic Doc Environment Class"""
    class Log():
            """CLI Log class to allow easy logging throughout the application"""

            def __init__(self, verbose, verbose_level):
                self.verbose = verbose
                self.verbose_level = verbose_level

            def clear(self):
                """Log method that will perform a screen clear when called"""
                click.clear()
            
            def write(self, msg, termcolor='green', fnl=False, enl=False):
                """Log method to print output to the shell"""
                # Set termcolor if message type was specified
                termcolor = "red" if termcolor.lower() == "error" else termcolor
                termcolor = "bright_red" if termcolor.lower() == "warning" else termcolor
                termcolor = "cyan" if termcolor.lower() == "info" else termcolor
                termcolor = "magenta" if termcolor.lower() == "debug" else termcolor
                if fnl:
                    click.echo()
                click.secho(msg, file=sys.stderr, fg=termcolor)
                if enl:
                    click.echo()

            def header(self, msg, fnl=True, enl=True):
                """Log method to print command title to the shell"""
                # Set termcolor if message type was specified
                msg_length = len(msg)
                if fnl:
                    click.echo()
                click.secho(msg, file=sys.stderr, fg='yellow')
                click.secho("{}".format("=" * msg_length), fg='yellow')
                if enl:
                    click.echo()

            def options(self, msg, option, fnl=False, enl=True):
                """Log method to print command options"""
                # Set termcolor if message type was specified
                if fnl:
                    click.echo()
                click.secho("{}:{}".format(msg, " " * 25), file=sys.stderr, fg='blue', nl=False)
                click.secho("{}".format(option), file=sys.stderr, fg='cyan')
                if enl:
                    click.echo()

            def debug(self, msg, fnl=False, enl=False):
                """Print a debug message to the shell"""
                offset = 3
                level = self.verbose_level.lower()
                visible = ['debug', 'info', 'warning', 'error']
                if self.verbose and any(level in str for level in visible):
                    click.secho("{}:{}{}".format("DEBUG", " " * offset, msg), file=sys.stderr, fg='magenta')

            def info(self, msg):
                """Print a info message to the shell"""
                offset = 4
                level = self.verbose_level.lower()
                visible = ['info', 'warning', 'error']
                if self.verbose and any(level in str for level in visible):
                    click.secho("{}:{}{}".format("INFO", " " * offset, msg), file=sys.stderr, fg='cyan')

            def warning(self, msg):
                """Print a warning message to the shell"""
                offset = 1
                level = self.verbose_level.lower()
                visible = ['warning', 'error']
                if self.verbose and any(level in str for level in visible):
                    click.secho("{}:{}{}".format("WARNING", " " * offset, msg), file=sys.stderr, fg='bright_red')

            def error(self, msg):
                """Print a error message to the shell"""
                offset = 3
                level = self.verbose_level.lower()
                visible = ['error']
                if self.verbose and any(level in str for level in visible):
                    click.secho("{}:{}{}".format("ERROR", " " * offset, msg), file=sys.stderr, fg='red')


    def __init__(self):
        self.verbose = False
        self.no_recursion = False
        self.workdir = os.getcwd()
        self.exclude_dir = None
        self.template_dir = None
        self.config_template = 'tf_config.j2'
        self.readme_template = 'tf_readme.j2'
        self.changelog_template = 'changelog.j2'
        self.gitignore_template = 'gitignore.j2'
        self.project_config = None
        self.tf = None
        self.terminal_colors = [
            'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'bright_black',
            'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
            'bright_cyan', 'bright_white'
        ]
        self.log = self.Log(self.verbose)


    # Environment method available to any command to format a map or object styled terraform variable into the proper format.
    def format_as_map(self, value, indent=0, offset=0):
        """Command Function that will print the desired output in a terraform map style format"""
        try:
            self.log.info("Environment object format_as_map call initiated...")
            self.log.info("Function: format_as_map called with provided value type: {}".format(type(value)))
            self.log.debug(json.dumps(value, indent=4, sort_keys=True))
            click.secho("{}{{".format(" " * indent), fg='cyan')
            self.log.debug("Attempting to parse object into proper map, dict, or object format")
            for k, v in value.items():
                self.log.debug("Attempting to format: {} = {}".format(k, v))
                click.secho("{}{}{} = ".format(" " * (indent + 4), k, " " * offset), fg='cyan', nl=False)
                click.secho("'{}'".format(v), fg='green')
            click.secho("{}}}".format(" " * indent), fg='cyan')
            self.log.debug("Passed value formatted successfully!")
        except Exception as e:
            self.log.warning("Attempt to format [map, object, dict] matched variable for shell display failed!. Defaulting to raw string format...")
            self.log.info(str(e))
            click.secho("{}".format(value), fg='green')


    # Environment method available to any command to format a list, set, or tuple styled terraform variable into the proper format.
    def format_as_list(self, value, indent=0, offset=0):
        """Command Function that will print the desired output in a terraform list style format"""
        try:
            self.log.info("Environment object format_as_list call initiated...")
            self.log.info("Function: format_as_list called with provided value type: {}".format(type(value)))
            self.log.debug("{}".format(value))
            click.secho("{}[".format(" " * indent), fg='cyan')
            self.log.debug("Attempting to parse object into proper list, set, or tuple format")
            for item in value:
                self.log.debug("Attempting to format: {}, identified as type: {}".format(item, type(item)))
                if isinstance(item, (list, set, tuple)):
                    self.log.debug("Item is of type: {}.. recursively calling this function on {}".format(type(item), item))
                    self.format_as_list(item, (indent + 4), 0)
                elif isinstance(item, dict):
                    self.log.debug("Item is of type: {}.. calling format_as_map function on {}".format(type(item), item))
                    self.format_as_map(item, (indent + 4), 0)
                elif isinstance(item, int):
                    self.log.debug("Item is of type: {}.. formatting item: {}".format(type(item), item))
                    click.secho("{}{}".format(" " * (indent + 4), item), fg='bright_red')
                else:
                    self.log.debug("Item is of type: {}.. no format modification necessary for: {}".format(type(item), item))
                    click.secho("{}'{}'".format(" " * (indent + 4), item), fg='green')
            click.secho("{}]".format(" " * indent), fg='cyan')
        except Exception as e:
            self.log.warning("Attempt to format [list, set, tuple] matched variable for shell display failed!. Defaulting to raw string format...")
            self.log.info(str(e))
            click.secho("{}".format(value), fg='green')


# Create Environment Class decorator to apply the Environment Class to each sub command
pass_environment = click.make_pass_decorator(Environment, ensure=True)

@click.group()
@click.option(
    '--verbose', '-v', is_flag=True, show_envvar=True,
    help='Enables verbose mode.'
)
@click.option(
    '--verbose_level', '-vl', show_envvar=True,
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    default='DEBUG'
    help='Enables verbose mode.'
)
@click.option(
    '--directory', '-d', show_envvar=True,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help='Changes the working directory where files will be read from and written to.'
)
@click.option(
    '--exclude_dir', '-e', show_envvar=True,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    default=None,
    help='Exclude a subdirectory from the search path.'
)
@click.option(
    '--config', '-c', show_envvar=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True),
    default=None,
    help='Specify the file path of the MagicDoc project config.'
)
@click.option(
    '--no_recursion', '-nr', is_flag=True, show_envvar=True,
    help='Disable recursion, This will exclude searching any sub-directory found in the workdir.'
)
@pass_environment
def cli(ctx, verbose: bool, verbose_level: str, directory: str, exclude_dir: str, config: str, no_recursion: bool):
    """Terraform based project commands and utilities"""
    this = "MagicDocCMD:tf"
    ctx.log.info("{}: Instantiating `magicdoc tf` environment...".format(this))
    
    # Set the default template directory.
    ctx.template_dir = CTX_TEMPLATE_DIR
    ctx.log.debug("{}: Setting environment template directory location: {}".format(this, CTX_TEMPLATE_DIR))

    # If user specified verbose settings set it, or pull from environment context.
    ctx.verbose = verbose
    ctx.log.verbose = verbose
    ctx.log.debug("{}: Setting environment verbose setting: {}".format(this, ctx.verbose))

    # If user specified workdir settings set it, or pull from environment context.
    if directory is not None:
        ctx.workdir = directory
    ctx.log.debug("{}: Setting environment working directory: {}".format(this, ctx.workdir))

    # If user specified a sub directory exclusion then pass it, otherwise the default is set to None.
    if exclude_dir is not None:
        ctx.exclude_dir = exclude_dir
    ctx.log.debug("{}: Setting environment excluded directory: {}".format(this, ctx.exclude_dir))

    # Allow the user to specify a custom path/filename to the MagicDoc config.
    if config is not None and config.endswith(('.yaml', '.yml')):
        ctx.project_config = config
    elif os.path.exists(os.path.join(ctx.workdir, 'magicdoc.yaml')):
        ctx.project_config = os.path.exists(ctx.workdir, 'magicdoc.yaml')

    # If user specified verbose settings set it, or pull from environment context.
    ctx.no_recursion = no_recursion

    # Create a Terraform project object.
    ctx.tf = TFMagicDoc(ctx.log, ctx.workdir, ctx.exclude_dir, ctx.project_config, ctx.no_recursion)
    pass


##############################
# TF Env CMD:
# CMD: magicdoc tf env
##############################
@cli.command()
@click.pass_context
def env(ctx):
    """Display Information about the tf subcommand environment."""
    
    # Assign context objects
    log = ctx.obj.log

    # Set Yes/No values if the project_config and tf dictionaries are populated/empty
    ctx_verbose = "On" if ctx.obj.verbose else "Off"
    ctx_no_recursion = "No" if ctx.obj.no_recursion else "Yes"
    ctx_project_config = "Yes" if bool(ctx.obj.project_config) else "No"
    ctx_tf = "Yes" if bool(ctx.obj.tf) else "No"

    if not ctx.obj.verbose:
        click.clear()
    log.header("MagicDoc TF Command Environment:")

    click.secho("Verbose Mode:              ", fg='blue', nl=False)
    click.secho(ctx_verbose, fg='green')
    
    click.secho("Search Subdirectories:     ", fg='blue', nl=False)
    click.secho(ctx_no_recursion, fg='green')
    
    click.secho("Working Directory:         ", fg='blue', nl=False)
    click.secho("[{}]".format(ctx.obj.workdir), fg='green')
    
    click.secho("Template Directory:        ", fg='blue', nl=False)
    click.secho("[{}]".format(ctx.obj.template_dir), fg='green')
    
    click.secho("Project Config Found:      ", fg='blue', nl=False)
    click.secho(ctx_project_config, fg='green')
    
    click.secho("Terraform Data Found:      ", fg='blue', nl=False)
    click.secho(ctx_tf, fg='green')
    click.echo()
    if ctx.obj.verbose:
        click.secho("Available Term Colors:      ", fg='blue')
        for item in ctx.obj.terminal_colors:
            click.secho("{}".format(item), fg=item)
        click.echo()


##############################
# TF Sub Command Imports:
# CMD: magicdoc tf show *
##############################
# Import Show Subcommands
cli.add_command(tf_show.show)