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
import os, sys, json, ntpath, inspect

# MagicDoc Imports
from magicdoc.classes.TFMagicDoc import TFMagicDoc
from magicdoc.commands.tf_commands import show as tf_show

# Set the Module Path for the Templates directory
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.realpath('__file__')))
LOG_CONTEXT = "CMD->tf"

# CLI Environment Class
class Environment(object):
    """Magic Doc Environment Class"""


    ''' Import Log class'''
    from magicdoc.classes.Log import Log


    '''Define class constructor and class methods:'''
    def __init__(self):
        self.verbose = False
        self.verbose_level = None
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
        # Create Log object to add to the context.
        self.log = self.Log(self.verbose, self.verbose_level)


    # Environment method available to any command to format a map or object styled terraform variable into the proper format.
    def format_as_map(self, arg_value, arg_indent=0, arg_offset=0):
        """Command Function that will print the desired output in a terraform map style format"""
        try:
            self.log.info("{}: Environment object format_as_map call initiated...".format(LOG_CONTEXT))
            self.log.info("{}: Function: format_as_map called with provided value type: {}".format(LOG_CONTEXT, type(arg_value)))
            self.log.debug("{}: \n{}".format(LOG_CONTEXT, json.dumps(arg_value, indent=4, sort_keys=True)))
            click.secho("{}{{".format(" " * arg_indent), fg='cyan')
            self.log.debug("{}: Attempting to parse object into proper map, dict, or object format".format(LOG_CONTEXT))
            for k, v in arg_value.items():
                self.log.debug("{}: Attempting to format: {} = {}".format(LOG_CONTEXT, k, v))
                click.secho("{}{}{} = ".format(" " * (arg_indent + 4), k, " " * arg_offset), fg='cyan', nl=False)
                click.secho("'{}'".format(v), fg='green')
            click.secho("{}}}".format(" " * arg_indent), fg='cyan')
            self.log.info("{}: Provided object formatted successfully!".format(LOG_CONTEXT))
        except Exception as e:
            self.log.warning("{}: Attempt to format [map, object, dict] matched variable for shell display failed!. Defaulting to raw string format...".format(LOG_CONTEXT))
            self.log.warning("{}: {}".format(LOG_CONTEXT, str(e)))
            click.secho("{}".format(arg_value), fg='green')


    # Environment method available to any command to format a list, set, or tuple styled terraform variable into the proper format.
    def format_as_list(self, arg_value, arg_indent=0, arg_offset=0):
        """Command Function that will print the desired output in a terraform list style format"""
        try:
            self.log.info("{}: Environment object format_as_list call initiated...".format(LOG_CONTEXT))
            self.log.info("{}: Function: format_as_list called with provided value type: {}".format(LOG_CONTEXT, type(arg_value)))
            self.log.debug("{}: \n{}".format(LOG_CONTEXT, arg_value))
            click.secho("{}[".format(" " * arg_indent), fg='cyan')
            self.log.debug("{}: Attempting to parse object into proper list, set, or tuple format".format(LOG_CONTEXT))
            for item in arg_value:
                self.log.debug("{}: Attempting to format: {}, identified as type: {}".format(LOG_CONTEXT, item, type(item)))
                if isinstance(item, (list, set, tuple)):
                    self.log.debug("{}: Item is of type: {}.. recursively calling this function on {}".format(LOG_CONTEXT, type(item), item))
                    self.format_as_list(item, (arg_indent + 4), 0)
                elif isinstance(item, dict):
                    self.log.debug("{}: Item is of type: {}.. calling format_as_map function on {}".format(LOG_CONTEXT, type(item), item))
                    self.format_as_map(item, (arg_indent + 4), 0)
                elif isinstance(item, int):
                    self.log.debug("{}: Item is of type: {}.. formatting item: {}".format(LOG_CONTEXT, type(item), item))
                    click.secho("{}{}".format(" " * (arg_indent + 4), item), fg='bright_red')
                else:
                    self.log.debug("{}: Item is of type: {}.. no format modification necessary for: {}".format(LOG_CONTEXT, type(item), item))
                    click.secho("{}'{}'".format(" " * (arg_indent + 4), item), fg='green')
            click.secho("{}]".format(" " * arg_indent), fg='cyan')
        except Exception as e:
            self.log.warning("{}: Attempt to format [list, set, tuple] matched variable for shell display failed!. Defaulting to raw string format...".format(LOG_CONTEXT))
            self.log.warning("{}: {}".format(LOG_CONTEXT, str(e)))
            click.secho("{}".format(arg_value), fg='green')


