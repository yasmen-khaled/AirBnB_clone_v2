
#!/usr/bin/python3
# web server distrbute
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["100.24.238.235", "18.210.16.58"]

def do_deploy(archive_path):
    """web"""
    
    if os.path.isfile(archive_path) is False:
        return False
    
    x = archive_path.split("/")[-1]
    n = x.split(".")[0]

    if put(archive_path, "/tmp/{}".format(x)).failed is True:
        return False
    
    if run("rm -rf /data/web_static/releases/{}/".
           format(n)).failed is True:
        return False
    
    if run("mkdir -p /data/web_static/releases/{}/".
           format(n)).failed is True:
        return False
    
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(x, n)).failed is True:
        return False
    
    if run("rm /tmp/{}".format(x)).failed is True:
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
