from copy import deepcopy

SLAVES = {
    'linux': ['cb-seamonkey-linux-%02i' % x for x in [1,2,3]] +
             ['cn-sea-qm-centos5-%02i' % x for x in [1]] +
             ['cb-sea-linux-tbox'],
    'linux64': ['cb-seamonkey-linux64-%02i' % x for x in [1]],
    'win32': ['cb-seamonkey-win32-%02i' % x for x in [1,2,3]] +
             ['cn-sea-qm-win2k3-%02i' % x for x in [1]] +
             ['cb-sea-win32-tbox'],
    'macosx': ['cb-sea-miniosx%02i' % x for x in [1,2]],
    'macosx64': ['cb-sea-miniosx64-%02i' % x for x in [1,2,3]],
}


GLOBAL_VARS = {
    # It's a little unfortunate to have both of these but some things (HgPoller)
    # require an URL while other things (BuildSteps) require only the host.
    # Since they're both right here it shouldn't be
    # a problem to keep them in sync.
    'hgurl': 'http://hg.mozilla.org/',
    'hghost': 'hg.mozilla.org',
    'cvsroot': ':ext:seabld@cvs.mozilla.org:/cvsroot', #?
    'config_subdir': 'seamonkey',
    'irc_bot_name': 'sea-build-bot', #?
    'irc_bot_channels': ['mozbot'], #?
    'objdir': 'objdir',
    'objdir_unittests': 'objdir',
    'stage_username': 'seabld',
    'stage_base_path': '/home/ftp/pub/seamonkey',
    'stage_group': 'seamonkey',
    'stage_ssh_key': 'seabld_dsa',
    'symbol_server_path': '/mnt/netapp/breakpad/symbols_sea/',
    'symbol_server_post_upload_cmd': '/usr/local/bin/post-symbol-upload.py',
    'aus2_user': 'seabld',
    'aus2_ssh_key': 'seabld_dsa',
    'hg_username': 'seabld',
    'hg_ssh_key': '~seabld/.ssh/seabld_dsa',
    'graph_selector': '/server/collect.cgi',
    'compare_locales_repo_path': 'build/compare-locales',
    'compare_locales_tag': 'RELEASE_AUTOMATION',
    'default_build_space': 5,
    'default_l10n_space': 3,
    'default_clobber_time': 24*7, # 1 week
    'unittest_suites': [
        ('mochitests', dict(suite='mochitest-plain', chunkByDir=4, totalChunks=5)),
        ('mochitest-other', ['mochitest-chrome', 'mochitest-browser-chrome',
            'mochitest-a11y']),
        ('reftest', ['reftest']),
        ('crashtest', ['crashtest']),
        ('xpcshell', ['xpcshell']),
    ],
    # Unittest suites to run directly in the unittest build cycle
    'unittest_exec_xpcshell_suites': False,
    'unittest_exec_reftest_suites': False,
    'unittest_exec_mochi_suites': False,
    'unittest_exec_mozmill_suites': False,
    'geriatric_masters': [],
    'geriatric_branches': {},
    'platforms': {
        'linux': {},
        'linux64': {},
        'win32': {},
        'macosx64': {},
        'linux-debug': {},
        'macosx-debug': {},
        'macosx64-debug': {},
        'win32-debug': {},
    },
    'enable_shark': False,
    'enable_codecoverage': False,
    'enable_blocklist_update': False,
    'blocklist_update_on_closed_tree': False,
    'enable_nightly': True,

    # if true, this branch will get bundled and uploaded to ftp.m.o for users
    # to download and thereby accelerate their cloning
    'enable_weekly_bundle': False,

    'hash_type': 'sha512',
    'create_snippet': False,
    'create_partial': False,
    'create_partial_l10n': False,
    'l10n_modules': [
            'suite', 'editor/ui',
            'netwerk', 'dom', 'toolkit',
            'security/manager',
            'sync/services',
            ],
    'use_old_updater': False,
    'idle_timeout': 60*60*12,     # 12 hours

    # staging/production-dependent settings - all is production for us
    'config_repo_path': 'build/buildbot-configs',
    'buildbotcustom_repo_path': 'build/buildbotcustom',
    'stage_server': 'stage.mozilla.org',
    'aus2_host': 'aus2-community.mozilla.org',
    'download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/seamonkey',
    'graph_server': 'graphs-old.mozilla.org',
    'build_tools_repo_path': 'users/Callek_gmail.com/tools',
#    'build_tools_repo_path': 'build/tools',
    'base_clobber_url': 'http://cb-seamonkey-linuxmaster-01.mozilla.org/index.php',
    # List of talos masters to notify of new builds,
    # and if a failure to notify the talos master should result in a warning
    'talos_masters': [],
    # List of unittest masters to notify of new builds to test,
    # if a failure to notify the master should result in a warning,
    # and sendchange retry count before give up
    'unittest_masters': [('cb-seamonkey-linuxmaster-01.mozilla.org:9010', False, 5)],
    'weekly_tinderbox_tree': 'Testing',
    'l10n_tinderbox_tree': 'Mozilla-l10n',
    'tinderbox_tree': 'MozillaTest',
}

