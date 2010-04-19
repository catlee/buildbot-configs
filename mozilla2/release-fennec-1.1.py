hgUsername          = 'ffxbld'
hgSshKey            = '~cltbld/.ssh/ffxbld_dsa'
mobileBranchNick    = 'mobile-1.9.2'
mozSourceRepoName      = 'mozilla-1.9.2'
# This parameter (and its l10n equivalent) is for staging only and necessary
# because the repo_setup builder needs to know where to clone repositories from.
# It is not used for anything else.
mozSourceRepoPath      = 'releases/mozilla-1.9.2'
mozSourceRepoRevision  = '838c05e99a8e'
mobileSourceRepoName      = 'mobile-browser'
mobileSourceRepoPath      = 'mobile-browser'
mobileSourceRepoRevision  = 'ce825c90cf36'
mozRelbranchOverride      = 'GECKO1925pre_20100414_RELBRANCH'
l10nRelbranchOverride     = 'GECKO1925pre_20100414_RELBRANCH'
mobileRelbranchOverride   = 'GECKO1925pre_20100414_RELBRANCH'
l10nRepoPath        = 'releases/l10n-mozilla-1.9.2'
l10nRevisionFile    = 'l10n-changesets_mobile-1.1.json'
productName         = 'fennec'
appName             = 'mobile'
mergeLocales        = True
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
version             = '1.1b1'
appVersion          = '1.1b1'
milestone           = '1.9.2.5pre'
buildNumber         = 2
baseTag             = 'FENNEC_1_1b1'
enUSPlatforms       = ('maemo',)
l10nPlatforms       = enUSPlatforms
enUSDesktopPlatforms = ('linux-i686', 'macosx-i686', 'win32-i686')
l10nDesktopPlatforms = ()
talosTestPlatforms  = ()
ftpServer           = 'ftp.mozilla.org'
stagingServer       = 'stage.mozilla.org'
stageBasePath       = '/home/ftp/pub/mobile/candidates'
base_enUS_binaryURL = 'http://%s/pub/mozilla.org/mobile/candidates/%s-candidates/build%d' % (ftpServer, version, buildNumber)
doPartnerRepacks    = False
partnersRepoPath    = 'build/partner-repacks'
partnerRepackPlatforms = ('maemo',)
