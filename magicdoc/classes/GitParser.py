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
        self._config = None
        self._repo = None
        self._release = None

        # Execute Files Setter, this object is needed for all other setters, and so should be ran at the time of instance instantiation.
        self.config = True


    ############################################
    # Parse Git Config File:  [Verified]       #
    ############################################
    @property
    def config(self):
        """Getter for class property config method. This object property will return the self._config list containing potentially parsed URL data."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._config is not None and isinstance(self._config, list) and bool(self._config):
            return self._config
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
            self._config = local_repo_results
            self._log.debug("{}: Git parse results saved successfully!".format(log_msg))
        except Exception as e:
            self._log.error("{}: Failed to find or parse a git config in the target project directory: {}".format(log_msg, local_git_config_path))
            self._log.warning("{}: Git repository and release data will not be available during this execution cycle.".format(log_msg))
            self._log.error("{}: Exception: {}".format(log_msg, str(e)))


    ############################################
    # Parse Git Config and Request Repo Data:  #
    ############################################
    # TODO: This method will need to be restructured to handle other git providers such as gitlab and bitbucket in the near future.
    @property
    def repo(self):
        """Getter for class property repo method. This object property will return the self._git_repo dictionary if a successful request to the repo provider was completed."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._repo is not None and isinstance(self._repo, dict) and bool(self._repo):
            return self._repo
        else:
            self._log.write("MagicDoc git repo http provider request did not complete successfully. No git repo data is currently available.", 'bright_red')
            self._log.write("No git repository data is currently available for the target project at this time.", 'bright_red')
            return None


    @repo.setter
    def repo(self, token=None):
        """Setter for class property repo method that will attempt to orchestrate the creation of a valid request URL, the sending of that request,
        the parsing of the response, and finally setting the class repo property with valid response data."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Refresh requested".format(log_msg))
        try:
            # Instantiate local variables:
            git_repository = False
            git_repository_provider = False
            git_repository_request_processor = False
            git_authentication_token = token if token is not None and isinstance(token, str) and len(str(token)) > 0 else None

            # Validate that config data is available to construct a proper request URL.
            if self._config is not None and isinstance(self._config, list) and bool(self._config) and len(self._config) > 0:
                self._log.debug("{}: Targeted project git config was found and loaded successfully".format(log_msg))
                # TODO: Handle multiple URL sources, check origin or have user specify via input or selection prompt.
                # TODO: Handle searching the MagicDoc config file for configured repository data required to make the repository provider request.
                for config in self._config:
                    git_repository = "{}/{}".format(config.get('namespace', 'not'), config.get('name', 'provided'))
                    self._log.debug("{}: Setting target git repository for target project to: {}".format(log_msg, git_repository))
                    git_repository_provider = config.get('provider')
                    # TODO: Remove this when support for other repos is developed.
                    if git_repository_provider != 'github.com' or 'github.com' not in git_repository_provider:
                        continue
                    self._log.debug("{}: Setting target git repository provider to: {}".format(log_msg, git_repository_provider))
                    self._log.debug("{}: Attempting to determine repository processor...".format(log_msg))
                    if git_repository_provider == 'github.com' or 'github.com' in git_repository_provider:
                        self._log.debug("{}: Repository provider has been identified as {}".format(log_msg, git_repository_provider))
                        self._log.debug("{}: Sending request data to {} request processor".format(log_msg, git_repository_provider))
                        git_repository_request_processor = self.github_request(git_repository, token)
                        if git_repository_request_processor is not None and isinstance(git_repository_request_processor, dict) and bool(git_repository_request_processor):
                            self._log.debug("{}: Request processor has completed successfully".format(log_msg))
                            self._log.debug("{}: Updating repository property.".format(log_msg))
                            self._repo = git_repository_request_processor
                        else:
                            self._log.warning("{}: An error occurred attempting to process the git repository data request.".format(log_msg))
                    else:
                        self._log.warning("{}: Git repository request URL could not be constructed! Currently only github is supported. Support for other git repository providers is in development.".format(log_msg))
                        self._log.warning("{}: Git repository data will not be availabe during this execution. Please enable debug mode for additional information!".format(log_msg))
                        continue
            else:
                self._log.warning("{}: Git config data was unavailable during this execution. Repository URL could not be constructed!".format(log_msg))
                self._log.warning("{}: Git repository data will not be availabe during this execution. Please enable debug mode for additional information!".format(log_msg))
        except Exception as e:
            self._log.error("{}: Unable to parse Github response data".format(log_msg))
            self._log.error("{}: Exception: {}.".format(log_msg, str(e)))


    ############################################
    # Parse Git Config and Request Repo Data:  #
    ############################################
    # TODO: This method will need to be restructured to handle other git providers such as gitlab and bitbucket in the near future.
    @property
    def release(self):
        """Getter for class property release method. This object property will return the self._git_release version string. This properties setter will be initiated from the repo property method.."""
        # Define this function for logging
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Property requested".format(log_msg))
        if self._release is not None and isinstance(self._release, str):
            return self._release
        else:
            self._log.write("MagicDoc git release http provider request did not complete successfully. No git repo data is currently available.", 'bright_red')
            self._log.write("No git repository data is currently available for the target project at this time.", 'bright_red')
            return None


    @release.setter
    def release(self, version):
        """Setter for class property release method. This method simply is used to set the self.release property sourced from the data collected during the repo setter method action."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Update requested".format(log_msg))
        if version is not None and isinstance(version, str):
            self._release = version

    
    ############################################
    # Github Request/Response Parser Methods:  #
    ############################################
    def github_request(self, repo, token=None):
        """Class method to handle the construction of the github API URL that will be used to fetch the required repository/release data.
        This method will also be responsible for sending the request and ensuring that the request response is valid."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Github URL construction requested".format(log_msg))
        try:
            # Instantiate local variables
            github_request_url = False
            github_repo_request = False
            github_release_request = False
            github_request_headers = {}
            github_response = None

            # Construct Github repository URL
            github_request_url = "https://api.github.com/repos/{}".format(repo)
            self._log.info("{}: Github repository API URL has been set to: {}".format(log_msg, github_request_url))
            if token is not None:
                self._log.info("{}: Github authentication token has been provided and appears to be valid. Building request headers to include provided auth token...".format(log_msg))
                github_request_headers.update({'Authorization': 'token {}'.format(token)})
            # Send the request
            self._log.debug("{}: Sending repository request to request handler for execution".format(log_msg))
            github_repo_request = self.request_handler(github_request_url, github_request_headers)

            # Construct Github releases URL
            github_request_url = "https://api.github.com/repos/{}/releases/latest".format(repo)
            self._log.info("{}: Github releases API URL has been set to: {}".format(log_msg, github_request_url))

            # Send the request and then set the version number to the self._releases property
            self._log.debug("{}: Sending releases request to request handler for execution.".format(log_msg))
            github_release_request = self.request_handler(github_request_url, github_request_headers)
            # TODO Validate this response further in the future.
            self._release = github_release_request.get('tag_name', 'v0.0.0')
            self._log.debug("{}: Setting Github release property to {}".format(log_msg, self._release))

            # Send both requests for processing
            self._log.debug("{}: Sending repository and release responses to response processor.".format(log_msg))
            github_response = self.github_response(github_repo_request, github_release_request)
            if github_response is not None and isinstance(github_response, dict) and bool(github_response):
                self._log.debug("{}: Response processor has completed successfully.".format(log_msg))
                return github_response
            else:
                self._log.error("{}: Unable to parse Github repository response object".format(log_msg))
                self._log.error("{}: GitHub repository data will not be availabe for generating the repo documentation.".format(log_msg))
                return {}
        except Exception as e:
            self._log.error("{}: Unable to parse Github response data".format(log_msg))
            self._log.error("{}: Exception: {}.".format(log_msg, str(e)))
            return {}


    def github_response(self, repo_response, releases_response):
        """Class method to handle the parsing Github API request responses and the construction of the caller response object."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: Github response parsing requested".format(log_msg))
        try:
            # Instantiate local variables required for processing:
            github_response = {}

            # Process the repository response first
            self._log.info("{}: Parsing Github repository response data...".format(log_msg))
            # Construct Github Repo/Release response object.
            if isinstance(repo_response, dict) and bool(repo_response):
                github_response.update(name=repo_response.get('name'))
                github_response.update(full_name=repo_response.get('full_name'))
                github_response.update(description=repo_response.get('description'))
                github_response.update(owner=repo_response.get('owner').get('login'))
                github_response.update(owner_url=repo_response.get('owner').get('html_url'))
                self._log.info("{}: Github response parsing completed successfully!".format(log_msg))
                self._log.info(json.dumps(github_response, indent=4, sort_keys=True))
                return github_response
            else:
                self._log.error("{}: Unable to parse Github repository response object".format(log_msg))
                self._log.error("{}: GitHub repository data will not be availabe for generating the repo documentation.".format(log_msg))
                return {}
        except:
            self._log.error("{}: Unable to parse Github response data".format(log_msg))
            self._log.error("{}: Exception: {}.".format(log_msg, str(e)))
            return {}


    def request_handler(self, request, headers):
        """Class Method to send an http/https request and validate that the response object is valid, once completed, the method will send the response back to the caller."""
        # Define this function for log messages and function call identification. 
        this = inspect.stack()[0][3]
        log_msg = "{}.{}".format(self._log_context, this)
        self._log.info("{}: HTTP/HTTPS request processor called!".format(log_msg))
        try:
            # Set local variables required to perform necessary method operations.
            response = None
            # Send the HTTP/HTTPS request
            self._log.info("{}: Sending API request to: {}".format(log_msg, request))
            r = requests.get(request, headers=headers)
            self._log.info("{}: Request sent successfully!  Starting response validation...".format(log_msg))
            # Validate that the request was successful and if so, then flag the response object for processing
            if r.status_code == 200:
                response = json.loads(r.text)
                if isinstance(response, dict) and bool(response):
                    self._log.info("{}: API response status: {} passed validation check. Sending success response object back to the instance caller".format(log_msg, r.status_code))
                    self._log.debug(json.dumps(response, indent=4, sort_keys=True))
                else:
                    self._log.error("{}: The response object does not appear to be valid json. Sending failure response back to caller...".format(log_msg))
                    self._log.error(json.dumps(response, indent=4, sort_keys=True))
                    return {}
            else:
                self._log.error("{}: API response status: {} failed validation check. Sending failure response object back to the instance caller".format(log_msg, r.status_code))
                return {}
        except Exception as e:
            self._log.error("{}: An error occurred when attempting to send the API request!".format(log_msg))
            self._log.error("{}: Exception: {}".format(str(e)))
            return {}
        return response


# Code for later: Gitlab, Bitbucket API research.
# elif 'gitlab' in git_repository_provider:
#     git_repo_url = "https://{}/api/v4/projects/{}".format(git_repository_provider, git_repository)
#     if token is not None and len(token) > 0 and isinstance(token, str):
#         self._log.info("{}: Authentication token for git repository provider provider: {} provided... constructing request headers...".format(log_msg, git_repository_provider))
#         request_headers = {'PRIVATE-TOKEN': '{}'.format(token)}
# elif 'bitbucket' in git_repository_provider:
#     git_repo_url = "https://bitbucket.org/api/2.0/repositories/{}".format(git_repository)
#     if token is not None and len(token) > 0 and isinstance(token, str):
#         self._log.info("{}: Authentication token for git repository provider provider: {} provided... constructing request headers...".format(log_msg, git_repository_provider))
#         request_headers = {'Authorization': 'Bearer {}'.format(token)}