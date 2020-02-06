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
from python_terraform import *
import hcl, yaml, requests
from graphviz import Source

# Import Base Python Modules
import os, shutil, logging

# Instantiate Logger
logging.basicConfig(format='%(asctime)-15s-%(levelname)s:    %(message)s', level=logging.DEBUG)
log = logging.getLogger()

#####################
# Class Definition: #
#####################
class TFDoc(object):
    """MagicDoc Terraform Documentation Class"""

    def __init__(self, path, no_recursion):
        '''TFDoc Class Constructor'''

        # Set class variables
        self.path = path
        self.no_recursion = no_recursion

        # File collection vars (Dictionary is only for direct method call return)
        self.tf_files = {}
        self.tf_file_list = []
        self.tfvars_file_list = []

        # Terraform variable collection vars
        self.tf_variables = {
            'required_vars': [],
            'optional_vars': [],
            'required_vars_maxlength': 0,
            'optional_vars_maxlength': 0
        }

        # Terraform output collection var
        self.tf_outputs = []

        # Terraform graph var
        self.tf_graph = None
        self.tf_graph_image = None

        # Execute the Class methods to populate the class attributes.
        self.file_search()
        # self.build_variables()
        # self.build_outputs()
        # self.build_graph()
        # self.render_graph_image()

    ############################################
    # Construct Terraform File List:           #
    ############################################
    def file_search(self):
        '''Class method that iterates through a given file path and collects a list of terraform files.'''
        try:
            log.debug("Gathering list of all Terraform files ending in the [.tf, .tfvars] file extensions from: {}".format(self.path))
            for root, dirs, files in os.walk(self.path):
                # Strip the current directory designations
                filepath = root.replace(self.path, "")
                for filename in files:
                    if filename.endswith('.tf'):
                        self.tf_file_list.append(os.path.join(filepath, filename))
                    elif filename.endswith('.tfvars'):
                        self.tfvars_file_list.append(os.path.join(filepath, filename))
                # If recursion is set to false, then break, as the first pass gathers only the current directory.
                if self.no_recursion:
                    break
            self.tf_files.update(tf_files=self.tf_file_list, tfvar_files=self.tfvars_file_list)
            # Log and return the result list.
            log.debug("File lists have been collected successfully!")
            log.debug("{} .tf files collected: {}".format(len(self.tf_file_list), self.tf_file_list))
            log.debug("{} .tfvar files collected: {}".format(len(self.tf_file_list), self.tfvars_file_list))
        except Exception as e:
            log.error("Failed to collect terraform files from {} with exception: {}".format(str(e)))
        finally:
            return self.tf_files


    ################################################
    # Set Required and Optional max length values: #
    ################################################
    def set_required_maxlength(self, value):
        '''Class method that will simply check to see if the passed value is greater then the currently set required_vars_maxlength. If the passed value is higher, it will update the self.tf_variables key.'''
        try:
            if len(value) > self.tf_variables.get('required_vars_maxlength'):
                self.tf_variables.update(required_vars_maxlength=value)
        except Exception as e:
            log.error("Failed to update required_vars_maxlength with exception: {}".format(str(e)))


    def set_optional_maxlength(self, value):
        '''Class method that will simply check to see if the passed value is greater then the currently set optional_vars_maxlength. If the passed value is higher, it will update the self.tf_variables key.'''
        try:
            if len(value) > self.tf_variables.get('optional_vars_maxlength'):
                self.tf_variables.update(optional_vars_maxlength=value)
        except Exception as e:
            log.error("Failed to update optional_vars_maxlength with exception: {}".format(str(e)))


    ##############################################
    # Construct Terraform Module Variable Lists: #
    ##############################################
    def build_variables(self):
        '''Class method that iterates through the collected terraform files, and locates any variables.tf files, parses the files, and returns a dict object of the collected file contents.
        
        Files will be ignored if found in a directory named 'example'
        '''
        try:
            # Iterate through the project files and look for any files named variables.tf, if found, parse the files and construct an object for each variable that will be stored into the class dictionary object.
            log.info("Parsing terraform variable files. Ignoring 'example' files")
            for tf_file in self.tf_file_list:
                tf_file = tf_file.lower()
                if 'variables.tf' in tf_file and 'example' not in tf_file:
                    log.debug("Parsing file: [{}]".format(tf_file))
                    try:
                        with open(tf_file, 'r') as variables_file:
                            tf_variables = hcl.load(variables_file)
                    except:
                        log.error("Unable to open {}".format(tf_file))
                    log.debug("{} parsed successfully.".format(tf_file))
                    log.debug(json.dumps(tf_variables, indent=4, sort_keys=True))
                    # For each variable in the variables.tf file:
                    # Put the variable into either the required, or optional respective list based on the existence or absence of a default value.
                    log.debug("Parsing project variables..")
                    for k, v in tf_variables.get('variable').items():
                        if v.get('default') == None:
                            # Check the variable name len and update maxlength, then create and store the variable object.
                            self.set_optional_maxlength(len(k))
                            self.tf_variables.get('required_vars').append({
                                'name': k,
                                'type': v.get('type', 'No Type Defined'),
                                'description': v.get('description', "No Description Provided"),
                                'example_value': "Required Value"
                            })
                            log.debug("Added {} to required_vars list.".format(k))
                        # If the variable has a default value, then it must be an optional.
                        else:
                            # Check the variable name len and update maxlength, then create and store the variable object.
                            self.set_required_maxlength(len(k))
                            self.tf_variables.get('optional_vars').append({
                                'name': k,
                                'type': v.get('type', 'No Type Defined'),
                                'description': v.get('description', "No Description Provided"),
                                'default': v.get('default', "Example Value")
                            })
                            log.debug("Added {} to optional_vars list.".format(k))
            # Log and return the results.
            log.debug("Variable list processing completed:")
            log.debug("{} Required variables collected: {}".format(len(self.tf_variables.get('required_vars')), self.tf_variables.get('required_vars')))
            log.debug("Longest required variable length: {}".format(self.tf_variables.get('required_vars_maxlength')))
            log.debug("{} Optional variables collected: {}".format(len(self.tf_variables.get('optional_vars')), self.tf_variables.get('optional_vars')))
            log.debug("Longest optional variable length: {}".format(self.tf_variables.get('optional_vars_maxlength')))
        except Exception as e:
            log.error("Failed to construct terraform variables list with exception: {}".format(str(e)))
        finally:
            return self.tf_variables


    ############################################
    # Construct Terraform Module Output List:  #
    ############################################
    def build_outputs(self):
        '''Class method that iterates through the collected terraform files, and locates any outputs.tf files, parses the files, and returns a dict object of the collected file contents
        
        Files will be ignored if found in a directory named 'example'
        '''
        try:            
            # Iterate through the project files and look for any files named outputs.tf, if found, parse the files and construct an object for each output that will be stored into the class dictionary object.
            log.info("Parsing terraform output files. Ignoring 'example' files")
            for tf_file in self.tf_file_list:
                tf_file = tf_file.lower()
                if 'outputs.tf' in tf_file and 'example' not in tf_file:
                    log.debug("Parsing file: [{}]".format(tf_file))
                    try:
                        with open(tf_file, 'r') as outputs_file:
                            tf_outputs = hcl.load(outputs_file)
                    except:
                        log.error("Unable to open {}".format(tf_file))
                    log.debug("{} parsed successfully.".format(tf_file))
                    log.debug(json.dumps(tf_outputs, indent=4, sort_keys=True))
                    # Parse each output from the outputs.tf file and build a dict that can be sent to the doc template:
                    for k, v in tf_outputs.get('output').items():
                        # Create an output object and add it the self.tf_outputs list object.
                        self.tf_outputs.append({
                            'name': k,
                            'value': v.get('value')
                        })
                        # Log the output
                        log.debug("Added {} to tf_outputs list.".format(k))
            # Log all the things
            log.info("Output list processing completed:")
            log.info("{} outputs collected: {}".format(len(self.tf_outputs), self.tf_outputs))
        except Exception as e:
            log.error("Failed to construct terraform outputs list with exception: {}".format(str(e)))
        finally:
            return self.tf_outputs

