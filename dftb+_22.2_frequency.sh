#!/bin/bash
#
#SBATCH --job-name=frequency_calculation
#SBATCH --output=output_%j.out
#SBATCH --error=error_%j.err
#SBATCH --ntasks=Nan
#SBATCH --time=Nan
#SBATCH --partition=Nan
#SBATCH --mail-user=auguste.tetenoire@univ-rennes1.fr
#SBATCH --mail-type=FAIL,REQUEUE,INVALID_DEPEND,STAGE_OUT


#Name of the directory where you will do the calculation
directory_name=${SLURM_JOB_ID}_${SLURM_JOB_NAME}
directory=/tmp/job_${directory_name}


# Create working directory
mkdir ${directory}

# directories where datas are stored
DD=${SLURM_SUBMIT_DIR}


# copy files in the working directory
for i in *.gen *.hsd ; do
cp -rv ${i} ${directory}/.
done


#write that the calculation start
echo ${directory} ${SLURM_JOB_NODELIST}>> /home/users/${USER}/slurm.log.working


echo $SLURM_JOB_NODELIST  >> ${DD}/mpd.hosts


cat >> /home/users/${USER}/slurm.log <<EOF
################################################################
$(date +'%A %d %B (%D) %Hh%M')

${SLURM_JOB_ID}
${SLURM_JOB_NAME}
${SLURM_SUBMIT_DIR}
${SLURM_JOB_NODELIST}

nodes=${SLURM_JOB_NUM_NODES}:ppn${SLURM_CPUS_ON_NODE}
${SLURM_NTASKS}
$(squeue -j ${SLURM_JOB_ID} -h --Format TimeLimit)
echo ${SLURM_JOB_PARTITION}
EOF



echo '======================'
echo '======================'
echo ''
echo "Starting at `date +"%D%t%A%t%T"`"
echo ''
echo '======================'
echo '======================'
echo ''



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

    delai=3000 # augmentation du delai pour limiter l'utilisation de la bande passante

  done
}

# Def function of periodic top
top-periodique ()
{
  tjsPresent=`ls -l $TMPDIR | wc -l`

  delai=10 # pour recopie des le demarrage du calcul

  while [ $tjsPresent -gt 0 ] 
  do

    sleep $delai

    touch *

    echo "Copie fichier : `date`"

    echo >> ${DD}/top_output.out
    date +"%D%t%A%t%T" >> ${DD}/top_output.out   
    echo >> ${DD}/top_output.out
    top -b -n 1 |head -n 50 >> ${DD}/top_output.out

    tjsPresent=`ls -l $TMPDIR | wc -l`

    delai=300 # augmentation du delai pour limiter l'utilisation de la bande passante

  done
}





recopie-periodique &
top-periodique &

# Run the code

export OMP_NUM_THREADS=${SLURM_NTASKS}
#export OMP_NUM_THREADS=36

if [[ $SLURM_JOB_PARTITION == *"AMD"* ]]; then
. /opt/intel/oneapi/setvars.sh
ulimit -s hard
else
#source /opt/intel/intel_2020/compilers_and_libraries/linux/bin/compilervars.sh intel64
. /opt/intel/oneapi/setvars.sh
ulimit -s hard
fi




mkdir frozen_slab free_slab

cp *.gen *.hsd frozen_slab/.
(
cd frozen_slab

sed -i "7s/Nan/225:-1/" dftb_in.hsd
sed -i "8s/Nan/225:-1/" modes_in.hsd

/cluster_cti/bin/DFTB+/dftbplus-22.2/bin/dftb+ > ${directory}/frozen_slab/output_dftb_${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
/home/users/atetenoire/bin/dftbplus-22.2.x86_64-linux/bin/modes > ${directory}/frozen_slab/modes_dftb_${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
)

cp *.gen *.hsd free_slab/.
(
cd free_slab

sed -i "7s/Nan/57:-1/" dftb_in.hsd
sed -i "8s/Nan/57:-1/" modes_in.hsd

/cluster_cti/bin/DFTB+/dftbplus-22.2/bin/dftb+ > ${directory}/free_slab/output_dftb_${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
/home/users/atetenoire/bin/dftbplus-22.2.x86_64-linux/bin/modes > ${directory}/free_slab/modes_dftb_${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
)


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
${SLURM_JOB_NODELIST}

nodes=${SLURM_JOB_NUM_NODES}:ppn${SLURM_CPUS_ON_NODE}
${SLURM_NTASKS}
$(squeue -j ${SLURM_JOB_ID} -h --Format TimeLimit)
echo ${SLURM_JOB_PARTITION}
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
