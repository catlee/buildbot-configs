releaseConfig['PassRecipients']      = ['release@mozilla.com',]
releaseConfig['l10nRepoPath']        = 'users/prepr-ffxbld'
releaseConfig['l10nChunks']          = 2
releaseConfig['hgUsername']          = 'prepr-ffxbld'
releaseConfig['cvsroot']             = ':ext:stgbld@cvs.mozilla.org:/cvsroot'
releaseConfig['stagingServer']       = 'preproduction-stage.build.mozilla.org'
releaseConfig['ausServerUrl']        = 'http://preproduction-stage.build.mozilla.org'
releaseConfig['partnersRepoPath']    = 'users/prepr-ffxbld/partner-repacks'
releaseConfig['tuxedoServerUrl']     = 'https://tuxedo.stage.mozilla.com/api/'
releaseConfig['enable_repo_setup']   = True
releaseConfig['commitPatcherConfig'] = False # TODO: toggle when CVS mirror is live
releaseConfig['messagePrefix']       = '[preprod-release] '
releaseConfig['userRepoRoot']        = 'users/prepr-ffxbld'
