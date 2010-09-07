import commands
import os
import sys

BASE_VERSION = "0.3"

def _prerelease():
    """
    Currently always a prerelease.
    
    The prerelease version is based on number of commits (which should always
    increase in a master that does not allow rebasing) and the gitref for
    reference purposes.
    
    See here for the version name rules:
    http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version
    """
    (code, current_head) = commands.getstatusoutput("git rev-parse HEAD")
    if code != 0:
        raise Exception("cannot determine Nimboss version, git failed")
    
    (code, output) = commands.getstatusoutput("git log --abbrev-commit --pretty=format:'%h' | wc -l")
    if code != 0:
        raise Exception("cannot determine Nimboss version, git log failed")
    
    try:
        num_commits = int(output)
    except:
        raise Exception("cannot determine Nimboss version, unknown git log output")
    
    return "pre%d-%s" % (num_commits, current_head[:8])

version = BASE_VERSION + _prerelease()
