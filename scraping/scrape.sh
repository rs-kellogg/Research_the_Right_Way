#!/bin/sh

# load python anaconda library
module load python-anaconda3/2019.10

# load firefox
module load chrome/72


# create a conda environment for web scraping the right way
conda env create -f ~/Research_the_Right_Way/scraping/harvest.yml
