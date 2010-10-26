from buildbot.scheduler import Scheduler, Dependent
from buildbot.process.factory import BuildFactory
from buildbot.steps.dummy import Dummy

import buildbotcustom.l10n
import buildbotcustom.misc
import buildbotcustom.process.factory

from buildbotcustom.l10n import DependentL10n
from buildbotcustom.misc import get_locales_from_json, \
                                isHgPollerTriggered
from buildbotcustom.process.factory import StagingRepositorySetupFactory, \
  ReleaseTaggingFactory, MultiSourceFactory, MaemoReleaseBuildFactory, \
  MaemoReleaseRepackFactory, PartnerRepackFactory, \
  ReleaseMobileDesktopBuildFactory, AndroidReleaseBuildFactory
from buildbotcustom.changes.ftppoller import FtpPoller

# this is where all of our important configuration is stored. build number,
# version number, sign-off revisions, etc.
import release_mobile_config
reload(release_mobile_config)
from release_mobile_config import *

import mobile_master
reload(mobile_master)
from mobile_master import MOBILE_L10N_SLAVES

# for the 'build' step we use many of the same vars as the nightlies do.
# we import those so we don't have to duplicate them in release_config
import config as nightly_config
import mobile_config as mobile_nightly_config

branchConfig = nightly_config.BRANCHES[mozSourceRepoName]
mobileBranchConfig = mobile_nightly_config.MOBILE_BRANCHES[mobileBranchNick]

builders = []
schedulers = []
change_source = []
status = []

##### Change sources and Schedulers

(l10n_clone_repos, platform_locales) = get_locales_from_json(
                                         l10nRevisionFile,
                                         l10nRepoClonePath,
                                         l10nRelbranchOverride)
(l10n_tag_repos, platform_locales) = get_locales_from_json(l10nRevisionFile,
                                                           l10nRepoPath,
                                                           l10nRelbranchOverride)

repo_setup_scheduler = Scheduler(
    name='mobile_repo_setup',
    branch=mobileSourceRepoPath,
    treeStableTimer=0,
    builderNames=['mobile_repo_setup'],
    fileIsImportant=lambda c: not isHgPollerTriggered(c, branchConfig['hgurl'])
)
schedulers.append(repo_setup_scheduler)
tag_scheduler = Dependent(
    name='mobile_tag',
    upstream=repo_setup_scheduler,
    builderNames=['mobile_tag']
)
schedulers.append(tag_scheduler)
source_scheduler = Dependent(
    name='mobile_source',
    upstream=tag_scheduler,
    builderNames=['mobile_source']
)
schedulers.append(source_scheduler)
for platform in enUSPlatforms:
    build_scheduler = Dependent(
        name='%s_build' % platform,
        upstream=tag_scheduler,
        builderNames=['%s_build' % platform]
    )
    schedulers.append(build_scheduler)
    if platform in l10nPlatforms:
        l10nPlatform = platform
        if l10nPlatform.startswith('maemo'):
            l10nPlatform = 'maemo'
        repack_scheduler = DependentL10n(
            name='%s_repack' % platform,
            platform=l10nPlatform,
            upstream=build_scheduler,
            builderNames=['%s_repack' % platform],
            repoType='hg',
            branch=mobileSourceRepoPath,
            baseTag='%s_RELEASE' % baseTag,
            locales=platform_locales[l10nPlatform],
            tree='release'
        )
        schedulers.append(repack_scheduler)
    if doPartnerRepacks and platform in partnerRepackPlatforms:
        partner_scheduler = Dependent(
            name='%s_partner_repack' % platform,
            upstream=build_scheduler,
            builderNames=['%s_partner_repack' % platform]
        )
        schedulers.append(partner_scheduler)
for platform in enUSDesktopPlatforms:
    build_scheduler = Dependent(
        name='mobile_%s_desktop_build' % platform,
        upstream=tag_scheduler,
        builderNames=['mobile_%s_desktop_build' % platform]
    )
    schedulers.append(build_scheduler)
    if platform in l10nDesktopPlatforms:
        repack_scheduler = DependentL10n(
            name='mobile_%s_desktop_repack' % platform,
            platform=platform,
            upstream=build_scheduler,
            builderNames=['mobile_%s_desktop_repack' % platform],
            repoType='hg',
            branch=mobileSourceRepoPath,
            baseTag='%s_RELEASE' % baseTag,
            locales=platform_locales[platform],
            tree='release'
        )
        schedulers.append(repack_scheduler)

