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
import os, sys, json, ntpath

# Import MagicDoc Classes/Modules
from magicdoc.modules.tree import DirTree


##############################
# Define TF Show Group
# CMD: magicdoc tf show *
##############################
# Instantiate the tf subcommand groups:
@click.group()
@click.pass_context
def show(ctx):
    pass

##############################
# TF Files CMD:
# CMD: magicdoc tf show files
##############################
@show.command()
@click.pass_context
def files(ctx):
    """Display Terraform Project File Lists."""
    try:
        # Assign context objects
        log = ctx.obj.log
        files = ctx.obj.tf.files

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF File Summary:")

        log.info("Invoking command magicdoc tf show files")
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
        log.error("MagicDoc failed to parse the terraform project files object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
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
    try:
        # Assign context objects
        log = ctx.obj.log
        
        # Trigger the property setter to populate the variables object, then assign it for usage.
        ctx.obj.tf.variables = include_examples
        variables = ctx.obj.tf.variables

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF Variable Summary:")

        log.info("Invoking command magicdoc tf show variables")
        log.info("Working with returned variables object:")
        log.debug(json.dumps(variables, indent=4, sort_keys=True))
        log.debug(' ')
        click.secho("{} required terraform project variables found in target project: {}".format(len(variables.get('required_vars', [])), ctx.obj.workdir), fg='bright_black')
        click.secho("{} optional terraform project variables found in target project: {}".format(len(variables.get('optional_vars', [])), ctx.obj.workdir), fg='bright_black')
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
        log.error("MagicDoc failed to parse the terraform project variables object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
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
    try:
        # Assign context objects
        log = ctx.obj.log
        # Trigger the property setter to populate the outputs object, then assign it for usage.
        ctx.obj.tf.outputs = include_examples
        outputs = ctx.obj.tf.outputs

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF Output Summary:")

        log.info("Invoking command magicdoc tf show outputs")
        log.info("Working with returned outputs list:")
        log.debug(outputs)
        log.debug(' ')
        click.secho("{} terraform project outputs found in target project: {}".format(len(outputs), ctx.obj.workdir), fg='bright_black')
        click.echo()

        # List TF Outputs:
        outputs_maxlength = 0
        # Check length of output name, if longer then current value replace. This variable will be used for alignment offset.
        for output in outputs:
            outputs_maxlength = len(output.get('name')) if len(output.get('name')) > outputs_maxlength else outputs_maxlength
            log.debug("Output maxlength offset value set to {}".format(outputs_maxlength))
        
        # Iterate back through the output list, and print all the things.
        for output in outputs:
            output_offset = outputs_maxlength - len(output.get('name'))
            click.secho("{}{} = {{".format(output.get('name', ""), " " * output_offset), fg='blue')
            click.secho("{}{}".format(" " * 4, output.get('value', 'resource.name.arn')), fg='green')
            click.secho("}", fg='blue')
            click.echo()
        log.debug("Listing output results completed!")
        click.echo()
    except Exception as e:
        log.error("MagicDoc failed to parse the terraform project outputs object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
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
    try:
        # Assign context objects
        log = ctx.obj.log

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF Project Tree:")

        log.info("Invoking command magicdoc tf show tree")
        log.debug("Call tree constructor module...")
        # Call the tree module to construct the tree variable used for output.
        dir_tree = DirTree(ctx.obj.log, ctx.obj.workdir)
        log.debug("Directory tree render completed!")
        click.secho(dir_tree, fg='blue')
        click.echo()
    except Exception as e:
        log.error("MagicDoc failed to render directory tree structure! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
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
    try:
        # Assign context objects
        log = ctx.obj.log

        log.info("Invoking command magicdoc tf show graph")
        log.debug("Calling terraform dot graph generation and working with returned graph object.")

        if not ctx.obj.verbose:
            click.clear()
        log.header("MagicDoc TF Project Graph:")

        # Trigger the property setter to populate the outputs object, then assign it for usage.
        click.secho("Generating terraform graph dot object...", fg='green')
        ctx.obj.tf.graph = overwrite
        graph = ctx.obj.tf.graph
        
        if graph is not None:
            log.debug("Terraform project graph structure object instantiation completed successfully!")
            click.secho(graph, fg='blue')
        else:
            click.secho("Attempt to generate Terraform project graph structure object failed! See debug log for details", 'bright_red')
        click.echo()
    except Exception as e:
        log.error("MagicDoc failed to generate graph dot structure object! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.")
        log.error("Exception: {}".format(str(e)))
        click.echo()
        sys.exit()