# TODO:
    ##############################################
    # Construct Terraform Graph:                 #
    ##############################################
    def build_graph(self):
        '''Class method that runs a terraform graph on the module source code and produces a dot style diagram.'''
        try:
            # Instantiate the TF Object
            tf = Terraform(working_dir=self.path)
            
            # Check to see if TF has been initialzed, and if not initialize it
            try:
                log.debug("Performing terraform init on {}".format(self.path))
                if not os.path.exists(os.path.join(self.path, ".terraform")):
                    tf.cmd('init')
            except Exception as e:
                log.error("Failed to perform terraform init execution on {} with exception: {}".format(self.path, str(e)))

            # Run a Terraform Graph action to generate the graph dot structure
            try:
                log.debug("Attempting to build terraform graph object...")
                tf_graph = tf.cmd('graph')
                self.tf_graph = tf_graph[1]
                log.debug("Terraform graph object creation completed successfully")
                log.debug(self.tf_graph)
            except Exception as e:
                log.error("Failed to perform terraform graph execution with exception: {}".format(str(e)))
        except Exception as e:
            log.error("Failed to build terraform graph object: {}".format(str(e)))


    def render_graph_image(self):
        '''Class method to convert a terraform graph dot object to a png image, and save it in the provided path/images directory.'''
        graphviz_binary = shutil.which('dot')
        if graphviz_binary is not None:
            log.debug("Graphviz dot binary found in path {}".format(graphviz_binary))
            try:
                log.debug("Attempting to convert tf_graph object to png image...")
                # File Save Directory and Graph FileName values
                # TODO: Make this into a config variable
                tf_graph_file_basename = "tf_graph"
                image_dir = "images"
                image_dir_path = os.path.join(self.path, image_dir)
                log.debug("Image path ")

                # Make sure the Image Directory exists, if not then create it.
                try:
                    if not os.path.exists(image_dir_path):
                        log.info("{} directory not found, attempting to create directory".format(image_dir_path))
                        os.makedirs(image_dir_path)
                except Exception as e:
                    log.error("Failed to create directory {}: {}".format(image_dir_path, str(e)))

                try:
                    log.debug("Attempting to build terraform graph png from graph dot object...")
                    terraform_dot = Source(self.tf_graph, directory=image_dir_path, filename=tf_graph_file_basename, format='png')
                    terraform_dot.render()
                    self.tf_graph_image = "{}.png".format(os.path.join(image_dir, tf_graph_file_basename))
                    log.debug("Terraform graph image created successfully in path: {}".format(os.path.join(image_dir_path, tf_graph_file_basename)))
                except Exception as e:
                    log.error("Failed to render terraform graph image with exception: {}".format(str(e)))
            except Exception as e:
                log.error("Failed to create terraform graph image from the provided terraform graph object with exception: {}".format(str(e)))
            finally:
                return self.tf_graph_image
        else:
            log.warning("Terraform graph image render failed because the Graphviz dot executable was not found in the system path. Install the Graphviz dot binary to render the graph on future executions.")
