from copy import deepcopy

import config_common
reload(config_common)
from config_common import loadDefaultValues, loadCustomTalosSuites

import master_common
reload(master_common)
from master_common import setMainFirefoxVersions, items_before, items_at_least

import project_branches
reload(project_branches)
from project_branches import PROJECT_BRANCHES, ACTIVE_PROJECT_BRANCHES

import localconfig
reload(localconfig)
from localconfig import SLAVES, TRY_SLAVES, GLOBAL_VARS, GRAPH_CONFIG
from config import MOZHARNESS_REBOOT_CMD

TALOS_REMOTE_FENNEC_OPTS = {
    'productName': 'fennec',
    'remoteTests': True,
    'remoteExtras': {
        'options': [
            '--sampleConfig', 'remote.config',
            '--output', 'local.yml',
            '--webServer', 'talos-remote.pvt.build.mozilla.org',
            '--browserWait', '60',
        ],
    },
}

ANDROID_UNITTEST_REMOTE_EXTRAS = {'cmdOptions': ['--bootstrap'], }

BRANCHES = {
    'mozilla-central':     {},
    'mozilla-aurora':      {},
    'mozilla-release':     {},
    'mozilla-beta':        {},
    'mozilla-b2g26_v1_2': {
        'gecko_version': 26,
    },
    'mozilla-b2g28_v1_3': {
        'gecko_version': 28,
    },
    'mozilla-b2g30_v1_4': {
        'gecko_version': 30,
    },
    'mozilla-b2g18': {
        'datazilla_url': None,
        'gecko_version': 18,
        'platforms': {
            'android-noion': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g18_v1_1_0_hd': {
        'datazilla_url': None,
        'gecko_version': 18,
        'platforms': {
            'android-noion': {},
        },
        'lock_platforms': True,
    },
    'try': {'coallesce_jobs': False},
}

setMainFirefoxVersions(BRANCHES)

# Talos
PLATFORMS = {
    'android': {},
    'android-armv6': {},
    'android-noion': {},
    'android-x86': {},
}

PLATFORMS['android']['slave_platforms'] = \
    ['tegra_android', 'panda_android', 'vm_android_2_3', 'ubuntu64_hw_mobile', ]
PLATFORMS['android']['env_name'] = 'android-perf'
PLATFORMS['android']['is_mobile'] = True
PLATFORMS['android']['tegra_android'] = {
    'name': "Android 2.2 Tegra",
    'mozharness_talos': False,
}
PLATFORMS['android']['panda_android'] = {
    'name': "Android 4.0 Panda",
    'mozharness_talos': True,
}
PLATFORMS['android']['vm_android_2_3'] = {
    'name': "Android 2.3 Emulator",
}
PLATFORMS['android']['ubuntu64_hw_mobile'] = {
    'name': "Android 2.3 Emulator on ix",
}
PLATFORMS['android']['stage_product'] = 'mobile'
PLATFORMS['android']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': None,
    'talos_script_maxtime': 10800,
}

PLATFORMS['android-armv6']['slave_platforms'] = ['tegra_android-armv6']
PLATFORMS['android-armv6']['env_name'] = 'android-perf'
PLATFORMS['android-armv6']['is_mobile'] = True
PLATFORMS['android-armv6']['tegra_android-armv6'] = {'name': "Android 2.2 Armv6 Tegra"}
PLATFORMS['android-armv6']['stage_product'] = 'mobile'
PLATFORMS['android-armv6']['mozharness_config'] = {}

PLATFORMS['android-noion']['slave_platforms'] = ['tegra_android-noion']
PLATFORMS['android-noion']['env_name'] = 'android-perf'
PLATFORMS['android-noion']['is_mobile'] = True
PLATFORMS['android-noion']['tegra_android-noion'] = {'name': "Android 2.2 no-ionmonkey Tegra"}
PLATFORMS['android-noion']['stage_product'] = 'mobile'
PLATFORMS['android-noion']['mozharness_python'] = '/tools/buildbot/bin/python'

