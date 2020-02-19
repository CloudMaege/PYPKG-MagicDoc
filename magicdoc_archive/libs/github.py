##############################################################################
# CloudMage : MagicDoc GitHub Repo Data Getter
#=============================================================================
# CloudMage MagicDoc Automatic Documentation Generator CLI Utility/Library
#   - Github Data Fetch Class
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/28/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
from termcolor import colored, cprint
import requests

# Import Base Python Modules
import logging, json

# Instantiate Logger
log = logging.getLogger('magicdoc.libs.github')


#####################
# Class Definition: #
#####################
class Github(object):
    """MagicDoc GitHub DataFetch Class"""

    def __init__(self, RepoNamespace, Repo, AccessToken=None):
        '''GitHub DataFetch Class Constructor'''

        # Run ascertains for expected data types
        assert(isinstance(RepoNamespace, str)), cprint("Error: RepoNamespace expected type string, but was provided: {}".format(type(RepoNamespace)), 'red')
        assert(isinstance(Repo, str)), cprint("Error: Namespace expected type string, but was provided: {}".format(type(Repo)), 'red')

        # Set class variables
        self.repo_namespace = RepoNamespace
        log.debug("Setting GitHub NameSpace: {}".format(RepoNamespace))
        self.repo = Repo

        # Check if an AccessToken was provided, and if so, then create the request headers
        if AccessToken is not None:
            self.access_token = AccessToken
            log.info("GitHub Authentication Token provided")
            self.request_headers = {'Authorization': 'token {}'.format(self.access_token)}
            log.debug("Github repository request headers have been set to include the provided access token.")
        else:
            self.access_token = None
            log.info("No GitHub Authentication Token provided")
            self.request_headers = {}
            log.debug("Github repository request headers have been set to { }")

        self.github_repo_url = "https://api.github.com/repos/{}/{}".format(self.repo_namespace, self.repo)
        logging.info("Setting GitHub Repo API URL: {}".format(self.github_repo_url))
        self.github_releases_url = "https://api.github.com/repos/{}/{}/releases/latest".format(self.repo_namespace, self.repo)
        logging.info("Setting GitHub Release API URL: {}".format(self.github_releases_url))


    ######################
    # Fetch Repo Data:   #
    ######################
    def GetGitHubData(self):
        """Function that will collect some repo information about the project being documented and if available, can be referenced in the generated documentation"""
        try:
            ResponseObj = {}
            
            # Make the request
            log.info("Sending Github repository request...")
            Req = requests.get(self.github_repo_url, headers=self.request_headers)
            ReqBody = json.loads(Req.text)

            # Check the response code, if 200 then return data, if not 200 return error.
            if Req.status_code == 200:
                ResponseObj.update(state="pass")
                ResponseObj.update(status_code=Req.status_code)
                ResponseObj.update(repo_name=ReqBody.get('name'))
                ResponseObj.update(repo_fullname=ReqBody.get('full_name'))
                ResponseObj.update(repo_description=ReqBody.get('description'))
                ResponseObj.update(repo_owner=ReqBody.get('owner').get('login'))
                ResponseObj.update(repo_owner_url=ReqBody.get('owner').get('html_url'))
                log.info("GitHub Request Response Code: [{}]".format(Req.status_code))
                log.debug("GitHub Request Response Message: {}".format(json.dumps(ResponseObj, indent=4, sort_keys=True)))
            else:
                ResponseObj.update(state="fail")
                ResponseObj.update(status_code=Req.status_code)
                ResponseObj.update(repo_name=self.repo)
                ResponseObj.update(repo_fullname="{}/{}".format(self.repo_namespace, self.repo))
                ResponseObj.update(repo_description="No repository description has been defined or provided.")
                ResponseObj.update(repo_owner=self.repo_namespace)
                ResponseObj.update(repo_owner_url="https://github.com/{}".format(self.repo_namespace))
                cprint(" WARNING ENCOUNTERED: ", 'grey', 'on_yellow')
                cprint("Error encountered attempting to send GitHub repository request to: {}".format(self.github_repo_url), 'yellow')
                cprint("GitHub repo data will be unavailable when rendering documentation.\n", 'yellow')
                cprint("GitHub Response Code: [{}]".format(Req.status_code), 'blue')
                cprint("GitHub Response Message: {}\n".format(json.dumps(response, indent=4, sort_keys=True)), 'blue')
                log.warning("Unable to retrieve repository details from GitHub:")
                log.warning("GitHub repository data will not be availabe for generating the repo documentation.")
            # Get the Release info and add it to the response payload before returning the response
            LatestRelease = self.GetLatestRelease()
            ResponseObj.update(latest_release=LatestRelease)
            return ResponseObj
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to send repository request to Github:\n\nException: {}".format(str(e)), 'red')
            log.error("Unknown Exception occurred: {}".format(str(e)))
            log.error("GitHub repository data will not be used to construct the repo documentation due to unavailability.")
            pass


    #######################
    # Fetch Release Data: #
    #######################
    def GetLatestRelease(self):
        """Function that will fetch the latest repository release."""
        try:
            # Make the request
            log.info("Sending Github release request...")
            Req = requests.get(self.github_releases_url, headers=self.request_headers)
            ReqBody = json.loads(Req.text)

            # Check the response code, if 200 then return data, if not 200 return error.
            if Req.status_code == 200:
                Release = ReqBody.get('tag_name')
                log.info("GitHub Release Request Response Code: [{}]".format(Req.status_code))
                log.info("Latest Project Release: {}".format(Release))
            else:
                Release = "UnReleased"
                cprint(" WARNING ENCOUNTERED: ", 'grey', 'on_yellow')
                cprint("Error encountered attempting to send GitHub repository release request to: {}".format(self.github_releases_url), 'yellow')
                cprint("GitHub release data will be unavailable when rendering documentation.\n", 'yellow')
                cprint("GitHub Response Code: [{}]".format(Req.status_code), 'blue')
                cprint("GitHub Response Message: {}\n".format(json.dumps(Release, indent=4, sort_keys=True)), 'blue')
                log.warning("Unable to retrieve repository release details from GitHub:")
                log.warning("GitHub repository release data will not be availabe for generating the repo documentation.")
            # Last Check to make sure that the release value is not null
            if Release == 'null' or Release is None or Release == "":
                Release == "UnReleased"
            return Release
        except Exception as e:
            cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to send repository release request to Github:\n\nException: {}".format(str(e)), 'red')
            log.error("Unknown Exception occurred: {}".format(str(e)))
            log.error("GitHub repository release data will not be used to construct the repo documentation due to unavailability.")
            pass
