releaseConfig = {}

# Release Notification
#  not used yet
# Basic product configuration
#  Names for the product/files
releaseConfig['productName']                = 'seamonkey'
releaseConfig['brandName']                  = 'SeaMonkey'
releaseConfig['appName']                    = 'suite'
#  Current version info
releaseConfig['version']                    = '2.9b2'
releaseConfig['appVersion']                 = '2.9'
releaseConfig['milestone']                  = '12.0'
releaseConfig['buildNumber']                = 1
releaseConfig['baseTag']                    = 'SEAMONKEY_2_9b2'
#  Old version info
releaseConfig['oldVersion']                 = '2.9b1'
releaseConfig['oldAppVersion']              = '2.9'
releaseConfig['oldBuildNumber']             = 1
releaseConfig['oldBaseTag']                 = 'SEAMONKEY_2_9b1'
releaseConfig['oldRepoPath']                = 'releases/comm-beta'
#  Next (nightly) version info
#     not yet available
#  Repository configuration, for tagging
releaseConfig['skip_tag']                   = False
releaseConfig['relbranchPrefix']            = 'SEA_COMM'
releaseConfig['sourceRepoName']             = 'comm-beta' # buildbot branch name
releaseConfig['sourceRepoPath']             = 'releases/comm-beta'
releaseConfig['sourceRepoRevision']         = 'ad8f79a72aa2'
releaseConfig['relbranchOverride']          = ''
#releaseConfig['productVersionFile']        = 'suite/config/version-20.txt'
releaseConfig['productVersionFile']         = ''
#   Mozilla
releaseConfig['mozillaRepoPath']            = 'releases/mozilla-beta'
releaseConfig['mozillaRepoRevision']        = 'FIREFOX_12_0b3_BUILD1'
releaseConfig['mozillaRelbranchOverride']   = 'GECKO120_2012032804_RELBRANCH' # put Gecko relbranch here that we base upon
#   Inspector
releaseConfig['inspectorRepoPath']          = 'dom-inspector' # leave empty if inspector is not to be tagged
releaseConfig['inspectorRepoRevision']      = 'b72c3dc211a0'
releaseConfig['inspectorRelbranchOverride'] = 'DOMI_2_0_10'
#   Venkman
releaseConfig['venkmanRepoPath']            = 'venkman' # leave empty if venkman is not to be tagged
releaseConfig['venkmanRepoRevision']        = 'VENKMAN_RELEASE_0_9_89'
releaseConfig['venkmanRelbranchOverride']   = ''
#   Chatzilla
releaseConfig['chatzillaRepoPath']          = 'chatzilla' # leave empty if chatzilla is not to be tagged
releaseConfig['chatzillaRepoRevision']      = 'CHATZILLA_0_9_88_1_RELEASE'
releaseConfig['chatzillaRelbranchOverride'] = ''
#  L10n repositories
releaseConfig['l10nRepoPath']               = 'releases/l10n/mozilla-beta'
releaseConfig['l10nRelbranchOverride']      = ''
releaseConfig['l10nRevisionFile']           = 'l10n-changesets-comm-beta'
#  Support repositories
#   not used yet

# Platform configuration
releaseConfig['enUSPlatforms']              = ('linux', 'linux64', 'win32', 'macosx64')
releaseConfig['talosTestPlatforms']         = ()

# Unittests
releaseConfig['unittestPlatforms']          = ()

# L10n configuration
releaseConfig['l10nPlatforms']              = ('linux', 'win32', 'macosx64')
releaseConfig['mergeLocales']               = True

# Mercurial account
releaseConfig['hgUsername']                 = 'seabld'
releaseConfig['hgSshKey']                   = '~seabld/.ssh/seabld_dsa'

# Update-specific configuration
releaseConfig['cvsroot']                    = ':ext:seabld@cvs.mozilla.org:/cvsroot' # for patcher, etc.
releaseConfig['patcherConfig']              = 'mozBeta-seamonkey-branch-patcher2.cfg'
releaseConfig['patcherToolsTag']            = 'UPDATE_PACKAGING_R14'
releaseConfig['binaryName']                 = releaseConfig['brandName']
releaseConfig['oldBinaryName']              = releaseConfig['binaryName']
releaseConfig['ftpServer']                  = 'ftp.mozilla.org'
releaseConfig['stagingServer']              = 'stage-old.mozilla.org'
releaseConfig['bouncerServer']              = 'download.mozilla.org'
releaseConfig['ausServerUrl']               = 'https://aus2-community.mozilla.org'
releaseConfig['testOlderPartials']          = False
releaseConfig['releaseNotesUrl']            = None
releaseConfig['releaseChannel']             = 'beta'
releaseConfig['verifyConfigs']              = {
    'linux':  'mozBeta-seamonkey-linux.cfg',
    'macosx64': 'mozBeta-seamonkey-mac64.cfg',
    'win32':  'mozBeta-seamonkey-win32.cfg'
}
releaseConfig['mozconfigs']                 = {
    'linux': 'suite/config/mozconfigs/linux32/release',
    'linux64': 'suite/config/mozconfigs/linux64/release',
    'macosx64': 'suite/config/mozconfigs/macosx-universal/release',
    'win32': 'suite/config/mozconfigs/win32/release',
}

# Major update configuration
releaseConfig['majorUpdateRepoPath']        = None

# Tuxedo/Bouncer related - XXX: atm not allowed for SeaMonkey
#releaseConfig['tuxedoConfig']              = 'seamonkey-tuxedo.ini'
#releaseConfig['tuxedoServerUrl']           = 'https://bounceradmin.mozilla.com/api/'
