# paths
import sys
import os

# MAIN DIRECTORIES
root_dir        = (os.path.dirname(os.path.realpath(__file__)))
libs_dir        = os.path.join(root_dir,"Libs")
information_dir = os.path.join(root_dir,"Information")
log_dir         = os.path.join(information_dir,'LogFiles')
database_dir    = os.path.join(root_dir,'Database')
pic_dir         = os.path.join(database_dir,'Pictures')

# database
host="localhost"
user="root"
passwd="fam4ev1*"
database="tinder"