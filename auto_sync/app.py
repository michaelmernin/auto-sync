import logging.config
import os
import shutil
import sys

import yaml

import auto_sync.resources as resources
from auto_sync.config import ConfigLoader
from auto_sync.sync import Sync
from auto_sync.util import read_file
from auto_sync.worker import Worker
from resources import get_resource

def abort():
    input("Press enter to exit")
    sys.exit(0)

props_filename = 'auto_sync.ini'
if getattr(sys, 'frozen', False):
    resources.resource_dir = sys._MEIPASS

# Just for process output
with open(get_resource("logging.yml")) as log_cfg:
    logging.config.dictConfig(yaml.safe_load(log_cfg))
logger = logging.getLogger("auto_sync")

if not os.path.exists(props_filename):
    shutil.copy(get_resource(props_filename), ".")
    logger.error("No configuration file ({0}) found: Generating "
                 "base default and exiting.".format(props_filename))
    abort()

# Load the default config and merge the user values into it
config = ConfigLoader.load(props_filename)

# We need to determine if there is an entry specifying the
# folder for yml files - hence this semi-circular import
config.set_source_dir(config.get_config('sync').get('sync_folder', '.'))
sync_config = config.get_config("sync")
sync_script = sync_config.get('sync_script')
if not os.path.exists(sync_script):
    logger.error("Error - missing run script: " + sync_script)
    abort()

# Output folder for sync logs
log_folder = sync_config.get("log_folder")
os.makedirs(log_folder, exist_ok=True)

# The "base" config into which sync config gets merged
template_config = config.get_resource_config().merge_with(sync_config.values)
template_config.set_value("log_folder", os.path.abspath(log_folder))

# Execute (single thread for now)
for config in read_file(sync_script):
    sync = Sync(config)
    w = Worker(sync, template_config)
    w.run()
