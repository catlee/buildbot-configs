# ATTENTION:
# If you are editing the non-template version of this file (eg, doesn't end
# with .template), your change WILL get overwritten. If you're adding, removing,
# or changing options as part of release automation changes you should be
# editing the .template instead. This file should only by edited directly if
# you're starting a release without Release Kickoff. You have been warned.
releaseConfig = {}
releaseConfig['disable_tinderbox_mail'] = True
releaseConfig['base_clobber_url'] = 'http://clobberer.pvt.build.mozilla.org/always_clobber.php'

# Release Notification
releaseConfig['AllRecipients']       = ['<release@mozilla.com>',
                                        '<release-mgmt@mozilla.com>',
                                        '<qa-drivers@mozilla.com>']
releaseConfig['ImportantRecipients'] = ['<release-drivers@mozilla.org>',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'fennec'
releaseConfig['stage_product']       = 'mobile'
releaseConfig['appName']             = 'mobile'
releaseConfig['relbranchPrefix']     = 'MOBILE'

# Function for bumping Android Version Code
# see bug 1040319
def bumpIntegerInFile(previousContents):
    return str(int(previousContents) + 1)

#  Current version info
releaseConfig['version']             = '31.2.0esr'
releaseConfig['appVersion']          = '31.2.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 2
releaseConfig['baseTag']             = 'FENNEC_31_2_0esr'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['version']
releaseConfig['nextMilestone']       = releaseConfig['version']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mobile': {
        'name': 'mozilla-esr31',
        'path': 'releases/mozilla-esr31',
        'revision': 'f5690f9ca229',
        'relbranch': None,
        'bumpFiles': {
            'mobile/android/confvars.sh': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
            'mobile/android/config/armv6_play_store_version_code.txt': {
                'version': bumpIntegerInFile,
                'nextVersion': bumpIntegerInFile,
            },
        }
    }
}
#  L10n repositories
releaseConfig['l10nRelbranch']       = None
releaseConfig['l10nRepoPath']        = 'releases/l10n/mozilla-release'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mobile-esr31.json'
releaseConfig['l10nJsonFile']        = releaseConfig['l10nRevisionFile']
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_AUTOMATION',
    'build/buildbot': 'production-0.8',
    'build/mozharness': 'production',
}

# Platform configuration
releaseConfig['enUSPlatforms']        = ('android-armv6',)
releaseConfig['notifyPlatforms']      = releaseConfig['enUSPlatforms']
releaseConfig['unittestPlatforms']    = ()
releaseConfig['talosTestPlatforms']   = ()
releaseConfig['enableUnittests']      = False

# L10n configuration
releaseConfig['l10nPlatforms']       = ()
releaseConfig['l10nNotifyPlatforms'] = releaseConfig['l10nPlatforms']
releaseConfig['mergeLocales']        = True
releaseConfig['enableMultiLocale']   = True

# Mercurial account
releaseConfig['hgUsername']          = 'ffxbld'
releaseConfig['hgSshKey']            = '~cltbld/.ssh/ffxbld_dsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'ftp.mozilla.org'
releaseConfig['stagingServer']       = 'stage.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus3.mozilla.org'
releaseConfig['ausHost']             = 'aus3-staging.mozilla.org'
releaseConfig['ausUser']             = 'ffxbld'
releaseConfig['ausSshKey']           = 'ffxbld_dsa'

# Partner repack configuration
releaseConfig['doPartnerRepacks']       = False
releaseConfig['partnersRepoPath']       = 'build/partner-repacks'
releaseConfig['partnerRepackPlatforms'] = ()

# mozconfigs
releaseConfig['mozconfigs']          = {
    'android-armv6': 'mobile/android/config/mozconfigs/android-armv6/release',
}
releaseConfig['releaseChannel']      = 'esr'

# Misc configuration
releaseConfig['enable_repo_setup']       = False

# Fennec specific
releaseConfig['usePrettyNames']           = False
releaseConfig['disableBouncerEntries']    = True
releaseConfig['disableStandaloneRepacks'] = True
releaseConfig['disablePermissionCheck']   = True
releaseConfig['disableVirusCheck']        = True
releaseConfig['enableUpdatePackaging']    = False
releaseConfig['balrog_api_root']          = None

releaseConfig['multilocale_config'] = {
    'platforms': {
        'android-armv6':
            'multi_locale/release_mozilla-esr_android-armv6.json',
    },
    'multilocaleOptions': [
        '--tag-override=%s_RELEASE' % releaseConfig['baseTag'],
        '--pull-locale-source',
        '--add-locales',
        '--package-multi',
        '--summary',
    ]
}
releaseConfig['build_tools_repo_path'] = 'build/tools'
releaseConfig['enableSigningAtBuildTime'] = True
releaseConfig['enablePartialMarsAtBuildTime'] = False
releaseConfig['autoGenerateChecksums'] = False
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('android-armv6',)