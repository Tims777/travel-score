#!/bin/bash
PROJECT_DIR=$(dirname "$BASH_SOURCE")
pip install -r requirements.txt
dagster asset materialize -m pipeline.definitions --select travel_score
read -p ""