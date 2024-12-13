#!/bin/bash
export ROOT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$ROOT_DIR/data"
cd $ROOT_DIR
python -m dagster asset materialize -m project.definitions --select "*"