hgUsername         = 'ffxbld'
hgSshKey           = '~cltbld/.ssh/ffxbld_dsa'
sourceRepoName     = 'mozilla-1.9.1'
sourceRepoPath     = 'releases/mozilla-1.9.1'
sourceRepoRevision = '3d9704097cd8'
relbranchOverride  = 'GECKO191b3_20090304_RELBRANCH'
l10nRepoPath       = 'releases/l10n-mozilla-1.9.1'
l10nRevisionFile   = 'l10n-changesets'
cvsroot            = ':ext:cltbld@cvs.mozilla.org:/cvsroot'
productName        = 'firefox'
appName            = 'browser'
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version            = '3.1b3'
appVersion         = version
milestone          = '1.9.1b3'
buildNumber        = 2
baseTag            = 'FIREFOX_3_1b3'
oldVersion         = '3.1b2'
oldAppVersion      = oldVersion
oldBuildNumber     = 2
oldBaseTag         = 'FIREFOX_3_1b2'
releasePlatforms   = ('linux', 'win32', 'macosx')
patcherConfig      = 'moz191-branch-patcher2.cfg'
patcherToolsTag    = 'UPDATE_PACKAGING_R7'
ftpServer          = 'ftp.mozilla.org'
stagingServer      = 'stage-old.mozilla.org'
bouncerServer      = 'download.mozilla.org'
ausServerUrl       = 'https://aus2.mozilla.org'
useBetaChannel     = 0
linuxVerifyConfig  = 'moz191-firefox-linux.cfg'
macVerifyConfig    = 'moz191-firefox-mac.cfg'
win32VerifyConfig  = 'moz191-firefox-win32.cfg'
