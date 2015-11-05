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
releaseConfig['AVVendorsRecipients'] = EMAIL_RECIPIENTS
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[staging-release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'firefox'
releaseConfig['stage_product']       = 'firefox'
releaseConfig['appName']             = 'browser'
#  Current version info
releaseConfig['version']             = '41.0'
releaseConfig['appVersion']          = '41.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 2
releaseConfig['baseTag']             = 'FIREFOX_41_0'
releaseConfig['partialUpdates']      = {

    '40.0.2': {
        'appVersion': '40.0.2',
        'buildNumber': 1,
        'baseTag': 'FIREFOX_40_0_2',
    },

    '41.0b2': {
        'appVersion': '41.0',
        'buildNumber': 1,
        'baseTag': 'FIREFOX_41_0b2',
    },

}
# What's New Page, should be revisited with each release.
# releaseConfig['openURL'] = 'https://www.mozilla.org/%LOCALE%/firefox/41.0/whatsnew/?oldversion=%OLD_VERSION%'

# win64 support
#releaseConfig['HACK_first_released_version'] = {'win64': TBD}

#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['appVersion']
releaseConfig['nextMilestone']       = releaseConfig['milestone']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mozilla': {
        'name': 'mozilla-release',
        'path': 'users/stage-ffxbld/mozilla-release',
        'revision': '74f5ca4d4b6e',
        'relbranch': None,
        'bumpFiles': {
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'browser/config/version_display.txt': {
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
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mozilla-release'
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'users/stage-ffxbld/compare-locales': 'RELEASE_AUTOMATION',
    'users/stage-ffxbld/buildbot': 'production-0.8',
    'users/stage-ffxbld/partner-repacks': 'default',
}

# Platform configuration
# TODO: add win64 when we're ready to ship it
releaseConfig['enUSPlatforms']       = ('linux', 'linux64', 'win32', 'macosx64')
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
releaseConfig['l10nChunks']          = 1

# Mercurial account
releaseConfig['hgUsername']          = 'stage-ffxbld'
releaseConfig['hgSshKey']            = '/home/mock_mozilla/.ssh/ffxbld_rsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'ftp.stage.mozaws.net'
releaseConfig['stagingServer']       = 'upload.ffxbld.productdelivery.stage.mozaws.net'
releaseConfig['previousReleasesStagingServer'] = 'archive.mozilla.org'
releaseConfig['S3Credentials']       = '/builds/release-s3.credentials'
releaseConfig['S3Bucket']            = 'net-mozaws-stage-delivery-firefox'
releaseConfig['bouncerServer']       = 'download.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus4-dev.allizom.org'
releaseConfig['releaseNotesUrl']     = None
releaseConfig['testOlderPartials']   = False
releaseConfig['promptWaitTime']      = None
releaseConfig['updateVerifyChunks']  = 2
releaseConfig['mozconfigs']          = {
    'linux': 'browser/config/mozconfigs/linux32/release',
    'linux64': 'browser/config/mozconfigs/linux64/release',
    'macosx64': 'browser/config/mozconfigs/macosx-universal/release',
    'win32': 'browser/config/mozconfigs/win32/release',
    #'win64': 'browser/config/mozconfigs/win64/release',
}
releaseConfig["releaseChannel"] = "release"
releaseConfig['updateChannels'] = {
    "release": {
        "versionRegex": r"^\d+\.\d+(\.\d+)?$",
        "ruleId": 31,
        "patcherConfig": "mozRelease-branch-patcher2.cfg",
        "localTestChannel": "release-localtest",
        "cdnTestChannel": "release-cdntest",
        "verifyConfigs": {
            "linux":  "mozRelease-firefox-linux.cfg",
            "linux64":  "mozRelease-firefox-linux64.cfg",
            "macosx64": "mozRelease-firefox-mac64.cfg",
            "win32":  "mozRelease-firefox-win32.cfg",
            #"win64":  "mozRelease-firefox-win64.cfg",
        },
        "testChannels": {
            "release-localtest": {
                "ruleId": 19,
            },
            "release-cdntest": {
                "ruleId": 20,
            },
        },
    },
    "beta": {
        "enabled": True,
        # For the beta channel, we want to able to provide updates to this
        # from prior betas or prior RCs that were shipped to the beta channel,
        # so this regex matches either.
        "versionRegex": r"^(\d+\.\d+(b\d+)?)$",
        "ruleId": 26,
        "requiresMirrors": False,
        "patcherConfig": "mozBeta-branch-patcher2.cfg",
        "localTestChannel": "beta-localtest",
        "cdnTestChannel": "beta-cdntest",
        "verifyConfigs": {
            "linux":  "mozBeta-firefox-linux.cfg",
            "linux64":  "mozBeta-firefox-linux64.cfg",
            "macosx64": "mozBeta-firefox-mac64.cfg",
            "win32":  "mozBeta-firefox-win32.cfg",
            #"win64":  "mozBeta-firefox-win32.cfg",
        },
        "marChannelIds": [
            "firefox-mozilla-beta",
            "firefox-mozilla-release",
        ],
        "testChannels": {
            "beta-cdntest": {
                "ruleId": 41,
            },
            "beta-localtest": {
                "ruleId": 40,
            },
        }
    }
}

# Partner repack configuration
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'users/stage-ffxbld/partner-repacks'
releaseConfig['syncPartnerBundles']  = False

# Tuxedo/Bouncer configuration
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.allizom.org/api'
releaseConfig['bouncer_submitter_config'] = 'releases/bouncer_firefox_release.py'

# Product details config
releaseConfig["productDetailsRepo"] = "svn+ssh://ffxbld@dev-stage01.srv.releng.scl3.mozilla.com/libs/product-details"
releaseConfig["mozillaComRepo"]     = "svn+ssh://ffxbld@dev-stage01.srv.releng.scl3.mozilla.com/projects/mozilla.com"
releaseConfig["svnSshKey"]          = "/home/cltbld/.ssh/ffxbld_rsa"

# Misc configuration
releaseConfig['build_tools_repo_path'] = "users/stage-ffxbld/tools"
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('linux','linux64')
releaseConfig['ftpSymlinkName'] = 'latest'

releaseConfig['bouncer_aliases'] = {
    'Firefox-%(version)s': 'firefox-latest',
    'Firefox-%(version)s-stub': 'firefox-stub',
}
