from copy import deepcopy

from config import MOZHARNESS_REBOOT_CMD
from localconfig import SLAVES, TRY_SLAVES, GLOBAL_VARS

import b2g_localconfig
reload(b2g_localconfig)

from buildbot.steps.shell import WithProperties

GLOBAL_VARS = deepcopy(GLOBAL_VARS)

GLOBAL_VARS['stage_username'] = 'ffxbld'
GLOBAL_VARS.update(b2g_localconfig.GLOBAL_VARS.copy())

BRANCHES = {
    'ash': {},
    'cedar': {},
    'fx-team': {},
    'mozilla-b2g18': {},
    'mozilla-b2g18_v1_0_0': {},
    'mozilla-central': {},
    'mozilla-inbound': {},
    'services-central': {},
    'try': {'coallesce_jobs': False},
}

PLATFORMS = {
    'ics_armv7a_gecko': {},
    'b2g_panda': {},
    'b2g_panda_gaia_central': {},
}

builder_prefix = "b2g"

PLATFORMS['ics_armv7a_gecko']['slave_platforms'] = ['fedora-b2g']
PLATFORMS['ics_armv7a_gecko']['env_name'] = 'linux-perf'
PLATFORMS['ics_armv7a_gecko']['fedora-b2g'] = {'name': builder_prefix + "_ics_armv7a_gecko_emulator"}
PLATFORMS['ics_armv7a_gecko']['stage_product'] = 'b2g'
PLATFORMS['ics_armv7a_gecko']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['b2g_panda']['slave_platforms'] = ['b2g_panda']
PLATFORMS['b2g_panda']['env_name'] = None
PLATFORMS['b2g_panda']['b2g_panda'] = {'name': builder_prefix + "_panda"}
PLATFORMS['b2g_panda']['stage_product'] = 'b2g'
PLATFORMS['b2g_panda']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    # path to hg on the foopies
    'hg_bin': '/usr/local/bin/hg',
    # TODO: call something else
    'reboot_command': None,
}

PLATFORMS['b2g_panda_gaia_central']['slave_platforms'] = ['b2g_panda_gaia_central']
PLATFORMS['b2g_panda_gaia_central']['env_name'] = None
PLATFORMS['b2g_panda_gaia_central']['b2g_panda_gaia_central'] = {'name': builder_prefix + "_panda_gaia_central"}
PLATFORMS['b2g_panda_gaia_central']['stage_product'] = 'b2g'
PLATFORMS['b2g_panda_gaia_central']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    # path to hg on the foopies
    'hg_bin': '/usr/local/bin/hg',
    # TODO: call something else
    'reboot_command': None,
}

# Lets be explicit instead of magical.  leopard-o should be a second
# entry in the SLAVE dict
for platform, platform_config in PLATFORMS.items():
    for slave_platform in platform_config['slave_platforms']:
        platform_config[slave_platform]['slaves'] = sorted(SLAVES[slave_platform])
        if slave_platform in TRY_SLAVES:
            platform_config[slave_platform]['try_slaves'] = sorted(TRY_SLAVES[slave_platform])
        else:
            platform_config[slave_platform]['try_slaves'] = platform_config[slave_platform]['slaves']

BRANCH_UNITTEST_VARS = {
    'hghost': 'hg.mozilla.org',
    # turn on platforms as we get them running
    'platforms': {
        'ics_armv7a_gecko': {},
        'b2g_panda': {},
        'b2g_panda_gaia_central': {},
    },
}

SUITES = {}

