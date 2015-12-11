PROJECT_BRANCHES = {
    ### PLEASE ADD NEW BRANCHES ALPHABETICALLY (twigs at the bottom, also alphabetically)
    # 'build-system': {},  # Bug 1010674
    'fx-team': {
        'merge_builds': False,
        'enable_perproduct_builds': True,
        'repo_path': 'integration/fx-team',
        'mozconfig_dir': 'mozilla-central',
        'enable_nightly': False,
        'pgo_strategy': 'periodic',
        'periodic_start_hours': range(2, 24, 3),
        'enable_weekly_bundle': True,
    },
    'mozilla-inbound': {
        'merge_builds': False,
        'repo_path': 'integration/mozilla-inbound',
        'enable_perproduct_builds': True,
        'mozconfig_dir': 'mozilla-central',
        'enable_weekly_bundle': True,
        'pgo_strategy': 'periodic',
        'periodic_start_hours': range(1, 24, 3),
        'talos_suites': {
            'xperf': 1,
        },
        'branch_projects': ['spidermonkey_tier_1', 'spidermonkey_info'],
    },
    'b2g-inbound': {
        'merge_builds': False,
        'repo_path': 'integration/b2g-inbound',
        'enable_perproduct_builds': True,
        'mozconfig_dir': 'mozilla-central',
        'pgo_strategy': 'periodic',
        'periodic_start_hours': range(2, 24, 3),
        'enable_weekly_bundle': True,
        'talos_suites': {
            'xperf': 1,
        },
        'platforms': {
            'win32': {
                'enable_checktests': False,
                'slave_platforms': ['win7-ix'],
                'talos_slave_platforms': ['win7-ix'],
            },
            'win32-debug': {
                'enable_checktests': False,
                'slave_platforms': ['win7-ix'],
            },
            'macosx64': {
                'enable_checktests': False,
                'slave_platforms': ['snowleopard'],
                'talos_slave_platforms': ['snowleopard'],
            },
            'macosx64-debug': {
                'enable_checktests': False,
                'slave_platforms': ['snowleopard'],
            },
        },
    },
    #'services-central': {},  # Bug 1010674
    # customized for bug 1156408
    'alder': {
        "enable_nightly": True,
        'desktop_mozharness_repacks_enabled': True,
        "enable_weekly_bundle": True,
        "pgo_strategy": None,
        "platforms": {
            "android-api-9": {
                "is_mobile_l10n": True,
            },
        },
        "enable_onchange_scheduler": False,
        "enable_nightly_scheduler": False,
        "enable_periodic_scheduler": False,
        "enable_weekly_scheduler": False,
        "enable_triggered_nightly_scheduler": False,
    },
    'ash': {
        'merge_builds': False,
        'enable_perproduct_builds': True,
        'pgo_strategy': 'per-checkin',
        'enable_l10n': True,
        'enable_l10n_onchange': True,
        'l10n_repo_path': 'l10n-central',
        'l10n_platforms': ['linux', 'linux64', 'win32', 'macosx64', 'win64'],
        'l10nDatedDirs': True,
        'l10n_tree': 'fxcentral',
        'updates_enabled': True,
        'l10nNightlyUpdate': True,
        'enUS_binaryURL': '/nightly/latest-ash',
        'enable_mac_a11y': True,
        'enable_multi_locale': True,
        'create_partial': True,
        'create_partial_l10n': True,
        'upload_mobile_symbols': True,
        'desktop_mozharness_repacks_enabled': True,
        'l10n_extra_configure_args': ['--with-macbundlename-prefix=Firefox'],
        'enable_nightly': True,
        'platforms': {
            'linux': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'linux64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'macosx64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win64': {
                'nightly_signing_servers': 'nightly-signing',
            },
        },
    },
    #'birch': {},  # Bug 1010674
    'cedar': {
        'enable_perproduct_builds': False,
        'mozharness_tag': 'default',
        'enable_talos': True,
        'talos_suites': {
            'xperf': 1,
        },
        'enable_opt_unittests': True,
        'mobile_platforms': {
            'android-x86': {
                'enable_opt_unittests': True,
            },
        },
    },
    'cypress': {
        'gecko_version': 40,
        'enable_perproduct_builds': False,
        'enable_talos': True,
        'pgo_strategy': 'per-checkin',
        'lock_platforms': True,
        'platforms': {
            # Limit to win64 for Bug 1164935
            'win64': {},
            'win64-debug': {},
        },
    },
    'date': {
        'desktop_mozharness_builds_enabled': True,
        'use_mozharness_repo_cache': False,
        'branch_projects': [],
        'enable_talos': False,
        'enable_opt_unittests': False,
        'enable_debug_unittests': False,
        'lock_platforms': True,
        'platforms': {
            'linux': {
                "slave_platforms": [],
            },
            'linux64': {
                "slave_platforms": [],
            },
            'win32': {
                "slave_platforms": [],
            },
            'macosx64': {
                "slave_platforms": [],
            },
            'linux-debug': {
                "slave_platforms": [],
            },
            'linux64-debug': {
                "slave_platforms": [],
            },
            'linux64-asan': {
                "slave_platforms": [],
            },
            'linux64-asan-debug': {
                "slave_platforms": [],
            },
            'macosx64-debug': {
                "slave_platforms": [],
            },
            'win32-debug': {
                "slave_platforms": [],
            },
            'win64': {
                "slave_platforms": [],
            },
            'win64-debug': {
                "slave_platforms": [],
            },
        },
        'enable_valgrind': False,
        'pgo_strategy': 'per-checkin',
        'enable_release_promotion': True,
        'partners_repo_path': 'build/partner-repacks',
        'partner_repack_platforms': ('linux', 'linux64', 'win32', 'win64', 'macosx64'),
        "release_platforms": ("linux", "linux64", "win32", "win64", "macosx64"),
        "l10n_release_platforms": ("linux", "linux64", "win32", "win64", "macosx64"),
        'balrog_api_root': 'https://aus4-admin-dev.allizom.org/api',
        'tuxedoServerUrl':  'https://bounceradmin.mozilla.com/api',
        'bouncer_submitter_config':  "releases/bouncer_firefox_date.py",
        'bouncer_branch': "releases/date",
        'bouncer_enabled': True
    },
    'elm': {
        'branch_projects': [],
        'enable_talos': True,
        'enable_valgrind': False,
        'lock_platforms': True,
        'platforms': {
            # dep signing with nightly key, see bug 1176152
            'linux': {
                'dep_signing_servers': 'nightly-signing',
            },
            'linux64': {
                'dep_signing_servers': 'nightly-signing',
            },
            'linux-debug': {},
            'linux64-debug': {},
        },
    },
    # Dsiabled by Bug 1135702
    # 'fig': {},
    # Disabled by Bug 1206269
    # 'gum': {},
    # disabled in bug 1215527
    # 'holly': {},
    'jamun': {
        'lock_platforms': True,
        'platforms': {
            'linux': {},
            'linux64': {},
            'linux-debug': {},
            'linux64-br-haz': {},
            'linux64-asan': {},
            'linux64-asan-debug': {},
            'linux64-debug': {},
            'linux64-st-an-debug': {},
            'macosx64-debug': {},
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
            'macosx64': {},
            'macosx64-st-an-debug': {},
        }
    },
    'larch': {
        'lock_platforms': True,
        'platforms': {
        },
    },
    # disabled in bug 1215527
    # 'maple': {},
    # customizations for integration work for bugs 481815 and 307181
    'oak': {
        'enable_nightly': True,
        'updates_enabled': True,
        'create_partial': True,
        'enable_talos': False,
        'pgo_strategy': 'periodic',
        'platforms': {
            'linux': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'linux64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'macosx64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win64': {
                'nightly_signing_servers': 'nightly-signing',
            },
        },
    },
    # Not needed whilst booked for bug 929203.
    #'pine': {}
}

# All is the default
ACTIVE_PROJECT_BRANCHES = PROJECT_BRANCHES.keys()

# Load up project branches' local values
for branch in PROJECT_BRANCHES.keys():
    PROJECT_BRANCHES[branch]['tinderbox_tree'] = PROJECT_BRANCHES[branch].get('tinderbox_tree', branch.title())
    PROJECT_BRANCHES[branch]['mobile_tinderbox_tree'] = PROJECT_BRANCHES[branch].get('mobile_tinderbox_tree', branch.title())
