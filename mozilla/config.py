from copy import deepcopy

import project_branches
reload(project_branches)
from project_branches import PROJECT_BRANCHES, ACTIVE_PROJECT_BRANCHES

import localconfig
reload(localconfig)
from localconfig import SLAVES, TRY_SLAVES

import master_common
reload(master_common)
from master_common import setMainFirefoxVersions, items_before, items_at_least

GLOBAL_VARS = {
    # It's a little unfortunate to have both of these but some things (HgPoller)
    # require an URL while other things (BuildSteps) require only the host.
    # Since they're both right here it shouldn't be
    # a problem to keep them in sync.
    'hgurl': 'https://hg.mozilla.org/',
    'hghost': 'hg.mozilla.org',
    'objdir': 'obj-firefox',
    'objdir_unittests': 'objdir',
    'stage_username': 'ffxbld',
    'stage_base_path': '/home/ftp/pub',
    'stage_group': None,
    'stage_ssh_key': 'ffxbld_rsa',
    'symbol_server_path': '/mnt/netapp/breakpad/symbols_ffx/',
    'symbol_server_post_upload_cmd': '/usr/local/bin/post-symbol-upload.py',
    'symbol_server_mobile_path': '/mnt/netapp/breakpad/symbols_mob/',
    'balrog_credentials_file': 'BuildSlaves.py',
    'hg_username': 'ffxbld',
    'hg_ssh_key': '~cltbld/.ssh/ffxbld_rsa',
    'graph_selector': '/server/collect.cgi',
    'compare_locales_repo_path': 'build/compare-locales',
    'compare_locales_tag': 'RELEASE_AUTOMATION',
    'mozharness_repo_path': 'build/mozharness',
    'mozharness_tag': 'production',
    'script_repo_manifest': 'https://hg.mozilla.org/%(repo_path)s/raw-file/%(revision)s/' + \
                            'testing/mozharness/mozharness.json',
    # mozharness_archiver_repo_path tells the factory to use a copy of mozharness from within the
    #  gecko tree and also allows us to overwrite which gecko repo to use. Useful for platforms
    # like Thunderbird
    'mozharness_archiver_repo_path': '%(repo_path)s',
    'use_mozharness_repo_cache': True,
    'multi_locale_merge': True,
    'default_build_space': 5,
    'default_l10n_space': 3,
    'default_clobber_time': 24*7,  # 1 week
    'unittest_suites': [
        ('mochitest', dict(suite='mochitest-plain', chunkByDir=4, totalChunks=5)),
        ('mochitest-browser-chrome', ['mochitest-browser-chrome']),
        ('mochitest-other', ['mochitest-chrome', 'mochitest-a11y', 'mochitest-ipcplugins']),
        ('reftest', ['reftest']),
        ('crashtest', ['crashtest']),
        ('xpcshell', ['xpcshell']),
        ('jsreftest', ['jsreftest']),
    ],
    'platforms': {
        'linux': {},
        'linux64': {},
        'win32': {},
        'win64': {},
        'macosx64': {},
        'linux-debug': {},
        'linux64-br-haz': {},
        'linux64-debug': {},
        'linux64-asan': {},
        'linux64-asan-debug': {},
        'linux64-st-an-debug': {},
        'linux64-av': {},
        'macosx64-debug': {},
        'macosx64-st-an-debug': {},
        'win32-debug': {},
        'win64-debug': {},
        'android-api-9': {},
        'android-api-11': {},
        'android-x86': {},
        'android-api-11-debug': {},
        'android-api-9-debug': {},
    },
    'pgo_strategy': None,
    'pgo_platforms': ('linux', 'linux64', 'win32', 'win64',),
    'periodic_start_hours': range(0, 24, 6),
    'enable_blocklist_update': False,
    'enable_hsts_update': False,
    'enable_hpkp_update': False,
    'file_update_on_closed_tree': False,
    'file_update_set_approval': True,
    'enable_nightly': True,
    'enabled_products': ['firefox', 'mobile'],
    'enable_valgrind': True,
    'valgrind_platforms': ('linux64',),

    # List of keys in BRANCH_PROJECTS that will be activated for the BRANCH
    'branch_projects': ['spidermonkey_tier_1'],

    # if true, this branch will get bundled and uploaded to ftp.m.o for users
    # to download and thereby accelerate their cloning
    'enable_weekly_bundle': False,

    'hash_type': 'sha512',
    'updates_enabled': False,
    'create_partial': False,
    'create_partial_l10n': False,
    'l10n_modules': [
            'browser',
            'dom',
            'extensions/reporter',
            'extensions/spellcheck',
            'netwerk',
            'other-licenses/branding/firefox',
            'security/manager',
            'services/sync',
            'toolkit',
            ],
    'use_old_updater': False,
    # rather than repeat these options in each of these options in
    # every platform, let's define the arguments here and when we want to
    # turn an existing platform into say a 'nightly' version, add the options
    #  from here and append it to 'extra_options'
    'mozharness_desktop_extra_options': {
        'nightly': ['--enable-nightly'],
        'pgo': ['--enable-pgo'],
    },
    # list platforms with mozharness l10n repacks enabled.
    # mozharness repacks will be enabled per branch

}
GLOBAL_VARS.update(localconfig.GLOBAL_VARS.copy())

# shorthand, because these are used often
OBJDIR = GLOBAL_VARS['objdir']
SYMBOL_SERVER_PATH = GLOBAL_VARS['symbol_server_path']
SYMBOL_SERVER_POST_UPLOAD_CMD = GLOBAL_VARS['symbol_server_post_upload_cmd']
SYMBOL_SERVER_MOBILE_PATH = GLOBAL_VARS['symbol_server_mobile_path']

GLOBAL_ENV = {
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
    'TINDERBOX_OUTPUT': '1',
    'MOZ_AUTOMATION': '1',
}

