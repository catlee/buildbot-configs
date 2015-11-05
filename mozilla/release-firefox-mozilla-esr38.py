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
releaseConfig['ImportantRecipients'] = ['<release-drivers@mozilla.org>', '<mikeperry@torproject.org>']
releaseConfig['AVVendorsRecipients'] = ['<av-vendor-release-announce@mozilla.org>',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'firefox'
releaseConfig['stage_product']       = 'firefox'
releaseConfig['appName']             = 'browser'
#  Current version info
releaseConfig['version']             = '38.4.0esr'
releaseConfig['appVersion']          = '38.4.0'
releaseConfig['milestone']           = releaseConfig['appVersion']
releaseConfig['buildNumber']         = 2
releaseConfig['baseTag']             = 'FIREFOX_38_4_0esr'
releaseConfig['partialUpdates']      = {

    '38.3.0esr': {
        'appVersion': '38.3.0',
        'buildNumber': 2,
        'baseTag': 'FIREFOX_38_3_0esr',
    },

}
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = '38.4.0esrpre'
releaseConfig['nextMilestone']       = releaseConfig['nextAppVersion']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mozilla': {
        'name': 'mozilla-esr38',
        'path': 'releases/mozilla-esr38',
        'revision': '0eff77a5b7ba',
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
        }
    }
}
#  L10n repositories
releaseConfig['l10nRelbranch']       = None
releaseConfig['l10nRepoPath']        = 'releases/l10n/mozilla-release'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mozilla-esr38'
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_0_9_5',
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
releaseConfig['useBetaChannel']      = 1
releaseConfig['updateVerifyChunks']  = 6
releaseConfig['mozconfigs']          = {
    'linux': 'browser/config/mozconfigs/linux32/release',
    'linux64': 'browser/config/mozconfigs/linux64/release',
    'macosx64': 'browser/config/mozconfigs/macosx-universal/release',
    'win32': 'browser/config/mozconfigs/win32/release',
}
releaseConfig['releaseChannel']        = 'esr'
releaseConfig['updateChannels'] = {
    "esr": {
        "versionRegex": r"^.*$",
        "ruleId": 168,
        "patcherConfig": "mozEsr38-branch-patcher2.cfg",
        "localTestChannel": "esr-localtest",
        "cdnTestChannel": "esr-cdntest",
        "verifyConfigs": {
            "linux":  "mozEsr38-firefox-linux.cfg",
            "linux64":  "mozEsr38-firefox-linux64.cfg",
            "macosx64": "mozEsr38-firefox-mac64.cfg",
            "win32":  "mozEsr38-firefox-win32.cfg",
        },
        "testChannels": {
            "esr-localtest": {
                "ruleId": 166,
            },
            "esr-cdntest": {
                "ruleId": 167,
            },
        },
    },
}


# Partner repack configuration
releaseConfig['doPartnerRepacks']    = False
releaseConfig['partnersRepoPath']    = 'build/partner-repacks'

# Tuxedo/Bouncer configuration
releaseConfig['tuxedoServerUrl']     = 'https://bounceradmin.mozilla.com/api'
releaseConfig['bouncer_submitter_config'] = 'releases/bouncer_firefox_esr.py'

# Product details config
releaseConfig["productDetailsRepo"] = "svn+ssh://ffxbld@svn.mozilla.org/libs/product-details"
releaseConfig["mozillaComRepo"]     = "svn+ssh://ffxbld@svn.mozilla.org/projects/mozilla.com"
releaseConfig["svnSshKey"]          = "/home/cltbld/.ssh/ffxbld_rsa"

# Misc configuration
releaseConfig['enableAutomaticPushToMirrors'] = False
releaseConfig['use_mock'] = True
releaseConfig['mock_platforms'] = ('linux','linux64')
releaseConfig['ftpSymlinkName'] = 'latest-esr'

releaseConfig['bouncer_aliases'] = {
    'Firefox-%(version)s': 'firefox-esr-latest',
}
