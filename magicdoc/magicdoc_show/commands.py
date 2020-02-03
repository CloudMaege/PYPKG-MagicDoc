##############################################################################
# CloudMage : MagicDoc Show Commands
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#  - Show Subcommand List
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

# Import MagicDoc classes
from libs.utils import SetPath, SplitPath
from libs.tfdoc import TFDoc
from libs.github import Github

# Import Base Python Modules
import logging, sys, json, os

# Instantiate Logger
log = logging.getLogger('magicdoc.show.commands')


##############################
# MagicDoc Show Subcommands: #
##############################
@click.group()
@click.pass_context
def show(ctx):
    cprint("Using Provider: {}".format(ctx.obj.get('provider')), 'blue')
    log.debug("Show command called using provided context: {}".format(ctx.obj))
    pass


##############################
# MagicDoc Show Files:       #
##############################
@show.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Set scan subdirectory option to true or false. True = recursive, False = parent directory only
@click.option(
    '--subdir', '-s', show_envvar=True,
    type=click.BOOL,
    default=True,
    help="Specify if the target project directory should be scanned recursively. [True = Recursive, False = Parent Directory Only]"
)

# Pass context
@click.pass_context

# Files subcommand call.
def files(ctx, subdir: bool, directory: str):
    """Command that will retrieve a list of files from a target directory location matching the provider type specified (terraform = .tf)"""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)
        
        # Set the type of provider class to call
        if ctx.obj.get('provider').lower() == 'terraform' or ctx.obj.get('provider') == 'tf':
            Files = TFDoc(path, subdir).FetchFileList()
            log.debug("File list retrieved from provided file path...")
        # Print command results.
        cprint("{} {} files found in target directory: {}".format(len(Files), ctx.obj.get('provider').lower(), path), 'green')
        
        # Print the results
        for item in Files:
            # For the command output remove the base path specified as its redundant
            item = item.replace("{}/".format(path), "")
            # Call SplitPath to find found results in subdirectories.
            item_path_list = SplitPath(item)
            # Print results
            if not item_path_list[0]:
                cprint(item_path_list[1], 'white')
                log.debug(item_path_list[1])
            else:
                print(colored("/{} =>".format(item_path_list[0]), 'blue'), colored(item_path_list[1], 'white'))
                log.debug("{} => {}".format(item_path_list[0], item_path_list[1]))
            print("\n")
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again")
        log.error(str(e))
        sys.exit()


##############################
# MagicDoc Show Variables:   #
##############################
@show.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Set scan subdirectory option to true or false. True = recursive, False = parent directory only
@click.option(
    '--subdir', '-s', show_envvar=False,
    type=click.BOOL,
    default=True,
    help="Specify if the target project directory should be scanned recursively. [True = Recursive, False = Parent Directory Only]. If True, then the variable output will be a collection of all variable files."
)

# Pass context
@click.pass_context

# Variables subcommand call.
def variables(ctx, subdir: bool, directory: str):
    """Command that will retrieve a list of all of the project variables from the specified project path."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)

        # Set the type of provider class to call
        if ctx.obj.get('provider').lower() == 'terraform' or ctx.obj.get('provider') == 'tf':
            Variables = TFDoc(path, subdir).BuildVarList()
            log.debug("Variable list retrieved from provided file path...")
        
        # Print Required Variable Results.
        cprint("{} {} required variables found in target project: {}".format(len(Variables.get('required_vars')), ctx.obj.get('provider').lower(), path), 'green')
        for reqvar in Variables.get('required_vars', []):
            offset = Variables.get('required_vars_maxlength') - len(reqvar.get('Name'))
            print(colored("{}{} =".format(reqvar.get('Name'), " " * offset), 'blue'), colored("Value Required", 'green'))
        print("\n")
        # Print Optional Variable Results.
        cprint("{} {} optional variables found in target project: {}".format(len(Variables.get('optional_vars')), ctx.obj.get('provider').lower(), path), 'green')
        for optvar in Variables.get('optional_vars', []):
            offset = Variables.get('optional_vars_maxlength') - len(optvar.get('Name'))
            # Try to make the output nice and pretty, but if it fails, then default to normal print
            try:
                if 'list' in optvar.get('Type') and len(optvar.get('DefaultValue')) > 0:
                    print(colored("{}{} =".format(optvar.get('Name'), " " * offset), 'blue'), colored('[', 'green'))
                    for item in optvar.get('DefaultValue'):
                        if isinstance(item, dict):
                            cprint(json.dumps(item, indent=4, sort_keys=True), 'green')
                        else:
                            cprint("    {}".format(item), 'green')
                    cprint(']', 'green')
                elif 'map' in optvar.get('Type'):
                    print(colored("{}{} =".format(optvar.get('Name'), " " * offset), 'blue'), colored(json.dumps(optvar.get('DefaultValue'), indent=4, sort_keys=True), 'green'))
                else:
                    print(colored("{}{} =".format(optvar.get('Name'), " " * offset), 'blue'), colored(optvar.get('DefaultValue'), 'green'))
            except Exception:
                print(colored("{}{} =".format(optvar.get('Name'), " " * offset), 'blue'), colored(optvar.get('DefaultValue'), 'green'))
        print("\n")
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to retrieve variable list from the provided file path location, check the provided file path and try again", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to retrieve variable list from the provided file path location, check the provided file path and try again")
        log.error(str(e))
        sys.exit()


##############################
# MagicDoc Show Outputs:     #
##############################
@show.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Set scan subdirectory option to true or false. True = recursive, False = parent directory only
@click.option(
    '--subdir', '-s', show_envvar=False,
    type=click.BOOL,
    default=True,
    help="Specify if the target project directory should be scanned recursively. [True = Recursive, False = Parent Directory Only]. If True, then outputs will be a collection of all output files."
)

# Pass context
@click.pass_context

# Outputs subcommand call.
def outputs(ctx, subdir: bool, directory: str):
    """Command that will retrieve a list of all of the project outputs from the specified project path."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)

        # Set the type of provider class to call
        if ctx.obj.get('provider').lower() == 'terraform' or ctx.obj.get('provider') == 'tf':
            Outputs = TFDoc(path, subdir).BuildOutputList()
            log.debug("Variable list retrieved from provided file path...")
        # Print Outputs.
        cprint("{} {} outputs found in target project: {}".format(len(Outputs), ctx.obj.get('provider').lower(), path), 'green')
        
        # To make the print format uniform, cycle through the outputs object and get a max length to use for an offset value.
        Output_MaxLength = 0
        for output in Outputs:
            if len(output.get('Name')) > Output_MaxLength:
                Output_MaxLength = len(output.get('Name'))
        # Print Outputs:
        for output in Outputs:
            offset = Output_MaxLength - len(output.get('Name'))
            print(colored("{}{} =".format(output.get('Name'), " " * offset), 'blue'), colored(str(output.get('OutputValue')), 'green'))
        print("\n")
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to retrieve output list from the provided file path location, check the provided file path and try again", 'red')
        cprint(str(e), 'red')
        log.error("Error: Failed to retrieve outputs list from the provided file path location, check the provided file path and try again")
        log.error(str(e))
        raise
        sys.exit()


