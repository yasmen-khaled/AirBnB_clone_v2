#!/usr/bin/python3
# Fabfile to create an archive
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["100.24.238.235", "18.210.16.58"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    x = datetime.utcnow()
    f = "versions/web_static_{}{}{}{}{}{}.tgz".format(x.year,
                                                         x.month,
                                                         x.day,
                                                         x.hour,
                                                         x.minute,
                                                         x.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(f)).failed is True:
        return None
    return f


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    f = archive_path.split("/")[-1]
    n = f.split(".")[0]

    if put(archive_path, "/tmp/{}".format(f)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(n)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(n)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(f, n)).failed is True:
        return False
    if run("rm /tmp/{}".format(f)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(n, n)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(n)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(n)).failed is True:
        return False
    return True


def deploy():
    """server."""
    f = do_pack()
    if f is None:
        return False
    return do_deploy(f)
