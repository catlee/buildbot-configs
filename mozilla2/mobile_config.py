# -*- python -*-
# ex: set syntax=python:

from copy import deepcopy
import re

import config
reload(config)

import buildbotcustom.env
reload(buildbotcustom.env)
from buildbotcustom.env import MozillaEnvironments

OBJDIR = 'objdir'
SBOX_HOME = '/scratchbox/users/cltbld/home/cltbld'

MOBILE_SLAVES = {
    'maemo4': config.SLAVES['linux'],
    'maemo5-gtk': config.SLAVES['linux'],
    'maemo5-qt': config.SLAVES['linux'],
    'linux-i686': config.SLAVES['linux'],
    'macosx-i686': config.SLAVES['macosx'],
    'win32-i686': config.SLAVES['win32'],
    'android-r7': config.SLAVES['linux'],
}

MOBILE_BRANCHES = {
    'mobile-trunk': {},
    'mobile-1.9.2': {},
}

DEFAULT_ENV = {
    'SYMBOL_SERVER_HOST': 'dm-symbolpush01.mozilla.org',
    'SYMBOL_SERVER_USER': 'ffxbld',
    'SYMBOL_SERVER_PATH': '/mnt/netapp/breakpad/symbols_mob/',
    'MOZ_CRASHREPORTER_NO_REPORT': '1',
    'TINDERBOX_OUTPUT': '1',
}
DEFAULT_LINUX_ENV = DEFAULT_ENV.copy()
DEFAULT_LINUX_ENV['SYMBOL_SERVER_SSH_KEY'] = '/home/cltbld/.ssh/ffxbld_dsa'
DEFAULT_MACOSX_ENV = DEFAULT_ENV.copy()
DEFAULT_MACOSX_ENV['SYMBOL_SERVER_SSH_KEY'] = '/Users/cltbld/.ssh/ffxbld_dsa'
DEFAULT_MACOSX_ENV['CHOWN_ROOT'] = '~/bin/chown_root'
DEFAULT_MACOSX_ENV['CHOWN_REVERT'] = '~/bin/chown_revert'
DEFAULT_WIN32_ENV = DEFAULT_ENV.copy()
DEFAULT_WIN32_ENV['SYMBOL_SERVER_SSH_KEY'] = '/c/Documents and Settings/cltbld/.ssh/ffxbld_dsa'

