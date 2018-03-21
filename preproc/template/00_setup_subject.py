#!/usr/bin/env python3

from os.path import isfile, join, exists
from os import listdir, makedirs, walk, remove, getlogin
from nilearn import image, plotting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import fileinput
import subprocess


#---- Set subject specific variables ----#

# Set subject ID
subid = 'teach4'

# manually set scan num, type, and conds
epis = [3, 4, 5, 6, 7, 9, 10]
anat = [11]
epi_preprocs = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7']

scanCond = ['review1', 'review2', 'review3', 'review4', 'review5', 'quiz1', 'quiz2', 'anat']
preprocDirs = epi_preprocs + [0]
scanType = ['epi', 'epi', 'epi', 'epi', 'epi', 'epi', 'epi', 'anat']


#---- Set experiment-specific parameters ----#
print('\nsetting exp params...')

# Set data dir
projdir = '/mnt/bucket/labs/hasson/mai/projects/b2b_teaching/'

# Set datadir
datadir = join(projdir, 'teach_data')

# Set code dir
codedir = '/mnt/bucket/labs/hasson/mai/projects/b2b_teaching/code/preproc/bash'

# Set template dir
templatedir = '/mnt/bucket/labs/hasson/mai/projects/b2b_teaching/code/preproc/template'

# Set refdir
refdir = '/mnt/bucket/labs/hasson/mai/projects/b2b_teaching/code/preproc/ref_brains'

# Setup fsf dir
fsfdir_out = join(datadir, subid, 'preproc', 'feat_out', 'fsf')
if not exists(fsfdir_out):
    print(fsfdir_out + ' does not exist, creating')
    makedirs(fsfdir_out)


# Do nonlinear registration?
nonlinear_flag = 0


#---- Setup subject directories -----#
print('setting up sub dirs...')
subdir = join(datadir, subid)
if not exists(subdir):
    print(subdir + ' does not exist, creating')
    makedirs(subdir)

subdir_data = join(subdir, 'raw')
if not exists(subdir_data):
    print(subdir_data + ' does not exist, creating')
    makedirs(subdir_data)

subdir_log = join(subdir, 'logs')
if not exists(subdir_log):
    print(subdir_log + ' does not exist, creating')
    makedirs(subdir_log)

preproc_script_dir = join(subdir, 'preproc', 'scripts')
if not exists(preproc_script_dir):
    print(preproc_script_dir + ' does not exist, creating')
    makedirs(preproc_script_dir)



#---- Copy and modify preproc scripts for subject ----#
print('copying template scripts...')

# Setup script1: 01_convert_dcm2nii.py
template_script = join(templatedir, '01_convert_dcm2nii_template.py')
subj_script = join(preproc_script_dir, '01_convert_dcm2nii.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###EPI_NS###', str(epis), line.rstrip())
    line = re.sub('###ANAT_N###', str(anat), line.rstrip())
    line = re.sub('###PREPROC_DIRS###', str(preprocDirs), line.rstrip())
    line = re.sub('###SCAN_TYPE###', str(scanType), line.rstrip())
    line = re.sub('###SCAN_COND###', str(scanCond), line.rstrip())
    line = re.sub('###PROJ_DIR###', "'" + datadir + "'", line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + codedir + "'" , line.rstrip())

    print(line)
fileinput.close()

# Setup script: 02_run_feat.py
template_script = join(templatedir, '02_run_feat_template.py')
subj_script = join(preproc_script_dir, '02_run_feat.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###CONDS###', str(scanCond), line.rstrip())
    line = re.sub('###PROJ_DIR###', "'" + projdir + "'", line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + codedir + "'" , line.rstrip())
    line = re.sub('###DATA_DIR###', "'" + datadir + "'" , line.rstrip())

    print(line)
fileinput.close()

# Setup script: 02_run_feat_sbatch.py
template_script = join(templatedir, '02_run_feat_sbatch_template.sh')
subj_script = join(preproc_script_dir, '02_run_feat_sbatch.sh')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###CODE_DIR###', "'" + preproc_script_dir + "'" , line.rstrip())
    line = re.sub('###SUB_DIR###', subdir, line.rstrip())
    line = re.sub('###N_RUNS###', str(len(epis)) , line.rstrip())

    print(line)
fileinput.close()

# Setup script: 03_applyTransform.py
template_script = join(templatedir, '03_apply_transform_template.py')
subj_script = join(preproc_script_dir, '03_apply_transform.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + codedir + "'" , line.rstrip())
    line = re.sub('###DATA_DIR###', "'" + datadir + "'" , line.rstrip())
    line = re.sub('###REF_DIR###', "'" + refdir + "'" , line.rstrip())
    line = re.sub('###NON_LIN###', str(nonlinear_flag), line.rstrip())

    print(line)
fileinput.close()


print('\ndone!\n')
