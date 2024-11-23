#!/bin/bash
export PROJECT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$PROJECT_DIR/data/dagster"
cd $PROJECT_DIR
pip install -r project/requirements.txt
dagster asset materialize -m project.definitions --select *travel_score