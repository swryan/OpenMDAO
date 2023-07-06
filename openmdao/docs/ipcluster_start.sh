#!/bin/bash
echo "============================================================="
echo "additional setup to run MPI under notebooks"
echo "============================================================="

export OMPI_MCA_rmaps_base_oversubscribe=1

CFG_FILE="$HOME/.ipython/profile_mpi/ipcluster_config.py"
if [[ -f "$CFG_FILE" ]]; then
  echo "using existing ipcluster configuration: $CFG_FILE"
else
  echo "creating ipcluster configuration: $CFG_FILE"
  ipython profile create --parallel --profile=mpi
fi

cp -R  $HOME/.profile_default $HOME/.jupyter/
cp -R  $HOME/.profile_mpi $HOME/.jupyter/

ipcluster nbextension enable
ipcluster start -n 4 --profile=mpi --engines='ipyparallel.cluster.launcher.MPIEngineSetLauncher' &