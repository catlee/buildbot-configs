# ATTENTION:
# If you are editing the non-template version of this file (eg, doesn't end
# with .template), your change WILL get overwritten. If you're adding, removing,
# or changing options as part of release automation changes you should be
# editing the .template instead. This file should only by edited directly if
# you're starting a release without Release Kickoff. You have been warned.
EMAIL_RECIPIENTS = []

releaseConfig = {}
releaseConfig['skip_repo_setup'] = True
releaseConfig['disable_tinderbox_mail'] = True
releaseConfig['base_clobber_url'] = 'http://clobberer-stage.pvt.build.mozilla.org/always_clobber.php'

# Release Notification
releaseConfig['AllRecipients'] = EMAIL_RECIPIENTS
releaseConfig['ImportantRecipients'] = EMAIL_RECIPIENTS
releaseConfig['AVVendorsRecipients'] = EMAIL_RECIPIENTS
releaseConfig['releaseTemplates'] = 'release_templates'
releaseConfig['messagePrefix'] = '[staging-release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName'] = 'thunderbird'
releaseConfig['appName'] = 'mail'
releaseConfig['mozilla_dir'] = 'mozilla'
#  Current version info
releaseConfig['version'] = '10.0.1esr'
releaseConfig['appVersion'] = '10.0.1'
releaseConfig['milestone'] = '10.0.1'
releaseConfig['buildNumber'] = 1
releaseConfig['baseTag'] = 'THUNDERBIRD_10_0_1esr'
releaseConfig['partialUpdates'] = {
    '10.0esr': {
        'appVersion': '10.0',
        'buildNumber': 1,
        'baseTag': 'THUNDERBIRD_10_0esr',
    }
}
#  Next (nightly) version info
releaseConfig['nextAppVersion'] = releaseConfig['appVersion']
releaseConfig['nextMilestone'] = releaseConfig['milestone']
#  Repository configuration, for tagging
## Staging repository path
releaseConfig['userRepoRoot'] = 'users/stage-ffxbld'
releaseConfig['sourceRepositories'] = {
    'comm': {
        'name': 'comm-esr10',
        'clonePath': 'releases/comm-esr10',
        'path': 'users/stage-ffxbld/comm-esr10',
        'revision': 'default',
        'relbranch': None,
        'bumpFiles': {
            'mail/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
        }
    },
    'mozilla': {
        'name': 'mozilla-esr10',
        'clonePath': 'releases/mozilla-esr10',
        'path': 'users/stage-ffxbld/mozilla-esr10',
        'revision': 'default',
        'relbranch': None,
        'bumpFiles': {
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
releaseConfig['l10nRelbranch'] = None
releaseConfig['l10nRepoClonePath'] = 'releases/l10n/mozilla-release'
releaseConfig['l10nRepoPath'] = 'users/stage-ffxbld'
releaseConfig['l10nRevisionFile'] = 'l10n-changesets_thunderbird-esr10'
#  Support repositories
releaseConfig['otherReposToTag'] = {
    'users/stage-ffxbld/compare-locales': 'RELEASE_0_8_2',
    'users/stage-ffxbld/buildbot': 'production-0.8',
    'users/stage-ffxbld/partner-repacks': 'default',
}

# Platform configuration
releaseConfig['enUSPlatforms'] = ('linux', 'linux64', 'win32',
                                  'macosx64')
releaseConfig['notifyPlatforms'] = ('linux', 'linux64', 'win32',
                                    'macosx64')
releaseConfig['talosTestPlatforms'] = ()
releaseConfig['xulrunnerPlatforms'] = ()

# Unittests
releaseConfig['unittestPlatforms'] = ()
releaseConfig['enableUnittests'] = True

# L10n configuration
releaseConfig['l10nPlatforms'] = releaseConfig['enUSPlatforms']
releaseConfig['shippedLocalesPath'] = 'mail/locales/shipped-locales'
releaseConfig['l10nChunks'] = 2
releaseConfig['mergeLocales'] = True

# Mercurial account
releaseConfig['hgUsername'] = 'stage-ffxbld'
releaseConfig['hgSshKey'] = '~cltbld/.ssh/ffxbld_dsa'

# Update-specific configuration
releaseConfig[
    'patcherConfig'] = 'mozEsr10-thunderbird-branch-patcher2.cfg'
releaseConfig[
    'ftpServer'] = 'dev-stage01.srv.releng.scl3.mozilla.com'
releaseConfig[
    'stagingServer'] = 'dev-stage01.srv.releng.scl3.mozilla.com'
releaseConfig['previousReleasesStagingServer'] = 'stage.mozilla.org'
releaseConfig['bouncerServer'] = 'download.mozilla.org'
releaseConfig[
    'ausServerUrl'] = 'http://dev-stage01.srv.releng.scl3.mozilla.com'
releaseConfig[
    'ausHost'] = 'dev-stage01.srv.releng.scl3.mozilla.com'
releaseConfig['ausUser'] = 'tbirdbld'
releaseConfig['ausSshKey'] = 'tbirdbld_dsa'
releaseConfig['releaseNotesUrl'] = 'http://live.mozillamessaging.com/thunderbird/releasenotes?locale=%locale%&platform=%platform%&version=%version%'
releaseConfig['testOlderPartials'] = False
releaseConfig['verifyConfigs'] = {
    'linux': 'mozEsr10-thunderbird-linux.cfg',
    'linux64': 'mozEsr10-thunderbird-linux64.cfg',
    'macosx64': 'mozEsr10-thunderbird-mac64.cfg',
    'win32': 'mozEsr10-thunderbird-win32.cfg'
}
releaseConfig['mozconfigs'] = {
    'linux': 'mail/config/mozconfigs/linux32/release',
    'linux64': 'mail/config/mozconfigs/linux64/release',
    'macosx64': 'mail/config/mozconfigs/macosx-universal/release',
    'win32': 'mail/config/mozconfigs/win32/release',
}
releaseConfig['releaseChannel'] = 'esr'

# Partner repack configuration
releaseConfig['doPartnerRepacks'] = False
releaseConfig['partnersRepoPath'] = 'users/stage-ffxbld/partner-repacks'

# Tuxedo/Bouncer configuration
releaseConfig['tuxedoConfig'] = 'firefox-tuxedo.ini'
releaseConfig['tuxedoServerUrl'] = 'https://tuxedo.stage.mozilla.com/api/'
releaseConfig['extraBouncerPlatforms'] = ('solaris-sparc', 'solaris-i386',
                                          'opensolaris-sparc',
                                          'opensolaris-i386')

# Misc configuration
releaseConfig['enable_repo_setup'] = False
releaseConfig['build_tools_repo_path'] = "users/stage-ffxbld/tools"
releaseConfig['use_mock'] = False
releaseConfig['ftpSymlinkName'] = 'latest-esr'
