c = BuildmasterConfig = {}
c['slavePortnum'] = 9012

from buildbot.status.html import WebStatus
c['status'] = [
        WebStatus(http_port=8012, allowForce=True)
]

c['buildbotURL'] = 'http://talos-staging-master02.build.mozilla.org:8012/'

from buildbot import manhole
c['manhole'] = manhole.PasswordManhole("tcp:1236:interface=127.0.0.1", "cltbld", "password")

from config import BRANCHES, PLATFORMS, PROJECTS
from thunderbird_config import BRANCHES as THUNDERBIRD_BRANCHES, \
    PLATFORMS as THUNDERBIRD_PLATFORMS

# Do everything!
#ACTIVE_BRANCHES = BRANCHES.keys()
# I changed my mind; do only trunk
ACTIVE_BRANCHES = ['mozilla-central']
ACTIVE_PLATFORMS = dict((k,None) for k in PLATFORMS.keys())
ACTIVE_PROJECTS = PROJECTS.keys()
ACTIVE_THUNDERBIRD_BRANCHES = THUNDERBIRD_BRANCHES.keys()
ACTIVE_THUNDERBIRD_PLATFORMS = dict((k,None) for k in THUNDERBIRD_PLATFORMS.keys())

QUEUEDIR = "/dev/shm/queue"
