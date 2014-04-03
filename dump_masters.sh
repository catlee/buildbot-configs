#!/bin/bash
# This script has been rewritten in setup_master.py using
# the -t option.  We use that now
exit=0

# even though it isn't fully used, the config check does require a valid
# shared memory setup AT THE DEFAULT LOCATION. If you're running on a
# laptop, that may not exist. Fail early.
#
# OSX note: it "works" (for test-masters purposes) to just create the
#           directory, even though that isn't how shared memory is
#           handled on OSX. The directories must be owned by the id
#           running the tests.
shm=(/dev/shm)
good_shm=true
for needed_dir in ${shm[@]}; do
    if ! test -w $needed_dir; then
        echo 1>&2 "No shm setup, please create writable directory '$needed_dir'"
        good_shm=false
    fi
done
$good_shm || exit 1

if [ -z "$1" ]; then
    OUTPUT="allthethings.json"
else
    OUTPUT=$1
fi
echo "outputting to ${OUTPUT}"
WORK=test-output
mkdir $WORK 2>/dev/null

actioning="Checking"
MASTERS_JSON_URL="${MASTERS_JSON_URL:-https://hg.mozilla.org/build/tools/raw-file/tip/buildfarm/maintenance/production-masters.json}"

atexit=()
trap 'for cmd in "${atexit[@]}"; do eval $cmd; done' EXIT

# I have had problems where a whole bunch of parallel HTTP requests caused
# errors (?), so fetch it once here and pass it in.
MASTERS_JSON=$(mktemp $WORK/tmp.masters.XXXXXXXXXX)
if [[ $MASTERS_JSON_URL =~ ^http ]]; then
    wget -q -O$MASTERS_JSON "$MASTERS_JSON_URL" || exit 1
else
    cp "$MASTERS_JSON_URL" $MASTERS_JSON
fi
atexit+=("rm $MASTERS_JSON")

FAILFILE=$(mktemp $WORK/tmp.failfile.XXXXXXXXXX)
atexit+=("rm $FAILFILE")

# Construct the set of masters that we will test.
MASTERS=($(./setup-master.py -l -j "$MASTERS_JSON" --tested-only))

# Create all the masters in parallel
for MASTER in ${MASTERS[*]}; do (
    rm -rf $WORK/$MASTER
    if [[ $MASTER =~ universal ]]; then
        echo "skipping universal master $MASTER"
        continue
    fi
    OUTFILE=$(mktemp $WORK/tmp.testout.XXXXXXXXXX)
    ./setup-master.py --tested-only -j "$MASTERS_JSON" $WORK/$MASTER $MASTER > $OUTFILE 2>&1 || echo "$MASTER" >> $FAILFILE
    cat $OUTFILE # Make the output a little less interleaved
    rm $OUTFILE
) &
atexit+=("[ -e /proc/$! ] && kill $!")
done

echo "$actioning ${#MASTERS[*]} masters..."
echo "${MASTERS[*]}"
wait

# Now combine them
MASTER_DIRS=()
for MASTER in ${MASTERS[*]}; do
    if [[ $MASTER =~ universal ]]; then
        continue
    fi
    MASTER_DIRS+=("$WORK/$MASTER/master.cfg")
done
python dump_master_json.py -o $OUTPUT ${MASTER_DIRS[*]}

if [ -s $FAILFILE ]; then
    echo "*** $(wc -l < $FAILFILE) master tests failed ***" >&2
    echo "Failed masters:" >&2
    sed -e 's/^/  /' "$FAILFILE" >&2
    exit 1
fi

exit $exit
