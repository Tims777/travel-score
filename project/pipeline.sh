#!/bin/bash
export ROOT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$ROOT_DIR/data"
export SKIP_PBF_ANALYSIS="yes"  # uncomment to enable (will download ~20 GB)
cd $ROOT_DIR
python -m dagster asset materialize -m project.definitions --select "*"