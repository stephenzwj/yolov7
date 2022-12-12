JOB_ID=$(qsub ./scripts/run_training_in_hpc.sh | cut -d '.' -f1) && qstat -f ${JOB_ID}
# return JOB_ID to the caller
echo ${JOB_ID}