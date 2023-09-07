#!/usr/bin/python3

"""
This script compresses the web static package
"""

from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['100.25.19.204', '54.157.159.85']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
        """
        Deploys the web files to server
        """
        try:
                if not (path.exists(archive_path)):
                        return False

                # Uploads archive
                put(archive_path, '/tmp/')

                # Creates target dir
                timestamp = archive_path[-18:-4]
                run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

                # Uncompresses archive and delete .tgz
                run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                    .format(timestamp, timestamp))

                # Removes archive
                run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

                # Moves contents into host web_static
                run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

                # Removes extraneous web_static dir
                run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                    .format(timestamp))

                # Deletes pre-existing sym link
                run('sudo rm -rf /data/web_static/current')

                # Re-establishes symbolic link
                run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
        except:
                return False

        # Returns True on success
        return True
