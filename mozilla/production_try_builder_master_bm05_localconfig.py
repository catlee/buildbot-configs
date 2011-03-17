c = BuildmasterConfig = {}
c['slavePortnum'] = 9012

from buildbot.status.html import WebStatus
c['status'] = [
        WebStatus(http_port=8012, allowForce=True)
]

c['buildbotURL'] = 'http://buildbot-master05.build.mozilla.org:8012/'

from buildbot import manhole
c['manhole'] = manhole.PasswordManhole("tcp:1238:interface=127.0.0.1", "cltbld", "password")

from config import BRANCHES, TRY_SLAVES, PROJECTS
ACTIVE_BRANCHES = ['tryserver']
ACTIVE_RELEASE_BRANCHES = []
# Override with TRY_SLAVES
SLAVES = TRY_SLAVES

# Don't do any projects
ACTIVE_PROJECTS = []

# Set up our fast slaves
# No need to reload, this is reloaded by builder_master.cfg
import buildbotcustom.misc
buildbotcustom.misc.fastRegexes.extend([
    '-ix-',
    'xserve',
    ])
ENABLE_RELEASES = False
STAGING = False
RESERVED_SLAVES = None
