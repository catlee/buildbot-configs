HGURL = 'http://hg.mozilla.org/'
HGHOST = 'hg.mozilla.org'
CONFIG_REPO_URL = 'http://hg.mozilla.org/build/buildbot-configs'
CONFIG_REPO_PATH = 'build/buildbot-configs'
COMPARE_LOCALES_REPO_PATH = 'build/compare-locales'
CONFIG_SUBDIR = 'calendar'
LOCALE_REPO_URL = 'http://hg.mozilla.org/releases/l10n-mozilla-1.9.1/%(locale)s'
OBJDIR = 'objdir-tb'
STAGE_USERNAME = 'calbld'
STAGE_SERVER = 'stage.mozilla.org'
STAGE_GROUP = 'calendar'
STAGE_SSH_KEY = 'calbld_dsa'
AUS2_USER = 'calbld'
AUS2_HOST = 'aus-staging.sj.mozillamessaging.com'
DOWNLOAD_BASE_URL = 'http://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird'
PRODUCT = 'mail'
MOZ_APP_NAME = 'sunbird'

ORGANIZATION = 'community'

BUILDERS = {
    'linux': {
        'community': [ 'cb-sb-linux-tbox' ],
    },
    'macosx': {
        '10.5': {
            'community': [ 'cb-xserve03' ],
        },
    },
    'win32': {
        'community': [ 'cb-sb-win32-tbox' ],
    },
}

DEFAULTS = {
    'factory':                'build',
    'hgurl':                  HGURL,
    'branch_name':            'comm-central',
    'stage_base_path':        '/home/ftp/pub/mozilla.org/calendar',
    'mozilla_central_branch': 'releases/mozilla-1.9.1',
    'add_poll_branches':      [ 'dom-inspector' ],
    'period':                 60 * 60 * 8,
    'nightly_hour':          [3],
    'nightly_minute':        [0],
    'irc':                    True,
    'clobber_url':            "http://build.mozillamessaging.com/clobberer/",
    'builder_type':           "build",
    'tinderbox_tree':         "ThunderbirdTest",
    'codesighs':               False,
    'mozmill':                 False,
    'product_name':           'sunbird',
    'brand_name':             'Sunbird',
    'app_name':			      'calendar',
    'build_space':            8,
    'l10n_nightly_updates':    False,

    'stage_username':		STAGE_USERNAME,
    'stage_server':		STAGE_SERVER,
    'stage_group':		STAGE_GROUP,
    'stage_ssh_key':		STAGE_SSH_KEY,
    
    # Unit Test
    'client_py_args':       ['--skip-comm', '--skip-chatzilla', '--skip-venkman', '--hg-options=--verbose --time'],

    'clobber_url':  "http://build.mozillamessaging.com/clobberer/",
    'build_tools_repo': "build/tools",
    'hg_rev_shortnames': {
      'mozilla-central':        'moz',
      'comm-central':           'cc',
      'dom-inspector':          'domi',
      'releases/mozilla-1.9.1': 'moz191',
      'releases/mozilla-1.9.2': 'moz192',
      'releases/comm-1.9.1':    'cc191',
    }
}

# All branches that are to be built MUST be listed here.
BRANCHES = {
    'comm-1.9.2-lightning': {},
    'comm-central-lightning': {},
}

######## lightning-hg
# All platforms being built for this branch MUST be listed here.
BRANCHES['comm-1.9.2-lightning']['platforms'] = {
    'linux': {},
    'win32': {},
    'macosx': {}
}

