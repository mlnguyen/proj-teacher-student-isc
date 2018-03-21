
#!/usr/bin/env python3

from os.path import isfile, join, exists
from os import listdir, makedirs, walk, remove, getlogin
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess


# -----------------------------------
# Set subject-specific parameters
print('\nsetting up sub/exp params...')

# Set subject ID
subid = ###SUB_ID###

# read in subj params
epis = ###EPI_NS###
anat = ###ANAT_N###

# ---------------------------------
### Set experiment-specific parameters #####

# Set data dir
projdir = ###PROJ_DIR###

#Set code dir
codedir = ###CODE_DIR###

# Set rawdata path
rawdir = join(projdir, subid, 'raw', 'dcm')

# Set savefile
savefile = join(projdir, subid, 'scanInfo.csv')

# Set output dir
outputdir = join(projdir, subid, 'raw', 'niftis_good')
if not exists(outputdir):
    print(outputdir + ' does not exist, creating')
    makedirs(outputdir)

# Set final outputdir for anats
anatdir = join(projdir, subid, 'data')
if not exists(anatdir):
    print(anatdir + ' does not exist, creating')
    makedirs(anatdir)

# ----- Convert dicoms to niftis ------------------------------------------------
# This script copies dicoms from the raw directory to the nifti preproc dir.
# Then it unzips everything and converts dicoms to niftis. Finally, it deletes
# the original dicoms.
print('converting dicoms to niftis...')
subprocess.check_call([join(codedir, 'prep_and_dcm2nii.sh'), rawdir, outputdir])


# check niftis
print('\nniftis output by dcm2niix:')
subprocess.check_call(['ls', outputdir])


# ----- Make scan info df ------------------------------------------------------
print('\nsaving scan info...')

# Create subject information file
scanNum = epis + anat
scanType = ###SCAN_TYPE###
scanCond = ###SCAN_COND###
preprocDir = ###PREPROC_DIRS###

# automatically get scan names
scanNames = np.array([])
niftis_all = listdir(outputdir)
for i in scanNum:
    for filename in niftis_all:
        if str(i) + '_' in filename:
            scanNames = np.append(scanNames, filename)
            break

# make dataframe
df = pd.DataFrame({'scanNum': scanNum,'scanCond': scanCond, 'scanName':scanNames,
					'preprocDir': preprocDir}, index=scanType)


# ---- Reorient and copy anatomy ----------------------------------------------
anat_orig = join(outputdir, df.loc['anat']['scanName'])
anat_reorient = join(anatdir, subid + '_t1w_reorient.nii.gz')
output = subprocess.check_output([join(codedir, 'run_reorient.sh'), anat_orig, anat_reorient])


# add niftis to scan info
newNiftis = pd.DataFrame({'scanName': [subid + '_t1w_reorient.nii.gz', subid + '_t1w_reorient_brain.nii.gz'],
                          'scanNum': [anat[0], anat[0]], 'scanCond': ['anat', 'anat'],
                          'preprocDir': [0,0]}, index=['anat_reorient', 'anat_brain'] )
df = df.append(newNiftis)
df.to_csv(join(projdir, subid, 'scanInfo.csv'))

# if everything looks fine, save dataframe to subjects dir
df.to_csv(savefile)

print(df)

print('\n**** done!\n')






