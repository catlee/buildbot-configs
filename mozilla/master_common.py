import time
import random
import re

c = BuildmasterConfig = {}
c['projectName'] = "Firefox"
c['projectURL'] = "http://wiki.mozilla.org/Firefox"
c['logMaxSize'] = 50 * 1024 * 1024
c['changeHorizon'] = None
c['logCompressionMethod'] = 'gz'
c['eventHorizon'] = 20
c['buildCacheSize'] = 10
c['changeCacheSize'] = 10000

c['status'] = []
c['slaves'] = []
c['builders'] = []
c['schedulers'] = []
c['change_source'] = []

# Builders from these branches are given custom priority, default is 4 for unlisted branches
# Please leave in sorted order
DEFAULT_BRANCH_PRIORITY = 4
BRANCH_PRIORITIES = {
    'mozilla-release': 0,
    'comm-esr24': 0,
    'mozilla-esr24': 1,
    'mozilla-b2g18': 1,
    'mozilla-b2g18_v1_1_0_hd': 1,
    'mozilla-b2g26_v1_2': 1,
    'mozilla-b2g28_v1_3': 1,
    'mozilla-beta': 2,
    'comm-beta': 2,
    'mozilla-central': 3,
    'comm-central': 3,
    'mozilla-aurora': 3,
    'comm-aurora': 3,
    # Unlisted branches are prioritized at this level
    'mozilla-inbound': 4,
    'b2g-inbound': 4,
    'fx-team': 4,
    'try': 5,
    'try-comm-central': 5,
    'alder': 5,
    'ash': 5,
    'birch': 5,
    'cedar': 5,
    'cypress': 5,
    'date': 5,
    'elm': 5,
    'fig': 5,
    'gum': 5,
    'holly': 5,
    'jamun': 5,
    'larch': 5,
    'maple': 5,
    'oak': 5,
    'pine': 5,
    'ux': 5,
    # Idle jobs like fuzzing
    'idle': 6,
}

# List of (regular expression, priority) tuples. If no expression matches the
# builder name, a priority of 100 is used. Lower priority values get run
# earlier.
BUILDER_PRIORITIES = [
    (re.compile('l10n'), 150),
]


def builderPriority(builder, request):
    """
    Our builder sorting function
    Returns (branch_priority, request_priority, builder_priority, submitted_at)

    NB: lower values returned by this function correspond to a "higher" or
    "better" priority
    """
    # larger request priorities correspond to more important jobs
    # see buildbot's DBConnector.get_unclaimed_buildrequests which sorts the
    # buildrequests by request.priority DESC
    # since lower is better for us, we should negate this value
    req_priority = -request[1]
    submitted_at = request[2]

    branch_priority = DEFAULT_BRANCH_PRIORITY
    if builder.builder_status.category.startswith('release'):
        branch_priority = 0
    elif builder.properties and 'branch' in builder.properties:
        for branch, p in BRANCH_PRIORITIES.iteritems():
            if branch in builder.properties['branch']:
                branch_priority = p
                break

    # Default builder priority is 100
    builder_priority = 100
    for exp, p in BUILDER_PRIORITIES:
        if exp.search(builder.name):
            builder_priority = p
            break

    return branch_priority, req_priority, builder_priority, submitted_at

cached_twlog = None
def getTwlog():
    global cached_twlog
    if cached_twlog:
        return cached_twlog
    else:
        from twisted.python import log as twlog
        cached_twlog = twlog
        return cached_twlog


