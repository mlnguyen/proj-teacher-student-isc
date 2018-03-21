#!/bin/bash
#
# apply_transform.sh
#
# Applies affine transformation to subject EPI, moving from subject space to 3mm MNI
# space. Data was collected in 3mm space with a 1 mm structural image. This script assumes
# that the original functional data was aligned to a 2mm MNI brain in a separate processing
# step using FEAT. We then combine the function->2mm MNI transformation with a 2mm->3mm
# MNI transformation.
#

module load fsl

NIFTI_IN=$1
NIFTI_OUT=$2
REF_DIR=$3
FEAT_DIR=$4


# Combine transforms:(1) subject space to MNI 2mm, and (2) MNI
# 2 mm to 3mm. Outputs a new transform that is subject space --> 3mm MNI
# Arguments: -omat <outputfile>, -concat <trans_mat1, trans_mat2, ...>
if [ -e $FEAT_DIR/reg/example_func2standard_3mm.mat ]
then
	echo 'xform already exists, skipping step'
else
	echo 'combining xforms...'
	convert_xfm -omat $FEAT_DIR/reg/example_func2standard_3mm.mat \
			-concat  $REF_DIR/transmat_2mm_to_3mm.mat $FEAT_DIR/reg/example_func2standard.mat
fi

# Apply transformations: subject space --> MNI 3mm
echo 'applying transform...'
flirt -in $NIFTI_IN -out $NIFTI_OUT -ref $REF_DIR/MNI152_T1_3mm_brain.nii \
		-init $FEAT_DIR/reg/example_func2standard_3mm.mat -applyxfm

echo 'done!'