# shorthand, because these are used often
OBJDIR = GLOBAL_VARS['objdir']
SYMBOL_SERVER_PATH = GLOBAL_VARS['symbol_server_path']
SYMBOL_SERVER_POST_UPLOAD_CMD = GLOBAL_VARS['symbol_server_post_upload_cmd']

PLATFORM_VARS = {
        'linux': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'Linux %(branch)s',
            'mozconfig': 'linux/%(branch)s/nightly',
            'mozconfig_dep': 'linux/%(branch)s/dep',
            'profiled_build': False,
            'builds_before_reboot': None,
            'build_space': 8,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['linux'],
            'platform_objdir': OBJDIR,
            'update_platform': 'Linux_x86-gcc3',
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
                'SYMBOL_SERVER_USER': 'seabld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/seabld/.ssh/seabld_dsa",
                'TINDERBOX_OUTPUT': '1',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_UMASK': '002',
                'DISPLAY': ':2',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'linux64': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'Linux x86-64 %(branch)s',
            'mozconfig': 'linux64/%(branch)s/nightly',
            'mozconfig_dep': 'linux64/%(branch)s/dep',
            'profiled_build': False,
            'builds_before_reboot': None,
            'build_space': 6,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['linux64'],
            'platform_objdir': OBJDIR,
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
                'SYMBOL_SERVER_USER': 'seabld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/seabld/.ssh/seabld_dsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64',
                'TINDERBOX_OUTPUT': '1',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_UMASK': '002',
                'DISPLAY': ':2',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'macosx': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'OS X 10.5 %(branch)s',
            'mozconfig': 'macosx/%(branch)s/nightly',
            'mozconfig_dep': 'macosx/%(branch)s/dep',
            'profiled_build': False,
            'builds_before_reboot': None,
            'build_space': 8,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['macosx'],
            'platform_objdir': "%s/ppc" % OBJDIR,
            'update_platform': 'Darwin_Universal-gcc3',
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
                'SYMBOL_SERVER_USER': 'seabld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/Users/seabld/.ssh/seabld_dsa",
                'TINDERBOX_OUTPUT': '1',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'CHOWN_ROOT': '~/bin/chown_root',
                'CHOWN_REVERT': '~/bin/chown_revert',
                'MOZ_PKG_PLATFORM': 'mac',
                'LC_ALL': 'C',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'macosx64': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'OS X 10.6 %(branch)s',
            'mozconfig': 'macosx64/%(branch)s/nightly',
            'mozconfig_dep': 'macosx64/%(branch)s/dep',
            'profiled_build': False,
            'builds_before_reboot': None,
            'build_space': 8,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['macosx64'],
            'platform_objdir': "%s/i386" % OBJDIR,
            'update_platform': 'Darwin_x86_64-gcc3',
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
                'SYMBOL_SERVER_USER': 'seabld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/Users/seabld/.ssh/seabld_dsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'macosx64',
                'TINDERBOX_OUTPUT': '1',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'CHOWN_ROOT': '~/bin/chown_root',
                'CHOWN_REVERT': '~/bin/chown_revert',
                'LC_ALL': 'C',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'win32': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'WINNT 5.2 %(branch)s',
            'mozconfig': 'win32/%(branch)s/nightly',
            'mozconfig_dep': 'win32/%(branch)s/dep',
            'profiled_build': False,
            'builds_before_reboot': 25,
            'build_space': 9,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['win32'],
            'platform_objdir': OBJDIR,
            'mochitest_leak_threshold': 484,
            'crashtest_leak_threshold': 484,
            'update_platform': 'WINNT_x86-msvc',
            'enable_shared_checkouts': True,
            'env': {
                'CVS_RSH': 'ssh',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
                'SYMBOL_SERVER_USER': 'seabld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/c/Documents and Settings/seabld/.ssh/seabld_dsa",
                'TINDERBOX_OUTPUT': '1',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                # Source server support, bug 506702
                'PDBSTR_PATH': '/c/Program Files/Debugging Tools for Windows/srcsrv/pdbstr.exe',
                'HG_SHARE_BASE_DIR': 'e:/builds/hg-shared',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'linux-debug': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'Linux %(branch)s leak test',
            'mozconfig_dep': 'linux/%(branch)s/debug',
            'profiled_build': False,
            'builds_before_reboot': None,
            'download_symbols': True,
            'build_space': 7,
            'slaves': SLAVES['linux'],
            'platform_objdir': OBJDIR,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'DISPLAY': ':2',
                'LD_LIBRARY_PATH': '%s/mozilla/dist/bin' % OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_UMASK': '002',
            },
            'enable_unittests': True,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'macosx-debug': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'OS X 10.5 %(branch)s leak test',
            'mozconfig_dep': 'macosx/%(branch)s/debug',
            'profiled_build': False,
            'builds_before_reboot': None,
            'download_symbols': True,
            'build_space': 5,
            'slaves': SLAVES['macosx'],
            'platform_objdir': OBJDIR,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'LC_ALL': 'C',
            },
            'enable_unittests': True,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'macosx64-debug': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'OS X 10.6 %(branch)s leak test',
            'mozconfig_dep': 'macosx64/%(branch)s/debug',
            'profiled_build': False,
            'builds_before_reboot': None,
            'download_symbols': True,
            'build_space': 5,
            'slaves': SLAVES['macosx64'],
            'platform_objdir': OBJDIR,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'LC_ALL': 'C',
            },
            'enable_unittests': True,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
        'win32-debug': {
            'product_name': 'seamonkey',
            'app_name': 'suite',
            'brand_name': 'SeaMonkey',
            'base_name': 'WINNT 5.2 %(branch)s leak test',
            'mozconfig_dep': 'win32/%(branch)s/debug',
            'profiled_build': False,
            'builds_before_reboot': 25,
            'download_symbols': True,
            'build_space': 8,
            'slaves': SLAVES['win32'],
            'platform_objdir': OBJDIR,
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'MOZ_CRASHREPORTER_NO_REPORT': '1',
                'HG_SHARE_BASE_DIR': 'e:/builds/hg-shared',
            },
            'enable_unittests': True,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
        },
}

