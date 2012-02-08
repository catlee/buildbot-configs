from buildbot.scheduler import Scheduler, Dependent, Triggerable
from buildbot.status.tinderbox import TinderboxMailNotifier

import buildbotcustom.l10n
import buildbotcustom.misc
import buildbotcustom.process.factory

from buildbotcustom.l10n import DependentL10n
from buildbotcustom.misc import get_l10n_repositories, isHgPollerTriggered, \
  generateTestBuilderNames, reallyShort
from buildbotcustom.process.factory import StagingRepositorySetupFactory, \
  ReleaseTaggingFactory, CCSourceFactory, CCReleaseBuildFactory, \
  ReleaseUpdatesFactory, UpdateVerifyFactory, ReleaseFinalVerification, \
  L10nVerifyFactory, CCReleaseRepackFactory, UnittestPackagedBuildFactory, \
  MajorUpdateFactory, TuxedoEntrySubmitterFactory
from buildbotcustom.changes.ftppoller import FtpPoller

# this is where all of our important configuration is stored. build number,
# version number, sign-off revisions, etc.
import release_config
reload(release_config)
from release_config import *

# for the 'build' step we use many of the same vars as the nightlies do.
# we import those so we don't have to duplicate them in release_config
import config as nightly_config

branchConfig = nightly_config.BRANCHES[releaseConfig['sourceRepoName']]

builders = []
test_builders = []
schedulers = []
change_source = []
status = []

def builderPrefix(s, platform=None):
    # sourceRepoName is in release_config and imported into global scope
    if platform:
        return "release-%s-%s_%s" % (releaseConfig['sourceRepoName'], platform, s)
    else:
        return "release-%s-%s" % (releaseConfig['sourceRepoName'], s)

##### Change sources and Schedulers
change_source.append(FtpPoller(
    branch="post_signing",
    ftpURLs=["http://%s/pub/mozilla.org/%s/nightly/%s-candidates/build%s/" \
             % (releaseConfig['stagingServer'], releaseConfig['productName'],
                releaseConfig['version'], releaseConfig['buildNumber'])],
    pollInterval= 60*10,
    searchString='win32_signing_build'
))

tag_scheduler = Scheduler(
    name='tag',
    branch=releaseConfig['sourceRepoPath'],
    treeStableTimer=0,
    builderNames=['tag'],
    fileIsImportant=lambda c: not isHgPollerTriggered(c, branchConfig['hgurl'])
)
schedulers.append(tag_scheduler)
source_scheduler = Dependent(
    name='source',
    upstream=tag_scheduler,
    builderNames=['source']
)
schedulers.append(source_scheduler)
for platform in releaseConfig['enUSPlatforms']:
    build_scheduler = Dependent(
        name='%s_build' % platform,
        upstream=tag_scheduler,
        builderNames=['%s_build' % platform]
    )
    schedulers.append(build_scheduler)
    if platform in releaseConfig['l10nPlatforms']:
        repack_scheduler = DependentL10n(
            name='%s_repack' % platform,
            platform=platform,
            upstream=build_scheduler,
            builderNames=['%s_repack' % platform],
            branch=releaseConfig['sourceRepoPath'],
            baseTag='%s_RELEASE' % baseTag,
            localesFile='suite/locales/shipped-locales',
        )
        schedulers.append(repack_scheduler)

for platform in releaseConfig['l10nPlatforms']:
    l10n_verify_scheduler = Scheduler(
        name='%s_l10n_verification' % platform,
        treeStableTimer=0,
        branch='post_signing',
        builderNames=['%s_l10n_verification' % platform]
    )
    schedulers.append(l10n_verify_scheduler)

updates_scheduler = Scheduler(
    name='updates',
    treeStableTimer=0,
    branch='post_signing',
    builderNames=['updates']
)
schedulers.append(updates_scheduler)

updateBuilderNames = []
for platform in sorted(verifyConfigs.keys()):
    updateBuilderNames.append('%s_update_verify' % platform)
update_verify_scheduler = Dependent(
    name='update_verify',
    upstream=updates_scheduler,
    builderNames=updateBuilderNames
)
schedulers.append(update_verify_scheduler)

if majorUpdateRepoPath:
    majorUpdateBuilderNames = []
    for platform in sorted(majorUpdateVerifyConfigs.keys()):
        majorUpdateBuilderNames.append('%s_major_update_verify' % platform)
    major_update_verify_scheduler = Triggerable(
        name='major_update_verify',
        builderNames=majorUpdateBuilderNames
    )
    schedulers.append(major_update_verify_scheduler)

