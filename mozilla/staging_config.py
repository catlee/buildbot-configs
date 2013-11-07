from copy import deepcopy
import production_config as pc

MAC_LION_MINIS = ['bld-lion-r5-%03d' % x for x in range(87, 93) if x not in [88]]
WIN32_IXS      = ['mw32-ix-slave%02i' % x for x in (1,)]
WIN64_IXS      = ['w64-ix-slave%02i' % x for x in (4, 5, 22, 80)]
WIN64_REV2     = ['ix-mn-w0864-%03d' % x for x in range(1,3)]
MOCK_DL120G7   = ['bld-centos6-hp-%03d' % x for x in range(1, 6)]
LINUX64_EC2    = ['dev-linux64-ec2-%03d' % x for x in range(1, 50)]

STAGING_SLAVES = {
    'win32':            WIN32_IXS,
    'win64':            WIN64_IXS,
    'win64-rev2':       WIN64_REV2,
    'macosx64-lion':    MAC_LION_MINIS,
    'mock':             MOCK_DL120G7 + LINUX64_EC2,
}

SLAVES = deepcopy(STAGING_SLAVES)

for p, slaves in pc.SLAVES.items() + pc.TRY_SLAVES.items():
    if p not in SLAVES:
        SLAVES[p] = list(slaves)
    else:
        SLAVES[p].extend(slaves)


TRY_SLAVES = deepcopy(SLAVES)

GLOBAL_VARS = {
    'staging': True,
    'config_repo_path': 'build/buildbot-configs',
    'buildbotcustom_repo_path': 'build/buildbotcustom',
    'stage_server': 'dev-stage01.srv.releng.scl3.mozilla.com',
    'aus2_host': 'dev-stage01.srv.releng.scl3.mozilla.com',
    'aus2_user': 'ffxbld',
    'aus2_ssh_key': 'ffxbld_dsa',
    'download_base_url': 'http://dev-stage01.srv.releng.scl3.mozilla.com/pub/mozilla.org/firefox',
    'mobile_download_base_url': 'http://dev-stage01.srv.releng.scl3.mozilla.com/pub/mozilla.org/mobile',
    'graph_server': 'graphs.allizom.org',
    # XXX: should point at aus4-admin-dev once production is pointing elsewhere
    #'balrog_api_root': 'https://aus4-admin-dev.allizom.org',
    'build_tools_repo_path': 'build/tools',
    'base_clobber_url': 'http://clobberer-stage.pvt.build.mozilla.org/index.php',
    'disable_tinderbox_mail': True,
    # List of talos masters to notify of new builds,
    # and if a failure to notify the talos master should result in a warning,
    # and sendchange retry count before give up
    'talos_masters': [
        ('dev-master01.build.scl1.mozilla.com:9901', True, 1),
    ],
    # List of unittest masters to notify of new builds to test,
    # if a failure to notify the master should result in a warning,
    # and sendchange retry count before give up
    'unittest_masters': [
        ('dev-master01.build.scl1.mozilla.com:9901', True, 1),
        ],
    'xulrunner_tinderbox_tree': 'MozillaTest',
    'weekly_tinderbox_tree': 'MozillaTest',
    'l10n_tinderbox_tree': 'MozillaStaging',
    'packaged_unittest_tinderbox_tree': 'MozillaTest',
    'tinderbox_tree': 'MozillaTest',
    'mobile_tinderbox_tree': 'MobileTest',
    'hg_username': 'stage-ffxbld',
    'base_mirror_urls': ['http://hg-internal.dmz.scl3.mozilla.com'],
    'base_bundle_urls': ['http://dev-stage01.build.mozilla.org/pub/mozilla.org/firefox/bundles'],
    'tooltool_url_list': ['http://runtime-binaries.pvt.build.mozilla.org/tooltool'],
}

BUILDS_BEFORE_REBOOT = 5
SYMBOL_SERVER_HOST = 'dev-stage01.srv.releng.scl3.mozilla.com'

# Local branch overrides
BRANCHES = {
    'mozilla-central': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-release': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-beta': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-aurora': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-esr17': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-esr24': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-b2g18': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-b2g18_v1_0_1': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-b2g18_v1_1_0_hd': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'mozilla-b2g26_v1_2': {
        'enable_blocklist_update': False,
        'blocklist_update_on_closed_tree': False,
    },
    'try': {
        'download_base_url': 'http://dev-stage01.srv.releng.scl3.mozilla.com/pub/mozilla.org/firefox',
        'mobile_download_base_url': 'http://dev-stage01.srv.releng.scl3.mozilla.com/pub/mozilla.org/mobile',
        'enable_mail_notifier': False, # Set to True when testing
        'email_override': [], # Set to your address when testing
        'package_url': 'http://dev-stage01.srv.releng.scl3.mozilla.com/pub/mozilla.org/firefox/try-builds',
        'talos_masters': [],
        'platforms': {
            'win32': {
                'env': {
                    'SYMBOL_SERVER_HOST': 'dev-stage01.srv.releng.scl3.mozilla.com',
                    'MOZ_OBJDIR': 'obj-firefox',
                    'TINDERBOX_OUTPUT': '1',
                    'MOZ_CRASHREPORTER_NO_REPORT': '1',
                    # Source server support, bug 506702
                    'PDBSTR_PATH': '/c/Program Files (x86)/Windows Kits/8.0/Debuggers/x64/srcsrv/pdbstr.exe',
                    'HG_SHARE_BASE_DIR': 'c:/builds/hg-shared',
                    'BINSCOPE': 'C:\Program Files\Microsoft\SDL BinScope\Binscope.exe',
                    'PATH': "${MOZILLABUILD}python27;${MOZILLABUILD}buildbotve\\scripts;${PATH}",
                }
            }
        }
    },
}

PLATFORM_VARS = {}

PROJECTS = {
    'fuzzing': {
        'disable_tinderbox_mail': True,
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'fuzzing_bundle': 'http://pvtbuilds.pvt.build.mozilla.org/bundles/fuzzing.hg',
        'fuzzing_repo': 'ssh://stage-ffxbld@hg.mozilla.org/private/fuzzing',
        'fuzzing_remote_host': 'stage-ffxbld@stage.mozilla.org',
        # Path needs extra leading slash due to optparse expansion on Win32
        'fuzzing_base_dir': '//mnt/pvt_builds/staging/fuzzing/',
        'idle_slaves': 0,
    },
    'nanojit': {
        'disable_tinderbox_mail': True,
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'idle_slaves': 0,
        'tinderbox_tree': 'MozillaTest',
    },
}

BRANCH_PROJECTS = {
    'spidermonkey_tier_1': {
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'idle_slaves': 0,
        'disable_tinderbox_mail': False,
    },
    'spidermonkey_try': {
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'idle_slaves': 0,
        'disable_tinderbox_mail': False,
    },
    'spidermonkey_info': {
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'idle_slaves': 0,
        'disable_tinderbox_mail': False,
    },
}
