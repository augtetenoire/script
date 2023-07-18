#!/bin/bash
#
#SBATCH --job-name=gaussian_optimization
#SBATCH --output=output_gaussian_%j.out
#SBATCH --ntasks=36
#SBATCH --time=5-00:00:00
#SBATCH --partition=long_36_64
#SBATCH --mail-user=auguste.tetenoire@univ-rennes.fr
#SBATCH --mail-type=FAIL,REQUEUE,INVALID_DEPEND,STAGE_OUT





#Name of the directory where you will do the calculation
directory=/tmp/job_${SLURM_JOB_ID}_${SLURM_JOB_NAME}

# Create working directory
mkdir ${directory}

# directories where datas are stored
DD=${SLURM_SUBMIT_DIR}

# Name of the gaussian input file
input_files="input.gjf"

# copy files in the working directory
for i in *.gjf *.chk ; do
cp -rv ${i} ${directory}/.
done


#write that the calculation start
echo ${directory} ${SLURM_JOB_NODELIST} >> /home/users/${USER}/slurm.log.working


echo $SLURM_JOB_NODELIST  >> ${DD}/mpd.hosts


cat >> /home/users/${USER}/slurm.log <<EOF
################################################################
$(date +'%A %d %B (%D) %Hh%M')

${SLURM_JOB_ID}
${SLURM_JOB_NAME}
${SLURM_SUBMIT_DIR}
$(echo ${SLURM_JOB_NODELIST})

nodes=${SLURM_JOB_NUM_NODES}:ppn${SLURM_CPUS_ON_NODE}
$(sed -n '5p' "$(realpath ${0})" | awk '{print $2}' )
$(sed -n '2p' "$(realpath ${0})" | awk '{print $2}' )
EOF


echo '======================'
echo '======================'
echo ''
echo "Starting at `date +"%D%t%A%t%T"`"
echo ''
echo '======================'
echo '======================'
echo ''


# load compiler
if [[ $SLURM_JOB_PARTITION == *"AMD"* ]]; then
sudo chgrp -R users /cluster_cti/bin/gaussian
export g16root=/cluster_cti/bin/gaussian/new_g16_OK
. $g16root/g16/bsd/g16.profile

. /opt/intel/oneapi/setvars.sh


else
sudo chgrp -R users /cluster_cti/bin/gaussian
export g16root=/cluster_cti/bin/gaussian/new_g16_OK
. $g16root/g16/bsd/g16.profile 

source /opt/intel/compilers_and_libraries_2017/linux/bin/compilervars.sh intel64

fi



# go to working directory
cd ${directory}


# Def function of periodic copy
recopie-periodique ()
{
  tjsPresent=`ls -l $TMPDIR | wc -l`

  delai=10 # pour recopie des le demarrage du calcul

  while [ $tjsPresent -gt 0 ]
  do

    sleep $delai

    touch *

    echo "Copie fichier : `date`"

    cp -rv ${directory} ${DD}/working_save.tmp

    tjsPresent=`ls -l $TMPDIR | wc -l`

    delai=3600 # augmentation du delai pour limiter l'utilisation de la bande passante

  done
}




recopie-periodique &

# Run the code
g16 < ${input_files} > ${SLURM_JOB_NAME}.log




cd ${DD}
# Retrieve data
mv ${DD}/mpd.hosts ${directory}/.
mv ${directory} ${DD}/.
rm -r ${DD}/working_save.tmp

# Write that calculation ended
cat >> /home/users/${USER}/slurm.log.end <<EOF
################################################################
$(date +'%A %d %B (%D) %Hh%M')

${SLURM_JOB_ID}
${SLURM_JOB_NAME}
${SLURM_SUBMIT_DIR}
$(echo ${SLURM_JOB_NODELIST})

nodes=${SLURM_JOB_NUM_NODES}:ppn${SLURM_CPUS_ON_NODE}
$(sed -n '5p' "$(realpath ${0})" | awk '{print $2}' )
$(sed -n '2p' "$(realpath ${0})" | awk '{print $2}' )
EOF

sed -i "s/${directory} ${SLURM_JOB_NODELIST}//" /home/users/${USER}/slurm.log.working

echo '======================'
echo '======================'
echo ''
echo "Ending at `date +"%D%t%A%t%T"`"
echo ''
echo '======================'
echo '======================'
echo ''