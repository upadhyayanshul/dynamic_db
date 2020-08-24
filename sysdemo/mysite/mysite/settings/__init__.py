# IMPORT REQUIRED MODULE HERE 
import os
import json

import pymysql
pymysql.install_as_MySQLdb()

# READ PRODUCTION SETTINGS BY DEFAULT 
CONFIG_FILE = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')),'config','productoion_config.json')

#SET THE DJANGO_DEVELOPMENT = TRUE IN OS ENVIRONMENT AND OVERWRITE SETTINGS
if(os.environ['DJANGO_DEVELOPMENT']):
	CONFIG_FILE = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')),'config','development_config.json')

# IMPORT THE REQUIRED SETTINGS FROM THE DIFFERENT ENVIRONMENT 
try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        config['PROD']
    from .production import *

except KeyError:
    from .development import *

## USE ENV VARIABLES FROM THE JSON FILE OF CORRESPONDING ENVIRONMENT
SECRET_KEY = config['SECRET_KEY']