# All branches that are to be built MUST be listed here, along with their
# platforms (if different from the default set).
BRANCHES = {
    'comm-central-trunk': {},
    'comm-2.0': {},
    'comm-aurora': {},
    'comm-beta': {},
    'comm-release': {},
    'comm-1.9.1': {'platforms': {
            'linux': {},
            'linux64': {},
            'win32': {},
            'macosx': {},
        }},
}

# Copy global vars in first, then platform vars
for branch in BRANCHES.keys():
    for key, value in GLOBAL_VARS.items():
        # Don't override platforms if it's set
        if key == 'platforms' and 'platforms' in BRANCHES[branch]:
            continue
        BRANCHES[branch][key] = deepcopy(value)

    for platform, platform_config in PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

######## comm-central-trunk
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-central-trunk']['repo_path'] = 'comm-central'
BRANCHES['comm-central-trunk']['mozilla_repo_path'] = 'mozilla-central'
BRANCHES['comm-central-trunk']['l10n_repo_path'] = 'l10n-central'
BRANCHES['comm-central-trunk']['start_hour'] = [0]
BRANCHES['comm-central-trunk']['start_minute'] = [30]
BRANCHES['comm-central-trunk']['platforms']['macosx-debug']['opt_base_name'] = 'OS X 10.5 comm-central-trunk'
BRANCHES['comm-central-trunk']['enable_mac_a11y'] = True
BRANCHES['comm-central-trunk']['unittest_build_space'] = 6
BRANCHES['comm-central-trunk']['enable_blocklist_update'] = True
BRANCHES['comm-central-trunk']['blocklist_update_on_closed_tree'] = True
# And code coverage
BRANCHES['comm-central-trunk']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-central-trunk']['enable_l10n'] = True
BRANCHES['comm-central-trunk']['enable_l10n_onchange'] = True
BRANCHES['comm-central-trunk']['l10nNightlyUpdate'] = True
BRANCHES['comm-central-trunk']['l10n_platforms'] = ['linux','win32','macosx','macosx64']
BRANCHES['comm-central-trunk']['l10nDatedDirs'] = True
BRANCHES['comm-central-trunk']['l10n_tree'] = 'sea22x'
#make sure it has an ending slash
BRANCHES['comm-central-trunk']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-central-trunk-l10n/'
BRANCHES['comm-central-trunk']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-central-trunk'
BRANCHES['comm-central-trunk']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-central-trunk']['create_snippet'] = True
BRANCHES['comm-central-trunk']['create_partial'] = True
BRANCHES['comm-central-trunk']['create_partial_l10n'] = True
BRANCHES['comm-central-trunk']['aus2_base_upload_dir'] = '/opt/aus2/incoming/2/SeaMonkey/comm-central-trunk'
BRANCHES['comm-central-trunk']['aus2_base_upload_dir_l10n'] = '/opt/aus2/incoming/2/SeaMonkey/comm-central-trunk'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-central-trunk']['tinderbox_tree'] = 'SeaMonkey'
BRANCHES['comm-central-trunk']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey'

