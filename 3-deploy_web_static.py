#!/usr/bin/python3
"""Distributes an archive to web servers using Fabric."""
from fabric.api import env, put, run, local
import os
from datetime import datetime
from pathlib import Path

env.user = 'ubuntu'
env.hosts = ['54.237.77.167', '100.27.3.4']
env.key_filename = '~/.ssh/school'


def do_pack():
    """"Generate a .tgz archive from web_static folder"""

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return (archived_f_path)
    else:
        return (None)


def do_deploy(archive_path):
    """Deploy the archive files to web server
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_ver = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_ver))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             new_ver))
        run("sudo rm {}".format(archived_file))
        run("sudo rsync -av --remove-source-files {}/web_static/* {}"
            .format(new_ver, new_ver))
        run("sudo rm -rf {}/web_static".format(new_ver))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_ver))

        print("New version deployed!")
        return (True)

    return (False)


def deploy():
    """Full deployment process"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
