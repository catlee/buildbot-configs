MAC_LION_MINIS = ['bld-lion-r5-%03d' % x for x in range(1,16) + range(41,87) + [88] + range(93,95)]
LINUX_VMS      = ['bld-centos5-32-vmw-%03i' % x for x in range(1,7)]
LINUX_IXS      = ['linux-ix-slave%02i' % x for x in [1,2,6]]
LINUX64_IXS    = ['linux64-ix-slave%02i' % x for x in range(3, 7)]
WIN32_IXS      = ['mw32-ix-slave%02i' % x for x in range(2,13)]
WIN64_IXS      = ['w64-ix-slave%02i' % x for x in range(88,100)] + \
                 ['w64-ix-slave%03i' % x for x in range(100,158) if x not in range(110,131)]
WIN64_REV2     = ['w64-ix-slave%02i' % x for x in range(6,30) + range(42,44) + range(75,88) if x not in [22,80,85,86]] + \
                 ['w64-ix-slave%03i' % x for x in range(111,131)]
MOCK_DL120G7   = ['bld-centos6-hp-%03d' % x for x in range(6,24)] # 5 staging, 17 prod, 17 try
LINUX64_EC2    = ['bld-linux64-ec2-%03d' % x for x in range(1, 900)]
MOCK_IX        = ['bld-linux64-ix-%03d' % x for x in range(27, 38)]
if set(WIN64_REV2).intersection(set(WIN64_IXS)):
    raise Exception('WIN64_REV2 and WIN64_IXS overlap')

SLAVES = {
    'linux':            LINUX_VMS + LINUX_IXS,
    'linux64':          LINUX64_IXS,
    'win32':            WIN32_IXS,
    'win64':            WIN64_IXS,
    'win64-rev2':       WIN64_REV2,
    'macosx64-lion':    MAC_LION_MINIS,
    'mock':             MOCK_DL120G7 + LINUX64_EC2 + MOCK_IX,
}

TRY_LINUX      = []
TRY_LINUX_IXS  = []
TRY_LINUX64    = []
TRY_LINUX64_IXS= []
TRY_LINUX64_EC2= ['try-linux64-ec2-%03d' % x for x in range(1, 900)]
TRY_MAC64      = []
TRY_WIN32_IXS  = []
TRY_WIN64_IXS  = ['w64-ix-slave%02i' % x for x in range(67,75)]
TRY_WIN64_REV2 = ['w64-ix-slave%02i' % x for x in [3] + range(30,67) if x not in [42,43]] + \
                 ['w64-ix-slave%03i' % x for x in [110]]
TRY_MOCK_DL120G7 = ['bld-centos6-hp-%03d' % x for x in range(24,43)] + \
                   ['b-linux64-hp-%03d' % x for x in range(1, 7)]
TRY_MOCK_IX      = ['bld-linux64-ix-%03d' % x for x in range(49, 74)]
TRY_LION         = ['bld-lion-r5-%03d' % x for x in range(16,41)]
if set(TRY_WIN64_REV2).intersection(set(TRY_WIN64_IXS)):
    raise Exception('TRY_WIN64_REV2 and TRY_WIN64_IXS overlap')
if set(TRY_WIN64_IXS + TRY_WIN64_REV2).intersection(WIN64_IXS + WIN64_REV2):
    raise Exception('(TRY_WIN64_IXS + TRY_WIN64_REV2) and (WIN64_IXS + WIN64_REV2) overlap')

TRY_SLAVES = {
    'win32':       TRY_WIN32_IXS,
    'win64':       TRY_WIN64_IXS,
    'win64-rev2':  TRY_WIN64_REV2,
    'macosx64':    TRY_MAC64,
    'macosx64-lion': TRY_LION,
    'mock':        TRY_MOCK_DL120G7 + TRY_LINUX64_EC2 + TRY_MOCK_IX,
}

# Local overrides for default values
GLOBAL_VARS = {
    'config_repo_path': 'build/buildbot-configs',
    'buildbotcustom_repo_path': 'build/buildbotcustom',
    'stage_server': 'stage.mozilla.org',
    'aus2_host': 'aus3-staging.mozilla.org',
    'aus2_user': 'ffxbld',
    'aus2_ssh_key': 'auspush',
    'download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/firefox',
    'mobile_download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/mobile',
    'graph_server': 'graphs.mozilla.org',
    'balrog_api_root': 'https://aus4-admin.mozilla.org',
    'build_tools_repo_path': 'build/tools',
    'base_clobber_url': 'http://clobberer.pvt.build.mozilla.org/index.php',
    'disable_tinderbox_mail': True,
    # List of talos masters to notify of new builds,
    # and if a failure to notify the talos master should result in a warning,
    # and sendchange retry count before give up
    'talos_masters': [
        ('buildbot-master81.build.mozilla.org:9301', True, 5),
    ],
    # List of unittest masters to notify of new builds to test,
    # if a failure to notify the master should result in a warning,
    # and sendchange retry count before give up
    'unittest_masters': [
        ('buildbot-master81.build.mozilla.org:9301', True, 5),
    ],
    'xulrunner_tinderbox_tree': 'XULRunner',
    'weekly_tinderbox_tree': 'Testing',
    'l10n_tinderbox_tree': 'Mozilla-l10n',
    'base_mirror_urls': ['http://hg-internal.dmz.scl3.mozilla.com'],
    'base_bundle_urls': ['http://ftp.mozilla.org/pub/mozilla.org/firefox/bundles'],
    'tooltool_url_list': ['http://runtime-binaries.pvt.build.mozilla.org/tooltool'],
}

