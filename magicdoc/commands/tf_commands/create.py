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
import yaml

# Import Base Python Modules
import os, sys, json, inspect, ntpath

# Import MagicDoc Classes/Modules
from cloudmage.jinjautils import JinjaUtils
from magicdoc.classes.GitParser import GitParser
from magicdoc.modules.tree import DirTree

# Define Global Variables
LOG_CONTEXT = "CMD->tf_create"


##############################
# Define TF Create Group
# CMD: magicdoc tf create *
##############################
# Instantiate the tf subcommand groups:
@click.group()
@click.pass_context
def create(ctx):
    """Create a Magicdoc config or Documentation for your project."""
    pass


##############################
# TF Create config CMD:
# CMD: magicdoc tf create config -t module magicdoc.yaml
##############################
@create.command()
@click.option(
    '--type', '-t', show_envvar=True,
    type=click.Choice(['module', 'root'], case_sensitive=False),
    default='module',
    help='Create a MagicDoc project config file.'
)
@click.argument('filename', required=False)
@click.pass_context
def config(ctx, type, filename):
    """Create a magicdoc project configuration file."""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # LOCAL_ENV_VARIABLES: Define any local environments that the command function requires.
    filename = filename if filename is not None and len(filename) > 0 else "magicdoc.yaml"

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "create {}".format(this), "MagicDoc Terraform Documentation Creator:", arg_args={'Config Output File': os.path.join(ctx.obj.workdir, filename)})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc Terraform {} {} Generator: [tf create {} -t {} <output_file>]:".format(type.title(), this.title(), this, type), arg_lower_nl=False)
    log.write("Attempting to Gather Terraform Project Data...", arg_upper_nl=False, arg_lower_nl=True, arg_termcolor='blue')

    # Gather TF Files
    files = ctx.obj.tf.files

    if len(files.get('list_tf_files', [])) <= 0:
        click.secho("The current or specified directory does not appear to contain any terraform files.", fg='red')
        click.secho("Please navigate to the proper directory location or use the magicdoc tf -d option to specify the correct target project directory.", fg='bright_red')
        click.echo()
        sys.exit()
    else:
        # Gather TF Variables
        ctx.obj.tf.variables = include_examples=False
        variables = ctx.obj.tf.variables

        # construct the object that will be provided to the config template
        # tf = {}
        # tf.update(files=files, variables=variables)

        # Gather git config data if available
        git = GitParser(log, ctx.obj.workdir)

        try:
            if git.config is not None and isinstance(git.config, (list)) and len(git.config) > 0:
                # TODO: Always assign the first list element, this will be addressed in the official gitutils packages
                git._config = git.config[0]
            else:
                git._config = {'url': 'https://github.com/example/example', 'namespace': 'example_namespace', 'name': 'example_repo', 'provider': 'github.com'}
        except Exception as e:
            log.error("{}: An error occurred attempting to set git data: {}".format(log_msg, str(e)))
            git = {}
            git.update(
                config={'url': 'https://github.com/example/example', 'namespace': 'example_namespace', 'name': 'example_repo', 'provider': 'github.com'},
            )

        # COMMAND SYNTAX: Define the command sequence.
        try:
            # Format the filename argument:
            head, tail = ntpath.split(filename)
            output_file_name = tail or ntpath.basename(head) if tail is not None else filename
            output_file_basename, output_file_extention = os.path.splitext(output_file_name)
            magicdoc_config_file_name = "{}.yaml".format(output_file_basename)

            click.echo()
            log.write("Generating Terraform {} Magicdoc Config: {}".format(type.title(), magicdoc_config_file_name), arg_termcolor='blue', arg_lower_nl=False)

            # Instantiate a jinja instance so that we can produce the project config file.
            tf_config_template = ctx.obj.module_config_template if type.lower() == "module" else ctx.obj.root_config_template
            Config = JinjaUtils(log=log)
            Config.template_directory = ctx.obj.template_dir
            Config.load = tf_config_template
            Config.render(git=git, tf=ctx.obj.tf)
            Config.write(ctx.obj.workdir, magicdoc_config_file_name)

            click.echo()
            click.secho("Magicdoc Terraform {} config file: {} has been successfully created in :{}!".format(type.title(), magicdoc_config_file_name, ctx.obj.workdir), fg="yellow")
            click.echo()
        except Exception as e:
            click.echo()
            log.write("MagicDoc failed to create the terraform project config file: {}! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(os.path.join(ctx.obj.workdir, filename)), 'error', arg_upper_nl=True, arg_lower_nl=True)
            log.error("{}: failed to create the terraform project config file: {}!".format(log_msg, os.path.join(ctx.obj.workdir, filename)))
            log.error("{}: Exception: {}".format(log_msg, str(e)))
            click.echo()
            sys.exit()


##############################
# TF Create doc CMD:
# CMD: magicdoc tf create doc -t module README.md
##############################
@create.command()
@click.option(
    '--type', '-t', show_envvar=True,
    type=click.Choice(['module', 'root'], case_sensitive=False),
    default='module',
    help='Create a Terraform project README.md file.'
)
@click.option(
    '--auth', '-a', show_envvar=True,
    type=click.STRING,
    default=None,
    help='Provide Git Repository Authentication Token.'
)
@click.pass_context
def doc(ctx, type, auth):
    """Create a terraform module or project README.md file."""
    # DEFINE_SELF: Assign function identifier, log and declare the cmd environment.
    log = ctx.obj.log
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)

    # CLS: Clear the screen for the command unless in verbose mode.
    log.clear()

    # HEADER Command function header.
    # Options arg can be passed in the format of {'Option Text': 'Value'}
    log.header(log_msg, "create {}".format(this), "MagicDoc Terraform Documentation Creator:", arg_args={'Output File': 'README.md'})

    # ACTION_TITLE: Define the command action title
    log.write("MagicDoc Terraform {} {} Generator: [tf create {} -t {}]:".format(type.title(), this.title(), this, type), arg_lower_nl=False)
    log.write("Attempting to Gather Terraform Project Data...", arg_upper_nl=False, arg_lower_nl=True, arg_termcolor='blue')

    # Gather TF Files
    files = ctx.obj.tf.files

    if len(files.get('list_tf_files', [])) <= 0:
        click.echo()
        click.secho("ATTENTION:", fg='bright_black', bg='red')
        click.secho("The current or specified directory does not appear to contain any terraform files.", fg='red')
        click.secho("Please navigate to the proper directory location or use the magicdoc tf -d option to specify the correct target project directory.", fg='bright_red')
        click.echo()
        sys.exit()
    else:
        # Check if git data exists, if so then make the call to obtain git data, if not then provide a mock object
        try:
            # Gather git config data if available, otherwise provide a mock data structure as Jinja will expect the data keys to exist.
            git = GitParser(log, ctx.obj.workdir)
            try:
                if git.config is not None and isinstance(git.config, (list)) and len(git.config) > 0:
                    # TODO: Always assign the first list element, this will be addressed in the official gitutils packages
                    # git._config = git.config[0]
                    git.repo = auth
                    log.debug("{}: Git repository data has successfully been processed.".format(log_msg))
                else:
                    git._config = {'url': 'https://github.com/example/example', 'namespace': 'example_namespace', 'name': 'example_repo', 'provider': 'github.com'}
                    git._repo = {'name': 'example_repo', 'fullname': 'example_namespace/example_repo', 'description': 'Git repository data was not available when creating this document.', 'owner': 'example_owner', 'owner_url': 'https://github.com/users/example_owner'}
                    git._release = 'v0.0.0'
                    log.warning("{}: Git repository data was unavailable, default data scaffolding has been processed.".format(log_msg))
            except Exception as e:
                log.error("{}: An error occurred attempting to set git data: {}".format(log_msg, str(e)))
                git = {}
                git.update(
                    config={'url': 'https://github.com/example/example', 'namespace': 'example_namespace', 'name': 'example_repo', 'provider': 'github.com'},
                    repo={'name': 'example_repo', 'fullname': 'example_namespace/example_repo', 'description': 'Git repository data was not available when creating this document.', 'owner': 'example_owner', 'owner_url': 'https://github.com/users/example_owner'},
                    release='v0.0.0'
                )
            # Generate the terraform variable and output data
            try:
                # Gather TF Variables by calling object variables setter
                ctx.obj.tf.variables = include_examples=False
                log.debug("{}: Terraform variables dataset created successfully.".format(log_msg))

                # Gather TF Outputs by calling object outputs setter
                ctx.obj.tf.outputs = include_examples=False
                log.debug("{}: Terraform outputs dataset created successfully.".format(log_msg))
            except Exception as e:
                log.write("MagicDoc failed to gather the necessary terraform data to construct the requested document! Check your syntax, and retry. Enable verbose mode to find the source of the error that prevented the data collection.", 'error', arg_upper_nl=True, arg_lower_nl=True)
                log.error("{}: failed to gather the necessary terraform data to construct the requested document!", log_msg)
                log.error("{}: Exception: {}".format(log_msg, str(e)))
                click.echo()
                sys.exit()

            # Check for a terraform config object, and if one exists, then load it, if not then generate a mock config object.
            try:
                # If a config file wasn't found try to render one, and if it fails then just provide a mock variable structure so that the template will render properly.
                if ctx.obj.tf.config is None or not isinstance(ctx.obj.tf.config, dict) or not bool(ctx.obj.tf.config):
                    # Instantiate a jinja instance so that we can produce the project config file.
                    tf_config_template = ctx.obj.module_config_template if type.lower() == "module" else ctx.obj.root_config_template
                    Config = JinjaUtils(log=log)
                    Config.template_directory = ctx.obj.template_dir
                    Config.load = tf_config_template
                    Config.render(git=git, tf=ctx.obj.tf)
                    log.write("")
                    log.write("Magicdoc successfully created a one time config instance that will be used to process the create readme request.", 'info')
                    log.write("")

                    # Insert the generated config file into the tf object.
                    ctx.obj.tf._config = yaml.load(Config.rendered)
                    log.debug("{}: The following project config dataset has been constructed for this documentation creation instance:".format(log_msg))
                    log.debug(ctx.obj.tf._config)
            except:
                log.warning("{}: Magicdoc failed to created a one time config instance, constructing default schema.".format(log_msg))
                tf_mock_config = {}
                tf_mock_config.update(Git={'Repository': 'https://github.com/example/example', 'Version': 'v.0.0.0'})
                tf_mock_config.update(ReadMe={
                    'Title': 'Terraform Module Documentation',
                    'HeroImage': '',
                    'DocLink': '',
                    'GettingStarted': 'No project description has been provided at this time.',
                    'PreRequisites': 'This module does not currently have any pre-requisites or dependency requirements.',
                    'Module': '',
                    'Changelog': '',
                    'Contact': {'UserName':  '', 'Email': ''}
                })
                tf_mock_config.update(Variables={'Required': {'Image': ""}, 'Optional': {'Image': ""}})
                ctx.obj.tf._config = tf_mock_config
                log.warning("{}: Magicdoc successfully created default config instance that will be used to process the create readme request.".format(log_msg))

            # Once Scans have been done print a console newline for display organization purposes
            click.echo()

            # Gather TF Graph Data
            # ctx.obj.tf.graph = overwrite
            # graph = ctx.obj.tf.graph

            # Generate the Terraform Project Graph
            # Create the Graph

            # Create Directory Structure Tree
            tree = DirTree(ctx.obj.log, ctx.obj.workdir)
        except Exception as e:
            log.write("MagicDoc failed to gather the necessary data to construct the requested document! Check your syntax, and retry. Enable verbose mode to find the source of the error that prevented the data collection.", 'error', arg_upper_nl=True, arg_lower_nl=True)
            log.error("{}: failed to gather the necessary data to construct the requested document!", log_msg)
            log.error("{}: Exception: {}".format(log_msg, str(e)))
            click.echo()
            sys.exit()

        # COMMAND SYNTAX: Define the command sequence.
        try:
            log.write("Generating Terraform {} Readme Documentation...".format(type.title()), arg_termcolor='green', arg_lower_nl=False)

            # Instantiate a jinja instance so that we can produce the project config file.
            log.debug("{}: Attempting to generate document with the following datasets:".format(log_msg))
            log.debug("{}: Dumping git object that will be passed to JinjaUtils -> {}".format(log_msg, dir(git)))
            log.debug("{}: Dumping tf object that will be passed to JinjaUtils -> {}".format(log_msg, dir(ctx.obj.tf)))
            log.debug("{}: Dumping tf config object that will be passed to JinjaUtils -> {}".format(log_msg, ctx.obj.tf.config))
            log.debug("{}: Dumping tree object that will be passed to JinjaUtils -> {}".format(log_msg, tree))
            tf_readme_template = ctx.obj.module_readme_template if type.lower() == "module" else ctx.obj.root_readme_template
            ReadMe = JinjaUtils(log=log)
            ReadMe.template_directory = ctx.obj.template_dir
            ReadMe.load = tf_readme_template
            ReadMe.render(git=git, tf=ctx.obj.tf, tree=tree)
            ReadMe.write(ctx.obj.workdir, 'README.md')
        except Exception as e:
            log.write("MagicDoc failed to create the terraform project documentation file: {}! Check your syntax, and retry. If you feel this is a bug please submit an issue on the project repository.".format(os.path.join(ctx.obj.workdir, "README.md")), 'error', arg_upper_nl=True, arg_lower_nl=True)
            log.error("{}: failed to create the terraform project documentation file!".format(log_msg, os.path.join(ctx.obj.workdir)))
            log.error("{}: Exception: {}".format(log_msg, str(e)))
            click.echo()
            sys.exit()

        click.secho("Magicdoc Terraform {} documentation file: {} has been successfully created in :{}!".format(type.title(), "README.md", ctx.obj.workdir), fg="yellow")
        click.echo()
