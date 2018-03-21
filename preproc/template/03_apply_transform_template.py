#!/usr/bin/env python3

# python imports
from os import listdir, makedirs, walk, remove, getlogin
import sys
from os.path import isfile, join, exists
import subprocess
import numpy as np
import pandas as pd

# Set params for experiment --------------------------------------------------------
print('\n\nsetting up params...')

# Which subjects? #
subj = ###SUB_ID###

# Set projdirs dir
datadir = ###DATA_DIR###
subdir = join(datadir, subj)

# Set codedir
codedir =  ###CODE_DIR###

# Set refdirs
refdir =  ###REF_DIR###

# Do nonlinear?
nonlinear_flag = ###NON_LIN###

# Do transform --------------------------------------------------------------------
print('starting transforms...\n')

# load scanInfo
scanInfo = pd.read_csv(join(subdir, 'scanInfo.csv'), index_col=0)
epiInfo = scanInfo.loc[['epi']]

for ind,row in epiInfo.iterrows():

	print('applying transform to ' + row['preprocDir'] + '...')
	feat_outdir = join(subdir, 'preproc', 'feat_out', row['preprocDir']+'.feat')
	orig_nifti = join(feat_outdir, 'filtered_func_data.nii.gz')
	out_nifti = join(subdir, 'data', subj + '_epi_' + row['scanCond'] + '.nii.gz')

	if nonlinear_flag == 1:
	 	output = subprocess.check_output([join(codedir, 'apply_transform_nonlin.sh'), orig_nifti,
 							out_nifti, feat_outdir, join(refdir, 'MNI152_T1_3mm_brain')])
	else:
		output = subprocess.check_output([join(codedir, 'apply_transform.sh'), orig_nifti,
							out_nifti, refdir, feat_outdir])


	print('\n')
