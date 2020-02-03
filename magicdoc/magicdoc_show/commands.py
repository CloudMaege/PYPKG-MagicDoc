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
from libs.utils import split_path, find_filename
from libs.tfdoc import TFDoc

# Import Base Python Modules
import logging, sys

# Instantiate Logger
log = logging.getLogger('magicdoc.show.commands')


##############################
# MagicDoc Show Subcommands: #
##############################
@click.group()
@click.pass_context
def show(ctx):
    cprint("Using Provider: {}".format(ctx.obj.get('provider')), 'blue')
    if ctx.obj.get('directory') is not None:
        cprint("Using Directory Path: {}\n".format(ctx.obj.get('directory', './')), 'blue')
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

# File subcommand call.
def files(ctx, subdir: bool, directory: str):
    """Command that will retrieve a list of files from a target directory location matching the provider type specified (terraform = .tf)"""
    try:
        log.debug("show files command called using provided context: {}".format(ctx.obj))
        # Set the directory location based on either the magicdoc option, or show files command argument.
        if directory is not None:
            path = directory
            log.debug("directory path location set by provided argument: {}".format(path))
        else:
            path = ctx.obj.get('directory', './')
            log.debug("directory path location set by provided context or default value: {}".format(path))
        # Print the provided directory path.
        cprint("Using Directory Path: {}\n".format(path), 'blue')
        
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
            # Call split_path to find found results in subdirectories.
            item_path_list = split_path(item)
            # Print results
            if not item_path_list[0]:
                cprint(item_path_list[1], 'white')
                log.debug(item_path_list[1])
            else:
                print(colored("/{} =>".format(item_path_list[0]), 'blue'), colored(item_path_list[1], 'white'))
                log.debug("{} => {}".format(item_path_list[0], item_path_list[1]))
    except Exception as e:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again", 'red')
        log.error("Error: Failed to retrieve file list from the provided file path location, check the provided file path and try again")
        log.error(str(e))
        sys.exit()


###############################################
# Add Show subcommands to Show Command Group: #
###############################################
show.add_command(files)