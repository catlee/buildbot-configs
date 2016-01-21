# ATTENTION:
# If you are editing the non-template version of this file (eg, doesn't end
# with .template), your change WILL get overwritten. If you're adding, removing,
# or changing options as part of release automation changes you should be
# editing the .template instead. This file should only by edited directly if
# you're starting a release without Release Kickoff. You have been warned.
releaseConfig = {}
releaseConfig['base_clobber_url'] = 'https://api.pub.build.mozilla.org/clobberer/forceclobber'

# Release Notification
releaseConfig['AllRecipients']       = ['<release-automation-notifications-thunderbird@mozilla.org>',]
releaseConfig['ImportantRecipients'] = ['<thunderbird-drivers@mozilla.org>',]
releaseConfig['AVVendorsRecipients'] = ['<av-vendor-release-announce@mozilla.org>',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'thunderbird'
releaseConfig['stage_product']       = 'thunderbird'
releaseConfig['appName']             = 'mail'
releaseConfig['relbranchPrefix']     = 'THUNDERBIRD'
releaseConfig['mozilla_srcdir']      = 'mozilla'
#  Current version info
releaseConfig['version']             = '44.0b1'
releaseConfig['appVersion']          = '44.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'THUNDERBIRD_44_0b1'
releaseConfig['partialUpdates']      = {

    '43.0b1': {
        'appVersion': '43.0',
        'buildNumber': 3,
        'baseTag': 'THUNDERBIRD_43_0b1',
    },

    '42.0b1': {
        'appVersion': '42.0',
        'buildNumber': 1,
        'baseTag': 'THUNDERBIRD_42_0b1',
    },

    '42.0b2': {
        'appVersion': '42.0',
        'buildNumber': 1,
        'baseTag': 'THUNDERBIRD_42_0b2',
    },

}
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['appVersion']
releaseConfig['nextMilestone']       = releaseConfig['milestone']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'comm': {
        'name': 'comm-beta',
        'path': 'releases/comm-beta',
        'revision': '8bfffb4cf500',
        'relbranch': None,
        'bumpFiles': {
            'mail/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
        }
    },
    'mozilla': {
        'name': 'mozilla-beta',
        'path': 'releases/mozilla-beta',
        'revision': '40e457de9ce8',
        'relbranch': None,
        'bumpFiles': {
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
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_thunderbird-beta'
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_AUTOMATION',
    'build/buildbot': 'production-0.8',
}

# Platform configuration
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64')
releaseConfig['notifyPlatforms']     = releaseConfig['enUSPlatforms']
releaseConfig['talosTestPlatforms']  = ()

# Unittests
releaseConfig['unittestPlatforms']   = ()
releaseConfig['enableUnittests']     = False

# L10n configuration
releaseConfig['l10nPlatforms']       = releaseConfig['enUSPlatforms']
releaseConfig['shippedLocalesPath']  = 'mail/locales/shipped-locales'
releaseConfig['mergeLocales']        = True
releaseConfig['l10nUsePymake']       = True

# Mercurial account
releaseConfig['hgUsername']          = 'tbirdbld'
releaseConfig['hgSshKey']            = '/home/mock_mozilla/.ssh/tbirdbld_dsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'archive.mozilla.org'
releaseConfig['stagingServer']       = 'upload.tbirdbld.productdelivery.prod.mozaws.net'
releaseConfig['S3Credentials']       = '/builds/release-s3.credentials'
releaseConfig['S3Bucket']            = 'net-mozaws-prod-delivery-archive'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus4.mozilla.org'
releaseConfig['releaseNotesUrl']     = 'http://live.mozillamessaging.com/thunderbird/releasenotes?locale=%locale%&platform=%platform%&version=%version%'
releaseConfig['testOlderPartials']   = False
releaseConfig['promptWaitTime']      = None
releaseConfig['updateVerifyChunks']  = 6
releaseConfig['mozconfigs']          = {
    'linux': 'mail/config/mozconfigs/linux32/release',
    'linux64': 'mail/config/mozconfigs/linux64/release',
    'macosx64': 'mail/config/mozconfigs/macosx-universal/release',
    'win32': 'mail/config/mozconfigs/win32/release',
}
releaseConfig['source_mozconfig']      = 'mail/config/mozconfigs/linux64/release'
releaseConfig['releaseChannel']        = 'beta'
releaseConfig['updateChannels'] = {
    "beta": {
        "versionRegex": r"^.*$",
        "ruleId": 43,
        "patcherConfig": "mozBeta-thunderbird-branch-patcher2.cfg",
        "localTestChannel": "beta-localtest",
        "cdnTestChannel": "beta-cdntest",
        "verifyConfigs": {
            "linux":  "mozBeta-thunderbird-linux.cfg",
            "linux64":  "mozBeta-thunderbird-linux64.cfg",
            "macosx64": "mozBeta-thunderbird-mac64.cfg",
            "win32":  "mozBeta-thunderbird-win32.cfg",
        },
        "testChannels": {
            "beta-cdntest": {
                "ruleId": 60,
            },
            "beta-localtest": {
                "ruleId": 27,
            },
        }
    }
}


# Partner repack configuration
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'build/partner-repacks'

# Tuxedo/Bouncer configuration
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.mozilla.com/api'
releaseConfig['bouncer_submitter_config'] = 'releases/bouncer_thunderbird.py'
releaseConfig['bouncer_aliases']     = {
    'Thunderbird-%(version)s': 'thunderbird-beta-latest',
}

# Misc configuration
releaseConfig['enableAutomaticPushToMirrors'] = True
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('linux','linux64')