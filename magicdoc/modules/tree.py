##############################################################################
# CloudMage : MagicDoc Tree Module Docs
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
import sys, logging

ModuleName = "MagicDocTree"
log = logging.getLogger()

def BuildDirTree(DirPath: Path, DirPrefix: str=''):
    """Function that will build a directory tree from a given file path"""
    try:
        # Designate Directory Tree Prefix Symbols
        SpacePrefix =  '    '
        BranchPrefix = '│   '
        TeePrefix =    '├── '
        FinalPrefix =   '└── '

        log.info("{}: BuildDirTree function called on {}".format(ModuleName, DirPath))
        Contents = list(DirPath.iterdir())
        log.debug("{}: {} contents collected".format(ModuleName, DirPath))
        log.debug(Contents)
        log.debug("{}: Seaching for [*.venv, *.git, *.terraform] files and directories to flag for list removal".format(ModuleName, DirPath))
        for item in Contents:
            if str(item).endswith(('.venv', '.git', '.terraform')) or 'venv' in str(item):
                Contents.remove(item)
        log.debug("{}: Setting item pointers".format(ModuleName))
        Pointers = [TeePrefix] * (len(Contents) - 1) + [FinalPrefix]
        log.debug("{}: Constructing file tree generator".format(ModuleName))
        for Pointer, Path in zip(Pointers, Contents):
            yield DirPrefix + Pointer + Path.name
            if Path.is_dir():
                Extension = BranchPrefix if Pointer == TeePrefix else SpacePrefix 
                yield from BuildDirTree(Path, DirPrefix=DirPrefix+Extension)
        log.debug("{}: File tree generator construction successful".format(ModuleName))
    except Exception as e:
        log.error("{}:{} failed to generate tree structure for directory {}".format(ModuleName, 'BuildDirTree', DirPath))
        log.error("Exception: {}".format(str(e)))
        pass


def DirTree(Log, DirPath):
    """Function will use the BuildDirTree Generator to generate a directory path ascii tree, store the output and return it to the caller."""
    try:
        Log.info("{}: DirTree function called on {}".format(ModuleName, DirPath))
        Log.info("{}: Attempting to render tree structure for directory: {}".format(ModuleName, DirPath))
        # Set a variable for the Directory tree, and then call the Directory Tree Generator
        Tree = ".\n"
        for line in BuildDirTree(Path(DirPath)):
            if line != "":
                Tree += "{}\n".format(line)
        Log.debug("{}: Directory Tree variable created successfully".format(ModuleName))
        Log.debug("\n{}".format(Tree))
        Log.info("{}: Returning constructed directory tree to caller.".format(ModuleName))
        return Tree
    except Exception as e:
        Log.error("{}:{} failed to render tree structure for directory {}".format(ModuleName, 'DirTree', DirPath))
        Log.error("Exception: {}".format(str(e)))
        pass
