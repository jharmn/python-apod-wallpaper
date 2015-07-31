import os
from io import open
from future.standard_library import install_aliases
install_aliases()
from glob import glob
from urllib.parse import urlparse
from urllib.request import urlopen

from . import date_utils

def download_url(url, single_date, download_path):
    path = expand_download_path(download_path)
    file = file_path(url, path, single_date)
    save_url(url, file)
    return file

def save_url(url, file):
    print("Saving image: {}".format(file))
    with urlopen(url) as response, open(file, "wb") as out_file:
        data = response.read()
        out_file.write(data)

def expand_download_path(download_path):
    path = os.path.expanduser(download_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def file_path(url, download_path, single_date):
    path = urlparse(url).path
    image_name = path.split("/")[-1]
    return os.path.join(download_path, 
        date_utils.format_date(single_date)+"_"+image_name)

def file_date_glob(download_path, single_date):
    path = expand_download_path(download_path)    
    path_glob = os.path.join(path, date_utils.format_date(single_date))
    path_glob += "*"
    return path_glob

def file_date_exists(download_path, single_date):
    date_list = glob(file_date_glob(download_path, single_date))
    return len(date_list) > 0