PLATFORM_VARS = {
        'linux': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_32_builds.py',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'mozharness_desktop_l10n': {
                'capable': True,
                'scriptName': 'scripts/desktop_l10n.py',
                'l10n_chunks': 6,
                'use_credentials_file': True,
                'script_timeout': 1800,
                'script_maxtime': 2 * 3600,
            },
            'dep_signing_servers': 'dep-signing',
            'base_name': 'Linux %(branch)s',
            'product_name': 'firefox',
            'unittest_platform': 'linux-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'mozconfig': 'linux/%(branch)s/nightly',
            'src_mozconfig': 'browser/config/mozconfigs/linux32/nightly',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': True,
            'download_symbols': True,
            'packageTests': True,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux',
            'update_platform': 'Linux_x86-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_checktests': True,
            'enable_build_analysis': True,
            'talos_masters': None,
            'test_pretty_names': False,
            'l10n_check_test': True,
            'nightly_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux32/releng.manifest',
            'tooltool_script': ['/builds/tooltool.py'],
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static.i686', 'libstdc++-static.i686', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel.i686', 'libnotify-devel.i686', 'yasm',
                        'alsa-lib-devel.i686', 'libcurl-devel.i686',
                        'wireless-tools-devel.i686', 'libX11-devel.i686',
                        'libXt-devel.i686', 'mesa-libGL-devel.i686',
                        'gnome-vfs2-devel.i686', 'GConf2-devel.i686', 'wget',
                        'mpfr',  # required for system compiler
                        'xorg-x11-font*',  # fonts required for PGO
                        'imake',  # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache',  # <-- from releng repo
                        'valgrind',
                        'pulseaudio-libs-devel.i686',
                        'gstreamer-devel.i686', 'gstreamer-plugins-base-devel.i686',
                        # Packages already installed in the mock environment, as x86_64
                        # packages.
                        'glibc-devel.i686', 'libgcc.i686', 'libstdc++-devel.i686',
                        # yum likes to install .x86_64 -devel packages that satisfy .i686
                        # -devel packages dependencies. So manually install the dependencies
                        # of the above packages.
                        'ORBit2-devel.i686', 'atk-devel.i686', 'cairo-devel.i686',
                        'check-devel.i686', 'dbus-devel.i686', 'dbus-glib-devel.i686',
                        'fontconfig-devel.i686', 'glib2-devel.i686',
                        'hal-devel.i686', 'libICE-devel.i686', 'libIDL-devel.i686',
                        'libSM-devel.i686', 'libXau-devel.i686', 'libXcomposite-devel.i686',
                        'libXcursor-devel.i686', 'libXdamage-devel.i686', 'libXdmcp-devel.i686',
                        'libXext-devel.i686', 'libXfixes-devel.i686', 'libXft-devel.i686',
                        'libXi-devel.i686', 'libXinerama-devel.i686', 'libXrandr-devel.i686',
                        'libXrender-devel.i686', 'libXxf86vm-devel.i686', 'libdrm-devel.i686',
                        'libidn-devel.i686', 'libpng-devel.i686', 'libxcb-devel.i686',
                        'libxml2-devel.i686', 'pango-devel.i686', 'perl-devel.i686',
                        'pixman-devel.i686', 'zlib-devel.i686',
                        # Freetype packages need to be installed be version, because a newer
                        # version is available, but we don't want it for Firefox builds.
                        'freetype-2.3.11-6.el6_1.8.i686', 'freetype-devel-2.3.11-6.el6_1.8.i686',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/tools/tooltool.py', '/builds/tooltool.py'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
        },
        'linux64': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'mozharness_desktop_l10n': {
                'capable': True,
                'scriptName': 'scripts/desktop_l10n.py',
                'l10n_chunks': 6,
                'use_credentials_file': True,
                'script_timeout': 1800,
                'script_maxtime': 2 * 3600,
            },
            'product_name': 'firefox',
            'unittest_platform': 'linux64-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s',
            'mozconfig': 'linux64/%(branch)s/nightly',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/nightly',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 14,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64',
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_checktests': True,
            'enable_build_analysis': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'test_pretty_names': False,
            'l10n_check_test': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/releng.manifest',
            'tooltool_script': ['/builds/tooltool.py'],
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind', 'dbus-x11',
                        'pulseaudio-libs-devel',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/tools/tooltool.py', '/builds/tooltool.py'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
        },
        'linux64-av': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'use_mock': False,
            'stage_product': None,
            'slaves': SLAVES['linux64-av'],
        },
        'linux64-asan': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'asan',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'product_name': 'firefox',
            'unittest_platform': 'linux64-asan-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s asan',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/nightly-asan',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': False,
            'download_symbols': False,
            'packageTests': True,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-asan',
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64-asan',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'enable_build_analysis': False,
            'updates_enabled': False,
            'create_partial': False,
            'test_pretty_names': False,
            'l10n_check_test': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/asan.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind',
                        'pulseaudio-libs-devel',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            # The status of this build doesn't affect the last good revision
            # algorithm for nightlies
            'consider_for_nightly': False,
        },
        'linux64-tsan': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'tsan',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'product_name': 'firefox',
            'unittest_platform': 'linux64-tsan-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s tsan',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/opt-tsan',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': False,
            'try_by_default': False,
            'download_symbols': False,
            'packageTests': True,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-tsan',
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64-tsan',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_opt_unittests': True,
            'enable_checktests': True,
            'enable_build_analysis': False,
            'updates_enabled': False,
            'create_partial': False,
            'test_pretty_names': False,
            'l10n_check_test': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/tsan.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind',
                        'pulseaudio-libs-devel',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            # The status of this build doesn't affect the last good revision
            # algorithm for nightlies
            'consider_for_nightly': False,
        },
        'linux64-asan-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'asan-and-debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': True,
            'product_name': 'firefox',
            'unittest_platform': 'linux64-asan-debug',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s debug asan',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/debug-asan',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': False,
            'download_symbols': False,
            'packageTests': True,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-asan-debug',
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64-asan-debug',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'enable_build_analysis': False,
            'updates_enabled': False,
            'create_partial': False,
            'test_pretty_names': False,
            'l10n_check_test': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/asan.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind',
                        'pulseaudio-libs-devel',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            # The status of this build doesn't affect the last good revision
            # algorithm for nightlies
            'consider_for_nightly': False,
        },
        'linux64-st-an-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'stat-and-debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'unittest_platform': 'linux64-st-an-debug',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s debug static analysis',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/debug-static-analysis-clang',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': False,
            'download_symbols': False,
            'packageTests': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-st-an-debug',
            'update_platform': 'Linux_x86_64-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64-st-an-debug',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_opt_unittests': False,
            'enable_checktests': False,
            'enable_build_analysis': False,
            'updates_enabled': False,
            'create_partial': False,
            'test_pretty_names': False,
            'l10n_check_test': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/clang.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind',
                        'pulseaudio-libs-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            # The status of this build doesn't affect the last good revision
            # algorithm for nightlies
            'consider_for_nightly': False,
        },
        'linux64-sh-haz': {
            'mozharness_config': {
                'script_name': 'scripts/spidermonkey_build.py',
                'extra_args': [
                    '--config-file', 'hazards/build_shell.py',
                    '--config-file', 'hazards/common.py',
                ],
                'mozharness_repo_cache': '/tools/checkouts/mozharness',
                'tools_repo_cache': '/tools/checkouts/build-tools',
            },
            'env': {
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
            },
            'stage_product': 'firefox',
            'product_name': 'firefox',
            'base_name': '%(platform)s_%(branch)s',
            'slaves': SLAVES['mock'],
            'try_by_default': False,
            'consider_for_nightly': False,
            'mock_target': 'mozilla-centos6-x86_64',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
        },
        'linux64-br-haz': {
            'mozharness_config': {
                'script_name': 'scripts/spidermonkey_build.py',
                'extra_args': [
                    '--config-file', 'hazards/build_browser.py',
                    '--config-file', 'hazards/common.py',
                ],
                'mozharness_repo_cache': '/tools/checkouts/mozharness',
                'tools_repo_cache': '/tools/checkouts/build-tools',
            },

            'env': {
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
            },
            'stage_product': 'firefox',
            'product_name': 'firefox',
            'base_name': '%(platform)s_%(branch)s',
            'slaves': SLAVES['mock'],
            'try_by_default': True,
            'consider_for_nightly': False,
            'mock_target': 'mozilla-centos6-x86_64',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
        },
        'linux64-cc': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': ['scripts/external_tools/count_and_reboot.py',
                               '-f', '../reboot_count.txt', '-n', '1', '-z'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'code-coverage',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'consider_for_nightly': False,
            'enable_nightly': False,
            'enable_opt_unittests': True,
            'try_by_default': False,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,

            'product_name': 'firefox',
            'unittest_platform': 'linux64-cc-opt',
            'app_name': 'browser',
            'base_name': 'Linux x86-64 Code Coverage %(branch)s',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/code-coverage',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-cc',
            'update_platform': 'Linux_x86_64-gcc3',
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'linux64',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_checktests': True,
            'enable_build_analysis': False,
            'test_pretty_names': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/releng.manifest',
            'tooltool_script': ['/builds/tooltool.py'],
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'valgrind', 'dbus-x11',
                        'pulseaudio-libs-devel',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/tools/tooltool.py', '/builds/tooltool.py'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
        },
        'macosx64': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': ['scripts/external_tools/count_and_reboot.py',
                               '-f', '../reboot_count.txt', '-n', '1', '-z'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_mac_64_builds.py',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'mozharness_desktop_l10n': {
                'capable': True,
                'scriptName': 'scripts/desktop_l10n.py',
                'l10n_chunks': 8,
                'use_credentials_file': True,
                'script_timeout': 1800,
                'script_maxtime': 3 * 3600,
            },

            'product_name': 'firefox',
            'unittest_platform': 'macosx64-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'OS X 10.7 %(branch)s',
            'mozconfig': 'macosx64/%(branch)s/nightly',
            'src_mozconfig': 'browser/config/mozconfigs/macosx-universal/nightly',
            'packageTests': True,
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': True,
            'download_symbols': True,
            'slaves': SLAVES['macosx64-lion'],
            'platform_objdir': "%s/i386" % OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'macosx64',
            'update_platform': 'Darwin_x86_64-gcc3',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/Users/cltbld/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'macosx64',
                'CHOWN_ROOT': '~/bin/chown_root',
                'CHOWN_REVERT': '~/bin/chown_revert',
                'LC_ALL': 'C',
                'PATH': '/tools/python/bin:/tools/buildbot/bin:/opt/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'test_pretty_names': False,
            # These refer to items in passwords.secrets
            # nightly_signing_servers defaults to dep-signing because we don't want
            # random new branches to accidentally use nightly-signing, which signs
            # with valid keys. Any branch that needs to be signed with these keys
            # must be overridden explicitly.
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/macosx64/releng.manifest',
            'enable_ccache': True,
        },
        'win32': {
            'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
            'reboot_command': [
                'c:/mozilla-build/python27/python', '-u',
                'scripts/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt','-n', '1', '-z'
            ],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_windows_32_builds.py',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(7.5 * 3600),
            },
            'mozharness_desktop_l10n': {
                'capable': True,
                'scriptName': 'scripts/desktop_l10n.py',
                'l10n_chunks': 6,
                'use_credentials_file': True,
                'script_timeout': 2 * 3600,
                'script_maxtime': 3 * 3600,
            },

            'product_name': 'firefox',
            'unittest_platform': 'win32-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'WINNT 5.2 %(branch)s',
            'mozconfig': 'win32/%(branch)s/nightly',
            'src_mozconfig': 'browser/config/mozconfigs/win32/nightly',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 12,
            'upload_symbols': True,
            'download_symbols': True,
            'enable_installer': True,
            'packageTests': True,
            'slaves': SLAVES['win64-rev2'],
            'l10n_slaves': SLAVES['win64-rev2'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'win32',
            'mochitest_leak_threshold': 484,
            'crashtest_leak_threshold': 484,
            'update_platform': 'WINNT_x86-msvc',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/c/Users/cltbld/.ssh/ffxbld_rsa",
                'PDBSTR_PATH': '/c/Program Files (x86)/Windows Kits/8.0/Debuggers/x64/srcsrv/pdbstr.exe',
                'HG_SHARE_BASE_DIR': 'c:/builds/hg-shared',
                'BINSCOPE': 'C:\Program Files (x86)\Microsoft\SDL BinScope\BinScope.exe',
                'PATH': "${MOZILLABUILD}nsis-3.0b1;${MOZILLABUILD}nsis-2.46u;${MOZILLABUILD}python27;${MOZILLABUILD}buildbotve\\scripts;${PATH}",
            },
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'test_pretty_names': False,
            'l10n_check_test': True,
            # These refer to items in passwords.secrets
            # nightly_signing_servers defaults to dep-signing because we don't want
            # random new branches to accidentally use nightly-signing, which signs
            # with valid keys. Any branch that needs to be signed with these keys
            # must be overridden explicitly.
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/win32/releng.manifest',
            'tooltool_script': ['python', '/c/mozilla-build/tooltool.py'],
        },
        'win64': {
            'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_windows_64_builds.py',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(7.5 * 3600),
            },
            'mozharness_desktop_l10n': {
                'capable': True,
                'scriptName': 'scripts/desktop_l10n.py',
                'l10n_chunks': 6,
                'use_credentials_file': True,
                'script_timeout': 2 * 3600,
                'script_maxtime': 3 * 3600,
            },
            'reboot_command': [
                'c:/mozilla-build/python27/python', '-u',
                'scripts/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt','-n', '1', '-z'
            ],

            'product_name': 'firefox',
            'unittest_platform': 'win64-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'WINNT 6.1 x86-64 %(branch)s',
            'src_mozconfig': 'browser/config/mozconfigs/win64/nightly',
            'mozconfig': 'win64/%(branch)s/nightly',
            'profiled_build': True,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 14,
            'upload_symbols': True,
            'enable_installer': True,
            'packageTests': True,
            'try_by_default': True,
            'slaves': SLAVES['win64-rev2'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'win64',
            'mochitest_leak_threshold': 484,
            'crashtest_leak_threshold': 484,
            'update_platform': 'WINNT_x86_64-msvc',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_PATH,
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SYMBOL_SERVER_SSH_KEY': "/c/Users/cltbld/.ssh/ffxbld_rsa",
                'MOZ_SYMBOLS_EXTRA_BUILDID': 'win64',
                'PDBSTR_PATH': '/c/Program Files (x86)/Windows Kits/8.0/Debuggers/x64/srcsrv/pdbstr.exe',
                'HG_SHARE_BASE_DIR': 'c:/builds/hg-shared',
                'PATH': "${MOZILLABUILD}python27;${MOZILLABUILD}buildbotve\\scripts;${PATH}",
            },
            'enable_opt_unittests': False,
            'enable_checktests': True,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'test_pretty_names': True,
            'l10n_check_test': True,
            # These refer to items in passwords.secrets
            # nightly_signing_servers defaults to dep-signing because we don't want
            # random new branches to accidentally use nightly-signing, which signs
            # with valid keys. Any branch that needs to be signed with these keys
            # must be overridden explicitly.
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            # The status of this build doesn't affect the last good revision
            # algorithm for nightlies
            'consider_for_nightly': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/win64/releng.manifest',
            'tooltool_script': ['python', '/c/mozilla-build/tooltool.py'],
        },
        'linux-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_32_builds.py',
                    '--custom-build-variant-cfg', 'debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux %(branch)s leak test',
            'mozconfig': 'linux/%(branch)s/debug',
            'src_mozconfig': 'browser/config/mozconfigs/linux32/debug',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': True,
            'packageTests': True,
            'build_space': 15,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux-debug',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'DISPLAY': ':2',
                'LD_LIBRARY_PATH': '%s/dist/bin' % OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_unittests': False,
            'enable_checktests': True,
            'talos_masters': None,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux32/releng.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static.i686', 'libstdc++-static.i686',
                        'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel.i686', 'libnotify-devel.i686', 'yasm',
                        'alsa-lib-devel.i686', 'libcurl-devel.i686',
                        'wireless-tools-devel.i686', 'libX11-devel.i686',
                        'libXt-devel.i686', 'mesa-libGL-devel.i686',
                        'gnome-vfs2-devel.i686', 'GConf2-devel.i686', 'wget',
                        'mpfr',  # required for system compiler
                        'xorg-x11-font*',  # fonts required for PGO
                        'imake',  # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache',  # <-- from releng repj
                        'valgrind',
                        'pulseaudio-libs-devel.i686',
                        'gstreamer-devel.i686', 'gstreamer-plugins-base-devel.i686',
                        # Packages already installed in the mock environment,
                        # as x86_64 packages.
                        'glibc-devel.i686', 'libgcc.i686', 'libstdc++-devel.i686',
                        # yum likes to install .x86_64 -devel packages that satisfy .i686
                        # -devel packages dependencies. So manually install the
                        # dependencies of the above packages.
                        'ORBit2-devel.i686', 'atk-devel.i686', 'cairo-devel.i686',
                        'check-devel.i686', 'dbus-devel.i686', 'dbus-glib-devel.i686',
                        'fontconfig-devel.i686', 'glib2-devel.i686',
                        'hal-devel.i686', 'libICE-devel.i686', 'libIDL-devel.i686',
                        'libSM-devel.i686', 'libXau-devel.i686', 'libXcomposite-devel.i686',
                        'libXcursor-devel.i686', 'libXdamage-devel.i686',
                        'libXdmcp-devel.i686', 'libXext-devel.i686',
                        'libXfixes-devel.i686', 'libXft-devel.i686',
                        'libXi-devel.i686', 'libXinerama-devel.i686', 'libXrandr-devel.i686',
                        'libXrender-devel.i686', 'libXxf86vm-devel.i686', 'libdrm-devel.i686',
                        'libidn-devel.i686', 'libpng-devel.i686', 'libxcb-devel.i686',
                        'libxml2-devel.i686', 'pango-devel.i686', 'perl-devel.i686',
                        'pixman-devel.i686', 'zlib-devel.i686',
                        'freetype-2.3.11-6.el6_1.8.i686', 'freetype-devel-2.3.11-6.el6_1.8.i686',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
        },
        'linux64-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': [
                '/tools/checkouts/mozharness/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt', '-n', '1', '-z'
            ],
            'mozharness_repo_cache': '/tools/checkouts/mozharness',
            'tools_repo_cache': '/tools/checkouts/build-tools',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_linux_64_builds.py',
                    '--custom-build-variant-cfg', 'debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Linux x86-64 %(branch)s leak test',
            'mozconfig': 'linux64/%(branch)s/debug',
            'src_mozconfig': 'browser/config/mozconfigs/linux64/debug',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': False,
            'packageTests': True,
            'build_space': 14,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'linux64-debug',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'DISPLAY': ':2',
                'LD_LIBRARY_PATH': '%s/dist/bin' % OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin',
            },
            'enable_unittests': False,
            'enable_checktests': True,
            'talos_masters': None,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/linux64/releng.manifest',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64',
            'mock_packages': \
                       ['autoconf213', 'python', 'zip', 'mozilla-python27-mercurial', 'git', 'ccache',
                        'glibc-static', 'libstdc++-static', 'perl-Test-Simple', 'perl-Config-General',
                        'gtk2-devel', 'libnotify-devel', 'yasm',
                        'alsa-lib-devel', 'libcurl-devel',
                        'wireless-tools-devel', 'libX11-devel',
                        'libXt-devel', 'mesa-libGL-devel',
                        'gnome-vfs2-devel', 'GConf2-devel', 'wget',
                        'mpfr', # required for system compiler
                        'xorg-x11-font*', # fonts required for PGO
                        'imake', # required for makedepend!?!
                        'gcc45_0moz3', 'gcc454_0moz1', 'gcc472_0moz1', 'gcc473_0moz1', 'yasm', 'ccache', # <-- from releng repo
                        'pulseaudio-libs-devel',
                        'freetype-2.3.11-6.el6_1.8.x86_64',
                        'freetype-devel-2.3.11-6.el6_1.8.x86_64',
                        'gstreamer-devel', 'gstreamer-plugins-base-devel',
                        ],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/gapi.data', '/builds/gapi.data'),
                ('/builds/google-oauth-api.key', '/builds/google-oauth-api.key'),
                ('/builds/mozilla-desktop-geoloc-api.key', '/builds/mozilla-desktop-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
        },
        'macosx64-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': ['scripts/external_tools/count_and_reboot.py',
                               '-f', '../reboot_count.txt', '-n', '1', '-z'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_mac_64_builds.py',
                    '--custom-build-variant-cfg', 'debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'OS X 10.7 64-bit %(branch)s leak test',
            'mozconfig': 'macosx64/%(branch)s/debug',
            'src_mozconfig': 'browser/config/mozconfigs/macosx64/debug',
            'packageTests': True,
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': True,
            'build_space': 10,
            'slaves': SLAVES['macosx64-lion'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'macosx64-debug',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'LC_ALL': 'C',
                'PATH': '/tools/python/bin:/tools/buildbot/bin:/opt/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
            },
            'enable_unittests': False,
            'enable_checktests': True,
            'talos_masters': None,
            # These refer to items in passwords.secrets
            # nightly_signing_servers defaults to dep-signing because we don't want
            # random new branches to accidentally use nightly-signing, which signs
            # with valid keys. Any branch that needs to be signed with these keys
            # must be overridden explicitly.
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/macosx64/releng.manifest',
            'enable_ccache': True,
        },
        'macosx64-st-an-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'reboot_command': ['scripts/external_tools/count_and_reboot.py',
                               '-f', '../reboot_count.txt', '-n', '1', '-z'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_mac_64_builds.py',
                    '--custom-build-variant-cfg', 'stat-and-debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'OS X 10.7 64-bit %(branch)s debug static analysis',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'browser/config/mozconfigs/macosx64/debug-static-analysis',
            'packageTests': False,
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': False,
            'build_space': 10,
            'slaves': SLAVES['macosx64-lion'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'macosx64-st-an-debug',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'LC_ALL': 'C',
                'PATH': '/tools/python/bin:/tools/buildbot/bin:/opt/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
            },
            'enable_unittests': False,
            'enable_checktests': False,
            'talos_masters': None,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/macosx64/releng.manifest',
            'enable_ccache': True,
        },
        'win32-debug': {
            'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
            'reboot_command': [
                'c:/mozilla-build/python27/python', '-u',
                'scripts/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt','-n', '1', '-z'
            ],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_windows_32_builds.py',
                    '--custom-build-variant-cfg', 'debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(7.5 * 3600),
            },

            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'WINNT 5.2 %(branch)s leak test',
            'mozconfig': 'win32/%(branch)s/debug',
            'src_mozconfig': 'browser/config/mozconfigs/win32/debug',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': True,
            'enable_installer': True,
            'packageTests': True,
            'build_space': 9,
            'slaves': SLAVES['win64-rev2'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'win32-debug',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'HG_SHARE_BASE_DIR': 'c:/builds/hg-shared',
                'BINSCOPE': 'C:\Program Files (x86)\Microsoft\SDL BinScope\BinScope.exe',
                'PATH': "${MOZILLABUILD}nsis-3.0b1;${MOZILLABUILD}nsis-2.46u;${MOZILLABUILD}python27;${MOZILLABUILD}buildbotve\\scripts;${PATH}",
            },
            'enable_unittests': False,
            'enable_checktests': True,
            'talos_masters': None,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/win32/releng.manifest',
            'tooltool_script': ['python', '/c/mozilla-build/tooltool.py'],
        },
        'win64-debug': {
            'mozharness_python': ['c:/mozilla-build/python27/python', '-u'],
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_windows_64_builds.py',
                    '--custom-build-variant-cfg', 'debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(7.5 * 3600),
            },
            'reboot_command': [
                'c:/mozilla-build/python27/python', '-u',
                'scripts/external_tools/count_and_reboot.py',
                '-f', '../reboot_count.txt','-n', '1', '-z'
            ],
            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'WINNT 6.1 x86-64 %(branch)s leak test',
            'mozconfig': 'win64/%(branch)s/debug',
            'src_mozconfig': 'browser/config/mozconfigs/win64/debug',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'download_symbols': True,
            'enable_installer': True,
            'packageTests': True,
            'build_space': 9,
            'try_by_default': False,
            'slaves': SLAVES['win64-rev2'],
            'platform_objdir': OBJDIR,
            'stage_product': 'firefox',
            'stage_platform': 'win64-debug',
            'enable_shared_checkouts': True,
            'env': {
                'MOZ_OBJDIR': OBJDIR,
                'XPCOM_DEBUG_BREAK': 'stack-and-abort',
                'HG_SHARE_BASE_DIR': 'c:/builds/hg-shared',
                'BINSCOPE': 'C:\Program Files (x86)\Microsoft\SDL BinScope\BinScope.exe',
                'PATH': "${MOZILLABUILD}nsis-3.0b1;${MOZILLABUILD}nsis-2.46u;${MOZILLABUILD}python27;${MOZILLABUILD}buildbotve\\scripts;${PATH}",
            },
            'enable_unittests': False,
            'enable_checktests': True,
            'talos_masters': None,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'consider_for_nightly': False,
            'tooltool_manifest_src': 'browser/config/tooltool-manifests/win64/releng.manifest',
            'tooltool_script': ['python', '/c/mozilla-build/tooltool.py'],
        },
        'android-api-9': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_android_64_builds.py',
                    '--custom-build-variant-cfg', 'api-9',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'product_name': 'firefox',
            'unittest_platform': 'android-api-9-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Android armv7 API 9 %(branch)s',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'mobile/android/config/mozconfigs/android-api-9-10-constrained/nightly',
            'mobile_dir': 'mobile/android',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 16,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,
            'create_partial': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64-android',
            'mock_packages': ['autoconf213', 'mozilla-python27-mercurial',
                              'ccache', 'zip',
                              'java-1.7.0-openjdk-devel', 'zlib-devel',
                              'glibc-static', 'openssh-clients', 'mpfr',
                              "gcc472_0moz1", "gcc473_0moz1", 'wget', 'glibc.i686',
                              'libstdc++.i686', 'zlib.i686',
                              'freetype-2.3.11-6.el6_1.8.x86_64', 'ant', 'ant-apache-regexp'],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/mozilla-api.key', '/builds/mozilla-api.key'),
                ('/builds/mozilla-fennec-geoloc-api.key', '/builds/mozilla-fennec-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/builds/adjust-sdk.token', '/builds/adjust-sdk.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_MOBILE_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SHIP_LICENSED_FONTS': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/opt/local/bin:/tools/python/bin:/tools/buildbot/bin:/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/home/',
            },
            'enable_opt_unittests': False,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'unittest_masters': GLOBAL_VARS['unittest_masters'],
            'stage_platform': "android-api-9",
            'stage_product': 'mobile',
            'post_upload_include_platform': True,
            'is_mobile_l10n': True,
            'l10n_chunks': 5,
            'multi_locale': True,
            'multi_locale_config_platform': 'android',
            'multi_locale_script': 'scripts/multil10n.py',
            'tooltool_manifest_src': 'mobile/android/config/tooltool-manifests/android/releng.manifest',
            'update_platform': 'Android_arm-eabi-gcc3',
            'updates_enabled': False,
        },
        'android-api-11': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_android_64_builds.py',
                    '--custom-build-variant-cfg', 'api-11',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'product_name': 'firefox',
            'unittest_platform': 'android-api-11-opt',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Android armv7 API 11+ %(branch)s',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'mobile/android/config/mozconfigs/android-api-11/nightly',
            'mobile_dir': 'mobile/android',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 16,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,
            'create_partial': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64-android',
            'mock_packages': ['autoconf213', 'mozilla-python27-mercurial',
                              'ccache', 'zip',
                              'java-1.7.0-openjdk-devel', 'zlib-devel',
                              'glibc-static', 'openssh-clients', 'mpfr',
                              "gcc472_0moz1", "gcc473_0moz1", 'wget', 'glibc.i686',
                              'libstdc++.i686', 'zlib.i686',
                              'freetype-2.3.11-6.el6_1.8.x86_64', 'ant', 'ant-apache-regexp'],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/mozilla-api.key', '/builds/mozilla-api.key'),
                ('/builds/mozilla-fennec-geoloc-api.key', '/builds/mozilla-fennec-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/builds/adjust-sdk.token', '/builds/adjust-sdk.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_MOBILE_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SHIP_LICENSED_FONTS': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/opt/local/bin:/tools/python/bin:/tools/buildbot/bin:/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/home/',
            },
            'enable_opt_unittests': False,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'unittest_masters': GLOBAL_VARS['unittest_masters'],
            'stage_platform': "android-api-11",
            'stage_product': 'mobile',
            'post_upload_include_platform': True,
            'is_mobile_l10n': True,
            'l10n_chunks': 5,
            'multi_locale': True,
            'multi_locale_script': 'scripts/multil10n.py',
            'multi_locale_config_platform': 'android',
            'tooltool_manifest_src': 'mobile/android/config/tooltool-manifests/android/releng.manifest',
            'update_platform': 'Android_arm-eabi-gcc3',
            'updates_enabled': False,
        },
        'android-x86': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_android_64_builds.py',
                    '--custom-build-variant-cfg', 'x86',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'product_name': 'firefox',
            'unittest_platform': 'android-x86-opt',
            'app_name': 'browser',
            'base_name': 'Android 4.2 x86 %(branch)s',
            'mozconfig': 'android-x86/%(branch)s/nightly',
            'src_mozconfig': 'mobile/android/config/mozconfigs/android-x86/nightly',
            'mobile_dir': 'mobile/android',
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 14,
            'upload_symbols': True,
            'packageTests': True,
            'profiled_build': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'update_platform': 'Android_x86-gcc3',
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'use_mock': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'mock_target': 'mozilla-centos6-x86_64-android',
            'mock_packages': ['autoconf213', 'mozilla-python27-mercurial',
                              'ccache', 'yasm', 'zip',
                              'java-1.7.0-openjdk-devel', 'zlib-devel',
                              'glibc-static', 'openssh-clients', 'mpfr', 'bc',
                              "gcc472_0moz1", "gcc473_0moz1", 'glibc.i686', 'libstdc++.i686',
                              'zlib.i686', 'freetype-2.3.11-6.el6_1.8.x86_64', 'ant', 'ant-apache-regexp'],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/mozilla-api.key', '/builds/mozilla-api.key'),
                ('/builds/mozilla-fennec-geoloc-api.key', '/builds/mozilla-fennec-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/builds/adjust-sdk.token', '/builds/adjust-sdk.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_MOBILE_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/bin:/usr/bin',
            },
            'enable_opt_unittests': False,
            'talos_masters': GLOBAL_VARS['talos_masters'],
            'unittest_masters': GLOBAL_VARS['unittest_masters'],
            'stage_platform': "android-x86",
            'stage_product': 'mobile',
            'post_upload_include_platform': True,
            'is_mobile_l10n': False,
            'multi_locale': True,
            'multi_locale_script': 'scripts/multil10n.py',
            'tooltool_manifest_src': 'mobile/android/config/tooltool-manifests/android-x86/releng.manifest',
            'updates_enabled': False,
        },
        'android-api-9-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_android_64_builds.py',
                    '--custom-build-variant-cfg', 'api-9-debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'enable_nightly': False,
            'product_name': 'firefox',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Android armv7 API 9 %(branch)s debug',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'mobile/android/config/mozconfigs/android-api-9-10-constrained/debug',
            'mobile_dir': 'mobile/android',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 14,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,
            'updates_enabled': False,
            'create_partial': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64-android',
            'mock_packages': ['autoconf213', 'mozilla-python27-mercurial',
                              'ccache', 'zip', "gcc472_0moz1", "gcc473_0moz1",
                              'java-1.7.0-openjdk-devel', 'zlib-devel',
                              'glibc-static', 'openssh-clients', 'mpfr',
                              'wget', 'glibc.i686', 'libstdc++.i686',
                              'zlib.i686', 'freetype-2.3.11-6.el6_1.8.x86_64', 'ant', 'ant-apache-regexp'],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/mozilla-api.key', '/builds/mozilla-api.key'),
                ('/builds/mozilla-fennec-geoloc-api.key', '/builds/mozilla-fennec-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/builds/adjust-sdk.token', '/builds/adjust-sdk.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_MOBILE_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SHIP_LICENSED_FONTS': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/bin:/usr/bin',
            },
            'enable_opt_unittests': False,
            'talos_masters': None,
            'unittest_masters': GLOBAL_VARS['unittest_masters'],
            'stage_platform': "android-api-9-debug",
            'stage_product': 'mobile',
            'post_upload_include_platform': True,
            'tooltool_manifest_src': 'mobile/android/config/tooltool-manifests/android/releng.manifest',
            'updates_enabled': False,
        },
        'android-api-11-debug': {
            'mozharness_python': '/tools/buildbot/bin/python',
            'mozharness_desktop_build': {
                'script_name': 'scripts/fx_desktop_build.py',
                'extra_args': [
                    '--config', 'builds/releng_base_android_64_builds.py',
                    '--custom-build-variant-cfg', 'api-11-debug',
                    '--config', GLOBAL_VARS['mozharness_configs']['balrog'],
                ],
                'script_timeout': 3 * 3600,
                'script_maxtime': int(5.5 * 3600),
            },
            'enable_nightly': False,
            'product_name': 'firefox',
            'unittest_platform': 'android-api-11-debug',
            'app_name': 'browser',
            'brand_name': 'Minefield',
            'base_name': 'Android armv7 API 11+ %(branch)s debug',
            'mozconfig': 'in_tree',
            'src_mozconfig': 'mobile/android/config/mozconfigs/android-api-11/debug',
            'mobile_dir': 'mobile/android',
            'profiled_build': False,
            'builds_before_reboot': localconfig.BUILDS_BEFORE_REBOOT,
            'build_space': 14,
            'upload_symbols': True,
            'download_symbols': False,
            'packageTests': True,
            'updates_enabled': False,
            'create_partial': False,
            'slaves': SLAVES['mock'],
            'platform_objdir': OBJDIR,
            'enable_ccache': True,
            'enable_shared_checkouts': True,
            'nightly_signing_servers': 'dep-signing',
            'dep_signing_servers': 'dep-signing',
            'use_mock': True,
            'mock_target': 'mozilla-centos6-x86_64-android',
            'mock_packages': ['autoconf213', 'mozilla-python27-mercurial',
                              'ccache', 'zip', "gcc472_0moz1", "gcc473_0moz1",
                              'java-1.7.0-openjdk-devel', 'zlib-devel',
                              'glibc-static', 'openssh-clients', 'mpfr',
                              'wget', 'glibc.i686', 'libstdc++.i686',
                              'zlib.i686', 'freetype-2.3.11-6.el6_1.8.x86_64', 'ant', 'ant-apache-regexp'],
            'mock_copyin_files': [
                ('/home/cltbld/.ssh', '/home/mock_mozilla/.ssh'),
                ('/home/cltbld/.hgrc', '/builds/.hgrc'),
                ('/home/cltbld/.boto', '/builds/.boto'),
                ('/builds/mozilla-api.key', '/builds/mozilla-api.key'),
                ('/builds/mozilla-fennec-geoloc-api.key', '/builds/mozilla-fennec-geoloc-api.key'),
                ('/builds/crash-stats-api.token', '/builds/crash-stats-api.token'),
                ('/builds/adjust-sdk.token', '/builds/adjust-sdk.token'),
                ('/usr/local/lib/hgext', '/usr/local/lib/hgext'),
            ],
            'env': {
                'DISPLAY': ':2',
                'HG_SHARE_BASE_DIR': '/builds/hg-shared',
                'TOOLTOOL_CACHE': '/builds/tooltool_cache',
                'TOOLTOOL_HOME': '/builds',
                'MOZ_OBJDIR': OBJDIR,
                'SYMBOL_SERVER_HOST': localconfig.SYMBOL_SERVER_HOST,
                'SYMBOL_SERVER_USER': 'ffxbld',
                'SYMBOL_SERVER_PATH': SYMBOL_SERVER_MOBILE_PATH,
                'SYMBOL_SERVER_SSH_KEY': "/home/mock_mozilla/.ssh/ffxbld_rsa",
                'POST_SYMBOL_UPLOAD_CMD': SYMBOL_SERVER_POST_UPLOAD_CMD,
                'SHIP_LICENSED_FONTS': '1',
                'CCACHE_DIR': '/builds/ccache',
                'CCACHE_COMPRESS': '1',
                'CCACHE_UMASK': '002',
                'LC_ALL': 'C',
                'PATH': '/tools/buildbot/bin:/usr/local/bin:/bin:/usr/bin',
            },
            'enable_opt_unittests': False,
            'talos_masters': None,
            'unittest_masters': GLOBAL_VARS['unittest_masters'],
            'stage_platform': "android-api-11-debug",
            'stage_product': 'mobile',
            'post_upload_include_platform': True,
            'tooltool_manifest_src': 'mobile/android/config/tooltool-manifests/android/releng.manifest',
            'updates_enabled': False,
        },
}
# Additional fixups for lion
PLATFORM_VARS["macosx64-lion"] = deepcopy(PLATFORM_VARS["macosx64"])
PLATFORM_VARS["macosx64-lion-debug"] = deepcopy(PLATFORM_VARS["macosx64-debug"])
PLATFORM_VARS["macosx64-lion"]["base_name"] = 'OS X 10.7 %(branch)s'
PLATFORM_VARS["macosx64-lion-debug"]["base_name"] = 'OS X 10.7 64-bit %(branch)s leak test'
PLATFORM_VARS["macosx64-lion"]["slaves"] = SLAVES['macosx64-lion']
PLATFORM_VARS["macosx64-lion-debug"]["slaves"] = SLAVES['macosx64-lion']

