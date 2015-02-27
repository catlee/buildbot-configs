from copy import deepcopy

import config_common
reload(config_common)
from config_common import loadDefaultValues, loadCustomTalosSuites, \
    get_talos_slave_platforms, delete_slave_platform

import master_common
reload(master_common)
from master_common import setMainFirefoxVersions, items_before, items_at_least

import project_branches
reload(project_branches)
from project_branches import PROJECT_BRANCHES, ACTIVE_PROJECT_BRANCHES

import localconfig
reload(localconfig)
from localconfig import SLAVES, TRY_SLAVES, GLOBAL_VARS, GRAPH_CONFIG

MOZHARNESS_REBOOT_CMD = ['scripts/external_tools/count_and_reboot.py',
                         '-f', '../reboot_count.txt',
                         '-n', '1', '-z']

TALOS_DIRTY_OPTS = {'talosAddOns': ['profiles/dirtyDBs.zip', 'profiles/dirtyMaxDBs.zip']}

TALOS_TP_NEW_OPTS = {'plugins': {'32': 'zips/flash32_10_3_183_5.zip', '64': 'zips/flash64_11_0_d1_98.zip'}, 'pagesets': ['zips/tp5n.zip']}

BRANCHES = {
    'mozilla-central':     {},
    'mozilla-aurora':      {},
    'mozilla-release':     {},
    'mozilla-beta':        {},
    'mozilla-esr31': {
        'gecko_version': 31,
        'platforms': {
            'macosx64': {},
            'win32': {},
            'linux': {},
            'linux64': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g30_v1_4': {
        'datazilla_url': None,
        'gecko_version': 30,
        'platforms': {
            # desktop per sicking in Bug 829513
            'macosx64': {},
            'win32': {},
            'linux': {},
            'linux64': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g32_v2_0': {
        'datazilla_url': None,
        'gecko_version': 32,
        'platforms': {
            # desktop per sicking in Bug 829513
            'macosx64': {},
            'win32': {},
            'linux': {},
            'linux64': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g34_v2_1': {
        'datazilla_url': None,
        'gecko_version': 34,
        'platforms': {
            # desktop per sicking in Bug 829513
            'macosx64': {},
            'win32': {},
            'linux': {},
            'linux64': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g34_v2_1s': {
        'datazilla_url': None,
        'gecko_version': 34,
        'platforms': {
            # desktop per sicking in Bug 829513
            'linux': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g37_v2_2': {
        'datazilla_url': None,
        'gecko_version': 37,
        'platforms': {
            # desktop per sicking in Bug 829513
            'macosx64': {},
            'win32': {},
            'linux': {},
            'linux64': {},
        },
        'lock_platforms': True,
    },
    'try': {
        'coallesce_jobs': False,
    },
}

setMainFirefoxVersions(BRANCHES)

# Talos
PLATFORMS = {
    'macosx64': {},
    'win32': {},
    'linux': {},
    'linux64': {},
    'linux64-asan': {},
    'linux64-cc': {},
    'win64': {},
}

PLATFORMS['macosx64']['slave_platforms'] = ['snowleopard', 'mountainlion', 'yosemite']
PLATFORMS['macosx64']['env_name'] = 'mac-perf'
PLATFORMS['macosx64']['snowleopard'] = {'name': "Rev4 MacOSX Snow Leopard 10.6"}
PLATFORMS['macosx64']['mountainlion'] = {'name': "Rev5 MacOSX Mountain Lion 10.8",
                                         'try_by_default': False}
PLATFORMS['macosx64']['yosemite'] = {'name': "Rev5 MacOSX Yosemite 10.10", 
                                     'try_by_default': False}
PLATFORMS['macosx64']['stage_product'] = 'firefox'
PLATFORMS['macosx64']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '64',
    'config_file': 'talos/mac_config.py',
}

PLATFORMS['win32']['slave_platforms'] = ['xp-ix', 'win7-ix', 'win8']
PLATFORMS['win32']['talos_slave_platforms'] = ['xp-ix', 'win7-ix', 'win8']
PLATFORMS['win32']['env_name'] = 'win32-perf'
PLATFORMS['win32']['xp-ix'] = {'name': "Windows XP 32-bit"}
PLATFORMS['win32']['win7-ix'] = {'name': "Windows 7 32-bit"}
PLATFORMS['win32']['win8'] = {'name': "WINNT 6.2"}
PLATFORMS['win32']['stage_product'] = 'firefox'
PLATFORMS['win32']['mozharness_config'] = {
    'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
    'hg_bin': 'c:\\mozilla-build\\hg\\hg',
    'reboot_command': ['c:/mozilla-build/python27/python', '-u'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '32',
    'config_file': 'talos/windows_config.py',
}

PLATFORMS['win64']['slave_platforms'] = ['win8_64']
PLATFORMS['win64']['talos_slave_platforms'] = ['win8_64']
PLATFORMS['win64']['env_name'] = 'win64-perf'
PLATFORMS['win64']['stage_product'] = 'firefox'
PLATFORMS['win64']['win8_64'] = {'name': 'Windows 8 64-bit'}
PLATFORMS['win64']['mozharness_config'] = {
    'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
    'hg_bin': 'c:\\mozilla-build\\hg\\hg',
    'reboot_command': ['c:/mozilla-build/python27/python', '-u'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '64',
    'config_file': 'talos/windows_config.py',
}

PLATFORMS['linux']['slave_platforms'] = ['ubuntu32_vm']
PLATFORMS['linux']['talos_slave_platforms'] = ['ubuntu32_hw']
PLATFORMS['linux']['env_name'] = 'linux-perf'
PLATFORMS['linux']['ubuntu32_vm'] = {'name': 'Ubuntu VM 12.04'}
PLATFORMS['linux']['ubuntu32_hw'] = {'name': 'Ubuntu HW 12.04'}
PLATFORMS['linux']['stage_product'] = 'firefox'
PLATFORMS['linux']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '32',
    'config_file': 'talos/linux_config.py',
}

PLATFORMS['linux64']['slave_platforms'] = ['ubuntu64_vm']
PLATFORMS['linux64']['talos_slave_platforms'] = ['ubuntu64_hw']
PLATFORMS['linux64']['env_name'] = 'linux-perf'
PLATFORMS['linux64']['ubuntu64_vm'] = {'name': 'Ubuntu VM 12.04 x64'}
PLATFORMS['linux64']['ubuntu64_hw'] = {'name': 'Ubuntu HW 12.04 x64'}
PLATFORMS['linux64']['stage_product'] = 'firefox'
PLATFORMS['linux64']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '64',
    'config_file': 'talos/linux_config.py',
}

PLATFORMS['linux64-asan']['slave_platforms'] = ['ubuntu64-asan_vm']
PLATFORMS['linux64-asan']['ubuntu64-asan_vm'] = {'name': 'Ubuntu ASAN VM 12.04 x64'}
PLATFORMS['linux64-asan']['stage_product'] = 'firefox'
PLATFORMS['linux64-asan']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '64',
    'config_file': 'talos/linux_config.py',
}

PLATFORMS['linux64-cc']['slave_platforms'] = ['ubuntu64_vm']
PLATFORMS['linux64-cc']['ubuntu64_vm'] = {
    'name': 'Ubuntu Code Coverage VM 12.04 x64',
    'build_dir_prefix': 'ubuntu64_vm_cc',
    'scheduler_slave_platform_identifier': 'ubuntu64_vm_cc'
}
PLATFORMS['linux64-cc']['stage_product'] = 'firefox'
PLATFORMS['linux64-cc']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'system_bits': '64',
}

# Lets be explicit instead of magical.
for platform, platform_config in PLATFORMS.items():
    all_slave_platforms = set(platform_config['slave_platforms'] +
                              platform_config.get('talos_slave_platforms', []))
    for slave_platform in all_slave_platforms:
        platform_config[slave_platform]['slaves'] = sorted(SLAVES[slave_platform])
        if slave_platform in TRY_SLAVES:
            platform_config[slave_platform]['try_slaves'] = sorted(TRY_SLAVES[slave_platform])
        else:
            platform_config[slave_platform]['try_slaves'] = platform_config[slave_platform]['slaves']

ALL_TALOS_PLATFORMS = get_talos_slave_platforms(PLATFORMS, platforms=('linux', 'linux64', 'win32', 'macosx64', 'win64'))
NO_WINXP = [platform for platform in ALL_TALOS_PLATFORMS if platform != 'xp-ix']
WIN7_ONLY = ['win7-ix']
WIN8_ONLY = ['win8_64']
LINUX64_ONLY = get_talos_slave_platforms(PLATFORMS, platforms=('linux64',))
NO_LINUX64 = get_talos_slave_platforms(PLATFORMS, platforms=('linux', 'win32', 'macosx64', 'win64'))

OSX_SNOW_ONLY = [platform for platform in ALL_TALOS_PLATFORMS if platform == 'snowleopard']
ALL_NO_SNOW = [platform for platform in ALL_TALOS_PLATFORMS if platform != 'snowleopard']
NO_SNOW_LINUX64 = [platform for platform in NO_LINUX64 if platform != 'snowleopard']
NO_SNOW_WINXP = [platform for platform in NO_WINXP if platform != 'snowleopard']

def win864_to_win8(platforms):
    retval = []
    for p in platforms:
        if p == 'win8_64':
            retval.append('win8')
        else:
            retval.append(p)
    return retval

SUITES = {
    'xperf': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5n', '--sampleConfig', 'xperf.config', '--mozAfterPaint', '--xperf_path',
                                  '"c:/Program Files/Microsoft Windows Performance Toolkit/xperf.exe"', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, WIN7_ONLY),
    },
    'xperf-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5n', '--sampleConfig', 'xperf.config', '--mozAfterPaint', '--xperf_path',
                                  '"c:/Program Files/Microsoft Windows Performance Toolkit/xperf.exe"', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, WIN7_ONLY),
    },
    'tp5o': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5o', '--mozAfterPaint', '--responsiveness', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, ALL_NO_SNOW),
    },
    'tp5o-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5o', '--mozAfterPaint', '--responsiveness', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, NO_SNOW_WINXP),
    },
    'g1': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5o_scroll', '--filter', 'ignore_first:1', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, ALL_NO_SNOW),
    },
    'g1-snow': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'glterrain', '--filter', 'ignore_first:1', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'g1-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp5o_scroll', '--filter', 'ignore_first:1', '--filter', 'median'],
        'options': (TALOS_TP_NEW_OPTS, NO_SNOW_WINXP),
    },
    'g1-snow-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'glterrain', '--filter', 'ignore_first:1', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'other': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:a11yr:ts_paint:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, ALL_NO_SNOW),
    },
    'other-snow': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'other_nol64': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:a11yr:ts_paint:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, NO_SNOW_LINUX64),
    },
    'other-e10s_nol64': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:a11yr:ts_paint:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, NO_SNOW_LINUX64),
    },
    'other_l64': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:a11yr:ts_paint:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, LINUX64_ONLY),
    },
    'other-snow-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr::tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'other-e10s_l64': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tscrollr:a11yr:ts_paint:tpaint', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, LINUX64_ONLY),
    },
    'svgr': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgr:tsvgr_opacity', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, ALL_NO_SNOW),
    },
    'svgr-snow': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgr', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'svgr-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgr:tsvgr_opacity', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, NO_SNOW_WINXP),
    },
    'svgr-snow-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgr', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'dromaeojs': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'dromaeo_css:dromaeo_dom:kraken:v8_7'],
        'options': ({}, NO_SNOW_WINXP),
    },
    'dromaeojs-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'dromaeo_css:dromaeo_dom:kraken:v8_7'],
        'options': ({}, NO_SNOW_WINXP),
    },
    'chromez': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tresize', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, ALL_NO_SNOW),
    },
    'chromez-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tresize', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, NO_SNOW_WINXP),
    },
    'chromez-snow': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tresize', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
    'chromez-snow-e10s': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tresize', '--mozAfterPaint', '--filter', 'ignore_first:5', '--filter', 'median'],
        'options': ({}, OSX_SNOW_ONLY),
    },
}