##### Builders
clone_repositories = {
    mozSourceRepoClonePath: {
        'revision': mozSourceRepoRevision,
        'relbranchOverride': mozRelbranchOverride,
        'bumpFiles': ['config/milestone.txt', 'js/src/config/milestone.txt'],
    },
    mobileSourceRepoClonePath: {
        'revision': mobileSourceRepoRevision,
        'relbranchOverride': mobileRelbranchOverride,
        'bumpFiles': ['confvars.sh'],
    },
}
clone_repositories.update(l10n_clone_repos)

tag_repositories = {
    mozSourceRepoPath: {
        'revision': mozSourceRepoRevision,
        'relbranchOverride': mozRelbranchOverride,
        'bumpFiles': ['config/milestone.txt', 'js/src/config/milestone.txt',]
    },
    mobileSourceRepoPath: {
        'revision': mobileSourceRepoRevision,
        'relbranchOverride': mobileRelbranchOverride,
        'bumpFiles': ['confvars.sh']
    }
}
tag_repositories.update(l10n_tag_repos)


repository_setup_factory = StagingRepositorySetupFactory(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    username=hgUsername,
    sshKey=hgSshKey,
    repositories=clone_repositories
)

builders.append({
    'name': 'mobile_repo_setup',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': 'mobile_repo_setup',
    'factory': repository_setup_factory
})


tag_factory = ReleaseTaggingFactory(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    repositories=tag_repositories,
    productName=productName,
    appName=appName,
    version=version,
    appVersion=appVersion,
    milestone=milestone,
    baseTag=baseTag,
    buildNumber=buildNumber,
    hgUsername=hgUsername,
    hgSshKey=hgSshKey
)

builders.append({
    'name': 'mobile_tag',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': 'mobile_tag',
    'factory': tag_factory
})

sourceRepoConfig=[{
        'repoPath': mozSourceRepoPath,
        'location': mozSourceRepoName,
        'bundleName': '%s-%s_%s.bundle' % (productName, version,
                                           mozSourceRepoName),
    },{
        'repoPath': mobileSourceRepoPath,
        'location': '%s/mobile' % mozSourceRepoName,
        'bundleName': '%s-%s_%s.bundle' % (productName, version,
                                           mobileSourceRepoName),
    }
]
mobile_source_factory = MultiSourceFactory(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    repoPath=mozSourceRepoPath,
    repoConfig=sourceRepoConfig,
    productName=productName,
    uploadProductName='mobile',
    version=version,
    baseTag=baseTag,
    stagingServer=branchConfig['stage_server'],
    stageUsername=branchConfig['stage_username'],
    stageSshKey=branchConfig['stage_ssh_key'],
    buildNumber=buildNumber,
    stageNightlyDir="candidates",
    autoconfDirs=['.', 'js/src']
)
builders.append({
    'name': 'mobile_source',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': 'mobile_source',
    'factory': mobile_source_factory
})


