#!/bin/bash
export ROOT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$ROOT_DIR/data-temp"
export SKIP_PBF_ANALYSIS="yes"  # comment to enable analysis (will download and process ~20 GB)
cd $ROOT_DIR
python -m dagster asset materialize -m project.definitions --select '*travel_score'