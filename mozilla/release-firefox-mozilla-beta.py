releaseConfig = {}
releaseConfig['disable_tinderbox_mail'] = True
releaseConfig['base_clobber_url'] = 'http://build.mozilla.org/clobberer/always_clobber.php'

# Release Notification
releaseConfig['AllRecipients']       = ['<release@mozilla.com>','<release-mgmt@mozilla.com>','<Callek@gmail.com>']
releaseConfig['ImportantRecipients'] = ['<release-drivers@mozilla.org>',]
releaseConfig['AVVendorsRecipients'] = ['<av-vendor-release-announce@mozilla.org>',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'firefox'
releaseConfig['appName']             = 'browser'
releaseConfig['binaryName']          = releaseConfig['productName'].capitalize()
releaseConfig['oldBinaryName']       = releaseConfig['binaryName']
#  Current version info
releaseConfig['version']             = '14.0b7'
releaseConfig['appVersion']          = '14.0'
releaseConfig['milestone']           = '14.0'
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FIREFOX_14_0b7'
#  Old version info
releaseConfig['oldVersion']          = '14.0b6'
releaseConfig['oldAppVersion']       = '14.0'
releaseConfig['oldBuildNumber']      = 2
releaseConfig['oldBaseTag']          = 'FIREFOX_14_0b6'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['appVersion']
releaseConfig['nextMilestone']       = releaseConfig['milestone']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mozilla': {
        'name': 'mozilla-beta',
        'path': 'releases/mozilla-beta',
        'revision': '271b0e7e0728',
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
    'build/buildbot': 'production-0.8',
    'build/mozharness': 'default',
}

# Platform configuration
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64')
releaseConfig['notifyPlatforms']     = releaseConfig['enUSPlatforms']
releaseConfig['talosTestPlatforms']  = releaseConfig['enUSPlatforms']
releaseConfig['xulrunnerPlatforms']  = releaseConfig['enUSPlatforms']

# Unittests
releaseConfig['unittestPlatforms']   = ()
releaseConfig['enableUnittests']     = True

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
releaseConfig['patcherToolsTag']     = 'UPDATE_PACKAGING_R16'
releaseConfig['ftpServer']           = 'ftp.mozilla.org'
releaseConfig['stagingServer']       = 'stage.mozilla.org'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus3.mozilla.org'
releaseConfig['ausHost']             = 'aus3-staging.mozilla.org'
releaseConfig['ausUser']             = 'ffxbld'
releaseConfig['ausSshKey']           = 'auspush'
releaseConfig['releaseNotesUrl']     = None
releaseConfig['testOlderPartials']   = False
releaseConfig['verifyConfigs']       = {
    'linux':  'mozBeta-firefox-linux.cfg',
    'linux64':  'mozBeta-firefox-linux64.cfg',
    'macosx64': 'mozBeta-firefox-mac64.cfg',
    'win32':  'mozBeta-firefox-win32.cfg'
}
releaseConfig['mozconfigs']          = {
    'linux': 'browser/config/mozconfigs/linux32/release',
    'linux64': 'browser/config/mozconfigs/linux64/release',
    'macosx64': 'browser/config/mozconfigs/macosx-universal/release',
    'win32': 'browser/config/mozconfigs/win32/release',
}
releaseConfig['xulrunner_mozconfigs']          = {
    'linux': 'xulrunner/config/mozconfigs/linux32/xulrunner',
    'linux64': 'xulrunner/config/mozconfigs/linux64/xulrunner',
    'macosx64': 'xulrunner/config/mozconfigs/macosx-universal/xulrunner',
    'win32': 'xulrunner/config/mozconfigs/win32/xulrunner',
}
releaseConfig['releaseChannel']      = 'beta'

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
releaseConfig['releaseUptake']       = 3
releaseConfig['releasetestUptake']   = 1

# Misc configuration
releaseConfig['enable_repo_setup'] = False
releaseConfig['enableAutomaticPushToMirrors'] = True
