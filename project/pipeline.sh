#!/bin/bash
export PROJECT_DIR=$(dirname "$BASH_SOURCE")
export DAGSTER_HOME=$(realpath "$PROJECT_DIR/../data/dagster")
cd $PROJECT_DIR
# pip install -r requirements.txt
dagster asset materialize -m pipeline.definitions --select *travel_score
read -p ""