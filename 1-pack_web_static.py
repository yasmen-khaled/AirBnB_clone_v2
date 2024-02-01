#!/usr/bin/python3

from datetime import datetime
from fabric.api import local
import os.path



def do_pack():
    """tar"""
    x = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(x.year,
                                                         x.month,
                                                         x.day,
                                                         x.hour,
                                                         x.minute,
                                                         x.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