for platform in PLATFORM_VARS.values():
    if 'env' not in platform:
        platform['env'] = deepcopy(GLOBAL_ENV)
    else:
        platform['env'].update((k, v) for k, v in GLOBAL_ENV.items() if k not in platform['env'])

PROJECTS = {
    'fuzzing': {
        'platforms': ['mock', 'macosx64-lion', 'win64-rev2'],
    },
}

# For bug 978211, we are using MOZ_AUTOMATION to trigger the automation build
# steps from mach. However, these build variants already use mach, and so they
# would inadvertently trigger the automation steps. We can remove the
# MOZ_AUTOMATION environment variable for them, since it's not used anyway.
del PLATFORM_VARS["linux64-sh-haz"]["env"]["MOZ_AUTOMATION"]
del PLATFORM_VARS["linux64-br-haz"]["env"]["MOZ_AUTOMATION"]

# Override config settings with local settings
def apply_localconfig(config, local):
    for k, v in local.items():
        if k not in config:
            config[k] = {}
        config[k].update(v)

apply_localconfig(PROJECTS, localconfig.PROJECTS)

# Branch-associated projects
#
# BRANCHES values contain a 'branch_projects' key containing a list of
# BRANCH_PROJECTS keys to instantiate for that branch. These are intended for
# builds that are associated with one or more branches, but use separate
# scheduling and build mechanisms. Each project will have a 'branch' key filled
# in with the name of the branch to which it applies.
#
# Configuration keys:
#
#  project_name - pattern used to construct (part of) the builder name. It
#    can use %-interpolation to select anything from the config, which
#    usually means it will contain "%(branch)s".
#
# Spidermonkey-specific configuration keys:
#
#  variants - mapping of platforms (with build configuration, eg linux64-debug)
#    to an array of variant names. These names correspond to files in
#    <gecko>/js/src/devtools/automation/variants/.
#
#  enable_try - this project should be active for the try server
#
#  try_by_default - list of variants that should be triggered by default on
#    try. If a variant is missing from this list, then the build will only be
#    triggered if the corresponding base platform is explicitly requested in
#    the -p option of trychooser. For example, |-p all| will not trigger such a
#    project, but either |-p linux64| or |-p all,linux64| will (assuming the
#    project has both 'platforms' and 'variants' entries for 'linux' or
#    'linux64'.)
#
BRANCH_PROJECTS = {
    # Builds that should trigger backouts if they break. Should be on all trees
    # feeding into mozilla-central.
    'spidermonkey_tier_1': {
        'variants': {
            'linux64-debug':  ['rootanalysis', 'compacting', 'arm64-sim'],
            'linux-debug': ['arm-sim'],
            'macosx64-debug': [],
            'win32-debug': ['plaindebug', 'compacting'],
            'win32': ['plain'],
        },
        'platforms': {
            'linux': {},
            'linux-debug': {},
            'linux64': {},
            'linux64-debug': {},
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
        },
        'hgurl': 'https://hg.mozilla.org/',
    },

    # Try server builds only triggered on changes to the spidermonkey source
    'spidermonkey_try': {
        'enable_try': True,
        'try_by_default': {
            'rootanalysis': True, # all platforms for which it is defined
            'compacting': set(['linux64-debug', 'win32-debug']),
            'arm-sim': True,
            'arm64-sim': True,
            'arm-sim-osx': set([]),
        },
        'variants': {
            'linux': ['warnaserr'],
            'linux-debug': ['arm-sim', 'warnaserrdebug'],
            'linux64':  ['warnaserr'],
            'linux64-debug':  ['rootanalysis', 'compacting', 'warnaserrdebug', 'arm64-sim'],
            'macosx64-debug': ['arm-sim-osx'],
            'win32': ['compacting', 'plain'],
            'win32-debug': ['compacting', 'plaindebug'],
            'win64': ['compacting', 'plain'],
            'win64-debug': ['compacting', 'plaindebug'],
        },
        'platforms': {
            'linux': {},
            'linux-debug': {},
            'linux64': {},
            'linux64-debug': {},
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
        },
        'hgurl': 'https://hg.mozilla.org/',
    },

    # Non-tier-1 builds that provide useful information but are hidden on tbpl.
    # These should be run on the (small) subset of trees looked at by the
    # relevant developers.
    'spidermonkey_info': {
        'variants': {
            'linux64':        ['warnaserr'],
            'linux64-debug':  ['warnaserrdebug'],
        },
        'platforms': {
            'linux': {},
            'linux-debug': {},
            'linux64': {},
            'linux64-debug': {},
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
        },
        'hgurl': 'https://hg.mozilla.org/',
    },
}

