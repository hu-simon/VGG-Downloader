"""
Python script that updates the URLs for the VGG Lipreading Datasets.
"""

import os

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def _get_info(base_url):
    """Scrapes ``base_url`` for the URLs where the data are stored.

    Parameters
    ----------
    base_url : str
        The URL of the main download page.
    
    Returns
    -------
    download_urls : list
        List containing the URLs where the data are stored.
    
    """
    dataset_name = base_url.split("/")[-1].split(".")[0]

    request = requests.get(base_url)
    soup = BeautifulSoup(request.content, "html.parser")
    all_urls = soup.findAll("a")

    if dataset_name == "lrw1":
        expression = "./data1"
    elif dataset_name == "lrs2":
        expression = "./data2"
    else:
        expression = "./data3"

    filtered_urls = list()
    for url in all_urls:
        if expression in str(url.get("href")):
            filtered_urls.append(url.get("href"))

    filtered_urls = [".".join(url.split(".")[1:]) for url in filtered_urls]
    download_urls = ["/".join(base_url.split("/")[:-1]) + url for url in filtered_urls]

    return download_urls


def _write(root_path, base_url):
    """Writes the download and checksum information to a file.

    Paramters
    ---------
    root_path : str
        The absolute path to the folder where the text file should be written.
    base_url : str
        The URL of the main download page. This is passed on to _get_info().

    """
    dataset_name = base_url.split("/")[-1].split(".")[0]
    dataset_name = dataset_name.upper()
    download_urls = _get_info(base_url)

    with open(os.path.join(root_path, "{}.txt".format(dataset_name)), "w") as f:
        for url in download_urls:
            f.write(url + "\n")
        f.close()


if __name__ == "__main__":
    base_urls = [
        "https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrw1.html",
        "https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs2.html",
        "https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs3.html",
    ]

    root_path = "/Users/shu/Documents/scripts"
    for _, base_url in tqdm(enumerate(base_urls)):
        _write(root_path, base_url)

