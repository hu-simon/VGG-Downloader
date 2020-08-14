# VGG-Downloader
Downloads the VGG Lipreading Datasets located at https://www.robots.ox.ac.uk/~vgg/data/lip_reading/

**Important**: To download the datasets, you need a username and a password, provided by the BBC. See https://www.bbc.co.uk/rd/projects/lip-reading-datasets for more details.

### Usage
URLs and MD5 checksums for each of the datasets are located at ``./lists/`` and should be updated if necessary. 

The following script can be used to download and prepare the LRS2 dataset.

```
python ./download_vgg.py --save_path /home/shu/VGG_Lipreading/LRS2 --download --username USER --password PASSWORD
python ./download_vgg.py --save_path /home/shu/VGG_Lipreading/LRS2 --extract
```

