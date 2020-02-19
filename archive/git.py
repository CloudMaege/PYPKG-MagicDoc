##############################################################################
# CloudMage : MagicDoc Git Module
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Git Config Parser / Repo API Request Module
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/09/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Base Python Modules
import os, inspect, logging

log = logging.getLogger()

# Define Global Variables
LOG_CONTEXT = "MOD->git"
# log.debug("{}: ".format(log_msg))

def git_config(arg_log, arg_path):
    """Function to search for and parse the .git/config repository settings file, and use it to determine the git repository name space and repo name"""
    # Define this function for log messages and function call identification. 
    # log = arg_log
    this = inspect.stack()[0][3]
    log_msg = "{}->[{}]".format(LOG_CONTEXT, this)
    try:
        # Search for a .git directory in the working directory search path, and if found parse to get the repo namespace and repo name.
        local_git_config_path = os.path.join(arg_path, '.git/config')
        local_repo_results = []
        log.info("{}: {} function call to search for repo data in target directory: {} ".format(log_msg, this, local_git_config_path))
        if os.path.exists(local_git_config_path):
            log.debug("{}: Search found the requested directory: {}".format(log_msg, local_git_config_path))
            log.debug("{}: Attempting to parse the target project repository data".format(log_msg))
            try:
                with open(local_git_config_path) as f:
                    for count, line in enumerate(f):
                        # Set Parse Variable
                        local_parse_result = {}

                        # For each line in the config, if url is found in the line, then attempt to parse it.
                        if 'url' in line:
                            k, v = line.partition("=")[::2]
                            log.debug("{}: Url string match found in the target git config... Attempting to parse URL string: {}".format(log_msg, v.strip()))
                            local_parse_result.update(url=v.strip())
                            local_git_url = v.strip().split("/")
                            log.debug("{}: Attempting to determine git platform provider from URL string.".format(log_msg))
                            log.debug("{}: Splitting URL string by '/' yielded {} list elements. Parsing repository namespace and repo name from generated list.".format(log_msg, len(local_git_url)))
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
                                log.warning("{}: Unable to parse repository platform provider, omitting from result dictionary.".format(log_msg))
                            log.debug("{}: Parse of URL string successful. Found: {} -> {}".format(log_msg, local_parse_result.get('namespace'), local_parse_result.get('name')))
                            local_repo_results.append(local_parse_result)
            except Exception as e:
                log.error("{}: File open operation failed!".format(log_msg))
                log.error("{}: Exception: {}".format(log_msg, str(e)))
        else:
            log.error("{}: Search could not find the requested directory: {}. Directory path does not exist.".format(log_msg, local_git_config_path))
            log.warning("{}: Git repository and release data will not be available during this execution cycle.".format(log_msg))
        return local_repo_results
    except Exception as e:
        log.error("{}: Failed to find or parse a git config in the target project directory: {}".format(log_msg, local_git_config_path))
        log.warning("{}: Git repository and release data will not be available during this execution cycle.".format(log_msg))
        log.error("{}: Exception: {}".format(log_msg, str(e)))

path = "/Volumes/MacData/Work/CloudMage/Terraform/TF-AWS-CodeBuild-Lambda-Deployment-Pipeline-Common-Root/"
test_repo_url = git_config({}, path)
print(test_repo_url)