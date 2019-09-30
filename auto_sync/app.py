import logging.config
import os
import shutil

import click
import yaml
from click_default_group import DefaultGroup

from auto_sync.config import ConfigLoader
from auto_sync.sync import Sync
from auto_sync.util import read_file
from auto_sync.worker import Worker
from auto_sync.resources import get_resource


@click.group(cls=DefaultGroup, default='sync', default_if_no_args=True)
def cli():
    pass

@cli.command()
@click.option('-c', '--config-path',
              help="point to config ini by name",
              type=click.Path(exists=True),
              default=None)
@click.option('-a', '--args',
              help="override pex args",
              type=str,
              default=None)
def sync(**cli_options):

    # Just for process output
    with open(get_resource("logging.yml")) as log_cfg:
        logging.config.dictConfig(yaml.safe_load(log_cfg))

    if cli_options['config_path']:
        props_filename = cli_options['config_path']
        working_dir = os.path.dirname(props_filename)
    else:
        props_filename = 'auto_sync.ini'
        working_dir = "."

    if not os.path.exists(props_filename):
        raise IOError(
            "Error - file '{}' cannot be found.  Please check path or run 'auto_sync.exe generate' "
            "to create a default version".format(props_filename))

    # Load the default config and merge the user values into it
    # We need to determine if there is an entry specifying the
    # folder for yml files and set it
    config = ConfigLoader.load(props_filename)
    working_dir = os.path.abspath(working_dir)
    sync_script = config.get_config('sync').require('sync_script')
    if not os.path.isabs(sync_script):
        sync_script = os.path.abspath(os.path.join(working_dir, sync_script))
    if not os.path.exists(sync_script):
        raise IOError(
            "Error - file '{}' cannot be found.  Please check path or run 'auto_sync.exe generate' "
            "to create a default version".format(props_filename))

    sync_folder = config.get_config('sync').get('sync_folder', working_dir)

    if not os.path.isabs(sync_folder):
        sync_folder = os.path.abspath(os.path.join(working_dir, sync_folder))

    if not os.path.exists(sync_folder):
        raise IOError(
            "Error - specified folder '{}' cannot be found.".format(props_filename))

    # Set the directory and read the sources
    config.set_source_dir(sync_folder)
    sync_config = config.get_config("sync")

    # Output folder for sync logs
    log_folder = os.path.join(working_dir, sync_config.get("log_folder", "logs"))
    os.makedirs(log_folder, exist_ok=True)

    # The "base" config into which sync config gets merged
    template_config = config.get_resource_config().merge_with(sync_config.values)
    template_config.set_value("log_folder", os.path.abspath(log_folder))
    if cli_options['args']:
        template_config.set_value("default_args", cli_options['args'])

    # Execute (single thread for now)
    for config in read_file(sync_script):
        sync = Sync(config)
        w = Worker(sync, template_config)
        w.run()


@cli.command()
def generate():
    if not os.path.exists("auto_sync.ini"):
        shutil.copy(get_resource("auto_sync.ini"), ".")
    else:
        print("Skipping autocreate for auto_sync.ini - file exists.")
    if not os.path.exists("example_script.yml"):
        shutil.copy(get_resource("example_script.yml"), ".")
    else:
        print("Skipping autocreate for example_script - file exists.")


if __name__ == '__main__':
    cli()
