#!/bin/bash
export ROOT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$ROOT_DIR/data"
# export BENCHMARK="yes"
# export EXTRA_MAPS="yes"
cd $ROOT_DIR
python -m dagster dev