1. Open jupyter notebook on spock
    1. In a terminal window, ssh into spock: 
        * ssh -X userName@spock.pni.princeton.edu
    2. Navigate to the project directory
        * cd /jukebox/hasson/mai/projs/b2b_teaching 
    3. Start a notebook
        1. module load pyger
        2. jupyter notebook --no-browser --port=8889
    4. Open a new tab in the terminal. Open a ssh tunnel
        1. ssh -N -f -L localhost:8889:localhost:8889 userName@spock.pni.princeton.edu
        2. Note that if port 8889 is busy (you’ll see this in step 3), the notebook may have opened in a different port. If so, change the second 8889 to whatever number that is
    5. Go back to your original terminal tab. At the bottom there will be a http:// address. Copy this to your browser window. This should open the jupyter notebooks
    6. Ref: https://coderwall.com/p/ohk6cg/remote-access-to-ipython-notebooks-via-ssh
2. Mount the fileserver from your finder window
    1. Finder -> cmd + k
    2. Server address: smb://bucket.pni.princeton.edu/hasson
    3. Enter, enter password if needed
    4. Navigate in finder to hasson/mai/projects/b2b_teaching/skyra_learning
    5. Open the excel sheet, b2b_subj_list.xlsx
3. In the browser window, navigate to code/preproc/notebooks
4. Convert dicom to nifti
    1. Open 01_convert_dcm2nifti.ipynb
    2. Change subid, epis, anat as appropriate for current subject. You can get the EPI numbers from the subj list excel sheet
    3. Run code.
    4. Check that everything succeeded
        1. Does the scanInfo look reasonable?
        3. Does the nifti_good dir contain the correct nifti files? Do the names of the files make sense?
        4. Did the re-oriented brain image wind up in the data dir?
5. Brain extraction. Next we want to extract just the brain from the anatomical image.
    1. In the terminal window, ssh into spock again. Navigate to the subject directory 
        1. cd /jukebox/hasson/mai/projects/b2b_teaching/skyra_learning/data/SUB_ID
    2. View the data using fslview
        1. module load fsl
        2. fslview_deprecated &
        3. Open the subject’s anatomy: file —> Open —> dayXX/data/subid_t1w_reorient.nii.gz
        4. Now click around this image until you get a point approximately in the center of the brain. Get the coordinates in the lower left corner 
    3. Open the brain extraction tool. Back in the terminal:
        1. Bet &
        2. Click upper right folder to select the input file (this is the reoriented brain image in data: day1/data/s01_t1w_reorient.nii.gz )
        3. Change fractional intensity to ~0.35
        4. Change “Run standard brain extraction using bet2” to “robust brain centre estimation”
        5. Enter the center of the brain coordinates from fslview in the bottom row
        6. Go!
            1. This will take a few seconds. If you check the terminal window, when it’s done, it’ll say something like “finished”
    4. Now go back to fslview to check how well it did.
        1. Add image: File -> Add -> subID_t1w_reorient_brain.nii.gz
        2. Change the color of the brain to hot. 
            1. Highlight the scan you want, and then click the square with an i in it. 
            2. Change “Lookup table options" from “grayscale" to “Red-Yellow”
        3. Now click around the brain image and check that the outline is pretty good. It’s not missing a lot of the brain, and it’s not including lots of non-brain stuff. Here’s a good example:
    5. If the brain extraction didn’t do a good job, repeat steps 2 and 3. You can try changing the center coordinates or changing the fractional intensity.
    6. When you’re satisfied, close fslview and Bet
6. Back in our jupyter notebooks, open 02_run_feat.ipynb. This is a wrapper python notebook that is going to launch a FEAT job, which is the name of the preprocessing tool from FSL. Feat takes a really long time to run, so we’re going to run it on the server.
    1. Change subject id and this_scan 
        1. For Day 1 data, we have two EPI scans that need to be preprocessed. So we’ll need to run this whole thing twice. Once with this_scan=1, and a second time with this_scan=2
    2. Run code
    3. This will start a Feat preprocessing job, which takes awhile to run (30-60 min). You can check the status of your job by going into your finder window:
        1. Navigate to your subject’s directory. There will be a new directory called “preproc.” Inside preproc, we now have feat_out, which contains “fsf” and “runXX.feat” (where x is the scan scan number)
        2. Inside the run folder, there’s a whole ton of files that are created by feat. You want the one called “report_log.html.” Double click to open
        3. This opens a really hideous progress report for FEAT. While feat is still running, it’ll say at the top something like “running.” If it stopped due to an error, it’ll say something like “finished with errors.” If it’s all done, it won’t say anything.
    4. Repeat steps 1-3 for this_scan=2.

When FEAT has completed:
1. Start in project directory: /jukebox/hasson/mai/projects/b2b_teaching
2. Open setup subject file:
    1. nano code/preproc/template/00_setup_subject.py 
    2. Edit subject info for this subject:
        1. subid
        2. epis
        3. anat
        4. preproc directories
        5. scanConds
        6. scantype
    3. Save and exit: ctrl+x, then “y” for yes
3. Run the file
    1. module load pyger
    2. python code/preproc/template/00_setup_subject.py 
    3. You should see an output in the terminal saying it created a bunch of directories/files
4. Go to the subject’s directory and check the files
    1. cd skyra_learning/data/s01/day1/
    2. Inside the current subject/day, there should be new directories “feat_out”,  “scripts”, and “logs”.  Scripts should contain several python/bashs cripts, featout just a directory containing fsf
5. Run convert_dcm2nii script
    1. python preproc/scripts/01_convert_dcm2nii.py
    2. This should take a few minutes. The script will output status updates to the terminal window. At the end, it’ll print some scan info. 
    3. Check that the scan info looks reasonable. Check that raw/nifti_good contains the actual niftis and that the number/naming matches what’s in the subj_list excel sheet
6. Extract brain (as before) using Bet and fslview
7. Back in the terminal, run feat
    1. sbatch preproc/scripts/02_run_feat_sbatch.sh
    2. This will automatically start a feat preprocessing job for each of the EPIs for the given subject. It usually takes around 30-60 min.
    3. Some important slurm commands for interacting with the scheduler
        1. sbatch scriptName.sh #submits a joab
        2. squeue -u userName #check on your jobs
        3. scancel -u userName #cancel all of your jobs
        4. scancel -n jobName #cancel jobs with jobName
    4. In addition to squeue, you can check the progress of your job using the report.html file as before.
    5. If everything crashes or doesn’t start, the first place to check is your log file for the job:
        1. nano logs/prep-JOBNUMBER_ARRAYNUMBER.log
        2. If something crashed, you should see an error message here
8. Make a note on the subj_list excel sheet that you’re currently running feat on the subject under the “status” column (e.g. “running feat (AC)”). While Feat is running, you can repeat steps 1-7 on other subjects. Often, I’ll run like a batch of 10 subjects, and then when all the jobs have finished, go on to step 9. Whatever you prefer.
9. When Feat is completed, check the feat report and make sure it all looks good. If the registration or motion correction looks bad, make a note of it on the sub_list excel sheet in the “notes” column.
10. Back in the terminal, run apply_transform
    1. python preproc/scripts/03_apply_transform.py
    2. This should take a few minutes as well. At the end, you should have nice, preprocessed niftis with informative names in subID/day1/data
11. Done!



















