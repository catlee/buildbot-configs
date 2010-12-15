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

# Builders from these branches are given higher priority.
PRIORITY_BRANCHES = ['mozilla-central',
                     'mozilla-1.9.2',
                     'mozilla-1.9.1']

# Give the release builders priority over other builders
def prioritizeBuilders(botmaster, builders):
    def sortkey(builder):
        builds = builder.getBuildable(1)
        if builds:
            # The builder that gets sorted first, gets run first, but the build
            # request priorities are in ascending order (higher priority gets
            # run next), so flip the sign of the priority so that higher
            # priorities sort to the front
            req_priority = -builds[0].priority
            submitted_at = builds[0].submittedAt
        else:
            req_priority = 0
            submitted_at = None

        if builder.builder_status.category.startswith('release'):
            priority = 0
        elif builder.properties and \
             builder.properties.has_key('branch') and \
             builder.properties['branch'] in PRIORITY_BRANCHES:
            priority = 1 
        elif builder.builder_status.category.startswith('try'):
            priority = 3
        else:
            priority = 2

        return priority, req_priority, submitted_at
    builders.sort(key=sortkey)
    return builders
c['prioritizeBuilders'] = prioritizeBuilders

import passwords
reload(passwords)
if hasattr(passwords, 'PULSE_PASSWORD'):
    # Send pulse messages
    import re
    import buildbotcustom.status.pulse
    reload(buildbotcustom.status.pulse)
    from buildbotcustom.status.pulse import PulseStatus
    from mozillapulse.publishers import GenericPublisher
    from mozillapulse.config import PulseConfiguration
    c['status'].append(PulseStatus(
        GenericPublisher(PulseConfiguration(
            user=passwords.PULSE_USERNAME,
            password=passwords.PULSE_PASSWORD,
            ),
            exchange=passwords.PULSE_EXCHANGE),
        ignoreBuilders=[re.compile('.*shadow-central.*'), re.compile('fuzzer-.*')],
        send_logs=False,
        ))