for platform in unittestPlatforms:
    if branchConfig['platforms'][platform]['enable_opt_unittests']:
        platform_test_builders = []
        base_name = branchConfig['platforms'][platform]['base_name']
        for suites_name, suites in branchConfig['unittest_suites']:
            platform_test_builders.extend(generateTestBuilderNames('%s_test' % platform, suites_name, suites))

        s = Scheduler(
         name='%s_release_unittest' % platform,
         treeStableTimer=0,
         branch='release-%s-%s-opt-unittest' % (releaseConfig['sourceRepoName'], platform),
         builderNames=platform_test_builders,
        )
        schedulers.append(s)

# Purposely, there is not a Scheduler for ReleaseFinalVerification
# This is a step run very shortly before release, and is triggered manually
# from the waterfall

if releaseConfig['productVersionFile']:
  bumpFiles = [releaseConfig['productVersionFile']]
else:
  bumpFiles = []

##### Builders
repositories = {
    releaseConfig['sourceRepoPath']: {
        'revision': releaseConfig['sourceRepoRevision'],
        'relbranchOverride': releaseConfig['relbranchOverride'],
        'bumpFiles': bumpFiles
    },
    releaseConfig['mozillaRepoPath']: {
        'revision': releaseConfig['mozillaRepoRevision'],
        'relbranchOverride': releaseConfig['mozillaRelbranchOverride'],
        'bumpFiles': []
    },
}
if releaseConfig['inspectorRepoPath']:
    repositories[releaseConfig['inspectorRepoPath']] = {
        'revision': releaseConfig['inspectorRepoRevision'],
        'relbranchOverride': releaseConfig['inspectorRelbranchOverride'],
        'bumpFiles': []
    }
if releaseConfig['venkmanRepoPath']:
    repositories[releaseConfig['venkmanRepoPath']] = {
        'revision': releaseConfig['venkmanRepoRevision'],
        'relbranchOverride': releaseConfig['venkmanRelbranchOverride'],
        'bumpFiles': []
    }
if releaseConfig['chatzillaRepoPath']:
    repositories[releaseConfig['chatzillaRepoPath']] = {
        'revision': releaseConfig['chatzillaRepoRevision'],
        'relbranchOverride': releaseConfig['chatzillaRelbranchOverride'],
        'bumpFiles': []
    }

if len(releaseConfig['l10nPlatforms']) > 0:
    l10n_repos = get_l10n_repositories(releaseConfig['l10nRevisionFile'], releaseConfig['l10nRepoPath'],
                                      releaseConfig['l10nRelbranchOverride'])
    repositories.update(l10n_repos)

# dummy factory for TESTING purposes
from buildbot.process.factory import BuildFactory
from buildbot.steps.dummy import Dummy
dummy_factory = BuildFactory()
dummy_factory.addStep(Dummy())

tag_factory = ReleaseTaggingFactory(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    repositories=repositories,
    productName=releaseConfig['productName'],
    appName=releaseConfig['appName'],
    version=releaseConfig['version'],
    appVersion=releaseConfig['appVersion'],
    milestone=releaseConfig['milestone'],
    baseTag=releaseConfig['baseTag'],
    buildNumber=releaseConfig['buildNumber'],
    hgUsername=releaseConfig['hgUsername'],
    hgSshKey=releaseConfig['hgSshKey'],
    relbranchPrefix=releaseConfig['relbranchPrefix'],
    clobberURL=branchConfig['base_clobber_url'],
)

if releaseConfig['skip_tag']:
  tag_factory = dummy_factory

builders.append({
    'name': 'tag',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': builderPrefix('tag'),
    'slavebuilddir': reallyShort(builderPrefix('tag')),
    'factory': tag_factory,
    'properties': {'builddir': builderPrefix('tag'),
                   'slavebuilddir': reallyShort(builderPrefix('tag'))}
})


source_factory = CCSourceFactory(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    repoPath=releaseConfig['sourceRepoPath'],
    productName=releaseConfig['productName'],
    version=releaseConfig['version'],
    baseTag=releaseConfig['baseTag'],
    stagingServer=branchConfig['stage_server'],
    stageUsername=branchConfig['stage_username'],
    stageSshKey=branchConfig['stage_ssh_key'],
    buildNumber=releaseConfig['buildNumber'],
    mozRepoPath=releaseConfig['mozillaRepoPath'],
    inspectorRepoPath=releaseConfig['inspectorRepoPath'],
    venkmanRepoPath=releaseConfig['venkmanRepoPath'],
    chatzillaRepoPath=releaseConfig['chatzillaRepoPath'],
    # Disable cvsroot on comm-central/comm-2.0 builds
    #cvsroot=releaseConfig['cvsroot'],
    autoconfDirs=['.', 'mozilla', 'mozilla/js/src'],
    clobberURL=branchConfig['base_clobber_url'],
)

