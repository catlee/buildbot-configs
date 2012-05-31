SLAVES = {
    'fedora': dict([("talos-r3-fed-%03i" % x, {}) for x in range(3,10) + range(11,18) + range(19,77)]),
    'fedora64' : dict([("talos-r3-fed64-%03i" % x, {}) for x in range (3,10) + range(11,35) + range(36,72)]),
    'xp': dict([("talos-r3-xp-%03i" % x, {}) for x in range(4,10) + range(11,76) \
          if x not in [45]]), # bug 661377
    'win7': dict([("talos-r3-w7-%03i" % x, {}) for x in range(4,10) + range(11,80)]),
    'w764': dict([("t-r3-w764-%03i" % x, {}) for x in range(1,6)]),
    'leopard': dict([("talos-r3-leopard-%03i" % x, {}) for x in range(3,10) + range(11,67) \
          if x not in [7]]), # bug 655437
    'snowleopard': dict([("talos-r4-snow-%03i" % x, {}) for x in range(4,10) + range(11,81) + [82,84]]),
    'lion': dict([("talos-r4-lion-%03i" % x, {}) for x in range(4,10) + range(11,83) + [84]]),
    'tegra_android': dict([('tegra-%03i' % x, {'http_port': '30%03i' % x, 'ssl_port': '31%03i' % x}) for x in range(31,289) \
          if x not in range(122,129) + [30,49,77,131,137,143,147,161,180,184,185,186,193,197,226,239,241,268,289]]), # decommissioned tegras
}

SLAVES['leopard-o'] = SLAVES['leopard']
SLAVES['tegra_android-xul'] = SLAVES['tegra_android']
SLAVES['tegra_android-o'] = SLAVES['tegra_android']

TRY_SLAVES = {}

GRAPH_CONFIG = ['--resultsServer', 'graphs.mozilla.org',
    '--resultsLink', '/server/collect.cgi']

GLOBAL_VARS = {
    'disable_tinderbox_mail': True,
    'build_tools_repo_path': 'build/tools',
    'stage_server': 'stage.mozilla.org',
    'stage_username': 'ffxbld',
    'stage_ssh_key': 'ffxbld_dsa',
}

# Local branch overrides
BRANCHES = {
    'mozilla-central': {
        'tinderbox_tree': 'Firefox',
        'mobile_tinderbox_tree': 'Firefox',
    },
    'mozilla-release': {
        'tinderbox_tree': 'Mozilla-Release',
        'mobile_tinderbox_tree': 'Mozilla-Release',
    },
    'mozilla-esr10': {
        'tinderbox_tree': 'Mozilla-Esr10',
        'mobile_tinderbox_tree': 'Mozilla-Esr10',
    },
    'mozilla-beta': {
        'tinderbox_tree': 'Mozilla-Beta',
        'mobile_tinderbox_tree': 'Mozilla-Beta',
    },
    'mozilla-aurora': {
        'tinderbox_tree': 'Mozilla-Aurora',
        'mobile_tinderbox_tree': 'Mozilla-Aurora',
    },
    'places': {
        'tinderbox_tree': 'Places',
        'mobile_tinderbox_tree': 'Places',
    },
    'electrolysis': {
        'tinderbox_tree': 'Electrolysis',
        'mobile_tinderbox_tree': 'Electrolysis',
    },
    'addontester': {
        'tinderbox_tree': 'AddonTester',
        'mobile_tinderbox_tree': 'AddonTester',
    },
    'addonbaselinetester': {
        'tinderbox_tree': 'AddonTester',
        'mobile_tinderbox_tree': 'AddonTester',
    },
    'try': {
        'tinderbox_tree': 'Try',
        'mobile_tinderbox_tree': 'Try',
        'enable_mail_notifier': True,
        'notify_real_author': True,
        'enable_merging': False,
        'slave_key': 'try_slaves',
        'package_url': 'http://ftp.mozilla.org/pub/mozilla.org/firefox/try-builds',
        'package_dir': '%(who)s-%(got_revision)s',
        'stage_username': 'trybld',
        'stage_ssh_key': 'trybld_dsa',
    },
    'jaegermonkey': {
        'tinderbox_tree': 'Jaegermonkey',
        'mobile_tinderbox_tree': 'Jaegermonkey',
    },
}

PLATFORM_VARS = {
}

PROJECTS = {
    'jetpack': {
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'tinderbox_tree': 'Jetpack',
    },
}
