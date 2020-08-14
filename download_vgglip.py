import os
import pdb
import time
import glob
import hashlib
import requests
import argparse
import subprocess
from tqdm import tqdm
from zipfile import ZipFile
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="VGG Lipreading Dataset Downloader")

parser.add_argument(
    "--save_path", type=str, help="Target directory to store the data", required=True
)
parser.add_argument(
    "--filenames",
    type=str,
    help="Text file containing the download links and MD5 checksum.",
    required=True,
)
parser.add_argument("--user", type=str, help="Username", required=True)
parser.add_argument("--password", type=str, help="Password", required=True)

parser.add_argument(
    "--download", dest="download", action="store_true", help="Enable download mode"
)
parser.add_argument(
    "--extract", dest="extract", action="store_true", help="Enable extraction mode"
)
parser.add_argument(
    "--convert", dest="convert", action="store_true", help="Enable conversion mode"
)

args = parser.parse_args()


def md5(fname):
    """Confirms the MD5 Checksum.

    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def download(args, lines):
    pass


if __name__ == "__main__":
    a = 1
