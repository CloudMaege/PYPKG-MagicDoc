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
import os, sys, shutil, json

#####################
# Class Definition: #
#####################
class TFMagicDoc(object):
    """MagicDoc Terraform Documentation Class"""

    def __init__(self, log, path, exclude_dir=None, no_recursion=False):
        '''TFMagicDoc Class Constructor'''

        # Set class instantiation variables
        self._log = log
        self._path = path
        self._exclude_dir = exclude_dir
        self._no_recursion = no_recursion
        self._logtitle = "TFMagicDoc"

        # Set properties to hold result sets.
        self._files = {}
        self._variables = {}
        # self.outputs = None
        # self.graph = None

        # Set object files property setter by calling itself and passing a value.
        self.files = True

        # Terraform output collection var
        # self.tf_outputs = []

        # Terraform graph var
        # self.tf_graph = None
        # self.tf_graph_image = None


    ############################################
    # Construct Terraform File List:           #
    ############################################
    @property
    def files(self):
        """Getter for class property files method. This object property will return a list of files from the provided path that ends with either the .tf or .tfvar extentions"""
        self._log.info("{}: {}.files property requested".format(self._logtitle, self._logtitle))
        if self._files is None:
            self._log.write("Search resulted in 0 [*.tf, *.tfvar] files found in {}".format(self._path))
            sys.exit()
        else:
            return self._files

    @files.setter
    def files(self, init=True):
        """Setter for class property files method that iterates through a given file path and collects a list of terraform files."""
        # Instantiate the results object to hold the file search results.
        self._log.info("{}: {}.files refresh requested".format(self._logtitle, self._logtitle))
        self._log.info("{}: Exclude all sub-directories from search: {}".format(self._logtitle, str(self._no_recursion)))
        self._log.info("{}: Sub-directory to exclude from search: {}".format(self._logtitle, str(self._exclude_dir)))
        self._log.write("Scanning project directory for terraform .tf and .tfvar files...")
        file_search_results = {'list_tf_files': [], 'list_tfvar_files': []}
        try:
            self._log.debug("{}: Gathering list of all Terraform files ending in [.tf, .tfvars] file extensions from: {}".format(self._logtitle, self._path))
            for root, dirs, files in os.walk(self._path):
                self._log.debug("{}: Searching directory: {}".format(self._logtitle, self._path))
                # Strip the current directory designations
                file_search_path = root.replace(self._path, "")
                self._log.debug("{}: Setting file search path: {}".format(self._logtitle, file_search_path))
                for filename in files:
                    self._log.debug("{}: Checking file: {}".format(self._logtitle, filename))
                    if filename.endswith('.tf'):
                        if self._exclude_dir is not None and self._exclude_dir in filename:
                            self._log.debug("{}: Terraform .tf file: {} located in excluded subdirectory {}. [Skipping...]: {}".format(self._logtitle, filename, self._exclude_dir))
                            continue
                        self._log.debug("{}: Terraform .tf file match found: {}".format(self._logtitle, filename))
                        file_search_results.get('list_tf_files').append(os.path.join(file_search_path, filename))
                    elif filename.endswith('.tfvars'):
                        self._log.debug("{}: Terraform .tfvar file match found: {}".format(self._logtitle, filename))
                        file_search_results.get('list_tfvar_files').append(os.path.join(file_search_path, filename))
                # If recursion is set to false, then break, as the first pass gathers only the current directory.
                if self._no_recursion:
                    self._log.info("{}: Recursion disabled, only parsing parent directory results".format(self._logtitle))
                    break
            # If no results were found then don't set the files property attribute.
            if not bool(file_search_results.get('list_tf_files')) and not bool(file_search_results.get('list_tfvar_files')):
                self._log.info("{}: Search for [*.tf, *.tfvar] files in {} yielded no results.".format(self._logtitle, self._path))
            else:
                # Log and return the result list.
                self._log.info("{}: Search for [*.tf, *.tfvar] files from {} completed successfully!".format(self._logtitle, self._path))
                self._log.info("{}: {} .tf files found: {}".format(self._logtitle, len(file_search_results.get('list_tf_files')), file_search_results.get('list_tf_files')))
                self._log.info("{} {} .tfvar files found: {}".format(self._logtitle, len(file_search_results.get('list_tfvar_files')), file_search_results.get('list_tfvar_files')))
                self._log.debug("{}: Saving file search results to object".format(self._logtitle))
                self._log.debug(json.dumps(file_search_results, indent=4, sort_keys=True))
                self._files = file_search_results
        except Exception as e:
            self._log.error("Search for [*.tf, *.tfvar] files in {} failed!".format(self._path))
            self._log.error("Exception: {}".format(str(e)))
            sys.exit()


    ##############################################
    # Construct Terraform Module Variable Lists: #
    ##############################################
    @property
    def variables(self):
        """Getter for class property variables method. This object property will return a dictionary of variables from the provided file list."""
        self._log.info("{}: {}.variables property requested".format(self._logtitle, self._logtitle))
        if self._variables is None:
            self._log.write("Specified project has no variables or unable to gather variables from: {}".format(self._path))
            sys.exit()
        else:
            return self._variables


    @variables.setter
    def variables(self, include_examples):
        """
        Setter for class property variables method that iterates through the collected terraform files,
        locates any variables.tf files, parses the files, and returns a dict object of the collected file contents.
        
        Files will be ignored if found in a directory named 'example' or 'examples' unless the include_examples flag was set as true.
        """
        # Instantiate the results object to hold the variables search results.
        self._log.info("{}: {}.variables refresh requested".format(self._logtitle, self._logtitle))
        self._log.info("{}: Include example sub-directories in search: {}".format(self._logtitle, str(include_examples)))
        self._log.write("Scanning project directory for defined module variables...")
        self._log.write("")

        # Intantiate variable results dictionary object.
        variable_results = {'required_vars': [], 'required_vars_maxlength': 0, 'optional_vars': [], 'optional_vars_maxlength': 0}
        try:
            # Iterate through the project files and look for any files named variables.tf, if found, parse the files and construct an object for each variable that will be stored into the class dictionary object.
            log.info("Parsing terraform variable files.")
            self._log.debug("{}: Parsing terraform variable files. Ignoring files in 'example(s)' directory".format(self._logtitle))
            for tf_file in self.files.get('list_tf_files'):
                tf_filepath = os.path.join(self._path, tf_file)
                tf_filename = tf_file.lower()
                self._log.debug("{}: Scanning file: [{}]".format(self._logtitle, tf_file))
                # If example or exampes is in the file path, then exclude unless include all was passed true.
                if 'variables.tf' in tf_file:
                    if ('example' in tf_file or 'examples' in tf_file) and not include_examples:
                        self._log.debug("{}: {} located in example subdirectory. [Skipping file parse...]".format(self._logtitle, tf_file))
                        continue
                    # if a passed directory name was passed and its in the file path then exclude unless include all was passed true.
                    elif self._exclude_dir is not None and self._exclude_dir in tf_filename:
                        self._log.debug("{}: {} located in excluded directory: {}. [Skipping file parse...]".format(self._logtitle, self._exclude_dir))
                        continue
                    else:
                        self._log.debug("{}: Parsing file: [{}]".format(self._logtitle, tf_filepath))
                        try:
                            with open(tf_filepath, 'r') as f:
                                tf_variables = hcl.load(f)
                                self._log.debug("{}: Successfully loaded file: [{}]".format(self._logtitle, tf_filepath))
                        except Exception as e:
                            self._log.error("Failed to open: [{}]".format(tf_filepath))
                            self._log.error("Exception: {}".format(str(e)))
                        self._log.debug("{}: {} flagged for parsing!".format(self._logtitle, tf_file))
                        self._log.debug(json.dumps(tf_variables, indent=4, sort_keys=True))
                        # For each variable in the variables.tf file:
                        # Put the variable into either the required, or optional respective list based on the existence or absence of a default value.
                        self._log.info("{}: Parsing project variables defined in: {}.".format(self._logtitle, tf_filepath))

                        # Parse each variable and place into the result variable in expected format.
                        for k, v in tf_variables.get('variable').items():
                            if v.get('default') == None:
                                self._log.debug("{} Setting variable: {} as {}".format(self._logtitle, k, 'Required'))
                                # Check the variable name len and update maxlength, then create and store the variable object.
                                if len(k) > int(variable_results.get('required_vars_maxlength')):
                                    self._log.debug("{}: Var: {} length: {} is longer then {}... setting required variable offset to: {}".format(self._logtitle, k, len(k), variable_results.get('required_vars_maxlength'), len(k)))
                                    variable_results.update(required_vars_maxlength=len(k))
                                # Create the variable obj and add it to the result set object.
                                variable_results.get('required_vars').append({
                                    'name': k,
                                    'type': v.get('type', 'string'),
                                    'description': v.get('description', "No Description Provided"),
                                    'example_value': "Required Value"
                                })
                                self._log.debug("{}: Adding {} to required_vars list.".format(self._logtitle, k))
                            # If the variable has a default value, then it must be an optional.
                            else:
                                self._log.debug("{} Setting variable: {} as {}".format(self._logtitle, k, 'Optional'))
                                # Check the variable name len and update maxlength, then create and store the variable object.
                                if len(k) > int(variable_results.get('optional_vars_maxlength')):
                                    self._log.debug("{}: {} length: {} is longer then {}... setting optional variable offset to: {}".format(self._logtitle, k, len(k), variable_results.get('optional_vars_maxlength'), len(k)))
                                    variable_results.update(optional_vars_maxlength=len(k))
                                # Create the variable obj and add it to the result set object.
                                variable_results.get('optional_vars').append({
                                    'name': k,
                                    'type': v.get('type', 'string'),
                                    'description': v.get('description', "No Description Provided"),
                                    'default': v.get('default', "Example Value")
                                })
                                self._log.debug("{}: Adding {} to optional_vars list.".format(self._logtitle, k))
            # If no results were found then don't set the variables property attribute.
            if not bool(variable_results.get('required_vars')) and not bool(variable_results.get('optional_vars')):
                self._log.info("{}: Search for project variables files in {} yielded no results.".format(self._logtitle, tf_filepath))
            else:
                # Log and return the result list.
                self._log.debug(' ')
                self._log.info("{}: Variable list processing completed successfully.".format(self._logtitle))
                self._log.info("{}: {} Required variables identified".format(self._logtitle, len(variable_results.get('required_vars'))))
                self._log.info("{}: {} Optional variables identified".format(self._logtitle, len(variable_results.get('optional_vars'))))
                self._log.debug(json.dumps(variable_results.get('required_vars'), indent=4, sort_keys=True))
                self._log.debug(json.dumps(variable_results.get('optional_vars'), indent=4, sort_keys=True))
                self._log.debug("{}: Saving variable search results to object".format(self._logtitle))
                self._variables = variable_results
        except Exception as e:
            self._log.error("Terraform project variable parsing operation failed!")
            self._log.error("Exception: {}".format(str(e)))


    # ############################################
    # # Construct Terraform Module Output List:  #
    # ############################################
    # def build_outputs(self):
    #     '''Class method that iterates through the collected terraform files, and locates any outputs.tf files, parses the files, and returns a dict object of the collected file contents
        
    #     Files will be ignored if found in a directory named 'example'
    #     '''
    #     try:            
    #         # Iterate through the project files and look for any files named outputs.tf, if found, parse the files and construct an object for each output that will be stored into the class dictionary object.
    #         log.info("Parsing terraform output files. Ignoring 'example' files")
    #         for tf_file in self.tf_file_list:
    #             tf_file = tf_file.lower()
    #             if 'outputs.tf' in tf_file and 'example' not in tf_file:
    #                 log.debug("Parsing file: [{}]".format(tf_file))
    #                 try:
    #                     with open(tf_file, 'r') as outputs_file:
    #                         tf_outputs = hcl.load(outputs_file)
    #                 except:
    #                     log.error("Unable to open {}".format(tf_file))
    #                 log.debug("{} parsed successfully.".format(tf_file))
    #                 log.debug(json.dumps(tf_outputs, indent=4, sort_keys=True))
    #                 # Parse each output from the outputs.tf file and build a dict that can be sent to the doc template:
    #                 for k, v in tf_outputs.get('output').items():
    #                     # Create an output object and add it the self.tf_outputs list object.
    #                     self.tf_outputs.append({
    #                         'name': k,
    #                         'value': v.get('value')
    #                     })
    #                     # Log the output
    #                     log.debug("Added {} to tf_outputs list.".format(k))
    #         # Log all the things
    #         log.info("Output list processing completed:")
    #         log.info("{} outputs collected: {}".format(len(self.tf_outputs), self.tf_outputs))
    #     except Exception as e:
    #         log.error("Failed to construct terraform outputs list with exception: {}".format(str(e)))
    #     finally:
    #         return self.tf_outputs

