releaseConfig['sourceRepositories']['mozilla']['path'] = 'users/prepr-ffxbld/mozilla-release'
releaseConfig['sourceRepositories']['mozilla']['clonePath'] = 'releases/mozilla-release'
releaseConfig['l10nRepoClonePath']   = 'releases/l10n/mozilla-release'
releaseConfig['otherReposToTag']     = {
    'users/prepr-ffxbld/compare-locales': 'RELEASE_AUTOMATION',
    'users/prepr-ffxbld/buildbot': 'production-0.8',
    'users/prepr-ffxbld/partner-repacks': 'default',
    'users/prepr-ffxbld/mozharness': 'production',
}