builders.append({
    'name': 'source',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': builderPrefix('source'),
    'slavebuilddir': reallyShort(builderPrefix('source')),
    'factory': source_factory,
    'properties': {'slavebuilddir': reallyShort(builderPrefix('source'))}
})


for platform in releaseConfig['enUSPlatforms']:
    # shorthand
    pf = branchConfig['platforms'][platform]
    mozconfig = '%s/%s/release' % (platform, releaseConfig['sourceRepoName'])
    l10nmozconfig = '%s/%s/release-l10n' % (platform, releaseConfig['sourceRepoName'])
    if platform in releaseConfig['talosTestPlatforms']:
        talosMasters = branchConfig['talos_masters']
    else:
        talosMasters = None

    if platform in releaseConfig['unittestPlatforms']:
        packageTests = True
        unittestMasters = branchConfig['unittest_masters']
        unittestBranch = 'release-%s-%s-opt-unittest' % (releaseConfig['sourceRepoName'],
                                                         platform)
    else:
        packageTests = False
        unittestMasters = None
        unittestBranch = None

    build_factory = CCReleaseBuildFactory(
        env=pf['env'],
        objdir=pf['platform_objdir'],
        platform=platform,
        hgHost=branchConfig['hghost'],
        repoPath=releaseConfig['sourceRepoPath'],
        mozRepoPath=releaseConfig['mozillaRepoPath'],
        inspectorRepoPath=releaseConfig['inspectorRepoPath'],
        venkmanRepoPath=releaseConfig['venkmanRepoPath'],
        chatzillaRepoPath=releaseConfig['chatzillaRepoPath'],
        # Disable cvsroot on comm-central/comm-2.0 builds
        #cvsroot=releaseConfig['cvsroot'],
        buildToolsRepoPath=branchConfig['build_tools_repo_path'],
        configRepoPath=branchConfig['config_repo_path'],
        configSubDir=branchConfig['config_subdir'],
        profiledBuild=pf['profiled_build'],
        mozconfig=mozconfig,
        buildRevision='%s_RELEASE' % releaseConfig['baseTag'],
        stageServer=branchConfig['stage_server'],
        stageUsername=branchConfig['stage_username'],
        stageGroup=branchConfig['stage_group'],
        stageSshKey=branchConfig['stage_ssh_key'],
        stageBasePath=branchConfig['stage_base_path'],
        codesighs=False,
        uploadPackages=True,
        uploadSymbols=True,
        createSnippet=False,
        doCleanup=True, # this will clean-up the mac build dirs, but not delete
                        # the entire thing
        buildSpace=10,
        productName=releaseConfig['productName'],
        version=releaseConfig['version'],
        buildNumber=releaseConfig['buildNumber'],
        talosMasters=talosMasters,
        packageTests=packageTests,
        unittestMasters=unittestMasters,
        unittestBranch=unittestBranch,
        clobberURL=branchConfig['base_clobber_url'],
    )

    builders.append({
        'name': '%s_build' % platform,
        'slavenames': pf['slaves'],
        'category': 'release',
        'builddir': builderPrefix('%s_build' % platform),
        'slavebuilddir': reallyShort(builderPrefix('%s_build' % platform)),
        'factory': build_factory,
        'properties': {'slavebuilddir': reallyShort(builderPrefix('%s_build' % platform))}
    })

    if platform in releaseConfig['l10nPlatforms']:
        repack_factory = CCReleaseRepackFactory(
            hgHost=branchConfig['hghost'],
            project=releaseConfig['productName'],
            appName=releaseConfig['appName'],
            brandName=releaseConfig['brandName'],
            repoPath=releaseConfig['sourceRepoPath'],
            mozRepoPath=releaseConfig['mozillaRepoPath'],
            inspectorRepoPath=releaseConfig['inspectorRepoPath'],
            venkmanRepoPath=releaseConfig['venkmanRepoPath'],
            chatzillaRepoPath=releaseConfig['chatzillaRepoPath'],
            # Disable cvsroot on comm-central/comm-2.0 builds
            #cvsroot=cvsroot,
            l10nRepoPath=releaseConfig['l10nRepoPath'],
            mergeLocales=releaseConfig['mergeLocales'],
            stageServer=branchConfig['stage_server'],
            stageUsername=branchConfig['stage_username'],
            stageSshKey=branchConfig['stage_ssh_key'],
            buildToolsRepoPath=branchConfig['build_tools_repo_path'],
            compareLocalesRepoPath=branchConfig['compare_locales_repo_path'],
            compareLocalesTag=branchConfig['compare_locales_tag'],
            buildSpace=2,
            configRepoPath=branchConfig['config_repo_path'],
            configSubDir=branchConfig['config_subdir'],
            mozconfig=l10nmozconfig,
            platform=platform + '-release',
            buildRevision='%s_RELEASE' % releaseConfig['baseTag'],
            version=releaseConfig['version'],
            buildNumber=releaseConfig['buildNumber'],
            tree='release',
            clobberURL=branchConfig['base_clobber_url'],
        )

        builders.append({
            'name': '%s_repack' % platform,
            'slavenames': branchConfig['l10n_slaves'][platform],
            'category': 'release',
            'builddir': builderPrefix('%s_repack' % platform),
            'slavebuilddir': reallyShort(builderPrefix('%s_repack' % platform)),
            'factory': repack_factory,
            'properties': {'slavebuilddir': reallyShort(builderPrefix('%s_repack' % platform))}
        })

    if pf['enable_opt_unittests']:
        mochitestLeakThreshold = pf.get('mochitest_leak_threshold', None)
        crashtestLeakThreshold = pf.get('crashtest_leak_threshold', None)
        for suites_name, suites in branchConfig['unittest_suites']:
            # Release builds on mac don't have a11y enabled, do disable the mochitest-a11y test
            if platform.startswith('macosx') and 'mochitest-a11y' in suites:
                suites = suites[:]
                suites.remove('mochitest-a11y')

            test_builders.extend(generateTestBuilder(
                branchConfig, 'release', platform, "%s_test" % platform,
                'release-%s-%s-opt-unittest' % (sourceRepoName, platform),
                suites_name, suites, mochitestLeakThreshold,
                crashtestLeakThreshold))