# TODO:
    ##############################################
    # Construct Terraform Graph:                 #
    ##############################################
    # def build_graph(self):
    #     '''Class method that runs a terraform graph on the module source code and produces a dot style diagram.'''
    #     try:
    #         # Instantiate the TF Object
    #         tf = Terraform(working_dir=self._path)
            
    #         # Check to see if TF has been initialzed, and if not initialize it
    #         try:
    #             log.debug("Performing terraform init on {}".format(self._path))
    #             if not os.path.exists(os.path.join(self._path, ".terraform")):
    #                 tf.cmd('init')
    #         except Exception as e:
    #             log.error("Failed to perform terraform init execution on {} with exception: {}".format(self._path, str(e)))

    #         # Run a Terraform Graph action to generate the graph dot structure
    #         try:
    #             log.debug("Attempting to build terraform graph object...")
    #             tf_graph = tf.cmd('graph')
    #             self.tf_graph = tf_graph[1]
    #             log.debug("Terraform graph object creation completed successfully")
    #             log.debug(self.tf_graph)
    #         except Exception as e:
    #             log.error("Failed to perform terraform graph execution with exception: {}".format(str(e)))
    #     except Exception as e:
    #         log.error("Failed to build terraform graph object: {}".format(str(e)))


    # def render_graph_image(self):
    #     '''Class method to convert a terraform graph dot object to a png image, and save it in the provided path/images directory.'''
    #     graphviz_binary = shutil.which('dot')
    #     if graphviz_binary is not None:
    #         log.debug("Graphviz dot binary found in path {}".format(graphviz_binary))
    #         try:
    #             log.debug("Attempting to convert tf_graph object to png image...")
    #             # File Save Directory and Graph FileName values
    #             # TODO: Make this into a config variable
    #             tf_graph_file_basename = "tf_graph"
    #             image_dir = "images"
    #             image_dir_path = os.path.join(self._path, image_dir)
    #             log.debug("Image path ")

    #             # Make sure the Image Directory exists, if not then create it.
    #             try:
    #                 if not os.path.exists(image_dir_path):
    #                     log.info("{} directory not found, attempting to create directory".format(image_dir_path))
    #                     os.makedirs(image_dir_path)
    #             except Exception as e:
    #                 log.error("Failed to create directory {}: {}".format(image_dir_path, str(e)))

    #             try:
    #                 log.debug("Attempting to build terraform graph png from graph dot object...")
    #                 terraform_dot = Source(self.tf_graph, directory=image_dir_path, filename=tf_graph_file_basename, format='png')
    #                 terraform_dot.render()
    #                 self.tf_graph_image = "{}.png".format(os.path.join(image_dir, tf_graph_file_basename))
    #                 log.debug("Terraform graph image created successfully in path: {}".format(os.path.join(image_dir_path, tf_graph_file_basename)))
    #             except Exception as e:
    #                 log.error("Failed to render terraform graph image with exception: {}".format(str(e)))
    #         except Exception as e:
    #             log.error("Failed to create terraform graph image from the provided terraform graph object with exception: {}".format(str(e)))
    #         finally:
    #             return self.tf_graph_image
    #     else:
    #         log.warning("Terraform graph image render failed because the Graphviz dot executable was not found in the system path. Install the Graphviz dot binary to render the graph on future executions.")
