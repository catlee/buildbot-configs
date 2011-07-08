hgUsername                 = 'seabld'
hgSshKey                   = '~seabld/.ssh/seabld_dsa'
relbranchPrefix            = 'COMM'
sourceRepoName             = 'comm-1.9.1' # buildbot branch name
sourceRepoPath             = 'releases/comm-1.9.1'
sourceRepoRevision         = 'b292e787146b'
relbranchOverride          = 'COMM19119_20110416_RELBRANCH'
mozillaRepoPath            = 'releases/mozilla-1.9.1'
mozillaRepoRevision        = 'FIREFOX_3_5_19_RELEASE'
mozillaRelbranchOverride   = 'GECKO19119_2011041408_RELBRANCH' # put Gecko relbranch here that we base upon
inspectorRepoPath          = 'dom-inspector' # leave empty if inspector is not to be tagged
inspectorRepoRevision      = 'f6c78804ebb4'
inspectorRelbranchOverride = 'COMM_1_9_1_BRANCH'
venkmanRepoPath            = 'venkman' # leave empty if venkman is not to be tagged
venkmanRepoRevision        = 'f13c813e4ec6'
venkmanRelbranchOverride   = 'COMM_1_9_1_BRANCH'
chatzillaRepoPath          = 'chatzilla' # leave empty if chatzilla is not to be tagged
chatzillaRepoRevision      = 'f5fd1b073bf8'
chatzillaRelbranchOverride = 'COMM_1_9_1_BRANCH'
l10nRepoPath               = 'releases/l10n-mozilla-1.9.1'
l10nRevisionFile           = 'l10n-changesets'
l10nRelbranchOverride      = 'COMM_1_9_1_BRANCH'
cvsroot                    = ':ext:seabld@cvs.mozilla.org:/cvsroot' # for patcher, etc.
productVersionFile         = 'suite/config/version-191.txt'
# mergeLocales allows missing localized strings to be filled in by their en-US
# equivalent string. This is on (True) by default for nightly builds, but
# should be False for releases *EXCEPT* alphas and early betas. If in doubt,
# ask release-drivers.
mergeLocales               = False
productName                = 'seamonkey'
brandName                  = 'SeaMonkey'
appName                    = 'suite'
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version                    = '2.0.14'
usePrettyLongVer           = True
appVersion                 = version
milestone                  = '1.9.1.19'
buildNumber                = 2
baseTag                    = 'SEAMONKEY_2_0_14'
oldVersion                 = '2.0.13'
oldAppVersion              = oldVersion
oldBuildNumber             = 1
oldBaseTag                 = 'SEAMONKEY_2_0_13'
oldRepoPath                = 'releases/comm-1.9.1'
enUSPlatforms              = ('linux', 'linux64', 'win32', 'macosx')
l10nPlatforms              = ('linux', 'win32', 'macosx')
patcherConfig              = 'moz191-seamonkey-branch-patcher2.cfg'
patcherToolsTag            = 'UPDATE_PACKAGING_R11_1'
binaryName                 = brandName
oldBinaryName              = binaryName
ftpServer                  = 'ftp.mozilla.org'
stagingServer              = 'stage-old.mozilla.org'
talosTestPlatforms         = ()
unittestPlatforms          = ()
bouncerServer              = 'download.mozilla.org'
ausServerUrl               = 'https://aus2-community.mozilla.org'
testOlderPartials          = True
releaseNotesUrl            = None
useBetaChannel             = 1
verifyConfigs              = {'linux':  'moz191-seamonkey-linux.cfg',
                              'macosx': 'moz191-seamonkey-mac.cfg',
                              'win32':  'moz191-seamonkey-win32.cfg'}
majorUpdateRepoPath        = 'releases/mozilla-release'
majorPatcherToolsTag       = 'UPDATE_PACKAGING_R11_1_MU'
majorUpdateSourceRepoPath  = 'releases/comm-release'
majorUpdatePatcherConfig  = 'moz191-seamonkey-branch-major-patcher2.cfg'
majorUpdateVerifyConfigs   = {'linux':  'moz191-seamonkey-linux-major.cfg',
                              'macosx': 'moz191-seamonkey-mac-major.cfg',
                              'win32':  'moz191-seamonkey-win32-major.cfg'}
majorUpdateToVersion       = '2.2'
majorUpdateAppVersion      = '2.2'
majorUpdateBaseTag         = 'SEAMONKEY_2_2'
majorUpdateBuildNumber     = 2
majorUpdateReleaseNotesUrl = 'https://www.mozilla.org/start/2.2/en-US/index.html'

# Tuxedo/Bouncer related - XXX: atm not allowed for SeaMonkey
#tuxedoConfig        = 'seamonkey-tuxedo.ini'
#tuxedoServerUrl     = 'https://bounceradmin.mozilla.com/api/'
