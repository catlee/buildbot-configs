#!/bin/sh
export COVERAGE_FILE=$PWD/.coverage
coverage erase
./test-masters.sh --coverage --buildbot=$(which buildbot) "$*"
coverage combine
rm -rf htmlcov
bbcustom=$(dirname $(python -c 'import buildbotcustom; print buildbotcustom.__file__'))
coverage html -i --include="$PWD/*,$bbcustom/*"
