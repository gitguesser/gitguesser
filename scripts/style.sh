#!/bin/bash

cd $(dirname $(realpath "$0"))
cd ..

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place backend
isort backend --profile black
black backend
