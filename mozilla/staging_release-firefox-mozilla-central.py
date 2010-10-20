releaseConfig = {}

releaseConfig['hgUsername']          = 'stage-ffxbld'
releaseConfig['hgSshKey']            = '~cltbld/.ssh/ffxbld_dsa'
releaseConfig['sourceRepoName']      = 'mozilla-central'
releaseConfig['sourceRepoClonePath'] = releaseConfig['sourceRepoName']
releaseConfig['sourceRepoPath']      = 'users/stage-ffxbld/mozilla-central'
releaseConfig['sourceRepoRevision']  = '633e895d5e84'
releaseConfig['relbranchOverride']   = 'GECKO20b5_20100831_RELBRANCH'
releaseConfig['l10nRepoClonePath']   = 'l10n-central'
releaseConfig['l10nRepoPath']        = 'users/stage-ffxbld'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mozilla-2.0'
releaseConfig['mergeLocales']        = True
releaseConfig['cvsroot']             = ':ext:stgbld@cvs.mozilla.org:/cvsroot'
releaseConfig['productName']         = 'firefox'
releaseConfig['appName']             = 'browser'
# Sometimes we need the application version to be different from what we "call"
# the build, eg public release candidates for a major release (3.1 RC1).
# appVersion and oldAppVersion are optional definitions used in places that
# don't care about what we call it. Eg, when version bumping we will bump to
# appVersion, not version.
releaseConfig['version']             = '4.0b6'
releaseConfig['appVersion']          = releaseConfig['version']
releaseConfig['milestone']           = '2.0b6'
releaseConfig['buildNumber']         = 2
releaseConfig['baseTag']             = 'FIREFOX_4_0b6'
releaseConfig['oldVersion']          = '4.0b5'
releaseConfig['oldAppVersion']       = releaseConfig['oldVersion']
releaseConfig['oldBuildNumber']      = 1
releaseConfig['oldBaseTag']          = 'FIREFOX_4_0b5'
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64')
releaseConfig['l10nPlatforms']       = releaseConfig['enUSPlatforms']
releaseConfig['talosTestPlatforms']  = releaseConfig['enUSPlatforms']
releaseConfig['unittestPlatforms']   = releaseConfig['enUSPlatforms']
releaseConfig['xulrunnerPlatforms']  = ()
releaseConfig['patcherConfig']       = 'moz20-branch-patcher2.cfg'
releaseConfig['patcherToolsTag']     = 'UPDATE_PACKAGING_R12'
releaseConfig['binaryName']          = releaseConfig['productName'].capitalize()
releaseConfig['oldBinaryName']       = releaseConfig['binaryName']
releaseConfig['ftpServer']           = 'ftp.mozilla.org'
releaseConfig['stagingServer']       = 'staging-stage.build.mozilla.org'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'http://staging-stage.build.mozilla.org'
releaseConfig['ausUser']             = 'cltbld'
releaseConfig['ausSshKey']           = 'cltbld_dsa'
releaseConfig['releaseNotesUrl']     = 'http://www.mozilla.com/%locale%/firefox/4.0b6/releasenotes/'
releaseConfig['testOlderPartials']   = False
releaseConfig['useBetaChannel']      = 0
releaseConfig['verifyConfigs']       = {
    'linux':  'moz20-firefox-linux.cfg',
    'linux64':  'moz20-firefox-linux64.cfg',
    'macosx64': 'moz20-firefox-mac64.cfg',
    'win32':  'moz20-firefox-win32.cfg'
}
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'build/partner-repacks'
releaseConfig['majorUpdateRepoPath'] = None
# Tuxedo/Bouncer related
releaseConfig['tuxedoConfig']        = 'firefox-tuxedo.ini'
releaseConfig['tuxedoServerUrl']     = 'https://tuxedo.stage.mozilla.com/api/'