BUILDS_BEFORE_REBOOT = 1
SYMBOL_SERVER_HOST = 'symbolpush.mozilla.org'

# Local branch overrides
BRANCHES = {
    'mozilla-central': {
        'packaged_unittest_tinderbox_tree': 'Firefox',
        'tinderbox_tree': 'Firefox',
        'mobile_tinderbox_tree': 'Mobile',
        'mobile_build_failure_emails': ['<mobile-build-failures@mozilla.org>'],
    },
    'mozilla-release': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-Release',
        'tinderbox_tree': 'Mozilla-Release',
        'mobile_tinderbox_tree': 'Mozilla-Release',
    },
    'mozilla-esr17': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-Esr17',
        'tinderbox_tree': 'Mozilla-Esr17',
        'mobile_tinderbox_tree': 'Mozilla-Esr17',
    },
    'mozilla-esr24': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-Esr24',
        'tinderbox_tree': 'Mozilla-Esr24',
        'mobile_tinderbox_tree': 'Mozilla-Esr24',
    },
    'mozilla-b2g18': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-B2g18',
        'tinderbox_tree': 'Mozilla-B2g18',
        'mobile_tinderbox_tree': 'Mozilla-B2g18',
    },
    'mozilla-b2g18_v1_0_1': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-B2g18_v1_0_1',
        'tinderbox_tree': 'Mozilla-B2g18_v1_0_1',
        'mobile_tinderbox_tree': 'Mozilla-B2g18_v1_0_1',
    },
    'mozilla-b2g18_v1_1_0_hd': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-B2g18-v1.1.0hd',
        'tinderbox_tree': 'Mozilla-B2g18-v1.1.0hd',
        'mobile_tinderbox_tree': 'Mozilla-B2g18-v1.1.0hd',
    },
    'mozilla-b2g26_v1_2': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-B2g26-v1.2',
        'tinderbox_tree': 'Mozilla-B2g26-v1.2',
        'mobile_tinderbox_tree': 'Mozilla-B2g26-v1.2',
    },
    'mozilla-beta': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-Beta',
        'tinderbox_tree': 'Mozilla-Beta',
        'mobile_tinderbox_tree': 'Mozilla-Beta',
    },
    'mozilla-aurora': {
        'packaged_unittest_tinderbox_tree': 'Mozilla-Aurora',
        'tinderbox_tree': 'Mozilla-Aurora',
        'mobile_tinderbox_tree': 'Mozilla-Aurora',
    },
    'try': {
        'tinderbox_tree': 'Try',
        'mobile_tinderbox_tree': 'Try',
        'packaged_unittest_tinderbox_tree': 'Try',
        'download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/firefox/try-builds',
        'mobile_download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/firefox/try-builds',
        'enable_mail_notifier': True,
        'notify_real_author': True,
        'package_url': 'http://ftp.mozilla.org/pub/mozilla.org/firefox/try-builds',
        'talos_masters': [],
        'platforms': {
            'win32': {
                'env': {
                    'SYMBOL_SERVER_HOST': 'relengweb1.dmz.scl3.mozilla.com',
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
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'fuzzing_bundle': 'http://pvtbuilds.pvt.build.mozilla.org/bundles/fuzzing.hg',
        'fuzzing_repo': 'ssh://ffxbld@hg.mozilla.org/private/fuzzing',
        'fuzzing_remote_host': 'ffxbld@stage.mozilla.org',
        # Path needs extra leading slash due to optparse expansion on Win32
        'fuzzing_base_dir': '//mnt/pvt_builds/fuzzing/',
        'idle_slaves': 3,
        'disable_tinderbox_mail': False,
    },
    'nanojit': {
        'scripts_repo': 'http://hg.mozilla.org/build/tools',
        'idle_slaves': 3,
        'tinderbox_tree': 'Nanojit',
        'disable_tinderbox_mail': False,
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

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    # print build slave details
    host_info = {
        'production': SLAVES,
        'try': TRY_SLAVES,
    }

    if len(args) > 0:
        list_names = args
    else:
        list_names = host_info.keys()

    for list_name in list_names:
        for host_platform in host_info[list_name]:
            for host_name in host_info[list_name][host_platform]:
                print("%s,%s,%s" % (list_name, host_platform, host_name))