apply_localconfig(BRANCH_PROJECTS, localconfig.BRANCH_PROJECTS)

# All branches (not in project_branches) that are to be built MUST be listed here, along with their
# platforms (if different from the default set).
BRANCHES = {
    'mozilla-central': {
        'merge_builds': False,
    },
    'mozilla-release': {
        'merge_builds': False,
    },
    'mozilla-beta': {
        'merge_builds': False,
    },
    'mozilla-aurora': {
        'merge_builds': False,
    },
    'mozilla-esr38': {
        'merge_builds': False,
        'lock_platforms': True,
        'gecko_version': 38,
        'platforms': {
            'linux': {},
            'linux64': {},
            'macosx64': {},
            'win32': {},
            'win64': {},
            'linux64-av': {},
            'linux-debug': {},
            'linux64-debug': {},
            'macosx64-debug': {},
            'win32-debug': {},
            'win64-debug': {},
        },
    },
    'mozilla-b2g37_v2_2': {
        'merge_builds': False,
        'branch_projects': [],
        'lock_platforms': True,
        'gecko_version': 37,
        'platforms': {
            'linux': {},
            'linux64': {},
            'win32': {},
            'macosx64': {},
            'linux-debug': {},
            'linux64-debug': {},
            'macosx64-debug': {},
            'win32-debug': {},
        },
    },
    'mozilla-b2g37_v2_2r': {
        'merge_builds': False,
        'branch_projects': [],
        'lock_platforms': True,
        'gecko_version': 37,
        'platforms': {},
    },
    'mozilla-b2g44_v2_5': {
        'merge_builds': False,
        'branch_projects': [],
        'lock_platforms': True,
        'gecko_version': 44,
        'platforms': {},
    },
    'b2g-ota': {
        'merge_builds': False,
        'branch_projects': [],
        'lock_platforms': True,
        'gecko_version': 45,
        'platforms': {},
    },
    'try': {
        'branch_projects': ['spidermonkey_try'],
        # The following platforms are not part of the default set,
        # so only run on Try.
        'extra_platforms': {
            'linux64-sh-haz': {},
            'linux64-cc': {},
            'linux64-tsan': {},
        },
    },
}

