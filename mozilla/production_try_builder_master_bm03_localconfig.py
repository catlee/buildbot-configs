c = BuildmasterConfig = {}
c['slavePortnum'] = 9011

from buildbot.status.html import WebStatus
c['status'] = [
        WebStatus(http_port=8011, allowForce=True)
]

c['buildbotURL'] = 'http://buildbot-master3.build.mozilla.org:8011/'

from buildbot import manhole
c['manhole'] = manhole.PasswordManhole("tcp:1236:interface=127.0.0.1", "cltbld", "password")

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
