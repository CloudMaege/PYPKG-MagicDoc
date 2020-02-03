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


    ############################################
    # Construct Terraform File List:           #
    ############################################
    def FetchFileList(self):
        '''Class method that iterates through a given file path and collects a list of terraform files.'''
        try:
            # Set variable to hold the retrieved file list.
            CollectedFileList = []
            
            log.debug("Gathering list of all Terraform Files ending in the [.tf] file extension from: {}".format(self.path))
            # Gather the file list.
            for root, dirs, files in os.walk(self.path):
                # Strip the current directory designations
                dirpath = root.replace(".", "")
                dirpath = dirpath.replace("./", "")
                for filename in files:
                    # If the file is a TF file, then append it to the list.
                    if '.tf' in filename:
                        CollectedFileList.append(os.path.join(dirpath, filename))
                # If scan_subdirectories is set to false, then break, as the first pass gathers only the current directory.
                if not self.scan_subdir:
                    break
            # Log and return the result list.
            log.debug("File List Collected Successfully")
            log.debug(CollectedFileList)
            return CollectedFileList
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to construct terraform file list:\n\nException: {}\n".format(str(e)), 'red')
            log.error("Unexpected Error occurred attempting to construct terraform file list.")
            log.error(str(e))
            raise


    ##############################################
    # Construct Terraform Module Variable Lists: #
    ##############################################
    def BuildVarList(self):
        '''Class method that iterates through the collected terraform files, and locates any variables.tf files, parses the files, and returns a dict object of the collected file contents'''
        try:
            # Define the return Object
            TFVariables = {}
            
            # Define Variables that will hold the Required and Optional Variables.
            TFRequiredVars = []
            TFOptionalVars = []
            
            # Define Variables to track the length of each variable so that spacing can be set correctly in the documentation
            TFReqMaxLen = 0
            TFOptMaxLen = 0

            # Iterate through the project files and look for the variables.tf file, then load it into a dict that can be sent to the doc template.
            log.info("Building module variable list...")
            
            # Call the FetchFileList method to get a list of all tf files
            TF_Files = self.FetchFileList()
            
            # Iterate through the file collection and construct a variables dictionary containing all of the projects variables.
            for tf in TF_Files:
                if 'variables.tf' in tf and 'example' not in tf and 'examples' not in tf:
                    log.debug("variables.tf file FOUND: [{}]".format(tf))
                    with open(tf, 'r') as VarFile:
                        Vars = hcl.load(VarFile)
                    log.debug("variables.tf file open, parsing, sorting, and storing variables...")
                    log.debug(json.dumps(Vars, indent=4, sort_keys=True))
                    # For each variable in the variables.tf file:
                    # Put the variable into either the Required, or Optional lists based on the existence or absence of a default value.
                    for k, v in Vars.get('variable').items():
                        # Create a base VarObject to pass to the template or back to the CLI containing the data collected from parsing the variables.tf file
                        VarObject = {
                            'Name': k,
                            'Type': v.get('type', 'Undefined'),
                            'Description': v.get('description', "No Description Provided"),
                            'ExampleValue': "Example Value"
                        }
                        # Check if Required Var
                        if v.get('default') == None:       
                            # Check the length of the current item, and if its larger then the current max, then set the new max.
                            if len(k) > TFReqMaxLen:
                                TFReqMaxLen = len(k)
                            # Log the required var and append to the required vars list.
                            log.debug("Added {} to TFRequiredVars list.".format(k))
                            TFRequiredVars.append(VarObject)
                        # If its not a Required Var, then it must be an Optional Var
                        else:
                            # Check the length of the current item, and if its larger then the current max, then set the new max.
                            if len(k) > TFOptMaxLen:
                                TFOptMaxLen = len(k)
                            # Add the default value to the optional variable object.
                            VarObject.update(DefaultValue=v.get('default'))
                            # Log the optional var and append to the optional vars list.
                            log.debug("Added {} to TFOptionalVars list.".format(k))
                            TFOptionalVars.append(VarObject)
            # Add the Variable Lists to the Template Dictionary
            log.debug("Adding Lists to return variables dictionary")
            TFVariables.update(required_vars=TFRequiredVars)
            TFVariables.update(required_vars_maxlength=TFReqMaxLen)
            TFVariables.update(optional_vars=TFOptionalVars)
            TFVariables.update(optional_vars_maxlength=TFOptMaxLen)
            # Log and return the results.
            log.info("Variable list processing completed:")
            log.info("{} Required Variables Collected: {}".format(len(TFRequiredVars), TFRequiredVars))
            log.info("Longest Required Variable Length: {}".format(TFReqMaxLen))
            log.info("{} Optional Variables Collected: {}".format(len(TFOptionalVars), TFOptionalVars))
            log.info("Longest Optional Variable Length: {}".format(TFOptMaxLen))
            return TFVariables
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to construct terraform variables list:\n\nException: {}\n".format(str(e)), 'red')
            log.error("Unexpected Error occurred attempting to construct terraform variables list.")
            log.error(str(e))
            raise


    ############################################
    # Construct Terraform Module Output List:  #
    ############################################
    def BuildOutputList(self):
        '''Class method that iterates through the collected terraform files, and locates any outputs.tf files, parses the files, and returns a dict object of the collected file contents'''
        try:
            # Define the return list Object
            TFOutputs = []
            
            # Call the FetchFileList method to get a list of all tf files
            TF_Files = self.FetchFileList()

            # Iterate through the project files and look for the outputs.tf file, then load it into a dict that can be sent to the doc templates.
            log.info("Building module output list...")
            for tf in TF_Files:
                if 'outputs.tf' in tf and 'example' not in tf and 'examples' not in tf:
                    log.debug("outputs.tf file FOUND: [{}]".format(tf))
                    with open(tf, 'r') as VarFile:
                        Outputs = hcl.load(VarFile)
                    log.debug("outputs.tf file open, parsing, sorting, and storing outputs...")
                    log.debug(json.dumps(Outputs, indent=4, sort_keys=True))

                    # Parse each output from the outputs.tf file and build a dict that can be sent to the doc template:
                    for k, v in Outputs.get('output').items():
                        # Create a OutputObj to pass to the template containing the data collected from parsing the output.tf file
                        OutputObj = {
                            'Name': k,
                            'OutputValue': v.get('value')
                        }

                        # Log the required var and append to the required vars list.
                        log.debug("Added {} to TFOutputs list.".format(k))
                        TFOutputs.append(OutputObj)

            # Log all the things
            log.info("Output list processing completed:")
            log.info("{} Module outputs Collected: {}".format(len(TFOutputs), TFOutputs))
            return TFOutputs
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to construct terraform outputs list:\n\nException: {}\n".format(str(e)), 'red')
            log.error("Unexpected Error occurred attempting to construct terraform outputs list.")
            log.error(str(e))
            raise