######## comm-aurora
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-aurora']['repo_path'] = 'releases/comm-aurora'
BRANCHES['comm-aurora']['mozilla_repo_path'] = 'releases/mozilla-aurora'
BRANCHES['comm-aurora']['l10n_repo_path'] = 'releases/l10n/mozilla-aurora'
BRANCHES['comm-aurora']['enable_nightly'] = True
BRANCHES['comm-aurora']['start_hour'] = [1]
BRANCHES['comm-aurora']['start_minute'] = [30]
BRANCHES['comm-aurora']['platforms']['macosx-debug']['opt_base_name'] = 'OS X 10.5 comm-aurora'
BRANCHES['comm-aurora']['enable_mac_a11y'] = True
BRANCHES['comm-aurora']['unittest_build_space'] = 6
BRANCHES['comm-aurora']['enable_blocklist_update'] = True
BRANCHES['comm-aurora']['blocklist_update_on_closed_tree'] = True
# And code coverage
BRANCHES['comm-aurora']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-aurora']['enable_l10n'] = True
BRANCHES['comm-aurora']['enable_l10n_onchange'] = True
BRANCHES['comm-aurora']['l10nNightlyUpdate'] = True
BRANCHES['comm-aurora']['l10n_platforms'] = ['linux','win32','macosx','macosx64']
BRANCHES['comm-aurora']['l10nDatedDirs'] = True
BRANCHES['comm-aurora']['l10n_tree'] = 'sea_aurora'
#make sure it has an ending slash
BRANCHES['comm-aurora']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-aurora-l10n/'
BRANCHES['comm-aurora']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-aurora'
BRANCHES['comm-aurora']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-aurora']['create_snippet'] = True
BRANCHES['comm-aurora']['create_partial'] = True
BRANCHES['comm-aurora']['create_partial_l10n'] = True
BRANCHES['comm-aurora']['aus2_base_upload_dir'] = '/opt/aus2/incoming/2/SeaMonkey/comm-aurora'
BRANCHES['comm-aurora']['aus2_base_upload_dir_l10n'] = '/opt/aus2/incoming/2/SeaMonkey/comm-aurora'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-aurora']['tinderbox_tree'] = 'SeaMonkey-Aurora'
BRANCHES['comm-aurora']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey-Aurora'