BRANCH_UNITTEST_VARS = {
    'hghost': 'hg.mozilla.org',
    # turn on platforms as we get them running
    'platforms': {
        'linux': {},
        'linux64': {},
        'linux64-asan': {},
        'linux64-cc': {},
        'macosx64': {},
        'win32': {},
        'win64': {},
    },
}

MOCHITEST_WO_BC = [
    ('mochitest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'plain-chunked'],
        'blob_upload': True,
        'script_maxtime': 7200,
        'totalChunks': 5,
    }),
]

MOCHITEST_BC = [
    ('mochitest-browser-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'browser-chrome'],
        'blob_upload': True,
        'script_maxtime': 12000,
    }),
]

MOCHITEST_JP = [
    ('mochitest-jetpack', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'jetpack-package', '--mochitest-suite', 'jetpack-addon'],
        'blob_upload': True,
        'script_maxtime': 12000,
    }),
]

MOCHITEST_OTHER = [
    ('mochitest-other', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'chrome,a11y,plugins'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

MOCHITEST_E10S = [
    ('mochitest-e10s', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'plain-chunked', '--e10s'],
        'blob_upload': True,
        'script_maxtime': 7200,
        'totalChunks': 5,
    }),
]

# Plain mochitests with a more strict content sandbox enabled.
MOCHITEST_CSB = [
    ('mochitest-csb', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'plain-chunked', '--strict-content-sandbox'],
        'blob_upload': True,
        'script_maxtime': 7200,
        'totalChunks': 5,
    }),
]

