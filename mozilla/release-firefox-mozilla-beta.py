# ATTENTION:
# If you are editing the non-template version of this file (eg, doesn't end
# with .template), your change WILL get overwritten. If you're adding, removing,
# or changing options as part of release automation changes you should be
# editing the .template instead. This file should only by edited directly if
# you're starting a release without Release Kickoff. You have been warned.
releaseConfig = {}
releaseConfig['base_clobber_url'] = 'https://api.pub.build.mozilla.org/clobberer/forceclobber'

# Release Notification
releaseConfig['AllRecipients']       = ['<release-automation-notifications@mozilla.com>',]
releaseConfig['ImportantRecipients'] = ['<release-drivers@mozilla.org>',]
releaseConfig['AVVendorsRecipients'] = ['<av-vendor-release-announce@mozilla.org>',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'firefox'
releaseConfig['stage_product']       = 'firefox'
releaseConfig['appName']             = 'browser'
#  Current version info
releaseConfig['version']             = '42.0b9'
releaseConfig['appVersion']          = '42.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FIREFOX_42_0b9'
releaseConfig['partialUpdates']      = {

    '42.0b6': {
        'appVersion': '42.0',
        'buildNumber': 1,
        'baseTag': 'FIREFOX_42_0b6',
    },

    '42.0b7': {
        'appVersion': '42.0',
        'buildNumber': 1,
        'baseTag': 'FIREFOX_42_0b7',
    },

    '42.0b8': {
        'appVersion': '42.0',
        'buildNumber': 1,
        'baseTag': 'FIREFOX_42_0b8',
    },

}
releaseConfig['ui_update_tests'] = False

# win64 support
releaseConfig['HACK_first_released_version'] = {'win64': '37.0b2'}

#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['appVersion']
releaseConfig['nextVersion']         = releaseConfig['version']
releaseConfig['nextMilestone']       = releaseConfig['milestone']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mozilla': {
        'name': 'mozilla-beta',
        'path': 'releases/mozilla-beta',
        'revision': '894bc1fcf2a9',
        'relbranch': None,
        'bumpFiles': {
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'browser/config/version_display.txt': {
                'version': releaseConfig['version'],
                'nextVersion': releaseConfig['nextVersion']
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
releaseConfig['l10nRepoPath']        = 'releases/l10n/mozilla-beta'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mozilla-beta'
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_AUTOMATION',
    'build/buildbot': 'production-0.8',
    'build/partner-repacks': 'default',
}

# Platform configuration
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64', 'win64')
releaseConfig['notifyPlatforms']     = releaseConfig['enUSPlatforms']
releaseConfig['talosTestPlatforms']  = ()

# Unittests
releaseConfig['unittestPlatforms']   = ()
releaseConfig['enableUnittests']     = False

# L10n configuration
releaseConfig['l10nPlatforms']       = releaseConfig['enUSPlatforms']
releaseConfig['shippedLocalesPath']  = 'browser/locales/shipped-locales'
releaseConfig['mergeLocales']        = True
releaseConfig['l10nUsePymake']       = True

# Mercurial account
releaseConfig['hgUsername']          = 'ffxbld'
releaseConfig['hgSshKey']            = '/home/mock_mozilla/.ssh/ffxbld_rsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'archive.mozilla.org'
releaseConfig['stagingServer']       = 'upload.ffxbld.productdelivery.prod.mozaws.net'
releaseConfig['S3Credentials']       = '/builds/release-s3.credentials'
releaseConfig['S3Bucket']            = 'net-mozaws-prod-delivery-firefox'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus4.mozilla.org'
releaseConfig['releaseNotesUrl']     = None
releaseConfig['testOlderPartials']   = False
releaseConfig['promptWaitTime']      = None
releaseConfig['updateVerifyChunks']  = 6
releaseConfig['mozconfigs']          = {
    'linux': 'browser/config/mozconfigs/linux32/beta',
    'linux64': 'browser/config/mozconfigs/linux64/beta',
    'macosx64': 'browser/config/mozconfigs/macosx-universal/beta',
    'win32': 'browser/config/mozconfigs/win32/beta',
    'win64': 'browser/config/mozconfigs/win64/beta',
}
releaseConfig['releaseChannel']        = 'beta'
releaseConfig['updateChannels'] = {
    "beta": {
        "versionRegex": r"^.*$",
        "ruleId": 32,
        "patcherConfig": "mozBeta-branch-patcher2.cfg",
        "localTestChannel": "beta-localtest",
        "cdnTestChannel": "beta-cdntest",
        "verifyConfigs": {
            "linux":  "mozBeta-firefox-linux.cfg",
            "linux64":  "mozBeta-firefox-linux64.cfg",
            "macosx64": "mozBeta-firefox-mac64.cfg",
            "win32":  "mozBeta-firefox-win32.cfg",
            "win64":  "mozBeta-firefox-win64.cfg",
        },
        "testChannels": {
            "beta-cdntest": {
                "ruleId": 45,
            },
            "beta-localtest": {
                "ruleId": 25,
            },
        }
    }
}

# Partner repack configuration
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'build/partner-repacks'

# Tuxedo/Bouncer configuration
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.mozilla.com/api'
releaseConfig['bouncer_submitter_config'] = 'releases/bouncer_firefox_beta.py'

# Product details config
releaseConfig["productDetailsRepo"] = "svn+ssh://ffxbld@svn.mozilla.org/libs/product-details"
releaseConfig["mozillaComRepo"]     = "svn+ssh://ffxbld@svn.mozilla.org/projects/mozilla.com"
releaseConfig["svnSshKey"]          = "/home/cltbld/.ssh/ffxbld_rsa"

# Misc configuration
releaseConfig['enableAutomaticPushToMirrors'] = True
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('linux','linux64')
releaseConfig['ftpSymlinkName'] = 'latest-beta'

releaseConfig['bouncer_aliases'] = {
    'Firefox-%(version)s': 'firefox-beta-latest',
    'Firefox-%(version)s-stub': 'firefox-beta-stub',
}
