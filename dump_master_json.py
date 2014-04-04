#!/usr/bin/env python
"""Usage: dump_master_json.py [options] /path/to/master ...
"""
import os.path
import json
import sys
import multiprocessing
import subprocess
import time
import tempfile
import hashlib
from contextlib import contextmanager

import logging
log = logging.getLogger(__name__)


def loadMaster(path):
    """Loads the master configuration and returns the 'c' object"""
    g = {}
    log.debug("loading %s", path)
    path = os.path.abspath(path)
    master_dir = os.path.dirname(path)
    sys.path.append(master_dir)
    os.chdir(master_dir)
    execfile(path, g, g)
    return g['c']


def getSlavePool(slavenames, pools):
    """
    Returns the id of a pool
    Modifies pools if necessary
    """
    slave_hash = hashlib.new("sha1")
    slave_hash.update("".join(sorted(slavenames)))
    slave_hash = slave_hash.hexdigest()
    if slave_hash not in pools:
        pools[slave_hash] = sorted(slavenames)
    return slave_hash


def getMasterInfo(c):
    """Returns stuff important for a static dump"""
    builders = {}
    slavepools = {}
    schedulers = {}
    for b in c['builders']:
        builder = {}
        builders[b['name']] = builder
        builder['slavepool'] = getSlavePool(b['slavenames'], slavepools)
        builder['shortname'] = b['builddir']
        builder['slavebuilddir'] = b.get('slavebuilddir')
        builder['properties'] = b.get('properties', {})

    for s in c['schedulers']:
        schedulers[s.name] = {
            'downstream': sorted(s.builderNames),
        }

    retval = {
        'builders': builders,
        'slavepools': slavepools,
        'schedulers': schedulers,
    }
    return retval


def safeupdate(dest, src):
    """Updates dict dest from src, raising an error if values for the same key differ"""
    for key, value in src.iteritems():
        if key in dest:
            if dest[key] != value:
                print "%s != %s for key %s" % (dest[key], value, key)
        dest[key] = value


def combineDumps(dumps):
    builders = {}
    slavepools = {}
    schedulers = {}
    master_builders = {}

    for d in sorted(dumps, key=lambda d: d['master']):
        safeupdate(builders, d['builders'])
        safeupdate(slavepools, d['slavepools'])
        safeupdate(schedulers, d['schedulers'])
        master_builders[d['master']] = sorted(d['builders'].keys())

    retval = {
        'builders': builders,
        'slavepools': slavepools,
        'schedulers': schedulers,
        'master_builders': master_builders,
    }
    return retval


def worker(path):
    output = tempfile.NamedTemporaryFile()
    proc = subprocess.Popen([sys.executable, sys.argv[0], path, '-o', output.name])
    proc.wait()
    return json.load(open(output.name))


def dump_master(path):
    try:
        c = loadMaster(path)
        retval = getMasterInfo(c)
        retval['master'] = os.path.basename(os.path.dirname(path))
        return retval
    except Exception:
        log.exception("Couldn't load %s", path)
        raise


@contextmanager
def atomic_output(path):
    fd, tmpname = tempfile.mkstemp(dir=os.path.dirname(path))
    fp = os.fdopen(fd, 'wb')
    try:
        yield fp, tmpname
        fp.close()
        os.rename(tmpname, path)
    except:
        fp.close()
        os.unlink(tmpname)
        raise


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("masters", nargs="*")
    parser.add_argument("-j", "--concurrency", dest="concurrency", type=int, default=None)
    parser.add_argument("-o", "--output-file", dest="output_file")

    args = parser.parse_args()

    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    if len(args.masters) == 1:
        dump = dump_master(args.masters[0])
    else:
        pool = multiprocessing.Pool(args.concurrency)
        s = time.time()
        dumps = pool.map(worker, args.masters)
        log.info("Loaded %i masters in %.2fs", len(args.masters), time.time() - s)
        dump = combineDumps(dumps)

    if args.output_file == '-':
        args.output_file = None

    if args.output_file:
        with atomic_output(args.output_file) as (fp, tmpname):
            json.dump(dump, fp, indent=2, sort_keys=True)
    else:
        print json.dumps(dump, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
