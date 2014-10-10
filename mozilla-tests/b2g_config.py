from copy import deepcopy

from config import MOZHARNESS_REBOOT_CMD

import localconfig
reload(localconfig)
from localconfig import SLAVES, TRY_SLAVES, GLOBAL_VARS

import b2g_localconfig
reload(b2g_localconfig)

import master_common
reload(master_common)
from master_common import setMainFirefoxVersions, items_before, items_at_least

import config_common
reload(config_common)
from config_common import nested_haskey

# Import WithProperties for gaia-try.  Allow for a bogus WithProperties for
# tools that don't want to have the full buildbot stack.
try:
    from buildbot.steps.shell import WithProperties
except ImportError:
    def WithProperties(s):
        return s

GLOBAL_VARS = deepcopy(GLOBAL_VARS)

GLOBAL_VARS['stage_username'] = 'ffxbld'
GLOBAL_VARS.update(b2g_localconfig.GLOBAL_VARS.copy())

BRANCHES = {
    'ash': {},
    # Not needed right now, see bug 977420
    # 'birch': {},
    'cedar': {},
    'cypress': {},
    'jamun': {},
    'pine': {},
    'fx-team': {},
    'graphics': {},
    'mozilla-b2g28_v1_3t': {
        'gecko_version': 28,
        'b2g_version': (1, 3, 0),
        'lock_platforms': True,
        'platforms': {
            'emulator': {},
        },
    },
    'mozilla-b2g30_v1_4': {
        'gecko_version': 30,
        'b2g_version': (1, 4, 0),
    },
    'mozilla-b2g32_v2_0': {
        'gecko_version': 32,
        'b2g_version': (2, 0, 0),
    },
    'mozilla-b2g34_v2_1': {
        'gecko_version': 34,
        'b2g_version': (2, 1, 0),
    },
    'mozilla-aurora': {
        'gecko_version': 34,
        'b2g_version': (2, 1, 0),
    },
    'mozilla-central': {},
    'mozilla-inbound': {},
    'b2g-inbound': {},
    #'services-central': {},  # Bug 1010674
    'try': {},
    'gaia-try': {
        'lock_platforms': True,
        'platforms': {
            'linux32_gecko': {},
            'linux64_gecko': {},
            'macosx64_gecko': {},
        },
    },
}

setMainFirefoxVersions(BRANCHES)

PLATFORMS = {
    'linux32_gecko': {},
    'linux64_gecko': {},
    'linux64-mulet': {},
    'macosx64_gecko': {},
    'macosx64-mulet': {},
    'emulator': {},
    'emulator-jb': {},
    'emulator-kk': {},
}

builder_prefix = "b2g"

PLATFORMS['linux32_gecko']['slave_platforms'] = ['ubuntu32_vm-b2gdt', ]
PLATFORMS['linux32_gecko']['env_name'] = 'linux-perf'
PLATFORMS['linux32_gecko']['ubuntu32_vm-b2gdt'] = {'name': builder_prefix + "_ubuntu32_vm"}
PLATFORMS['linux32_gecko']['stage_product'] = 'b2g'
PLATFORMS['linux32_gecko']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['linux64_gecko']['slave_platforms'] = ['ubuntu64_vm-b2gdt', ]
PLATFORMS['linux64_gecko']['env_name'] = 'linux-perf'
PLATFORMS['linux64_gecko']['ubuntu64_vm-b2gdt'] = {'name': builder_prefix + "_ubuntu64_vm"}
PLATFORMS['linux64_gecko']['stage_product'] = 'b2g'
PLATFORMS['linux64_gecko']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['linux64-mulet']['slave_platforms'] = ['ubuntu64_vm-mulet']
PLATFORMS['linux64-mulet']['env_name'] = 'linux-perf'
PLATFORMS['linux64-mulet']['ubuntu64_vm-mulet'] = {'name': 'Ubuntu VM 12.04 x64 Mulet'}
PLATFORMS['linux64-mulet']['stage_product'] = 'b2g'
PLATFORMS['linux64-mulet']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['macosx64_gecko']['slave_platforms'] = ['mountainlion-b2gdt', ]
PLATFORMS['macosx64_gecko']['env_name'] = 'linux-perf'
PLATFORMS['macosx64_gecko']['mountainlion-b2gdt'] = {'name': builder_prefix + "_macosx64"}
PLATFORMS['macosx64_gecko']['stage_product'] = 'b2g'
PLATFORMS['macosx64_gecko']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['macosx64-mulet']['slave_platforms'] = ['snowleopard']
PLATFORMS['macosx64-mulet']['env_name'] = 'mac-perf'
PLATFORMS['macosx64-mulet']['snowleopard'] = {
    'name': 'Rev4 MacOSX Mulet Snow Leopard 10.6',
    'build_dir_prefix': 'snowleopard_mulet',
    'scheduler_slave_platform_identifier': 'snowleopard_mulet'
}
PLATFORMS['macosx64-mulet']['stage_product'] = 'b2g'
PLATFORMS['macosx64-mulet']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['emulator']['slave_platforms'] = ['ubuntu64_vm-b2g-emulator', 'ubuntu64_vm-b2g-lg-emulator']
PLATFORMS['emulator']['env_name'] = 'linux-perf'
PLATFORMS['emulator']['ubuntu64_vm-b2g-emulator'] = {'name': "b2g_emulator_vm"}
PLATFORMS['emulator']['ubuntu64_vm-b2g-lg-emulator'] = {'name': "b2g_emulator_vm_large"}
PLATFORMS['emulator']['stage_product'] = 'b2g'
PLATFORMS['emulator']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['emulator-jb']['slave_platforms'] = ['ubuntu64_vm-b2g-emulator-jb']
PLATFORMS['emulator-jb']['env_name'] = 'linux-perf'
PLATFORMS['emulator-jb']['ubuntu64_vm-b2g-emulator-jb'] = {'name': "b2g_emulator-jb_vm"}
PLATFORMS['emulator-jb']['stage_product'] = 'b2g'
PLATFORMS['emulator-jb']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