def prioritizeBuilders(buildmaster, builders):
    """
    This is called by the buildmaster to sort the list of builders
    Builders for which there are no available slaves are discarded
    Builders that share the same set of slaves are grouped together, and the
    builders with the most important priority as defined by builderPriority()
    are kept, with the rest being discarded.
    The final list is shuffled so that each of the important builders has a
    fair chance of being assigned to a slave.
    """
    twlog = getTwlog()
    start_time = time.time()

    def log(msg, *args):
        msg = msg % args
        twlog.msg("prioritizeBuilders: %.2fs %s" % (time.time() - start_time, msg))
    log("starting")
    # Get the list pending builds, at most one per builder
    db = buildmaster.db
    q = """SELECT br.buildername, max(br.priority), min(br.submitted_at)
             FROM buildrequests AS br
             WHERE br.complete=0
             AND (br.claimed_at<?
                  OR (br.claimed_by_name=?
                      AND br.claimed_by_incarnation!=?))
             GROUP BY br.buildername"""
    requests = db.runQueryNow(db.quoteq(q),
                              (time.time() - 3600, buildmaster.master_name, buildmaster.master_incarnation))
    log("got %i request(s)", len(requests))

    # Filter out requests we're not running builders for
    allBuilderNames = set(builder.name for builder in builders)
    requests = filter(lambda request: request[0] in allBuilderNames, requests)
    log("requests for my builders: %i", len(requests))

    # Turn into a dictionary keyed by buildername
    requests = dict((request[0], request) for request in requests)

    # Remove builders we don't have requests for
    builders = filter(lambda builder: builder.name in requests, builders)
    log("builders with requests: %i", len(builders))

    # Figure out which slaves are available.
    # This is a little expensive, so we do it once here to avoid doing it twice
    # below
    avail_slaves = set()
    seen_slaves = set()
    for b in builders:
        for s in b.slaves:
            if s.slave.slavename not in seen_slaves:
                if s.isAvailable():
                    avail_slaves.add(s.slave.slavename)
                seen_slaves.add(s.slave.slavename)
    log("found %i available of %i connected slaves", len(avail_slaves), len(seen_slaves))

    # Remove builders we have no slaves for
    builders = filter(lambda builder: [s for s in builder.slaves if s.slave.slavename in avail_slaves], builders)
    log("builders with slaves: %i", len(builders))

    # Annotate our list of builders with their priority
    builders = map(lambda builder: (builderPriority(builder, requests[builder.name]), builder), builders)
    builders.sort()
    log("prioritized %i builder(s): %s", len(builders), [(p, b.name) for (p, b) in builders])

    # For each set of slaves, create a list of (priority, builder) for that set
    # of slaves
    # If we're checking the jacuzzi allocations, then limit the available
    # slaves by whatever the jacuzzi allocation is.
    # If we don't incorporate the jacuzzi allocations here, we could end up
    # with lower priority builders being discarded below which have available
    # slaves attached and allocated.
    from buildbotcustom.misc import J
    builders_by_slaves = {}
    for b in builders:
        slaves = [s for s in b[1].slaves if s.slave.slavename in avail_slaves]
        if getattr(prioritizeBuilders, 'check_jacuzzis', False):
            try:
                # Filter the available slaves through the jacuzzi bubbles..
                slaves = J.get_slaves(b[1].name, slaves)
            except Exception:
                twlog.err("handled exception talking to jacuzzi; trying to carry on")

        if slaves:
            slaves = frozenset(s.slave.slavename for s in slaves)
            builders_by_slaves.setdefault(slaves, []).append(b)
        else:
            log('removed builder %s with no allocated slaves available' % b[1].name)
    log("assigned into %i slave set(s)", len(builders_by_slaves))

    # Find the set of builders with the highest priority for each set of slaves
    # If there are multiple builders with the same priority, keep all of them,
    # but discard builders with lower priority.
    # By removing lower priority builders, we avoid the situation where a slave
    # connects when the master is partway through iterating through the full
    # set of builders and assigns work to lower priority builders while there's
    # still work pending for higher priority builders.
    # If we do end up discarding lower priority builders, we should re-run the
    # builder loop after assigning the high-priority work.
    run_again = False
    important_builders = set()
    for slaves, builder_list in builders_by_slaves.items():
        builder_list.sort()
        # The first entry in the list is the builder with the highest priority
        best_priority = builder_list[0][0]
        if len(slaves) < 20:
            log("finding important builders for slaves: %s", list(slaves))
        else:
            log("finding important builders for slaves: %s", list(slaves)[:20] + ["..."])

        for p, b in builder_list:
            if p == best_priority:
                important_builders.add(b)
                log("important builder %s (p == %s)", b.name, p)
            else:
                run_again = True
                log("unimportant builder %s (%s != %s)", b.name, p, best_priority)
    log("found %i important builder(s): %s", len(important_builders), [b.name for b in important_builders])

    # Now we're left with important builders for all the slave pools
    builders = list(important_builders)
    # They should be all the same priority now, so we can shuffle them to make
    # sure we assign jobs to slaves fairly
    log("shuffling important builders")
    random.shuffle(builders)

    # We've ended up dropping some builders
    if run_again:
        log("triggering builder loop again since we've dropped some lower priority builders")
        buildmaster.botmaster.loop.trigger()
    log("finished prioritization")

    return builders

c['prioritizeBuilders'] = prioritizeBuilders


# BRANCHES without 'gecko_version' set are considered to have a gecko_version
# later (larger) than any other value. See items_before for example usage.
def setMainFirefoxVersions(BRANCHES):
    # MERGE DAY
    if 'mozilla-release' in BRANCHES:
        BRANCHES['mozilla-release']['gecko_version'] = 27
    if 'mozilla-beta' in BRANCHES:
        BRANCHES['mozilla-beta']['gecko_version'] = 28
    if 'mozilla-aurora' in BRANCHES:
        BRANCHES['mozilla-aurora']['gecko_version'] = 29


def setMainCommVersions(BRANCHES):
    # MERGE DAY
    BRANCHES['comm-beta']['gecko_version'] = 28
    BRANCHES['comm-aurora']['gecko_version'] = 29

# Typical usage pattern:
#
#   set cfg = current_behavior
#   for (b in items_before(BRANCHES, 'gecko_version', N)):
#     set cfg = previous_behavior
#
def items_before(map, key, maxval):
    """
    yield all items from the dict 'map' where mapvalue[key] is present and less
    than 'maxval' (assume that anything missing a value is later than the
    threshold you're testing for.)
    """
    for k, v in map.items():
        value = v.get(key)
        if value and cmp(value, maxval) < 0:
            yield (k, v)

# Typical usage pattern:
#
#   for (b in items_at_least(BRANCHES, 'gecko_version', N)):
#     set cfg = new_behavior
#
def items_at_least(map, key, minval):
    """yield all items from the dict 'map' where mapvalue[key] is either not
    present, or at least 'minval' if it is present (assume that anything
    missing a value is definitely greater than the minimum)"""
    for k, v in map.items():
        value = v.get(key, minval)
        if cmp(value, minval) >= 0:
            yield (k, v)
