#!/bin/bash
#
# apply_transform.sh


module load fsl

NIFTI_IN=$1
NIFTI_OUT=$2
REF_DIR=$3
FEAT_DIR=$4

flirt -in $NIFTI_IN -ref $REF_DIR/MNI152_T1_3mm_brain -init $FEAT_DIR/reg/example_func2standard.mat \
		-out  $NIFTI_OUT -applyxfm

