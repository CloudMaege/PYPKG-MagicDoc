##############################################################################
# CloudMage : MagicDoc Jinja Template Class
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Jinja Template Class
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
from jinja2 import Template, Environment, FileSystemLoader
from termcolor import colored, cprint

# Import MagicDoc Modules
from .utils import SplitPath

# Import Base Python Modules
import logging, json, os, sys

# Instantiate Logger
log = logging.getLogger('magicdoc.libs.jinja')


#####################
# Class Definition: #
#####################
class Jinja(object):
    """MagicDoc Jinja Loader Class"""

    def __init__(self, TemplateDir=None, Template=None, OutputDir="./", OutputFile=None):
        '''Jinja Loader Class Constructor'''
        try:
            # Set Templates Directory
            self.SetTemplateDir(TemplateDir)

            # Validate the provided template and set, or reset to default
            self.SetTemplate(os.path.join(Template))

            # Validate the provided output directory and set, or reset to default
            self.SetOutputDir(OutputDir)

            # Set the Outputfile to the provided filename. As it will be written, no need to currently validate its path.
            self.SetOutputFile(OutputFile)

            # Set the template loader options
            # TODO: Make these configurable in a future release.
            self.trim_blocks = True
            self.lstrip_blocks = True
            log.info("trim_blocks setting: {}".format(self.trim_blocks))
            log.info("lstrip_blocks setting: {}".format(self.lstrip_blocks))
        except Exception as e:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The expected {} template file was not found in the directory: {}.\n".format(self.template_dir, self.template), 'red')
            log.info("The expected {} template file was not found in the directory: {}.".format(self.template_dir, self.template))
            raise
            sys.exit()


    #############################################
    # Template Directory Getter/Setter Methods: #
    #############################################
    def SetTemplateDir(self, TemplateDir):
        """Class Method to set the Template Directory."""
        try:
            # If a custom template directory location isn't set, set the default path
            if TemplateDir is None:
                TemplatePath = os.path.dirname(os.path.abspath(__file__))
                self.template_dir = os.path.join(TemplatePath, 'templates')
            else:
                self.template_dir = TemplateDir
            log.info("Setting template directory to: {}....".format(self.template_dir))
        except Exception as e:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The provided template directory path: {} is not a valid path: {}.\n".format(self.template_dir), 'red')
            log.info("The provided template directory path: {} is not a valid path: {}.\n".format(self.template_dir))
            raise
            sys.exit()


    def GetTemplateDir(self):
        """Class Method to get the Template Directory."""
        return self.template_dir


    #############################################
    # Template Directory Getter/Setter Methods: #
    #############################################
    def SetTemplate(self, Template):
        """Class Method to set the Template required template."""
        try:
            if Template is not None:
                FilePath = os.path.join(self.template_dir, Template)
                if os.path.isfile(FilePath):
                    self.template = Template
                    log.info("Setting target template to: {}....".format(Template))
            else:
                self.template = None
                log.warning("The specified template does not exist, recheck the specified template path and try again. Template will remain configured to its default value: {}".format(self.template))
        except Exception as e:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The specified template: {} was not found in the template directory: {}.\n".format(self.template, self.template_dir), 'red')
            log.info("The specified template: {} was not found in the template directory: {}.\n".format(self.template, self.template_dir))
            raise
            sys.exit()



    def GetTemplate(self):
        """Class Method to get the currently set template."""
        return self.template


    #############################################
    # Destination Directory Path:                #
    #############################################
    def SetOutputDir(self, OutputDir):
        """Class Method to set the the output file path location of where the rendered template will be written."""
        try:
            if os.path.exists(OutputDir):
                log.info("Setting template render output directory to: {}....".format(OutputDir))
                self.output_dir = OutputDir
            else:
                self.output_dir = "./"
                log.warning("The specified rendered template output directory does not exist, recheck the provided output path and try again. Output directory will remain configured to its default location: {}".format(self.output_dir))
        except Exception as e:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The specified output directory path: {} is not a valid path: {}.\n".format(OutputDir), 'red')
            log.info("The specified output directory path: {} is not a valid path: {}.\n".format(OutputDir))
            raise
            sys.exit()


    def GetDestinationDir(self):
        """Class Method to return the currently configured output Directory."""
        return self.output_dir

    
    #############################################
    # Destination File Path:                    #
    #############################################
    def SetOutputFile(self, OutputFile):
        """Class Method to set the the output file path location of where the rendered template will be written."""
        log.info("Setting output file to {}/{}".format(self.output_dir, OutputFile))
        self.output_file = OutputFile


    def GetOutputFile(self):
        """Class Method to return the currently configured output File."""
        return self.output_file


    #############################################
    # Load Template:                            #
    #############################################
    def LoadTemplate(self, CustomTemplate=None):
        """Class Method to load all templates contained within the templates dir."""
        try:
            # If a custom template was specified, then set it, if not 
            if CustomTemplate is not None:
                if os.path.exists(CustomTemplate):
                    self.SetTemplate(CustomTemplate)
            
            # Load the configured templates.
            TplLoader = FileSystemLoader(self.template_dir)
            TemplateLib = Environment(loader=TplLoader, trim_blocks=self.trim_blocks, lstrip_blocks=self.lstrip_blocks)
            log.info("Loading Template: {}...".format(self.template))
            self.loaded_template = TemplateLib.get_template(self.template)
            log.info("Template {} successfully loaded.".format(self.template))
        except (OSError, IOError) as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to load jinja templates:\n\nException: {} NOT FOUND!\n".format(str(e)), 'red')
            log.error("Unable to load jinja template: {}".format(str(e)))
            raise
            sys.exit()

    
    def RenderTemplate(self, TemplateObj={}):
        """Class Method to render the specified template file."""
        try:
            log.info("Rendering Template: {}...".format(self.template))
            self.render_template = self.loaded_template.render(
                var=TemplateObj
            )
            log.info("{} rendered successfully!".format(self.loaded_template))
        except (OSError, IOError) as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to render {} template:\n\nException: {}\n".format(self.loaded_template, str(e)), 'red')
            log.error("Unexpected Error occurred attempting to render the {} template".format(self.loaded_template))
            log.error(str(e))
            raise
            sys.exit()

    
    def WriteTemplate(self, OutputDir=None, OutputFile=None, Overwrite=False):
        """Class Method to write the rendered template file to disk."""
        # Send output dir and output file to their respective setters.
        if OutputDir is not None:
            self.SetOutputDir(OutputDir)
        if OutputFile is not None:
            self.SetOutputFile(OutputFile)
        
        Output = os.path.join(self.output_dir, self.output_file)
        log.info('Output path set to: {}'.format(Output))

        if os.path.exists(Output) and not Overwrite:
            cprint("Configuration file already exists in the specified output path provided. Backup your file and re-run this command with the --overwrite flag to replace the existing config file.")
            sys.exit()
        
        if not os.path.exists(Output) or Overwrite:
            # Write the template to disk
            try:
                logging.info("Writing {} from rendered template...".format(Output))
                OutputFile = open(Output, "w")
                OutputFile.write(self.render_template)
                OutputFile.close()
                log.info("{} wrote successfully".format(self.template))
            except (OSError, IOError) as e:
                cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
                cprint("Error encountered attempting to write README.md file:\n\nException: {}\n".format(str(e)), 'red')
                log.error("Unexpected Error occurred attempting to write README.md file to the current directory.")
                log.error(str(e))
                raise
            sys.exit()
