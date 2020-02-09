##############################################################################
# CloudMage : MagicDoc Tree Module
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - ASCII Directory Tree Constructor Module 
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Base Python Modules
from pathlib import Path
import sys, logging, inspect

# Define Global Variables
LOG_CONTEXT = "MOD->tree"

log = logging.getLogger()

def BuildDirTree(DirPath: Path, DirPrefix: str=''):
    """Function that will build a directory tree from a given file path"""
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)
    try:
        # Designate Directory Tree Prefix Symbols
        SpacePrefix =  '    '
        BranchPrefix = '│   '
        TeePrefix =    '├── '
        FinalPrefix =   '└── '

        log.info("{}: BuildDirTree function called on {}".format(log_msg, DirPath))
        Contents = list(DirPath.iterdir())
        log.debug("{}: {} contents collected".format(log_msg, DirPath))
        log.debug(Contents)
        log.debug("{}: Seaching for [*.venv, *.git, *.terraform] files and directories to flag for list removal".format(log_msg, DirPath))
        for item in Contents:
            if str(item).endswith(('.venv', '.git', '.terraform')) or 'venv' in str(item):
                Contents.remove(item)
        log.debug("{}: Setting item pointers".format(log_msg))
        Pointers = [TeePrefix] * (len(Contents) - 1) + [FinalPrefix]
        log.debug("{}: Constructing file tree generator".format(log_msg))
        for Pointer, Path in zip(Pointers, Contents):
            yield DirPrefix + Pointer + Path.name
            if Path.is_dir():
                Extension = BranchPrefix if Pointer == TeePrefix else SpacePrefix 
                yield from BuildDirTree(Path, DirPrefix=DirPrefix+Extension)
        log.debug("{}: File tree generator construction successful".format(log_msg))
    except Exception as e:
        log.error("{}:{} failed to generate tree structure for directory {}".format(log_msg, 'BuildDirTree', DirPath))
        log.error("Exception: {}".format(str(e)))
        pass


def DirTree(Log, DirPath):
    """Function will use the BuildDirTree Generator to generate a directory path ascii tree, store the output and return it to the caller."""
    this = inspect.stack()[0][3]
    log_msg = "{}.{}".format(LOG_CONTEXT, this)
    try:
        Log.info("{}: DirTree function called on {}".format(log_msg, DirPath))
        Log.info("{}: Attempting to render tree structure for directory: {}".format(log_msg, DirPath))
        # Set a variable for the Directory tree, and then call the Directory Tree Generator
        Tree = ".\n"
        for line in BuildDirTree(Path(DirPath)):
            if line != "":
                Tree += "{}\n".format(line)
        Log.debug("{}: Directory Tree variable created successfully".format(log_msg))
        Log.debug("\n{}".format(Tree))
        Log.info("{}: Returning constructed directory tree to caller.".format(log_msg))
        return Tree
    except Exception as e:
        Log.error("{}:{} failed to render tree structure for directory {}".format(log_msg, 'DirTree', DirPath))
        Log.error("Exception: {}".format(str(e)))
        pass
