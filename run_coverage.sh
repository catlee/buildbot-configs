#!/bin/sh
export COVERAGE_FILE=$PWD/.coverage
coverage erase
./test-masters.sh --coverage --buildbot=$(which buildbot)
coverage html -i