MOCHITEST_DT = [
    ('mochitest-devtools-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'mochitest-devtools-chrome'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

MOCHITEST_DT_E10S = [
    ('mochitest-e10s-devtools-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'mochitest-devtools-chrome', '--e10s'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

MOCHITEST_DT_3 = [
    ('mochitest-devtools-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'mochitest-devtools-chrome-chunked'],
        'blob_upload': True,
        'script_maxtime': 4800,
        'totalChunks': 3,
    }),
]

MOCHITEST_BC_3 = [
    ('mochitest-browser-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'browser-chrome-chunked'],
        'blob_upload': True,
        'script_maxtime': 12000,
        'totalChunks': 3,
    }),
]

MOCHITEST_BC_3_E10S = [
    ('mochitest-e10s-browser-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'browser-chrome-chunked', '--e10s'],
        'blob_upload': True,
        'script_maxtime': 12000,
        'totalChunks': 3,
    }),
]

MOCHITEST_WEBGL = [
    ('mochitest-gl', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mochitest-suite', 'mochitest-gl'],
        'blob_upload': True,
        'script_maxtime': 12000,
    }),
]

MOCHITEST_PLAIN = MOCHITEST_WO_BC[:]
MOCHITEST = MOCHITEST_WO_BC[:] + MOCHITEST_BC_3 + MOCHITEST_OTHER
MOCHITEST_WO_BC += MOCHITEST_OTHER

WEBAPPRT_CHROME = [
    ('webapprt-chrome', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--webapprt-suite', 'chrome'],
        'blob_upload': True,
        'script_maxtime': 4800,
    })
]

REFTEST_ONE_CHUNK = [
    ('reftest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

REFTEST_TWO_CHUNKS = [
    ('reftest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest'],
        'blob_upload': True,
        'script_maxtime': 7200,
        'totalChunks': 2,
    }),
]

REFTEST_NO_IPC = [
    ('jsreftest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'jsreftest'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
    ('crashtest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'crashtest'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

REFTEST_NOACCEL = [
    ('reftest-no-accel', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest-no-accel'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]
REFTEST_OMTC = [
    ('reftest-omtc', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest-omtc'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]
REFTEST_IPC = [
    ('reftest-ipc', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest-ipc'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
    ('crashtest-ipc', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'crashtest-ipc'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]
REFTEST_E10S = [
    ('reftest-e10s', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'reftest', '--e10s'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
    ('crashtest-e10s', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--reftest-suite', 'crashtest', '--e10s'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

XPCSHELL = [
    ('xpcshell', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--xpcshell-suite', 'xpcshell'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

CPPUNIT = [
    ('cppunit', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--cppunittest-suite', 'cppunittest'],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]
MARIONETTE = [
    ('marionette', {
        'use_mozharness': True,
        'script_path': 'scripts/marionette.py',
        'download_symbols': False,
        'blob_upload': True,
    }),
]
MARIONETTE_E10S = [
    ('marionette-e10s', {
        'use_mozharness': True,
        'script_path': 'scripts/marionette.py',
        'extra_args': ['--e10s'],
        'download_symbols': False,
        'blob_upload': True,
    }),
]
JITTEST = [
    ('jittest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--jittest-suite', 'jittest'],
        'script_maxtime': 7200,
    }),
]
JITTEST_CHUNKED = [
    ('jittest', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--jittest-suite', 'jittest-chunked'],
        'blob_upload': True,
        'script_maxtime': 7200,
        'totalChunks': 2,
    }),
]
MOZBASE = [
    ('mozbase', {
        'use_mozharness': True,
        'script_path': 'scripts/desktop_unittest.py',
        'extra_args': ['--mozbase-suite', 'mozbase'],
        'script_maxtime': 7200,
    }),
]

WEB_PLATFORM_REFTESTS = [
    ('web-platform-tests-reftests', {
        'use_mozharness': True,
        'script_path': 'scripts/web_platform_tests.py',
        'extra_args': ["--test-type=reftest"],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

WEB_PLATFORM_TESTS = [
    ('web-platform-tests', {
        'use_mozharness': True,
        'script_path': 'scripts/web_platform_tests.py',
        'extra_args': ["--test-type=testharness"],
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]

WEB_PLATFORM_TESTS_CHUNKED = [
    ('web-platform-tests', {
        'use_mozharness': True,
        'script_path': 'scripts/web_platform_tests.py',
        'extra_args': ["--test-type=testharness"],
        'totalChunks': 4,
        'blob_upload': True,
        'script_maxtime': 7200,
    }),
]


UNITTEST_SUITES = {
    'opt_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + CPPUNIT + MOCHITEST_DT,
    'debug_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + CPPUNIT + MARIONETTE + MOCHITEST_DT_3,
}


# You must define opt_unittest_suites when enable_opt_unittests is True for a
# platform. Likewise debug_unittest_suites for enable_debug_unittests
PLATFORM_UNITTEST_VARS = {
    'linux': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'ubuntu32_vm': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:] + REFTEST_NOACCEL,
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-ipc': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest-ipc': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'marionette-e10s': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
            },
        },
    },
    'linux64': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'ubuntu64_vm': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
            },
        },
    },
    'linux64-asan': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64-asan_vm': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
            },
        },
    },
    'linux64-cc': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'unittest-env': {'DISPLAY': ':0'},
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'ubuntu64_vm': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/linux_unittest.py"],
                },
            },
        },
    },
    'win32': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'mochitest_leak_threshold': 484,
        'crashtest_leak_threshold': 484,
        'env_name': 'win32-perf-unittest',
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'xp-ix': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + MOCHITEST_DT_3,
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-csb': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-omtc': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/windows_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
            },
        },
        'win7-ix': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:] + REFTEST_NOACCEL,
            'debug_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + MOCHITEST_DT_3,
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-csb': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-omtc': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/windows_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
            },
        },
        'win8': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:] + REFTEST_NOACCEL[:],
            'debug_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + CPPUNIT + MOCHITEST_DT_3,
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-csb': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-omtc': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/windows_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
            },
        }
    },
    'win64': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'mochitest_leak_threshold': 484,
        'crashtest_leak_threshold': 484,
        'env_name': 'win64-perf-unittest',
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'win8_64': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:] + REFTEST_NOACCEL[:],
            'debug_unittest_suites': MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + XPCSHELL + CPPUNIT + MOCHITEST_DT_3,
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-csb': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/windows_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/win_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config_windows.py"],
                },
            },
        },
    },
    'macosx64': {
        'product_name': 'firefox',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'builds_before_reboot': 1,
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'snowleopard': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
            },
        },
        'mountainlion': {
            'opt_unittest_suites': UNITTEST_SUITES['opt_unittest_suites'][:],
            'debug_unittest_suites': UNITTEST_SUITES['debug_unittest_suites'][:],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
            },
        },
        'yosemite': {
            'opt_unittest_suites': [],
            'debug_unittest_suites': [],
            'suite_config': {
                'mochitest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-browser-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-other': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-e10s-devtools-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-gl': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'mochitest-jetpack': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'webapprt-chrome': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'jsreftest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'crashtest-e10s': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'reftest-no-accel': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'xpcshell': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'cppunit': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'marionette': {
                    'config_files': ["marionette/prod_config.py"],
                },
                'jittest': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
                'web-platform-tests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'web-platform-tests-reftests': {
                    'config_files': ["web_platform_tests/prod_config.py"],
                },
                'mozbase': {
                    'config_files': ["unittests/mac_unittest.py"],
                },
            },
        },
    },
}

