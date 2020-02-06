##############################################################################
# CloudMage : MagicDoc Configuration Parser
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Yaml Config Parser
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################


###############
# Imports:    #
###############
# Import Pip Installed Modules:
from termcolor import colored, cprint
import yaml

# Import Base Python Modules
import logging, json, os, sys

# Instantiate Logger
log = logging.getLogger('magicdoc.libs.config')


#####################
# Class Definition: #
#####################
class Config(object):
    """MagicDoc Documentation Config Parser Class"""
    
    def __init__(self, Directory="./", FileName='README.yaml'):
        '''MagicDoc Documentation Config Parser Class Constructor'''

        # Set class variables
        self.directory = Directory
        self.filename = FileName
        log.debug("Config File Path: [{}]".format(self.directory))
        log.debug("Config File Name: [{}]".format(self.filename))

        # Load the config object
        self.LoadConfig()


    ######################
    # Load Config:      #
    ######################
    def LoadConfig(self):
        """Class method that will capture the provided config file, parse it, and construct the config dictionary object."""
        try:
            self.config = {}
            # Separate the file name from the given path, then, validate the extention.
            ConfigExt = os.path.splitext(self.filename)[1]
            log.debug("Config File Extension: [{}]".format(ConfigExt))
            # Verify that the file passed has the .yaml or .yml extension
            if ConfigExt == '.yaml' or ConfigExt == '.yml':
                # Attempt to open the file, err on exception
                with open(os.path.join(self.directory, self.filename)) as YamlFile:
                    self.config = yaml.load(YamlFile, Loader=yaml.FullLoader)
                log.info("Config loaded successfully from given file path.")
                log.debug(self.config)
            else:
                # If the passed file name isn't a yaml file
                cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
                cprint("Error encountered attempting to open the specified config file: [{}]".format(os.path.join(self.directory, self.filename)), 'red')
                cprint("Invalid file type specified. Config file must be of type .yaml or .yml\n", 'red')
                log.error("Invalid file specified. Config file must be of type .yaml or .yml")
                sys.exit()
        except Exception as e:
                cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
                cprint("Exception encountered attempting to open the specified config file: [{}]\n\nException: {}\n".format(os.path.join(self.directory, self.filename), str(e)), 'red')
                log.error("Unable to open the specified config file path.")
                log.error(str(e))


    #######################
    # Update Variables:   #
    #######################
    def UpdateVars(self, TemplateObj):
        """Class Method that will accept a dictionary object of variables, and add the additional keys from the config for use within the readme template."""
        try:
            # Update Required Vars
            log.debug("Attempting to update the provided template dictionary")
            log.debug(json.dumps(TemplateObj, indent=4, sort_keys=True))
            TFVariables = TemplateObj.get('variables')
            for variable in TFVariables.get('required_vars'):
                # For each variable in the TemplateObject Required Vars list, set the config variable
                log.debug("Attempting to update: {}".format(variable))
                ConfigVar = self.config.get('VariablesConfig').get('Required').get(variable.get('Name'))
                log.debug('Retrieved config variable data for {}: {}'.format(variable.get('Name'), ConfigVar))
                if ConfigVar is not None:
                    # Iterate over each key in the Config list, and add it to the TemplateObject Required Var.
                    log.debug("Attempting to update the template dictionaries required variables...")
                    for k, v in ConfigVar.items():
                        log.debug("Adding {}:{} to {}".format(k, v, json.dumps(variable, indent=4, sort_keys=True)))
                        variable.update({k: v})
                        log.debug("Update successful: {}".format(json.dumps(variable, indent=4, sort_keys=True)))
            # Rinse wash and repeat for optional vars
            for variable in TFVariables.get('optional_vars'):
                # For each variable in the TemplateObject Optional Vars list, set the config variable
                log.debug("Attempting to update: {}".format(variable))
                ConfigVar = self.config.get('VariablesConfig').get('Optional').get(variable.get('Name'))
                log.debug('Retrieved config variable data for {}: {}'.format(variable.get('Name'), ConfigVar))
                if ConfigVar is not None:
                    # Iterate over each key in the Config list, and add it to the TemplateObject Required Var.
                    log.debug("Attempting to update the template dictionaries required variables...")
                    for k, v in ConfigVar.items():
                        log.debug("Adding {}:{} to {}".format(k, v, json.dumps(variable, indent=4, sort_keys=True)))
                        variable.update({k: v})
                        log.debug("Update successful: {}".format(json.dumps(variable, indent=4, sort_keys=True)))
            log.info("Template dictionary required variables have been updated")
            log.info(json.dumps(TemplateObj, indent=4, sort_keys=True))
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to update the Template Dictionary Object: {}".format(str(e)), 'red')
            log.error("Error encountered attempting to update the Template Dictionary Object: {}".format(str(e)))
            sys.exit()