######## comm-beta
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-beta']['repo_path'] = 'releases/comm-beta'
BRANCHES['comm-beta']['mozilla_repo_path'] = 'releases/mozilla-beta'
BRANCHES['comm-beta']['l10n_repo_path'] = 'releases/l10n/mozilla-beta'
BRANCHES['comm-beta']['enable_nightly'] = False
BRANCHES['comm-beta']['start_hour'] = [0]
BRANCHES['comm-beta']['start_minute'] = [30]
BRANCHES['comm-beta']['platforms']['macosx-debug']['opt_base_name'] = 'OS X 10.5 comm-beta'
BRANCHES['comm-beta']['enable_mac_a11y'] = True
BRANCHES['comm-beta']['unittest_build_space'] = 6
BRANCHES['comm-beta']['enable_blocklist_update'] = False # for now
BRANCHES['comm-beta']['blocklist_update_on_closed_tree'] = True
# And code coverage
BRANCHES['comm-beta']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-beta']['enable_l10n'] = False
BRANCHES['comm-beta']['enable_l10n_onchange'] = True
BRANCHES['comm-beta']['l10nNightlyUpdate'] = True
BRANCHES['comm-beta']['l10n_platforms'] = ['linux','win32','macosx','macosx64']
BRANCHES['comm-beta']['l10nDatedDirs'] = True
BRANCHES['comm-beta']['l10n_tree'] = 'sea_beta'
#make sure it has an ending slash
BRANCHES['comm-beta']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-beta-l10n/'
BRANCHES['comm-beta']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-beta'
BRANCHES['comm-beta']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-beta']['create_snippet'] = True
BRANCHES['comm-beta']['create_partial'] = True
BRANCHES['comm-beta']['create_partial_l10n'] = True
BRANCHES['comm-beta']['aus2_base_upload_dir'] = '/opt/aus2/incoming/2/SeaMonkey/comm-beta'
BRANCHES['comm-beta']['aus2_base_upload_dir_l10n'] = '/opt/aus2/incoming/2/SeaMonkey/comm-beta'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-beta']['tinderbox_tree'] = 'SeaMonkey-Beta'
BRANCHES['comm-beta']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey-Beta'

