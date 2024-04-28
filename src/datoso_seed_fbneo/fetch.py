import os
import zipfile
from datetime import datetime
from pathlib import Path

from dateutil import tz

from datoso.configuration import config, logger
from datoso.configuration.folder_helper import Folders
from datoso.helpers import show_progress
from datoso.helpers.download import downloader
from datoso_seed_fbneo import __prefix__

url = 'https://github.com/libretro/FBNeo/archive/refs/heads/master.zip'

def download(folders):
    logger.info(f'Downloading {url} to {folders.download}\n')
    downloader(url=url, destination=folders.download / 'fbneo.zip', reporthook=show_progress)
    logger.info(f'Extracting dats from {folders.download}\n')

def extract_dats(folders, full=False, light=False):
    with zipfile.ZipFile(folders.download / 'fbneo.zip', 'r') as zip_ref:
        filelist = [f for f in zip_ref.filelist if f.filename.startswith('FBNeo-master/dats/') and f.filename.endswith('.dat')]
        filelist_full = [f for f in filelist if '/light/' not in f.filename]
        filelist_light = [f for f in filelist if '/light/' in f.filename]
        if full:
            for file in filelist_full:
                file_name = file.filename
                file.filename = Path(file_name).name
                zip_ref.extract(file, folders.dats / 'full')
                file.filename = file_name
        if light:
            for file in filelist_light:
                file_name = file.filename
                file.filename = Path(file_name).name
                zip_ref.extract(file, folders.dats / 'light')
                file.filename = file_name

def backup(folders):
    logger.info(f'Making backup from {folders.dats}\n')
    backup_daily_name = f'fbneo-{datetime.now(tz.tzlocal()).strftime("%Y-%m-%d")}.zip'
    with zipfile.ZipFile(folders.backup / backup_daily_name, 'w') as zip_ref:
        for root, _, files in os.walk(folders.dats):
            for file in files:
                zip_ref.write(Path(root) / file, arcname=Path(root).relative_to(folders.dats) / file, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    logger.info(f'Backup created at {folders.backup}\n')

def clean(folders):
    logger.info(f'Cleaning {folders.download}\n')
    path = folders.download / 'fbneo.zip'
    if path.exists():
        path.unlink()

def fetch():
    fetch_full = config['FBNEO'].getboolean('FetchFull', True)
    fetch_light = config['FBNEO'].getboolean('FetchLight', False)
    extras = []
    if fetch_full:
        extras.append('full')
    if fetch_light:
        extras.append('light')

    folder_helper = Folders(seed=__prefix__, extras=extras)
    folder_helper.clean_dats()
    folder_helper.create_all()

    download(folder_helper)
    extract_dats(folder_helper, full=fetch_full, light=fetch_light)
    backup(folder_helper)
    clean(folder_helper)

if __name__ == '__main__':
    fetch()
