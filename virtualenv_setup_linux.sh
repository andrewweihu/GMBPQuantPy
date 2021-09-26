#!/bin/bash

. ~/.bashrc

SCRIPT=$(readlink -f $0)
PROJ_ROOT=$(dirname $SCRIPT)

#MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
MINICONDA_DIR=$HOME/miniconda/miniconda3-py39-4.9.2
MINICONDA_PYTHON_BIN=$MINICONDA_DIR/bin/
VENV=$HOME/.envs/gmbp-quant

if [ ! -d $MINICONDA_DIR ]
then
  echo "===== Downloading Miniconda3 ... ====="
  wget ${MINICONDA_URL} -O miniconda.sh

  echo "===== Installing Miniconda3 to $MINICONDA_DIR ... ====="
  chmod 755 miniconda.sh
  ./miniconda.sh -u -b -p $MINICONDA_DIR
  rm miniconda.sh
fi

echo "===== Removing virtualenv: $VENV ... ====="
rm -rf $VENV

echo "===== Creating virtualenv: $VENV ... ====="
$MINICONDA_PYTHON_BIN/python -m venv $VENV
source $VENV/bin/activate

export PIP_CONFIG_FILE=$PROJ_ROOT/pip.conf

echo "===== Installing requirements.txt ... ====="
which pip
pip install --upgrade pip
pip install -r requirements.txt