# Copy project branches into BRANCHES keys
for branch in ACTIVE_PROJECT_BRANCHES:
    BRANCHES[branch] = deepcopy(PROJECT_BRANCHES[branch])

# Copy unittest vars in first, then platform vars
for branch in BRANCHES.keys():
    for key, value in GLOBAL_VARS.items():
        # In order to have things ride the trains we need to be able to
        # override "global" things. Therefore, we shouldn't override anything
        # that's already been set.
        if key in BRANCHES[branch]:
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
    if branch in localconfig.BRANCHES:
        for key, value in localconfig.BRANCHES[branch].items():
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

    # Merge in any project branch config for platforms
    if branch in ACTIVE_PROJECT_BRANCHES and 'platforms' in PROJECT_BRANCHES[branch]:
        for platform, platform_config in PROJECT_BRANCHES[branch]['platforms'].items():
            if platform in PLATFORMS:
                for key, value in platform_config.items():
                    value = deepcopy(value)
                    if isinstance(value, str):
                        value = value % locals()
                    BRANCHES[branch]['platforms'][platform][key] = value

    for platform, platform_config in localconfig.PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

### PROJECTS ###
PROJECTS = {
    'jetpack': {
        'branches': ['fx-team'],
        'platforms': {
            'ubuntu64_vm': {
                'ext': 'linux-x86_64.tar.bz2',
                'env': 'linux-perf',
                'debug': True
            },
            'ubuntu64-asan_vm': {
                'ext': 'linux-x86_64-asan.tar.bz2',
                'env': 'linux-perf',
                'debug': False
            },
            'ubuntu32_vm': {
                'ext': 'linux-i686.tar.bz2',
                'env': 'linux-perf',
                'debug': True
            },
            'snowleopard': {'ext': '(mac|mac64).dmg', 'debug': True},
            'mountainlion': {'ext': '(mac|mac64).dmg', 'debug': True},
            'xp-ix': {
                'ext': 'win32.zip',
                'env': PLATFORM_UNITTEST_VARS['win32']['env_name'],
                'debug': True,
            },
            'win7-ix': {
                'ext': 'win32.zip',
                'env': PLATFORM_UNITTEST_VARS['win32']['env_name'],
                'debug': True,
            },
            'win8': {
                'ext': 'win32.zip',
                'env': PLATFORM_UNITTEST_VARS['win32']['env_name'],
                'debug': True,
            },
        },
        'hgurl': 'https://hg.mozilla.org',
        'repo_path': 'projects/addon-sdk',
        'ftp_url': 'ftp://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/%(branch)s-%(platform)s',
    },
}
for k, v in localconfig.PROJECTS.items():
    if k not in PROJECTS:
        PROJECTS[k] = {}
    for k1, v1 in v.items():
        PROJECTS[k][k1] = v1

########
# Entries in BRANCHES for tests should be a tuple of:
# - Number of tests to run per build
# - Whether queue merging is on
# - TalosFactory options
# - Which platforms to run on

# Let's load the defaults
for branch in BRANCHES.keys():
    loadDefaultValues(BRANCHES, branch, BRANCHES[branch])
    loadCustomTalosSuites(BRANCHES, SUITES, branch, BRANCHES[branch])

# The following are exceptions to the defaults

######## mozilla-central
BRANCHES['mozilla-central']['branch_name'] = "Firefox"
BRANCHES['mozilla-central']['repo_path'] = "mozilla-central"
BRANCHES['mozilla-central']['build_branch'] = "1.9.2"
BRANCHES['mozilla-central']['pgo_strategy'] = 'periodic'
BRANCHES['mozilla-central']['xperf-e10s_tests'] = (1, False, TALOS_TP_NEW_OPTS, WIN7_ONLY)
BRANCHES['mozilla-central']['tp5o-e10s_tests'] = (1, False, TALOS_TP_NEW_OPTS, NO_SNOW_WINXP)
BRANCHES['mozilla-central']['g1-e10s_tests'] = (1, False, TALOS_TP_NEW_OPTS, NO_SNOW_WINXP)
BRANCHES['mozilla-central']['g1-snow-e10s_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['mozilla-central']['other-e10s_nol64_tests'] = (1, False, {}, NO_SNOW_LINUX64)
BRANCHES['mozilla-central']['other-e10s_l64_tests'] = (1, False, {}, LINUX64_ONLY)
BRANCHES['mozilla-central']['other-snow-e10s_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['mozilla-central']['svgr-e10s_tests'] = (1, False, {}, NO_SNOW_WINXP)
BRANCHES['mozilla-central']['svgr-snow-e10s_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['mozilla-central']['dromaeojs-e10s_tests'] = (1, False, {}, NO_SNOW_WINXP)
BRANCHES['mozilla-central']['chromez-e10s_tests'] = (1, False, {}, NO_SNOW_WINXP)
BRANCHES['mozilla-central']['chromez-snow-e10s_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['mozilla-central']['pgo_only_suites'] = ['g1-e10s', 'xperf-e10s',
                                                  'tp5o-e10s',
                                                  'other-e10s_nol64',
                                                  'other-e10s_l64',
                                                  'svgr-e10s',
                                                  'dromaeojs-e10s',
                                                  'chromez-e10s']


######### mozilla-release
BRANCHES['mozilla-release']['repo_path'] = "releases/mozilla-release"
BRANCHES['mozilla-release']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-release']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-release']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-release']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-release']['platforms']['linux64']['talos_slave_platforms'] = []

######### mozilla-beta
BRANCHES['mozilla-beta']['repo_path'] = "releases/mozilla-beta"
BRANCHES['mozilla-beta']['pgo_strategy'] = 'per-checkin'

######### mozilla-aurora
BRANCHES['mozilla-aurora']['repo_path'] = "releases/mozilla-aurora"
BRANCHES['mozilla-aurora']['pgo_strategy'] = 'per-checkin'

######### mozilla-esr31
BRANCHES['mozilla-esr31']['repo_path'] = "releases/mozilla-esr31"
BRANCHES['mozilla-esr31']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-esr31']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-esr31']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-esr31']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-esr31']['platforms']['linux64']['talos_slave_platforms'] = []