setMainFirefoxVersions(BRANCHES)

# Copy project branches into BRANCHES keys
for branch in ACTIVE_PROJECT_BRANCHES:
    BRANCHES[branch] = deepcopy(PROJECT_BRANCHES[branch])
    if 'mobile_platforms' in BRANCHES[branch]:
        if 'platforms' not in BRANCHES[branch]:
            BRANCHES[branch]['platforms'] = deepcopy(BRANCHES[branch]['mobile_platforms'])
        else:
            BRANCHES[branch]['platforms'].update(deepcopy(BRANCHES[branch]['mobile_platforms']))

# Copy global vars in first, then platform vars
for branch in BRANCHES.keys():
    for key, value in GLOBAL_VARS.items():
        # Don't override platforms if it's set and locked
        if key == 'platforms' and 'platforms' in BRANCHES[branch] and BRANCHES[branch].get('lock_platforms'):
            continue
        # Don't override something that's set
        elif key in ('enable_weekly_bundle','branch_projects',) and key in BRANCHES[branch]:
            continue
        # If the key is already set then we won't override with GLOBAL_VARS
        # The "platforms" key is handle separatedely (see next for loop)
        elif key == 'platforms' or key not in BRANCHES[branch]:
            BRANCHES[branch][key] = deepcopy(value)

    BRANCHES[branch]['platforms'].update(BRANCHES[branch].get('extra_platforms', {}))

    for platform, platform_config in PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                # put default platform set in all branches, but grab any
                # project_branches.py overrides/additional keys
                if branch in ACTIVE_PROJECT_BRANCHES and 'platforms' in PROJECT_BRANCHES[branch]:
                    if platform in PROJECT_BRANCHES[branch]['platforms'].keys():
                        if key in PROJECT_BRANCHES[branch]['platforms'][platform].keys():
                            value = deepcopy(PROJECT_BRANCHES[branch]['platforms'][platform][key])
                else:
                    value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                else:
                    value = deepcopy(value)
                BRANCHES[branch]['platforms'][platform][key] = value

            if branch in ACTIVE_PROJECT_BRANCHES and 'platforms' in PROJECT_BRANCHES[branch] and \
                    PROJECT_BRANCHES[branch]['platforms'].has_key(platform):
                for key, value in PROJECT_BRANCHES[branch]['platforms'][platform].items():
                    if key == 'env':
                        value = deepcopy(PLATFORM_VARS[platform]['env'])
                        value.update(PROJECT_BRANCHES[branch]['platforms'][platform][key])
                    else:
                        value = deepcopy(value)
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

    for platform, platform_config in localconfig.PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

    # Check for project branch removing a platform from default platforms
    if branch in ACTIVE_PROJECT_BRANCHES:
        for key, value in PROJECT_BRANCHES[branch].items():
            if key in ('platforms', 'mobile_platforms'):
                for platform, platform_config in value.items():
                    if platform_config.get('dont_build'):
                        del BRANCHES[branch]['platforms'][platform]

######## mozilla-central
# This is a path, relative to HGURL, where the repository is located
# HGURL + repo_path should be a valid repository
BRANCHES['mozilla-central']['repo_path'] = 'mozilla-central'
BRANCHES['mozilla-central']['l10n_repo_path'] = 'l10n-central'
BRANCHES['mozilla-central']['enable_perproduct_builds'] = True
BRANCHES['mozilla-central']['enable_weekly_bundle'] = True
BRANCHES['mozilla-central']['start_hour'] = [3]
BRANCHES['mozilla-central']['start_minute'] = [2]
# Enable PGO Builds on this branch
BRANCHES['mozilla-central']['pgo_strategy'] = 'periodic'
BRANCHES['mozilla-central']['periodic_start_hours'] = range(1, 24, 3)
BRANCHES['mozilla-central']['periodic_start_minute'] = 30
# Enable unit tests
BRANCHES['mozilla-central']['enable_mac_a11y'] = True
BRANCHES['mozilla-central']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-central']['enable_l10n'] = True
BRANCHES['mozilla-central']['enable_l10n_onchange'] = True
BRANCHES['mozilla-central']['l10nNightlyUpdate'] = True
BRANCHES['mozilla-central']['l10n_platforms'] = ['linux', 'linux64', 'win32',
                                                 'macosx64', 'win64']