### mozilla-central
MOBILE_BRANCHES['mobile-trunk']['main_config'] = config.BRANCHES['mozilla-central']
MOBILE_BRANCHES['mobile-trunk']['repo_path'] = 'mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['l10n_repo_path'] = 'l10n-central'
MOBILE_BRANCHES['mobile-trunk']['mobile_repo_path'] = 'mobile-browser'
MOBILE_BRANCHES['mobile-trunk']['product_name'] = 'fennec'
MOBILE_BRANCHES['mobile-trunk']['app_name'] = 'mobile'
MOBILE_BRANCHES['mobile-trunk']['aus2_base_upload_dir'] = '/opt/aus2/build/0/{a23983c0-fd0e-11dc-95ff-0800200c9a66}/mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['download_base_url'] = 'http://stage.mozilla.org/pub/mozilla.org/mobile'
MOBILE_BRANCHES['mobile-trunk']['stage_base_path'] = '/home/ftp/pub/mobile'
MOBILE_BRANCHES['mobile-trunk']['mail_on_failure'] = True
MOBILE_BRANCHES['mobile-trunk']['platforms'] = {
    'maemo4': {},
    'linux-i686': {},
    'macosx-i686': {},
    'win32-i686': {},
    'android-r7': {},
}
MOBILE_BRANCHES['mobile-trunk']['l10n_platforms'] = {}
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['mozconfig'] = 'mobile/maemo4/mobile-browser/nightly'
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['sb_target'] = 'CHINOOK-ARMEL-2007'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['mozconfig'] = 'mobile/linux-i686/mobile-browser/nightly'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['mozconfig'] = 'mobile/macosx-i686/mobile-browser/nightly'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['mozconfig'] = 'mobile/win32-i686/mobile-browser/nightly'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['mozconfig'] = 'mobile/android/mobile-browser/nightly'
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['base_upload_dir'] = 'mozilla-central-maemo4'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['base_upload_dir'] = 'mozilla-central-linux'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['base_upload_dir'] = 'mozilla-central-macosx'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['base_upload_dir'] = 'mozilla-central-win32'
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['base_name'] = 'Maemo mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['base_name'] = 'Linux Fennec Desktop mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['base_name'] = 'OS X Fennec Desktop mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['base_name'] = 'Win32 Fennec Desktop mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['base_name'] = 'Android mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['build_space'] = 5
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['build_space'] = 5
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['base_workdir'] = '%s/build/maemo-trunk' % SBOX_HOME
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['base_builddir'] = 'maemo-trunk'
# This base directory is for the individual locales repackaging; it is not for the multi-locale build
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['base_l10n_workdir'] = '%s/build/maemo-trunk-l10n' % SBOX_HOME
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['base_workdir'] = 'build'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['base_builddir'] = 'linux-fennec-trunk'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['base_l10n_workdir'] = 'build/linux-fennec-trunk-l10n'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['base_workdir'] = 'build'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['base_builddir'] = 'macosx-fennec-trunk'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['base_l10n_workdir'] = 'build/macosx-fennec-trunk-l10n'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['base_workdir'] = '.'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['base_builddir'] = 'w32mob-trunk'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['base_l10n_workdir'] = 'w32mob-trunk-l10n'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['base_workdir'] = 'build'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['base_builddir'] = 'android-trunk'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['base_l10n_workdir'] = 'android-trunk-l10n'
MOBILE_BRANCHES['mobile-trunk']['enable_l10n'] = True 
MOBILE_BRANCHES['mobile-trunk']['enable_l10n_onchange'] = False 
MOBILE_BRANCHES['mobile-trunk']['enable_multi_locale'] = True
MOBILE_BRANCHES['mobile-trunk']['l10n_tree'] = 'fennec_mc'
MOBILE_BRANCHES['mobile-trunk']['l10n_platforms']['maemo4'] = 'linux'
MOBILE_BRANCHES['mobile-trunk']['l10n_platforms']['linux-i686'] = 'linux'
#MOBILE_BRANCHES['mobile-trunk']['l10n_platforms']['macosx-i686'] = 'macosx'
MOBILE_BRANCHES['mobile-trunk']['l10n_platforms']['win32-i686'] = 'win32'
#MOBILE_BRANCHES['mobile-trunk']['l10n_platforms']['android-r7'] = 'linux'
MOBILE_BRANCHES['mobile-trunk']['allLocalesFile'] = "locales/all-locales"
MOBILE_BRANCHES['mobile-trunk']['multiLocalesFile'] = "locales/maemo-locales"
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-trunk']['download_base_url'] + '/nightly/latest-mozilla-central-maemo4'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-trunk']['download_base_url'] + '/nightly/latest-mozilla-central-linux'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-trunk']['download_base_url'] + '/nightly/latest-mozilla-central-macosx'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-trunk']['download_base_url'] + '/nightly/latest-mozilla-central-win32'
MOBILE_BRANCHES['mobile-trunk']['tinderbox_tree'] = 'Mobile'
MOBILE_BRANCHES['mobile-trunk']['l10n_tinderbox_tree'] = 'Mozilla-l10n'
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['slaves'] = MOBILE_SLAVES['maemo4']
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['slaves'] = MOBILE_SLAVES['linux-i686']
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['slaves'] = MOBILE_SLAVES['macosx-i686']
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['slaves'] = MOBILE_SLAVES['win32-i686']
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['slaves'] = MOBILE_SLAVES['android-r7']
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['env'] = DEFAULT_LINUX_ENV.copy()
MOBILE_BRANCHES['mobile-trunk']['platforms']['maemo4']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-central-maemo4'
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['env'] = DEFAULT_LINUX_ENV.copy()
MOBILE_BRANCHES['mobile-trunk']['platforms']['linux-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['env'] = DEFAULT_MACOSX_ENV.copy()
MOBILE_BRANCHES['mobile-trunk']['platforms']['macosx-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['env'] = DEFAULT_WIN32_ENV.copy()
MOBILE_BRANCHES['mobile-trunk']['platforms']['win32-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['env'] = DEFAULT_LINUX_ENV.copy()
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-central'
MOBILE_BRANCHES['mobile-trunk']['platforms']['android-r7']['glob_list'] = ['embedding/android/*.apk']

### mobile-1.9.2
MOBILE_BRANCHES['mobile-1.9.2']['main_config'] = config.BRANCHES['mozilla-1.9.2']
MOBILE_BRANCHES['mobile-1.9.2']['repo_path'] = 'releases/mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['l10n_repo_path'] = 'releases/l10n-mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['mobile_repo_path'] = 'releases/mobile-1.1'
MOBILE_BRANCHES['mobile-1.9.2']['product_name'] = 'fennec'
MOBILE_BRANCHES['mobile-1.9.2']['app_name'] = 'mobile'
MOBILE_BRANCHES['mobile-1.9.2']['aus2_base_upload_dir'] = '/opt/aus2/build/0/{a23983c0-fd0e-11dc-95ff-0800200c9a66}/mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['download_base_url'] = 'http://stage.mozilla.org/pub/mozilla.org/mobile'
MOBILE_BRANCHES['mobile-1.9.2']['stage_base_path'] = '/home/ftp/pub/mobile'
MOBILE_BRANCHES['mobile-1.9.2']['mail_on_failure'] = True
MOBILE_BRANCHES['mobile-1.9.2']['platforms'] = {
    'maemo4': {},
    'linux-i686': {},
    'macosx-i686': {},
    'win32-i686': {},
}
MOBILE_BRANCHES['mobile-1.9.2']['l10n_platforms'] = {}
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['mozconfig'] = 'mobile/maemo4/mobile-1.1/nightly'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['sb_target'] = 'CHINOOK-ARMEL-2007'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['mozconfig'] = 'mobile/linux-i686/mobile-1.1/nightly'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['mozconfig'] = 'mobile/macosx-i686/mobile-1.1/nightly'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['mozconfig'] = 'mobile/win32-i686/mobile-1.1/nightly'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['upload_symbols'] = True
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['base_upload_dir'] = 'mozilla-central-maemo4'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['base_upload_dir'] = 'mozilla-central-linux'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['base_upload_dir'] = 'mozilla-central-macosx'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['base_upload_dir'] = 'mozilla-central-win32'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['base_name'] = 'Maemo mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['base_name'] = 'Linux Fennec Desktop mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['base_name'] = 'OS X Fennec Desktop mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['base_name'] = 'Win32 Fennec Desktop mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['build_space'] = 5
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['build_space'] = 5
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['builds_before_reboot'] = 1
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['base_workdir'] = '%s/build/maemo-1.9.2' % SBOX_HOME
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['base_builddir'] = 'maemo-1.9.2'
# This base directory is for the individual locales repackaging; it is not for the multi-locale build
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['base_l10n_workdir'] = '%s/build/maemo-1.9.2-l10n' % SBOX_HOME
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['base_workdir'] = 'build'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['base_builddir'] = 'linux-fennec-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['base_l10n_workdir'] = 'build/linux-fennec-1.9.2-l10n'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['base_workdir'] = 'build'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['base_builddir'] = 'macosx-fennec-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['base_l10n_workdir'] = 'build/macosx-fennec-1.9.2-l10n'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['base_workdir'] = '.'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['base_builddir'] = 'w32mob-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['base_l10n_workdir'] = 'w32mob-1.9.2-l10n'
MOBILE_BRANCHES['mobile-1.9.2']['enable_l10n'] = True 
MOBILE_BRANCHES['mobile-1.9.2']['enable_l10n_onchange'] = False 
MOBILE_BRANCHES['mobile-1.9.2']['enable_multi_locale'] = True
MOBILE_BRANCHES['mobile-1.9.2']['l10n_tree'] = 'fennec11x'
MOBILE_BRANCHES['mobile-1.9.2']['l10n_platforms']['maemo4'] = 'linux'
MOBILE_BRANCHES['mobile-1.9.2']['l10n_platforms']['linux-i686'] = 'linux'
#MOBILE_BRANCHES['mobile-1.9.2']['l10n_platforms']['macosx-i686'] = 'macosx'
MOBILE_BRANCHES['mobile-1.9.2']['l10n_platforms']['win32-i686'] = 'win32'
MOBILE_BRANCHES['mobile-1.9.2']['allLocalesFile'] = "locales/all-locales"
MOBILE_BRANCHES['mobile-1.9.2']['multiLocalesFile'] = "locales/maemo-locales"
MOBILE_BRANCHES['mobile-1.9.2']['tinderbox_tree'] = 'Mobile1.1'
MOBILE_BRANCHES['mobile-1.9.2']['l10n_tinderbox_tree'] = 'Mozilla-l10n'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-1.9.2']['download_base_url'] + '/nightly/latest-mozilla-1.9.2-maemo4'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-1.9.2']['download_base_url'] + '/nightly/latest-mozilla-1.9.2-linux'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-1.9.2']['download_base_url'] + '/nightly/latest-mozilla-1.9.2-macosx'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['enUS_binaryURL'] = \
    MOBILE_BRANCHES['mobile-1.9.2']['download_base_url'] + '/nightly/latest-mozilla-1.9.2-win32'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['slaves'] = MOBILE_SLAVES['maemo4']
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['slaves'] = MOBILE_SLAVES['linux-i686']
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['slaves'] = MOBILE_SLAVES['macosx-i686']
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['slaves'] = MOBILE_SLAVES['win32-i686']
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['env'] = DEFAULT_LINUX_ENV.copy()
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['maemo4']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-1.9.2-maemo4'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['env'] = DEFAULT_LINUX_ENV.copy()
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['linux-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['env'] = DEFAULT_MACOSX_ENV.copy()
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['macosx-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-1.9.2'
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['env'] = DEFAULT_WIN32_ENV.copy()
MOBILE_BRANCHES['mobile-1.9.2']['platforms']['win32-i686']['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = 'mozilla-1.9.2'

#This is needed because we don't use the real branch name as the branch name.
hacktionary = {'mobile-trunk': 'mozilla-central',
               'mobile-1.9.2': 'mozilla-1.9.2',
              }

# Create configs for Maemo5 GTK/QT that are identical to Maemo4 GTK in all
# respects other than:
#  -naming
#  -workdirs
#  -upload location
#  -qt builds use qt mozconfigs
#  -no QT multilocale or l10n until bug 555351 is fixed
for toolkit in ['gtk', 'qt']:
    for branch in MOBILE_BRANCHES.keys():
        if 'qt' in toolkit and '1.9.2' in branch:
                continue
        maemo5 = deepcopy(MOBILE_BRANCHES[branch]['platforms']['maemo4'])
        maemo5['base_name'] = "Maemo 5 %s %s" % (toolkit.upper(),
                                                 hacktionary.get(branch, branch))
        if 'l10n_platforms' in MOBILE_BRANCHES[branch]:
            MOBILE_BRANCHES[branch]['l10n_platforms']['maemo5-%s'%toolkit] = 'linux'
        maemo5['enUS_binaryURL'] = maemo5['enUS_binaryURL'].replace('maemo4', 'maemo5-%s' % toolkit)
        maemo5['mozconfig'] = maemo5['mozconfig'].replace('maemo4', 'maemo5-%s' % toolkit)
        maemo5['base_workdir'] = '%s/build/%s-maemo5-%s' % (SBOX_HOME,
                                                            branch, toolkit)
        maemo5['base_builddir'] = '%s-maemo5-%s' % (branch, toolkit)
        maemo5['base_upload_dir'] = '%s-maemo5-%s' % (hacktionary[branch], toolkit)
        maemo5['env']['MOZ_SYMBOLS_EXTRA_BUILDID'] = '%s-maemo5-%s' % (hacktionary.get(branch, branch), toolkit)
        maemo5['base_l10n_workdir'] = '%s/build/%s-maemo5-%s-l10n' % (SBOX_HOME,
                                                                      branch, toolkit)
        maemo5['sb_target'] = 'FREMANTLE_ARMEL'
        MOBILE_BRANCHES[branch]['platforms']['maemo5-%s'%toolkit] = maemo5

if __name__=="__main__":
    print MOBILE_BRANCHES
