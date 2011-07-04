hgUsername          = 'stage-ffxbld'
hgSshKey            = '~cltbld/.ssh/ffxbld_dsa'
sourceRepoName      = 'mozilla-1.9.2'
# This parameter (and it's l10n equivalent) is for staging only and necessary
# because the repo_setup builder needs to know where to clone repositories from.
# It is not used for anything else.
sourceRepoClonePath = 'releases/mozilla-1.9.2'
sourceRepoPath      = 'users/stage-ffxbld/mozilla-1.9.2'
sourceRepoRevision  = 'f029575f82e4'
relbranchOverride   = ''
l10nRepoClonePath   = 'releases/l10n-mozilla-1.9.2'
l10nRepoPath        = 'users/stage-ffxbld'
l10nRevisionFile    = 'l10n-changesets_mozilla-1.9.2'
# mergeLocales allows missing localized strings to be filled in by their en-US
# equivalent string. This is on (True) by default for nightly builds, but 
# should be False for releases *EXCEPT* alphas and early betas. If in doubt, 
# ask release-drivers.
mergeLocales        = False
cvsroot             = ':ext:stgbld@cvs.mozilla.org:/cvsroot'
productName         = 'firefox'
appName             = 'browser'
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version             = '3.6b1'
appVersion          = version
milestone           = '1.9.2b1'
buildNumber         = 1
baseTag             = 'FIREFOX_3_6b1'
oldVersion          = '3.6a1'
oldAppVersion       = oldVersion
oldBuildNumber      = 1
oldBaseTag          = 'FIREFOX_3_6a1'
enUSPlatforms       = ('linux', 'win32', 'macosx')
l10nPlatforms       = ('linux', 'win32', 'macosx')
talosTestPlatforms  = ('linux', 'win32', 'macosx')
unittestPlatforms   = ('linux', 'win32', 'macosx')
xulrunnerPlatforms  = enUSPlatforms
patcherConfig       = 'moz192-branch-patcher2.cfg'
patcherToolsTag     = 'UPDATE_PACKAGING_R11'
binaryName          = productName.capitalize()
oldBinaryName       = binaryName
ftpServer           = 'ftp.mozilla.org'
stagingServer       = 'dev-stage01.build.sjc1.mozilla.com'
bouncerServer       = 'download.mozilla.org'
ausServerUrl        = 'http://dev-stage01.build.sjc1.mozilla.com'
ausUser             = 'cltbld'
ausSshKey           = 'cltbld_dsa'
testOlderPartials   = True
releaseNotesUrl     = None
useBetaChannel      = 0
# TODO: create these files before 3.6b1
verifyConfigs       = {'linux':  'moz192-firefox-linux.cfg',
                       'macosx': 'moz192-firefox-mac.cfg',
                       'win32':  'moz192-firefox-win32.cfg'}
doPartnerRepacks    = True
partnersRepoPath    = 'build/partner-repacks'
majorUpdateRepoPath = None
# Tuxedo/Bouncer related
tuxedoConfig        = 'firefox-tuxedo.ini'
tuxedoServerUrl     = 'https://tuxedo.stage.mozilla.com/api/'
