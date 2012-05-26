#!/usr/bin/python

from fabric.api import env

class Conf:
    pass

# save all variables to one object
conf_class = Conf()

# specify operating system ["ubuntu", "debian", "archlinux"]
conf_class.oper_sys="ubuntu"

# path with installation files
conf_class.files_dir="/root/fabric/dark-acer/files"

# prefix of old disk (mounted or backup location)
conf_class.old_disk="/mnt/disk"

# rather do prompt section instead total halt (keeping last state)
conf_class.warn_only = True

# variable for env variable
conf_class.hosts = [
"192.168.2.218",
#"192.168.2.118",
]

# variable for env variable
conf_class.key_filename = [
"/root/.ssh/id_rsa_dark_acer",
#"/root/.ssh/id_rsa_proxy",
]

# set environment variables
env.hosts = conf_class.hosts
env.key_filename = conf_class.key_filename
env.warn_only = conf_class.warn_only

# rewrite global env variable to object attribute
conf_class.env = env

