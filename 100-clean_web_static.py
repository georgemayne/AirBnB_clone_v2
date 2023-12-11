#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import isfile
from fabric.contrib import files

env.user = 'ubuntu'
env.hosts = ['54.237.77.167', '100.27.3.4']
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """Delete out-of-date archives
    Parameters:
        number (int): The number of recent archives
        to retain. Set to 0 or 1 to keep
        only the latest archive, or increase
        for more recent archives.
    Returns:
        None
    """
    number = int(number)

    if number < 0:
        return

    number = max(1, number)

    archives_to_keep = sorted(run("ls -x /data/web_static/releases").split())
    archives_to_delete = archives_to_keep[:-number]
    for archive in archives_to_delete:
        run("rm -rf /data/web_static/releases/{}".format(archive))
    versions_path = local("ls -x versions", capture=True).split()
    versions_to_del = versions_path[:-number]
    for version in versions_to_del:
        local("rm -f versions/{}".format(version))