PLATFORMS['android-x86']['slave_platforms'] = ['ubuntu64_hw']
PLATFORMS['android-x86']['env_name'] = 'android-perf'
PLATFORMS['android-x86']['is_mobile'] = True
PLATFORMS['android-x86']['ubuntu64_hw'] = {'name': "Android 4.2 x86 Emulator"}
PLATFORMS['android-x86']['stage_product'] = 'mobile'
PLATFORMS['android-x86']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
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

# List of Android platforms that have talos enabled
ANDROID = ["panda_android", "tegra_android"]
ANDROID_NOT_PANDA = [slave_plat for slave_plat in ANDROID if 'panda' not in slave_plat]

SUITES = {
    'remote-ts': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'ts', '--mozAfterPaint', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-tspaint': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'ts_paint', '--mozAfterPaint'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-tsvg': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvg', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-tsvgx': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgx', '--noChrome', '--tppagecycles', '10'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-tcanvasmark': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tcanvasmark', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_PANDA),
    },
    'remote-trobopan': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'trobopan', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-troboprovider': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tprovider', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-trobocheck2': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tcheck2', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
    'remote-tp4m_nochrome': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp4m', '--noChrome', '--rss'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID),
    },
}

BRANCH_UNITTEST_VARS = {
    'hghost': 'hg.mozilla.org',
    # turn on platforms as we get them running
    'platforms': {
        'android': {},
        'android-armv6': {},
        'android-noion': {},
        'android-debug': {},
        'android-x86': {},
    },
}

EMPTY_UNITTEST_DICT = {'opt_unittest_suites': [], 'debug_unittest_suites': []}

ANDROID_UNITTEST_DICT = {
    'opt_unittest_suites': [
        ('mochitest-1', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 1,
             },
        )),
        ('mochitest-2', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 2,
             },
        )),
        ('mochitest-3', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 3,
             },
        )),
        ('mochitest-4', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 4,
             },
        )),
        ('mochitest-5', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 5,
             },
        )),
        ('mochitest-6', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 6,
             },
        )),
        ('mochitest-7', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 7,
             },
        )),
        ('mochitest-8', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 8,
             },
        )),
        ('reftest-1', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 1,
             },
        )),
        ('reftest-2', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 2,
             },
        )),
        ('reftest-3', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 3,
             },
        )),
        ('reftest-4', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 4,
             },
        )),
        ('crashtest', (
            {'suite': 'crashtest',
             },
        )),
        ('xpcshell', (
            {'suite': 'xpcshell',
             },
        )),
        ('jsreftest-1', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 1,
             },
        )),
        ('jsreftest-2', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 2,
             },
        )),
        ('jsreftest-3', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 3,
             },
        )),
        ('robocop', (
            {'suite': 'mochitest-robocop',
             },
        )),
        ('mochitest-gl', (
            {'suite': 'mochitest-plain',
             'testManifest': 'gl.json',
             },
        )),
    ],
    'debug_unittest_suites': [],
}