# Create Environment Class decorator to apply the Environment Class to each sub command
pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.option(
    '--verbose', '-v', is_flag=True, show_envvar=True,
    help='Enables verbose mode.'
)
@click.option(
    '--verbose_level', '-l', show_envvar=True,
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    default='DEBUG',
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
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)
    
    # Set Verbose and Verbose Level Settings. Note that the verbose_level log attribute is calling getter/setter methods.
    ctx.verbose = verbose
    log.verbose = verbose
    ctx.verbose_level = verbose_level.lower()
    log.verbose_level = verbose_level.lower()
    log.info("{}: Instantiating `magicdoc tf` environment...".format(log_msg))
    log.args("Environment: Verbose Attribute Set", ctx.verbose, arg_lower_nl=False)
    log.args("Log: Verbose Attribute Set", log.verbose, arg_lower_nl=False)
    log.args("Environment: Verbose Level Attribute Set", ctx.verbose_level, arg_lower_nl=False)
    log.args("Log: Verbose Level Attribute Set", log.verbose_level, arg_lower_nl=False)

    # ENVIRONMENT: Set the command group environment context by assigning the environment object values based on passed cmd args.
    # Template Directory
    ctx.template_dir = os.path.join(MODULE_PATH, 'templates')
    log.args("Environment: Template Path Set", ctx.template_dir, arg_lower_nl=False)

    # Set WorkDir, Target Project Directory.
    if directory is not None:
        ctx.workdir = directory
        log.args("Environment: Work Directory Set", ctx.workdir, arg_lower_nl=False)

    # Set Exclude Directory Path.
    if exclude_dir is not None:
        ctx.exclude_dir = exclude_dir
        log.args("Environment: Exclude Directory Set", ctx.exclude_dir, arg_lower_nl=False)

    # Set Project Config Path.
    if config is not None and config.endswith(('.yaml', '.yml')):
        ctx.project_config = config
        log.args("Environment: Project Config Set", ctx.project_config, arg_lower_nl=False)
    elif os.path.exists(os.path.join(ctx.workdir, 'magicdoc.yaml')):
        ctx.project_config = os.path.join(ctx.workdir, 'magicdoc.yaml')
        log.args("Environment: Project Config", ctx.project_config, arg_lower_nl=False)

    # Set Non-Recursion Flag.
    ctx.no_recursion = no_recursion
    log.args("Environment: Directory Recursion Set", ctx.no_recursion)

    # REQUIRED_OBJECTS: Instantiate a TFMagicDoc instance and assign the object to the context object.
    ctx.tf = TFMagicDoc(ctx.log, ctx.workdir, ctx.exclude_dir, ctx.project_config, ctx.no_recursion)
    log.info("{}: Environment: Terraform MagicDoc object instantiated successfully".format(log_msg))
    pass