for platform in releaseConfig['l10nPlatforms']:
    l10n_verification_factory = L10nVerifyFactory(
        hgHost=branchConfig['hghost'],
        buildToolsRepoPath=branchConfig['build_tools_repo_path'],
        cvsroot=releaseConfig['cvsroot'],
        stagingServer=releaseConfig['stagingServer'],
        productName=releaseConfig['productName'],
        version=releaseConfig['version'],
        buildNumber=releaseConfig['buildNumber'],
        oldVersion=releaseConfig['oldVersion'],
        oldBuildNumber=releaseConfig['oldBuildNumber'],
        clobberURL=branchConfig['base_clobber_url'],
        platform=platform,
    )

    verifySlavePlat = 'macosx64'
    if sourceRepoName == 'comm-1.9.1':
       verifySlavePlat = 'macosx'

    builders.append({
        'name': '%s_l10n_verification' % platform,
        'slavenames': branchConfig['platforms'][verifySlavePlat]['slaves'],
        'category': 'release',
        'builddir': builderPrefix('%s_l10n_verification' % platform),
        'slavebuilddir': reallyShort(builderPrefix('%s_l10n_verification' % platform)),
        'factory': l10n_verification_factory,
        'properties': {'slavebuilddir': reallyShort(builderPrefix('%s_l10n_verification' % platform))}
    })