######### mozilla-b2g30_v1_4
BRANCHES['mozilla-b2g30_v1_4']['repo_path'] = "releases/mozilla-b2g30_v1_4"
BRANCHES['mozilla-b2g30_v1_4']['pgo_strategy'] = None
BRANCHES['mozilla-b2g30_v1_4']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g30_v1_4']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g30_v1_4']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g30_v1_4']['platforms']['linux64']['talos_slave_platforms'] = []

######### mozilla-b2g32_v2_0
BRANCHES['mozilla-b2g32_v2_0']['repo_path'] = "releases/mozilla-b2g32_v2_0"
BRANCHES['mozilla-b2g32_v2_0']['pgo_strategy'] = None
BRANCHES['mozilla-b2g32_v2_0']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g32_v2_0']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g32_v2_0']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g32_v2_0']['platforms']['linux64']['talos_slave_platforms'] = []

######### mozilla-b2g34_v2_1
BRANCHES['mozilla-b2g34_v2_1']['repo_path'] = "releases/mozilla-b2g34_v2_1"
BRANCHES['mozilla-b2g34_v2_1']['pgo_strategy'] = None
BRANCHES['mozilla-b2g34_v2_1']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g34_v2_1']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g34_v2_1']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g34_v2_1']['platforms']['linux64']['talos_slave_platforms'] = []

######### mozilla-b2g34_v2_1s
BRANCHES['mozilla-b2g34_v2_1s']['repo_path'] = "releases/mozilla-b2g34_v2_1s"
BRANCHES['mozilla-b2g34_v2_1s']['pgo_strategy'] = None

######### mozilla-b2g37_v2_2
BRANCHES['mozilla-b2g37_v2_2']['repo_path'] = "releases/mozilla-b2g37_v2_2"
BRANCHES['mozilla-b2g37_v2_2']['pgo_strategy'] = None
BRANCHES['mozilla-b2g37_v2_2']['platforms']['win32']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g37_v2_2']['platforms']['macosx64']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g37_v2_2']['platforms']['linux']['talos_slave_platforms'] = []
BRANCHES['mozilla-b2g37_v2_2']['platforms']['linux64']['talos_slave_platforms'] = []


