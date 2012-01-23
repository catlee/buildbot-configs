# Additional branches that start as identical (individual variables can be overriden here)
PROJECT_BRANCHES = {
    ### PLEASE ADD NEW BRANCHES ALPHABETICALLY (twigs at the bottom, also alphabetically)
    'accessibility': {
        'mozconfig_dir': 'accessibility',
        'enable_nightly': True,
        'enabled_products': ['firefox'],
        # only want a11y which is run within the "chrome" suite
        # turn other suites off
        'talos_suites': {
            'dirty': 0,
            'tp4': 0,
            'tp': 0,
            'chrome_twinopen': 0,
            'chrome_mac': 0,
            'chrome': 0,
            'nochrome': 0,
            'dromaeo': 0,
            'svg': 0,
            'paint': 0,
        },
        'add_test_suites': [
            ('macosx64', 'snowleopard', 'opt', 'mochitest-other', 'mochitest-a11y'),
            ('macosx64', 'snowleopard', 'debug', 'mochitest-other', 'mochitest-a11y'),
        ]
    },
    'build-system': {
        'enable_talos': True,
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
            'android': {
                'enable_opt_unittests': False,
                'enable_debug_unittests': False,
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
        'pgo_strategy': 'periodic',
        'pgo_platforms': ['linux', 'linux64', 'win32'],
    },
    'graphics':{
        'enable_unittests': False,
        'enable_talos': False,
    },
    'ionmonkey': {
        'disable_tinderbox_mail': False,
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
        'pgo_strategy': 'periodic',
        'pgo_platforms': ['linux', 'linux64', 'win32'],
        'periodic_pgo_interval': 3,
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
            'macosx64-debug': {
                'enable_leaktests': True,
            },
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
        },
        'talos_suites': {
            'v8': 1,
        }
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
    'profiling': {
        'enable_talos': True,
        'enabled_products': ['firefox'],
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
    },
    'services-central': {
        'repo_path': 'services/services-central',
        'enable_weekly_bundle': True,
    },
    'ux': {
        'branch_name': 'UX',
        'mobile_branch_name': 'UX',
        'build_branch': 'UX',
        'tinderbox_tree': 'UX',
        'mobile_tinderbox_tree': 'UX',
        'packaged_unittest_tinderbox_tree': 'UX',
        'enabled_products': ['firefox'],
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
    # customizations while booked for bug 687570 - WebRTC project
    'alder': {
        'enable_unittests': False,
        'enable_talos': False,
    },
    'ash': {},
    'birch': {},
    'cedar': {},
    # customizations for windows update service changes (bug 481815)
    'elm': {
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
        'lock_platforms': True,
        'platforms': {
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win32-debug': {},
        },
        'enable_talos': False,
    },
    'holly': {},
    'larch': {},
    # customizations while booked for bcp47 project as per bug 667734
    'maple': {
        'enable_talos': False,
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
    },
    # customizations for integration work for bugs 481815 and 307181
    'oak': {
        'enable_nightly': True,
        'create_snippet': True,
        'create_partial': True,
        'enable_talos': False,
        'platforms': {
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
        },
    },
    'pine': {
        'enable_unittests': False,
        'enabled_products': ['firefox'],
        'talos_suites': {
            'tp': [1, {'suites': ['--sampleConfig', 'cycles.config']}],
            'chrome': [1, {'suites': ['--sampleConfig', 'cycles.config']}],
            'chrome_mac': [1, {'suites': ['--sampleConfig', 'cycles.config']}],
            'nochrome': [1, {'suites': ['--sampleConfig', 'cycles.config']}],
            'dirty': 0,
            'svg': [1, {'suites': ['--sampleConfig', 'cycles.config']}],
            'dromaeo': 0,
            # hate that remote talos still show up when mobile product is not being requested
            # but that's not part of the bug i'm doing this for, so leaving for now
            'remote-ts': 0,
            'remote-tdhtml': 0,
            'remote-tsvg': 0,
            'remote-tsspider': 0,
            'remote-tpan': 0,
            'remote-tp4m': 0,
            'remote-tp4m_nochrome': 0,
            'remote-twinopen': 0,
            'remote-tzoom': 0,
        },
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
