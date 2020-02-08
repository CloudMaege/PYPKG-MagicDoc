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

# Set the Module Path for the Templates directory
CTX_TEMPLATE_DIR = COMMANDS = os.path.abspath(os.path.join(os.getcwd(), 'templates'))

# CLI Environment Class
class Environment(object):
    """Magic Doc Environment Class"""
    class Log():
            """CLI Log class to allow easy logging throughout the application"""

            def __init__(self, verbose):
                self.verbose = verbose

            def clear(self):
                """Log method that will perform a screen clear when called"""
                click.clear()
            
            def write(self, msg, termcolor='green'):
                """Log method to print output to the shell"""
                # Set termcolor if message type was specified
                termcolor = "red" if termcolor.lower() == "error" else termcolor
                termcolor = "bright_red" if termcolor.lower() == "warning" else termcolor
                termcolor = "cyan" if termcolor.lower() == "info" else termcolor
                termcolor = "magenta" if termcolor.lower() == "debug" else termcolor
                click.echo()
                click.secho(msg, file=sys.stderr, fg=termcolor)

            def header(self, msg):
                """Log method to print command title to the shell"""
                # Set termcolor if message type was specified
                msg_length = len(msg)
                click.echo()
                click.secho(msg, file=sys.stderr, fg='yellow')
                click.secho("{}".format("=" * msg_length), fg='yellow')
                click.echo()

            def debug(self, msg):
                """Print a debug message to the shell"""
                offset = 3
                if self.verbose:
                    click.secho("{}:{}{}".format("DEBUG", " " * offset, msg), file=sys.stderr, fg='magenta')

            def info(self, msg):
                """Print a info message to the shell"""
                offset = 4
                if self.verbose:
                    click.secho("{}:{}{}".format("INFO", " " * offset, msg), file=sys.stderr, fg='cyan')

            def warning(self, msg):
                """Print a warning message to the shell"""
                offset = 1
                if self.verbose:
                    click.secho("{}:{}{}".format("WARNING", " " * offset, msg), file=sys.stderr, fg='bright_red')

            def error(self, msg):
                """Print a error message to the shell"""
                offset = 3
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
        self.project_config = {}
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
    '--no_recursion', '-nr', is_flag=True, show_envvar=True,
    help='Disable recursion, This will exclude searching any sub-directory found in the workdir.'
)
@pass_environment
def cli(ctx, verbose, directory, exclude_dir, no_recursion):
    """Terraform based project commands and utilities"""
    # Set the default template directory.
    ctx.template_dir = CTX_TEMPLATE_DIR

    # If user specified verbose settings set it, or pull from environment context.
    ctx.verbose = verbose
    ctx.log.verbose = verbose

    # If user specified workdir settings set it, or pull from environment context.
    if directory is not None:
        ctx.workdir = directory

    # If user specified a sub directory exclusion then pass it, otherwise the default is set to None.
    if exclude_dir is not None:
        ctx.exclude_dir = exclude_dir

    # If user specified verbose settings set it, or pull from environment context.
    ctx.no_recursion = no_recursion

    # Create a Terraform project object.
    ctx.tf = TFMagicDoc(ctx.log, ctx.workdir, ctx.exclude_dir, ctx.no_recursion)
    pass

# Command: tf env
@cli.command()
@click.pass_context
def env(ctx):
    """Print Information about the tf subcommand environment"""
    
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