for platform in enUSPlatforms:

    baseUploadDir='%s-candidates/build%d' % (version, buildNumber)
    candidatesPath = '%s/%s' % (stageBasePath, baseUploadDir)
    build_factory = None
    repack_factory = None
    pf = mobileBranchConfig['platforms'][platform]
    clobberTime = pf.get('clobber_time', branchConfig['default_clobber_time'])

    if platform.startswith('maemo'):
        if disableMultiLocale:
            multiLocale = False
        else:
            multiLocale = mobileBranchConfig['enable_multi_locale']
        mozconfig = 'mobile/%s/%s/release' % (platform, mobileSourceRepoName)
        releaseWorkDir  = pf['base_workdir'] + '-release'
        releaseBuildDir = pf['base_builddir'] + '-release'
        build_factory = MaemoReleaseBuildFactory(
            env=pf['env'],
            hgHost=branchConfig['hghost'],
            repoPath=mozSourceRepoPath,
            configRepoPath=branchConfig['config_repo_path'],
            configSubDir=branchConfig['config_subdir'],
            mozconfig=mozconfig,
            stageUsername=branchConfig['stage_username'],
            stageServer=branchConfig['stage_server'],
            stageSshKey=branchConfig['stage_ssh_key'],
            stageBasePath=candidatesPath,
            mobileRepoPath=mobileSourceRepoPath,
            mozRevision='%s_RELEASE' % baseTag,
            mobileRevision='%s_RELEASE' % baseTag,
            l10nTag='%s_RELEASE' % baseTag,
            platform=platform,
            uploadSymbols=True,
            sb_target=pf['sb_target'],
            buildsBeforeReboot=pf['builds_before_reboot'],
            baseWorkDir=releaseWorkDir,
            baseBuildDir=releaseBuildDir,
            baseUploadDir=baseUploadDir,
            buildToolsRepoPath=branchConfig['build_tools_repo_path'],
            clobberURL=branchConfig['base_clobber_url'],
            clobberTime=clobberTime,
            buildSpace=10,
            mergeLocales=mergeLocales,
            locales=platform_locales['maemo-multilocale'].keys(),
            multiLocale=multiLocale,
            l10nRepoPath=l10nRepoPath,
            triggerBuilds=False,
        )
    elif platform.startswith('android'):
        mozconfig = 'mobile/android/%s/release' % (mobileSourceRepoName)
        releaseWorkDir  = pf['base_workdir'] + '-release'
        previousCandidateDir='%s-candidates/build%s/%s' % (oldVersion,
                                                           oldBuildNumber,
                                                           platform)
        currentCandidateDir='%s-candidates/build%s/%s' % (version,
                                                          buildNumber,
                                                          platform)
        updatePlatform='Android_arm-eabi-gcc3'
        ausPreviousUploadDir = "%s/%s/%s/%%(previous_buildid)s/en-US/beta-cck-test" % \
                               (ausBaseUploadDir, oldVersion, updatePlatform)
        ausFullUploadDir = '%s/%s/%s/%%(buildid)s/en-US/beta-cck-test' % \
                           (ausBaseUploadDir, version, updatePlatform)
        build_factory = AndroidReleaseBuildFactory(
            env=pf['env'],
            hgHost=branchConfig['hghost'],
            repoPath=mozSourceRepoPath,
            configRepoPath=branchConfig['config_repo_path'],
            configSubDir=branchConfig['config_subdir'],
            mozconfig=mozconfig,
            stageUsername=branchConfig['stage_username'],
            stageServer=branchConfig['stage_server'],
            stageSshKey=branchConfig['stage_ssh_key'],
            stageBasePath=candidatesPath,
            mobileRepoPath=mobileSourceRepoPath,
            mozRevision='%s_RELEASE' % baseTag,
            mobileRevision='%s_RELEASE' % baseTag,
            platform=platform,
            uploadSymbols=True,
            buildsBeforeReboot=pf['builds_before_reboot'],
            baseWorkDir=releaseWorkDir,
            baseUploadDir=baseUploadDir,
            buildToolsRepoPath=branchConfig['build_tools_repo_path'],
            clobberURL=branchConfig['base_clobber_url'],
            clobberTime=clobberTime,
            buildSpace=10,
            packageGlobList=pf.get('glob_list', ['embedding/android/*.apk',]),
            createSnippet=True,
            ausUser=ausUser,
            ausSshKey=ausSshKey,
            ausPreviousUploadDir=ausPreviousUploadDir,
            ausFullUploadDir=ausFullUploadDir,
            ausHost=branchConfig['aus2_host'],
            downloadBaseURL='%s/candidates' % (
              mobileBranchConfig['download_base_url']),
            previousCandidateDir=previousCandidateDir,
            currentCandidateDir=currentCandidateDir,
            version=version,
            previousVersion=oldVersion,
            buildNumber=buildNumber,
            updatePlatform=updatePlatform,
            multiLocale=multiLocale,
            mozharnessConfig="multi_locale/staging_4.0_release_android.json",
        )
    builders.append({
        'name': '%s_build' % platform,
        'slavenames': pf['slaves'],
        'category': 'release',
        'builddir': '%s_build' % platform,
        'factory': build_factory
    })

    if platform in l10nPlatforms:
        if platform.startswith('maemo'):
            releaseBuildDir = pf['base_builddir'] + '-l10n-release'
            repack_factory = MaemoReleaseRepackFactory(
                enUSBinaryURL='%s/%s' % (base_enUS_binaryURL, platform),
                stageServer=branchConfig['stage_server'],
                stageUsername=branchConfig['stage_username'],
                stageSshKey=branchConfig['stage_ssh_key'],
                stageBasePath='%s/%s-candidates/build%d/%s' % (stageBasePath,
                                                               version,
                                                               buildNumber,
                                                               platform),
                baseWorkDir='%s-release' % pf['base_l10n_workdir'],
                baseBuildDir=releaseBuildDir,
                l10nTag='%s_RELEASE' % baseTag,
                hgHost=branchConfig['hghost'],
                repoPath=mozSourceRepoPath,
                l10nRepoPath=l10nRepoPath,
                mobileRepoPath=mobileSourceRepoPath,
                packageGlobList=['-r', '%(locale)s'],
                buildToolsRepoPath=branchConfig['build_tools_repo_path'],
                compareLocalesRepoPath=branchConfig['compare_locales_repo_path'],
                compareLocalesTag=branchConfig['compare_locales_tag'],
                mergeLocales=mergeLocales,
                buildSpace=2,
                sb_target=pf['sb_target'],
                configRepoPath=branchConfig['config_repo_path'],
                configSubDir=branchConfig['config_subdir'],
                mozconfig=mozconfig,
                platform=platform,
                tree='release'
            )

        builders.append({
            'name': '%s_repack' % platform,
            'slavenames': MOBILE_L10N_SLAVES['maemo4'],
            'category': 'release',
            'builddir': '%s_repack' % platform,
            'factory': repack_factory
        })
    if doPartnerRepacks and platform in partnerRepackPlatforms:
        partner_repack_factory = PartnerRepackFactory(
            hgHost=branchConfig['hghost'],
            repoPath='mozSourceRepoPath',
            buildToolsRepoPath=branchConfig['build_tools_repo_path'],
            productName='mobile',
            version=version,
            buildNumber=buildNumber,
            partnersRepoPath=partnersRepoPath,
            stagingServer=stagingServer,
            stageUsername=branchConfig['stage_username'],
            stageSshKey=branchConfig['stage_ssh_key'],
            nightlyDir='candidates',
            platformList=[platform],
            baseWorkDir='%s-partner' % mobileBranchConfig['platforms'][platform]['base_workdir'],
            python='python2.5',
            packageDmg=False,
            createRemoteStageDir=True
        )
        builders.append({
            'name': '%s_partner_repack' % platform,
            'slavenames': branchConfig['platforms']['linux']['slaves'],
            'category': 'release',
            'builddir': '%s_partner_repack' % platform,
            'factory': partner_repack_factory
        })

