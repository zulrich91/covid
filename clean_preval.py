# Script to clean the prevalence datasets

from pathlib import Path, PurePath
import pandas as pd
import glob
import os

PREVAL_BASE = './data/prevalence/'
PREVAL_FOLDERS = listdirs(PREVAL_BASE)

def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def clean_data():
    for folder in PREVAL_FOLDERS:
        columns = ['code', 'region',folder]
        CLEAN_FOLDER = PREVAL_BASE+folder+"/clean/"
        FILES = glob.glob(PREVAL_BASE+folder+"/*.csv")
        for file in FILES:
            df = pd.read_csv(file, encoding='utf-8', sep=";",header=2)
            df.columns = columns
            df.to_csv(CLEAN_FOLDER+PurePath(file).parts[-1], index=False)
    print('done')