ANDROID_MOZHARNESS_MOCHITEST = [
    ('mochitest-1',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-1'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-2',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-2'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-3',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-3'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-4',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-4'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-5',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-5'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-6',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-6'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-7',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-7'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-8',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-8'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_REFTEST = [
    ('reftest-1',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-1'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-2',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-2'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-3',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-3'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-4',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-4'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]
ANDROID_MOZHARNESS_CRASHTEST = [
    ('crashtest',
     {'suite': 'crashtest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--crashtest-suite', 'crashtest'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_JSREFTEST = [
    ('jsreftest-1',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-1'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('jsreftest-2',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-2'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('jsreftest-3',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-3'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_XPCSHELL = [
    ('xpcshell',
     {'suite': 'xpcshell',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--xpcshell-suite', 'xpcshell'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_MOCHITESTGL = [
    ('mochitest-gl',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-gl'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_PLAIN_REFTEST = [
    ('plain-reftest-1',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-1'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-2',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-2'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-3',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-3'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-4',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-4'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-5',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-5'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-6',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-6'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-7',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-7'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-8',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-8'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_JITTEST = [
    ('jittest',
     {'suite': 'jittest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jittest-suite', 'jittest'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_CPPUNITTEST = [
    ('cppunit',
     {'suite': 'cppunit',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--cppunittest-suite', 'cppunittest'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_PLAIN_ROBOCOP = [
    ('robocop-1',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-1'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-2',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-2'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-3',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-3'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-4',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-4'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-5',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-5'],
      'blob_upload': True,
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_NOION_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}
for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if not suite[0].startswith('jsreftest'):
        continue
    ANDROID_NOION_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_PLAIN_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}

TEGRA_RELEASE_PLAIN_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}

ANDROID_PLAIN_REFTEST_DICT = {
    'opt_unittest_suites': [
        ('plain-reftest-1', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 1,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-2', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 2,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-3', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 3,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-4', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 4,
             'extra_args': '--ignore-window-size'
             },
        )),
    ],
}


ANDROID_PLAIN_ROBOCOP_DICT = {
    'opt_unittest_suites': [
        ('robocop-1', (
            {'suite': 'mochitest-robocop',
             'totalChunks': 2,
             'thisChunk': 1
             },
        )),
        ('robocop-2', (
            {'suite': 'mochitest-robocop',
             'totalChunks': 2,
             'thisChunk': 2
             },
        )),
    ],
}

for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if suite[0].startswith('reftest'):
        continue
    if suite[0].startswith('robocop'):
        continue
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_MOZHARNESS_PANDA_UNITTEST_DICT = {
    'opt_unittest_suites': ANDROID_MOZHARNESS_MOCHITEST + ANDROID_MOZHARNESS_PLAIN_ROBOCOP + ANDROID_MOZHARNESS_JSREFTEST + ANDROID_MOZHARNESS_CRASHTEST + ANDROID_MOZHARNESS_MOCHITESTGL + ANDROID_MOZHARNESS_PLAIN_REFTEST + ANDROID_MOZHARNESS_XPCSHELL + ANDROID_MOZHARNESS_JITTEST + ANDROID_MOZHARNESS_CPPUNITTEST,
    'debug_unittest_suites': ANDROID_MOZHARNESS_MOCHITEST + ANDROID_MOZHARNESS_PLAIN_ROBOCOP + ANDROID_MOZHARNESS_JSREFTEST + ANDROID_MOZHARNESS_CRASHTEST + ANDROID_MOZHARNESS_MOCHITESTGL + ANDROID_MOZHARNESS_JITTEST,
}

for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if suite[0].startswith('reftest'):
        continue
    if suite[0].startswith('mochitest-gl'):
        continue
    if suite[0].startswith('robocop'):
        continue
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

for suite in ANDROID_PLAIN_REFTEST_DICT['opt_unittest_suites']:
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

for suite in ANDROID_PLAIN_ROBOCOP_DICT['opt_unittest_suites']:
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_NOWEBGL_UNITTEST_DICT = deepcopy(ANDROID_PLAIN_UNITTEST_DICT)
# Bug 869590 Disable mochitest-gl for armv6, Bug 875633 Disable for Tegras
for suite in ANDROID_NOWEBGL_UNITTEST_DICT['opt_unittest_suites'][:]:
    if suite[0] == 'mochitest-gl':
        ANDROID_NOWEBGL_UNITTEST_DICT['opt_unittest_suites'].remove(suite)

ANDROID_PLAIN_UNITTEST_DICT['debug_unittest_suites'] = deepcopy(ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'])

# Beginning Androidx86 configurations
ANDROID_X86_MOZHARNESS_DICT = [
    ('androidx86-set-4', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'robocop-1',
            '--test-suite', 'robocop-2',
            '--test-suite', 'robocop-3',
            '--test-suite', 'xpcshell',
        ],
        'trychooser_suites': ['robocop-1', 'robocop-2', 'robocop-3', 'xpcshell'],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
]

ANDROID_X86_NOT_GREEN_DICT = [
    ('androidx86-set-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'jsreftest',
            '--test-suite', 'mochitest-1',
        ],
        'trychooser_suites': ['mochitest-1', 'jsreftest'],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('androidx86-set-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'mochitest-2',
            '--test-suite', 'mochitest-gl',
        ],
        'trychooser_suites': ['mochitest-2', 'mochitest-gl'],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('androidx86-set-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'reftest-1',
            '--test-suite', 'reftest-2',
            '--test-suite', 'reftest-3',
            '--test-suite', 'crashtest',
        ],
        'trychooser_suites': ['plain-reftest-1', 'plain-reftest-2', 'plain-reftest-3', 'crashtest'],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
]

# Funky DICT naming
ANDROID_X86_MOZHARNESS_UNITTEST_DICT = {
    'opt_unittest_suites': ANDROID_X86_MOZHARNESS_DICT,
    'debug_unittest_suites': [],
}
# End of Androidx86 configurations

# Beginning Android 2.3 configurations
ANDROID_2_3_MOZHARNESS_ENABLED_DICT = [
    ('mochitest-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-4', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-4',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-5', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-5',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-6', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-6',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-7', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-7',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-8', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-8',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-9', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-9',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-10', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-10',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-11', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-11',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('mochitest-12', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-12',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('robocop-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'robocop-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('robocop-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'robocop-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('robocop-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'robocop-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('robocop-4', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'robocop-4',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('xpcshell-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'xpcshell-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('xpcshell-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'xpcshell-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('xpcshell-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'xpcshell-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
]

# Beginning Android 2.3 configurations
ANDROID_2_3_MOZHARNESS_DISABLED_DICT = [
    ('mochitest-gl', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'mochitest-gl',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-4', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-4',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-5', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-5',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('jsreftest-6', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'jsreftest-6',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-4', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-4',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-5', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-5',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-6', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-6',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-7', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-7',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-8', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-8',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-9', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-9',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-10', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-10',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-11', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-11',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('plain-reftest-12', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'reftest-12',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('crashtest-1', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'crashtest-1',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('crashtest-2', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'crashtest-2',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
    ('crashtest-3', {
        'use_mozharness': True,
        'script_path': 'scripts/android_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidarm.py',
            '--test-suite', 'crashtest-3',
        ],
        'blob_upload': True,
        'timeout': 2400,
        'script_maxtime': 14400,
    },
    ),
]

# Funky DICT naming
ANDROID_2_3_MOZHARNESS_DICT = ANDROID_2_3_MOZHARNESS_ENABLED_DICT + ANDROID_2_3_MOZHARNESS_DISABLED_DICT
ANDROID_2_3_MOZHARNESS_UNITTEST_DICT = {
    'opt_unittest_suites': ANDROID_2_3_MOZHARNESS_DICT,
    'debug_unittest_suites': [],
}
# End of Android 2.3 configurations

# You must define opt_unittest_suites when enable_opt_unittests is True for a
# platform. Likewise debug_unittest_suites for enable_debug_unittests
PLATFORM_UNITTEST_VARS = {
    'android': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://talos-remote.pvt.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android': deepcopy(ANDROID_NOWEBGL_UNITTEST_DICT),
        'panda_android': deepcopy(ANDROID_MOZHARNESS_PANDA_UNITTEST_DICT),
    },
    'android-armv6': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://talos-remote.pvt.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android-armv6': deepcopy(ANDROID_NOWEBGL_UNITTEST_DICT),
    },
    'android-noion': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://talos-remote.pvt.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android-noion': deepcopy(ANDROID_NOION_UNITTEST_DICT),
    },
    'android-x86': {
        'product_name': 'fennec',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64_hw': deepcopy(ANDROID_X86_MOZHARNESS_UNITTEST_DICT),
    },
}

# Copy project branches into BRANCHES keys
for branch in ACTIVE_PROJECT_BRANCHES:
    BRANCHES[branch] = deepcopy(PROJECT_BRANCHES[branch])
    if BRANCHES[branch].get('mobile_platforms'):
        BRANCHES[branch]['platforms'] = deepcopy(BRANCHES[branch]['mobile_platforms'])

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
    if branch in ACTIVE_PROJECT_BRANCHES and 'mobile_platforms' in PROJECT_BRANCHES[branch]:
        for platform, platform_config in PROJECT_BRANCHES[branch]['mobile_platforms'].items():
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

#
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
BRANCHES['mozilla-central']['mobile_branch_name'] = "Mobile"
BRANCHES['mozilla-central']['mobile_talos_branch'] = "mobile"
BRANCHES['mozilla-central']['build_branch'] = "1.9.2"
BRANCHES['mozilla-central']['pgo_strategy'] = 'periodic'
BRANCHES['mozilla-central']['pgo_platforms'] = []
BRANCHES['mozilla-central']['platforms']['android']['enable_debug_unittests'] = True

######### mozilla-release
BRANCHES['mozilla-release']['release_tests'] = 1
BRANCHES['mozilla-release']['repo_path'] = "releases/mozilla-release"
BRANCHES['mozilla-release']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-release']['pgo_platforms'] = []

######### mozilla-beta
BRANCHES['mozilla-beta']['release_tests'] = 1
BRANCHES['mozilla-beta']['repo_path'] = "releases/mozilla-beta"
BRANCHES['mozilla-beta']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-beta']['pgo_platforms'] = []

######### mozilla-aurora
BRANCHES['mozilla-aurora']['repo_path'] = "releases/mozilla-aurora"
BRANCHES['mozilla-aurora']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-aurora']['pgo_platforms'] = []

######### mozilla-b2g26_v1_2
BRANCHES['mozilla-b2g26_v1_2']['repo_path'] = "releases/mozilla-b2g26_v1_2"
BRANCHES['mozilla-b2g26_v1_2']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g26_v1_2']['pgo_platforms'] = []

######### mozilla-b2g28_v1_3
BRANCHES['mozilla-b2g28_v1_3']['repo_path'] = "releases/mozilla-b2g28_v1_3"
BRANCHES['mozilla-b2g28_v1_3']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g28_v1_3']['pgo_platforms'] = []

######### mozilla-b2g30_v1_4
BRANCHES['mozilla-b2g30_v1_4']['repo_path'] = "releases/mozilla-b2g30_v1_4"
BRANCHES['mozilla-b2g30_v1_4']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g30_v1_4']['pgo_platforms'] = []

######### mozilla-b2g18
BRANCHES['mozilla-b2g18']['release_tests'] = 1
BRANCHES['mozilla-b2g18']['repo_path'] = "releases/mozilla-b2g18"
BRANCHES['mozilla-b2g18']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g18']['pgo_platforms'] = []

######### mozilla-b2g18_v1_1_0_hd
BRANCHES['mozilla-b2g18_v1_1_0_hd']['release_tests'] = 1
BRANCHES['mozilla-b2g18_v1_1_0_hd']['repo_path'] = "releases/mozilla-b2g18_v1_1_0_hd"
BRANCHES['mozilla-b2g18_v1_1_0_hd']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g18_v1_1_0_hd']['pgo_platforms'] = []

######## try
BRANCHES['try']['repo_path'] = "try"
BRANCHES['try']['platforms']['android']['enable_debug_unittests'] = True
BRANCHES['try']['pgo_strategy'] = 'try'
BRANCHES['try']['pgo_platforms'] = []
BRANCHES['try']['enable_try'] = True

# Ignore robocop chunks for mozilla-release, robocop-chunks is defined in
# ANDROID_PLAIN_UNITTEST_DICT
BRANCHES['mozilla-release']["platforms"]["android"]["tegra_android"][
    "opt_unittest_suites"] = deepcopy(TEGRA_RELEASE_PLAIN_UNITTEST_DICT["opt_unittest_suites"])

# Until we green out these Android x86 tests
BRANCHES['cedar']['platforms']['android-x86']['ubuntu64_hw']['opt_unittest_suites'] += ANDROID_X86_NOT_GREEN_DICT[:]
BRANCHES['ash']['platforms']['android-x86']['ubuntu64_hw']['opt_unittest_suites'] += ANDROID_X86_NOT_GREEN_DICT[:]
BRANCHES['ash']['platforms']['android']['ubuntu64_hw_mobile'] = {
    'opt_unittest_suites': deepcopy(ANDROID_2_3_MOZHARNESS_DICT)
}

# enable 2.3 tests to ride the trains but only mochitest, robocop and
# xpshell bug 989462
for name, branch in items_at_least(BRANCHES, 'gecko_version', 31):
    # Loop removes it from any branch that gets beyond here
    if name in ('ash',):
        continue
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform == ('android'):
            continue
        BRANCHES[name]['platforms']['android']['vm_android_2_3'] = {
            'opt_unittest_suites': deepcopy(ANDROID_2_3_MOZHARNESS_ENABLED_DICT),
            'debug_unittest_suites': []
        }

# MERGE DAY - Delete all references to android-noion once mozilla-b2g18 is EOL.
for branch in BRANCHES:
    if branch not in ('mozilla-b2g18', 'mozilla-b2g18_v1_1_0_hd'):
        if 'android-noion' in BRANCHES[branch]['platforms']:
            del BRANCHES[branch]['platforms']['android-noion']

for name, branch in items_before(BRANCHES, 'gecko_version', 22):
    if 'android' in branch['platforms']:
        del branch['platforms']['android']['panda_android']
        branch['platforms']['android']['slave_platforms'] = ['tegra_android']

# Panda debug enabled on trunk that rides the trains
# this stanza is to disable it for branches on an older version of gecko
for name, branch in items_before(BRANCHES, 'gecko_version', 31):
    # Loop removes it from any branch that gets beyond here
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform == ('android'):
            continue
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in branch['platforms'][platform]:
                continue
            if not 'panda' in slave_plat:
                continue
            if not branch['platforms'][platform][slave_plat]['debug_unittest_suites']:
                continue
            else:
                branch['platforms'][platform]['enable_debug_unittests'] = False

BRANCHES['cedar']['platforms']['android']['enable_debug_unittests'] = True
# this loop is to limit the debug tests run on trunk branches to
# M4,M5,M6,M7,J1,J2,J3 only for panda-android
d = ['mochitest-1', 'mochitest-2', 'mochitest-3', 'mochitest-4', 
     'mochitest-5', 'mochitest-6', 'mochitest-7', 'mochitest-8',
     'jsreftest-1', 'jsreftest-2', 'jsreftest-3', ]
for name, branch in items_at_least(BRANCHES, 'gecko_version', 31):
    # Loop removes it from any branch that gets beyond here
    if name in ('cedar', ):
        continue
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform == ('android'):
            continue
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in branch['platforms'][platform]:
                continue
            if not 'panda' in slave_plat:
                continue
            if not branch['platforms'][platform][slave_plat]['debug_unittest_suites']:
                continue
            if branch['platforms'][platform]['enable_debug_unittests'] is True:
                for type in branch['platforms'][platform][slave_plat]:
                    if 'debug_unittest_suite' in type:
                        for suite in branch['platforms'][platform][slave_plat][type][:]:
                            if suite[0] not in d:
                               branch['platforms'][platform][slave_plat][type].remove(suite)

# have to disable this manually or it blows up in misc.py
BRANCHES['ash']['platforms']['android']['enable_debug_unittests'] = False

# XPCShell (Gecko 23 based)
for name, branch in items_before(BRANCHES, 'gecko_version', 23):
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in branch['platforms'][platform]:
                continue
            for type in branch['platforms'][platform][slave_plat]:
                for suite in branch['platforms'][platform][slave_plat][type][:]:
                    if "xpcshell" in suite[0]:
                        branch['platforms'][platform][slave_plat][type].remove(suite)

# Panda XPCShell
for name, branch in items_before(BRANCHES, 'gecko_version', 28):
    # Loop removes it from any branch that gets beyond here
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in branch['platforms'][platform]:
                continue
            if not 'panda' in slave_plat:
                continue
            for type in branch['platforms'][platform][slave_plat]:
                for suite in branch['platforms'][platform][slave_plat][type][:]:
                    if "xpcshell" in suite[0]:
                        branch['platforms'][platform][slave_plat][type].remove(suite)

# panda reftests jobs ride the train with 29, so they need to be disabled
# for branches running an older version.
# https://bugzilla.mozilla.org/show_bug.cgi?id=929447
for name, branch in items_before(BRANCHES, 'gecko_version', 29):
    for platform in branch['platforms']:
        if platform not in PLATFORMS:
            continue
        for slave_plat in PLATFORMS[platform].get('slave_platforms', {}):
            # we don't want to change scheduling for non panda slaves
            # https://bugzilla.mozilla.org/show_bug.cgi?id=961575
            if not 'panda_android' in slave_plat:
                continue
            if slave_plat not in branch['platforms'][platform]:
                continue
            for type_ in branch['platforms'][platform][slave_plat]:
                for suite in branch['platforms'][platform][slave_plat][type_][:]:
                    if "plain-reftest" in suite[0]:
                        branch['platforms'][platform][slave_plat][type_].remove(suite)

# Disable Android x86 on branches that are older than gecko 29
# should not run Android x86 jobs
for name, branch in items_before(BRANCHES, 'gecko_version', 29):
    if 'android-x86' in branch['platforms']:
        branch['platforms']['android-x86']['ubuntu64_hw']['opt_unittest_suites'] = []

# cppunittest jobs ride the train with 28, so they need to be disabled
# for branches running an older version.
# https://bugzilla.mozilla.org/show_bug.cgi?id=937637
for name, branch in items_before(BRANCHES, 'gecko_version', 28):
    for platform in branch['platforms']:
        if platform not in PLATFORMS:
            continue
        for slave_plat in PLATFORMS[platform].get('slave_platforms', {}):
            if slave_plat not in branch['platforms'][platform]:
                continue
            for type_ in branch['platforms'][platform][slave_plat]:
                for suite in branch['platforms'][platform][slave_plat][type_][:]:
                    if "cppunit" in suite[0]:
                        branch['platforms'][platform][slave_plat][type_].remove(suite)

# schedule jittests for pandas on cedar and try
# https://bugzilla.mozilla.org/show_bug.cgi?id=912997
# https://bugzilla.mozilla.org/show_bug.cgi?id=931874
for branch in BRANCHES:
    # Loop removes it from any branch that gets beyond here
    if branch in ('cedar', 'try'):
        continue
    for platform in BRANCHES[branch]['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in BRANCHES[branch]['platforms'][platform]:
                continue
            if not slave_plat == "panda_android":
                continue
            for type in BRANCHES[branch]['platforms'][platform][slave_plat]:
                for suite in BRANCHES[branch]['platforms'][platform][slave_plat][type][:]:
                    if "jittest" in suite[0]:
                        BRANCHES[branch]['platforms'][platform][slave_plat][type].remove(suite)

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