######## try
BRANCHES['try']['repo_path'] = "try"
BRANCHES['try']['xperf_tests'] = (1, False, TALOS_TP_NEW_OPTS, WIN7_ONLY)
BRANCHES['try']['tp5o_tests'] = (1, False, TALOS_TP_NEW_OPTS, ALL_NO_SNOW)
BRANCHES['try']['other_tests'] = (0, False, {}, ALL_NO_SNOW)
BRANCHES['try']['other-snow_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['try']['other_nol64_tests'] = (1, False, {}, NO_SNOW_LINUX64)
BRANCHES['try']['other_l64_tests'] = (1, False, {}, LINUX64_ONLY)
BRANCHES['try']['g1-snow_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['try']['g1_tests'] = (1, False, TALOS_TP_NEW_OPTS, ALL_NO_SNOW)
BRANCHES['try']['chromez-snow_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['try']['svgr-snow_tests'] = (1, False, {}, OSX_SNOW_ONLY)
BRANCHES['try']['pgo_strategy'] = 'try'
BRANCHES['try']['enable_try'] = True
BRANCHES['try']['platforms']['macosx64']['yosemite']['opt_unittest_suites'] = UNITTEST_SUITES['opt_unittest_suites'][:]
BRANCHES['try']['platforms']['macosx64']['yosemite']['debug_unittest_suites'] = UNITTEST_SUITES['debug_unittest_suites'][:]

######## cedar
BRANCHES['cedar']['platforms']['linux64-asan']['ubuntu64-asan_vm']['opt_unittest_suites'] += MARIONETTE[:]
BRANCHES['cedar']['platforms']['win32']['xp-ix']['opt_unittest_suites'] += REFTEST_OMTC[:]
BRANCHES['cedar']['platforms']['win32']['win7-ix']['opt_unittest_suites'] += REFTEST_OMTC[:]
BRANCHES['cedar']['platforms']['win64']['win8_64']['opt_unittest_suites'] += REFTEST_OMTC[:]
BRANCHES['cedar']['platforms']['win32']['xp-ix']['debug_unittest_suites'] += REFTEST_OMTC[:]
BRANCHES['cedar']['platforms']['win32']['win7-ix']['debug_unittest_suites'] += REFTEST_OMTC[:]
BRANCHES['cedar']['platforms']['win64']['win8_64']['debug_unittest_suites'] += REFTEST_OMTC[:]

######## mozilla-inbound
# Skip test runs (see bug 1056787)
# Note that if we set this higher than 3, we'll start to get strange behaviour
# due to the currently global coalescing limit of 3 defined at
# http://hg.mozilla.org/build/buildbotcustom/file/e3713abcd36d/misc.py#l647
BRANCHES['mozilla-inbound']['platforms']['win32']['xp-ix']['opt_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['win32']['xp-ix']['opt_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['win32']['win7-ix']['opt_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['win32']['win7-ix']['opt_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['win64']['win8_64']['opt_unittest_skipcount'] = 3
BRANCHES['mozilla-inbound']['platforms']['win64']['win8_64']['opt_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['macosx64']['mountainlion']['opt_unittest_skipcount'] = 6
BRANCHES['mozilla-inbound']['platforms']['macosx64']['mountainlion']['opt_unittest_skiptimeout'] = 3200
BRANCHES['mozilla-inbound']['platforms']['win32']['xp-ix']['debug_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['win32']['xp-ix']['debug_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['win32']['win7-ix']['debug_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['win32']['win7-ix']['debug_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['win64']['win8_64']['debug_unittest_skipcount'] = 3
BRANCHES['mozilla-inbound']['platforms']['win64']['win8_64']['debug_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['macosx64']['snowleopard']['debug_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['macosx64']['snowleopard']['debug_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['macosx64']['mountainlion']['debug_unittest_skipcount'] = 6
BRANCHES['mozilla-inbound']['platforms']['macosx64']['mountainlion']['debug_unittest_skiptimeout'] = 3200
BRANCHES['mozilla-inbound']['platforms']['macosx64']['yosemite']['debug_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['macosx64']['yosemite']['debug_unittest_skiptimeout'] = 1800
BRANCHES['mozilla-inbound']['platforms']['linux']['ubuntu32_vm']['debug_unittest_skipcount'] = 2
BRANCHES['mozilla-inbound']['platforms']['linux']['ubuntu32_vm']['debug_unittest_skiptimeout'] = 1800

# Enable mozharness pinning
for _, branch in items_at_least(BRANCHES, 'gecko_version', 30):
    branch['script_repo_manifest'] = \
        "https://hg.mozilla.org/%(repo_path)s/raw-file/%(revision)s/" + \
        "testing/mozharness/mozharness.json"

BRANCHES['mozilla-b2g30_v1_4']['script_repo_manifest'] = \
    "https://hg.mozilla.org/%(repo_path)s/raw-file/%(revision)s/" + \
    "testing/mozharness/mozharness.json"

# Filter the tests that are enabled on holly for bug 985718.
for platform in BRANCHES['holly']['platforms'].keys():
    if platform not in PLATFORMS:
        continue

    for slave_platform in PLATFORMS[platform]['slave_platforms']:
        slave_p = BRANCHES['holly']['platforms'][platform][slave_platform]
        slave_p['opt_unittest_suites'] = MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + MOCHITEST_DT
        slave_p['debug_unittest_suites'] = MOCHITEST + REFTEST_ONE_CHUNK + REFTEST_NO_IPC + MOCHITEST_DT_3

        # Enable content sandbox tests for Windows bit
        if slave_platform in PLATFORMS['win64']['slave_platforms'] or slave_platform in PLATFORMS['win32']['slave_platforms']:
            slave_p['opt_unittest_suites'] += MOCHITEST_CSB
            slave_p['debug_unittest_suites'] += MOCHITEST_CSB

# Enable Yosemite testing on select branches only
delete_slave_platform(BRANCHES, PLATFORMS, {'macosx64': 'yosemite'}, branch_exclusions=['try'])

# Run Jetpack tests everywhere except on versioned B2G branches.
for name in [x for x in BRANCHES.keys() if not x.startswith('mozilla-b2g')]:
    branch = BRANCHES[name]
    for pf in PLATFORMS:
        if pf not in branch['platforms']:
            continue
        # Skip these platforms
        if pf in ('linux64-asan', ):
            continue
        for slave_pf in branch['platforms'][pf].get(
                'slave_platforms', PLATFORMS[pf]['slave_platforms']):
            if slave_pf not in branch['platforms'][pf]:
                continue
            branch['platforms'][pf][slave_pf]['opt_unittest_suites'].append(('jetpack', ['jetpack']))
            branch['platforms'][pf][slave_pf]['debug_unittest_suites'].append(('jetpack', ['jetpack']))

# cppunittest jobs ride the train with 28, so they need to be disabled
# for branches running an older version.
# https://bugzilla.mozilla.org/show_bug.cgi?id=937637
# cppunittest jobs ride the train with 28, so they need to be disabled
# for branches running an older version.
# https://bugzilla.mozilla.org/show_bug.cgi?id=937637
for platform in PLATFORMS.keys():
    # See Bug 997946 - skip these on OS X 10.8 due to limited capacity
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 28):
        if platform not in branch['platforms']:
            continue
        for slave_platform in branch['platforms'][platform]:
            if slave_platform not in ['mountainlion', 'yosemite']:
                continue
            for suite_type in ['opt_unittest_suites', 'debug_unittest_suites']:
                for cpp_suite in CPPUNIT:
                    try:
                        branch['platforms'][platform][slave_platform][suite_type].remove(cpp_suite)
                    except ValueError:
                        # wasn't in the list anyways
                        pass

# Enable Mn on opt/debug win for gecko >= 33
for platform in PLATFORMS.keys():
    if platform != 'win32':
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 33):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += MARIONETTE[:]
                    BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites'] += MARIONETTE[:]

# Enable Mn on opt/debug win64 for gecko >= 36
for platform in PLATFORMS.keys():
    if platform != 'win64':
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 36):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += MARIONETTE[:]
                    BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites'] += MARIONETTE[:]

# Enable wpt on linux[64] opt for gecko >= 35
for platform in PLATFORMS.keys():
    if platform not in ['linux', 'linux64']:
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 35):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEB_PLATFORM_TESTS_CHUNKED[:] + WEB_PLATFORM_REFTESTS[:]

# Enable wpt on windows opt for gecko >= 36
for platform in PLATFORMS.keys():
    if platform not in ['win32', 'win64']:
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 36):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEB_PLATFORM_TESTS_CHUNKED[:] + WEB_PLATFORM_REFTESTS[:]

# Enable wpt on OSX 10.8 for gecko >= 39
for platform in PLATFORMS.keys():
    if platform not in ['macosx64']:
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 39):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:

            # These are not stable enough on OS X 10.6
            if slave_platform == "snowleopard":
                continue

            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEB_PLATFORM_TESTS_CHUNKED[:] + WEB_PLATFORM_REFTESTS[:]

# Enable Mn on opt linux/linux64 for gecko >= 32
for platform in PLATFORMS.keys():
    if platform not in ['linux', 'linux64']:
        continue
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 32):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += MARIONETTE[:]

# reftest-ipc and crashtest-ipc on linux opt disabled on gecko > 36
for platform in PLATFORMS.keys():
    if platform not in ['linux']:
        continue
    for name, branch in items_before(BRANCHES, 'gecko_version', 36):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += REFTEST_IPC

# reftest is chunked on linux32 for gecko >= 36
for platform in PLATFORMS.keys():
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 36):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if slave_platform not in ['ubuntu32_vm']:
                continue
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    opt_suites = BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites']
                    opt_suites = [x for x in opt_suites if x[0] and x[0] != 'reftest'] + REFTEST_TWO_CHUNKS
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] = opt_suites
                    debug_suites = BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites']
                    debug_suites = [x for x in debug_suites if x[0] and x[0] != 'reftest'] + REFTEST_TWO_CHUNKS
                    BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites'] = debug_suites

# Enable jittests on trunk trees https://bugzilla.mozilla.org/show_bug.cgi?id=973900
for platform in PLATFORMS.keys():
    # run in chunks on linux only
    if platform in ['linux', 'linux64', 'linux64-asan', 'linux64-cc']:
        jittests = JITTEST_CHUNKED
    else:
        jittests = JITTEST

    for name, branch in items_at_least(BRANCHES, 'gecko_version', 31):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:

            # See Bug 997946 - skip these on OS X 10.8 due to limited capacity
            if slave_platform in ['mountainlion', 'yosemite']:
                continue

            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += jittests[:]
                    BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites'] += jittests[:]

# Enable webapprt-chrome tests on cedar
for platform in PLATFORMS.keys():
    for slave_platform in PLATFORMS[platform]['slave_platforms']:
        if slave_platform not in BRANCHES['cedar']['platforms'][platform]:
            continue
        BRANCHES['cedar']['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEBAPPRT_CHROME[:]
        BRANCHES['cedar']['platforms'][platform][slave_platform]['debug_unittest_suites'] += WEBAPPRT_CHROME[:]

# bug 1051886 enable mochitest-gl tests to ride trains
for platform in PLATFORMS.keys():
    for name, branch in items_at_least(BRANCHES, 'gecko_version', 36):
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in BRANCHES[name]['platforms']:
                if slave_platform in BRANCHES[name]['platforms'][platform]:
                    BRANCHES[name]['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_WEBGL
                    BRANCHES[name]['platforms'][platform][slave_platform]['debug_unittest_suites']+= MOCHITEST_WEBGL

# Enable web-platform-tests on cedar
for platform in PLATFORMS.keys():
    if platform not in BRANCHES['cedar']['platforms']:
        continue

    for slave_platform in PLATFORMS[platform]['slave_platforms']:
        if slave_platform not in BRANCHES['cedar']['platforms'][platform]:
            continue

        if not (platform in ('linux64', 'linux', 'win32', 'win64') or
                (platform == "macosx64" and slave_platform != "snowleopard")):
            BRANCHES['cedar']['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEB_PLATFORM_REFTESTS[:]
            BRANCHES['cedar']['platforms'][platform][slave_platform]['opt_unittest_suites'] += WEB_PLATFORM_TESTS_CHUNKED[:]
        BRANCHES['cedar']['platforms'][platform][slave_platform]['debug_unittest_suites'] += WEB_PLATFORM_TESTS_CHUNKED[:] + WEB_PLATFORM_REFTESTS

# Enable mozbase unit tests on cedar
# https://bugzilla.mozilla.org/show_bug.cgi?id=971687
for platform in PLATFORMS.keys():
    if platform not in BRANCHES['cedar']['platforms']:
        continue
    for slave_platform in PLATFORMS[platform]['slave_platforms']:
        if slave_platform in BRANCHES['cedar']['platforms'][platform]:
            BRANCHES['cedar']['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOZBASE[:]
            BRANCHES['cedar']['platforms'][platform][slave_platform]['debug_unittest_suites'] += MOZBASE[:]

# Enable mochitest-jetpack tests on try
for platform in PLATFORMS.keys():
    for slave_platform in PLATFORMS[platform]['slave_platforms']:
        if slave_platform not in BRANCHES['try']['platforms'][platform]:
            continue
        BRANCHES['try']['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_JP[:]
        BRANCHES['try']['platforms'][platform][slave_platform]['debug_unittest_suites'] += MOCHITEST_JP[:]

# Enable e10s Linux mochitests on trunk branches
# Enable e10s browser-chrome mochitests on trunk branches, opt builds only for all platforms (not ready for Xp).
# Enable e10s devtools tests for Linux opt on trunk branches
# Enable e10s reftests/crashtests for Linux opt on trunk branches
# Enable e10s marionette tests for Linux32 opt on trunk branches
# Fix this to a certain gecko version once e10s starts riding the trains
mc_gecko_version = BRANCHES['mozilla-central']['gecko_version']
for name, branch in items_at_least(BRANCHES, 'gecko_version', mc_gecko_version):
    if name == "holly": # On Holly we use normal mochitest as e10s ones
        continue
    for platform in PLATFORMS.keys():
        if platform not in branch['platforms']:
            continue
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if platform in branch['platforms'] and slave_platform in branch['platforms'][platform] and \
                    not slave_platform == 'xp-ix':
                branch['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_BC_3_E10S[:]
            if platform in ('linux', 'linux64', 'linux64-asan'):
                branch['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_E10S[:]
            if platform in ('linux', 'linux64'):
                branch['platforms'][platform][slave_platform]['debug_unittest_suites'] += MOCHITEST_E10S[:]
                branch['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_DT_E10S[:] + REFTEST_E10S[:]
            if platform == 'linux':
                branch['platforms'][platform][slave_platform]['opt_unittest_suites'] += MARIONETTE_E10S[:]

# Bug 1080134: we want to disable all 32-bit testing on win8 for gecko 36 and
# higher, and enable 64-bit tests on win8 instead.
# Disable 64-bit win8 testing on gecko 35 and lower
for name, branch in items_before(BRANCHES, 'gecko_version', 36):
    if 'win64' in branch['platforms']:
        del branch['platforms']['win64']
for name, branch in items_at_least(BRANCHES, 'gecko_version', 36):
    if 'win32' not in branch['platforms']:
        continue
    if 'slave_platforms' in branch['platforms']['win32']:
        if 'win8' in branch['platforms']['win32']['slave_platforms']:
            branch['platforms']['win32']['slave_platforms'].remove('win8')
    else:
        branch['platforms']['win32']['slave_platforms'] = ['xp-ix', 'win7-ix']
    if 'talos_slave_platforms' in branch['platforms']['win32']:
        if 'win8' in branch['platforms']['win32']['talos_slave_platforms']:
            branch['platforms']['win32']['talos_slave_platforms'].remove('win8')
    else:
        branch['platforms']['win32']['talos_slave_platforms'] = ['xp-ix', 'win7-ix']


# TALOS: If you set 'talos_slave_platforms' for a branch you will only get that subset of platforms
for branch in BRANCHES.keys():
    for os in PLATFORMS.keys():  # 'macosx64', 'win32' and on
        if os not in BRANCHES[branch]['platforms'].keys():
            continue
        if BRANCHES[branch]['platforms'][os].get('talos_slave_platforms') is None:
            continue
        platforms_for_os = get_talos_slave_platforms(PLATFORMS, platforms=(os,))
        enabled_platforms_for_os = BRANCHES[branch]['platforms'][os]['talos_slave_platforms']
        for s in SUITES.iterkeys():
            tests_key = '%s_tests' % s
            if tests_key in BRANCHES[branch]:
                tests = list(BRANCHES[branch]['%s_tests' % s])
                tests[3] = [x for x in tests[3] if x not in platforms_for_os or x in enabled_platforms_for_os]
                BRANCHES[branch]['%s_tests' % s] = tuple(tests)

# Versioned b2g branches shouldn't run mochitest-browser-chrome on linux debug builds
for name in [x for x in BRANCHES.keys() if x.startswith('mozilla-b2g')]:
    branch = BRANCHES[name]
    if 'linux' in branch['platforms'] and 'ubuntu32_vm' in branch['platforms']['linux']:
        for chunked_bc in MOCHITEST_BC_3:
            branch['platforms']['linux']['ubuntu32_vm']['debug_unittest_suites'].remove(chunked_bc)
    if 'linux64' in branch['platforms'] and 'ubuntu64_vm' in branch['platforms']['linux64']:
        for chunked_bc in MOCHITEST_BC_3:
            branch['platforms']['linux64']['ubuntu64_vm']['debug_unittest_suites'].remove(chunked_bc)
    if 'linux64-asan' in branch['platforms'] and 'ubuntu64-asan_vm' in branch['platforms']['linux64-asan']:
        for chunked_bc in MOCHITEST_BC_3:
            branch['platforms']['linux64-asan']['ubuntu64-asan_vm']['debug_unittest_suites'].remove(chunked_bc)
    if 'linux64-cc' in branch['platforms'] and 'ubuntu64_vm' in branch['platforms']['linux64-cc']:
        for chunked_bc in MOCHITEST_BC_3:
            branch['platforms']['linux64-cc']['ubuntu64_vm']['debug_unittest_suites'].remove(chunked_bc)


# remove mochitest-browser-chrome and mochitest-devtools-chrome
# from b2g30, b2g32 - bug 1045398
for name in [x for x in BRANCHES.keys() if x.startswith('mozilla-b2g')]:
    branch = BRANCHES[name]
    for platform in branch['platforms']:
        for item in branch['platforms'][platform].keys():
            try:
                if 'debug_unittest_suites' in branch['platforms'][platform][item]:
                    unit_tests = branch['platforms'][platform][item]
                    for element in unit_tests:
                        for component in unit_tests[element]:
                            if (component[0] == 'mochitest-browser-chrome' or
                                component[0] == 'mochitest-devtools-chrome'):
                                unit_tests[element].remove(component)
            except TypeError:
                # not an iterable,
                pass


# mochitest-browser-chrome changes in 30:
#  * it's done chunked
#
# Exception: linux debug tests are always chunked and always on ec2 machines,
# so don't make any changes to them (the defaults are correct).
for name, branch in items_before(BRANCHES, 'gecko_version', 30):
    for platform in branch['platforms']:
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if slave_platform not in branch['platforms'][platform]:
                continue
            branch['platforms'][platform][slave_platform]['opt_unittest_suites'] += MOCHITEST_BC
            if 'ubuntu' not in slave_platform:
                branch['platforms'][platform][slave_platform]['debug_unittest_suites'] += MOCHITEST_BC
            for chunked_bc in MOCHITEST_BC_3:
                try:
                    branch['platforms'][platform][slave_platform]['opt_unittest_suites'].remove(chunked_bc)
                    if 'ubuntu' not in slave_platform:
                        branch['platforms'][platform][slave_platform]['debug_unittest_suites'].remove(chunked_bc)
                except ValueError:
                    # wasn't in the list anyways
                    pass

# mochitest-devtools-chrome only exists on 30+; remove mountainlion from
# b2g branches 29 and below
for name, branch in items_before(BRANCHES, 'gecko_version', 30):
    for platform in branch['platforms']:
        for slave_platform in PLATFORMS[platform]['slave_platforms']:
            if slave_platform not in branch['platforms'][platform]:
                continue
            # Delete mountainlion, bug 997959
            if slave_platform in ('mountainlion', ) and 'b2g' in name:
                del branch['platforms'][platform][slave_platform]
                continue
            try:
                branch['platforms'][platform][slave_platform]['opt_unittest_suites'].remove(MOCHITEST_DT[0])
            except ValueError:
                # wasn't there anyways
                pass
            for dt in MOCHITEST_DT_3:
                try:
                    branch['platforms'][platform][slave_platform]['debug_unittest_suites'].remove(dt)
                except ValueError:
                    # wasn't there anyways
                    pass

# Disable Linux64-cc in every branch except try
for name in BRANCHES.keys():
    if name in ('try',):
        continue
    for platform in ('linux64-cc',):
        if platform in BRANCHES[name]['platforms']:
            del BRANCHES[name]['platforms'][platform]

# Mac OSX signing changes in gecko 34 - bug 1117637, bug 1047584
for name, branch in items_before(BRANCHES, 'gecko_version', 34):
  if 'macosx64' in BRANCHES[name]['platforms']:
    BRANCHES[name]['platforms']['macosx64']['mac_res_subdir'] = 'MacOS'

if __name__ == "__main__":
    import sys
    import pprint

    args = sys.argv[1:]

    if len(args) > 0:
        items = dict([(b, BRANCHES[b]) for b in args])
    else:
        items = dict(BRANCHES.items() + PROJECTS.items())

    for k, v in sorted(items.iteritems()):
        out = pprint.pformat(v)
        for l in out.splitlines():
            print '%s: %s' % (k, l)

    for suite in sorted(SUITES):
        out = pprint.pformat(SUITES[suite])
        for l in out.splitlines():
            print '%s: %s' % (suite, l)
