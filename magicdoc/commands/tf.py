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
                """Log method to print to output to the shell"""
                # Set termcolor if message type was specified
                termcolor = "red" if termcolor.lower() == "error" else termcolor
                termcolor = "orange" if termcolor.lower() == "warning" else termcolor
                termcolor = "blue" if termcolor.lower() == "info" else termcolor
                termcolor = "yellow" if termcolor.lower() == "debug" else termcolor
                click.echo()
                click.secho(msg, file=sys.stderr, fg=termcolor)
                click.echo()

            def debug(self, msg):
                """Print a debug message to the shell"""
                offset = 3
                if self.verbose:
                    click.secho("{}:{}{}".format("DEBUG", " " * offset, msg), file=sys.stderr, fg='yellow')

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
    '--no_recursion', '-nr', is_flag=True, show_envvar=True,
    help='Disable recursion, This will exclude searching any sub-directory found in the workdir.'
)
@pass_environment
def cli(ctx, verbose, directory, no_recursion):
    """Terraform based project commands and utilities"""
    # Set the default template directory.
    ctx.template_dir = CTX_TEMPLATE_DIR

    # If user specified verbose settings set it, or pull from environment context.
    ctx.verbose = verbose
    ctx.log.verbose = verbose

    # If user specified workdir settings set it, or pull from environment context.
    if directory is not None:
        ctx.workdir = directory

    # If user specified verbose settings set it, or pull from environment context.
    ctx.no_recursion = no_recursion

    # Create a Terraform project object.
    ctx.tf = TFMagicDoc(ctx.log, ctx.workdir, ctx.no_recursion)
    pass

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

    click.clear()
    log.write("MagicDoc TF Command Environment:")

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


@cli.command()
@click.pass_context
def files(ctx):
    """Print Terraform Project Variables"""
    try:
        # Assign context objects
        log = ctx.obj.log
        files = ctx.obj.tf.files

        click.clear()
        log.write("MagicDoc TF File Summary:")

        log.info("Invoking command magicdoc tf files.")
        log.debug("Working with returned file object:")
        log.debug(json.dumps(files, indent=4, sort_keys=True))
        log.debug(' ')
        click.secho("{} terraform file(s) found in target directory: {}".format(len(files.get('list_tf_files')), ctx.obj.workdir), fg='cyan')
        click.secho("{} tfvar file(s) found in target directory: {}".format(len(files.get('list_tfvar_files')), ctx.obj.workdir), fg='cyan')
        click.echo()

        # List TF Files:
        click.secho("Terraform .tf files:", fg='green')
        for filename in files.get('list_tf_files'):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("Using file path: {}".format(str(file_path)))
            log.debug("Using file name: {}".format(str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='blue', nl=False)
            click.secho(file_name, fg='white')
        log.debug("Listing .tf file results completed!")
        click.echo()

        # List TFVar Files:
        click.secho("Terraform .tfvar files:", fg='green')
        for filename in files.get('list_tfvar_files'):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("Using file path: {}".format(str(file_path)))
            log.debug("Using file name: {}".format(str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='blue', nl=False)
            click.secho(file_name, fg='white')
        log.debug("Listing .tf file results completed!")
        click.echo()
    except Exception as e:
        log.error("Failed to print terraform project files!")
        log.error("Exception: {}".format(str(e)))


# @cli.command()
# def update():
#     click.echo('update is invoked in command1.')


# @cli.command()
# @click.pass_environment
# def files(ctx):
#     """Command that will retrieve a list of files from a target directory location matching the provider type specified (terraform = .tf)"""
#     try:
#         click.echo("hello tf command")
#         # # Print command results.
#         # click.secho("{} terraform files found in target directory: {}".format(len(ctx.tf.get('files')), ctx.workdir), fg='green')
        
#         # for filename in ctx.tf.get('files'):
#         #     click.echo('Path: %s' % click.format_filename(b'filename'))
        
#         # # Print the results
#         # for item in ctx.tf.get('files'):
#         #     # For the command output remove the base path specified as its redundant
#         #     # Call SplitPath to find found results in subdirectories.
#         #     item_path_list = SplitPath(item)
#         #     # Print results
#         #     if not item_path_list[0]:
#         #         cprint(item_path_list[1], 'white')
#         #         log.debug(item_path_list[1])
#         #     else:
#         #         print(colored("/{} =>".format(item_path_list[0]), 'blue'), colored(item_path_list[1], 'white'))
#         #         log.debug("{} => {}".format(item_path_list[0], item_path_list[1]))
#         #     print("\n")
#     except Exception as e:
#         # cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
#         # cprint("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again", 'red')
#         # cprint(str(e), 'red')
#         # log.error("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again")
#         # log.error(str(e))
#         sys.exit()






# # @click.command('init', short_help='Initializes a repo.')
# # @click.argument('path', required=False, type=click.Path(resolve_path=True))
# # @pass_environment
# # def cli(ctx, path):
# #     """Initializes a repository."""
# #     if path is None:
# #         path = ctx.home
# #     ctx.log('Initialized the repository in %s',
# #             click.format_filename(path))


# # import click
# # from complex.cli import pass_environment


# # @click.command('status', short_help='Shows file changes.')
# # @pass_environment
# # def cli(ctx):
# #     """Shows file changes in the current working directory."""
#     ctx.log('Changed files: none')
#     ctx.vlog('bla bla bla, debug info')