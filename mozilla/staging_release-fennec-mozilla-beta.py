# ATTENTION:
# If you are editing the non-template version of this file (eg, doesn't end
# with .template), your change WILL get overwritten. If you're adding, removing,
# or changing options as part of release automation changes you should be
# editing the .template instead. This file should only by edited directly if
# you're starting a release without Release Kickoff. You have been warned.
EMAIL_RECIPIENTS = []

releaseConfig = {}
releaseConfig['base_clobber_url'] = 'https://api-pub-build.allizom.org/clobberer/forceclobber'

# Release Notification
releaseConfig['AllRecipients']       = EMAIL_RECIPIENTS
releaseConfig['ImportantRecipients'] = EMAIL_RECIPIENTS
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[staging-release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'fennec'
releaseConfig['stage_product']       = 'mobile'
releaseConfig['appName']             = 'mobile'
releaseConfig['relbranchPrefix']     = 'MOBILE'
#  Current version info
releaseConfig['version']             = '15.0b4'
releaseConfig['appVersion']          = '15.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FENNEC_15_0b4'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['appVersion']
releaseConfig['nextMilestone']       = releaseConfig['milestone']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mobile': {
        'name': 'mozilla-beta',
        'path': 'users/stage-ffxbld/mozilla-beta',
        'revision': 'default',
        'relbranch': None,
        'bumpFiles': {
            'browser/config/version_display.txt': {
                'version': releaseConfig['version'],
                'nextVersion': releaseConfig['nextVersion']
            },
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
        }
    }
}
#  L10n repositories
releaseConfig['l10nRelbranch']       = None
releaseConfig['l10nRepoPath']        = 'users/stage-ffxbld'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mobile-beta.json'
releaseConfig['l10nJsonFile']        = releaseConfig['l10nRevisionFile']
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'users/stage-ffxbld/compare-locales': 'RELEASE_AUTOMATION',
    'users/stage-ffxbld/buildbot': 'production-0.8',
}

# Platform configuration
releaseConfig['enUSPlatforms']        = ('android-api-9', 'android-api-11', 'android-x86')
releaseConfig['notifyPlatforms']      = releaseConfig['enUSPlatforms']
releaseConfig['unittestPlatforms']    = ()
releaseConfig['talosTestPlatforms']   = ()
releaseConfig['enableUnittests']      = False

# L10n configuration
releaseConfig['l10nPlatforms']       = ('android-api-9', 'android-api-11')
releaseConfig['l10nNotifyPlatforms'] = releaseConfig['l10nPlatforms']
releaseConfig['l10nChunks']          = 1
releaseConfig['mergeLocales']        = True
releaseConfig['enableMultiLocale']   = True

# Mercurial account
releaseConfig['hgUsername']          = 'stage-ffxbld'
releaseConfig['hgSshKey']            = '/home/mock_mozilla/.ssh/ffxbld_rsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'ftp.stage.mozaws.net'
releaseConfig['stagingServer']       = 'upload.ffxbld.productdelivery.stage.mozaws.net'
releaseConfig['S3Credentials']       = '/builds/release-s3.credentials'
releaseConfig['S3Bucket']            = 'net-mozaws-stage-delivery-archive'
releaseConfig['ausServerUrl']        = 'https://aus4-dev.allizom.org'

# Partner repack configuration
releaseConfig['doPartnerRepacks']       = False
releaseConfig['partnersRepoPath']       = 'users/stage-ffxbld/partner-repacks'
releaseConfig['partnerRepackPlatforms'] = ()

# mozconfigs
releaseConfig['mozconfigs']          = {
    'android-api-9': 'mobile/android/config/mozconfigs/android-api-9-10-constrained/release',
    'android-api-11': 'mobile/android/config/mozconfigs/android-api-11/release',
    'android-x86': 'mobile/android/config/mozconfigs/android-x86/release',
}
releaseConfig['releaseChannel']      = 'beta'
releaseConfig["updateChannels"] = {
    "beta": {
        "ruleId": 34,
        "localTestChannel": "beta-localtest",
        "cdnTestChannel": "beta-cdntest",
        "testChannels": {
            "beta-localtest": {
                "ruleId": 49,
            },
            "beta-cdntest": {
                "ruleId": 37,
            }
        }
    }
}

# Product details config
releaseConfig["productDetailsRepo"] = "svn+ssh://ffxbld@dev-stage01.srv.releng.scl3.mozilla.com/libs/product-details"
releaseConfig["mozillaComRepo"]     = "svn+ssh://ffxbld@dev-stage01.srv.releng.scl3.mozilla.com/projects/mozilla.com"
releaseConfig["svnSshKey"]          = "/home/cltbld/.ssh/ffxbld_rsa"

# Fennec specific
releaseConfig['usePrettyNames']           = False
releaseConfig['disableStandaloneRepacks'] = True
releaseConfig['disableVirusCheck']        = True
releaseConfig['enableUpdatePackaging']    = False
releaseConfig['balrog_api_root']          = None

releaseConfig['single_locale_options'] = {
    'android-api-9': [
        '--cfg',
        'single_locale/staging_release_mozilla-beta_android_api_9.py',
        '--tag-override', '%s_RELEASE' % releaseConfig['baseTag'],
        '--user-repo-override', 'users/stage-ffxbld',
    ],
    'android-api-11': [
        '--cfg',
        'single_locale/staging_release_mozilla-beta_android_api_11.py',
        '--tag-override', '%s_RELEASE' % releaseConfig['baseTag'],
        '--user-repo-override', 'users/stage-ffxbld',
    ],
}

releaseConfig['multilocale_config'] = {
    'platforms': {
        'android-api-9':
            'multi_locale/staging_release_mozilla-beta_android.json',
        'android-api-11':
            'multi_locale/staging_release_mozilla-beta_android.json',
        'android-x86':
            'multi_locale/staging_release_mozilla-beta_android-x86.json',
    },
    'multilocaleOptions': [
        '--tag-override=%s_RELEASE' % releaseConfig['baseTag'],
        '--user-repo-override=users/stage-ffxbld',
        '--pull-locale-source',
        '--add-locales',
        '--package-multi',
        '--summary',
    ]
}

# Staging config
releaseConfig['build_tools_repo_path'] = "users/stage-ffxbld/tools"
releaseConfig['enableSigningAtBuildTime'] = True
releaseConfig['enablePartialMarsAtBuildTime'] = False
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('android-api-9', 'android-api-11', 'android-x86', 'linux')
releaseConfig['ftpSymlinkName'] = 'latest-beta'
releaseConfig['enableAutomaticPushToMirrors'] = True
releaseConfig['partialUpdates']      = {}
releaseConfig['bouncerServer']       = 'download.mozilla.org'
# Tuxedo/Bouncer configuration
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.mozilla.com/api'
releaseConfig['bouncer_submitter_config'] = 'releases/bouncer_fennec.py'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['bouncer_aliases'] = {
    'Fennec-%(version)s': 'fennec-beta-latest',
}
releaseConfig['skip_updates']        = True