BRANCHES['mozilla-central']['l10nDatedDirs'] = True
BRANCHES['mozilla-central']['l10n_tree'] = 'fxcentral'
# make sure it has an ending slash
BRANCHES['mozilla-central']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/firefox/nightly/latest-mozilla-central-l10n/'
BRANCHES['mozilla-central']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-central'
BRANCHES['mozilla-central']['localesURL'] = \
    '%s/build/buildbot-configs/raw-file/production/mozilla/l10n/all-locales.mozilla-central' % (GLOBAL_VARS['hgurl'])
BRANCHES['mozilla-central']['enable_multi_locale'] = True
BRANCHES['mozilla-central']['upload_mobile_symbols'] = True
# Enable desktop repacks with mozharness
BRANCHES['mozilla-central']['desktop_mozharness_repacks_enabled'] = True

# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['mozilla-central']['updates_enabled'] = True
BRANCHES['mozilla-central']['update_channel'] = 'nightly'
BRANCHES['mozilla-central']['create_partial'] = True
BRANCHES['mozilla-central']['create_partial_l10n'] = True
BRANCHES['mozilla-central']['enable_blocklist_update'] = True
BRANCHES['mozilla-central']['enable_hsts_update'] = True
BRANCHES['mozilla-central']['enable_hpkp_update'] = True
BRANCHES['mozilla-central']['platforms']['android-x86']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-x86'
BRANCHES['mozilla-central']['platforms']['android-x86']['updates_enabled'] = True
BRANCHES['mozilla-central']['platforms']['android-api-9']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-9'
BRANCHES['mozilla-central']['platforms']['android-api-9']['updates_enabled'] = True
BRANCHES['mozilla-central']['platforms']['android-api-11']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-11'
BRANCHES['mozilla-central']['platforms']['android-api-11']['updates_enabled'] = True
BRANCHES['mozilla-central']['platforms']['linux']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['linux64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['win32']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['win64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['android-api-9']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['android-api-11']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['platforms']['macosx64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-central']['l10n_extra_configure_args'] = ['--with-macbundlename-prefix=Firefox']

######## mozilla-release
BRANCHES['mozilla-release']['repo_path'] = 'releases/mozilla-release'
BRANCHES['mozilla-release']['update_channel'] = 'release'
BRANCHES['mozilla-release']['l10n_repo_path'] = 'releases/l10n/mozilla-release'
BRANCHES['mozilla-release']['enable_weekly_bundle'] = True
BRANCHES['mozilla-release']['start_hour'] = [3]
BRANCHES['mozilla-release']['start_minute'] = [2]
# Enable PGO Builds on this branch
BRANCHES['mozilla-release']['pgo_strategy'] = 'per-checkin'
# Enable unit tests
BRANCHES['mozilla-release']['enable_mac_a11y'] = True
# L10n configuration
BRANCHES['mozilla-release']['enable_l10n'] = False
BRANCHES['mozilla-release']['enable_l10n_onchange'] = True
BRANCHES['mozilla-release']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-release']['l10n_platforms'] = ['linux', 'linux64', 'win32',
                                                 'macosx64']
BRANCHES['mozilla-release']['l10nDatedDirs'] = True
BRANCHES['mozilla-release']['l10n_tree'] = 'fxrel'
BRANCHES['mozilla-release']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-release'
BRANCHES['mozilla-release']['localesURL'] = \
    '%s/build/buildbot-configs/raw-file/production/mozilla/l10n/all-locales.mozilla-release' % (GLOBAL_VARS['hgurl'])
BRANCHES['mozilla-release']['enable_multi_locale'] = True
BRANCHES['mozilla-release']['upload_mobile_symbols'] = True
# temp disable nightlies (which includes turning off enable_l10n and l10nNightlyUpdate)
BRANCHES['mozilla-release']['enable_nightly'] = False
BRANCHES['mozilla-release']['enable_blocklist_update'] = True
BRANCHES['mozilla-release']['enable_valgrind'] = False
BRANCHES['mozilla-release']['enabled_products'] = ['firefox', 'mobile']
BRANCHES['mozilla-release']['platforms']['android-x86']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-x86'
BRANCHES['mozilla-release']['platforms']['android-api-9']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-9'
BRANCHES['mozilla-release']['platforms']['android-api-11']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-11'
BRANCHES['mozilla-release']['platforms']['macosx64']['platform_objdir'] = "%s/x86_64" % OBJDIR

######## mozilla-beta
BRANCHES['mozilla-beta']['repo_path'] = 'releases/mozilla-beta'
BRANCHES['mozilla-beta']['l10n_repo_path'] = 'releases/l10n/mozilla-beta'
BRANCHES['mozilla-beta']['enable_weekly_bundle'] = True
BRANCHES['mozilla-beta']['update_channel'] = 'beta'
BRANCHES['mozilla-beta']['start_hour'] = [3]
BRANCHES['mozilla-beta']['start_minute'] = [2]
# Enable PGO Builds on this branch
BRANCHES['mozilla-beta']['pgo_strategy'] = 'per-checkin'
# Enable unit tests
BRANCHES['mozilla-beta']['enable_mac_a11y'] = True
BRANCHES['mozilla-beta']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-beta']['enable_l10n'] = False
BRANCHES['mozilla-beta']['enable_l10n_onchange'] = True
BRANCHES['mozilla-beta']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-beta']['l10n_platforms'] = ['linux', 'linux64', 'win32',
                                              'macosx64']
BRANCHES['mozilla-beta']['l10nDatedDirs'] = True
BRANCHES['mozilla-beta']['l10n_tree'] = 'fxbeta'
#make sure it has an ending slash
BRANCHES['mozilla-beta']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/firefox/nightly/latest-mozilla-beta-l10n/'
BRANCHES['mozilla-beta']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-beta'
BRANCHES['mozilla-beta']['localesURL'] = \
    '%s/build/buildbot-configs/raw-file/production/mozilla/l10n/all-locales.mozilla-beta' % (GLOBAL_VARS['hgurl'])
BRANCHES['mozilla-beta']['enable_multi_locale'] = True
BRANCHES['mozilla-beta']['upload_mobile_symbols'] = True
# temp disable nightlies (which includes turning off enable_l10n and l10nNightlyUpdate)
BRANCHES['mozilla-beta']['enable_nightly'] = False
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['mozilla-beta']['enable_blocklist_update'] = True
BRANCHES['mozilla-beta']['enable_valgrind'] = False
BRANCHES['mozilla-beta']['platforms']['android-x86']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-x86'
BRANCHES['mozilla-beta']['platforms']['android-api-9']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-9'
BRANCHES['mozilla-beta']['platforms']['android-api-11']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-11'
BRANCHES['mozilla-beta']['platforms']['android-api-9']['enable_dep'] = True
BRANCHES['mozilla-beta']['platforms']['android-api-11']['enable_dep'] = True
BRANCHES['mozilla-beta']['platforms']['android-api-9-debug']['enable_dep'] = True
BRANCHES['mozilla-beta']['platforms']['android-api-11-debug']['enable_dep'] = True
BRANCHES['mozilla-beta']['platforms']['macosx64']['platform_objdir'] = "%s/x86_64" % OBJDIR
BRANCHES['mozilla-beta']['enabled_products'] = ['firefox', 'mobile']
BRANCHES['mozilla-beta']['enable_perproduct_builds'] = True

######## mozilla-aurora
BRANCHES['mozilla-aurora']['repo_path'] = 'releases/mozilla-aurora'
BRANCHES['mozilla-aurora']['l10n_repo_path'] = 'releases/l10n/mozilla-aurora'
BRANCHES['mozilla-aurora']['enable_perproduct_builds'] = True
BRANCHES['mozilla-aurora']['enable_weekly_bundle'] = True
BRANCHES['mozilla-aurora']['start_hour'] = [0]
BRANCHES['mozilla-aurora']['start_minute'] = [40]
BRANCHES['mozilla-aurora']['periodic_start_hours'] = range(1, 24, 6)
BRANCHES['mozilla-aurora']['periodic_start_minute'] = 30
# Enable PGO Builds on this branch
BRANCHES['mozilla-aurora']['pgo_strategy'] = 'per-checkin'
# Enable unit tests
BRANCHES['mozilla-aurora']['enable_mac_a11y'] = True
BRANCHES['mozilla-aurora']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-aurora']['enable_l10n'] = True
BRANCHES['mozilla-aurora']['enable_l10n_onchange'] = True
BRANCHES['mozilla-aurora']['l10nNightlyUpdate'] = True
BRANCHES['mozilla-aurora']['l10n_platforms'] = ['linux', 'linux64', 'win32',
                                                 'macosx64', 'win64']
BRANCHES['mozilla-aurora']['l10nDatedDirs'] = True
BRANCHES['mozilla-aurora']['l10n_tree'] = 'fxaurora'
#make sure it has an ending slash
BRANCHES['mozilla-aurora']['l10nUploadPath'] = \
    '/home/ftp/pub/mozilla.org/firefox/nightly/latest-mozilla-aurora-l10n/'
BRANCHES['mozilla-aurora']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-aurora'
BRANCHES['mozilla-aurora']['localesURL'] = \
    '%s/build/buildbot-configs/raw-file/production/mozilla/l10n/all-locales.mozilla-aurora' % (GLOBAL_VARS['hgurl'])
BRANCHES['mozilla-aurora']['enable_multi_locale'] = True
BRANCHES['mozilla-aurora']['upload_mobile_symbols'] = True
# Enable desktop repacks with mozharness
BRANCHES['mozilla-aurora']['desktop_mozharness_repacks_enabled'] = True
# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['mozilla-aurora']['updates_enabled'] = True
BRANCHES['mozilla-aurora']['update_channel'] = 'aurora'
BRANCHES['mozilla-aurora']['create_partial'] = True
BRANCHES['mozilla-aurora']['create_partial_l10n'] = True
# use mozilla-aurora-test when disabling updates for merges
BRANCHES['mozilla-aurora']['enable_blocklist_update'] = True
BRANCHES['mozilla-aurora']['enable_hsts_update'] = True
BRANCHES['mozilla-aurora']['enable_hpkp_update'] = True
BRANCHES['mozilla-aurora']['enable_valgrind'] = False
BRANCHES['mozilla-aurora']['platforms']['android-api-9']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-9'
BRANCHES['mozilla-aurora']['platforms']['android-api-9']['updates_enabled'] = True
BRANCHES['mozilla-aurora']['platforms']['android-api-11']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-11'
BRANCHES['mozilla-aurora']['platforms']['android-api-11']['updates_enabled'] = True
BRANCHES['mozilla-aurora']['platforms']['android-x86']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-x86'
BRANCHES['mozilla-aurora']['platforms']['android-x86']['updates_enabled'] = True
# aurora nightlies should use our nightly signing server
BRANCHES['mozilla-aurora']['platforms']['linux']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-aurora']['platforms']['linux64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-aurora']['platforms']['win32']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-aurora']['platforms']['win64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-aurora']['platforms']['macosx64']['nightly_signing_servers'] = 'nightly-signing'
BRANCHES['mozilla-aurora']['l10n_extra_configure_args'] = ['--with-macbundlename-prefix=Firefox']
BRANCHES['mozilla-aurora']['enabled_products'] = ['firefox', 'mobile']

