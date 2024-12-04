#!/bin/bash
export PROJECT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$PROJECT_DIR/data"
mkdir $DAGSTER_HOME
cd $PROJECT_DIR
pip install -r project/requirements.txt
python -m dagster asset materialize -m project.definitions --select "*"