######## comm-release
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-release']['repo_path'] = 'releases/comm-release'
BRANCHES['comm-release']['mozilla_repo_path'] = 'releases/mozilla-release'
BRANCHES['comm-release']['l10n_repo_path'] = 'releases/l10n/mozilla-release'
BRANCHES['comm-release']['enable_nightly'] = False
BRANCHES['comm-release']['start_hour'] = [0]
BRANCHES['comm-release']['start_minute'] = [30]
BRANCHES['comm-release']['platforms']['macosx-debug']['opt_base_name'] = 'OS X 10.5 comm-release'
BRANCHES['comm-release']['enable_mac_a11y'] = True
BRANCHES['comm-release']['unittest_build_space'] = 6
BRANCHES['comm-release']['enable_blocklist_update'] = False # for now
BRANCHES['comm-release']['blocklist_update_on_closed_tree'] = True
# And code coverage
BRANCHES['comm-release']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-release']['enable_l10n'] = False
BRANCHES['comm-release']['enable_l10n_onchange'] = True
BRANCHES['comm-release']['l10nNightlyUpdate'] = True
BRANCHES['comm-release']['l10n_platforms'] = ['linux','win32','macosx','macosx64']
BRANCHES['comm-release']['l10nDatedDirs'] = True
BRANCHES['comm-release']['l10n_tree'] = 'sea_release'
#make sure it has an ending slash
BRANCHES['comm-release']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-release-l10n/'
BRANCHES['comm-release']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-release'
BRANCHES['comm-release']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-release']['create_snippet'] = True
BRANCHES['comm-release']['create_partial'] = True
BRANCHES['comm-release']['create_partial_l10n'] = True
BRANCHES['comm-release']['aus2_base_upload_dir'] = '/opt/aus2/incoming/2/SeaMonkey/comm-release'
BRANCHES['comm-release']['aus2_base_upload_dir_l10n'] = '/opt/aus2/incoming/2/SeaMonkey/comm-release'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-release']['tinderbox_tree'] = 'SeaMonkey-Release'
BRANCHES['comm-release']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey-Release'

######## comm-2.0
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-2.0']['repo_path'] = 'releases/comm-2.0'
BRANCHES['comm-2.0']['mozilla_repo_path'] = 'releases/mozilla-2.0'
BRANCHES['comm-2.0']['l10n_repo_path'] = 'releases/l10n-mozilla-2.0'
BRANCHES['comm-2.0']['enable_nightly'] = False
BRANCHES['comm-2.0']['start_hour'] = [1]
BRANCHES['comm-2.0']['start_minute'] = [0]
BRANCHES['comm-2.0']['platforms']['macosx-debug']['opt_base_name'] = 'OS X 10.5 comm-2.0'
BRANCHES['comm-2.0']['enable_mac_a11y'] = True
BRANCHES['comm-2.0']['unittest_build_space'] = 6
# We only need one c-c blocklist update.
BRANCHES['comm-2.0']['enable_blocklist_update'] = False
BRANCHES['comm-2.0']['blocklist_update_on_closed_tree'] = False
# And code coverage
BRANCHES['comm-2.0']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-2.0']['enable_l10n'] = True
BRANCHES['comm-2.0']['enable_l10n_onchange'] = False
BRANCHES['comm-2.0']['l10nNightlyUpdate'] = True
BRANCHES['comm-2.0']['l10n_platforms'] = ['linux','win32','macosx','macosx64']
BRANCHES['comm-2.0']['l10nDatedDirs'] = True
BRANCHES['comm-2.0']['l10n_tree'] = 'sea21x'
#make sure it has an ending slash
BRANCHES['comm-2.0']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-2.0-l10n/'
BRANCHES['comm-2.0']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-2.0'
BRANCHES['comm-2.0']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-2.0']['create_snippet'] = True
BRANCHES['comm-2.0']['create_partial'] = True
BRANCHES['comm-2.0']['create_partial_l10n'] = True
BRANCHES['comm-2.0']['aus2_base_upload_dir'] = '/opt/aus2/incoming/2/SeaMonkey/comm-2.0'
BRANCHES['comm-2.0']['aus2_base_upload_dir_l10n'] = '/opt/aus2/incoming/2/SeaMonkey/comm-2.0'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-2.0']['tinderbox_tree'] = 'SeaMonkey2.1'
BRANCHES['comm-2.0']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey2.1'

