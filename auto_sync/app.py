import logging.config
import os
import shutil
import sys

import yaml

from auto_sync.config import ConfigLoader
from auto_sync.resources import resource_dir, get_resource
from auto_sync.sync import Sync
from auto_sync.util import read_file
from auto_sync.worker import Worker

props_filename = 'auto_sync.ini'

resource_folder = resource_dir
if getattr(sys, 'frozen', False):
    resource_folder = sys._MEIPASS

# Just for process output
with open(get_resource("logging.yml")) as log_cfg:
    logging.config.dictConfig(yaml.safe_load(log_cfg))
logger = logging.getLogger("auto_sync")

if not os.path.exists(props_filename):
    shutil.copy(get_resource(props_filename), ".")

# Load the default config and merge the user values into it
config = ConfigLoader.load(get_resource(props_filename))
user_config = ConfigLoader.load(props_filename)
config.merge_with(user_config)

# We need to determine if there is an entry specifying the
# folder for yml files - hence this semi-circular import
sync_folder = config.get_config('sync').get('sync_folder', '.')
config.set_resource_dir(sync_folder)

sync_config = config.get_config("sync")
sync_script = sync_config.get('sync_script')
if not os.path.exists(sync_script):
    shutil.copy(get_resource("example_script.yml"), ".")
    logger.error("Error - configuration: " + sync_script
                 + " not found.  Generating base example and exiting.")
    exit()

# Load all properties from INI and point to the folder where resources are stored
# if os.path.exists('app.ini') and os.path.exists('example.yml'):
#     props_file = 'app.ini'
# else:
#     generate_files = input("'app.ini' and 'example.yml' not found. Would you like to create them now? y/n: ")
#     generate_files.lower()
#     if generate_files == 'y':
#         copyfile(resource_folder + '\\app.ini', 'app.ini')
#         copyfile(resource_folder + '\\example.yml', 'example.yml')
#         print('Files have been created. Open files and modify.')
#         sys.exit()
#     else:
#         # prompt do you want to generate example files? yes: create and exit, no: exit
#         # create copy of app.ini from where it is to the same folder shutil copy
#         # do the same for the example.yml file
#         print('The files have not been created.')
#         props_file = os.path.join(resource_folder, "app.ini")
#         sys.exit()


# Output folder for sync logs
log_folder = sync_config.get("log_folder")

# Read in the YAML and binaries from the config section
resources_config = config.get_resource_config()

# Create logs folder
os.makedirs(log_folder, exist_ok=True)

# The "base" config into which sync config gets merged
template_config = resources_config.merge_with(sync_config.values)
template_config.set_value("log_folder", os.path.abspath(log_folder))

# Execute (single thread for now)
for config in read_file(sync_script):
    sync = Sync(config)
    w = Worker(sync, template_config)
    w.run()


