from buildbot.util import json
from buildbot.status.html import WebStatus
from buildbot import manhole

master_config = json.load(open('master_config.json'))

c = BuildmasterConfig = {}
c['slavePortnum'] = master_config.get('pb_port', None)
c['status'] = []

if 'http_port' in master_config:
    c['status'].append(
            WebStatus(http_port=master_config['http_port'], allowForce=True))
    c['buildbotURL'] = 'http://%(hostname)s:%(http_port)i/' % master_config

if 'ssh_port' in master_config:
    c['manhole'] = manhole.PasswordManhole(
            "tcp:%(ssh_port)i:interface=127.0.0.1" % master_config,
            "cltbld", "password")

from config import BRANCHES, SLAVES, PROJECTS, ACTIVE_PROJECT_BRANCHES
ACTIVE_BRANCHES = ACTIVE_PROJECT_BRANCHES[:]
ACTIVE_BRANCHES.extend([
    'mozilla-1.9.2',
    'mozilla-2.0',
    'mozilla-central',
    'shadow-central',
    ])
ACTIVE_PROJECTS = PROJECTS.keys()

ACTIVE_RELEASE_BRANCHES = []

# Set up our fast slaves
# No need to reload, this is reloaded by builder_master.cfg
import buildbotcustom.misc
buildbotcustom.misc.fastRegexes.extend([
    '-ix-',
    'xserve',
    ])
ENABLE_RELEASES = False
RESERVED_SLAVES = "reserved_slaves_%(name)s" % master_config
