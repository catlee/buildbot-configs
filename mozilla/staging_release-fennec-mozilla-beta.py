releaseConfig = {}

# Release Notification
releaseConfig['AllRecipients']       = ['release@mozilla.com',]
releaseConfig['PassRecipients']      = ['release@mozilla.com',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[staging-release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'fennec'
releaseConfig['appName']             = 'mobile'
releaseConfig['binaryName']          = releaseConfig['productName'].capitalize()
releaseConfig['oldBinaryName']       = releaseConfig['binaryName']
releaseConfig['relbranchPrefix']     = 'MOBILE'
#  Current version info
releaseConfig['version']             = '6.0b1'
releaseConfig['appVersion']          = '6.0'
releaseConfig['milestone']           = '6.0'
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FENNEC_6_0b1'
#  Old version info
releaseConfig['oldVersion']          = '5.0b5'
releaseConfig['oldAppVersion']       = '5.0'
releaseConfig['oldBuildNumber']      = 1
releaseConfig['oldBaseTag']          = 'FENNEC_5_0b5'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = '6.0'
releaseConfig['nextMilestone']       = '6.0'
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mobile': {
        'name': 'mozilla-beta',
        'clonePath': 'releases/mozilla-beta',
        'path': 'users/stage-ffxbld/mozilla-beta',
        'revision': 'FIXME:',
        'relbranch': None,
        'bumpFiles': {
            'mobile/confvars.sh': {
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
releaseConfig['l10nRepoClonePath']   = 'releases/l10n/mozilla-beta'
releaseConfig['l10nRepoPath']        = 'users/stage-ffxbld'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mobile-beta.json'
releaseConfig['l10nJsonFile'] = releaseConfig['l10nRevisionFile']
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'users/stage-ffxbld/compare-locales': 'RELEASE_AUTOMATION',
    'users/stage-ffxbld/buildbot': 'production-0.8',
    'users/stage-ffxbld/partner-repacks': 'default',
}

# Platform configuration
releaseConfig['enUSPlatforms']        = ('linux-maemo5-gtk', 'linux-android',
                                         'linux-mobile', 'macosx-mobile',
                                         'win32-mobile')
releaseConfig['signedPlatforms']      = ('linux-android',)
releaseConfig['unittestPlatforms']    = ()
releaseConfig['talosTestPlatforms']   = ()
releaseConfig['enableUnittests']      = True

# L10n configuration
releaseConfig['l10nPlatforms']       = ('linux-mobile', 'macosx-mobile',
                                        'win32-mobile')
releaseConfig['l10nChunks']          = 2
releaseConfig['mergeLocales']        = True
releaseConfig['enableMultiLocale']   = True

# Mercurial account
releaseConfig['hgUsername']          = 'stage-ffxbld'
releaseConfig['hgSshKey']            = '~cltbld/.ssh/ffxbld_dsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'dev-stage01.build.sjc1.mozilla.com'
releaseConfig['stagingServer']       = 'dev-stage01.build.sjc1.mozilla.com'
releaseConfig['ausServerUrl']        = 'http://dev-stage01.build.sjc1.mozilla.com'
releaseConfig['ausUser']             = 'cltbld'
releaseConfig['ausSshKey']           = 'cltbld_dsa'

# Partner repack configuration
releaseConfig['doPartnerRepacks']       = False
releaseConfig['partnersRepoPath']       = 'users/stage-ffxbld/partner-repacks'
releaseConfig['partnerRepackPlatforms'] = ('linux-maemo5-gtk',)

# Misc configuration
releaseConfig['enable_repo_setup']       = False

releaseConfig['mozharness_config'] = {
    'linux-android':
    'multi_locale/staging_release_mozilla-beta_linux-android.json',
    'linux-maemo5-gtk':
    'multi_locale/staging_release_mozilla-beta_linux-maemo5-gtk.json',
}
releaseConfig['usePrettyNames']           = False
releaseConfig['disableBouncerEntries']    = True
releaseConfig['disableStandaloneRepacks'] = True
releaseConfig['disableL10nVerification']  = True
releaseConfig['disablePermissionCheck']   = True
releaseConfig['disableVirusCheck']        = True
releaseConfig['disablePushToMirrors']     = True


# Staging config
releaseConfig['build_tools_repo_path'] = "users/stage-ffxbld/tools"
releaseConfig['skip_release_download'] = True