######## mozilla-esr38
BRANCHES['mozilla-esr38']['repo_path'] = 'releases/mozilla-esr38'
BRANCHES['mozilla-esr38']['update_channel'] = 'nightly-esr38'
BRANCHES['mozilla-esr38']['l10n_repo_path'] = 'releases/l10n/mozilla-release'
BRANCHES['mozilla-esr38']['enable_weekly_bundle'] = True
BRANCHES['mozilla-esr38']['start_hour'] = [0]
BRANCHES['mozilla-esr38']['start_minute'] = [15]
BRANCHES['mozilla-esr38']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-esr38']['enable_mac_a11y'] = True
BRANCHES['mozilla-esr38']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-esr38']['enable_l10n'] = False
BRANCHES['mozilla-esr38']['enable_l10n_onchange'] = False
BRANCHES['mozilla-esr38']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-esr38']['l10n_platforms'] = ['linux', 'linux64', 'win32', 'macosx64']
BRANCHES['mozilla-esr38']['l10nDatedDirs'] = True
BRANCHES['mozilla-esr38']['l10n_tree'] = 'fxesr38'
BRANCHES['mozilla-esr38']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-esr38'
BRANCHES['mozilla-esr38']['enable_nightly'] = True
BRANCHES['mozilla-esr38']['enable_nightly_everytime'] = False
BRANCHES['mozilla-esr38']['updates_enabled'] = False
BRANCHES['mozilla-esr38']['create_partial'] = False
BRANCHES['mozilla-esr38']['enable_blocklist_update'] = True
BRANCHES['mozilla-esr38']['enable_hsts_update'] = True
BRANCHES['mozilla-esr38']['enable_hpkp_update'] = True
BRANCHES['mozilla-esr38']['enable_valgrind'] = False
BRANCHES['mozilla-esr38']['enabled_products'] = ['firefox']

######## mozilla-b2g37_v2_2
BRANCHES['mozilla-b2g37_v2_2']['repo_path'] = 'releases/mozilla-b2g37_v2_2'
BRANCHES['mozilla-b2g37_v2_2']['update_channel'] = 'nightly-b2g37'
BRANCHES['mozilla-b2g37_v2_2']['l10n_repo_path'] = 'releases/l10n/mozilla-aurora'
BRANCHES['mozilla-b2g37_v2_2']['enable_weekly_bundle'] = True
BRANCHES['mozilla-b2g37_v2_2']['enable_perproduct_builds'] = True
BRANCHES['mozilla-b2g37_v2_2']['start_hour'] = [3]
BRANCHES['mozilla-b2g37_v2_2']['start_minute'] = [15]
BRANCHES['mozilla-b2g37_v2_2']['pgo_platforms'] = []
BRANCHES['mozilla-b2g37_v2_2']['enable_mac_a11y'] = True
BRANCHES['mozilla-b2g37_v2_2']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-b2g37_v2_2']['enable_l10n'] = False
BRANCHES['mozilla-b2g37_v2_2']['enable_l10n_onchange'] = False
BRANCHES['mozilla-b2g37_v2_2']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-b2g37_v2_2']['l10n_platforms'] = ['linux', 'linux64',
                                                    'win32', 'macosx64']
BRANCHES['mozilla-b2g37_v2_2']['l10nDatedDirs'] = True
BRANCHES['mozilla-b2g37_v2_2']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-b2g37_v2_2'
BRANCHES['mozilla-b2g37_v2_2']['enable_nightly'] = False
BRANCHES['mozilla-b2g37_v2_2']['create_partial'] = False
BRANCHES['mozilla-b2g37_v2_2']['enable_blocklist_update'] = False
BRANCHES['mozilla-b2g37_v2_2']['enable_hsts_update'] = True
BRANCHES['mozilla-b2g37_v2_2']['enable_hpkp_update'] = True
BRANCHES['mozilla-b2g37_v2_2']['enable_valgrind'] = False
BRANCHES['mozilla-b2g37_v2_2']['enabled_products'] = ['firefox']

######## mozilla-b2g37_v2_2r
BRANCHES['mozilla-b2g37_v2_2r']['repo_path'] = 'releases/mozilla-b2g37_v2_2r'
BRANCHES['mozilla-b2g37_v2_2r']['update_channel'] = 'nightly-b2g37-2.2r'
BRANCHES['mozilla-b2g37_v2_2r']['l10n_repo_path'] = 'releases/l10n/mozilla-aurora'
BRANCHES['mozilla-b2g37_v2_2r']['enable_weekly_bundle'] = False
BRANCHES['mozilla-b2g37_v2_2r']['enable_perproduct_builds'] = True
BRANCHES['mozilla-b2g37_v2_2r']['start_hour'] = [3]
BRANCHES['mozilla-b2g37_v2_2r']['start_minute'] = [15]
BRANCHES['mozilla-b2g37_v2_2r']['pgo_platforms'] = []
BRANCHES['mozilla-b2g37_v2_2r']['enable_mac_a11y'] = True
BRANCHES['mozilla-b2g37_v2_2r']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-b2g37_v2_2r']['enable_l10n'] = False
BRANCHES['mozilla-b2g37_v2_2r']['enable_l10n_onchange'] = False
BRANCHES['mozilla-b2g37_v2_2r']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-b2g37_v2_2r']['l10n_platforms'] = ['linux', 'linux64',
                                                    'win32', 'macosx64']
BRANCHES['mozilla-b2g37_v2_2r']['l10nDatedDirs'] = True
BRANCHES['mozilla-b2g37_v2_2r']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-b2g37_v2_2r'
BRANCHES['mozilla-b2g37_v2_2r']['enable_nightly'] = False
BRANCHES['mozilla-b2g37_v2_2r']['create_partial'] = False
BRANCHES['mozilla-b2g37_v2_2r']['enable_blocklist_update'] = False
BRANCHES['mozilla-b2g37_v2_2r']['enable_hsts_update'] = True
BRANCHES['mozilla-b2g37_v2_2r']['enable_hpkp_update'] = True
BRANCHES['mozilla-b2g37_v2_2r']['enable_valgrind'] = False
BRANCHES['mozilla-b2g37_v2_2r']['enabled_products'] = ['firefox']

######## mozilla-b2g44_v2_5
BRANCHES['mozilla-b2g44_v2_5']['repo_path'] = 'releases/mozilla-b2g44_v2_5'
BRANCHES['mozilla-b2g44_v2_5']['update_channel'] = 'nightly-b2g44-2.5'
BRANCHES['mozilla-b2g44_v2_5']['l10n_repo_path'] = 'releases/l10n/mozilla-aurora'
BRANCHES['mozilla-b2g44_v2_5']['enable_weekly_bundle'] = False
BRANCHES['mozilla-b2g44_v2_5']['enable_perproduct_builds'] = True
BRANCHES['mozilla-b2g44_v2_5']['start_hour'] = [3]
BRANCHES['mozilla-b2g44_v2_5']['start_minute'] = [45]
BRANCHES['mozilla-b2g44_v2_5']['pgo_platforms'] = []
BRANCHES['mozilla-b2g44_v2_5']['enable_mac_a11y'] = True
BRANCHES['mozilla-b2g44_v2_5']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['mozilla-b2g44_v2_5']['enable_l10n'] = False
BRANCHES['mozilla-b2g44_v2_5']['enable_l10n_onchange'] = False
BRANCHES['mozilla-b2g44_v2_5']['l10nNightlyUpdate'] = False
BRANCHES['mozilla-b2g44_v2_5']['l10n_platforms'] = ['linux', 'linux64',
                                                    'win32', 'macosx64']
BRANCHES['mozilla-b2g44_v2_5']['l10nDatedDirs'] = True
BRANCHES['mozilla-b2g44_v2_5']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-mozilla-b2g44_v2_5'
BRANCHES['mozilla-b2g44_v2_5']['enable_nightly'] = False
BRANCHES['mozilla-b2g44_v2_5']['create_partial'] = False
BRANCHES['mozilla-b2g44_v2_5']['enable_blocklist_update'] = False
BRANCHES['mozilla-b2g44_v2_5']['enable_hsts_update'] = True
BRANCHES['mozilla-b2g44_v2_5']['enable_hpkp_update'] = True
BRANCHES['mozilla-b2g44_v2_5']['enable_valgrind'] = False
BRANCHES['mozilla-b2g44_v2_5']['enabled_products'] = ['firefox']


######## b2g-ota
BRANCHES['b2g-ota']['repo_path'] = 'releases/b2g-ota'
BRANCHES['b2g-ota']['update_channel'] = 'b2g-ota'
BRANCHES['b2g-ota']['l10n_repo_path'] = 'l10n-central'
BRANCHES['b2g-ota']['enable_weekly_bundle'] = False
BRANCHES['b2g-ota']['enable_perproduct_builds'] = True
BRANCHES['b2g-ota']['start_hour'] = [3]
BRANCHES['b2g-ota']['start_minute'] = [45]
BRANCHES['b2g-ota']['pgo_platforms'] = []
BRANCHES['b2g-ota']['enable_mac_a11y'] = True
BRANCHES['b2g-ota']['unittest_build_space'] = 6
# L10n configuration
BRANCHES['b2g-ota']['enable_l10n'] = False
BRANCHES['b2g-ota']['enable_l10n_onchange'] = False
BRANCHES['b2g-ota']['l10nNightlyUpdate'] = False
BRANCHES['b2g-ota']['l10n_platforms'] = ['linux', 'linux64',
                                                    'win32', 'macosx64']
BRANCHES['b2g-ota']['l10nDatedDirs'] = True
BRANCHES['b2g-ota']['enUS_binaryURL'] = \
    GLOBAL_VARS['download_base_url'] + '/nightly/latest-b2g-ota'
BRANCHES['b2g-ota']['enable_nightly'] = False
BRANCHES['b2g-ota']['create_partial'] = False
BRANCHES['b2g-ota']['enable_blocklist_update'] = False
BRANCHES['b2g-ota']['enable_hsts_update'] = True
BRANCHES['b2g-ota']['enable_hpkp_update'] = True
BRANCHES['b2g-ota']['enable_valgrind'] = False
BRANCHES['b2g-ota']['enabled_products'] = ['firefox']

