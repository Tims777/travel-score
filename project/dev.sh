#!/bin/bash
export PROJECT_DIR=$(realpath "$(dirname $BASH_SOURCE)/..")
export DAGSTER_HOME="$PROJECT_DIR/data/dagster"
dagster dev