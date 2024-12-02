#!/bin/bash
export PROJECT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$PROJECT_DIR/data/dagster"
cd $PROJECT_DIR
python -m dagster dev