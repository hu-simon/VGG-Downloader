"""
Python script that downloads the VGG Lipreading Dataset from the BBC.

NOTE
* This entire script needs testing on the two datasets that we have available to us (LRS2 and LRS3).
* Everything should be done on the .26 machine for speed and ease. Try first on a small subset and then expand it to the entire thing.
"""

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
parser.add_argument("--username", type=str, help="Username", required=True)
parser.add_argument("--password", type=str, help="Password", required=True)
parser.add_argument(
    "--url_list",
    type=str,
    help="Path to .txt file containing the download URLs and MD5 checksums.",
    required=True,
)

parser.add_argument(
    "--download", dest="download", action="store_true", help="Enable download mode"
)
parser.add_argument(
    "--extract", dest="extract", action="store_true", help="Enable extraction mode"
)

args = parser.parse_args()


def check_md5(fname):
    """Confirms the MD5 Checksum.

    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def download(args, lines):

    for line in lines:
        url = line.split()[0]
        md5_truth = line.split()[1]
        output_file = url.split("/")[-1]

        result = subprocess.call(
            "wget {} --user {} --password {} -O {}/{}".format(
                url, args.username, args.password, args.save_path, output_file
            ),
            shell=True,
        )
        if result != 0:
            raise ValueError("[ERROR] Download failed for {}".format(url))

        md5_check = check_md5("{}/{}".format(args.save_path, output_file))
        if md5_check == md5_truth:
            print("[INFO] Checksum successful for {}".format(output_file))
        else:
            raise ValueError("[ERROR] Checksum failed for {}".format(output_file))


def extract(args):

    files = glob.glob("{}/*.zip".format(args.save_path))

    for file_name in files:
        print("[INFO] Extracting {}".format(file_name))
        zipfile = ZipFile(file_name, "r")
        zipfile.extractall(args.save_path)
        zipfile.close()


def concatenate(args, lines):

    for line in lines:
        input_file = line.split()[0]
        output_file = line.split()[1]
        md5_truth = line.split()[2]

        result = subprocess.call(
            "cat {}/{} > {}/{}".format(
                args.save_path, input_file, args.save_path, output_file
            ),
            shell=True,
        )
        if result != 0:
            raise ValueError("[ERROR] Concatenation failed for {}".format(output_file))

        md5_check = check_md5("{}/{}".format(args.save_path, output_file))
        if md5_check == md5_truth:
            print("[INFO] Checksum successful for {}".format(output_file))
        else:
            raise ValueError("[ERROR] Checksum failed for {}".format(output_file))

        result = subprocess.call(
            "rm {}/{}".format(args.save_path, input_file), shell=True
        )


if __name__ == "__main__":

    if not os.path.exists(args.save_path):
        raise ValueError("Target directory does not exist.")

    f = open(args.url_list, "r")
    urls = f.readlines()
    f.close()

    # Need to figure out what file_names containes here.

    if args.download:
        download(args, urls)

    if args.extract:
        concatenate(args, file_names)
        extract(args)
