##############################################################################
# CloudMage : MagicDoc Terraform Module Docs
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Terraform Documentation Class 
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
from termcolor import colored, cprint
from python_terraform import *
import hcl, yaml, requests

# Import Base Python Modules
from datetime import datetime
import logging, os

# Instantiate Logger
log = logging.getLogger('magicdoc.libs.tfdoc')


#####################
# Class Definition: #
#####################
class TFDoc(object):
    """MagicDoc Terraform Documentation Class"""

    def __init__(self, path='./', subdir=True):
        '''TFDoc Class Constructor'''

        # Set class variables
        self.path = path
        self.scan_subdir = subdir

        # Check the provided directory path
        assert os.path.isdir(self.path), "Error: Provided path is not a valid path. No File or Directory Found in specified location: {}".format(self.path)


    def FetchFileList(self):
        '''Class function that iterates through a given file path and collects a list of terraform files.'''

        try:
            # Set variable to hold the retrieved file list.
            file_list = []
            log.debug("Gathering list of all Terraform Files ending in the [.tf] file extension from: {}".format(self.path))
            # Gather the file list.
            for root, dirs, files in os.walk(self.path):
                # Strip the current directory designations
                dirpath = root.replace(".", "")
                dirpath = dirpath.replace("./", "")
                for filename in files:
                    # If the file is a TF file, then append it to the list.
                    if '.tf' in filename:
                        file_list.append(os.path.join(dirpath, filename))
                # If scan_subdirectories is set to false, then break, as the first pass gathers only the current directory.
                if not self.scan_subdir:
                    break
            # Log and return the result list.
            log.debug("File List Collected Successfully")
            log.debug(file_list)
            return file_list
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to construct terraform file list:\n\nException: {}\n".format(str(e)), 'red')
            log.error("Unexpected Error occurred attempting to construct terraform file list.")
            log.error(str(e))
            raise