MOCHITEST_ONLY = [
    ('mochitest-1', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('mochitest-2', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('mochitest-3', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('mochitest-4', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('mochitest-5', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('mochitest-6', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
]
REFTEST_ONLY = [
    ('reftest-1', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-2', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-3', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-4', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-5', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-6', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-7', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-8', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-9', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
    ('reftest-10', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
]

CRASHTEST_ONLY = [
    ('crashtest-1', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('crashtest-2', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
    ('crashtest-3', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                    },
    ),
]

XPCSHELL_ONLY = [
    ('xpcshell', {'suite': 'xpcshell',
                  'use_mozharness': True,
                  'script_path': 'scripts/b2g_emulator_unittest.py',
                  },
    ),
]

ALL_UNITTESTS = MOCHITEST_ONLY + REFTEST_ONLY + CRASHTEST_ONLY + XPCSHELL_ONLY + [
    ('marionette-webapi', {'suite': 'marionette-webapi',
                           'use_mozharness': True,
                           'script_path': 'scripts/marionette.py',
                          },
    ),
]

# Default set of unit tests
UNITTEST_SUITES = {
    'opt_unittest_suites': ALL_UNITTESTS[:],
    'debug_unittest_suites': [],
}

# You must define opt_unittest_suites when enable_opt_unittests is True for a
# platform. Likewise debug_unittest_suites for enable_debug_unittests
PLATFORM_UNITTEST_VARS = {
    'ics_armv7a_gecko': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env' : {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'fedora-b2g': {
            'opt_unittest_suites' : \
                UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites' : UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'crashtest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'crashtest',
                        '--this-chunk', '1', '--total-chunks', '3',
                    ],
                },
                'crashtest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'crashtest',
                        '--this-chunk', '2', '--total-chunks', '3',
                    ],
                },
                'crashtest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'crashtest',
                        '--this-chunk', '3', '--total-chunks', '3',
                    ],
                },
                'marionette-webapi': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py"
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '1', '--total-chunks', '6',
                    ],
                },
                'mochitest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '2', '--total-chunks', '6',
                    ],
                },
                'mochitest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '3', '--total-chunks', '6',
                    ],
                },
                'mochitest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '4', '--total-chunks', '6',
                    ],
                },
                'mochitest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '5', '--total-chunks', '6',
                    ],
                },
                'mochitest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '6', '--total-chunks', '6',
                    ],
                },
                'reftest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '1', '--total-chunks', '10',
                    ],
                },
                'reftest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '2', '--total-chunks', '10',
                    ],
                },
                'reftest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '3', '--total-chunks', '10',
                    ],
                },
                'reftest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '4', '--total-chunks', '10',
                    ],
                },
                'reftest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '5', '--total-chunks', '10',
                    ],
                },
                'reftest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '6', '--total-chunks', '10',
                    ],
                },
                'reftest-7': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '7', '--total-chunks', '10',
                    ],
                },
                'reftest-8': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '8', '--total-chunks', '10',
                    ],
                },
                'reftest-9': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '9', '--total-chunks', '10',
                    ],
                },
                'reftest-10': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '10', '--total-chunks', '10',
                    ],
                },
                'xpcshell': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'xpcshell',
                    ],
                },
            },
        },
    }, # end of ics_armv7a_gecko configs
    'b2g_panda': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'builds_before_reboot': 1,
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'b2g_panda': {
            'opt_unittest_suites' : [
                ('gaia-ui-test', {
                    'suite': 'gaia-ui-test',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_panda.py',
                },)
            ],
            'debug_unittest_suites' : [],
            'suite_config': {
                'gaia-ui-test': {
                    'extra_args': ["--cfg", "b2g/panda_releng.py" ],
                },
            },
        },
    },
    'b2g_panda_gaia_central': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'builds_before_reboot': 1,
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'b2g_panda_gaia_central': {
            'opt_unittest_suites' : [
                ('gaia-ui-test', {
                    'suite': 'gaia-ui-test',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_panda.py',
                },)
            ],
            'debug_unittest_suites' : [],
            'suite_config': {
                'gaia-ui-test': {
                    'extra_args': ["--cfg", "b2g/panda_releng.py" ],
                },
            },
        },
    },
}

# Copy unittest vars in first, then platform vars
for branch in BRANCHES.keys():
    for key, value in GLOBAL_VARS.items():
        # Don't override platforms if it's set
        if key == 'platforms' and 'platforms' in BRANCHES[branch]:
            continue
        BRANCHES[branch][key] = deepcopy(value)

    for key, value in BRANCH_UNITTEST_VARS.items():
        # Don't override platforms if it's set and locked
        if key == 'platforms' and 'platforms' in BRANCHES[branch] and BRANCHES[branch].get('lock_platforms'):
            continue
        BRANCHES[branch][key] = deepcopy(value)

    for platform, platform_config in PLATFORM_UNITTEST_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

    # Copy in local config
    if branch in b2g_localconfig.BRANCHES:
        for key, value in b2g_localconfig.BRANCHES[branch].items():
            if key == 'platforms':
                # Merge in these values
                if 'platforms' not in BRANCHES[branch]:
                    BRANCHES[branch]['platforms'] = {}

                for platform, platform_config in value.items():
                    for key, value in platform_config.items():
                        value = deepcopy(value)
                        if isinstance(value, str):
                            value = value % locals()
                        BRANCHES[branch]['platforms'][platform][key] = value
            else:
                BRANCHES[branch][key] = deepcopy(value)

