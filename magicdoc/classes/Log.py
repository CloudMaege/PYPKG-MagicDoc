##############################################################################
# CloudMage : CLI Log Class
#=============================================================================
# CloudMage Command Line Click Log Utility Class
#   - Provide simplified logging method across an entire click CLI environment
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/8/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:
###############
# Import Pip Installed Modules:
import click

# Import Base Python Modules
import sys

class Log():
    """
    CLI Log class to allow easy logging throughout a click CLI application taking advantage of clicks context passing.
    This class is based on the following log format opinion, controlled by the self._env class attribute.
    """


    def __init__(self, arg_verbose=False, arg_verbose_level='debug'):
        """Construct the Log Class"""
        # Class Attributes
        self.verbose = arg_verbose
        self._verbose_level = arg_verbose_level
        self._debug = True
        self._info = True
        self._warning = True
        self._error = True


    @property
    def verbose_level(self):
        """Log method that will return the current log verbose level"""
        # If not verbose mode then clear the screen.
        return self._verbose_level

    @verbose_level.setter
    def verbose_level(self, arg_level):
        """Log setter method to set the log verbose level"""
        # Set verbose_level attribute
        self._verbose_level = arg_level

        # Set default values for all log levels
        self._debug = True
        self._info = True
        self._warning = True
        self._error = True
        
        # Based on the specified log level, set the proper log values.
        if arg_level.lower() == "info":
            self._debug = False
        elif arg_level.lower() == "warning":
            self._debug = False
            self._info = False
        elif arg_level.lower() == "error":
            self._debug = False
            self._info = False
            self._warning = False


    def clear(self):
        """Log method that will perform a screen clear when called"""
        # If not verbose mode then clear the screen.
        if not self.verbose:
            click.clear()


    def write(self, arg_msg, arg_termcolor='green', arg_upper_nl=False, arg_lower_nl=False):
        """Log method to print output to the shell"""
        # Set arg_termcolor if message type was specified
        arg_termcolor = "red" if arg_termcolor.lower() == "error" else arg_termcolor
        arg_termcolor = "bright_red" if arg_termcolor.lower() == "warning" else arg_termcolor
        arg_termcolor = "cyan" if arg_termcolor.lower() == "info" else arg_termcolor
        arg_termcolor = "magenta" if arg_termcolor.lower() == "debug" else arg_termcolor
        if arg_upper_nl:
            click.echo()
        click.secho(arg_msg, file=sys.stderr, fg=arg_termcolor)
        if arg_lower_nl:
            click.echo()


    def header(self, arg_env, arg_cmd, arg_msg, arg_args=None, arg_upper_nl=True, arg_lower_nl=True):
        """Log method to print command title and command environment to the shell"""
        # Local function variables:
        this_msg_length = len(arg_msg)
        
        # Log Templated Header Definition
        if arg_upper_nl:
            click.echo()
        # Print command header and underline:
        click.secho(arg_msg, file=sys.stderr, fg='yellow')
        click.secho("{}".format("=" * this_msg_length), fg='yellow')
        # Print environment metadata info
        self.info("{}: Invoking command: magicdoc tf {}".format(arg_env, arg_cmd))
        self.info("{}: Instantiating `magicdoc tf {}` environment...".format(arg_env, arg_cmd))
        # Print command argument info
        if arg_args is None:
            self.info("{}: Command Args: None".format(arg_env, arg_cmd))
        else:
            if isinstance(arg_args, dict) and bool(arg_args):
                for k, v in arg_args.items():
                    self.args("{}".format(k), v, arg_lower_nl=False)
        if arg_lower_nl:
            click.echo()


    def args(self, arg_msg, arg_option, arg_upper_nl=False, arg_lower_nl=True):
        """Log method to print command args"""
        # Local function variables:
        this_msg_length = len(arg_msg)
        this_msg_offset = 50 - this_msg_length
        
        if arg_upper_nl:
            click.echo()
        click.secho("  {}:{}".format(arg_msg, " " * this_msg_offset), file=sys.stderr, fg='blue', nl=False)
        click.secho("{}".format(arg_option), file=sys.stderr, fg='green')
        if arg_lower_nl:
            click.echo()


    def debug(self, arg_msg):
        """Print a debug message to the shell"""
        this_msg_offset = 3
        if self.verbose and self._debug:
            click.secho("{}:{}{}".format("DEBUG", " " * this_msg_offset, arg_msg), file=sys.stderr, fg='magenta')


    def info(self, arg_msg):
        """Print a info message to the shell"""
        this_msg_offset = 4
        if self.verbose and self._info:
            click.secho("{}:{}{}".format("INFO", " " * this_msg_offset, arg_msg), file=sys.stderr, fg='cyan')


    def warning(self, arg_msg):
        """Print a warning message to the shell"""
        this_msg_offset = 1
        if self.verbose and self._warning:
            click.secho("{}:{}{}".format("WARNING", " " * this_msg_offset, arg_msg), file=sys.stderr, fg='bright_red')


    def error(self, arg_msg):
        """Print a error message to the shell"""
        this_msg_offset = 3
        click.echo()
        click.secho("ATTENTION:", fg='red')
        click.secho("{}:{}{}".format("ERROR", " " * this_msg_offset, arg_msg), file=sys.stderr, fg='red')
        sys.exit()
