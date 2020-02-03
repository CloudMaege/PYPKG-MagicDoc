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
# Import Base Python Modules
import ntpath, logging


# Instantiate the logger
log = logging.getLogger('magicdoc.libs.utils')


def split_path(filepath):
    """Takes a passed file path (/var/lib/file1) and returns the file as a list separated by path/file ([path, file])"""
    # Split the path from the file name and just return the file name.        
    head, tail = ntpath.split(filepath)
    return head, tail


def find_filename(filepath):
    """Takes a passed file path (/var/lib/file1) and returns only the filename, stripping the path (file1)"""
    # Split the path from the file name and just return the file name.        
    head, tail = ntpath.split(filepath)
    return tail or ntpath.basename(head)
