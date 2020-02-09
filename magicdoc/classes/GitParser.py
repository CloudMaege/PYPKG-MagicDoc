##############################################################################
# CloudMage : MagicDoc GitHub Repo Find/Parse/Request Class
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Github Data Fetch Class
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/9/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
import requests

# Import Base Python Modules
import json, os, inspect


#####################
# Class Definition: #
#####################
class GitParser(object):
    """MagicDoc Git Parser Class
    This class is designed to search a provided target directory path and attempt to find configured repository URLs from the directories git config.
    If found, the repository name and user's namespace will be parsed and used to send requests to the repository to collect repository data and
    latest release information for the targeted project.
    """

    def __init__(self, log, path):
        '''GitParser Class Constructor'''

        # Set class instantiation variables
        self._log = log
        self._path = path
        self._log_context = "CLS->GitParser"

        # Set Git platform provider API URLs
        # TODO: Need to test these in order to support others besides github. Need exact URL paths to repo data, and releases
        # self._github_api = 'https://api.github.com'
        # self._gitlab_api = 'https://{}}/api/v4/projects'.format("REPO_BASE_URL")
        # self._bitbucket_api = 'https://api.bitbucket.org/2.0/repositories/tutorials/tutorials.bitbucket.org'
        
        # Set properties to hold result sets.
        self._repo_config = None
        self._repo = None
        self._releases = None

        # Execute Files Setter, this object is needed for all other setters, and so should be ran at the time of instance instantiation.
        self.config = True


    ############################################
    # Parse Git Config File:  #
    ############################################
    @property
    def config(self):
        """Getter for class property config method. This object property will return the self._repo_config list containing potentially parsed URL data."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._repo_config is not None and isinstance(self._repo_config, list) and bool(self._repo_config):
            return self._repo_config
        else:
            self._log.write("MagicDoc git config file not found in {}".format(self._path), 'bright_red')
            self._log.write("No git information about the target project can be provided at this time.", 'bright_red')
            return None


    @config.setter
    def config(self, init=True):
        """Setter for class property config method that will attempt to locate, open and parse the git config file in the target project path. List of Dicts returned."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Refresh requested".format(log_msg))
        try:
            # Search for a .git directory in the working directory search path, and if found parse to get the repo namespace and repo name.
            local_git_config_path = os.path.join(self._path, '.git/config')
            local_repo_results = []
            self._log.info("{}: {} function call to search for repo data in target directory: {} ".format(log_msg, this, local_git_config_path))
            if os.path.exists(local_git_config_path):
                self._log.debug("{}: Search found the requested directory: {}".format(log_msg, local_git_config_path))
                self._log.debug("{}: Attempting to parse the target project repository data".format(log_msg))
                try:
                    with open(local_git_config_path) as f:
                        for count, line in enumerate(f):
                            # Set Parse Variable
                            local_parse_result = {}

                            # For each line in the config, if url is found in the line, then attempt to parse it.
                            if 'url' in line:
                                k, v = line.partition("=")[::2]
                                self._log.debug("{}: Url string match found in the target git config... Attempting to parse URL string: {}".format(log_msg, v.strip()))
                                local_parse_result.update(url=v.strip())
                                local_git_url = v.strip().split("/")
                                self._log.debug("{}: Attempting to determine git platform provider from URL string.".format(log_msg))
                                self._log.debug("{}: Splitting URL string by '/' yielded {} list elements. Parsing repository namespace and repo name from generated list.".format(log_msg, len(local_git_url)))
                                # Parse out the repo name and namespace
                                local_parse_result.update(namespace=local_git_url[-2].split(":")[-1])
                                local_parse_result.update(name=local_git_url[-1].split(".")[0])
                                # Parse out the git platform provider
                                try:
                                    if len(local_git_url) == 2:
                                        local_parse_result.update(provider=local_git_url[-2].split(":")[0].split("@")[1])
                                    elif len(local_git_url) > 3:
                                        local_parse_result.update(provider=local_git_url[-3])
                                except:
                                    self._log.warning("{}: Unable to parse repository platform provider, omitting from result dictionary.".format(log_msg))
                                self._log.debug("{}: Parse of URL string successful. Found: {} -> {}".format(log_msg, local_parse_result.get('namespace'), local_parse_result.get('name')))
                                local_repo_results.append(local_parse_result)
                except Exception as e:
                    self._log.error("{}: File open operation failed!".format(log_msg))
                    self._log.error("{}: Exception: {}".format(log_msg, str(e)))
            else:
                self._log.error("{}: Search could not find the requested directory: {}. Directory path does not exist.".format(log_msg, local_git_config_path))
                self._log.warning("{}: Git repository and release data will not be available during this execution cycle.".format(log_msg))
            self._log.debug("{}: Git parse results: {}".format(log_msg, local_repo_results))
            self._repo_config = local_repo_results
            self._log.debug("{}: Git parse results saved successfully: {}".format(log_msg))
        except Exception as e:
            self._log.error("{}: Failed to find or parse a git config in the target project directory: {}".format(log_msg, local_git_config_path))
            self._log.warning("{}: Git repository and release data will not be available during this execution cycle.".format(log_msg))
            self._log.error("{}: Exception: {}".format(log_msg, str(e)))
