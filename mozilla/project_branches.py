# Additional branches that start as identical (individual variables can be overriden here)
PROJECT_BRANCHES = {
    ### PLEASE ADD NEW BRANCHES ALPHABETICALLY (twigs at the bottom, also alphabetically)
    'accessibility': {
        'mozconfig_dir': 'accessibility',
        'enable_nightly': True,
        'enabled_products': ['firefox'],
        # only want a11y so turn off the default set
        'talos_suites': {
            'dirty': 0,
            'tp4': 0,
            'tp': 0,
            'chrome': 0,
            'nochrome': 0,
            'dromaeo': 0,
            'svg': 0,
            'scroll': 0,
            'paint': 0,
        },
        'add_test_suites': [
            ('macosx64', 'snowleopard', 'opt', 'mochitest-other', 'mochitest-a11y'),
            ('macosx64', 'snowleopard', 'debug', 'mochitest-other', 'mochitest-a11y'),
        ]
    },
    'build-system': {
        'enable_talos': False,
    },
    'devtools':{
        'enable_nightly': True,
        'enabled_products': ['firefox'],
        'platforms': {
            'macosx-debug': {
                'dont_build': True,
            },
            'macosx': {
                'slave_platforms': [],
            },
            'macosx64': {
                'slave_platforms': ['snowleopard'],
            },
            'linux-android': {
                'tegra_android': {},
            },
        },
    },
    'electrolysis': {
        'mozconfig_dir': 'electrolysis',
        'enable_talos': True,
    },
    'fx-team': {
        'repo_path': 'integration/fx-team',
        'mozconfig_dir': 'mozilla-central',
        'enable_nightly': True,
        'enabled_products': ['firefox'],
        'talos_suites': {
            'remote-ts': 1,
            'remote-tdhtml': 1,
            'remote-tsvg': 1,
            'remote-tsspider': 1,
            'remote-twinopen': 1,
        }
    },
    'graphics':{
        'enable_unittests': False,
        'enable_talos': False,
    },
    'ionmonkey': {
        'mozconfig_dir': 'mozilla-central',
        'enable_talos' : False,
    },
    'jaegermonkey': {
        'mozconfig_dir': 'jaegermonkey',
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
        'talos_suites': {
            'remote-ts': 1,
            'remote-tdhtml': 1,
            'remote-tsvg': 1,
            'remote-tsspider': 1,
            'remote-twinopen': 1,
        },
    },
    'mozilla-inbound': {
        'repo_path': 'integration/mozilla-inbound',
        'mozconfig_dir': 'mozilla-central',
        'enable_nightly': True,
        'enable_weekly_bundle': True,
        'platforms': {
            'linux64': {
                'build_space': 7,
            },
            'linux': {
                'build_space': 7,
            },
            'linuxqt': {
                'build_space': 7,
            },
        },
    },
    'places': {
        'platforms': {
            'linux64': {
                'build_space': 6,
            },
            'linux': {
                'build_space': 6,
            },
            'linuxqt': {
                'build_space': 6,
            },
        },
    },
    'private-browsing': {
        'enable_talos': False,
        'enabled_products': ['firefox'],
        'enable_nightly': False,
    },
    'services-central': {
        'repo_path': 'services/services-central',
        'enable_weekly_bundle': True,
    },
    'tracemonkey': {
        'repo_path': 'tracemonkey',
        'mozconfig_dir': 'tracemonkey',
        'branch_name': 'TraceMonkey',
        'mobile_branch_name': 'TraceMonkey',
        'build_branch': 'TraceMonkey',
        'start_hour': [3],
        'start_minute': [32],
        'enable_nightly': True,
        'enable_shark': True,
        'platforms': {
            'linux64': {
                'build_space': 7,
            },
            'linux': {
                'build_space': 7,
            },
            'linuxqt': {
                'build_space': 7,
            },
            'linux-debug': {
                'enable_valgrind_checktests': True,
            },
            'linux64-debug': {
                'enable_valgrind_checktests': True,
            },
        },
        'create_snippet': True,
        'create_partial': True,
        'talos_suites': {
            'v8': 1,
        }
    },
    'ux': {
        'branch_name': 'UX',
        'mobile_branch_name': 'UX',
        'build_branch': 'UX',
        'tinderbox_tree': 'UX',
        'mobile_tinderbox_tree': 'UX',
        'packaged_unittest_tinderbox_tree': 'UX',
        'enabled_products': ['firefox'],
        'enable_mobile': False,
        'mozconfig_dir' : 'ux',
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
        'platforms': {
            'macosx-debug': {
                'dont_build': True,
            },
            'macosx64-debug': {
                'dont_build': True,
            },
            'linux-debug': {
                'dont_build': True,
            },
            'linux64-debug': {
                'dont_build': True,
            },
            'win32-debug': {
                'dont_build': True,
            },
        },
    },
    #####  TWIGS aka RENTABLE BRANCHES
    'alder': {},
    'birch': {},
    'cedar': {},
    'holly': {},
    'larch': {},
    # customizations while booked for bcp47 project as per bug 667734
    'maple': {
        'enable_talos': False,
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
    },
}

# All is the default
ACTIVE_PROJECT_BRANCHES = PROJECT_BRANCHES.keys()
# Turning off graphics - bug 649507
for branch in ('graphics',):
    ACTIVE_PROJECT_BRANCHES.remove(branch)

# Load up project branches' local values
for branch in PROJECT_BRANCHES.keys():
    PROJECT_BRANCHES[branch]['tinderbox_tree'] = PROJECT_BRANCHES[branch].get('tinderbox_tree', branch.title())
    PROJECT_BRANCHES[branch]['mobile_tinderbox_tree'] = PROJECT_BRANCHES[branch].get('mobile_tinderbox_tree', branch.title())
    PROJECT_BRANCHES[branch]['packaged_unittest_tinderbox_tree'] = PROJECT_BRANCHES[branch].get('packaged_unittest_tinderbox_tree', branch.title())
