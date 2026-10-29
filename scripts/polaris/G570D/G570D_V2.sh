#!/bin/bash
#SBATCH -J G570D_V2
#SBATCH --output=output/G570D_V2.o%j
#SBATCH --error=output/G570D_V2.e%j
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --partition=highmem
#SBATCH --time=UNLIMITED
#SBATCH --mail-user=ealvarado9@sfsu.edu
#SBATCH --mail-type=ALL

# 1. Clean environment
module purge

# 2. Load MPI (must match mpi4py build)
module load mpi/openmpi-x86_64

# 3. Activate conda properly (IMPORTANT: use conda.sh, not just "conda activate")
source ~/miniconda3/etc/profile.d/conda.sh
conda activate polaris_bv2

# 4. Fix Open MPI fabric issue (mlx5_0 problem)
export OMPI_MCA_mtl=^ofi
export OMPI_MCA_pml=ob1
export OMPI_MCA_btl=self,vader,tcp
export OMPI_MCA_btl_tcp_if_exclude=mlx5_0

# (optional but useful for debugging)
echo "---- ENV CHECK ----"
which python
which mpirun
python -c "import mpi4py; print(mpi4py.__file__)"
python -c "from mpi4py import MPI; print(MPI.Get_library_version())"
echo "-------------------"

declare -xr WDIR="/Users/917543996/brewster_v2/"

declare PATH=${PATH}:${WDIR}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${WDIR}:~/

whoami
pwd

time_start=`date '+%T%t%d_%h_06'`
  
echo ------------------------------------------------------
echo -n 'Job is running on node '$SLURM_JOB_NODELIST
echo ------------------------------------------------------
echo SBATCH: sbatch is running on $SLURM_SUBMIT_HOST
echo SBATCH: originating queue is $SLURM_SUBMIT_PARTITION
echo SBATCH: executing queue is $SLURM_JOB_PARTITION
echo SBATCH: working directory is $SLURM_SUBMIT_DIR
echo SBATCH: job identifier is $SLURM_JOBID
echo SBATCH: job name is $SLURM_JOB_NAME
echo SBATCH: node file is $SLURM_JOB_NODELIST
echo SBATCH: current home directory is $SLURM_SUBMIT_HOME
echo SBATCH: PATH = $SLURM_SUBMIT_PATH
echo ------------------------------------------------------


cd ${WDIR}

mpirun  --mca btl_tcp_if_include 130.212.15.0/24 --mca btl ^openib -n 128 python3 G570D_V2.py > /Users/917543996/Saves/G570D/test/G570D_V2.log

time_end=`date '+%T%t%d_%h_06'`
echo Started at: $time_start
echo Ended at: $time_end
echo ------------------------------------------------------
echo Job ends
