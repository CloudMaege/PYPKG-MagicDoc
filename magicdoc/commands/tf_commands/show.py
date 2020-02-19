##############################################################################
# CloudMage : MagicDoc tf show
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#  - magicdoc tf [show] subcommand set
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

# Import MagicDoc Classes/Modules
from magicdoc.modules.tree import DirTree
from magicdoc.classes.GitParser import GitParser

# Define Global Variables
LOG_CONTEXT = "CMD->tf_show"


##############################
# Define TF Show Group
# CMD: magicdoc tf show *
##############################
# Instantiate the tf subcommand groups:
@click.group()
@click.pass_context
def show(ctx):
    """Display information about the terraform target project."""
    pass


##############################
# TF Files CMD:
# CMD: magicdoc tf show files
##############################
@show.command()
@click.pass_context
def files(ctx):
    """Display the terraform target project file lists."""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # LOCAL_ENV_VARIABLES: Define any local environments that the command function requires.
    files = ctx.obj.tf.files

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project File Summary:")

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Gathering Terraform Project Files...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        click.secho("Terraform file search target directory location: {}".format(ctx.obj.workdir), fg='blue')
        click.secho("  -> {} terraform file(s) found in target directory.".format(len(files.get('list_tf_files', []))), fg='bright_blue')
        click.secho("  -> {} tfvar file(s) found in target directory.".format(len(files.get('list_tfvar_files', []))), fg='bright_blue')
        click.echo()

        # List TF Files:
        click.secho("Terraform .tf files:", fg='yellow')
        click.secho("====================", fg='yellow')
        for filename in files.get('list_tf_files', []):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("{}: Using file path: {}".format(log_msg, str(file_path)))
            log.debug("{}: Using file name: {}".format(log_msg, str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='bright_red', nl=False)
            click.secho(file_name, fg='cyan')
        log.debug("{}: Listing .tf file results completed!".format(log_msg))
        click.echo()

        # List TFVar Files:
        click.secho("Terraform .tfvar files:", fg='yellow')
        click.secho("=======================", fg='yellow')
        for filename in files.get('list_tfvar_files', []):
            file_path, file_name = ntpath.split(filename)
            file_path = file_path.replace("/", "")
            log.debug("{}: Using file path: {}".format(log_msg, str(file_path)))
            log.debug("{}: Using file name: {}".format(log_msg, str(file_name)))
            if file_path != "":
                click.secho("{}/".format(file_path), fg='bright_red', nl=False)
            click.secho(file_name, fg='cyan')
        log.debug("{}: Listing .tfvar file results completed!".format(log_msg))
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to parse the terraform project files object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.", 'error', arg_upper_nl=True, arg_lower_nl=True)
        log.error("{}: MagicDoc failed to parse the terraform project files object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg))
        log.error("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()

##################################
# TF Variables CMD:
# CMD: magicdoc tf show variables
##################################
@show.command()
@click.option(
    '--include_examples', '-i', show_envvar=True,
    type=click.BOOL,
    default=False,
    help='Include all subdirectories including example(s)'
)
@click.pass_context
def variables(ctx, include_examples: bool):
    """Display Terraform Project Variables."""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Variable Summary:", arg_args={'Include Example Directories': str(include_examples)})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Gathering Terraform Project Files...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        # LOCAL_ENV_VARIABLES: Define any local environments that the command function requires.
        # Trigger the property setter to populate the variables object, then assign it for usage.
        click.secho("Parsing variables.tf files for Terraform variables...", fg='green')
        ctx.obj.tf.variables = include_examples
        variables = ctx.obj.tf.variables

        click.secho("Terraform variable search target directory location: {}".format(ctx.obj.workdir), fg='blue')
        click.secho(" -> {} required terraform project variables found in target project: {}".format(len(variables.get('required_vars', [])), ctx.obj.workdir), fg='bright_black')
        click.secho(" -> {} optional terraform project variables found in target project: {}".format(len(variables.get('optional_vars', [])), ctx.obj.workdir), fg='bright_black')
        click.echo()

        # List TF Required Variables:
        click.secho("Terraform Project Required Variables:", fg='yellow')
        click.secho("=====================================", fg='yellow')
        for var in variables.get('required_vars', []):
            offset = variables.get('required_vars_maxlength', 0) - len(var.get('name', ""))
            log.debug("{}: Setting required variable offset to: {}".format(log_msg, offset))
            log.debug("{}: Printing defined required variable: {}!".format(log_msg, var.get('name', "")))
            # Check variable type and fix formatting
            log.debug("{}: Checking variable type and adjusting display format".format(log_msg))
            click.secho("{}{} = ".format(var.get('name', ""), " " * offset), fg='blue', nl=False)
            # Print example value in list, set, or tuple format:
            if var.get('type', 'string').startswith(('list', 'set', 'tuple')):
                log.debug("{}: Variable type set to list, set, or tuple... adjusting example format".format(log_msg))
                ctx.obj.format_as_list(['Required_Value_1', 'Required_Value_2'])
            # Print example value in map or object format:
            elif var.get('type', 'string').startswith(('map', 'object')):
                log.debug("{}: Variable type set to map, or object... adjusting example format".format(log_msg))
                ctx.obj.format_as_map({'Required_Variable_1': 'Required_Value_1', 'Required_Variable_2': 'Required_Value_2'})
            # Print example value in number format:
            elif var.get('type', 'string').startswith('number'):
                log.debug("{}: Variable type set to number... adjusting example format".format(log_msg))
                click.secho(100, fg='bright_red')
            # Just print in normal string format.
            else:
                log.debug("{}: Variable type is set to string or undefined.. printing in raw string value format".format(log_msg))
                click.secho("'Required Value'", fg='green')
        log.debug("{}: Listing required variable results completed!".format(log_msg))
        click.echo()

        # List TF Optional Variables:
        click.secho("Terraform Project Optional Variables:", fg='yellow')
        click.secho("=====================================", fg='yellow')
        for var in variables.get('optional_vars', []):
            offset = variables.get('optional_vars_maxlength', 0) - len(var.get('name', ""))
            log.debug("{}: Setting optional variable offset to: {}".format(log_msg, offset))
            log.debug("{}: Printing defined optional variable: {}!".format(log_msg, var.get('name', "")))
            log.debug("{}: Checking variable type and adjusting display format".format(log_msg))
            click.secho("{}{} = ".format(var.get('name', ""), " " * offset), fg='blue', nl=False)
            # Print example value in list, set, or tuple format:
            if var.get('type', 'string').startswith(('list', 'set', 'tuple')):
                log.debug("{}: Variable type set to list, set, or tuple... adjusting example format".format(log_msg))
                ctx.obj.format_as_list(var.get('default', ['Example_Value_1', 'Example_Value_2']))
            # Print example value in map or object format:
            elif var.get('type', 'string').startswith(('map', 'object')):
                log.debug("{}: Variable type set to map, or object... adjusting example format".format(log_msg))
                ctx.obj.format_as_map(var.get('default', {'Example_Key_1': 'Example_Value_1', 'Example_Key_2': 'Example_Value_2'}))
            # Print example value in number format:
            elif var.get('type', 'string').startswith('number'):
                log.debug("{}: Variable type set to number... adjusting example format".format(log_msg))
                click.secho("{}".format(var.get('default', 100)), fg='bright_red')
            # Just print in normal string format.
            else:
                log.debug("{}: Variable type is set to string or undefined.. printing in raw string value format".format(log_msg))
                click.secho("'{}'".format(var.get('default', 'Example_Value')), fg='green')
        log.debug("{}: Listing optional variable results completed!".format(log_msg))
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to parse the terraform project variables object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg), 'error', arg_lower_nl=True, arg_upper_nl=True)
        log.error("{}: MagicDoc failed to parse the terraform project variables object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg))
        log.error("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()


###############################
# TF Outputs CMD:
# CMD: magicdoc tf show outputs
################################
@show.command()
@click.option(
    '--include_examples', '-i', show_envvar=True,
    type=click.BOOL,
    default=False,
    help='Include all subdirectories including example(s)'
)
@click.pass_context
def outputs(ctx, include_examples):
    """Display Terraform Project Outputs"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Outputs Summary:", arg_args={'Include Example Directories': str(include_examples)})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Gathering Terraform Project Variables...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        # LOCAL_ENV_VARIABLES: Define any local environments that the command function requires.
        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Parsing outputs.tf files for Terraform outputs...", fg='green')
        ctx.obj.tf.outputs = include_examples
        outputs = ctx.obj.tf.outputs

        click.secho("Terraform output search target directory location: {}".format(ctx.obj.workdir), fg='blue')
        click.secho(" -> {} terraform project outputs found in target project: {}".format(len(outputs), ctx.obj.workdir), fg='bright_black')
        click.echo()

        # List TF Outputs:
        local_outputs_maxlength = 0
        # Check length of output name, if longer then current value replace. This variable will be used for alignment offset.
        for output in outputs:
            local_outputs_maxlength = len(output.get('name')) if len(output.get('name')) > local_outputs_maxlength else local_outputs_maxlength
            log.debug("{}: Output maxlength offset value set to {}".format(log_msg, local_outputs_maxlength))
        
        # Iterate back through the output list, and print all the things.
        for output in outputs:
            output_offset = local_outputs_maxlength - len(output.get('name'))
            click.secho("{}{} = {{".format(output.get('name', ""), " " * output_offset), fg='blue')
            click.secho("{}{}".format(" " * 4, output.get('value', 'resource.name.arn')), fg='green')
            click.secho("}", fg='blue')
            click.echo()
        log.debug("{}: Listing output results completed!".format(log_msg))
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to parse the terraform project outputs object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.", 'error', arg_lower_nl=True, arg_upper_nl=True)
        log.error("{}: MagicDoc failed to parse the terraform project outputs object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg))
        log.error("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()


###############################
# TF Tree CMD:
# CMD: magicdoc tf show tree
################################
@show.command()
@click.pass_context
def tree(ctx):
    """Display Terraform Project Directory Tree"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Directory Tree Structure:")

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Gathering Terraform Project Outputs...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        log.debug("{}: Call tree constructor module...".format(log_msg))
        # Call the tree module to construct the tree variable used for output.
        local_dir_tree = DirTree(ctx.obj.log, ctx.obj.workdir)
        log.debug("{}: Directory tree render completed!".format(log_msg))
        click.secho(local_dir_tree, fg='blue')
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to render directory tree structure! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.", 'warning', arg_upper_nl=True, arg_lower_nl=True)
        log.warning("{}: MagicDoc failed to render directory tree structure! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg))
        log.warning("{}: Exception: {}".format(str(e)).format(log_msg))
        click.echo()
        sys.exit()


###############################
# TF Graph CMD:
# CMD: magicdoc tf show graph
################################
@show.command()
@click.option(
    '--overwrite', '-o', show_envvar=True,
    type=click.BOOL,
    default=False,
    help='Overwrite existing .terraform init if found.'
)
@click.pass_context
def graph(ctx, overwrite):
    """Display Terraform Project dot Graph Object"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Graph dot Structure:", arg_args={'Overwrite Existing .terraform Directory': str(overwrite)})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Generating Terraform Project Graph...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        log.debug("{}: Calling terraform dot graph file generation on target project directory: {}.".format(log_msg, ctx.obj.workdir))

        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Generating terraform graph dot object...", fg='green')
        ctx.obj.tf.graph = overwrite
        graph = ctx.obj.tf.graph
        
        if graph is not None:
            log.debug("{}: Terraform project graph structure object instantiation completed successfully!".format(log_msg))
            click.secho(graph, fg='blue')
        else:
            click.secho("Attempt to generate Terraform project graph structure object failed! See debug log for details", 'bright_red')
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to generate graph dot structure object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.", 'warning', arg_upper_nl=True, arg_lower_nl=True)
        log.warning("{}: MagicDoc failed to generate graph dot structure object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(log_msg))
        log.warning("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()


###############################
# TF Git CMD:
# CMD: magicdoc tf show git
################################
@show.command()
@click.pass_context
def git(ctx):
    """Display Terraform Project Git Config Data"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Git Config:")

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Parsing Terraform Project Git Config...", arg_upper_nl=False, arg_lower_nl=True)

    # COMMAND SYNTAX: Define the command sequence.
    try:
        log.debug("{}: Calling GitParser to attempt to parse the target project git config: {}.".format(log_msg, os.path.join(ctx.obj.workdir, '.git/config')))

        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Attempting to parse target project git config...", fg='green')
        git = GitParser(ctx.obj.log, ctx.obj.workdir)
        
        if git.config is not None and isinstance(git.config, list) and len(git.config) > 0:
            log.debug("{}: Terraform project repo object instantiation completed successfully!".format(log_msg))
            for item in git.config:
                ctx.obj.format_as_map(item)
        else:
            click.secho("Attempt to parse Terraform project git config failed! See debug log for details", 'bright_red')
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to parse git config for target project! Ensure that the project has a git configuration and try again.", 'warning', arg_upper_nl=True, arg_lower_nl=True)
        log.warning("{}: MagicDoc failed to parse git config for target project!".format(log_msg))
        log.warning("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()


###############################
# TF Repo CMD:
# CMD: magicdoc tf show repo
################################
@show.command()
@click.option(
    '--auth', '-a', show_envvar=True,
    type=click.STRING,
    default=None,
    help='Provide Git Repository Auth Token.'
)
@click.pass_context
def repo(ctx, auth):
    """Display Terraform Project Git Repository Data"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Git Repository:", arg_args={'Git Authentication Token Provided': str(bool(auth))})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Sending Terraform Project Git Repository Request...", arg_upper_nl=False, arg_lower_nl=True)
    click.echo()

    # COMMAND SYNTAX: Define the command sequence.
    try:
        log.debug("{}: Calling GitParser to attempt to send GET request to target project repository: {}.".format(log_msg, os.path.join(ctx.obj.workdir, '.git/config')))

        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Git Repository Response:", fg='yellow')
        click.secho("========================", fg='yellow')
        git = GitParser(ctx.obj.log, ctx.obj.workdir)
        
        if git.config is not None and isinstance(git.config, list) and len(git.config) > 0:
            log.debug("{}: Terraform project repo object instantiation completed successfully!".format(log_msg))
            git.repo = auth
            ctx.obj.format_as_map(git.repo)
        else:
            click.secho("The Terraform project git repository request failed! See debug log for details", 'bright_red')
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to receive valid data back from a sent request for the target directories  git repository. Please Ensure that the project has a git configuration and try again.", 'warning', arg_upper_nl=True, arg_lower_nl=True)
        log.warning("{}: MagicDoc failed to receive a valid git repository response for the target project!".format(log_msg))
        log.warning("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()


###############################
# TF Release CMD:
# CMD: magicdoc tf show release
################################
@show.command()
@click.option(
    '--auth', '-a', show_envvar=True,
    type=click.STRING,
    default=None,
    help='Provide Git Repository Auth Token.'
)
@click.pass_context
def release(ctx, auth):
    """Display Terraform Project Latest Release"""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "show {}".format(this), "MagicDoc Terraform Project Latest Release:", arg_args={'Git Authentication Token Provided': str(bool(auth))})
    click.echo()

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc [tf show {}] Command Environment:".format(this), arg_lower_nl=False)
    log.write("Sending Terraform Project Git Release Request...", arg_upper_nl=False, arg_lower_nl=True)
    click.echo()

    # COMMAND SYNTAX: Define the command sequence.
    try:
        log.debug("{}: Calling GitParser to attempt to send GET request to target project repository release data: {}.".format(log_msg, os.path.join(ctx.obj.workdir, '.git/config')))

        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Project Latest Release:", fg='green')
        click.secho("=======================", fg='green')
        git = GitParser(ctx.obj.log, ctx.obj.workdir)
        
        if git.config is not None and isinstance(git.config, list) and len(git.config) > 0:
            log.debug("{}: Terraform project config object instantiation completed successfully!".format(log_msg))
            # Call the repo method to gather the required data from github.
            git.repo = auth
            ctx.obj.log.args("{} Latest Release".format(git.repo.get('name')), "     {}".format(git.release))
        else:
            click.secho("The Terraform project git repository release request failed! See debug log for details", 'bright_red')
        click.echo()
    except Exception as e:
        log.write("MagicDoc failed to receive valid data back from a request sent to obtain the lastest project release. Please Ensure that the project has a git configuration and try again.", 'warning', arg_upper_nl=True, arg_lower_nl=True)
        log.warning("{}: MagicDoc failed to receive a valid git repository release response for the target project!".format(log_msg))
        log.warning("{}: Exception: {}".format(log_msg, str(e)))
        click.echo()
        sys.exit()
