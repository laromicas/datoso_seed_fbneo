import os
from datetime import datetime
from pathlib import Path
import shutil
import urllib.request
import zipfile
from datoso_seed_fbneo import __preffix__

from datoso.configuration import config, logger
from datoso.helpers import parse_folder

url = 'https://github.com/libretro/FBNeo/archive/refs/heads/master.zip'

class Folders:
    download = None
    dats = None
    backup = None
    full = None
    light = None

    @staticmethod
    def create(full=True, light=False):
        base_path = parse_folder(config['PATHS'].get('DownloadPath', 'tmp'))
        Folders.download = os.path.join(base_path, __preffix__)
        Folders.dats = os.path.join(Folders.download, 'dats')
        # Clean dats folder
        if os.path.exists(Folders.dats):
            shutil.rmtree(Folders.dats)
        os.makedirs(Folders.dats, exist_ok=True)
        Folders.backup = os.path.join(Folders.download, 'backup')
        os.makedirs(Folders.backup, exist_ok=True)
        Folders.full = os.path.join(Folders.dats, 'full')
        if full:
            os.makedirs(Folders.full, exist_ok=True)
        Folders.light = os.path.join(Folders.dats, 'light')
        if light:
            os.makedirs(Folders.light, exist_ok=True)

def download():
    logger.info(f'Downloading {url} to {Folders.download}\n')
    urllib.request.urlretrieve(url, os.path.join(Folders.download, 'fbneo.zip'))
    logger.info(f'Extracting dats from {Folders.download}\n')

def extract_dats(full=True, light=False):
    with zipfile.ZipFile(os.path.join(Folders.download, 'fbneo.zip'), 'r') as zip_ref:
        filelist = [f for f in zip_ref.filelist if f.filename.startswith('FBNeo-master/dats/') and f.filename.endswith('.dat')]
        filelist_full = [f for f in filelist if '/light/' not in f.filename]
        filelist_light = [f for f in filelist if '/light/' in f.filename]
        if full:
            for file in filelist_full:
                file_name = file.filename
                file.filename = Path(file_name).name
                zip_ref.extract(file, Folders.full)
                file.filename = file_name
        if light:
            for file in filelist_light:
                file_name = file.filename
                file.filename = Path(file_name).name
                zip_ref.extract(file, Folders.light)
                file.filename = file_name

def backup():
    logger.info(f'Making backup from {Folders.dats}\n')
    backup_daily_name = f'fbneo-{datetime.now().strftime("%Y-%m-%d")}.zip'
    with zipfile.ZipFile(os.path.join(Folders.backup, backup_daily_name), 'w') as zip_ref:
        for root, dirs, files in os.walk(Folders.dats):
            for file in files:
                zip_ref.write(os.path.join(root, file), arcname=os.path.join(root.replace(Folders.dats, ''), file), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    logger.info(f'Backup created at {Folders.backup}\n')

def clean():
    logger.info(f'Cleaning {Folders.download}\n')
    os.remove(os.path.join(Folders.download, 'fbneo.zip'))

def fetch():
    fetch_full = config['FBNEO'].getboolean('FetchFull', True)
    fetch_light = config['FBNEO'].getboolean('FetchLight', False)
    Folders.create(full=fetch_full, light=fetch_light)
    download()
    extract_dats(full=fetch_full, light=fetch_light)
    backup()
    clean()

if __name__ == '__main__':
    fetch()