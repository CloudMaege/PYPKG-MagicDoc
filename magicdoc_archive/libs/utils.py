##############################################################################
# CloudMage : MagicDoc Utility Functions
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#  - Utility Functions
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:
###############
# Import Pip Installed Modules:
from termcolor import colored, cprint

# Import Base Python Modules
import ntpath, logging
from pathlib import Path


# Instantiate the logger
log = logging.getLogger('magicdoc.libs.utils')


def SplitPath(Path):
    """Takes a passed file path (/var/lib/file1) and returns the file as a list separated by path/file ([path, file])"""
    # Split the path from the file name and just return the file name.        
    head, tail = ntpath.split(Path)
    return head, tail


def FindFileName(Path):
    """Takes a passed file path (/var/lib/file1) and returns only the filename, stripping the path (file1)"""
    # Split the path from the file name and just return the file name.        
    head, tail = ntpath.split(Path)
    return tail or ntpath.basename(head)


def BuildDirTree(DirPath: Path, DirPrefix: str=''):
    """Function that will build a directory tree from a given file path"""
    try:
        # Designate Directory Tree Prefix Symbols
        SpacePrefix =  '    '
        BranchPrefix = '│   '
        TeePrefix =    '├── '
        FinalPrefix =   '└── '

        # Create the Directory List
        Contents = list(DirPath.iterdir())
        # Remove virtualenv and git directories, as these won't be committed to the repo and shouldn't be in the module documentation.
        for item in Contents:
            if 'venv' in str(item) or '.git' in str(item):
                Contents.remove(item)
        # Set Pointers
        Pointers = [TeePrefix] * (len(Contents) - 1) + [FinalPrefix]
        # Build the Tree Generator
        for Pointer, Path in zip(Pointers, Contents):
            yield DirPrefix + Pointer + Path.name
            if Path.is_dir():
                Extension = BranchPrefix if Pointer == TeePrefix else SpacePrefix 
                yield from BuildDirTree(Path, DirPrefix=DirPrefix+Extension)
    except Exception as e:
        cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error encountered attempting to build directory tree:\n\nException: {}".format(str(e)), 'red')
        log.error("Unknown Exception occurred attempting to build the directory structure tree:")
        log.error(str(e))
        pass


def DirTree(DirPath):
    """Function will use the BuildDirTree Generator to generate a directory path ascii tree, store the output and return it to the caller."""
    try:
        log.debug("Attempting to build directory tree variable...")
        # Set a variable for the Directory tree, and then call the Directory Tree Generator
        Tree = ".\n"
        for line in BuildDirTree(Path(DirPath)):
            if line != "":
                Tree += "{}\n".format(line)
        log.debug("Directory Tree variable created successfully:")
        log.debug("\n{}".format(Tree))
        # Return the tree to the caller:
        return Tree
    except Exception as e:
        cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error encountered requesting directory tree return object:\n\nException: {}".format(str(e)), 'red')
        log.error("Unknown Exception occurred attempting to request a directory structure tree build request.:")
        log.error(str(e))
        pass


def SetPath(directory, context):
    """Function to set the command path from either a passed argument, or from the click context object"""
    # Set the directory location based on either the magicdoc option, or provided command argument.
    if directory is not None:
        log.debug("Directory path location set by provided argument: {}".format(directory))
        path = directory
    else:
        path = context.obj.get('directory', './')
        log.debug("Directory path location set by provided context or default value: {}".format(path))
    cprint("Using Directory Path: {}\n".format(path), 'blue')
    return path

def ParseRepoUrl(path):
    """Function to parse the .git/config Repository settings file, and use it to determine the Git Repo NameSpace and RepoName"""
    # Set the RepoUrl variable as it need to be checked while parsing the .git/config file.
    RepoUrl = None
    log.debug("Checking if .git/config exists within the specified path...")
    log.debug(".git/config file found.. parsing for configured url")
    try:
        # Open the file and attempt to find the Repository URL
        with open("{}/.git/config".format(path), 'r') as GitConfig:
            for count, line in enumerate(GitConfig):
                if 'url' in line:
                    RepoUrl = line
                    log.debug("Repository URL found: {}".format(RepoUrl))
                    break
        GitConfig.close()

        if RepoUrl is not None:
            log.debug("Attempting to determine namespace and repo from parsed URL...")
            RepoUrl = RepoUrl.strip()
            RepoUrl = RepoUrl.split(" = ")[1]
            log.debug("Formatted RepoUrl: {}... splitting by /".format(RepoUrl))
            RepoUrl = RepoUrl.split("/")
            ParsedRepo = RepoUrl[-1].replace(".git", "")
            ParsedNamespace = RepoUrl[-2]
            # If the git@ pattern is found then split on the colon, if not, then the repo should be https, and will not need the split.
            # The second to last list element should already be purely the namespace.
            if "git@" in ParsedNamespace:
                ParsedNamespace = ParsedNamespace.split(":")[1]
            # Log the results and return the objects.
            log.debug("Setting Repository Namespace: {} for Repository: {}".format(ParsedNamespace, ParsedRepo))
            return ParsedNamespace, ParsedRepo
    except Exception as e:
        cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error encountered while determining RepoUrl from .git/config file:\n\nException: {}".format(str(e)), 'red')
        log.error("Unknown Exception occurred attempting to determine RepoUrl from .git/config")
        log.error(str(e))
    pass