##############################
# TF Env CMD:
# CMD: magicdoc tf env
##############################
@cli.command()
@click.pass_context
def env(ctx):
    """Display Information about the tf subcommand environment."""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, this, "MagicDoc: Terraform Environment Configuration")

    # LOCAL_ENV_VARIABLES: Define any local environments that the command function requires.
    env_verbose = "Enabled" if ctx.obj.verbose else "Disabled"
    log_verbose = "Enabled" if log.verbose else "Disabled"
    env_log = "Instantiated" if isinstance(log, object) else "Undefined"
    env_recursion = "Disabled" if ctx.obj.no_recursion else "Enabled"
    env_project_config = "Found" if ctx.obj.project_config is not None and os.path.exists(ctx.obj.project_config) else "Not Found"
    env_tf = "Instantiated" if isinstance(ctx.obj.tf, object) else "Undefined"
    env_tf_files = "Found" if bool(ctx.obj.tf.files) else "Not Found"
    env_config_template = "Found" if ctx.obj.template_dir is not None and os.path.exists(os.path.join(ctx.obj.template_dir, 'tf_config.j2')) else "Not Found"
    env_readme_template = "Found" if ctx.obj.template_dir is not None and os.path.exists(os.path.join(ctx.obj.template_dir, 'tf_readme.j2')) else "Not Found"
    env_changelog_template = "Found" if ctx.obj.template_dir is not None and os.path.exists(os.path.join(ctx.obj.template_dir, 'changelog.j2')) else "Not Found"
    env_gitignore_template = "Found" if ctx.obj.template_dir is not None and os.path.exists(os.path.join(ctx.obj.template_dir, 'gitignore.j2')) else "Not Found"

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf] Command Environment:", arg_lower_nl=False)
    log.write("Gathering Environment Context...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    click.secho("Console tf Command Settings:", fg='yellow')
    click.secho("============================", fg='yellow')
    click.secho("Verbose Mode:                    ", fg='blue', nl=False)
    click.secho(env_verbose, fg='green')

    click.secho("Verbose Level:                   ", fg='blue', nl=False)
    click.secho(ctx.obj.verbose_level, fg='green')

    click.secho("Log Verbose Mode:                ", fg='blue', nl=False)
    click.secho(log_verbose, fg='green')

    click.secho("Log Verbose Level:               ", fg='blue', nl=False)
    click.secho(log.verbose_level, fg='green')

    click.secho("Log Object State:                ", fg='blue', nl=False)
    click.secho(env_tf, fg='green')
    
    click.secho("Search Sub-Directories:          ", fg='blue', nl=False)
    click.secho(env_recursion, fg='green')

    click.secho("Working Directory:               ", fg='blue', nl=False)
    click.secho("{}".format(ctx.obj.workdir), fg='green')

    click.secho("Template Directory:              ", fg='blue', nl=False)
    click.secho("{}".format(ctx.obj.template_dir), fg='green')

    click.secho("Project Config Path:             ", fg='blue', nl=False)
    click.secho("{}".format(env_project_config), fg='green')
    
    click.secho("Project Config State:            ", fg='blue', nl=False)
    click.secho("{}".format(env_project_config), fg='green')

    click.secho("Terraform Object State:          ", fg='blue', nl=False)
    click.secho(env_tf, fg='green')
    
    click.secho("Terraform Data State:            ", fg='blue', nl=False)
    click.secho(env_tf_files, fg='green')
    click.echo()

    click.secho("Default Jinja Templates:", fg='yellow')
    click.secho("========================", fg='yellow')
    click.secho("Config Template:                 ", fg='blue', nl=False)
    click.secho(env_config_template, fg='green')
    click.secho("ReadMe Template:                 ", fg='blue', nl=False)
    click.secho(env_readme_template, fg='green')
    click.secho("Changelog Template:              ", fg='blue', nl=False)
    click.secho(env_changelog_template, fg='green')
    click.secho("GitIgnore Template:              ", fg='blue', nl=False)
    click.secho(env_gitignore_template, fg='green')
    click.echo()

    if ctx.obj.verbose:
        click.secho("Available Term Colors:", fg='yellow')
        click.secho("======================", fg='yellow')
        for item in ctx.obj.terminal_colors:
            if 'bright' in item:
                continue
            else:
                local_color_length = len(item)
                local_color_offset = 15 - local_color_length
                click.secho("{}{}".format(item, " " * local_color_offset), fg=item, nl=False)
                click.secho("bright_{}".format(item), fg="bright_{}".format(item))
        click.echo()

    click.secho("Console Log Color Scheme:", fg='yellow')
    click.secho("=========================", fg='yellow')
    click.secho("{}{}".format('DEBUG', ' ' * 8), fg='magenta', nl=False)
    log.debug("{}: -> Example DEBUG Message".format(log_msg))
    if not ctx.obj.verbose:
        click.echo()

    click.secho("{}{}".format('INFO', ' ' * 9), fg='cyan', nl=False)
    log.info("{}: -> Example INFO Message".format(log_msg))
    if not ctx.obj.verbose:
        click.echo()

    click.secho("{}{}".format('WARNING', ' ' * 6), fg='bright_red', nl=False)
    log.warning("{}: -> Example WARNING Message".format(log_msg))
    if not ctx.obj.verbose:
        click.echo()

    click.secho("{}{}".format('ERROR', ' ' * 8), fg='red', nl=False)
    log.error("{}: -> Example ERROR Message".format(log_msg))
    if not ctx.obj.verbose:
        click.echo()


##############################
# TF Sub Command Imports:
# CMD: magicdoc tf show *
##############################
# Import Show Subcommands
cli.add_command(tf_show.show)