for platform in enUSDesktopPlatforms:
    pf = mobileBranchConfig['platforms'][platform]
    clobberTime = pf.get('clobber_time', branchConfig['default_clobber_time'])
    packageGlobList = []
    if platform == 'linux-i686':
        packageGlobList = ['-r', 'dist/*.tar.bz2']
    elif platform == 'macosx-i686':
        packageGlobList = ['-r', 'dist/*.dmg']
    elif platform == 'win32-i686':
        packageGlobList = ['-r', 'dist/*.zip']
    
    build_factory = ReleaseMobileDesktopBuildFactory(
        hgHost=branchConfig['hghost'],
        repoPath=mozSourceRepoPath,
        configRepoPath=branchConfig['config_repo_path'],
        configSubDir=branchConfig['config_subdir'],
        mozconfig=pf['mozconfig'].replace('nightly', 'release'),
        env=pf['env'],
        stageUsername=branchConfig['stage_username'],
        stageGroup=branchConfig['stage_group'],
        stageSshKey=branchConfig['stage_ssh_key'],
        stageServer=branchConfig['stage_server'],
        stageBasePath='%s/%s' % (candidatesPath, platform),
        mobileRepoPath=mobileSourceRepoPath,
        mozRevision='%s_RELEASE' % baseTag,
        mobileRevision='%s_RELEASE' % baseTag,
        platform=platform,
        uploadSymbols=True,
        packageGlobList=packageGlobList,
        baseWorkDir=pf['base_workdir'],
        baseUploadDir=baseUploadDir,
        buildToolsRepoPath=branchConfig['build_tools_repo_path'],
        clobberURL=branchConfig['base_clobber_url'],
        clobberTime=clobberTime,
        buildSpace=10,
        buildsBeforeReboot=pf['builds_before_reboot'],
        triggerBuilds=False,
        version=version,
        buildNumber=buildNumber,
    )

    builders.append({
        'name': 'mobile_%s_desktop_build' % platform,
        'slavenames': pf['slaves'],
        'category': 'release',
        'builddir': 'mobile_%s_desktop_build' % platform,
        'factory': build_factory
    })

    if platform in l10nDesktopPlatforms:
        # Not implemented yet
        pass