######## try
# Try-specific configs
BRANCHES['try']['stage_username'] = 'trybld'
BRANCHES['try']['stage_username_mobile'] = 'trybld'
BRANCHES['try']['stage_ssh_key'] = 'trybld_dsa'
BRANCHES['try']['stage_ssh_mobile_key'] = 'trybld_dsa'
BRANCHES['try']['stage_base_path'] = '/home/ftp/pub/firefox/try-builds'
BRANCHES['try']['stage_base_path_mobile'] = '/home/ftp/pub/firefox/try-builds'
BRANCHES['try']['enable_merging'] = False
BRANCHES['try']['enable_try'] = True
BRANCHES['try']['pgo_strategy'] = 'try'
BRANCHES['try']['package_dir'] = '%(who)s-%(got_revision)s/'
# This is a path, relative to HGURL, where the repository is located
# HGURL  repo_path should be a valid repository
BRANCHES['try']['repo_path'] = 'try'
BRANCHES['try']['start_hour'] = [3]
BRANCHES['try']['start_minute'] = [2]
# Disable Nightly builds
BRANCHES['try']['enable_nightly'] = False
BRANCHES['try']['enable_mac_a11y'] = True
BRANCHES['try']['enable_l10n'] = True
BRANCHES['try']['desktop_mozharness_repacks_enabled'] = True
BRANCHES['try']['l10n_platforms'] = ['linux', 'linux64', 'win32', 'macosx64',
                                     'win64']
BRANCHES['try']['enable_l10n_onchange'] = False
BRANCHES['try']['l10nNightlyUpdate'] = False
BRANCHES['try']['l10nDatedDirs'] = False
# need this or the master.cfg will bail
BRANCHES['try']['platforms']['linux']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['win32']['slaves'] = TRY_SLAVES['win64-rev2']
BRANCHES['try']['platforms']['win64']['slaves'] = TRY_SLAVES['win64-rev2']
BRANCHES['try']['platforms']['win64-debug']['slaves'] = TRY_SLAVES['win64-rev2']
BRANCHES['try']['platforms']['macosx64']['slaves'] = TRY_SLAVES['macosx64-lion']
BRANCHES['try']['platforms']['linux-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-asan']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-asan-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-st-an-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-tsan']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-sh-haz']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-br-haz']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['linux64-cc']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['win32-debug']['slaves'] = TRY_SLAVES['win64-rev2']
BRANCHES['try']['platforms']['macosx64-debug']['slaves'] = TRY_SLAVES['macosx64-lion']
BRANCHES['try']['platforms']['macosx64-st-an-debug']['slaves'] = TRY_SLAVES['macosx64-lion']
BRANCHES['try']['platforms']['android-api-9']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['android-api-11']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['android-api-9-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['android-api-11-debug']['slaves'] = TRY_SLAVES['mock']
BRANCHES['try']['platforms']['android-x86']['slaves'] = TRY_SLAVES['mock']
for platform in BRANCHES['try']['platforms'].keys():
    # Disable symbol upload across the board
    BRANCHES['try']['platforms'][platform]['upload_symbols'] = False
del BRANCHES['try']['platforms']['linux64-av']

######## generic branch configs
for branch in ACTIVE_PROJECT_BRANCHES:
    branchConfig = PROJECT_BRANCHES[branch]
    BRANCHES[branch]['product_name'] = branchConfig.get('product_name', None)
    BRANCHES[branch]['app_name'] = branchConfig.get('app_name', None)
    BRANCHES[branch]['brand_name'] = branchConfig.get('brand_name', None)
    BRANCHES[branch]['repo_path'] = branchConfig.get('repo_path', 'projects/' + branch)
    BRANCHES[branch]['enabled_products'] = branchConfig.get('enabled_products',
                                                            GLOBAL_VARS['enabled_products'])
    BRANCHES[branch]['enable_nightly'] = branchConfig.get('enable_nightly', False)
    BRANCHES[branch]['enable_nightly_everytime'] = branchConfig.get('enable_nightly_everytime', False)
    BRANCHES[branch]['enable_mobile'] = branchConfig.get('enable_mobile', True)
    BRANCHES[branch]['pgo_strategy'] = branchConfig.get('pgo_strategy', None)
    BRANCHES[branch]['periodic_start_hours'] = branchConfig.get('periodic_start_hours', range(0, 24, 6))
    BRANCHES[branch]['periodic_start_minute'] = branchConfig.get('periodic_start_minute', 30)
    BRANCHES[branch]['start_hour'] = branchConfig.get('start_hour', [4])
    BRANCHES[branch]['start_minute'] = branchConfig.get('start_minute', [2])
    # Enable unit tests
    BRANCHES[branch]['enable_mac_a11y'] = branchConfig.get('enable_mac_a11y', True)
    BRANCHES[branch]['unittest_build_space'] = branchConfig.get('unittest_build_space', 6)
    # L10n configuration is not set up for project_branches
    BRANCHES[branch]['enable_l10n'] = branchConfig.get('enable_l10n', False)
    BRANCHES[branch]['l10nNightlyUpdate'] = branchConfig.get('l10nNightlyUpdate', False)
    BRANCHES[branch]['l10nDatedDirs'] = branchConfig.get('l10nDatedDirs', False)
    # nightly updates
    BRANCHES[branch]['updates_enabled'] = branchConfig.get('updates_enabled', False)
    BRANCHES[branch]['update_channel'] = branchConfig.get('update_channel', 'nightly-%s' % branch)
    BRANCHES[branch]['create_partial'] = branchConfig.get('create_partial', False)
    BRANCHES[branch]['create_partial_l10n'] = branchConfig.get('create_partial_l10n', False)
    #make sure it has an ending slash
    BRANCHES[branch]['l10nUploadPath'] = \
        '/home/ftp/pub/mozilla.org/firefox/nightly/latest-' + branch + '-l10n/'
    BRANCHES[branch]['enUS_binaryURL'] = GLOBAL_VARS['download_base_url'] + branchConfig.get('enUS_binaryURL', '')
    if 'linux' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['linux']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = branch
    if 'android-api-9' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['android-api-9']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-9-' + branch
    if 'android-api-11' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['android-api-11']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-api-11-' + branch
    if 'android-x86' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['android-x86']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'android-x86-' + branch
    if 'linux64' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['linux64']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'linux64-' + branch
    if 'win32' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['win32']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = branch
    if 'macosx64' in BRANCHES[branch]['platforms']:
        BRANCHES[branch]['platforms']['macosx64']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'macosx64-' + branch
    # Platform-specific defaults/interpretation
    for platform in BRANCHES[branch]['platforms']:
        # point to the mozconfigs, default is generic
        if platform.endswith('debug') and 'android' not in platform:
            BRANCHES[branch]['platforms'][platform]['mozconfig'] = platform.split('-')[0] + '/' + branchConfig.get('mozconfig_dir', 'generic') + '/debug'
        else:
            BRANCHES[branch]['platforms'][platform]['mozconfig'] = platform + '/' + branchConfig.get('mozconfig_dir', 'generic') + '/nightly'
        # Project branches should be allowed to override the signing servers.
        # If a branch does not set dep_signing_servers, it should be set to the global default.
        BRANCHES[branch]['platforms'][platform]['dep_signing_servers'] = branchConfig.get('platforms', {}).get(platform, {}).get('dep_signing_servers',
                                                                         PLATFORM_VARS[platform].get('dep_signing_servers'))

        # If a branch does not set nightly_signing_servers, first check if it wants
        # a different signing server set for all platforms, if not it should be set to
        # its dep signing server, which may have already been set to the global default.
        BRANCHES[branch]['platforms'][platform]['nightly_signing_servers'] = \
            branchConfig.get('nightly_signing_servers', branchConfig.get('platforms', {}).get(
                             platform, {}).get('nightly_signing_servers',
                             BRANCHES[branch]['platforms'][platform]['dep_signing_servers']))

# Expand out the branch_projects into a full PROJECT object per branch. This
# must come after the BRANCHES configuration above, so that
# BRANCHES[*]['enable_try'] is set when appropriate.
for b, branch in BRANCHES.items():
    for name in branch.get('branch_projects', []):
        branch_project = BRANCH_PROJECTS[name]
        if branch.get('enable_try', False) != branch_project.get('enable_try', False):
            continue

        project = deepcopy(branch_project)
        project['project_name'] = name
        project['branch'] = b
        project['branchconfig'] = branch
        branch_project_name = '%s__%s' % (name, b)
        assert branch_project_name not in PROJECTS, '%s already in PROJECTS' % name
        PROJECTS[branch_project_name] = project

PROJECTS["spidermonkey_tier_1__alder"]["enable_schedulers"] = False

# ant test on try
## ant rides the trains (Bug 971841)
# for name, branch in items_before(BRANCHES, 'gecko_version', 30):
for name, branch in BRANCHES.items():
    if "try" in name:
        continue # Remove this condition when we switch to riding trains
    for plat, pc in branch['platforms'].items():
        if 'mock_packages' in pc and "android" in plat:
            pc['mock_packages'] = \
                [x for x in pc['mock_packages'] if x not in (
                    'ant', 'ant-apache-regexp',
                )]

# mozilla-central's gecko version
mc_gecko_version = BRANCHES['mozilla-central']['gecko_version']

# Static analysis happens only on m-c and derived branches.
for name, branch in items_before(BRANCHES, 'gecko_version', mc_gecko_version):
    if 'linux64-st-an-debug' in branch['platforms']:
        del branch['platforms']['linux64-st-an-debug']
    if 'macosx64-st-an-debug' in branch['platforms']:
        del branch['platforms']['macosx64-st-an-debug']

# Only test pretty names on train branches, not m-c or project branches.
for branch in ("mozilla-aurora", "mozilla-beta", "mozilla-release",
               "mozilla-esr38"):
    for platform in ("linux", "linux64", "macosx64", "win32", "win64"):
        if platform in BRANCHES[branch]['platforms']:
            BRANCHES[branch]['platforms'][platform]['test_pretty_names'] = True

# B2G's INBOUND
for b in ('b2g-inbound',):
    for p in BRANCHES[b]['platforms'].keys():
        if 'linux' not in p:
            BRANCHES[b]['platforms'][p]['enable_checktests'] = False
# END B2G's INBOUND

ma_gecko_version = BRANCHES['mozilla-aurora']['gecko_version']
# enable mozharness desktop builds on m-a, m-c, and m-c related branches
for name, branch in items_at_least(BRANCHES, 'gecko_version', ma_gecko_version):
    # if true, any platform with mozharness_desktop_build in its config
    # will use mozharness instead of MozillaBuildFactory
    branch['desktop_mozharness_builds_enabled'] = True

# enable mozharness mobile builds on m-a, m-c, and m-c related branches
for name, branch in items_before(BRANCHES, 'gecko_version', ma_gecko_version):
    for platform in branch['platforms'].keys():
        if 'android' in platform:
            # we don't want to disable the branch level item: "desktop_mozharness_builds_enabled"
            # we do want to remove the platform level item: "mozharness_desktop_build"
            del branch['platforms'][platform]['mozharness_desktop_build']

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
