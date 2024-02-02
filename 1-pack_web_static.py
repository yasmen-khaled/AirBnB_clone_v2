#!/usr/bin/python3
# Fabfile to generates a .tgz archive
from datetime import datetime
from fabric.api import local
import os.path as v



def do_pack():
    """tar"""
    x = datetime.utcnow()
    f= "versions/web_static_{}{}{}{}{}{}.tgz".format(x.year,
                                                         x.month,
                                                         x.day,
                                                         x.hour,
                                                         x.minute,
                                                         x.second)
    if v.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
            
    if local("tar -cvzf {} web_static".format(f)).failed is True:
        return None
        
    return f