###########################
# MagicDoc Show Repo:     #
###########################
@show.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Provide an access token to make the repository request.
@click.option(
    '--token', '-t', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the git provider access token that will be used to authenticate the repository and release requests."
)

# Set repository namespace
@click.option(
    '--namespace', '-n', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the repository namespace under which the target repository exists."
)

# Set repository name
@click.option(
    '--repo', '-r', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the name of the repository being searched for."
)

# Pass context
@click.pass_context

# Files subcommand call.
def repo(ctx, namespace: str, repo: str, directory: str, token: str):
    """Command that will retrieve the project repository information from the projects configured GIT repository."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)
        
        # If the namespace and repository were provided, then assign the values, if not check for .git/config file and parse.
        if repo is not None and namespace is not None:
            RequestObj = Github(namespace, repo, token).GetGitHubData()
        # Try and fetch the repository URL from the configured directory.
        elif os.path.exists("{}/.git/config".format(path)):
            namespace, repo = ParseRepoUrl(path)
            RequestObj = Github(namespace, repo, token).GetGitHubData()
        else:
            RequestObj = {'state': 'fail'}
        print(json.dumps(RequestObj, indent=4, sort_keys=True))
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Warning: Failed to retrieve GIT repository data for the targeted project.", 'red')
        cprint(str(e), 'red')
        log.error("Warning: Failed to retrieve GIT repository data for the targeted project. Check the provided namespace and repo settings and try again.")
        log.error(str(e))
        sys.exit()


###########################
# MagicDoc Show Release:  #
###########################
@show.command()

# Pass directory path to search:
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    default=None,
    required=False
)

# Provide an access token to make the repository request.
@click.option(
    '--token', '-t', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the git provider access token that will be used to authenticate the repository and release requests."
)

# Set repository namespace
@click.option(
    '--namespace', '-n', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the repository namespace under which the target repository exists."
)

# Set repository name
@click.option(
    '--repo', '-r', show_envvar=True,
    type=click.STRING,
    default=None,
    help="Specify the name of the repository being searched for."
)

# Pass context
@click.pass_context

# Files subcommand call.
def release(ctx, namespace: str, repo: str, directory: str, token: str):
    """Command that will retrieve the project repository information from the projects configured GIT repository."""
    try:
        # Set the directory path based on either the passed directory arg, or the click context.
        path = SetPath(directory, ctx)

        # If the namespace and repository were provided, then assign the values, if not check for .git/config file and parse.
        if repo is not None and namespace is not None:
            RequestObj = Github(namespace, repo, token).GetLatestRelease()
        # Try and fetch the repository URL from the configured directory.
        elif os.path.exists("{}/.git/config".format(path)):
            namespace, repo = ParseRepoUrl(path)
            RequestObj = Github(namespace, repo, token).GetLatestRelease()
        else:
            RequestObj = "Undefined"
        print("Latest Release: {}".format(RequestObj))
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Warning: Failed to retrieve GIT repository release data for the targeted project.", 'red')
        cprint(str(e), 'red')
        log.error("Warning: Failed to retrieve GIT repository release data for the targeted project. Check the provided namespace and repo settings and try again.")
        log.error(str(e))
        sys.exit()


###############################################
# Add Show subcommands to Show Command Group: #
###############################################
show.add_command(files)
show.add_command(variables)
show.add_command(outputs)
show.add_command(repo)