PLATFORMS['emulator-kk']['slave_platforms'] = ['ubuntu64_vm-b2g-emulator-kk']
PLATFORMS['emulator-kk']['env_name'] = 'linux-perf'
PLATFORMS['emulator-kk']['ubuntu64_vm-b2g-emulator-kk'] = {'name': "b2g_emulator-kk_vm"}
PLATFORMS['emulator-kk']['stage_product'] = 'b2g'
PLATFORMS['emulator-kk']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'use_mozharness': True,
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

# Lets be explicit instead of magical.
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
        'linux32_gecko': {},
        'linux64_gecko': {},
        'linux64-mulet': {},
        'macosx64_gecko': {},
        'macosx64-mulet': {},
        'emulator': {},
        'emulator-jb': {},
        'emulator-kk': {},
    },
}

SUITES = {}

MOCHITEST = [
    ('mochitest-1', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-2', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-3', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-4', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-5', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-6', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-7', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-8', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('mochitest-9', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
]

MOCHITEST_EMULATOR_JB = [
    ('mochitest-1', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
]

MOCHITEST_MULET_PLAIN = [
    ('mochitest-1', {'suite': 'mochitest-plain',
                                 'use_mozharness': True,
                                 'script_path': 'scripts/desktop_unittest.py',
                                 'blob_upload': True,
                                }
    ),
    ('mochitest-2', {'suite': 'mochitest-plain',
                                 'use_mozharness': True,
                                 'script_path': 'scripts/desktop_unittest.py',
                                 'blob_upload': True,
                                }
    ),
    ('mochitest-3', {'suite': 'mochitest-plain',
                                 'use_mozharness': True,
                                 'script_path': 'scripts/desktop_unittest.py',
                                 'blob_upload': True,
                                }
    ),
    ('mochitest-4', {'suite': 'mochitest-plain',
                                 'use_mozharness': True,
                                 'script_path': 'scripts/desktop_unittest.py',
                                 'blob_upload': True,
                                }
    ),
    ('mochitest-5', {'suite': 'mochitest-plain',
                                 'use_mozharness': True,
                                 'script_path': 'scripts/desktop_unittest.py',
                                 'blob_upload': True,
                                }
    ),
]

REFTEST_MULET = [
    ('reftest', {
        'suite': 'reftest',
        'use_mozharness': True,
        'script_path': 'scripts/mulet_unittest.py',
        'blob_upload': True,
    }),
]

MOCHITEST_EMULATOR_DEBUG = [
    ('mochitest-debug-1', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-2', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-3', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-4', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-5', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-6', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-7', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-8', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-9', {'suite': 'mochitest-plain',
                           'use_mozharness': True,
                           'script_path': 'scripts/b2g_emulator_unittest.py',
                           'blob_upload': True,
                           },
     ),
    ('mochitest-debug-10', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-11', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-12', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-13', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-14', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-15', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-16', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-17', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-18', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-19', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
    ('mochitest-debug-20', {'suite': 'mochitest-plain',
                            'use_mozharness': True,
                            'script_path': 'scripts/b2g_emulator_unittest.py',
                            'blob_upload': True,
                            },
     ),
]

MOCHITEST_MEDIA = [
    ('mochitest-media', {'suite': 'mochitest-plain',
                         'use_mozharness': True,
                         'script_path': 'scripts/b2g_emulator_unittest.py',
                         'blob_upload': True,
                        },
     ),
]

MOCHITEST_DESKTOP = [
    ('mochitest-1', {'suite': 'mochitest-plain',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_desktop_unittest.py',
                     'blob_upload': True,
                     },
     ),
]

MOCHITEST_OOP_DESKTOP = [('mochitest-oop-1', MOCHITEST_DESKTOP[0][1])]

GAIA_JS_INTEGRATION = [
    ('gaia-js-integration-1', {'suite': 'gaia-js-integration',
                           'use_mozharness': True,
                           'script_path': 'scripts/gaia_integration.py',
                           'timeout': 500,
                           },
    ),
    ('gaia-js-integration-2', {'suite': 'gaia-js-integration',
                           'use_mozharness': True,
                           'script_path': 'scripts/gaia_integration.py',
                           'timeout': 500,
                           },
    ),
    ('gaia-js-integration-3', {'suite': 'gaia-js-integration',
                           'use_mozharness': True,
                           'script_path': 'scripts/gaia_integration.py',
                           'timeout': 500,
                           },
    ),
    ('gaia-js-integration-4', {'suite': 'gaia-js-integration',
                           'use_mozharness': True,
                           'script_path': 'scripts/gaia_integration.py',
                           'timeout': 500,
                           },
    ),
]

REFTEST = [
    ('reftest-1', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-2', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-3', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-4', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-5', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-6', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-7', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-8', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-9', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_emulator_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-10', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
]

REFTEST_20 = REFTEST[:]
REFTEST_20 += [
    ('reftest-11', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-12', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-13', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-14', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-15', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-16', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-17', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-18', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-19', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('reftest-20', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
]

REFTEST_SANITY = [
    ('reftest-sanity', {'suite': 'reftest',
                        'use_mozharness': True,
                        'script_path': 'scripts/b2g_emulator_unittest.py',
                       },
     ),
]

REFTEST_DESKTOP = [
    ('reftest-1', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-2', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-3', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-4', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-5', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-6', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-7', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-8', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-9', {'suite': 'reftest',
                   'use_mozharness': True,
                   'script_path': 'scripts/b2g_desktop_unittest.py',
                   'blob_upload': True,
                   },
     ),
    ('reftest-10', {'suite': 'reftest',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_desktop_unittest.py',
                    'blob_upload': True,
                    },
     ),
]

REFTEST_DESKTOP_SANITY = [
    ('reftest-sanity', {'suite': 'reftest',
                        'use_mozharness': True,
                        'script_path': 'scripts/b2g_desktop_unittest.py',
                        'blob_upload': True,
                       },
     ),
]

REFTEST_DESKTOP_OOP_SANITY = [('reftest-sanity-oop', REFTEST_DESKTOP_SANITY[0][1])]

JSREFTEST = [
    ('jsreftest-1', {'suite': 'jsreftest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('jsreftest-2', {'suite': 'jsreftest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('jsreftest-3', {'suite': 'jsreftest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
]

CRASHTEST = [
    ('crashtest-1', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('crashtest-2', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
    ('crashtest-3', {'suite': 'crashtest',
                     'use_mozharness': True,
                     'script_path': 'scripts/b2g_emulator_unittest.py',
                     'blob_upload': True,
                     },
     ),
]

MARIONETTE = [
    ('marionette-webapi', {'suite': 'marionette-webapi',
                           'use_mozharness': True,
                           'script_path': 'scripts/marionette.py',
                           'blob_upload': True,
                           },
     ),
]

MARIONETTE_UNIT = [
    ('marionette', {'suite': 'marionette',
                     'use_mozharness': True,
                     'script_path': 'scripts/marionette.py',
                     'blob_upload': True,
                     },
    ),
]

XPCSHELL = [
    ('xpcshell', {'suite': 'xpcshell',
                  'use_mozharness': True,
                  'script_path': 'scripts/b2g_emulator_unittest.py',
                  'blob_upload': True,
                  },
     ),
]

XPCSHELL_CHUNKED = [
    ('xpcshell-1', {'suite': 'xpcshell',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
    ('xpcshell-2', {'suite': 'xpcshell',
                    'use_mozharness': True,
                    'script_path': 'scripts/b2g_emulator_unittest.py',
                    'blob_upload': True,
                    },
     ),
]

GAIA_INTEGRATION = [(
    'gaia-integration', {
        'suite': 'gaia-integration',
        'use_mozharness': True,
        'script_path': 'scripts/gaia_integration.py',
        'timeout': 1800,
    },
)]

GAIA_BUILD = [(
    'gaia-build', {
        'suite': 'gaia-build',
        'use_mozharness': True,
        'script_path': 'scripts/gaia_build_integration.py',
        'timeout': 1800,
    },
)]

GAIA_BUILD_UNIT = [(
    'gaia-build-unit', {
        'suite': 'gaia-build-unit',
        'use_mozharness': True,
        'script_path': 'scripts/gaia_build_unit.py',
        'timeout': 1800,
    },
)]

GAIA_LINTER = [(
    'gaia-linter', {
        'suite': 'gaia-linter',
        'use_mozharness': True,
        'script_path': 'scripts/gaia_linter.py',
        'timeout': 1800,
    },
)]

GAIA_UNITTESTS = [(
    'gaia-unit', {
        'suite': 'gaia-unit',
        'use_mozharness': True,
        'script_path': 'scripts/gaia_unit.py',
        'blob_upload': True,
    },
)]

GAIA_UNITTESTS_OOP = [('gaia-unit-oop', GAIA_UNITTESTS[0][1])]

GAIA_UI = [(
    'gaia-ui-test', {
        'suite': 'gaia-ui-test',
        'use_mozharness': True,
        'script_path': 'scripts/marionette.py',
        'blob_upload': True,
    },
)]

#Gaia Python Integration Tests
# will replae GAIA_UI, Bug 1046694
GIP = [
    ('gaia-ui-test-functional-1', {
                                    'suite': 'gip',
                                    'use_mozharness': True,
                                    'script_path': 'scripts/marionette.py',
                                    'blob_upload': True,
                                   },
    ),
    ('gaia-ui-test-functional-2', {
                                    'suite': 'gip',
                                    'use_mozharness': True,
                                    'script_path': 'scripts/marionette.py',
                                    'blob_upload': True,
                                   },
    ),
    ('gaia-ui-test-functional-3', {
                                    'suite': 'gip',
                                    'use_mozharness': True,
                                    'script_path': 'scripts/marionette.py',
                                    'blob_upload': True,
                                   },
    ),
    ('gaia-ui-test-unit', {
                            'suite': 'gip',
                            'use_mozharness': True,
                            'script_path': 'scripts/marionette.py',
                            'blob_upload': True,
                           },
    ),
    ('gaia-ui-test-accessibility', {
                                     'suite': 'gip',
                                     'use_mozharness': True,
                                     'script_path': 'scripts/marionette.py',
                                     'blob_upload': True,
                                   },
    )
]

GAIA_UI_OOP = [('gaia-ui-test-oop', GAIA_UI[0][1])]

CPPUNIT = [(
    'cppunit', {
        'suite': 'cppunit',
        'use_mozharness': True,
        'script_path': 'scripts/b2g_emulator_unittest.py',
        'blob_upload': True,
    },
)]

ALL_UNITTESTS = MOCHITEST + REFTEST + CRASHTEST + MARIONETTE + MARIONETTE_UNIT + XPCSHELL

# Default set of unit tests
UNITTEST_SUITES = {
    'opt_unittest_suites': ALL_UNITTESTS[:],
    'debug_unittest_suites': [],
}

# You must define opt_unittest_suites when enable_opt_unittests is True for a
# platform. Likewise debug_unittest_suites for enable_debug_unittests
PLATFORM_UNITTEST_VARS = {
    'linux64-mulet': {
        'product_name': 'b2g',
        'app_name': 'firefox',
        'brand_name': 'Mulet',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64_vm-mulet': {
            'opt_unittest_suites': MOCHITEST_MULET_PLAIN[:],
            'debug_unittest_suites': [],
            'suite_config': {
                'mochitest-1': {
                    'extra_args': [
                      '--cfg', 'unittests/linux_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 1,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-2': {
                    'extra_args': [
                      '--cfg', 'unittests/linux_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 2,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-3': {
                    'extra_args': [
                      '--cfg', 'unittests/linux_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 3,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-4': {
                    'extra_args': [
                      '--cfg', 'unittests/linux_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 4,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-5': {
                    'extra_args': [
                      '--cfg', 'unittests/linux_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 5,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'reftest': {
                    'extra_args': [
                      '--cfg', 'b2g/generic_config.py',
                      '--cfg', 'b2g/mulet_config.py',
                      '--test-suite', 'reftest',
                      '--test-manifest', 'tests/layout/reftests/reftest.list',
                    ]
                },
            },
        },
    },
    'macosx64-mulet': {
        'product_name': 'b2g',
        'app_name': 'firefox',
        'brand_name': 'Mulet',
        'builds_before_reboot': 1,
        'unittest-env': {
            "MOZ_NO_REMOTE": '1',
            "NO_EM_RESTART": '1',
            "XPCOM_DEBUG_BREAK": 'warn',
            "MOZ_CRASHREPORTER_NO_REPORT": '1',
            # for extracting dmg's
            "PAGER": '/bin/cat',
        },
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'snowleopard': {
            'opt_unittest_suites': MOCHITEST_MULET_PLAIN[:],
            'debug_unittest_suites': [],
            'suite_config': {
                'mochitest-1': {
                    'extra_args': [
                      '--cfg', 'unittests/mac_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 1,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-2': {
                    'extra_args': [
                      '--cfg', 'unittests/mac_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 2,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-3': {
                    'extra_args': [
                      '--cfg', 'unittests/mac_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 3,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-4': {
                    'extra_args': [
                      '--cfg', 'unittests/mac_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 4,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
                'mochitest-5': {
                    'extra_args': [
                      '--cfg', 'unittests/mac_unittest.py',
                      '--total-chunks', 5, '--this-chunk', 5,
                      '--mochitest-suite', 'plain-chunked',
                    ]
                },
            },
        },
    },
    'linux32_gecko': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu32_vm-b2gdt': {
            'opt_unittest_suites': MOCHITEST_DESKTOP[:] + REFTEST_DESKTOP_SANITY[:],
            'debug_unittest_suites': [],
            'suite_config': {
                'gaia-integration': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-js-integration-1': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 1, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-2': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 2, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-3': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 3, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-4': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 4, '--total-chunks', 4,
	                    ],
	            },
                'gaia-unit': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_unit_production_config.py',
                    ],
                },
                'gaia-ui-test': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                    ],
                },
                'gaia-ui-test-functional-1': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '1', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-2': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                       '--this-chunk', '2', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-3': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '3', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-unit': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'unit',
                    ],
                },
                'gaia-ui-test-accessibility': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'accessibility',
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', 1, '--total-chunks', 1,
                    ],
                },
                'reftest-sanity': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
                    ],
                },
                'reftest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 1, '--total-chunks', 10,
                    ],
                },
                'reftest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 2, '--total-chunks', 10,
                    ],
                },
                'reftest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 3, '--total-chunks', 10,
                    ],
                },
                'reftest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 4, '--total-chunks', 10,
                    ],
                },
                'reftest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 5, '--total-chunks', 10,
                    ],
                },
                'reftest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 6, '--total-chunks', 10,
                    ],
                },
                'reftest-7': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 7, '--total-chunks', 10,
                    ],
                },
                'reftest-8': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 8, '--total-chunks', 10,
                    ],
                },
                'reftest-9': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 9, '--total-chunks', 10,
                    ],
                },
                'reftest-10': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 10, '--total-chunks', 10,
                    ],
                },
            },
        },
    },
    'linux64_gecko': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'ubuntu64_vm-b2gdt': {
            'opt_unittest_suites': GAIA_UI[:] + MOCHITEST_DESKTOP[:] + GAIA_INTEGRATION[:] + \
                    REFTEST_DESKTOP_SANITY[:] + GAIA_UNITTESTS[:] + GAIA_LINTER[:],
            'debug_unittest_suites': GAIA_UI[:],
            'suite_config': {
                'gaia-integration': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-js-integration-1': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 1, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-2': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 2, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-3': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 3, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-4': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 4, '--total-chunks', 4,
	                    ],
	            },
                'gaia-build': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-build-unit': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-linter': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-unit': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_unit_production_config.py',
                    ],
                },
                'gaia-unit-oop': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_unit_production_config.py',
                        '--browser-arg', '-oop',
                    ],
                },
                'gaia-ui-test': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                    ],
                },
                'gaia-ui-test-functional-1': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '1', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-2': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                       '--this-chunk', '2', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-3': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '3', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-unit': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'unit',
                    ],
                },
                'gaia-ui-test-accessibility': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'accessibility',
                    ],
                },
                'gaia-ui-test-oop': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--app-arg', '-oop',
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', 1, '--total-chunks', 1,
                    ],
                },
                'mochitest-oop-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', 1, '--total-chunks', 1,
                        '--browser-arg', '-oop',
                    ],
                },
                'reftest-sanity': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
                    ],
                },
                'reftest-sanity-oop': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
                        '--browser-arg', '-oop',
                    ],
                },
                'reftest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 1, '--total-chunks', 10,
                    ],
                },
                'reftest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 2, '--total-chunks', 10,
                    ],
                },
                'reftest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 3, '--total-chunks', 10,
                    ],
                },
                'reftest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 4, '--total-chunks', 10,
                    ],
                },
                'reftest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 5, '--total-chunks', 10,
                    ],
                },
                'reftest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 6, '--total-chunks', 10,
                    ],
                },
                'reftest-7': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 7, '--total-chunks', 10,
                    ],
                },
                'reftest-8': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 8, '--total-chunks', 10,
                    ],
                },
                'reftest-9': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 9, '--total-chunks', 10,
                    ],
                },
                'reftest-10': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', 10, '--total-chunks', 10,
                    ],
                },
            },
        },
    },
    'macosx64_gecko': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {
            "MOZ_NO_REMOTE": '1',
            "NO_EM_RESTART": '1',
            "XPCOM_DEBUG_BREAK": 'warn',
            "MOZ_CRASHREPORTER_NO_REPORT": '1',
            # for extracting dmg's
            "PAGER": '/bin/cat',
        },
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'mountainlion-b2gdt': {
            'opt_unittest_suites': GAIA_UI[:],
            'debug_unittest_suites': [],
            'suite_config': {
                'gaia-integration': {
                    'extra_args': [
                        '--cfg', 'b2g/gaia_integration_config.py',
                    ],
                },
                'gaia-js-integration-1': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 1, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-2': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 2, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-3': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 3, '--total-chunks', 4,
	                    ],
	            },
                'gaia-js-integration-4': {
	                    'extra_args': [
	                        '--cfg', 'b2g/gaia_integration_config.py',
	                        '--this-chunk', 4, '--total-chunks', 4,
	                    ],
	            },
                'gaia-ui-test': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                    ],
                },
                'gaia-ui-test-functional-1': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '1', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-2': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                       '--this-chunk', '2', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-3': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '3', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-unit': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'unit',
                    ],
                },
                'gaia-ui-test-accessibility': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'accessibility',
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', 1, '--total-chunks', 1,
                    ],
                },
                'reftest-sanity': {
                    'extra_args': [
                        '--cfg', 'b2g/desktop_automation_config.py',
                        '--test-suite', 'reftest',
                        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
                    ],
                },
            },
        },
    },
    'emulator': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'ubuntu64_vm-b2g-emulator': {
            'opt_unittest_suites': MOCHITEST + CRASHTEST + XPCSHELL + MARIONETTE + MARIONETTE_UNIT + CPPUNIT,
            'debug_unittest_suites': MOCHITEST_EMULATOR_DEBUG + XPCSHELL_CHUNKED + CPPUNIT,
            'suite_config': {
                'marionette': {
                  'extra_args': [
                      "--cfg", "marionette/automation_emulator_config.py",
                  ],
                },
                'marionette-webapi': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py",
                        "--test-manifest", "webapi-tests.ini"
                    ],
                },
                'gaia-ui-test': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--cfg', 'marionette/gaia_ui_test_emu_config.py',
                    ],
                },
                'gaia-ui-test-functional-1': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '1', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-2': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                       '--this-chunk', '2', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-functional-3': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'functional',
                        '--this-chunk', '3', '--total-chunks', 3,
                    ],
                },
                'gaia-ui-test-unit': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'unit',
                    ],
                },
                'gaia-ui-test-accessibility': {
                    'extra_args': [
                        '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                        '--gip-suite', 'accessibility',
                    ],
                },
                'mochitest-media': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--test-path', 'dom/media/tests/',
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '1', '--total-chunks', '9',
                    ],
                },
                'mochitest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '2', '--total-chunks', '9',
                    ],
                },
                'mochitest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '3', '--total-chunks', '9',
                    ],
                },
                'mochitest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '4', '--total-chunks', '9',
                    ],
                },
                'mochitest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '5', '--total-chunks', '9',
                    ],
                },
                'mochitest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '6', '--total-chunks', '9',
                    ],
                },
                'mochitest-7': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '7', '--total-chunks', '9',
                    ],
                },
                'mochitest-8': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '8', '--total-chunks', '9',
                    ],
                },
                'mochitest-9': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '9', '--total-chunks', '9',
                    ],
                },
                'mochitest-debug-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '1', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '2', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '3', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-4': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '4', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-5': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '5', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-6': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '6', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-7': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '7', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-8': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '8', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-9': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '9', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-10': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '10', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-11': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '11', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-12': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '12', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-13': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '13', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-14': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '14', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-15': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '15', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-16': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '16', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-17': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '17', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-18': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '18', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-19': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '19', '--total-chunks', '20',
                    ],
                },
                'mochitest-debug-20': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '20', '--total-chunks', '20',
                    ],
                },
                'xpcshell': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'xpcshell',
                    ],
                },
                'xpcshell-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'xpcshell',
                        '--this-chunk', '1', '--total-chunks', '2'
                    ],
                },
                'xpcshell-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'xpcshell',
                        '--this-chunk', '2', '--total-chunks', '2'
                    ],
                },
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
                'reftest-sanity': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--test-manifest', 'tests/layout/reftests/reftest-sanity/reftest.list',
                    ],
                },
                'reftest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '1', '--total-chunks', '20',
                    ],
                },
                'reftest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '2', '--total-chunks', '20',
                    ],
                },
                'reftest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '3', '--total-chunks', '20',
                    ],
                },
                'reftest-4': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '4', '--total-chunks', '20',
                    ],
                },
                'reftest-5': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '5', '--total-chunks', '20',
                    ],
                },
                'reftest-6': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '6', '--total-chunks', '20',
                    ],
                },
                'reftest-7': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '7', '--total-chunks', '20',
                    ],
                },
                'reftest-8': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '8', '--total-chunks', '20',
                    ],
                },
                'reftest-9': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '9', '--total-chunks', '20',
                    ],
                },
                'reftest-10': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '10', '--total-chunks', '20',
                    ],
                },
                'reftest-11': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '11', '--total-chunks', '20',
                    ],
                },
                'reftest-12': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '12', '--total-chunks', '20',
                    ],
                },
                'reftest-13': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '13', '--total-chunks', '20',
                    ],
                },
                'reftest-14': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '14', '--total-chunks', '20',
                    ],
                },
                'reftest-15': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '15', '--total-chunks', '20',
                    ],
                },
                'reftest-16': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '16', '--total-chunks', '20',
                    ],
                },
                'reftest-17': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '17', '--total-chunks', '20',
                    ],
                },
                'reftest-18': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '18', '--total-chunks', '20',
                    ],
                },
                'reftest-19': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '19', '--total-chunks', '20',
                    ],
                },
                'reftest-20': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'reftest',
                        '--this-chunk', '20', '--total-chunks', '20',
                    ],
                },
                'jsreftest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'jsreftest',
                        '--this-chunk', '1', '--total-chunks', '3',
                    ],
                },
                'jsreftest-2': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'jsreftest',
                        '--this-chunk', '2', '--total-chunks', '3',
                    ],
                },
                'jsreftest-3': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'jsreftest',
                        '--this-chunk', '3', '--total-chunks', '3',
                    ],
                },
                'cppunit': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'cppunittest',
                    ],
                },
            },
        },
        'ubuntu64_vm-b2g-lg-emulator': {
           'opt_unittest_suites': [],
           'debug_unittest_suites': [],
           'suite_config': {
               'gaia-ui-test': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--cfg', 'marionette/gaia_ui_test_emu_config.py',
                   ],
               },
               'gaia-ui-test-functional-1': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--gip-suite', 'functional',
                       '--this-chunk', '1', '--total-chunks', 3,
                   ],
               },
               'gaia-ui-test-functional-2': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--gip-suite', 'functional',
                      '--this-chunk', '2', '--total-chunks', 3,
                   ],
               },
               'gaia-ui-test-functional-3': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--gip-suite', 'functional',
                       '--this-chunk', '3', '--total-chunks', 3,
                   ],
               },
               'gaia-ui-test-unit': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--gip-suite', 'unit',
                   ],
               },
               'gaia-ui-test-accessibility': {
                   'extra_args': [
                       '--cfg', 'marionette/gaia_ui_test_prod_config.py',
                       '--gip-suite', 'accessibility',
                   ],
               },
                'mochitest-media': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--test-path', 'dom/media/tests/',
                    ],
                },
           },
       },
    },
    'emulator-jb': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64_vm-b2g-emulator-jb': {
            'opt_unittest_suites': [],
            'debug_unittest_suites': [],
            'suite_config': {
                'marionette': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py",
                    ],
                },
                'marionette-webapi': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py",
                        "--test-manifest", "webapi-tests.ini",
                    ],
                },
                'mochitest-1': {
                    'extra_args': [
                        '--cfg', 'b2g/emulator_automation_config.py',
                        '--test-suite', 'mochitest',
                        '--this-chunk', '1', '--total-chunks', '1',
                        '--test-manifest', 'manifests/emulator-jb.ini',
                    ],
                },
            },
        },
    },
    'emulator-kk': {
        'product_name': 'b2g',
        'app_name': 'b2g',
        'brand_name': 'Gecko',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64_vm-b2g-emulator-kk': {
            'opt_unittest_suites': [],
            'debug_unittest_suites': [],
            'suite_config': {
                'marionette': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py",
                    ],
                },
                'marionette-webapi': {
                    'extra_args': [
                        "--cfg", "marionette/automation_emulator_config.py",
                        "--test-manifest", "webapi-tests.ini",
                    ],
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
BRANCHES['ash']['mozharness_repo'] = "https://hg.mozilla.org/build/ash-mozharness"
BRANCHES['ash']['mozharness_tag'] = "default"
BRANCHES['cedar']['branch_name'] = "Cedar"
BRANCHES['cedar']['repo_path'] = "projects/cedar"
BRANCHES['cedar']['mozharness_tag'] = "default"
BRANCHES['cedar']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['opt_unittest_suites'] = \
    MOCHITEST + CRASHTEST + XPCSHELL + MARIONETTE + MARIONETTE_UNIT + JSREFTEST + CPPUNIT
BRANCHES['cedar']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['debug_unittest_suites'] = \
    MOCHITEST_EMULATOR_DEBUG[:] + REFTEST + CRASHTEST + MARIONETTE + MARIONETTE_UNIT + XPCSHELL_CHUNKED + CPPUNIT
BRANCHES['cedar']['platforms']['emulator']['ubuntu64_vm-b2g-lg-emulator']['opt_unittest_suites'] = GAIA_UI + MOCHITEST_MEDIA
BRANCHES['cedar']['platforms']['emulator-jb']['ubuntu64_vm-b2g-emulator-jb']['opt_unittest_suites'] = MOCHITEST_EMULATOR_JB[:]
BRANCHES['cedar']['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites'] += \
  REFTEST_DESKTOP + GAIA_UI_OOP + GAIA_UNITTESTS_OOP + GAIA_JS_INTEGRATION[:]
BRANCHES['cedar']['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['debug_unittest_suites'] += GAIA_JS_INTEGRATION[:]
BRANCHES['cedar']['platforms']['macosx64_gecko']['mountainlion-b2gdt']['opt_unittest_suites'] += MOCHITEST_DESKTOP + REFTEST_DESKTOP_SANITY + GAIA_INTEGRATION + GAIA_JS_INTEGRATION[:]
BRANCHES['cedar']['platforms']['macosx64_gecko']['mountainlion-b2gdt']['opt_unittest_suites'] += GIP
BRANCHES['cedar']['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites'] += GIP
BRANCHES['cedar']['platforms']['linux64-mulet']['ubuntu64_vm-mulet']['opt_unittest_suites'] += GAIA_JS_INTEGRATION[:]
BRANCHES['pine']['branch_name'] = "Pine"
BRANCHES['pine']['repo_path'] = "projects/pine"
BRANCHES['pine']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['opt_unittest_suites'] = \
    MOCHITEST + CRASHTEST + XPCSHELL + MARIONETTE + JSREFTEST
BRANCHES['pine']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['debug_unittest_suites'] = \
    MOCHITEST_EMULATOR_DEBUG[:] + REFTEST + CRASHTEST + MARIONETTE + XPCSHELL_CHUNKED
BRANCHES['cypress']['branch_name'] = "Cypress"
BRANCHES['cypress']['repo_path'] = "projects/cypress"
BRANCHES['cypress']['mozharness_tag'] = "default"
BRANCHES['jamun']['repo_path'] = "projects/jamun"
BRANCHES['fx-team']['repo_path'] = "integration/fx-team"
BRANCHES['graphics']['repo_path'] = "projects/graphics"
BRANCHES['mozilla-b2g28_v1_3t']['repo_path'] = "releases/mozilla-b2g28_v1_3t"
BRANCHES['mozilla-b2g30_v1_4']['repo_path'] = "releases/mozilla-b2g30_v1_4"
BRANCHES['mozilla-b2g32_v2_0']['repo_path'] = "releases/mozilla-b2g32_v2_0"
BRANCHES['mozilla-b2g34_v2_1']['repo_path'] = "releases/mozilla-b2g34_v2_1"
BRANCHES['mozilla-aurora']['branch_name'] = "Mozilla-Aurora"
BRANCHES['mozilla-aurora']['repo_path'] = "releases/mozilla-aurora"
BRANCHES['mozilla-central']['branch_name'] = "Firefox"
BRANCHES['mozilla-inbound']['repo_path'] = "integration/mozilla-inbound"
BRANCHES['b2g-inbound']['branch_name'] = "B2g-Inbound"
BRANCHES['b2g-inbound']['repo_path'] = "integration/b2g-inbound"
BRANCHES['try']['pgo_strategy'] = "try"
BRANCHES['try']['enable_try'] = True
BRANCHES['gaia-try']['repo_path'] = "integration/gaia-try"

def exclude_suites(slave_platform, branch, suites_to_be_excluded, from_opt_unittests, from_debug_unittests):
    #slave_platform is a tuple, e.g.:
    #('linux64_gecko', 'ubuntu64_vm-b2gdt')
    if nested_haskey(BRANCHES[branch]['platforms'], slave_platform[0], slave_platform[1]):
        slave_p = BRANCHES[branch]['platforms'][slave_platform[0]][slave_platform[1]]
        if from_opt_unittests:
            slave_p['opt_unittest_suites'] = [x for x in slave_p['opt_unittest_suites']
                                              if x[0] if x[0] not in suites_to_be_excluded]
        if from_debug_unittests:
            slave_p['debug_unittest_suites'] = [x for x in slave_p['debug_unittest_suites']
                                            if x[0] if x[0] not in suites_to_be_excluded]

exclude_suites(('linux64_gecko', 'ubuntu64_vm-b2gdt'), 'cedar', ('gaia-ui-test',), True, True)
exclude_suites(('linux32_gecko', 'ubuntu32_vm-b2gdt'), 'cedar', ('gaia-ui-test',), True, True)
exclude_suites(('macosx64_gecko', 'mountainlion-b2gdt'), 'cedar', ('gaia-ui-test',), True, True)
exclude_suites(('emulator', 'ubuntu64_vm-b2g-lg-emulator'), 'cedar', ('gaia-ui-test',), True, True)

# Enable mulet reftests on Ash, Cedar and Try
BRANCHES['ash']['platforms']['linux64-mulet']['ubuntu64_vm-mulet']['opt_unittest_suites'] += REFTEST_MULET
BRANCHES['try']['platforms']['linux64-mulet']['ubuntu64_vm-mulet']['opt_unittest_suites'] += REFTEST_MULET
BRANCHES['cedar']['platforms']['linux64-mulet']['ubuntu64_vm-mulet']['opt_unittest_suites'] += REFTEST_MULET

# new linux64_gecko tests as of gecko 32; OOP replaces their non-OOP variants
for name, branch in items_at_least(BRANCHES, 'gecko_version', 32):
    BRANCHES[name]['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites'] += \
      GAIA_BUILD + REFTEST_DESKTOP_OOP_SANITY + MOCHITEST_OOP_DESKTOP
    for suite_to_remove in ('mochitest-1', 'reftest-sanity'):
        for s in BRANCHES[name]['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites']:
            if s[0] == suite_to_remove:
                BRANCHES[name]['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites'].remove(s)

# new linux64_gecko tests as of gecko 34
for name, branch in items_at_least(BRANCHES, 'gecko_version', 34):
    BRANCHES[name]['platforms']['linux64_gecko']['ubuntu64_vm-b2gdt']['opt_unittest_suites'] += \
      GAIA_BUILD_UNIT

# explicitly set slave platforms per branch
for branch in BRANCHES.keys():
    for platform in BRANCHES[branch]['platforms']:
        if 'slave_platforms' not in BRANCHES[branch]['platforms'][platform]:
            BRANCHES[branch]['platforms'][platform]['slave_platforms'] = list(PLATFORMS[platform]['slave_platforms'])

# Disable emulator debug unittests on older branches
for branch in BRANCHES.keys():
    if branch in ('mozilla-esr24', ):
        if 'emulator' in BRANCHES[branch]['platforms']:
            BRANCHES[branch]['platforms']['emulator']['enable_debug_unittests'] = False

# Disable gecko-debug unittests on older branches, Bug 91611
# All tests need to be enabled on cedar until they green up, Bug 1004610
OLD_BRANCHES = set([name for name, branch in items_before(BRANCHES, 'gecko_version', 30)])
for b in BRANCHES.keys():
    if b in OLD_BRANCHES:
        for platform in ['linux32_gecko', 'linux64_gecko']:
             if platform in BRANCHES[b]['platforms']:
                 BRANCHES[b]['platforms'][platform]['enable_debug_unittests'] = False


# Disable b2g desktop reftest-sanity on cedar
for slave_platform in (('linux64_gecko', 'ubuntu64_vm-b2gdt'),):
    if nested_haskey(BRANCHES['cedar']['platforms'], slave_platform[0], slave_platform[1]):
        slave_p = BRANCHES['cedar']['platforms'][slave_platform[0]][slave_platform[1]]
        slave_p['opt_unittest_suites'] = [x for x in slave_p['opt_unittest_suites']
                                          if x[0] if x[0] != 'reftest']


# Disable linter tests on branches older than gecko 31
OLD_BRANCHES = set([name for name, branch in items_before(BRANCHES, 'gecko_version', 31)])
excluded_tests = ['gaia-linter']
for b in BRANCHES.keys():
    branch = BRANCHES[b]
    if b in OLD_BRANCHES:
        for slave_platform in (('linux64_gecko', 'ubuntu64_vm-b2gdt'),
                               ('linux32_gecko', 'ubuntu32_vm-b2gdt'),
                               ('macosx64_gecko', 'mountainlion-b2gdt')):
            if nested_haskey(branch['platforms'], slave_platform[0], slave_platform[1]):
                slave_p = branch['platforms'][slave_platform[0]][slave_platform[1]]
                slave_p['opt_unittest_suites'] = [x for x in slave_p['opt_unittest_suites']
                                                  if x[0] not in excluded_tests]
                slave_p['debug_unittest_suites'] = [x for x in slave_p['debug_unittest_suites']
                                                    if x[0] not in excluded_tests]

# Disable b2g desktop reftest-sanity, gaia-integration and gaia-unit tests on older branches
OLD_BRANCHES = set([name for name, branch in items_before(BRANCHES, 'gecko_version', 29)])
excluded_tests = ['gaia-integration', 'reftest-sanity', 'gaia-unit']
for b in BRANCHES.keys():
    branch = BRANCHES[b]
    if b in OLD_BRANCHES:
        for slave_platform in (('linux64_gecko', 'ubuntu64_vm-b2gdt'),
                               ('linux32_gecko', 'ubuntu32_vm-b2gdt'),
                               ('macosx64_gecko', 'mountainlion-b2gdt')):
            if nested_haskey(branch['platforms'], slave_platform[0], slave_platform[1]):
                slave_p = branch['platforms'][slave_platform[0]][slave_platform[1]]
                slave_p['opt_unittest_suites'] = [x for x in slave_p['opt_unittest_suites']
                                                  if x[0] not in excluded_tests]
                slave_p['debug_unittest_suites'] = [x for x in slave_p['debug_unittest_suites']
                                                    if x[0] not in excluded_tests]

# Enable b2g reftests on EC2
for name, branch in items_at_least(BRANCHES, 'gecko_version', 26):
    if 'emulator' in branch['platforms']:
        branch['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['opt_unittest_suites'] += REFTEST_20[:]

# Once we EOL mozilla-b2g28_v1_3t we can remove this
for suite_to_remove in ('reftest-10', 'reftest-15'):
    for s in BRANCHES['mozilla-b2g28_v1_3t']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['opt_unittest_suites']:
        if s[0] == suite_to_remove:
            BRANCHES['mozilla-b2g28_v1_3t']['platforms']['emulator']['ubuntu64_vm-b2g-emulator']['opt_unittest_suites'].remove(s)

# Disable macosx64_gecko gaia-ui tests on older branches
for branch in BRANCHES.keys():
    if branch in ('mozilla-b2g28_v1_3t',):
        for platform in ('macosx64_gecko',):
            if platform in BRANCHES[branch]['platforms']:
                for slave_platform in ('mountainlion-b2gdt',):
                    if slave_platform in BRANCHES[branch]['platforms'][platform]:
                        del BRANCHES[branch]['platforms'][platform][slave_platform]

# Disable debug emulator mochitests on older branches
OLD_BRANCHES = set([name for name, branch in items_before(BRANCHES, 'gecko_version', 29)])
for b in BRANCHES.keys():
    branch = BRANCHES[b]
    if b in OLD_BRANCHES:
        if nested_haskey(branch['platforms'], 'emulator', 'ubuntu64_vm-b2g-emulator'):
            slave_p = branch['platforms']['emulator']['ubuntu64_vm-b2g-emulator']
            slave_p['debug_unittest_suites'] = [x for x in slave_p['debug_unittest_suites']
                                                if not x[0].startswith('mochitest-debug')]

# Disable ubuntu64_vm-b2gdt/ubuntu32_vm-b2gdt (ie gaia-ui-test) on older branches
for branch in BRANCHES.keys():
    if branch in ('mozilla-esr24', ):
        for platform in ('linux64_gecko', 'linux32_gecko'):
            if platform in BRANCHES[branch]['platforms']:
                for slave_platform in ('ubuntu64_vm-b2gdt', 'ubuntu32_vm-b2gdt'):
                    if slave_platform in BRANCHES[branch]['platforms'][platform]:
                        del BRANCHES[branch]['platforms'][platform][slave_platform]

# Disable emulator cppunit tests on older branches
OLD_BRANCHES = set([name for name, branch in items_before(BRANCHES, 'gecko_version', 34)])
for b in BRANCHES.keys():
    branch = BRANCHES[b]
    if b in OLD_BRANCHES:
        if nested_haskey(branch['platforms'], 'emulator', 'ubuntu64_vm-b2g-emulator'):
            slave_p = branch['platforms']['emulator']['ubuntu64_vm-b2g-emulator']
            for suites in ['opt_unittest_suites', 'debug_unittest_suites']:
                slave_p[suites] = [x for x in slave_p[suites]
                                   if not x[0].startswith('cppunit')]

# Disable OSX Mulet in every branch except cedar
for name in BRANCHES.keys():
    if name in ('cedar', ):
        continue
    for platform in ('macosx64-mulet', ):
        if platform in BRANCHES[name]['platforms']:
            del BRANCHES[name]['platforms'][platform]

# Enable linux64-mulet only in gecko 34+
for name, branch in items_before(BRANCHES, 'gecko_version', 34):
    if 'linux64-mulet' in branch['platforms']:
        del branch['platforms']['linux64-mulet']

### PROJECTS ###
PROJECTS = {
    'gaia-try': {
        'hgurl': 'https://hg.mozilla.org',
        'repo_path': 'integration/gaia-try',
    },
}
PROJECTS['gaia-try']['platforms'] = deepcopy(BRANCHES['mozilla-central']['platforms'])
for k, v in localconfig.B2G_PROJECTS.items():
    if k not in PROJECTS:
        PROJECTS[k] = {}
    for k1, v1 in v.items():
        PROJECTS[k][k1] = v1
mc_gecko_version = BRANCHES['mozilla-central']['gecko_version']
for pf, pf_config in BRANCHES['gaia-try']['platforms'].items():
    for sp in pf_config['slave_platforms']:
        for suite, suite_config in pf_config[sp]['suite_config'].items():
            suite_config['extra_args'].extend([
                '-c', 'b2g/gaia_try.py',
            ])
            if 'linux32' in pf:
                suite_config['opt_extra_args'] = [
                    '-c',
                    WithProperties('http://hg.mozilla.org/integration/gaia-try/raw-file/%(revision)s/linux32.json'),
                ]
            elif 'linux64' in pf:
                suite_config['opt_extra_args'] = [
                    '-c',
                    WithProperties('http://hg.mozilla.org/integration/gaia-try/raw-file/%(revision)s/linux64.json'),
                ]
                suite_config['debug_extra_args'] = [
                    '-c',
                    WithProperties('http://hg.mozilla.org/integration/gaia-try/raw-file/%(revision)s/linux64-debug.json'),
                ]
            elif 'macosx64' in pf:
                suite_config['opt_extra_args'] = [
                    '-c',
                    WithProperties('http://hg.mozilla.org/integration/gaia-try/raw-file/%(revision)s/macosx64.json'),
                ]


if __name__ == "__main__":
    import sys
    import pprint

    args = sys.argv[1:]

    if len(args) > 0:
        items = dict([(b, BRANCHES[b]) for b in args])
    else:
        items = dict(BRANCHES.items())

    for k, v in sorted(items.iteritems()):
        out = pprint.pformat(v)
        for l in out.splitlines():
            print '%s: %s' % (k, l)

    for suite in sorted(SUITES):
        out = pprint.pformat(SUITES[suite])
        for l in out.splitlines():
            print '%s: %s' % (suite, l)
