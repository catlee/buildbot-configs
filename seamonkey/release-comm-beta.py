hgUsername                 = 'seabld'
hgSshKey                   = '~seabld/.ssh/seabld_dsa'
relbranchPrefix            = 'SEA_COMM'
sourceRepoName             = 'comm-beta' # buildbot branch name
sourceRepoPath             = 'releases/comm-beta'
sourceRepoRevision         = '258499d66bf4'
relbranchOverride          = ''
mozillaRepoPath            = 'releases/mozilla-beta'
mozillaRepoRevision        = 'FIREFOX_10_0b5_BUILD1'
mozillaRelbranchOverride   = 'GECKO100_2012011807_RELBRANCH' # put Gecko relbranch here that we base upon
inspectorRepoPath          = 'dom-inspector' # leave empty if inspector is not to be tagged
inspectorRepoRevision      = '589ef9b749f5'
inspectorRelbranchOverride = 'DOMI_2_0_10'
venkmanRepoPath            = 'venkman' # leave empty if venkman is not to be tagged
venkmanRepoRevision        = 'a38583d7164a'
venkmanRelbranchOverride   = ''
chatzillaRepoPath          = 'chatzilla' # leave empty if chatzilla is not to be tagged
chatzillaRepoRevision      = '48d3ca3f72e4' # 0.9.88 but without the version change.
chatzillaRelbranchOverride = ''
l10nRepoPath               = 'releases/l10n/mozilla-beta'
l10nRelbranchOverride      = ''
l10nRevisionFile           = 'l10n-changesets-comm-beta'
cvsroot                    = ':ext:seabld@cvs.mozilla.org:/cvsroot' # for patcher, etc.
#productVersionFile         = 'suite/config/version-20.txt'
productVersionFile         = ''
# mergeLocales allows missing localized strings to be filled in by their en-US
# equivalent string. This is on (True) by default for nightly builds, but
# should be False for releases *EXCEPT* alphas and early betas. If in doubt,
# ask release-drivers.
mergeLocales               = True
productName                = 'seamonkey'
brandName                  = 'SeaMonkey'
appName                    = 'suite'
skip_tag                   =  False
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version                    = '2.7b4'
appVersion                 = '2.7'
milestone                  = '10.0'
buildNumber                = 1
baseTag                    = 'SEAMONKEY_2_7b4'
oldVersion                 = '2.7b3'
oldAppVersion              = '2.7'
oldBuildNumber             = 1
oldBaseTag                 = 'SEAMONKEY_2_7b3'
oldRepoPath                = 'releases/comm-beta'
enUSPlatforms              = ('linux', 'linux64', 'win32', 'macosx64')
l10nPlatforms              = ('linux', 'win32', 'macosx64')
patcherConfig              = 'mozBeta-seamonkey-branch-patcher2.cfg'
patcherToolsTag            = 'UPDATE_PACKAGING_R14'
binaryName                 = brandName
oldBinaryName              = binaryName
ftpServer                  = 'ftp.mozilla.org'
stagingServer              = 'stage-old.mozilla.org'
talosTestPlatforms         = ()
unittestPlatforms          = ()
bouncerServer              = 'download.mozilla.org'
ausServerUrl               = 'https://aus2-community.mozilla.org'
testOlderPartials          = False
releaseNotesUrl            = None
useBetaChannel             = 0
verifyConfigs              = {'linux':  'mozBeta-seamonkey-linux.cfg',
                              'macosx64': 'mozBeta-seamonkey-mac64.cfg',
                              'win32':  'mozBeta-seamonkey-win32.cfg'}
majorUpdateRepoPath        = None
# Tuxedo/Bouncer related - XXX: atm not allowed for SeaMonkey
#tuxedoConfig        = 'seamonkey-tuxedo.ini'
#tuxedoServerUrl     = 'https://bounceradmin.mozilla.com/api/'