updates_factory = ReleaseUpdatesFactory(
    hgHost=branchConfig['hghost'],
    repoPath=releaseConfig['sourceRepoPath'],
    mozRepoPath=releaseConfig['mozillaRepoPath'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    cvsroot=releaseConfig['cvsroot'],
    patcherToolsTag=releaseConfig['patcherToolsTag'],
    patcherConfig=releaseConfig['patcherConfig'],
    verifyConfigs=releaseConfig['verifyConfigs'],
    appName=releaseConfig['appName'],
    productName=releaseConfig['productName'],
    brandName=releaseConfig['brandName'],
    version=releaseConfig['version'],
    appVersion=releaseConfig['appVersion'],
    baseTag=releaseConfig['baseTag'],
    buildNumber=releaseConfig['buildNumber'],
    oldVersion=releaseConfig['oldVersion'],
    oldAppVersion=releaseConfig['oldAppVersion'],
    oldBaseTag=releaseConfig['oldBaseTag'],
    oldBuildNumber=releaseConfig['oldBuildNumber'],
    ftpServer=releaseConfig['ftpServer'],
    bouncerServer=releaseConfig['bouncerServer'],
    stagingServer=releaseConfig['stagingServer'],
    useBetaChannel=releaseConfig['useBetaChannel'],
    stageUsername=branchConfig['stage_username'],
    stageSshKey=branchConfig['stage_ssh_key'],
    ausUser=branchConfig['aus2_user'],
    ausSshKey=branchConfig['aus2_ssh_key'],
    ausHost=branchConfig['aus2_host'],
    ausServerUrl=releaseConfig['ausServerUrl'],
    hgSshKey=releaseConfig['hgSshKey'],
    hgUsername=releaseConfig['hgUsername'],
    clobberURL=branchConfig['base_clobber_url'],
    oldRepoPath=releaseConfig['oldRepoPath'],
    releaseNotesUrl=releaseConfig['releaseNotesUrl'],
    binaryName=releaseConfig['binaryName'],
    oldBinaryName=releaseConfig['oldBinaryName'],
    testOlderPartials=releaseConfig['testOlderPartials'],
    schema=releaseConfig.get("snippetSchema", 1), # Bug 682805
)

builders.append({
    'name': 'updates',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': builderPrefix('updates'),
    'slavebuilddir': reallyShort(builderPrefix('updates')),
    'factory': updates_factory,
    'properties': {'slavebuilddir': reallyShort(builderPrefix('updates'))}
})


for platform in sorted(releaseConfig['verifyConfigs'].keys()):
    update_verify_factory = UpdateVerifyFactory(
        hgHost=branchConfig['hghost'],
        buildToolsRepoPath=branchConfig['build_tools_repo_path'],
        verifyConfig=releaseConfig['verifyConfigs'][platform],
        clobberURL=branchConfig['base_clobber_url'],
        useOldUpdater=branchConfig.get('use_old_updater', False),
    )

    builders.append({
        'name': '%s_update_verify' % platform,
        'slavenames': branchConfig['platforms'][platform]['slaves'],
        'category': 'release',
        'builddir': builderPrefix('%s_update_verify' % platform),
        'slavebuilddir': reallyShort(builderPrefix('%s_update_verify' % platform)),
        'factory': update_verify_factory,
        'properties': {'slavebuilddir': reallyShort(builderPrefix('%s_update_verify' % platform))}
    })


final_verification_factory = ReleaseFinalVerification(
    hgHost=branchConfig['hghost'],
    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
    verifyConfigs=releaseConfig['verifyConfigs'],
    clobberURL=branchConfig['base_clobber_url'],
)

builders.append({
    'name': 'final_verification',
    'slavenames': branchConfig['platforms']['linux']['slaves'],
    'category': 'release',
    'builddir': builderPrefix('final_verification'),
    'slavebuilddir': reallyShort(builderPrefix('final_verification')),
    'factory': final_verification_factory,
    'properties': {'slavebuilddir': reallyShort(builderPrefix('final_verification'))}
})

if releaseConfig['majorUpdateRepoPath']:
    # Not attached to any Scheduler
    major_update_factory = MajorUpdateFactory(
        hgHost=branchConfig['hghost'],
        repoPath=releaseConfig['majorUpdateSourceRepoPath'],
        mozRepoPath=releaseConfig['majorUpdateRepoPath'],
        buildToolsRepoPath=branchConfig['build_tools_repo_path'],
        cvsroot=releaseConfig['cvsroot'],
        patcherToolsTag=releaseConfig['majorPatcherToolsTag'],
        patcherConfig=releaseConfig['majorUpdatePatcherConfig'],
        verifyConfigs=releaseConfig['majorUpdateVerifyConfigs'],
        appName=releaseConfig['appName'],
        productName=releaseConfig['productName'],
        brandName=releaseConfig['brandName'],
        version=releaseConfig['majorUpdateToVersion'],
        appVersion=releaseConfig['majorUpdateAppVersion'],
        baseTag=releaseConfig['majorUpdateBaseTag'],
        buildNumber=releaseConfig['majorUpdateBuildNumber'],
        oldVersion=releaseConfig['version'],
        oldAppVersion=releaseConfig['appVersion'],
        oldBaseTag=releaseConfig['baseTag'],
        oldBuildNumber=releaseConfig['buildNumber'],
        ftpServer=releaseConfig['ftpServer'],
        bouncerServer=releaseConfig['bouncerServer'],
        stagingServer=releaseConfig['stagingServer'],
        useBetaChannel=releaseConfig['useBetaChannel'],
        stageUsername=branchConfig['stage_username'],
        stageSshKey=branchConfig['stage_ssh_key'],
        ausUser=branchConfig['aus2_user'],
        ausSshKey=branchConfig['aus2_ssh_key'],
        ausHost=branchConfig['aus2_host'],
        ausServerUrl=releaseConfig['ausServerUrl'],
        hgSshKey=releaseConfig['hgSshKey'],
        hgUsername=releaseConfig['hgUsername'],
        clobberURL=branchConfig['base_clobber_url'],
        oldRepoPath=releaseConfig['oldRepoPath'],
        triggerSchedulers=['major_update_verify'],
        releaseNotesUrl=releaseConfig['majorUpdateReleaseNotesUrl'],
        testOlderPartials=releaseConfig['testOlderPartials'],
        schema=releaseConfig.get("majorSnippetSchema", 1), # Bug 682805
    )

    builders.append({
        'name': 'major_update',
        'slavenames': branchConfig['platforms']['linux']['slaves'],
        'category': 'release',
        'builddir': builderPrefix('major_update'),
        'slavebuilddir': reallyShort(builderPrefix('major_update')),
        'factory': major_update_factory,
        'properties': {'slavebuilddir': reallyShort(builderPrefix('major_update'))}
    })

    for platform in sorted(releaseConfig['majorUpdateVerifyConfigs'].keys()):
        major_update_verify_factory = UpdateVerifyFactory(
            hgHost=branchConfig['hghost'],
            buildToolsRepoPath=branchConfig['build_tools_repo_path'],
            verifyConfig=releaseConfig['majorUpdateVerifyConfigs'][platform],
            clobberURL=branchConfig['base_clobber_url'],
        )

        builders.append({
            'name': '%s_major_update_verify' % platform,
            'slavenames': branchConfig['platforms'][platform]['slaves'],
            'category': 'release',
            'builddir': builderPrefix('%s_major_update_verify' % platform),
            'slavebuilddir': reallyShort(builderPrefix('%s_major_update_verify' % platform)),
            'factory': major_update_verify_factory,
            'properties': {'slavebuilddir': reallyShort(builderPrefix('%s_major_update_verify' % platform))}
        })

# XXX: SeaMonkey atm doesn't have permission to use this :(
#bouncer_submitter_factory = TuxedoEntrySubmitterFactory(
#    baseTag=releaseConfig['baseTag'],
#    appName=releaseConfig['appName'],
#    config=releaseConfig['tuxedoConfig'],
#    productName=releaseConfig['productName'],
#    version=releaseConfig['version'],
#    milestone=releaseConfig['milestone'],
#    tuxedoServerUrl=releaseConfig['tuxedoServerUrl'],
#    enUSPlatforms=releaseConfig['enUSPlatforms'],
#    l10nPlatforms=releaseConfig['l10nPlatforms'],
#    oldVersion=releaseConfig['oldVersion'],
#    hgHost=branchConfig['hghost'],
#    repoPath=releaseConfig['sourceRepoPath'],
#    buildToolsRepoPath=branchConfig['build_tools_repo_path'],
#    credentialsFile=os.path.join(os.getcwd(), "BuildSlaves.py"),
#)

#builders.append({
#    'name': 'bouncer_submitter',
#    'slavenames': branchConfig['platforms']['linux']['slaves'],
#    'category': 'release',
#    'builddir': 'bouncer_submitter',
#    'factory': bouncer_submitter_factory
#})

status.append(TinderboxMailNotifier(
    fromaddr="comm.buildbot@build.mozilla.org",
    tree=branchConfig["tinderbox_tree"] + "-Release",
    extraRecipients=["tinderbox-daemon@tinderbox.mozilla.org",],
    relayhost="mail.build.mozilla.org",
    builders=[b['name'] for b in builders],
    logCompression="bzip2")
)

status.append(TinderboxMailNotifier(
    fromaddr="comm.buildbot@build.mozilla.org",
    tree=branchConfig["tinderbox_tree"] + "-Release",
    extraRecipients=["tinderbox-daemon@tinderbox.mozilla.org",],
    relayhost="mail.build.mozilla.org",
    builders=[b['name'] for b in test_builders],
    logCompression="bzip2",
    errorparser="unittest")
)

builders.extend(test_builders)