######## comm-1.9.1
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['comm-1.9.1']['repo_path'] = 'releases/comm-1.9.1'
BRANCHES['comm-1.9.1']['mozilla_repo_path'] = 'releases/mozilla-1.9.1'
BRANCHES['comm-1.9.1']['l10n_repo_path'] = 'releases/l10n-mozilla-1.9.1'
BRANCHES['comm-1.9.1']['enable_nightly'] = False
BRANCHES['comm-1.9.1']['start_hour'] = [0]
BRANCHES['comm-1.9.1']['start_minute'] = [0]
BRANCHES['comm-1.9.1']['use_old_updater'] = True
BRANCHES['comm-1.9.1']['unittest_suites'] = [
    ('mochitests', ['mochitest-plain']),
    ('mochitest-other', ['mochitest-chrome', 'mochitest-browser-chrome',
        'mochitest-a11y']),
    ('reftest', ['reftest']),
    ('crashtest', ['crashtest']),
]
BRANCHES['comm-1.9.1']['platforms']['linux']['enable_unittests'] = True
BRANCHES['comm-1.9.1']['platforms']['linux']['enable_opt_unittests'] = False
BRANCHES['comm-1.9.1']['platforms']['linux']['enable_checktests'] = False
BRANCHES['comm-1.9.1']['platforms']['linux']['packageTests'] = False
BRANCHES['comm-1.9.1']['platforms']['linux64']['enable_opt_unittests'] = False
BRANCHES['comm-1.9.1']['platforms']['linux64']['enable_checktests'] = False
BRANCHES['comm-1.9.1']['platforms']['linux64']['packageTests'] = False
BRANCHES['comm-1.9.1']['platforms']['macosx']['enable_unittests'] = True
BRANCHES['comm-1.9.1']['platforms']['macosx']['enable_opt_unittests'] = False
BRANCHES['comm-1.9.1']['platforms']['macosx']['enable_checktests'] = False
BRANCHES['comm-1.9.1']['platforms']['macosx']['packageTests'] = False
BRANCHES['comm-1.9.1']['platforms']['win32']['enable_unittests'] = True
BRANCHES['comm-1.9.1']['platforms']['win32']['enable_opt_unittests'] = False
BRANCHES['comm-1.9.1']['platforms']['win32']['enable_checktests'] = False
BRANCHES['comm-1.9.1']['platforms']['win32']['packageTests'] = False
BRANCHES['comm-1.9.1']['unittest_exec_xpcshell_suites'] = True
BRANCHES['comm-1.9.1']['enable_mac_a11y'] = False
BRANCHES['comm-1.9.1']['unittest_build_space'] = 6
# And code coverage
BRANCHES['comm-1.9.1']['enable_codecoverage'] = False
# L10n configuration
BRANCHES['comm-1.9.1']['enable_l10n'] = True
BRANCHES['comm-1.9.1']['enable_l10n_onchange'] = False
BRANCHES['comm-1.9.1']['l10nNightlyUpdate'] = False
BRANCHES['comm-1.9.1']['l10n_platforms'] = ['linux','win32','macosx']
BRANCHES['comm-1.9.1']['l10nDatedDirs'] = False
BRANCHES['comm-1.9.1']['l10n_tree'] = 'sea20x'
#make sure it has an ending slash
BRANCHES['comm-1.9.1']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/seamonkey/nightly/latest-comm-1.9.1-l10n/'
BRANCHES['comm-1.9.1']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-comm-1.9.1'
BRANCHES['comm-1.9.1']['allLocalesFile'] = 'suite/locales/all-locales'
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-1.9.1']['create_snippet'] = True
BRANCHES['comm-1.9.1']['create_partial'] = True
BRANCHES['comm-1.9.1']['aus2_base_upload_dir'] = '/opt/aus2/build/0/SeaMonkey/comm-1.9.1'
BRANCHES['comm-1.9.1']['aus2_base_upload_dir_l10n'] = '/opt/aus2/build/0/SeaMonkey/comm-1.9.1'
# staging/production-dependent settings - all is production for us
BRANCHES['comm-1.9.1']['tinderbox_tree'] = 'SeaMonkey2.0'
BRANCHES['comm-1.9.1']['packaged_unittest_tinderbox_tree'] = 'SeaMonkey2.0'
