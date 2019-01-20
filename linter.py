#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Modified from VHDL to Verilog to SystemVerilog by Leon Woestenberg
# Original:
# Written by Bruno JJE
# Copyright (c) 2015 Bruno JJE
#
# License: MIT
#

"""This module exports the Xsvlog plugin class."""

from SublimeLinter.lint import Linter
import re

class Xsvlog(Linter):

    """Provides an interface to xvlog (from Xilinx Vivado Simulator)."""

    syntax = 'systemverilog'
    #cmd = 'xvlog -sv --work=/tmp/sublime-xvlog-work --log=/tmp/sublime-linter-sv.log $temp_file'
    cmd = 'xvlog -sv --work work=/tmp/sublime-xvlog-work --nolog $temp_file'
    #version_args = '--version --nolog'
    #version_re = r'Vivado Simulator (?P<version>\d+\.\d+)'
    #version_requirement = '>= 2014.4'
    #tempfile_suffix = 'sv'
    tempfile_suffix = 'linter'
    # Here is a sample xvhdl error output:
    # ----8<------------
    # ERROR: [VRFC 10-91] td_logic is not declared [/home/BrunoJJE/src/filtre8.vhd:35]
    # ----8<------------

    regex = (
        r"^(?P<error>(ERROR|INFO): )(?P<message>\[.*\].*)"
        r"\[(?P<path>.*):(?P<line>[0-9]+)\]"
    )

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method to prefix the error message with the
        linter name.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        # See if we can find a "near" keyword from the message to add a squirly line

        # "...near XXX"
        near_match = re.search(r'.*near (?P<near>\w+).*', message)
        if not near_match:
            # "XXX is not declared"
            near_match = re.search(r'(?P<near>\w+) is not declared.*', message)
        if not near_match:
            # "procedural assignment to a non-register XXX is not permitted..."
            near_match = re.search(r'non-register (?P<near>\w+) is not permitted.*', message)
        if not near_match:
            # "use of undefined macro XXX" for example `if instead of `ifdef
            near_match = re.search(r'use of undefined macro (?P<near>\w+).*', message)
        if not near_match:
            # for example `endif without `if
            near_match = re.search(r'(?P<near>\w+) without `if.*', message)
        if not near_match:
            # "procedural assignment to a non-register XXX is not permitted..."
            near_match = re.search(r'undeclared symbol (?P<near>\w+).*', message)
        # @TODO Extend this Linter here with near matches, as follows:
        # if not near_match:
            #near_match = re.search(r'prefix message (?P<near>\w+) postfix message.*', message)

        if near_match:
            near = near_match.group('near')

        if match:
            message = '[xsvlog] ' + message

        return match, line, col, error, warning, message, near
