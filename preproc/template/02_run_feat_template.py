
#!/usr/bin/env python3


# python imports
from os import listdir, makedirs, walk, remove, getlogin
import sys
from os.path import isfile, join, exists
import subprocess
import numpy as np
import shutil
import pandas as pd
import socket
from nilearn import image, plotting

# ----- Set params for this run --------------------------
print('\nsetting up params...')
# Which subjects? #
subj = ###SUB_ID###

# Which scan number?
this_scan = sys.argv[1]

# Set projdirs dir
projdir = ###PROJ_DIR###
datadir = ###DATA_DIR###
subdir = join(datadir, subj)

# Set code dir
codedir = ###CODE_DIR###

# Set raw dir
rawdir = join(subdir, 'raw', 'niftis_good')

# Set output dir for fsf files
fsfdir_out = join(subdir, 'preproc', 'feat_out', 'fsf')

# -----FEAT: preprocessing ------------------------------------------------------
# Load scanInfo
scanInfo = pd.read_csv(join(subdir, 'scanInfo.csv'), index_col=0)

# EPI to use in feat; output of applywarp step
epiInfo = scanInfo.loc[['epi']]
for ind,row in epiInfo.iterrows():
	if row['preprocDir'] == 'run'+str(this_scan):
		epi_in = join(rawdir, row['scanName'])
		break

print('\nepi: ' + epi_in + '\n')

# Anatomy to use in feat
anat_file = join(subdir, 'data', scanInfo.loc['anat_brain']['scanName'])

# Feat directory
preproc_dir = join(subdir, 'preproc', 'feat_out')

# FSf template
fsf_template = join(projdir, 'code', 'preproc', 'template', 'feat_template_b2b.fsf')

# Run
print('\ngo!\n\n')
output = subprocess.check_output([join(codedir, 'run_feat.sh'), str(this_scan), epi_in, anat_file, preproc_dir, fsf_template])
print(output)




