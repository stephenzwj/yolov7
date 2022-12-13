#!/bin/bash
### accept the job name as the first argument and print it
echo "Job name is $1"
### run the job name as a command
job_outputs=$($1)

### print the job outputs
echo "$job_outputs"