BRANCHES['comm-1.9.2-lightning']['mozilla_central_branch'] = 'releases/mozilla-1.9.2'
BRANCHES['comm-1.9.2-lightning']['branch_name'] = 'comm-1.9.2'
BRANCHES['comm-1.9.2-lightning']['hg_branch'] = 'releases/comm-1.9.2'
BRANCHES['comm-1.9.2-lightning']['client_py_args'] = ['--skip-comm', '--skip-chatzilla', '--skip-venkman'] + ['--mozilla-repo=http://hg.mozilla.org/releases/mozilla-1.9.2']
BRANCHES['comm-1.9.2-lightning']['cvsroot'] = ':ext:calbld@cvs.mozilla.org:/cvsroot'
BRANCHES['comm-1.9.2-lightning']['mozconfig'] = 'mozconfig-lightning'
BRANCHES['comm-1.9.2-lightning']['period'] = 60 * 60 * 6
BRANCHES['comm-1.9.2-lightning']['package'] = True
BRANCHES['comm-1.9.2-lightning']['upload_stage'] = True
BRANCHES['comm-1.9.2-lightning']['upload_complete_mar'] = False
#Might be better off per-platform instead of per-branch here.
BRANCHES['comm-1.9.2-lightning']['upload_glob'] = "mozilla/dist/xpi-stage/{lightning,gdata-provider}.xpi"
BRANCHES['comm-1.9.2-lightning']['stage_username'] = 'calbld'
BRANCHES['comm-1.9.2-lightning']['stage_base_path'] = '/home/ftp/pub/mozilla.org/calendar/lightning'
BRANCHES['comm-1.9.2-lightning']['stage_group'] = 'calendar'
BRANCHES['comm-1.9.2-lightning']['stage_ssh_key'] = 'calbld_dsa'
BRANCHES['comm-1.9.2-lightning']['codesighs'] = False
BRANCHES['comm-1.9.2-lightning']['l10n'] = False
BRANCHES['comm-1.9.2-lightning']['irc_nick'] = 'calbuild'
BRANCHES['comm-1.9.2-lightning']['irc_channels'] = [ 'maildev', 'calendar' ]
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['base_name'] = 'Linux comm-1.9.2 lightning'
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['base_name'] = 'WINNT 5.2 comm-1.9.2 lightning'
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['base_name'] = 'MacOSX 10.5 comm-1.9.2 lightning'
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['profiled_build'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['profiled_build'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['profiled_build'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['milestone'] = "comm-1.9.2/linux-xpi"
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['milestone'] = "comm-1.9.2/win32-xpi"
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['milestone'] = "comm-1.9.2/macosx-xpi"
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['upload_glob'] = "mozilla/dist/universal/xpi-stage/{lightning,gdata-provider}.xpi"

# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-1.9.2-lightning']['create_snippet'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['update_platform'] = 'Linux_x86-gcc3'
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['update_platform'] = 'WINNT_x86-msvc'
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['update_platform'] = 'Darwin_Universal-gcc3'
# If True, 'make buildsymbols' and 'make uploadsymbols' will be run
# SYMBOL_SERVER_* variables are setup in the environment section below
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['upload_symbols'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['upload_symbols'] = False
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['upload_symbols'] = False
BRANCHES['comm-1.9.2-lightning']['tinderbox_tree'] = 'Calendar1.0'
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['slaves'] = BUILDERS['linux']['community']
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['slaves'] = BUILDERS['win32']['community']
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['slaves'] = BUILDERS['macosx']['10.5']['community']

# This is used in a bunch of places where something needs to be run from
# the objdir. This is necessary because of universal builds on Mac
# creating subdirectories inside of the objdir.
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['platform_objdir'] = OBJDIR
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['platform_objdir'] = OBJDIR
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['platform_objdir'] = '%s/ppc' % OBJDIR
BRANCHES['comm-1.9.2-lightning']['platforms']['linux']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
}
BRANCHES['comm-1.9.2-lightning']['platforms']['win32']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
}
BRANCHES['comm-1.9.2-lightning']['platforms']['macosx']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
    'DISABLE_LIGHTNING_INSTALL': '1',
}

######## lightning-trunk
# All platforms being built for this branch MUST be listed here.
BRANCHES['comm-central-lightning']['platforms'] = {
    'linux': {},
    'win32': {},
    'macosx': {}
}
BRANCHES['comm-central-lightning']['nightly'] = False
BRANCHES['comm-central-lightning']['mozilla_central_branch'] = 'mozilla-central'
BRANCHES['comm-central-lightning']['branch_name'] = 'comm-central'
BRANCHES['comm-central-lightning']['hg_branch'] = 'comm-central'
BRANCHES['comm-central-lightning']['client_py_args'] = ['--skip-comm', '--skip-chatzilla', '--skip-venkman']
BRANCHES['comm-central-lightning']['cvsroot'] = ':ext:calbld@cvs.mozilla.org:/cvsroot'
BRANCHES['comm-central-lightning']['mozconfig'] = 'mozconfig-lightning'
BRANCHES['comm-central-lightning']['period'] = 60 * 60 * 6
BRANCHES['comm-central-lightning']['package'] = True
BRANCHES['comm-central-lightning']['upload_stage'] = True
BRANCHES['comm-central-lightning']['upload_complete_mar'] = False
#Might be better off per-platform instead of per-branch here.
BRANCHES['comm-central-lightning']['upload_glob'] = "mozilla/dist/xpi-stage/{lightning,gdata-provider}.xpi"
BRANCHES['comm-central-lightning']['stage_username'] = 'calbld'
BRANCHES['comm-central-lightning']['stage_base_path'] = '/home/ftp/pub/mozilla.org/calendar/lightning'
BRANCHES['comm-central-lightning']['stage_group'] = 'calendar'
BRANCHES['comm-central-lightning']['stage_ssh_key'] = 'calbld_dsa'
BRANCHES['comm-central-lightning']['codesighs'] = False
BRANCHES['comm-central-lightning']['l10n'] = False
BRANCHES['comm-central-lightning']['irc_nick'] = 'lt-trunk-builds'
BRANCHES['comm-central-lightning']['irc_channels'] = [ 'calendar' ]
BRANCHES['comm-central-lightning']['platforms']['linux']['base_name'] = 'Linux comm-central lightning'
BRANCHES['comm-central-lightning']['platforms']['win32']['base_name'] = 'WINNT 5.2 comm-central lightning'
BRANCHES['comm-central-lightning']['platforms']['macosx']['base_name'] = 'MacOSX 10.5 comm-central lightning'
BRANCHES['comm-central-lightning']['platforms']['linux']['profiled_build'] = False
BRANCHES['comm-central-lightning']['platforms']['win32']['profiled_build'] = False
BRANCHES['comm-central-lightning']['platforms']['macosx']['profiled_build'] = False
BRANCHES['comm-central-lightning']['platforms']['linux']['milestone'] = "comm-central/linux-xpi"
BRANCHES['comm-central-lightning']['platforms']['win32']['milestone'] = "comm-central/win32-xpi"
BRANCHES['comm-central-lightning']['platforms']['macosx']['milestone'] = "comm-central/macosx-xpi"
BRANCHES['comm-central-lightning']['platforms']['macosx']['upload_glob'] = "mozilla/dist/universal/xpi-stage/{lightning,gdata-provider}.xpi"

# If True, a complete update snippet for this branch will be generated and
# uploaded to. Any platforms with 'debug' in them will not have snippets
# generated.
BRANCHES['comm-central-lightning']['create_snippet'] = False
BRANCHES['comm-central-lightning']['platforms']['linux']['update_platform'] = 'Linux_x86-gcc3'
BRANCHES['comm-central-lightning']['platforms']['win32']['update_platform'] = 'WINNT_x86-msvc'
BRANCHES['comm-central-lightning']['platforms']['macosx']['update_platform'] = 'Darwin_Universal-gcc3'
# If True, 'make buildsymbols' and 'make uploadsymbols' will be run
# SYMBOL_SERVER_* variables are setup in the environment section below
BRANCHES['comm-central-lightning']['platforms']['linux']['upload_symbols'] = False
BRANCHES['comm-central-lightning']['platforms']['win32']['upload_symbols'] = False
BRANCHES['comm-central-lightning']['platforms']['macosx']['upload_symbols'] = False
BRANCHES['comm-central-lightning']['tinderbox_tree'] = 'Sunbird'
BRANCHES['comm-central-lightning']['platforms']['linux']['slaves'] = BUILDERS['linux']['community']
BRANCHES['comm-central-lightning']['platforms']['win32']['slaves'] = BUILDERS['win32']['community']
BRANCHES['comm-central-lightning']['platforms']['macosx']['slaves'] = BUILDERS['macosx']['10.5']['community']

# This is used in a bunch of places where something needs to be run from
# the objdir. This is necessary because of universal builds on Mac
# creating subdirectories inside of the objdir.
BRANCHES['comm-central-lightning']['platforms']['linux']['platform_objdir'] = OBJDIR
BRANCHES['comm-central-lightning']['platforms']['win32']['platform_objdir'] = OBJDIR
BRANCHES['comm-central-lightning']['platforms']['macosx']['platform_objdir'] = '%s/ppc' % OBJDIR
BRANCHES['comm-central-lightning']['platforms']['linux']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
}
BRANCHES['comm-central-lightning']['platforms']['win32']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
}
BRANCHES['comm-central-lightning']['platforms']['macosx']['env'] = {'CVS_RSH': 'ssh',
    'MOZ_OBJDIR': OBJDIR,
    'TINDERBOX_OUTPUT': '1',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
    'DISABLE_LIGHTNING_INSTALL': '1',
}

# Release automation expect to find these
STAGE_BASE_PATH=DEFAULTS['stage_base_path']
COMPARE_LOCALES_TAG = 'RELEASE_AUTOMATION'
