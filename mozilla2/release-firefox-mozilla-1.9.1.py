hgUsername         = 'ffxbld'
hgSshKey           = '~cltbld/.ssh/ffxbld_dsa'
sourceRepoName     = 'mozilla-1.9.1'
sourceRepoPath     = 'releases/mozilla-1.9.1'
sourceRepoRevision = 'ae51fe8759e3'
relbranchOverride  = ''
l10nRepoPath       = 'releases/l10n-mozilla-1.9.1'
l10nRevisionFile   = 'l10n-changesets'
# mergeLocales allows missing localized strings to be filled in by their en-US
# equivalent string. This is on (True) by default for nightly builds, but
# should be False for releases *EXCEPT* alphas and early betas. If in doubt,
# ask release-drivers.
mergeLocales       = False
cvsroot            = ':ext:cltbld@cvs.mozilla.org:/cvsroot'
productName        = 'firefox'
appName            = 'browser'
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version            = '3.5.11'
appVersion         = version
milestone          = '1.9.1.11'
buildNumber        = 1
baseTag            = 'FIREFOX_3_5_11'
oldVersion         = '3.5.10'
oldAppVersion      = oldVersion
oldBuildNumber     = 1
oldBaseTag         = 'FIREFOX_3_5_10'
enUSPlatforms      = ('linux', 'win32', 'macosx')
l10nPlatforms      = enUSPlatforms
patcherConfig      = 'moz191-branch-patcher2.cfg'
patcherToolsTag    = 'UPDATE_PACKAGING_R11'
binaryName         = productName.capitalize()
oldBinaryName      = binaryName
ftpServer          = 'ftp.mozilla.org'
stagingServer      = 'stage-old.mozilla.org'
talosTestPlatforms = ()
unittestPlatforms  = ()
xulrunnerPlatforms = enUSPlatforms
bouncerServer      = 'download.mozilla.org'
ausServerUrl       = 'https://aus2.mozilla.org'
ausUser            = 'cltbld'
ausSshKey          = 'cltbld_dsa'
releaseNotesUrl    = None
useBetaChannel     = 1
verifyConfigs      = {'linux':  'moz191-firefox-linux.cfg',
                      'macosx': 'moz191-firefox-mac.cfg',
                      'win32':  'moz191-firefox-win32.cfg'}
doPartnerRepacks    = False
partnersRepoPath    = 'build/partner-repacks'
majorUpdateRepoPath    = 'releases/mozilla-1.9.2'
majorUpdateToVersion   = '3.6.8'
majorUpdateAppVersion  = majorUpdateToVersion
majorUpdateBuildNumber = 1
majorUpdateBaseTag     = 'FIREFOX_3_6_8'
majorUpdateReleaseNotesUrl = 'http://www.mozilla.com/%locale%/firefox/3.6/details/index.html'
majorUpdatePatcherConfig = 'moz191-branch-major-update-patcher2.cfg'
majorUpdateVerifyConfigs = {'linux':  'moz191-firefox-linux-major.cfg',
                            'macosx': 'moz191-firefox-mac-major.cfg',
                            'win32':  'moz191-firefox-win32-major.cfg'}
# Tuxedo/Bouncer related
tuxedoConfig        = 'firefox-tuxedo.ini'
tuxedoServerUrl     = 'https://bounceradmin.mozilla.com/api/'