# Command: tf files
@cli.command()
@click.pass_context
def files(ctx):
    """Print Terraform Project Files"""
    try:
        # Assign context objects
        log = ctx.obj.log
        files = ctx.obj.tf.files

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF File Summary:")

        log.info("Invoking command magicdoc tf files.")
        log.info("Working with returned file object:")
        log.debug(json.dumps(files, indent=4, sort_keys=True))
        log.debug(' ')
        
        click.secho("Terraform file search target directory location: {}".format(ctx.obj.workdir), fg='blue')
        click.secho("  - {} terraform file(s) found in target directory.".format(len(files.get('list_tf_files', []))), fg='bright_blue')
        click.secho("  - {} tfvar file(s) found in target directory.".format(len(files.get('list_tfvar_files', []))), fg='bright_blue')
        click.echo()

        # List TF Files:
        click.secho("Terraform .tf files:", fg='green')
        click.secho("====================", fg='green')
        for filename in files.get('list_tf_files', []):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("Using file path: {}".format(str(file_path)))
            log.debug("Using file name: {}".format(str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='bright_red', nl=False)
            click.secho(file_name, fg='cyan')
        log.debug("Listing .tf file results completed!")
        click.echo()

        # List TFVar Files:
        click.secho("Terraform .tfvar files:", fg='green')
        click.secho("=======================", fg='green')
        for filename in files.get('list_tfvar_files', []):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("Using file path: {}".format(str(file_path)))
            log.debug("Using file name: {}".format(str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='bright_red', nl=False)
            click.secho(file_name, fg='cyan')
        log.debug("Listing .tf file results completed!")
        click.echo()
    except Exception as e:
        log.error("MagicDoc failed to parse the terraform project files output! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
        click.echo()
        sys.exit()


# Command: tf variables
@click.option(
    '--include_examples', '-i', is_flag=False, show_envvar=True,
    help='Include all subdirectories including example(s)'
)
@cli.command()
@click.pass_context
def variables(ctx, include_examples: bool):
    """Print Terraform Project Variables"""
    try:
        # Assign context objects
        log = ctx.obj.log
        
        # Trigger the property setter to populate the variables object, then assign it for usage.
        ctx.obj.tf.variables = include_examples
        variables = ctx.obj.tf.variables

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF Variable Summary:")

        log.info("Invoking command magicdoc tf variables.")
        log.info("Working with returned file object:")
        log.debug(json.dumps(variables, indent=4, sort_keys=True))
        log.debug(' ')
        click.secho("{} required terraform project variables found in target directory: {}".format(len(variables.get('required_vars', [])), ctx.obj.workdir), fg='bright_black')
        click.secho("{} optional terraform project variables found in target directory: {}".format(len(variables.get('optional_vars', [])), ctx.obj.workdir), fg='bright_black')
        click.echo()

        # List TF Required Variables:
        click.secho("Terraform Project Required Variables:", fg='yellow')
        click.secho("=====================================", fg='yellow')
        for var in variables.get('required_vars', []):
            offset = variables.get('required_vars_maxlength', 0) - len(var.get('name', ""))
            log.debug("Setting required variable offset to: {}".format(offset))
            log.debug("Printing defined required variable: {}!".format(var.get('name', "")))
            # Check variable type and fix formatting
            log.debug("Checking variable type")
            click.secho("{}{} = ".format(var.get('name', ""), " " * offset), fg='blue', nl=False)
            # Print example value in list, set, or tuple format:
            if var.get('type', 'string').startswith(('list', 'set', 'tuple')):
                log.debug("Variable type set to list, set, or tuple... adjusting example format")
                ctx.obj.format_as_list(['Required_Value_1', 'Required_Value_2'])
            # Print example value in map or object format:
            elif var.get('type', 'string').startswith(('map', 'object')):
                log.debug("Variable type set to map, or object... adjusting example format")
                ctx.obj.format_as_map({'Required_Variable_1': 'Required_Value_1', 'Required_Variable_2': 'Required_Value_2'})
            # Print example value in number format:
            elif var.get('type', 'string').startswith('number'):
                log.debug("Variable type set to number... adjusting example format")
                click.secho(100, fg='bright_red')
            # Just print in normal string format.
            else:
                log.debug("Variable type is set to string or undefined.. printing in raw string value format")
                click.secho("'Required Value'", fg='green')
        log.debug("Listing required variable results completed!")
        click.echo()

        # List TF Optional Variables:
        click.secho("Terraform Project Optional Variables:", fg='yellow')
        click.secho("=====================================", fg='yellow')
        for var in variables.get('optional_vars', []):
            offset = variables.get('optional_vars_maxlength', 0) - len(var.get('name', ""))
            log.debug("Setting optional variable offset to: {}".format(offset))
            log.debug("Printing defined optional variable: {}!".format(var.get('name', "")))
            log.debug("Checking variable type and adjusting display format")
            click.secho("{}{} = ".format(var.get('name', ""), " " * offset), fg='blue', nl=False)
            # Print example value in list, set, or tuple format:
            if var.get('type', 'string').startswith(('list', 'set', 'tuple')):
                log.debug("Variable type set to list, set, or tuple... adjusting example format")
                ctx.obj.format_as_list(var.get('default', ['Example_Value_1', 'Example_Value_2']))
            # Print example value in map or object format:
            elif var.get('type', 'string').startswith(('map', 'object')):
                log.debug("Variable type set to map, or object... adjusting example format")
                ctx.obj.format_as_map(var.get('default', {'Example_Key_1': 'Example_Value_1', 'Example_Key_2': 'Example_Value_2'}))
            # Print example value in number format:
            elif var.get('type', 'string').startswith('number'):
                log.debug("Variable type set to number... adjusting example format")
                click.secho("{}".format(var.get('default', 100)), fg='bright_red')
            # Just print in normal string format.
            else:
                log.debug("Variable type is set to string or undefined.. printing in raw string value format")
                click.secho("'{}'".format(var.get('default', 'Example_Value')), fg='green')
        log.debug("Listing optional variable results completed!")
        click.echo()
    except Exception as e:
        log.error("MagicDoc failed to parse the terraform project variables output! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
        click.echo()
        sys.exit()
