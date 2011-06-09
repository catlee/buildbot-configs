c = BuildmasterConfig = {}
c['slavePortnum'] = 9020

from buildbot.status.html import WebStatus
c['status'] = [
        WebStatus(http_port=8020, allowForce=True)
]

c['buildbotURL'] = 'http://preproduction-master.build.mozilla.org:8020/'

from buildbot import manhole
c['manhole'] = manhole.PasswordManhole("tcp:1245:interface=127.0.0.1", "cltbld", "password")

from config import BRANCHES, SLAVES, PROJECTS
ACTIVE_BRANCHES = []
ACTIVE_PROJECTS = []
ACTIVE_RELEASE_BRANCHES = ['mozilla-1.9.1', 'mozilla-1.9.2', 'mozilla-2.0',
                           'mozilla-beta']

# Set up our fast slaves
# No need to reload, this is reloaded by builder_master.cfg
import buildbotcustom.misc
buildbotcustom.misc.fastRegexes.extend([
    '-ix-',
    'xserve',
    ])
ENABLE_RELEASES = True
RESERVED_SLAVES = None