#    # Merge in any project branch config for platforms
#    if branch in ACTIVE_PROJECT_BRANCHES and PROJECT_BRANCHES[branch].has_key('platforms'):
#        for platform, platform_config in PROJECT_BRANCHES[branch]['platforms'].items():
#            if platform in PLATFORMS:
#                for key, value in platform_config.items():
#                    value = deepcopy(value)
#                    if isinstance(value, str):
#                        value = value % locals()
#                    BRANCHES[branch]['platforms'][platform][key] = value

    for platform, platform_config in b2g_localconfig.PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

########
# Entries in BRANCHES for tests should be a tuple of:
# - Number of tests to run per build
# - Whether queue merging is on
# - TalosFactory options
# - Which platforms to run on

# Let's load the defaults
for branch in BRANCHES.keys():
    BRANCHES[branch]['repo_path'] = branch
    BRANCHES[branch]['branch_name'] = branch.title()
    BRANCHES[branch]['build_branch'] = branch.title()
    BRANCHES[branch]['enable_unittests'] = True
    BRANCHES[branch]['fetch_symbols'] = True
    BRANCHES[branch]['fetch_release_symbols'] = False
    BRANCHES[branch]['pgo_strategy'] = None
    BRANCHES[branch]['pgo_platforms'] = []

# The following are exceptions to the defaults

BRANCHES['ash']['branch_name'] = "Ash"
BRANCHES['ash']['repo_path'] = "projects/ash"
BRANCHES['ash']['mozharness_repo'] = "http://hg.mozilla.org/users/asasaki_mozilla.com/ash-mozharness"
BRANCHES['ash']['mozharness_tag'] = "default"
BRANCHES['ash']['platforms']['ics_armv7a_gecko']['fedora-b2g']['debug_unittest_suites'] = ALL_UNITTESTS[:]
BRANCHES['ash']['platforms']['ics_armv7a_gecko']['enable_debug_unittests'] = True
BRANCHES['cedar']['branch_name'] = "Cedar"
BRANCHES['cedar']['repo_path'] = "projects/cedar"
BRANCHES['cedar']['mozharness_tag'] = "default"
BRANCHES['cedar']['platforms']['ics_armv7a_gecko']['fedora-b2g']['debug_unittest_suites'] = ALL_UNITTESTS[:]
BRANCHES['cedar']['platforms']['ics_armv7a_gecko']['enable_debug_unittests'] = True
BRANCHES['fx-team']['repo_path'] = "integration/fx-team"
BRANCHES['mozilla-b2g18']['repo_path'] = "releases/mozilla-b2g18"
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['opt_unittest_suites'] = [x for x in ALL_UNITTESTS if x not in CRASHTEST_ONLY]
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['debug_unittest_suites'] = MOCHITEST_ONLY + XPCSHELL_ONLY
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['enable_debug_unittests'] = True
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-1'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '1', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-2'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '2', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-3'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '3', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-4'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '4', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-5'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '5', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-6'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '6', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-7'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '7', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-8'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '8', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-9'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '9', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-10'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '10', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['repo_path'] = "releases/mozilla-b2g18_v1_0_0"
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['opt_unittest_suites'] = [x for x in ALL_UNITTESTS if x not in CRASHTEST_ONLY]
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['debug_unittest_suites'] = MOCHITEST_ONLY + XPCSHELL_ONLY
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['enable_debug_unittests'] = True
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-1'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '1', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-2'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '2', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-3'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '3', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-4'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '4', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-5'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '5', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-6'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '6', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-7'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '7', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-8'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '8', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-9'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '9', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-b2g18_v1_0_0']['platforms']['ics_armv7a_gecko']['fedora-b2g']['suite_config']['reftest-10'] = {
    'extra_args': [
        '--cfg', 'b2g/emulator_automation_config.py',
        '--test-suite', 'reftest',
        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
        '--this-chunk', '10', '--total-chunks', '10',
    ],
}
BRANCHES['mozilla-central']['branch_name'] = "Firefox"
BRANCHES['mozilla-inbound']['repo_path'] = "integration/mozilla-inbound"
BRANCHES['services-central']['repo_path'] = "services/services-central"
BRANCHES['try']['pgo_strategy'] = "try"
BRANCHES['try']['enable_try'] = True

if __name__ == "__main__":
    import sys, pprint, re

    class BBPrettyPrinter(pprint.PrettyPrinter):
        def format(self, object, context, maxlevels, level):
            if isinstance(object, WithProperties):
                return pprint.PrettyPrinter.format(self, object.fmtstring, context, maxlevels, level)
            return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

    args = sys.argv[1:]

    if len(args) > 0:
        branches = args
    else:
        branches = BRANCHES.keys()

    pp = BBPrettyPrinter()
    for branch in branches:
        print branch
        pp.pprint(BRANCHES[branch])

    for suite in SUITES:
        print suite
        pp.pprint(SUITES[suite])
