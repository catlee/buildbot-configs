releaseConfig = {}

# Release Notification
releaseConfig['AllRecipients']       = ['release@mozilla.com',]
releaseConfig['PassRecipients']      = ['release-drivers@mozilla.org',]
releaseConfig['AVVendorsRecipients'] = ['av-vendor-release-announce@mozilla.org',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'firefox'
releaseConfig['appName']             = 'browser'
releaseConfig['binaryName']          = releaseConfig['productName'].capitalize()
releaseConfig['oldBinaryName']       = releaseConfig['binaryName']
#  Current version info
releaseConfig['version']             = '7.0b4'
releaseConfig['appVersion']          = '7.0'
releaseConfig['milestone']           = '7.0'
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FIREFOX_7_0b4'
#  Old version info
releaseConfig['oldVersion']          = '7.0b3'
releaseConfig['oldAppVersion']       = '7.0'
releaseConfig['oldBuildNumber']      = 1
releaseConfig['oldBaseTag']          = 'FIREFOX_7_0b3'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = '7.0'
releaseConfig['nextMilestone']       = '7.0'
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mozilla': {
        'name': 'mozilla-beta',
        'path': 'releases/mozilla-beta',
        'revision': '6791db28b82f',
        'relbranch': None,
        'bumpFiles': {
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
            'js/src/config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
        }
    }
}
#  L10n repositories
releaseConfig['l10nRelbranch']       = None
releaseConfig['l10nRepoPath']        = 'releases/l10n/mozilla-beta'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mozilla-beta'
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_AUTOMATION',
    'build/buildbot': 'production-0.8'
}

# Platform configuration
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64')
releaseConfig['talosTestPlatforms']  = releaseConfig['enUSPlatforms']
releaseConfig['xulrunnerPlatforms']  = releaseConfig['enUSPlatforms']

# Unittests
releaseConfig['unittestPlatforms']   = ()
releaseConfig['enableUnittests'] = True

# L10n configuration
releaseConfig['l10nPlatforms']       = releaseConfig['enUSPlatforms']
releaseConfig['shippedLocalesPath']  = 'browser/locales/shipped-locales'
releaseConfig['l10nChunks']          = 6
releaseConfig['mergeLocales']        = True

# Mercurial account
releaseConfig['hgUsername']          = 'ffxbld'
releaseConfig['hgSshKey']            = '~cltbld/.ssh/ffxbld_dsa'

# Update-specific configuration
releaseConfig['cvsroot']             = ':ext:cltbld@cvs.mozilla.org:/cvsroot'
releaseConfig['patcherConfig']       = 'mozBeta-branch-patcher2.cfg'
releaseConfig['commitPatcherConfig'] = True
releaseConfig['patcherToolsTag']     = 'UPDATE_PACKAGING_R14'
releaseConfig['ftpServer']           = 'ftp.mozilla.org'
releaseConfig['stagingServer']       = 'stage-old.mozilla.org'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus2.mozilla.org'
releaseConfig['ausUser']             = 'cltbld'
releaseConfig['ausSshKey']           = 'cltbld_dsa'
releaseConfig['releaseNotesUrl']     = None
releaseConfig['testOlderPartials']   = False
releaseConfig['useBetaChannel']      = 0
releaseConfig['verifyConfigs']       = {
    'linux':  'mozBeta-firefox-linux.cfg',
    'linux64':  'mozBeta-firefox-linux64.cfg',
    'macosx64': 'mozBeta-firefox-mac64.cfg',
    'win32':  'mozBeta-firefox-win32.cfg'
}

# Partner repack configuration
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'build/partner-repacks'

# Major update configuration
releaseConfig['majorUpdateRepoPath'] = None
# Tuxedo/Bouncer configuration
releaseConfig['tuxedoConfig']        = 'firefox-tuxedo.ini'
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.mozilla.com/api/'
releaseConfig['extraBouncerPlatforms'] = ('solaris-sparc', 'solaris-i386',
                                          'opensolaris-sparc',
                                          'opensolaris-i386')

# Misc configuration
releaseConfig['enable_repo_setup'] = False
