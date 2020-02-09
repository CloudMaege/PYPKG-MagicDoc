##############################################################################
# CloudMage : MagicDoc Terraform Docs Class
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
import os, sys, shutil, json, inspect

#####################
# Class Definition: #
#####################
class TFMagicDoc(object):
    """MagicDoc Terraform Documentation Class"""


    def __init__(self, log, path, exclude_dir=None, config=None, no_recursion=False):
        '''TFMagicDoc Class Constructor'''

        # Set class instantiation variables
        self._log = log
        self._path = path
        self._exclude_dir = exclude_dir
        self._config_file = config
        self._config = {}
        self._no_recursion = no_recursion
        self._log_context = "CLS->TFMagicDoc"

        # Set properties to hold result sets.
        self._files = {}
        self._variables = {}
        self._outputs = []
        self._graph = None
        self._graph_image = None

        # Set dependency binary checks
        self._terraform_binary = shutil.which('terraform')
        self._graphviz_dot_binary = shutil.which('dot')

        # Set properties to track terraform command execution and object state.
        # Terraform Object
        self._terraform = None
        # Terraform Init State. If this instance created the init, then this will be set, otherwise it will be left to none.
        self._terraform_init_executed = None

        # Set object files property setter by calling itself and passing a value.
        # Load Config if available
        if self._config_file is not None and self._config_file.endswith(('.yaml', '.yml')) and os.path.exists(os.path.join(self._path, self._config_file)):
            self.config = True
        # Execute Files Setter, this object is needed for all other setters, and so should be ran at the time of instance instantiation.
        self.files = True


    ############################################
    # Load Project Documentation Config File:  #
    ############################################
    @property
    def config(self):
        """Getter for class property config method. This object property will return the project config.yaml file from the workdir if found. This config holds additional details used in building the documentation."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._config is not None and isinstance(self._config, dict) and bool(self._config):
            return self._config
        else:
            self._log.write("MagicDoc config file not found in {}".format(self._path), 'yellow')
            self._log.write("A properly formatted project config can be created using the `magicdoc tf config init` command.", 'yellow')
            return None


    @config.setter
    def config(self, init=False):
        """Setter for class property config method that will capture the provided config file, parse it, and construct the config dictionary object."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        if self._config_file is not None and init:
            # Instantiate the results object to hold the parsed config file.
            self._log.info("{}: {}.config load requested".format(log_msg, log_msg))
            self._log.info("{}: Config file: {}".format(log_msg, str(os.path.join(self._path, self._config_file))))
            try:
                if os.path.exists(os.path.join(self._path, self._config_file)):
                    self._log.debug("{}: Config file: {} found in project directory! Attempting to load:".format(log_msg, self._config_file))
                    if self._config_file.endswith(('.yaml', '.yml')):
                        self._log.debug("{}: Config file {} passed file type check. File extention match: [*.yaml, *.yml], Processing file".format(log_msg, self._config_file))
                        self._log.write("Loading terraform project config file: {}".format(os.path.join(self._path, self._config_file)))
                        # Attempt to open the file, err on exception
                        try:
                            with open(os.path.join(self._path, self._config_file)) as f:
                                self._config = yaml.load(f, Loader=yaml.FullLoader)
                                self._log.info("{}: Config file loaded successfully from given file path: {}.".format(log_msg, os.path.join(self._config_file, self._path)))
                                self._log.debug(json.dumps(self._config, indent=4, sort_keys=True))
                        except Exception as e:
                            self._log.error("Failed to open: [{}]".format(tf_filepath))
                            self._log.error("Exception: {}".format(str(e)))
                    else:
                        self._log.error("File: {} does not appear to have the required .yaml or .yml extention.".format(self._config_file))
                        self._log.error("The requested operation will continue, however config data will not be un-available.")
                        self._log.write("A properly formatted project config can be created using the `magicdoc tf config init` command.", 'yellow')
                        pass
                else:
                    self._log.error("File: {} does not exist in the project directory: {}".format(self._config_file, self._path))
                    self._log.error("The requested operation will continue, however config data will not be un-available.")
                    self._log.write("A properly formatted project config can be created using the `magicdoc tf config init` command.", 'yellow')
                    pass
            except Exception as e:
                self._log.error("Request to load project config file in {} failed!".format(self._path))
                self._log.error("Exception: {}".format(str(e)))
                self._log.error("The requested operation will continue, however config data will not be un-available.")
                self._log.write("A properly formatted project config can be created using the `magicdoc tf config init` command.", 'yellow')
                pass
        self._log.debug("{}: Config file not found in project directory or is of invalid type: {}".format(log_msg, self._config_file))


    ############################################
    # Construct Terraform File List:           #
    ############################################
    @property
    def files(self):
        """Getter for class property files method. This object property will return a list of files from the provided path that ends with either the .tf or .tfvar extentions"""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._files is None:
            self._log.write("Search resulted in 0 [*.tf, *.tfvar] files found in {}".format(self._path))
            sys.exit()
        else:
            return self._files


    @files.setter
    def files(self, init=True):
        """Setter for class property files method that iterates through a given file path and collects a list of terraform files. This method will also ignore files that start with .terraform."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        # Instantiate the results object to hold the file search results.
        self._log.info("{}: Refresh requested".format(log_msg))
        self._log.info("{}: Exclude all sub-directories from search: {}".format(log_msg, str(self._no_recursion)))
        self._log.info("{}: Sub-directory to exclude from search: {}".format(log_msg, str(self._exclude_dir)))
        self._log.write("Scanning project directory for terraform .tf and .tfvar files...")
        file_search_results = {'list_tf_files': [], 'list_tfvar_files': []}
        try:
            self._log.debug("{}: Gathering list of all Terraform files ending in [.tf, .tfvars] file extensions from: {}".format(log_msg, self._path))
            for root, dirs, files in os.walk(self._path):
                self._log.debug("{}: Searching directory: {}".format(log_msg, self._path))
                # Strip the current directory designations
                file_search_path = root.replace(self._path, "")
                self._log.debug("{}: Setting file search path: {}".format(log_msg, file_search_path))
                for filename in files:
                    self._log.debug("{}: Checking file: {}".format(log_msg, filename))
                    if filename.endswith('.tf') and not filename.startswith('.terraform'):
                        if self._exclude_dir is not None and self._exclude_dir in filename:
                            self._log.debug("{}: Terraform .tf file: {} located in excluded subdirectory {}. [Skipping...]: {}".format(log_msg, filename, self._exclude_dir))
                            continue
                        self._log.debug("{}: Terraform .tf file match found: {}".format(log_msg, filename))
                        file_search_results.get('list_tf_files').append(os.path.join(file_search_path, filename))
                    elif filename.endswith('.tfvars') and not filename.startswith('.terraform'):
                        self._log.debug("{}: Terraform .tfvar file match found: {}".format(log_msg, filename))
                        file_search_results.get('list_tfvar_files').append(os.path.join(file_search_path, filename))
                # If recursion is set to false, then break, as the first pass gathers only the current directory.
                if self._no_recursion:
                    self._log.info("{}: Recursion disabled, only parsing parent directory results".format(log_msg))
                    break
            # If no results were found then don't set the files property attribute.
            if not bool(file_search_results.get('list_tf_files')) and not bool(file_search_results.get('list_tfvar_files')):
                self._log.info("{}: Search for [*.tf, *.tfvar] files in {} yielded no results.".format(log_msg, self._path))
            else:
                # Log and return the result list.
                self._log.info("{}: Search for [*.tf, *.tfvar] files from {} completed successfully!".format(log_msg, self._path))
                self._log.info("{}: {} .tf files found: {}".format(log_msg, len(file_search_results.get('list_tf_files')), file_search_results.get('list_tf_files')))
                self._log.info("{} {} .tfvar files found: {}".format(log_msg, len(file_search_results.get('list_tfvar_files')), file_search_results.get('list_tfvar_files')))
                self._log.debug("{}: Saving file search results to object".format(log_msg))
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
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
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
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Refresh requested".format(log_msg))
        self._log.info("{}: Include example sub-directories in search: {}".format(log_msg, str(include_examples)))
        self._log.write("Scanning project directory for defined module variables...")
        self._log.write("")

        # Intantiate variable results dictionary object.
        variable_results = {'required_vars': [], 'required_vars_maxlength': 0, 'optional_vars': [], 'optional_vars_maxlength': 0}
        try:
            # Iterate through the project files and look for any files named variables.tf, if found, parse the files and construct an object for each variable that will be stored into the class dictionary object.
            self._log.info("{}: Parsing terraform variable files.".format(log_msg))
            for tf_file in self.files.get('list_tf_files'):
                tf_filepath = os.path.join(self._path, tf_file)
                tf_filename = tf_file.lower()
                self._log.debug("{}: Scanning file: [{}]".format(log_msg, tf_file))
                # If example or exampes is in the file path, then exclude unless include all was passed true.
                if 'variables.tf' in tf_file:
                    if ('example' in tf_file or 'examples' in tf_file) and not include_examples:
                        self._log.debug("{}: {} located in example subdirectory. [Skipping file parse...]".format(log_msg, tf_file))
                        continue
                    # if a passed exclude directory name was passed and its in the file path then exclude unless include all was passed true.
                    elif self._exclude_dir is not None and self._exclude_dir in tf_filename:
                        self._log.debug("{}: {} located in excluded directory: {}. [Skipping file parse...]".format(log_msg, self._exclude_dir))
                        continue
                    else:
                        self._log.debug("{}: Parsing file: [{}]".format(log_msg, tf_filepath))
                        try:
                            with open(tf_filepath, 'r') as f:
                                tf_variables = hcl.load(f)
                                self._log.debug("{}: Successfully loaded file: [{}]".format(log_msg, tf_filepath))
                        except Exception as e:
                            self._log.error("Failed to open: [{}]".format(tf_filepath))
                            self._log.error("Exception: {}".format(str(e)))
                        self._log.debug("{}: {} flagged for parsing!".format(log_msg, tf_file))
                        self._log.debug(json.dumps(tf_variables, indent=4, sort_keys=True))
                        # For each variable in the variables.tf file:
                        # Put the variable into either the required, or optional respective list based on the existence or absence of a default value.
                        self._log.info("{}: Parsing project variables defined in: {}.".format(log_msg, tf_filepath))

                        # Parse each variable and place into the result variable in expected format.
                        for k, v in tf_variables.get('variable').items():
                            if v.get('default') == None:
                                self._log.debug("{} Setting variable: {} as {}".format(log_msg, k, 'Required'))
                                # Check the variable name len and update maxlength, then create and store the variable object.
                                if len(k) > int(variable_results.get('required_vars_maxlength')):
                                    self._log.debug("{}: Var: {} length: {} is longer then {}... setting required variable offset to: {}".format(log_msg, k, len(k), variable_results.get('required_vars_maxlength'), len(k)))
                                    variable_results.update(required_vars_maxlength=len(k))
                                # Create the variable obj and add it to the result set object.
                                variable_results.get('required_vars').append({
                                    'name': k,
                                    'type': v.get('type', 'string'),
                                    'description': v.get('description', "No Description Provided"),
                                    'example_value': "Required Value",
                                    'general_details': {'description': v.get('description', "No Description Provided"), 'notes': [], 'images':[]},
                                    'variable_details': {'description': "", 'notes': [], 'images':[]},
                                    'usage_details': {'description': "", 'notes': [], 'images':[]},
                                    'additional': {'description': "", 'notes': [], 'images':[]}
                                })
                                self._log.debug("{}: Adding {} to required_vars list.".format(log_msg, k))
                            # If the variable has a default value, then it must be an optional.
                            else:
                                self._log.debug("{} Setting variable: {} as {}".format(log_msg, k, 'Optional'))
                                # Check the variable name len and update maxlength, then create and store the variable object.
                                if len(k) > int(variable_results.get('optional_vars_maxlength')):
                                    self._log.debug("{}: {} length: {} is longer then {}... setting optional variable offset to: {}".format(log_msg, k, len(k), variable_results.get('optional_vars_maxlength'), len(k)))
                                    variable_results.update(optional_vars_maxlength=len(k))
                                # Create the variable obj and add it to the result set object.
                                variable_results.get('optional_vars').append({
                                    'name': k,
                                    'type': v.get('type', 'string'),
                                    'description': v.get('description', "No Description Provided"),
                                    'default': v.get('default', "Example Value"),
                                    'general_details': {'description': v.get('description', "No Description Provided"), 'notes': [], 'images':[]},
                                    'variable_details': {'description': "", 'notes': [], 'images':[]},
                                    'usage_details': {'description': "", 'notes': [], 'images':[]},
                                    'additional': {'description': "", 'notes': [], 'images':[]}
                                })
                                self._log.debug("{}: Adding {} to optional_vars list.".format(log_msg, k))
            # If no results were found then don't set the variables property attribute.
            if not bool(variable_results.get('required_vars')) and not bool(variable_results.get('optional_vars')):
                self._log.info("{}: Search for project variables files in {} yielded no results.".format(log_msg, tf_filepath))
            else:
                # Log and return the result list.
                self._log.debug(' ')
                self._log.info("{}: Variable list processing completed successfully.".format(log_msg))
                self._log.info("{}: {} Required variables identified".format(log_msg, len(variable_results.get('required_vars'))))
                self._log.info("{}: {} Optional variables identified".format(log_msg, len(variable_results.get('optional_vars'))))
                self._log.debug(json.dumps(variable_results.get('required_vars'), indent=4, sort_keys=True))
                self._log.debug(json.dumps(variable_results.get('optional_vars'), indent=4, sort_keys=True))
                self._log.debug("{}: Saving variable search results to object".format(log_msg))
                self._variables = variable_results
        except Exception as e:
            self._log.error("Terraform project variable parsing operation failed!")
            self._log.error("Exception: {}".format(str(e)))
            sys.exit()


    ############################################
    # Construct Terraform Module Output List:  #
    ############################################
    @property
    def outputs(self):
        """Getter for class property outputs method. This object property will return a dictionary of outputs from the provided file list."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._outputs is None:
            self._log.write("Specified project has no outputs or unable to gather outputs from: {}".format(self._path))
            sys.exit()
        else:
            return self._outputs


    @outputs.setter
    def outputs(self, include_examples):
        """
        Setter for class property outputs method that iterates through the collected terraform files,
        locates any outputs.tf files, parses the files, and returns a dict object of the collected file contents.
        
        Files will be ignored if found in a directory named 'example' or 'examples' unless the include_examples flag was set as true.
        """
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        # Instantiate the results object to hold the outputs search results.
        self._log.info("{}: Refresh requested".format(log_msg))
        self._log.info("{}: Include example sub-directories in search: {}".format(log_msg, str(include_examples)))
        self._log.write("Scanning project directory for defined module outputs...")
        self._log.write("")

        # Intantiate outputs results dictionary object.
        outputs_results = []
        try:
            self._log.info("{}: Parsing terraform output files.".format(log_msg))
            for tf_file in self.files.get('list_tf_files'):
                tf_filepath = os.path.join(self._path, tf_file)
                tf_filename = tf_file.lower()
                self._log.debug("{}: Scanning file: [{}]".format(log_msg, tf_file))
                # If example or exampes is in the file path, then exclude unless include all was passed true.
                if 'outputs.tf' in tf_file:
                    if ('example' in tf_file or 'examples' in tf_file) and not include_examples:
                        self._log.debug("{}: {} located in example subdirectory. [Skipping file parse...]".format(log_msg, tf_file))
                        continue
                    # if a passed exclude directory name was passed and its in the file path then exclude unless include all was passed true.
                    elif self._exclude_dir is not None and self._exclude_dir in tf_filename:
                        self._log.debug("{}: {} located in excluded directory: {}. [Skipping file parse...]".format(log_msg, self._exclude_dir))
                        continue
                    else:
                        self._log.debug("{}: Parsing file: [{}]".format(log_msg, tf_filepath))
                        try:
                            with open(tf_filepath, 'r') as f:
                                tf_outputs = hcl.load(f)
                                self._log.debug("{}: Successfully loaded file: [{}]".format(log_msg, tf_filepath))
                        except Exception as e:
                            self._log.error("Failed to open: [{}]".format(tf_filepath))
                            self._log.error("Exception: {}".format(str(e)))
                        self._log.debug("{}: {} flagged for parsing!".format(log_msg, tf_file))
                        self._log.debug(json.dumps(tf_outputs, indent=4, sort_keys=True))
                        # For each output in the outputs.tf file:
                        self._log.info("{}: Parsing project outputs defined in: {}.".format(log_msg, tf_filepath))
                        # Parse each output and place into the result variable in expected format.
                        for k, v in tf_outputs.get('output').items():
                            # Create an output object and add it the self.tf_outputs list object.
                            self._log.debug("{} Parsing output: {} with value: {}".format(log_msg, k, v.get('value', "")))
                            outputs_results.append({
                                'name': k,
                                'value': v.get('value')
                            })
                            self._log.debug("{}: Adding {} to outputs list.".format(log_msg, k))
            # If no results were found then don't set the variables property attribute.
            if not bool(outputs_results) or len(outputs_results) == 0:
                self._log.info("{}: Search for project output files in {} yielded no results.".format(log_msg, tf_filepath))
            else:
                # Log and return the result list.
                self._log.debug(' ')
                self._log.info("{}: Output list processing completed successfully.".format(log_msg))
                self._log.info("{}: {} Outputs identified".format(log_msg, len(outputs_results)))
                self._log.debug(outputs_results)
                self._log.debug("{}: Saving output search results to object".format(log_msg))
                self._outputs = outputs_results
        except Exception as e:
            self._log.error("Terraform project output parsing operation failed!")
            self._log.error("Exception: {}".format(str(e)))
            sys.exit()


    ##############################################
    # Construct Terraform Graph:                 #
    ##############################################
    @property
    def graph(self):
        """Getter for class property graph method. This object property will return a terraform graph dot definition if one was able to be generated."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._graph is None:
            self._log.write("Specified project was unable to generate a graph object from: {}".format(self._path))
            return None
        else:
            self._log.info(self._graph)
            return self._graph


    @graph.setter
    def graph(self, overwrite=False):
        """
        Setter for class property graph method that will run a terraform init on the targeted directory, and then use that init environment to
        generate a dot graph definition that can later be rendered for the use.
        """
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        # Instantiate the results object to hold the outputs search results.
        self._log.info("{}: Refresh requested".format(log_msg))
        self._log.info("{}: Overwrite Existing Init: {}".format(log_msg, overwrite))
        self._log.info("")
        # Intantiate outputs results dictionary object.
        graph_results = []
        try: 
            # Call the Terraform init method
            self.terraform_init(overwrite)

            # Run a Terraform Graph action to generate the graph dot structure
            try:
                self._log.debug("{}: Attempting to generate `terraform graph` dot structure in target project directory: {}".format(log_msg, self._path))
                if self._terraform is not None:
                    self._log.debug("{}.graph current value: {}".format(log_msg, self._graph))
                    self._log.debug("{}: Executing `terraform graph` in target project directory: {}".format(log_msg, self._path))
                    graph_results = self._terraform.cmd('graph')
                    self._graph = graph_results[1]
                    self._log.debug("{}: Terraform graph dot structure object was created successfully!".format(log_msg))
                    self._log.debug(self._graph)
                    self._log.debug("")
            except Exception as e:
                log.warning("Failed to perform `terraform graph` execution on the target project directory: {}".format(self._path))
                log.warning("{}".format(str(e)))

            # TODO: Move this to its own method!!!
            # If this method executed the terraform init then clean up the .terraform directory.
            if self._terraform_init_executed is not None and self._terraform_init_executed:
                self.terraform_init_cleanup(self._terraform_init_executed)
        except Exception as e:
            log.warning("Failed to generate terraform graph structure object on target project directory: {}".format(self._path))
            log.warning("{}".format(str(e)))


    # def render_graph_image(self):
    #     '''Class method to convert a terraform graph dot object to a png image, and save it in the provided path/images directory.'''
    # # Define this function for logging
    #   this = inspect.stack()[0][3]
    #   log_msg = "{}.{}".format(self._log_context, this)    
    #   graphviz_binary = shutil.which('dot')
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


    ##############################################
    # Instantiate Terraform Object:              #
    ##############################################
    def _terraform_instance(self):
        """Class method that creates a terraform object that can be used to perform actions against the target project directory using terraform."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        # Instantiate the TF Object
        self._log.info("{}: Terraform object instantiation requested!".format(log_msg))
        if self._terraform is None:
            self._log.debug("{}: Attempting to instantiate Terraform object instance against the project directory: {}".format(log_msg, self._path))
            try:
                self._terraform = Terraform(working_dir=self._path)
                self._log.debug("{}: Terraform Object instantiation completed successfully: {}".format(log_msg))
                self._log.debug("")
            except Exception as e:
                log.warning("Attempt to instantiate a terraform object in the target directory failed.")
                log.warning("Exception: {}".format(str(e)))
        else:
            self._log.debug("{}: Existing Terraform object already exists... [Skipping...]: {}".format(log_msg))

    
    #########################################################
    # Perform Terraform Init Execution and Cleanup Methods: #
    #########################################################
    def terraform_init(self, overwrite=False):
        """Class method that performs a terraform init on the working directory.
        If an existing .terraform directory exists then overwrite must be set to True in order to refresh the init, otherwise, the
        init will be skipped.
        """
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Terraform init action requested!".format(log_msg))
        self._log.debug("{}: Overwrite existing init: {}".format(log_msg, overwrite))
        self._log.debug("{}: Terraform Binary Installed: {}".format(log_msg, self._terraform_binary))
        # Call this instances object creation method. If an object is already set, then the method will use the existing object.
        self._terraform_instance()
        try:
            if self._terraform_binary is not None:
                if self._terraform is not None:
                    self._log.debug("{}: Attempting to run `terraform init` on the target project directory: {}".format(log_msg, self._path))
                    # TODO: Need to check if this will reflect new changes or if an existing .terraform directory should be removed and recreated..
                    # TODO: If the finding is that the directory should be removed, then need to be state file aware to ensure that if local state
                    # is being used that the state is not removed, altered or affected by this at all. Default location of the state file is located
                    # in terraform.tfstate so just need to exact match .terraform and not do a like terraform when removing the directory.
                    init_exists = True if os.path.exists(os.path.join(self._path, '.terraform')) else False
                    if not init_exists or (init_exists and overwrite):
                        if init_exists:
                            self._log.debug("{}: A directory named .terraform already exists in the target project directory... Overwrite requested...: {}".format(log_msg))
                        else:
                            self._log.debug("{}: Search for .terraform directory in the target project path yielded no results. One will be created...".format(log_msg))
                        self._log.write("{}: Executing `terraform init` on target project directory: {}".format(log_msg, self._path), 'yellow')
                        return_code, stdout, stderr = self._terraform.cmd('init', capture_output=False)
                        self._log.write("{}: Execution of `terraform init` completed successfully against the target directory: {}".format(log_msg, self._path), 'yellow')
                        self._terraform_init_executed = True
                    else:
                        self._log.debug("{}: Project directory already contains a .terraform directory and Overwrite set to: {}. Aborting the init!".format(log_msg, overwrite))
                else:
                    self._log.warning("A valid terraform instance could not be found. Terraform Init operation cannot proceed.")
            else:
                self._log.write("{}: Terraform does not appear to be installed in this environment. Terraform Init operation cannot proceed.".format(log_msg))
                self._log.write("{}: Terraform can be downloaded from https://www.terraform.io/downloads.html.".format(log_msg))
        except Exception as e:
            log.warning("Failed to perform `terraform init` execution on the target project directory: {}".format(self._path))
            log.warning("{}".format(str(e)))


    def terraform_init_cleanup(self, confirm=False):
        """Class method that performs a terraform init directory cleanup on the working directory.
        If an existing .terraform directory exists and confirm is true, then the directory will be removed from the directory path.
        """
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Terraform init cleanup action requested!".format(log_msg))
        self._log.debug("{}: Confirm .terraform directory cleanup: {}".format(log_msg, confirm))
        try:
            if confirm:
                self._log.debug("{}: Cleaning up the .terraform directory in target project directory: {}".format(log_msg, self._path))
                tf_init_cleanup_directory = os.path.join(self._path, '.terraform')
                if os.path.exists(tf_init_cleanup_directory) and tf_init_cleanup_directory.endswith('.terraform') and 'tfstate' not in tf_init_cleanup_directory:
                    shutil.rmtree(tf_init_cleanup_directory)
                    self._log.debug("{}: Init cleanup completed successfully in the target project directory. Removed directory: {}".format(log_msg, tf_init_cleanup_directory))
                else:
                    self._log.debug("{}: Init cleanup failed to locate the .terraform directory in the target project directory: {}".format(log_msg, self._path))
            else:
                self._log.warning("Request to clean the .terraform directory in the target project path must be called setting the confirm property to True. Aborting Cleanup..")
                self._log.warning("{}".format(str(e)))
        except Exception as e:
            self._log.warning("Failed to remove the .terraform directory in the target project directory path: {}".format(self._path))
            self._log.warning("{}".format(str(e)))
